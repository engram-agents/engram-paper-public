# TierMem — First-Hand Read
**Sub-agent:** paper-research scout
**Access date:** 2026-05-12
**Status:** Primary-source verified

---

## 1. Metadata

| Field | Value |
|-------|-------|
| Title | From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents |
| Authors | Qiming Zhu, Shunian Chen, Rui Yu, Zhehao Wu, Benyou Wang |
| arXiv ID | 2602.17913v1 |
| Submitted | 2026-02-20 |
| Venue | arXiv preprint (cs.AI) |
| URL | https://arxiv.org/abs/2602.17913 |

---

## 2. Architecture / Framework Summary

TierMem addresses what the authors call the **write-before-query barrier**: summaries produced at write time may erase decisive evidence because "compression decisions are made before the system knows what a future query will hinge on."

The solution is a two-tier hierarchy:

**Tier-2 — Immutable Paged Raw Log:** Full interaction history stored as fixed-size pages (~1000 tokens each) with stable identifiers. The paper is explicit: "Tier-2 stores the full interaction history as immutable, fixed-size pages." No deletion mechanism is described anywhere in the paper. The log is append-only.

**Tier-1 — Summary Index:** Compact summaries with dense embeddings for retrieval. Each entry contains: "(i) a concise summary, (ii) a dense embedding for retrieval, and (iii) provenance links (ρ) pointing to the specific Tier-2 page identifiers that support the summary." Summaries are synthesized synchronously at page-seal time: "whenever a raw page is sealed in Tier-2, TierMem synthesizes corresponding summary entries in Tier-1, automatically recording the links ρ."

**Inference protocol:**
1. Fast Path — retrieve Tier-1 summaries only
2. Router (πθ) — binary Answer/Escalate decision
3. Optional Escalation — bounded retrieval from Tier-2 raw pages
4. Verified Write-back — ADD/UPDATE/SKIP back to Tier-1

**Router training:** Hindsight supervision. Label Answer (0) if "the summary-only answer is correct and complete"; Label Escalate (1) if "the summary answer is vague or incorrect, but the raw-grounded answer recovers necessary details." Training: SFT from GPT-5 distillation followed by GRPO (Group Relative Policy Optimization) with reward balancing accuracy, cost, and false-alarm rate.

**Write-back protocol:** Three operations (Section A.6, Table 5): "Retrieve-and-Edit write-back (recall related Tier-1, then ADD/UPDATE/SKIP)." UPDATE retrieves semantically related Tier-1 units and modifies the existing entry. The paper does **not** specify whether UPDATE preserves the old entry alongside the new information or overwrites it — this is not documented.

**Performance:** 0.851 accuracy on LoCoMo, 54.1% fewer input tokens and 60.7% lower latency vs. raw-only baselines.

---

## 3. ENGRAM-Function Comparison Table

| ENGRAM Mechanism | TierMem Status | Evidence |
|------------------|---------------|----------|
| Claim-level contradiction as first-class node (ct_*) | **Absent** | Paper does not use "conflict," "contradiction," or "inconsistency" as architectural primitives. Deduplication (semantic redundancy avoidance) is the closest concept. |
| Retraction cascade through derives_from edges | **Absent** | No retraction mechanism. Tier-2 is strictly append-only; Tier-1 UPDATE does not cascade to dependents. |
| Derivation primitive (typed reasoning edges) | **Absent** | No edge types or derivation chains. Provenance is a pointer from summary to raw page, not a reasoning-step record. |
| Evidence-class confidence taxonomy | **Partial** | Router produces binary Answer/Escalate signals; no multi-class confidence taxonomy. |
| Provenance to quoted span of committed source | **Page-level only** | Provenance links point to Tier-2 page identifiers (fixed ~1000-token pages), not to quoted spans or sentences. |
| Supersede relation | **Implicit / undocumented** | UPDATE modifies Tier-1 entries, but no explicit supersede relation is defined; old state fate is not documented. |
| Agent-as-epistemic-author posture | **Absent** | No framing of agent as author accumulating a structured epistemic record. |

---

## 4. OCC Mapping

