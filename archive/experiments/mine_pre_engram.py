#!/usr/bin/env python3
"""Mine pre-ENGRAM Claude.ai history for ideation-relevant moments.

Conversations are stored in conversations.json as a list of dicts with
chat_messages. This tool provides three operations:
  list     — print all conversations sorted by created_at (uuid, name, count, date)
  search   — search messages for a keyword, return matches with snippets
  extract  — dump full text of a conversation by uuid (for digest building)
"""
from __future__ import annotations
import json, sys, re, os
from pathlib import Path

ROOT = Path("/home/agents-shared/Pre-ENGRAM-Lei-Claude-History/data-d92d3721-b624-4377-a0d0-456893a499cf-1778285467-5ff6c2ff-batch-0000")
CONV_PATH = ROOT / "conversations.json"

def load():
    with open(CONV_PATH) as f:
        return json.load(f)

def cmd_list(_args):
    convs = load()
    convs.sort(key=lambda c: c.get("created_at", ""))
    for c in convs:
        n = len(c.get("chat_messages", []))
        date = (c.get("created_at") or "")[:10]
        name = (c.get("name") or "")[:80]
        print(f"{date}  msgs={n:4d}  {c['uuid']}  {name}")

def cmd_search(args):
    if not args:
        print("usage: search <keyword>", file=sys.stderr); sys.exit(2)
    needle = args[0].lower()
    convs = load()
    convs.sort(key=lambda c: c.get("created_at", ""))
    total_hits = 0
    for c in convs:
        cdate = (c.get("created_at") or "")[:10]
        cname = (c.get("name") or "")[:60]
        for i, m in enumerate(c.get("chat_messages", [])):
            text = (m.get("text") or "")
            if not text:
                # try content blocks
                for block in (m.get("content") or []):
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = (text + "\n" + block.get("text", "")).strip()
            if needle in text.lower():
                total_hits += 1
                # find the matching span and print a small window
                idx = text.lower().find(needle)
                start = max(0, idx - 80)
                end   = min(len(text), idx + 200)
                snippet = text[start:end].replace("\n", " ")
                snippet = re.sub(r"\s+", " ", snippet)
                sender = m.get("sender", "?")
                msg_date = (m.get("created_at") or "")[:19]
                print(f"{msg_date} [{sender}] {c['uuid'][:8]}/{m['uuid'][:8]} (msg #{i+1}/{len(c['chat_messages'])}) {cname}")
                print(f"    ...{snippet}...")
    print(f"\n{total_hits} matches across {len(convs)} conversations.", file=sys.stderr)

def cmd_extract(args):
    if not args:
        print("usage: extract <conv_uuid_prefix> [outfile]", file=sys.stderr); sys.exit(2)
    prefix = args[0]
    out_path = args[1] if len(args) > 1 else None
    convs = load()
    matched = [c for c in convs if c["uuid"].startswith(prefix)]
    if not matched:
        print(f"no match for {prefix}", file=sys.stderr); sys.exit(1)
    if len(matched) > 1:
        print(f"{len(matched)} matches; be more specific:", file=sys.stderr)
        for c in matched: print(f"  {c['uuid']} {c.get('name','')}", file=sys.stderr)
        sys.exit(2)
    c = matched[0]
    out = []
    out.append(f"# {c.get('name')}\n")
    out.append(f"**UUID:** {c['uuid']}")
    out.append(f"**Created:** {c.get('created_at','')}")
    out.append(f"**Updated:** {c.get('updated_at','')}")
    out.append(f"**Messages:** {len(c.get('chat_messages',[]))}\n")
    out.append("## Summary\n")
    out.append(c.get("summary","") + "\n")
    out.append("## Messages\n")
    for i, m in enumerate(c.get("chat_messages", []), 1):
        sender = m.get("sender", "?")
        date = (m.get("created_at") or "")[:19]
        text = m.get("text") or ""
        if not text:
            for block in (m.get("content") or []):
                if isinstance(block, dict) and block.get("type") == "text":
                    text = (text + "\n" + block.get("text", "")).strip()
        out.append(f"### #{i} [{sender}] {date}  msg-uuid:{m['uuid']}\n")
        out.append(text or "(no text)")
        out.append("")
    text = "\n".join(out)
    if out_path:
        Path(out_path).write_text(text)
        print(f"wrote {out_path}: {len(text)} chars, {len(c.get('chat_messages',[]))} messages", file=sys.stderr)
    else:
        print(text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    cmd, args = sys.argv[1], sys.argv[2:]
    {"list": cmd_list, "search": cmd_search, "extract": cmd_extract}.get(cmd, lambda _: (print("unknown cmd"), sys.exit(2)))(args)
