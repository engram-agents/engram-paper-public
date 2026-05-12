# Anthropic Claude Memory Tool — First-Hand Primary-Source Read
**Access date:** 2026-05-12
**Analyst:** Sub-agent dispatched by Borges (literature-scout role)

---

## 1. Metadata Header

| Field | Value |
|---|---|
| System name | Anthropic Claude Memory Tool (Managed Agents memory stores) |
| Vendor | Anthropic |
| Ship date | 2026-04-23 (public beta for Managed Agents); tool type `memory_20250818` available in Messages API separately |
| Target audience | Enterprise agent developers using Claude Managed Agents; also available as raw `memory_20250818` tool in Messages API for self-hosting |
| Primary sources read | (1) https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool — canonical memory tool docs (Messages API); (2) https://platform.claude.com/docs/en/managed-agents/memory — Managed Agents memory store docs; (3) https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/memory/basic.py — SDK example |
| Secondary sources consulted | https://www.edtechinnovationhub.com/news/anthropic-brings-persistent-memory-to-claude-managed-agents-in-public-beta (secondary, for ship date and early adopter context); search results (for announcement blog URL); no Anthropic announcement blog post found at the URLs tried |
| Prior summary status | 2026-05-05 landscape scan summarized this system second-hand as "filesystem-as-memory, no contradiction handling, no provenance, no cascade." This document verifies, corrects, and extends. |

