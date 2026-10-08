# Appendix C — Auto-Recall Ranking and the Memory-Utility Tradition

---

## C.1 The memory-utility tradition

A 2026 line of work — exemplified by **MemRL** [@zhang2026, p. 1] — applies reinforcement learning not
to a model's weights but to its **memory retrieval**: it learns *which stored
memories are worth surfacing* by treating retrieval as an action and downstream
usefulness as a reward, ranking memories by a learned **Q-value** (ob_0647). The
appeal is that it keeps the base model frozen — no fine-tuning, so no catastrophic
forgetting — while still improving over time at the level of *what gets recalled*.
Concretely, MemRL composites semantic similarity with an EMA-learned Q-value via a
weighted score, with the Q-error decaying as `(1−α)^t` [@zhang2026, pp. 4–5, 13] (ob_0651).

ENGRAM sits in this tradition. Every node carries a `utility_score` — a learned
value updated by the same exponential rule, `Q_new = Q_old + α(1 − Q_old)` — and
ranking composites that learned value with semantic relevance rather than ordering by
relevance alone. What differs is the reward: MemRL learns from task outcome, while
ENGRAM learns from **what the agent did with the node once it had it**, which is a
signal the substrate can observe directly and attribute without ambiguity. The rule
has no negative term: a recall that proves useless leaves a node's utility where it
was, so `utility_score` is non-decreasing. Demoting unhelpful nodes would need a
penalty the current rule does not have; we list it as a limitation (§7.2).

## C.2 ENGRAM's utility_score — a learned value, graded by the act it earned

ENGRAM's `utility_score` is the Q-value analogue, and what it grades is **the
cognitive load of the act a node took part in** — not how hard the agent looked to
find it (dv_1641). The learning rate α is keyed to the action, in three bands:

| α | actions | what the band means |
|---|---|---|
| **0.15** | `derive`, `supersede`, `contradict`, `resolve`, `register_exemplar` | the node took part in an **epistemic act** — it became a premise, drove a revision, or anchored a lesson |
| **0.10** | `inspect`, `subgraph`, `mention`, `focus`, `history`, `citation` | the node was **engaged with** — read closely, traversed, named in reasoning, or pinned |
| **0.05** | `focus_load`, `unfocus` | **loose touch** — the node moved with a set rather than being chosen |

When a node is reached several ways, *max-α-wins*.

Note what the top band contains: **no retrieval verb at all.** Every member is
something the agent *does with* a node once it has it. The table is not measuring
attention spent looking; it is measuring what the looking produced. `inspect` — the
most deliberate way to read a node — sits in the middle band, below `derive`, because
reading closely and then building on it are different achievements.

**Two independent paths award credit**, and the second one matters more than it
looks. The first is citation: naming a node as a premise in a new derivation. The
second is a stop-hook that scans each of the agent's own turns and credits any node
**mentioned** in it, at α = 0.10. The first path alone was the original design and
proved too narrow — it misses prose-mention, inline citation, and reasoning that is
plainly informed by a node without formally citing it. A node that shapes an argument
without being cited in it has still been useful, and the substrate now sees that.

This is the difference between *access frequency* (which a vector store can track) and
*epistemic usefulness* (which requires knowing what the recall went on to do) — the
distinction that puts ENGRAM's ranking in the memory-utility tradition rather than the
plain-retrieval one.

## C.3 The composite ranking — multiplicative amplifiers over a three-stage pipeline

Recall in production runs a **three-stage** `_search_nodes` pipeline (dv_0707):

1. **Gather** — FTS + semantic-embedding merge produces candidate nodes with a base
   **relevance** score.
2. **Composite re-rank** — the stage this appendix is about.
3. **Diversity** — an MMR (maximal-marginal-relevance) pass (MMR_LAMBDA = 0.9) trims
   near-duplicates so the surfaced set is not nine paraphrases of one claim.

The composite (stage 2) uses **multiplicative amplifiers**, not an additive blend
(ob_2017):

```
composite = relevance × (1 + UTIL_BETA × utility_score)
                      × (1 + IMP_BETA × normalized_importance)
```

with `UTIL_BETA = 0.10` and `IMP_BETA = 0.005` in current production. The design
rationale (Lei, 2026-05-19) is the load-bearing point: **relevance is the base
topical signal; utility and importance are *amplifiers* in orthogonal dimensions, not
co-equal addends.** An additive blend `(1−λ)·relevance + λ·utility` (the retired
form, UTILITY_LAMBDA = 0.3) requires careful λ-tuning to keep utility from *drowning*
relevance; multiplicative amplifiers preserve relevance's authority and let each
amplifier scale from 0 to a bounded gain (a max-utility node, Q=1, gets a 1.10×
boost). The importance amplifier is **homeostatic** — `normalized_importance` is
anchored to the current minimum-queryable importance, so the formula adapts as the
graph grows rather than using a fixed scale.

## C.4 Importance, forgetting, and the testing effect

Two further signals interact with the ranking. **Importance** gates *tier
eligibility* — it is a pre-filter deciding what is even in the queryable set (tier 2)
versus faded (tier 3), per the forgetting mechanism (Ch4 §4.5) — and then enters the
composite as the second amplifier. And recall itself *strengthens* a node (the
recall-count / recall-turn signals), so a node that keeps proving useful is both
retained longer and ranked higher: the **testing-effect** shape, where retrieval
is not a read-only event but reinforces the trace [@roediger2006, p. 249]. The result is a recall surface that
is adaptive on three coupled axes — topical relevance, learned usefulness, and
decaying importance — rather than a static similarity sort.

## C.5 Honest scope

Two honest qualifications, both consistent with the paper's posture:

- **The constants are harness-calibrated, not first-principles.** UTIL_BETA, IMP_BETA,
  and MMR_LAMBDA were tuned by an NDCG sweep on a local recall-measurement harness,
  which set them to 0.10, 0.005 and 0.9 and gained ≈0.05 NDCG over untuned values
  (ob_1955). They are *measured to
  rank well*, which is a stronger footing than the confidence-model constants (Ch7
  §7.2, which are *not* outcome-calibrated) — a useful internal contrast.
- **The reward signal is an engagement proxy, not a true outcome:** utility is
  learned from the engagement actions C.2 lists (citation among them), none of
  which verifies that the recalled node was right. A fuller outcome-based reward
  (did the downstream claim survive contradiction?) is a future direction,
  continuous with the confidence auto-calibration track (Ch7 §7.2).

**→ Ch4 §4.7** makes the claim; this appendix is the detail.
