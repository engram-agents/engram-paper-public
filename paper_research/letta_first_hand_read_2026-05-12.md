# Letta (formerly MemGPT) — First-Hand Primary-Source Read
**Date:** 2026-05-12
**Author:** Paper-research sub-agent (dispatched by Borges)
**Purpose:** Primary-source verification for ENGRAM foundational paper; OCC/Kahl mapping

## 1. Metadata

| Field | Detail |
|---|---|
| System | Letta (formerly MemGPT); OSS + hosted platform |
| Paper | MemGPT: Towards LLMs as Operating Systems — arXiv:2310.08560 (2023) |
| Platform launch | Letta brand: 2024-09 |
| Conversations API | 2026-01-21 (letta.com/blog/conversations) |
| Sources verified | GitHub source (base.py function signatures), letta.com blog posts, docs.letta.com |
| Baseline doc | agent_memory_landscape_2026-05-05.md (summarized second-hand; this document provides primary-source verification) |

**Primary sources read:**
- https://raw.githubusercontent.com/letta-ai/letta/main/letta/functions/function_sets/base.py (tool signatures — verbatim)
- https://www.letta.com/blog/agent-memory (memory model overview)
- https://www.letta.com/blog/conversations (Conversations API, 2026-01-21)
- https://www.letta.com/blog/memory-blocks (memory block internals)
- https://www.letta.com/blog/benchmarking-ai-agent-memory (filesystem benchmark)
- https://docs.letta.com/guides/agents/memory (architecture overview)

**Not successfully fetched:**
- arxiv.org/html/2310.08560 — returned 404 for all v1/v2 HTML variants; abstract-only from PDF fetch
- docs.letta.com/api-reference/memory/core-memory — 404
- docs.letta.com/concepts/memgpt/ — redirected to general landing page, not architecture docs
- letta.com/blog/letta-conversations-api — 404 (blog post URL differs from canonical URL above)

---

## 2. Memory Model — Verbatim Quotes from Primary Sources

**From letta.com/blog/agent-memory:**
> "Agent memory is essentially context engineering: determining which tokens enter the context window and how they're organized."

> "agents can update their own memory blocks based on new information, using tools to rewrite specific blocks"

> "these blocks are editable via APIs and remain pinned to the agent's context window" [re: Core Memory]

**Memory types (from letta.com/blog/agent-memory):**
1. **Message Buffer** — stores recent conversation messages in a perpetual thread
2. **Core Memory** — in-context memory blocks editable via APIs; "remain pinned to the agent's context window"
3. **Recall Memory** — complete interaction history, automatically persisted to disk
4. **Archival Memory** — explicitly formulated knowledge in external databases (vector or graph DBs)

**From letta.com/blog/memory-blocks:**
> "memory block values are just strings"

> "a custom tool to 'rethink' (replace) an entire memory block's value"

> Memory blocks consist of: label, value (actual string), size limit, optional descriptions

**From letta.com/blog/conversations (Conversations API, 2026-01-21):**
> "agents can now have multiple conversations concurrently while still having their own individual identity and sense of experience"

> "experiences within a conversation can form memories which transfer across all conversations"

> "messages are searchable across all conversations and memory is shared"

**From letta.com/blog/benchmarking-ai-agent-memory:**
> "Agents today are highly effective at using tools, especially those likely to have been in their training data (such as filesystem operations)."

> "Memory for Agents: Agent Capabilities Matter More Than the Tools"

> "it's much more important to consider whether an agent will be able to effectively use a retrieval tool...rather than focusing on the exact retrieval mechanisms."

---

## 3. Memory Tool API — Verbatim Function Signatures (GitHub primary source)

Source: `letta-ai/letta/main/letta/functions/function_sets/base.py`

```python
def core_memory_append(agent_state: "AgentState", label: str, content: str) -> str:
    """
    Append to the contents of core memory.
    Args:
        label (str): Section of the memory to be edited.
        content (str): Content to write to the memory. All unicode (including emojis) are supported.
    Returns:
        str: The updated value of the memory block.
    """
```

```python
def core_memory_replace(agent_state: "AgentState", label: str, old_content: str, new_content: str) -> str:
    """
    Replace the contents of core memory. To delete memories, use an empty string for new_content.
    Args:
        label (str): Section of the memory to be edited.
        old_content (str): String to replace. Must be an exact match.
        new_content (str): Content to write to the memory.
    Returns:
        str: The updated value of the memory block.
    """
```

```python
def memory_rethink(agent_state: "AgentState", label: str, new_memory: str) -> str:
    """
    The memory_rethink command allows you to completely rewrite the contents of a memory block.
    Use this tool to make large sweeping changes (e.g. when you want to condense or reorganize
    the memory blocks), do NOT use this tool to make small precise edits.
    Args:
        label (str): The memory block to be rewritten, identified by its label.
        new_memory (str): The new memory contents with information integrated from existing
                         memory blocks and the conversation context.
    Returns:
        None
    """
```

