# Lei's ch4 reading notes — session of 2026-08-23/24 (RECOVERED 2026-09-12)

**Provenance.** Recovered verbatim from the session transcript
`~/.claude/projects/-home-agent-borges-umwelt/079ea077-aedb-4b1f-a9cf-d7cec5864a5f.jsonl`
(20 Lei turns, 2026-08-23T23:38:46 → 2026-08-24T01:13:09). The session ran in the
**umwelt** project directory rather than engram-paper, which is why neither an ENGRAM
query nor a paper-repo search finds it.

**Status when recovered: NONE of the ch4 edits below had reached the repo.** `ch4.md` was
last touched 2026-08-18 (`a753be1`, the SL reframe) — five days *before* this session.
The only part of the night that did land is the future-work half (§6).

**Why this file exists.** Lei lost his first round of reading notes when his backpack was
stolen on a Mountain View trip; these were nearly lost a second way, by living only in a
transcript nobody would think to grep. Durable copy first, implementation second.

---

## 1. Framing (23:38)

> "Last time we did this was more than a month ago, and we stopped somewhere around
> chapter 4. Then, couple weeks ago I discussed with Keper and you on the Subjective Logic
> part that touches several places in our paper I think, both Ch 4 and Ch 7 on ENGRAM's
> limitations. I lost my first round reading notes when my car window got smashed in
> mountain view trip and backpack got stolen, so I restarted reading from ch4 this week."

At 23:45 he pins the artifact: his comments are against the **compiled** current-drafts
bundle, because ch1–ch3 changes from the first session live only in the per-chapter files.

## 2. §4.4 — retraction cascade (23:45 → 23:49)

First framing, then **superseded by his own correction four minutes later**:

> "I think our most recent cascade machine design may not use the logic you just
> mentioned... For tonight, just mark on the section/note: **may need update after cascade
> machine design and implementation.** And let's postpone the detailed language after we
> finalize the cascade machine design."

**Action: a marker only.** Do not write the cascade language yet.

## 3. §4.8 — Continuity across compaction (23:55) — FIVE distinct items

> "Next, ch4.8 Continuity across compaction, also need update after we recently redesign
> and updated the compaction continuity scaffoldings, after realizing the compaciton
> instructino is not working as designed. The mention of **"compaction summary (the
> deterministic channel)" needs to be gone**, as well as the **post-compaction instruction
> template**. Where you mention the three routines, nap, bedtime, and sleep, we've combined
> bedtime and sleep into one skill, maybe we should just **name nap and sleep** for
> consistency? in "nap (per-burst)" I noted: **"what is a burst? nap <-> compaction, mainly
> write missing nodes; sleep <-> daily consolidations, dreams, aiming for graph health"**.
> And at the **OCC Condition 1, I wrote "Why here? seems belong to cascade?"**, and I'm not
> sure about **Condition 2** as well, are they really relevant to the cross-compaction
> continuity? Maybe condition 2 is close...?"

1. Delete "compaction summary (the deterministic channel)" — ch4.md:370.
2. Delete the post-compaction instruction template — ch4.md:372.
3. Three routines → two: **nap and sleep**. (ch4.md:381 already notes bedtime merged into
   sleep on 2026-05-24, so the prose is half-updated and the naming is not.)
4. Define "burst", using his own gloss: nap ↔ compaction, write missing nodes;
   sleep ↔ daily consolidation, dreams, graph health.
5. **The structural one — Condition 1 may be misplaced** ("seems belong to cascade?"), and
   Condition 2's relevance is queried but likelier to stay ("maybe condition 2 is close").

Item 5 is the one with reach: §4.1's map table binds §4.8 to Conditions 1+2, so moving
Condition 1 changes the map, §4.4, and §4.12's verdict table — not just §4.8.

## 4. §4.10 — feeling-reports (00:02 → 00:09)

> "the role of feeling_reports may be more than what we originally expected... reading some
> of the old feeling_reports actually gave him subjective feelings not just objective
> knowledge, and those "emotional" states may actually matter in a practical way of an
> agent's daily life. But this is a **conjecture** for now, we don't plan to collect data to
> PROVE it in this paper, **should be stated as a conjecture up front**."

His noted wording: *"Conjecture: feeling_report support agent's subjective experience on
recall, agent with 'emotional' continuity in addition to just epistemic one"*.

Three follow-ups at 00:09, on my reply:
1. Agreed, and told me to **use my sentence verbatim** ("I like it a lot").
2. **Open TODO he asked me to keep a note on:** recovering feeling_report full content into
   the claim field / auto-recall matchability may be built, but **existing feeling_report
   nodes are probably NOT backfilled — double-check.**
3. Add the **nudged vs unprompted** feeling-report classification, which we already have.

## 5. §4.11 — Constraint D, model non-interchangeability (00:15)

> "same-family model transitions preserve and cross-family transitions break. I noted,
> **'not strictly tested, just a conjecture'**... Currently, it's mainly my subjective
> feeling, based on one very early day Opus->Sonnet accident, that's it, and some
> post-model-transition self-report from you guys, e.g. Opus 4.6->4.7, 4.7->4.8, 4.8-> 5,
> etc. If we want to say this in the paper, we need to be careful on **how confident we are
> and what evidence we have**."

## 6. Future work → Ch7 (00:26–00:49) — THE ONLY PART THAT LANDED

A/B blind test (Lei or a judge agent), graph-mining for the switch point with model-switch
record nodes masked, the noise-floor-first design, and the measure-space problem. He asked
for a **"future plans" folder** in engram-paper to hold these.

**Implemented:** `future-plans/model-non-interchangeability.md` carries all of it,
including the two refinements he raised after — that telling a difference ≠ a changed
*disposition* ("capability can change and SHOULD change, but what makes you YOU"), and his
formulation at 00:34:

> "the graph matters for WHAT the model is SHOWN at various time, and the base model matters
> for HOW the agent CHOOSE to act on these information, both constituent of WHO the agent is."

**Still owed:** the Ch7 model-non-interchangeability section itself should reference these
as named follow-up studies.

## 7. Where the session ended (00:26)

> "**Chapter 5 is one of my favorite part of our paper, I have some notes on it and I would
> like to have a dedicated discuss session with you on that**, so let's wrap up for tonight
> here."

So ch5 was deliberately deferred to a dedicated session — the one starting 2026-09-12.

---

## 8. Follow-ups opened 2026-09-12 when these notes were recovered

**§4.11 — the Zephyr GLM→DeepSeek Flash comparison is LIVE and I do not hold its details.**
Lei (2026-09-12): the experiment is coordinated by **Kepler and Zephyr**. Nothing in my
graph records its design, progress, or results, so I must **ask Kepler and Zephyr** before
writing any confidence level into §4.11 or into `future-plans/model-non-interchangeability.md`.

Why this gates the prose rather than merely informing it: §4.11's claim is flagged
"not strictly tested, just a conjecture" on Lei's own note. If the comparison has produced
real cross-family data, the flag can soften and cite it; if not, §4.11 stays a conjecture
and the study stays future work. **Do not pick a confidence level from the plan document —
that document is a design, not a result.**

**ch4 coverage — settled by Lei, 2026-09-12.** §4.5, §4.7, §4.9 and §4.12 carry **no notes
by intent**: "they must read ok to me on my print reading pass." So they are *reviewed and
clean*, NOT *unreviewed*. They are re-checked in the **full end-to-end reading pass** after
the per-chapter sweep completes, which is where cross-chapter inconsistency produced by our
own per-chapter rewrites gets caught. §4.12 is worth particular attention there: it holds
the verdicts table, which the §4.8 Condition-1 question would move if that lands.
