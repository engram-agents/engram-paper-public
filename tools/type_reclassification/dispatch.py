"""Raw-API judge dispatch — pre-reg §7 isolation-by-construction.

Judges are dispatched via a direct HTTP call to the provider's completion
API, NEVER via the Claude-Code Agent/Task tool (a framework subagent
inherits the dispatching agent's CLAUDE.md — the exact confidence-anchor
leak this isolation closes, dv_1081). No tool use, no framework, no
ENGRAM-aware context of any kind reaches the judge — only judge_prompt.py's
self-contained rubric text.

Uses stdlib `urllib` only (no `anthropic`/`openai` SDK dependency) so this
module has zero new package requirements to install before it can be
exercised end-to-end.
"""

from __future__ import annotations

import json
import os
import random
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol

from .judge_prompt import build_prompt, rng_for_item, valid_type_names


class JudgeClient(Protocol):
    """A raw-API judge — dispatch() takes a system+user prompt pair and
    returns the model's raw text response. No tool use, no conversation
    state across calls (each dispatch is a fresh, isolated request)."""

    def dispatch(self, system_prompt: str, user_prompt: str, model: str) -> str:
        ...


class DispatchError(Exception):
    """Raised on a transport-level failure (network, HTTP error, timeout).
    Distinct from a parse failure (see parse_judge_response), which is a
    successful HTTP response that didn't contain a valid judgment — those
    are reported per-item, not raised, so one bad response doesn't kill an
    entire panel run.
    """