No reference to Kahl, OCC, diachronic constraint, non-interchangeability, or self-maintaining arbitration anywhere in the paper. The paper does not engage philosophical identity literature at all.

The paper was submitted 2026-02-20, the same month as Kahl's AGI paper (exact Kahl submission date not confirmed here; prior ENGRAM research dates it to Feb 2026). Cross-pollination cannot be inferred from absence alone, but neither paper cites the other.

---

## 5. OCC Satisfaction Analysis

### Cond 1 — Diachronic Constraint
**Not satisfied structurally.** Tier-2 immutability means past information is preserved, but past commitments do not structurally constrain present deliberation. The router decides whether to consult the past at all, and this decision is a learned cost-benefit optimization (token budget vs. accuracy), not a structural dependency. There is no mechanism that forces prior commitments to bear on current outputs.

### Cond 2 — Non-Interchangeability Under Reset
**Partially approached, not satisfied.** Tier-2 stable page identifiers survive across sessions and are immutable. Replacing a TierMem instance with a fresh one would produce a different memory state. However, the paper makes no argument for agent-level token-distinctness; it is a memory system, not an identity system. The stable-identifier claim is architectural, not about agent identity continuity.

### Cond 3 — Self-Maintaining Arbitration
**Not satisfied.** No foundational-retraction-flagging mechanism exists. When a Tier-1 summary is UPDATEd, there is no cascade to dependent summaries or downstream uses of the old content. The system cannot flag that a downstream derivation rests on a now-corrected premise.

**Summary verdict for OCC:** TierMem satisfies none of Kahl's three conditions in their structural sense. It approaches Cond 2 asymptotically (immutability plus stable IDs) but does not make the agent-level identity claim those conditions require.

---

## 6. Load-Bearing for the ENGRAM Paper

**Strongest citation use:** TierMem is the best available comparator for ENGRAM's provenance discipline. The paper demonstrates that provenance-linked two-tier memory is a live research direction (Feb 2026), which establishes that provenance matters — but also that page-level granularity is the current art. ENGRAM's quote-level provenance (to committed span) is a meaningful finer-grained claim.

**Specific load-bearing contrast:** TierMem's write-back UPDATE does not preserve the prior Tier-1 state explicitly and does not cascade to dependents. ENGRAM's supersede relation + retraction cascade are architectural primitives TierMem lacks entirely. This is citable as a gap.

**Honest caveat:** TierMem's benchmarked accuracy (LoCoMo 0.851) and token efficiency are concrete empirical results. ENGRAM's paper needs a response to the efficiency question if TierMem is cited as a comparator.

---

## 7. Honest Pros / Cons

**Pros of citing TierMem:**
- Peer-reviewed arXiv preprint with clear architecture and empirical results
- Establishes that the field is moving toward provenance-aware memory (supports ENGRAM's provenance claim as timely)
- Page-level provenance creates a concrete foil for ENGRAM's quote-level claim
- Immutable raw log is a genuine parallel to ENGRAM's append-only observation record

**Cons / limitations:**
- No philosophical engagement — citing it for OCC mapping requires the ENGRAM paper to do that work itself
- UPDATE behavior is underdocumented: the paper doesn't confirm whether old Tier-1 entries are archived or destroyed, which weakens the retraction-absence claim (the correct claim is "not documented," not "definitively absent")
- LoCoMo benchmark focus may not transfer to the epistemic-identity use cases ENGRAM targets

---

## 8. Verdict

TierMem is a technically rigorous provenance-aware memory paper that arrives at the same intuition as ENGRAM (preserve raw evidence, link summaries to sources) but stops at the engineering problem of token efficiency. It does not attempt contradiction detection, retraction cascading, typed derivation edges, or agent-as-author framing. Its provenance is page-level rather than quote-level. It has no engagement with philosophical identity literature. For the ENGRAM paper, TierMem is the strongest existing-art foil for ENGRAM's provenance and immutability claims: close enough to share vocabulary, distant enough that ENGRAM's structural contributions remain distinct. The UPDATE-behavior gap (fate of old Tier-1 entries) should be noted as "not documented" rather than "absent" to maintain scholarly honesty.