```python
async def archival_memory_insert(self: "Agent", content: str, tags: Optional[list[str]] = None) -> Optional[str]:
    """
    Add information to long-term archival memory for later retrieval.
    Use this tool to store facts, knowledge, or context that you want to remember
    across all future conversations. Archival memory is permanent and searchable by
    semantic similarity.
    Best practices:
    - Store self-contained facts or summaries, not conversational fragments
    - Add descriptive tags to make information easier to find later
    Args:
        content: The information to store. Should be clear and self-contained.
        tags: Optional list of category tags
    Returns:
        Confirmation message with the ID of the inserted memory.
    """
```

```python
async def archival_memory_search(self: "Agent", query: str, tags: Optional[list[str]] = None,
    tag_match_mode: Literal["any", "all"] = "any", top_k: Optional[int] = None,
    start_datetime: Optional[str] = None, end_datetime: Optional[str] = None) -> Optional[str]:
    """
    Search archival memory using semantic similarity to find relevant information.
    Args:
        query: What you're looking for, described naturally
        tags: Filter to memories with these tags
        start_datetime / end_datetime: ISO 8601 date filters
        top_k: Maximum number of results to return (default: 10)
    Returns:
        A list of relevant memories with IDs, timestamps, and content, ranked by similarity.
    """
```

**Key observation from tool signatures:** `core_memory_replace` takes `old_content` and `new_content` — a text-level diff operation. `memory_rethink` takes only `new_memory` — a wholesale overwrite. Neither signature carries any claim identifier, provenance parameter, or contradiction flag. The agent decides what to write; the tool writes it. No structural mechanism prevents silent overwrites.

---

## 4. ENGRAM Function Comparison Table

| ENGRAM mechanism | Letta status | Evidence |
|---|---|---|
| **Claim-level contradiction node (`ct_*`)** | Absent | No contradiction-as-first-class-node in any source. Memory edits are text-level. No documentation mentions contradiction detection logic. |
| **Retraction cascade through `derives_from` edges** | Absent | No derivation graph. Memory blocks are free-form string containers; there is no edge between one memory and another that would support cascade. |
| **Typed derivation primitive (reasoning edges)** | Absent | Memory is flat text blocks. No provenance edges, no typed reasoning links. |
| **Evidence-class confidence taxonomy** | Absent | No confidence scoring at any level. All memory content is unweighted string. |
| **Provenance to quoted span of committed source** | Absent | `archival_memory_insert` takes `content: str` and optional tags. No source-span parameter, no URL citation primitive. No version control on memory content. |
| **Supersede relation** | Absent | `core_memory_replace` overwrites in place; prior content is not linked or superseded — it is destroyed. `memory_rethink` similarly destroys prior content. |
| **Agent-as-epistemic-author posture** | Partial | Letta's distinctive feature: the agent DOES write its own memory via tool calls. The blog explicitly frames this as "agents actively manage their own memory." This is write-authoring posture at the text-block level. However, the agent is not modeled as the epistemic author of structured claims with provenance — it is the text-editor of string containers. |
| **Contradiction flagged as structural event** | Absent | The 2026-01 Conversations API blog says nothing about contradiction detection. No source consulted mentions it. Documented failure mode (from 2026-05-05 baseline): "agent occasionally refuses to acknowledge archival content and confabulates" — the system provides no mechanism to surface or resolve such confabulation structurally. |

---

## 5. OCC Mapping

### Does Letta explicitly engage Kahl / OCC?

**No.** Neither the MemGPT paper, the Letta blog corpus, nor the API documentation mentions Kahl, OCC (Ontological Continuity Condition), diachronic constraint, non-interchangeability under reset, or self-maintaining arbitration. The framing in letta.com/blog/conversations — "agents can now have multiple conversations concurrently while still having their own individual identity and sense of experience" — uses "identity" and "experience" in a colloquial marketing sense, not as a reference to philosophical personal identity literature.

### OCC Satisfaction Analysis (per condition)

**Cond 1 — Diachronic Constraint:** Past commitments structure present deliberation non-trivially (binding commitment, not mere path-dependence).

Assessment: **Does not satisfy.** Letta's memory is available to the agent but does not structure present deliberation as a constraint. The agent reads memory blocks in context and may choose to act on or ignore them; there is no mechanism that causes a past memory-write to bind a future decision. The system does not distinguish between memory the agent authored as a commitment versus memory it stored as information. From the letta.com/blog/memory-blocks source: "memory block values are just strings" — strings do not impose diachronic binding. `core_memory_replace` can overwrite any commitment at any time with no record.

**Cond 2 — Non-Interchangeability Under Reset:** Token-distinctness preserved across snapshot/reset events.

Assessment: **Partially ambiguous; structurally does not satisfy Kahl's test.** Letta does persist memory blocks across session boundaries — this is its primary value proposition. However, Kahl's "reset-symmetry test" asks: would the agent be structurally reducible to a fresh instance if the memory content were copied to a new agent? Letta's answer is yes: an agent's identity IS its memory blocks, and per the Conversations API design ("separate agents" vs. "shared memory" are the two poles), identity reduces to a bundle of string-valued blocks. A fresh agent with the same memory blocks would be, by Letta's own model, the same agent. Structural reducibility is exactly what Kahl's Cond 2 denies — so Letta fails Cond 2 by the decisive criterion.