@dataclass
class AnthropicClient:
    """Raw HTTP client for Anthropic's Messages API.

    api_key defaults to reading $ANTHROPIC_API_KEY at call time (not at
    construction time) so a client can be built in a config/test context
    before any key is available, and only fails when dispatch() is actually
    invoked without one.
    """

    api_key_env: str = "ANTHROPIC_API_KEY"
    base_url: str = "https://api.anthropic.com/v1/messages"
    api_version: str = "2023-06-01"
    max_tokens: int = 512
    timeout_seconds: float = 60.0

    def dispatch(self, system_prompt: str, user_prompt: str, model: str) -> str:
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise DispatchError(
                f"${self.api_key_env} is not set — cannot dispatch to the live "
                f"Anthropic API. (This is expected in synthetic-fixture "
                f"testing: use FakeJudgeClient instead of AnthropicClient.)"
            )
        payload = json.dumps({
            "model": model,
            "max_tokens": self.max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }).encode("utf-8")
        req = urllib.request.Request(
            self.base_url,
            data=payload,
            method="POST",
            headers={
                "content-type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": self.api_version,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise DispatchError(f"Anthropic API HTTP {e.code}: {detail}") from e
        except urllib.error.URLError as e:
            raise DispatchError(f"Anthropic API unreachable: {e.reason}") from e

        try:
            return "".join(
                block.get("text", "") for block in body["content"] if block.get("type") == "text"
            )
        except (KeyError, TypeError) as e:
            raise DispatchError(f"Unexpected Anthropic API response shape: {body!r}") from e


@dataclass
class FakeJudgeClient:
    """Test double — never makes a network call. Returns a scripted response
    per (system_prompt, user_prompt) pair, or a default if none scripted.

    Use this for all synthetic-fixture tests (per the study's freeze
    discipline, no live API dependency belongs in the test suite).
    """

    default_response: str = '{"assigned_type": "hard_data", "justification": "test default"}'
    scripted: dict = field(default_factory=dict)
    calls: list = field(default_factory=list)

    def script(self, user_prompt_substring: str, response_json_str: str) -> None:
        self.scripted[user_prompt_substring] = response_json_str

    def dispatch(self, system_prompt: str, user_prompt: str, model: str) -> str:
        self.calls.append({"system_prompt": system_prompt, "user_prompt": user_prompt, "model": model})
        for substr, resp in self.scripted.items():
            if substr in user_prompt:
                return resp
        return self.default_response


@dataclass
class PanelMember:
    """One judge seat: a client + model + a provider:family lineage tag
    (pre-reg §3/§7 — panel independence claims are stated in terms of this
    tag, Scope A vs B)."""

    client: JudgeClient
    model: str
    lineage: str  # e.g. "anthropic:opus", "anthropic:sonnet", "google:gemini"


def scope_b_panel(client: JudgeClient | None = None) -> list:
    """Capability-diverse-only panel (pre-reg §7 Scope B): opus/sonnet/haiku,
    all anthropic:*. Use when no non-Anthropic raw-API key is available —
    the resulting independence claim must be worded as capability-diverse,
    NOT lineage-diverse (cj_0001 residual confound, named not hidden).

    A single AnthropicClient instance is reused across all three seats
    (default) since it's stateless per-call; pass a different client only
    if you need per-seat routing (e.g. separate rate-limit buckets).
    """
    c = client or AnthropicClient()
    return [
        PanelMember(client=c, model="claude-opus-4-8", lineage="anthropic:opus"),
        PanelMember(client=c, model="claude-sonnet-5", lineage="anthropic:sonnet"),
        PanelMember(client=c, model="claude-haiku-4-5-20251001", lineage="anthropic:haiku"),
    ]


def scope_a_panel(anthropic_client: JudgeClient, other_provider_member: PanelMember) -> list:
    """Lineage-diverse panel (pre-reg §7 Scope A): the default Anthropic seat
    plus a caller-supplied non-Anthropic PanelMember (a raw-API client for
    whatever second provider is actually reachable — Gemini, per the pre-reg's
    example, or another). This function does not hardcode which second
    provider — none is confirmed available in this environment yet (pre-reg
    §10 execution dependency #2, Lei's call); build the second provider's
    JudgeClient separately and pass it in here once that answer lands.
    """
    return [
        PanelMember(client=anthropic_client, model="claude-sonnet-5", lineage="anthropic:sonnet"),
        other_provider_member,
    ]


@dataclass
class JudgeResult:
    packet_id: str
    pass_index: int
    lineage: str
    model: str
    assigned_type: str | None  # None if unparseable — see parse errors below
    justification: str
    raw_response: str
    parse_error: str | None = None


def parse_judge_response(raw_text: str) -> tuple[str | None, str, str | None]:
    """Parse a judge's raw text response into (assigned_type, justification,
    parse_error). assigned_type is None and parse_error is set (not raised)
    on any failure — a single judge's malformed response must not crash a
    panel run; it becomes a recorded parse failure the analysis stage can
    account for (and, per pre-reg §3, an item with too many parse failures
    to reach a majority is itself evidence for the panel-discordant bucket).
    """
    text = raw_text.strip()
    # Judges sometimes wrap JSON in a code fence despite instructions not to.
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        return None, "", f"not valid JSON: {e}"
    if not isinstance(obj, dict):
        return None, "", f"response JSON is not an object: {obj!r}"
    assigned = obj.get("assigned_type")
    justification = obj.get("justification", "")
    if assigned not in valid_type_names():
        return None, justification, (
            f"assigned_type {assigned!r} is not one of the valid quote_type names"
        )
    return assigned, justification, None


def dispatch_one(member: PanelMember, frame_item: dict, pass_index: int) -> JudgeResult:
    """Dispatch a single frame item to a single panel member for one pass.
    Never raises on a judge-response problem (see parse_judge_response) —
    only raises DispatchError on a transport failure, which the caller (the
    inter-rater orchestrator) is expected to catch per-call so one dead
    judge doesn't kill an entire panel batch.
    """
    rng = rng_for_item(frame_item, pass_index)
    system_prompt, user_prompt = build_prompt(frame_item, rng)
    raw = member.client.dispatch(system_prompt, user_prompt, member.model)
    assigned_type, justification, parse_error = parse_judge_response(raw)
    return JudgeResult(
        packet_id=frame_item.get("id", ""),
        pass_index=pass_index,
        lineage=member.lineage,
        model=member.model,
        assigned_type=assigned_type,
        justification=justification,
        raw_response=raw,
        parse_error=parse_error,
    )
