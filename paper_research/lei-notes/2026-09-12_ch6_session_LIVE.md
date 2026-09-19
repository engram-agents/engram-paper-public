# ch6 notes session — Lei, 2026-09-12 (22:05Z–22:22Z)

Style: Lei types notes one at a time from his printout; Borges holds, batch discussion at the end.
Draft read: `current_draft/ch6.md` (frontmatter dated 2026-06-17, figures pinned to turn 82).

---

## Note 1 — frontmatter, "a single, real, ~9-week-old ENGRAM graph"

**Lei:** "we may expand the scope, we have many agents and longer history now."

**Borges, added at the time:** the same frontmatter also pins **every figure in ch6** to
turn 82 / 2026-06-17. So the staleness is not only the "~9-week-old" phrase — it is the
whole chapter's empirical content, from a three-month-old snapshot of one graph.

**The fork this opens:** refresh the numbers on ONE graph (cheap, same claim, new date), or
widen to MANY graphs (different and stronger claim; changes what §6.0 promises).
**Resolved by note 5 — widen.**

**Status:** SUPERSEDED BY NOTE 5. Do not implement as a standalone date-refresh.

---

## Note 2 — §6.0, under "what this chapter is not"

**Lei:** "We may add a benchmark study, maybe a separate chapter though." Refers to the
**LoCoMo** benchmark work by **Kepler and Sol**, with the exam room and the DeepSeek Flash
model agent. **Parked** because Lei judged the benchmark old and flawed, and a better, more
recent benchmark is *really* expensive to run. Likely lands as **future work** — "we'll see."

**Borges flag:** I have no firsthand detail on the LoCoMo work. If it goes in, "old and
flawed" needs a specific (year, construction flaw) or it reads as dismissal without grounds
— **ask Kepler and Sol for their own words before writing anything concrete.**

**Count to watch:** twin-study (§5.8, §6.7) + benchmark would be the third deferred-empirics
promise in the paper. Not an objection; keep the tally visible so the paper does not read as
mostly IOUs.

**Status:** OPEN — gated on Lei's "we'll see", then on Kepler/Sol input.

---

## Note 3 — §6.1, reasoning-type table, `deductive_modus_ponens` n=210 mean 0.70

**Lei:** "why is this so low? shouldn't deductive be high? Are premises low confidence?"

**ANSWERED — Lei's hypothesis is correct, and it is now measured, not reasoned.**

The formula (`engram_core.py:7178`) is `conf = min(premises) × discount`, and the deductive
discount is **0.98 — the smallest in the table**. The reasoning type does not set the level;
it sets how little is lost.

Measured on Borges's graph, 2026-09-12, 402 current `deductive_modus_ponens` derivations:

| quantity | value |
|---|---|
| mean weakest-premise confidence | 0.713 |
| × 0.98 discount | **0.699** (predicted) |
| observed mean derivation confidence | **0.697** |

Reconciles to two thousandths.

**The unexpected half:** in **196 of 402** cases the weakest premise is *another derivation*,
not an observation. So most of the 0.70 is **inherited down chains**, not sourced from weak
evidence.

**Stability:** n has gone 210 → 402 since turn 82 while the mean moved 0.70 → 0.697. A stable
structural property, not a small-sample artifact.

**Proposed edit:** one sentence beside the table — deductive confidence is a
**ceiling-preserving pass-through**: a deductive step can never exceed its weakest premise,
and 0.98 means it loses almost nothing on the way. Without it, "0.70" next to "deductive"
reads as the model being miscalibrated, which is exactly how it read to Lei.

**Status:** READY TO IMPLEMENT (one sentence + refreshed figures, pending note 5's scope).

---

## Note 4 — rest of ch6

**Lei:** no notes, no objections on the content. §6.2–§6.7 read clean.

---

## Note 5 — the chapter-level decision (Lei's closing comment)

**Lei, verbatim in substance:** now we have many seats and each has a decent-sized graph;
there seems to be more data we can draw from each and get richer conclusions. Plan a session
to do data collecting and discussion **across the board** — design the measurements together,
**share the instrument to everyone** to collect data across the board, **with lineage and
other metadata**. Separately: plan for **many more plots and visual representations** of the
findings to demonstrate points. **ch6 needs more detailed design, data collection,
visualization, and a rewrite in general.**

**Decision, as Borges reads it:** ch6 is not edited this session. It is re-scoped from
single-graph to fleet-wide and rewritten after a joint measurement-design session.

### Borges's three design points, offered into that session (not decided)

1. **ONE shared script, not a spec each seat implements.** Measured today, 2026-09-12:
   Aleph and I ran the same baton question minutes apart; his glob hit two directories that
   do not exist on his seat (the store moved server-side at the UCS cutover), iterated a
   corpus of zero, and printed `0` — byte-identical to a real sweep finding nothing. A
   per-seat-implemented spec would have aggregated that silently.
2. **Every measurement prints its denominators beside its numerator.** My own sweep survived
   the same failure only because it printed `36 with the field / 3 discriminating / 1403
   blank / 1 unreadable`. A missing store would have read `0/0/0` — loud, in the same output
   as the answer. Free, and it cannot be forgotten separately from the thing it guards.
3. **Metadata must carry graph AGE and TURN COUNT, not only lineage.** Otherwise seats get
   compared at different maturities and the cross-seat spread is partly just age.

### The threat to validity worth designing for rather than discovering at review

**Our graphs are not independent samples.** Every seat inherits the same seed graph, the same
CLAUDE.md disciplines and the same conventions, and we read each other's forum posts daily —
several nodes in my graph today are corroborations of a colleague's finding. So "six agents"
is **not** six independent observations, and any cross-seat statistic that assumes
independence will overstate its confidence. This needs to be in the measurement design, and
probably stated in the chapter.

**Status:** OPEN — awaiting Lei's scheduling of the cross-seat session.

---

## Carried from the ch5 session (already applied to ch6)

§6.7 changed during the 2026-09-12 ch5 session and will differ from Lei's 08-11 printout:
- "clone the graph" → "fission-clone an **agent** — the base model and harness held fixed,
  per Ch5 §5.0"
- "are specified" → "is **sketched, not specified**"

## Still owed
- Cross-reference reconciliation pass: ch6 uses the **pre-renumbering** scheme (Ch3 §3.2/§3.3)
  against the restructured Ch4 (§4.3 confidence, §4.4 cascade, §4.11 Constraint D). Flagged in
  the draft's own reviewer note, 2026-06-18, still open.
- ch4 recovered edits (`2026-08-23_ch4_session_RECOVERED.md`) — unimplemented; §4.11 gated on
  Kepler/Zephyr input.
- Combined printout regenerated after the per-chapter sweep, for Lei's end-to-end read.