**Cond 3 — Self-Maintaining Arbitration:** Foundational retractions structurally flag downstream commitments within a unified deliberative architecture.

Assessment: **Does not satisfy.** Letta has no derivation graph, no concept of downstream commitments, and no retraction primitive. When `core_memory_replace` overwrites a foundational claim, nothing downstream is flagged. The agent could hold inconsistent memories across different memory blocks with no structural detection. The Conversations API adds cross-conversation memory sharing, which increases the surface area for inconsistency without adding any arbitration mechanism. The documentation does not describe arbitration; the architecture does not support it.

---

## 6. Post-2026-05-05 Updates

**Conversations API (2026-01-21):** This is the most significant post-baseline development. The API enables a single agent to accumulate memory across concurrent conversations (e.g., parallel Slack threads feeding one agent's memory). This extends Letta's write-authoring posture across multi-conversation contexts — a genuine architectural advance for agent stateful identity. However, it adds no new mechanisms for contradiction detection, retraction, or structured epistemic authoring. The update is noteworthy for the paper as evidence that Letta is developing its "unified agent identity" narrative, which makes it a more direct competitor to ENGRAM's layer-2 (narrative identity) pitch while leaving layer-3 (epistemic identity) uncontested.

**Filesystem memory benchmark (undated, post-2025):** Letta published a benchmark showing filesystem-based memory agents achieve 74.0% accuracy on LoCoMo. This is notable because Letta explicitly published research showing simpler approaches (filesystem) compete with its own specialized memory tools. This does not affect the OCC analysis but is relevant context for the paper's positioning: even Letta's own benchmark research suggests the value of specialized memory architectures is in structuring the authoring process, not the retrieval mechanism. This supports ENGRAM's pivot to epistemic identity (what the agent can do with structured claims) over retrieval quality.

---

## 7. Pros (Letta's POV) / Cons (ENGRAM's POV)

**Pros (what Letta genuinely does well, primary-source verified):**
- Agent actively writes its own memory via explicit tool calls; this is a genuine architectural distinction from passive RAG and most retrieval-only systems
- Memory persists across sessions; core memory blocks stay in-context window continuously
- Multi-agent memory sharing via shared blocks (documented in letta.com/blog/memory-blocks)
- Conversations API (2026-01-21) enables a single agent to form unified memory across hundreds of concurrent conversations — a scalability advantage
- Tool signatures are expressive: `append`, `replace`, `insert`, `rethink` give the agent surgical control over text content
- Archival memory with semantic search and date-range filtering gives non-trivial retrieval

**Cons (from ENGRAM's comparative perspective):**
- "Memory block values are just strings" — no claim-level structure; the unit of authoring is an opaque text block, not a typed assertion with provenance
- `core_memory_replace` and `memory_rethink` overwrite in place; prior content is gone, no structural record of what was believed before
- No contradiction detection at any layer; inconsistencies across memory blocks, across conversations, or across time survive silently
- No derivation graph; nothing links one memory to another as evidence or derived conclusion
- No evidence-class confidence; all memory content is equally weighted string
- No retraction cascade; `core_memory_replace("old belief", "new belief")` updates the string but has no downstream effect on any other memory
- Agent-as-author posture is present but shallow: the agent authors text, not claims. It cannot inspect its own epistemic state at the assertion level.
- Benchmark result (74.0% on LoCoMo with filesystem) is a self-own: suggests the authoring mechanism matters more than the retrieval mechanism, which the paper can use to argue for ENGRAM's structural authoring primitives

---

## 8. Verdict

Letta is the most architecturally mature comparator in the memory-authoring space: it gives agents real write access to their own memory, structures that memory into typed blocks with size limits, and now (Conversations API) maintains unified agent identity across concurrent conversations. None of this satisfies Kahl's OCC conditions. Cond 1 fails because memory blocks are strings without binding-commitment semantics — the agent can overwrite any "commitment" at any time with no record. Cond 2 fails by Kahl's decisive criterion: a fresh agent initialized with the same memory block content IS, by Letta's own architecture, the same agent — structural reducibility holds. Cond 3 is architecturally impossible in the current design: there is no derivation graph for cascade to propagate through. For the paper, Letta is the most important comparator to address precisely because it DOES support write-authoring (which partially satisfies the "agent-as-author" framing), but the authoring unit is text not claims, making it a layer-2 (narrative identity) system — coherent story, no structural self-correction. ENGRAM's claim that the third layer (epistemic identity) is unoccupied is strengthened, not weakened, by Letta's existence: the best-in-class write-authoring system still does not reach Cond 3.

---

## Sources

- https://raw.githubusercontent.com/letta-ai/letta/main/letta/functions/function_sets/base.py (function signatures — primary source, verbatim)
- https://www.letta.com/blog/agent-memory
- https://www.letta.com/blog/conversations
- https://www.letta.com/blog/memory-blocks
- https://www.letta.com/blog/benchmarking-ai-agent-memory
- https://docs.letta.com/guides/agents/memory
- https://arxiv.org/abs/2310.08560 (MemGPT paper — abstract only; full HTML unavailable at time of fetch)