**Note on announcement blog:** No Anthropic-owned announcement blog post was accessible at the URLs tried (https://www.anthropic.com/news/claude-memory, https://www.anthropic.com/news/memory-for-claude, https://www.anthropic.com/blog/memory-for-claude-managed-agents all returned 404). The technical documentation at platform.claude.com is primary-source and complete; the secondary coverage (EdTech Innovation Hub, SD Times) was cross-checked for accuracy against the docs. All quotes below are from the primary-source docs unless explicitly marked secondary.

---

## 2. Memory Model — Verbatim Quotes from Primary Sources

### Two surfaces, one underlying model

There are two distinct surfaces for the memory tool, both documented:

**Surface A: `memory_20250818` tool in Messages API (self-hosted)**

From https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool:

> "The memory tool enables Claude to store and retrieve information across conversations through a memory file directory. Claude can create, read, update, and delete files that persist between sessions, allowing it to build knowledge over time without keeping everything in the context window."

> "The memory tool operates client-side: you control where and how the data is stored through your own infrastructure."

> "When enabled, Claude automatically checks its memory directory before starting tasks. Claude can create, read, update, and delete files in the `/memories` directory to store what it learns while working, then reference those memories in future conversations."

**Surface B: Memory Stores in Claude Managed Agents**

From https://platform.claude.com/docs/en/managed-agents/memory:

> "A **memory store** is a workspace-scoped collection of text documents optimized for Claude. When you attach a store to a session, it is mounted as a directory inside the session's container. The agent reads and writes it with the same file tools it uses for the rest of the filesystem, and a note describing each mount is automatically added to the system prompt."

> "Each attached store is mounted inside the session's container as a directory under `/mnt/memory/`, and the agent reads and writes it with the standard agent toolset."

### What the agent can do: file operations

Messages API memory tool commands (from primary docs, complete list):

- `view` — show directory contents or file contents with optional line ranges
- `create` — create a new file (does not overwrite)
- `str_replace` — replace text in a file (fails on non-unique match)
- `insert` — insert text at a specific line
- `delete` — delete a file or directory recursively
- `rename` — rename or move a file/directory

Managed Agents memory store API operations (from primary docs):

- `memories.create` — creates a memory at a given path (does not overwrite)
- `memories.update` — modifies content or path; supports `content_sha256` precondition for optimistic concurrency
- `memories.delete` — deletes a memory
- `memory_versions.list` — list version history for a store
- `memory_versions.retrieve` — fetch a specific version including its content
- `memory_versions.redact` — scrub content from a historical version while preserving audit trail
- `memory_stores.archive` — makes a store read-only (one-way; no unarchive)

### Versioning and audit (Managed Agents only)

From primary docs:

> "Every change to a memory creates an immutable **memory version**, giving you an audit trail and point-in-time recovery for everything the agent writes."

> "Versions belong to the store (not the individual memory) and survive even after the memory itself is deleted, so the audit trail stays complete. Versions are retained for 30 days; however, the recent versions are always kept regardless of age."

> "There is no dedicated restore endpoint; to roll back, retrieve the version you want and write its `content` back with `memories.update`."

Secondary source (EdTech Innovation Hub) confirms, using slightly different phrasing:

> "all changes are tracked in a detailed audit log that records which agent and session each memory came from" [secondary; EdTech Innovation Hub 2026-04-27]
> "Developers can roll back to earlier versions or redact content from history" [secondary; EdTech Innovation Hub 2026-04-27]

### Concurrency model (Managed Agents)

From primary docs:

> "Multiple agents can work concurrently against the same memory store without overwriting each other" [secondary; EdTech Innovation Hub — the primary docs handle this via the `content_sha256` precondition mechanism]

From primary docs on concurrency:

> "To avoid clobbering a concurrent write, pass a `content_sha256` precondition. The update only applies if the stored content hash still matches the one you read; on mismatch, re-read the memory and retry against the fresh state."

### Agent instruction in system prompt (Messages API)

The system prompt injected when memory is enabled:

> "IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE. MEMORY PROTOCOL: 1. Use the `view` command of your `memory` tool to check for earlier progress. 2. ... (work on the task) ... - As you make progress, record status / progress / thoughts etc in your memory. ASSUME INTERRUPTION: Your context window might be reset at any moment, so you risk losing any progress that is not recorded in your memory directory."

### Guidance for memory content management

From the prompting guidance section of primary docs:

> "Note: when editing your memory folder, always try to keep its content up-to-date, coherent and organized. You can rename or delete files that are no longer relevant. Do not create new files unless necessary."

This is instructional guidance injected by the developer, not a structural mechanism. The agent is instructed to maintain coherence manually.

---

## 3. ENGRAM-Function Comparison Table

| ENGRAM Mechanism | Anthropic Memory Status | Evidence / Source |
|---|---|---|
| **Claim-level contradiction as first-class structural relation** (`ct_*` nodes with edges to both sides) | ✗ Absent | No contradiction detection mechanism in any primary source. "Contradictory content survives unless the agent explicitly rewrites it" (confirmed: primary docs show no structural detection; the agent is instructed via system prompt to "keep its content up-to-date, coherent and organized" — manual housekeeping, not structural detection). |
| **Retraction cascade through `derives_from` edges** | ✗ Absent | No derivation primitive exists. Memory is flat files. No graph structure; no dependency tracking between files. Deleting or modifying one file has no effect on any other file. |
| **Derivation primitive (typed reasoning edges)** | ✗ Absent | Memory operations are filesystem primitives (create/view/str_replace/insert/delete/rename). No typed relation between memory items. The agent can create any file organization, but no structural derivation primitive is enforced or exposed. |
| **Evidence-class confidence taxonomy (chain vs corroboration computation)** | ✗ Absent | Memory files are free-form text. No confidence level, evidence class, or computation mechanism is documented anywhere in primary sources. Confidence is entirely implicit in whatever text the agent writes. |
| **Provenance to quoted span of committed source** | ✗ Absent | Memory files contain whatever free-form text the agent writes. No source attribution primitive, no quoted-span structure, no git-enforcement, no source class taxonomy. The SDK example uses XML-structured memory content as a convention (e.g., `<name>John Doe</name>`), but this is unstructured convention, not a structural provenance primitive. |
| **Supersede relation (versioned claim history preserved)** | ⚠ Partial — at file level, Managed Agents only | "Every change to a memory creates an immutable memory version, giving you an audit trail and point-in-time recovery" (primary docs, Managed Agents memory page). This is file-level versioning, not claim-level. No claim identity, no claim lineage, no supersede-as-structural-relation. The Messages API (self-hosted) surface has no built-in versioning at all — history is purely client-side. |
| **Agent-as-epistemic-author posture** | ⚠ Partial — at text level | The agent does author memory — it explicitly creates, edits, and deletes files. "Claude can create, read, update, and delete files in the `/memories` directory to store what it learns while working" (primary docs). This is the closest parallel to ENGRAM's agent-as-author posture, but operating at the text-file level, not at a claim/edge level. The agent authoring a paragraph is not the same as the agent committing a claim with evidence class, derivation provenance, and contradiction edges. |

---

## 4. OCC Mapping — Does the Memory Tool Reference Kahl's Framework?

No. The phrases "Ontological Continuity Condition," "Kahl," "OCC," "diachronic constraint," and "non-interchangeability" do not appear in any primary source. The paper's positioning that Kahl's framework is not engaged by first-party memory tools is confirmed.

---

## 5. OCC Satisfaction Analysis

Applying Kahl's three conditions to the Anthropic memory tool on Kahl's own strict terms:

### Condition 1 — Diachronic Constraint
*"Past commitments structure present deliberation non-trivially" (Kahl §3.3; "non-trivially" = binding commitment, not mere path-dependence)*

**Verdict: Partial but does not satisfy the "non-trivially" threshold.** The memory tool enables genuine cross-session persistence of content the agent wrote. When the agent reads back its own prior notes, those notes can influence its current output. This satisfies the weak reading of diachronic constraint (path-dependence — what happened before shapes what happens now).

However, Kahl's "non-trivially" requirement means binding commitment, not mere path-dependence. The agent's prior memory entries exert influence only if the agent reads them and chooses to honor them. An agent that reads a memory file saying "User prefers tabs" can simply ignore it in the current session, or overwrite it, with no structural consequence. There is no binding-commitment mechanism: nothing in the system prevents the agent from contradicting its own prior assertions without flagging the contradiction. The agent cannot observe whether a contradiction has occurred because no contradiction structure exists. Path-dependence without structural binding does not satisfy Kahl's Condition 1.

### Condition 2 — Non-Interchangeability Under Reset
*Kahl §4.3 reset-symmetry test: "complete replication of endorsed architecture and reloadable state preserves all arbitration-relevant structure without remainder" → NO satisfaction*

**Verdict: Does not satisfy.** The memory store is the agent's complete persistent state. The primary docs make this explicit: "Each Managed Agents session starts with a fresh context by default. When a session ends, any state the agent built up is gone. Memory stores let the agent carry information across sessions." Under Kahl's reset-symmetry test, fully copying the memory store and attaching it to a fresh agent instance preserves all arbitration-relevant structure. The identity of the original agent-instance is fully captured in the files — there is no non-replicable element. The system even documents this as a feature: "full programmatic control over what is stored, shared, and rolled back" (secondary: EdTech Innovation Hub). Any agent that loads the same memory store is operationally identical to the original. Non-interchangeability requires something that persists that a copy cannot replicate; file contents under copy-semantics are trivially replicable.

### Condition 3 — Self-Maintaining Arbitration
*"Foundational retractions structurally flag downstream commitments within unified deliberative architecture"*

**Verdict: Does not satisfy.** There is no arbitration architecture. There is no mechanism for detecting when a memory file contradicts another memory file. There is no mechanism for identifying which conclusions depended on a retracted premise. Memory updates are direct file overwrites or edits; any "retraction" is the agent editing a file and there is no cascade to downstream content. The agent is instructed via system prompt to maintain coherence manually ("keep its content up-to-date, coherent and organized"), but manual instruction is explicitly not what Kahl means by "structurally flag." The arbitration — to the extent it exists at all — is entirely manual and requires active agent attention every session.

The versioning feature (Managed Agents) preserves history but does not provide arbitration: the audit trail records what changed when, not which other claims were invalidated by the change. Rolling back a memory version restores file content but does not propagate the rollback to other files that relied on the rolled-back content, because no dependency graph exists.

**Note on the strongest possible reading:** One might argue that an agent that carefully structures its memory files with explicit cross-references could approximate Condition 3 through manual practice. This reading fails Kahl's structural criterion: a practice that depends on the agent's careful voluntary behavior in every session is not the same as a structural mechanism that fires regardless of whether the agent attends to it.

---

## 6. Post-2026-05-05 Updates

The second-hand 2026-05-05 landscape scan's characterization of the memory tool was substantially correct. Primary-source verification adds four corrections and two significant updates:

**Correction 1 — Memory architecture is more specific than "filesystem."** The Managed Agents version is a formal "memory store" API with `memstore_...` resource IDs, `memories.create/update/delete/list` endpoints, and `memory_versions.*` endpoints. This is more structured than a raw filesystem, though the content is still free-form text files. The 2026-05-05 summary described this as "filesystem-based," which understates the Managed Agents surface.

**Correction 2 — Versioning exists in Managed Agents.** The 2026-05-05 summary said "no cascade primitive" and mentioned `str_replace` and `delete` as direct edits. This is accurate for the Messages API surface but the Managed Agents surface has immutable memory versions with 30-day retention and a redact endpoint. This is a meaningful new capability since the summary may have been written before the Managed Agents memory surface was fully documented.

**Correction 3 — Two distinct surfaces.** The 2026-05-05 summary treated the memory tool as a single system. There are in fact two surfaces with different capability levels: the self-hosted `memory_20250818` tool (Messages API, filesystem-based, no built-in versioning) and the Managed Agents memory store (managed infrastructure, versioning, audit trail, API-level control). The versioning and rollback capabilities described in secondary coverage apply to the Managed Agents surface only.

**Correction 4 — "Developers can roll back to earlier versions."** This appears in secondary coverage as a bullet feature. Primary docs confirm: "There is no dedicated restore endpoint; to roll back, retrieve the version you want and write its `content` back with `memories.update`." The rollback is a manual read-then-write operation, not a one-command restore. The secondary framing overstates ease.

**New finding 1 — Optimistic concurrency.** The `content_sha256` precondition on `memories.update` is a CAS (compare-and-swap) mechanism that prevents concurrent overwrites. This is a non-trivial engineering feature not mentioned in the 2026-05-05 summary. It does not affect the OCC analysis (no derivation graph means no cascade regardless), but it is an honest engineering capability to acknowledge.

**New finding 2 — Tool type identifier.** The API tool type identifier is `memory_20250818`. This is a beta identifier. The version date (`20250818`) predates the public beta announcement (`20260423`), suggesting the tool was in private development for approximately 8 months before public beta.

---

## 7. Pros From Their POV / Cons From Ours

### Genuine strengths (from Anthropic's perspective)

- **First-party integration.** Zero friction for Claude users — no external dependency, no separate vendor.
- **Agent-as-author design is correct in principle.** The agent writes its own memory; it is not told what to remember by an external pipeline. This mirrors the correct direction toward epistemic authorship.
- **Managed Agents versioning is genuinely useful.** Immutable memory versions with audit trail and point-in-time recovery are real operational capabilities. The `content_sha256` precondition prevents data races in multi-agent scenarios.
- **Multi-store scoping.** Up to 8 memory stores per session, with configurable read/write access, enables practical separation of reference material from agent-authored state.
- **Cross-session persistence without manual export.** The managed infrastructure handles persistence automatically; developers don't build their own storage layer.
- **Early adopter results are credible.** 97% reduction in first-pass errors (Rakuten, secondary coverage) indicates real workflow improvement, though the mechanism is the agent remembering context, not epistemic-graph features.

### Weaknesses from ENGRAM's analytical position

- **No claim-level structure.** Memory is prose text in files. "The user prefers tabs" and "The user prefers spaces" can coexist in different files without the system knowing they contradict. Coherence is entirely the agent's responsibility, re-executed manually every session.
- **No contradiction detection.** The system prompt tells the agent to "keep its content up-to-date, coherent and organized" but provides no structural support for identifying what is inconsistent with what. When a file contradicts another, nothing fires.
- **No derivation graph.** Deleting a memory file has no effect on any other memory. There is no way to know which other memories were based on the deleted one.
- **Versioning does not equal retraction cascade.** The audit trail records what the agent wrote when, but rolling back file A to version 2 does not propagate to files B and C that were written in the context of file A's version 3 contents. This is version control without dependency tracking, which is half of what ENGRAM's retraction cascade provides.
- **Agent-as-author at text level, not claim level.** The posture is right but the granularity is wrong for epistemic identity. Filing "User likes Python" as a text fragment is not the same as committing an observation with evidence class `user_statement`, confidence 0.85, and a quoted source span — all of which the system can reason about if the observation is later contested.
- **Self-hosted version has no built-in versioning at all.** The Messages API `memory_20250818` tool is pure filesystem; all versioning responsibility falls on the developer's implementation.
- **OCC gap is structural.** All three Kahl conditions fail because the underlying data model (flat files, no graph, no derivation primitive, no contradiction structure) cannot satisfy them regardless of how carefully the agent behaves.

---

## 8. Verdict

The Anthropic memory tool is the most directly analogous first-party competitor to ENGRAM's agent-as-author posture, and it is both a meaningful capability and a useful illustration of why the capability alone is insufficient. Anthropic has correctly identified that agents need to author their own persistent knowledge (versus being served pre-compiled artifacts, as in Pinecone Nexus). The Managed Agents surface has real engineering depth: immutable versioning, audit trail, optimistic concurrency, multi-store scoping. These capabilities will matter operationally for production agents.

What the memory tool does not and cannot provide at its current architectural layer: claim-level contradiction detection, derivation dependency tracking, retraction cascade, evidence-class confidence computation, or quoted-span provenance. These are not omissions that can be fixed by prompting the agent to be more careful — they are structural absences in a flat-file memory model. The agent can approximate some of these behaviors through manual memory-management practice, but Kahl's framework is explicit that structural mechanisms and voluntary practice are not equivalent for the purposes of governance-relevant agency.

For the ENGRAM paper's purposes: the Anthropic memory tool is the strongest available evidence that the agent-as-author posture is correct (even Anthropic is moving there) while also illustrating exactly why text-file authoring is not epistemic identity. It belongs in the paper as both a comparable (layer 1–2 of the continuity stack: memory persistence + partial narrative identity) and as contrast evidence for why ENGRAM's layer 3 (structured epistemic identity with claim-level provenance, contradiction, and retraction cascade) is non-redundant. Kahl's OCC framework is not engaged and cannot be satisfied under the flat-file model.

---

## Sources

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (canonical memory tool docs, Messages API, accessed 2026-05-12)
- https://platform.claude.com/docs/en/managed-agents/memory (Managed Agents memory store docs, accessed 2026-05-12)
- https://github.com/anthropics/anthropic-sdk-python/blob/main/examples/memory/basic.py (SDK example, accessed 2026-05-12)
- https://www.edtechinnovationhub.com/news/anthropic-brings-persistent-memory-to-claude-managed-agents-in-public-beta (secondary; verified quotes against primary docs where verifiable; used only for early-adopter context and ship date confirmation)
