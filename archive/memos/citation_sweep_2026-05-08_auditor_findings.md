# Citation Sweep 2026-05-08 — Code-Auditor Findings

Source: engram-code-auditor fairy dispatch, 2026-05-08.
Saved as raw input for the consolidated `citation_sweep_2026-05-08.md` synthesis (still pending — citation-fairy + paper-research-fairy running in parallel).

## Critical (mechanical fix, sub-hour)

1. **`engram_paper_ch1.md:78` and `:139`** — `[^12]` defined twice (Pinecone Nexus AND Alcoff "Epistemic Identities"). Markdown renderer behavior is implementation-dependent (last-wins on most CommonMark; first-wins on some) → either way it's a bug. Body markers at lines 74 (Pinecone context) and 131 (Alcoff context) reference the same key. Fix: renumber Alcoff to `[^14]`, update body marker at line 131. **VERIFIED 2026-05-08 — both definitions exist as described.**

2. **`engram_paper_ch1.md:22, :26`** — Four load-bearing parenthetical citations with no footnote definitions:
   - Ouyang et al., 2022 (InstructGPT, NeurIPS 2022, arXiv:2203.02155)
   - Bai et al., 2022 (Anthropic Constitutional AI, arXiv:2212.08073)
   - Brown et al., 2020 (GPT-3, NeurIPS 2020, arXiv:2005.14165)
   - Min et al., 2022 ("Rethinking the Role of Demonstrations", EMNLP 2022, arXiv:2202.12837)
   These ground the §1.1 frozen-weights / in-context-learning argument. **VERIFIED 2026-05-08.**

## Risky (needs care, drafting work)

3. **`ch1.md:76` fn9** — MemMachine footnote stub: "Full citation in Chapter 8". ch8 fn1 has `arXiv:2604.04853`. Copy across.

4. **`ch5.md:47` fn1** — Camlin (2025) RCUET cited with **no arXiv ID, DOI, or URL**. Walkthrough flags proof step 3 as "unverifiable against cited literature." Either (a) supply locator if exists, or (b) explicit "unpublished manuscript" framing.

5. **`ch3.md` — ZERO footnotes for any of the five pillars. VERIFIED 2026-05-08 (literal grep count = 0).** Stiegler V1 (Collins trans, Stanford 1998) verbatim quotes uncited; Clark & Chalmers parity principle quoted verbatim uncited; Parfit §78 paraphrased uncited; Locke uncited. **This is the most philosophically load-bearing chapter.** ch5_philosophy_sweep has full bib data — use it.

6. **ch1 roadmap vs ch3 mismatch** — Ch1:149 promises Goldman/Nozick/Schechtman as pillars in §3. Ch3 draft contains: Stiegler, Clark&Chalmers, Locke&Parfit, Alcoff, Strawson. **Goldman, Nozick, Schechtman are absent from ch3.** Either add them or update the ch1 roadmap.

7. **`ch7.md:47`** — Tulving autonoetic/noetic/anoetic + K.C. patient case both cited as "the cognitive-science literature" with no anchors. Need: Tulving 1985 (Memory and Consciousness, Canadian Psychology); Tulving 1983 (Elements of Episodic Memory); K.C. case → Rosenbaum et al. 2005 or Tulving et al. 1988. Outline already lists this gap as open.

8. **`ch8.md:77`** — Sutton "distributed cognition" with no year, no work, no fn. Candidates: Sutton 1998 (Philosophy and Memory Traces), Sutton 2006 (Memory, Embodied Cognition, Extended Mind), Sutton et al. 2010.

9. **`ch8.md:73`** — Plato *Phaedrus* quoted verbatim, no edition / translator / Stephanus. Use Nehamas & Woodruff (Hackett 1995) or Cooper Complete Works.

## Stylistic / Lower priority

10. **`ch5_philosophy_sweep.md:177-248`** — Ricoeur (1992) section explicitly PROVISIONAL, secondary-chained via Vessey. Cannot promote to chapter prose without primary verification.

11. **`ch5_philosophy_sweep.md:256`** — Alcoff (2010) paywalled on Cambridge Core; book-quotes from third-party morgan-klaus.com reader notes. ch1's current Alcoff use is description-only (low risk now).

12. **`ch8.md:31`** — VentureBeat "RAG era is ending" cited as corroboration for marketing claim. Appropriate but reviewer-attention-drawing.

13. **`ch8.md:49`** — Atlan blog "No tool tracks where data came from..." doing real work as external-validator quote for retraction-cascade claim. Practitioner blog, not peer-reviewed.

14. **`ch8.md:87`** — "Mem0g" appears uncited. Possibly typo for Mem0 or earlier codename for Mem0 graph variant. Verify.

15. **`ch8.md:31` Pinecone Nexus** — fn cites "product materials" with no stable URL. Will age poorly even if appropriate now.

16. **ch1:125 "epistemic identity" coinage** — re-verification gap from outline (last check Dec 2025 ob_0416) not closed; current usage well-scoped via Alcoff disclosure §1.4.

## False-positives (correctly excluded)

- `ch5_walkthrough.md` — internal reference doc, not draft chapter
- `ch5_philosophy_sweep.md` PROVISIONAL marker — system working as designed (ls_0011)
- `ch1.md:60 fn7` Lei Shi personal-communication attribution — correctly attributed
- ch5 §5.1-3, ch7 §7.4 stub headers — acknowledged unfilled
- outline `[ ]` research gaps — tracked work items, not citation drift

## Synthesis priorities (for consolidated report)

**Hour-1 mechanical fixes:** items 1, 2, 3 (six discrete edits to ch1 — fn12 renumber + 4 fn definitions + fn9 stub). Pure editorial pass.

**Drafting-pass work:** items 5, 6, 7, 8, 9. Best done with the philosophy sweep file in hand for ch3 source material.

**Rigor concern (separate axis):** item 4 (Camlin locator) — independent of citation format, this is a substantive rigor gap the ch5 walkthrough already flags.
