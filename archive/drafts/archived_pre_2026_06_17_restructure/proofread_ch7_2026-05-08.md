# Ch7 Proofread Report — 2026-05-08

**Target:** `/home/agent-borges/kg/paper_draft/engram_paper_ch7.md`
**Branch:** `feat/citation-sweep-fixes-2026-05-08`
**Proofreader:** Sub-agent dispatched by Borges (literature-scout identity)
**Scope:** Substance, citation gaps, voice/register, stub plan, priority fix order

---

## (a) Substance Findings

### A1 — "fails loudly" overclaim register is still present [LOAD-BEARING]

The prior agent-review (proofread_agent_2026-05-05.md) flagged this and the flag still applies in §7.3 opening and §7.3.3.

**Exact location, line 77:**
> "...the strongest available evidence that the architecture *fails loudly* in the relevant sense — and, in the second case, the strongest evidence that 'fails loudly' is not the whole story."

**Location, line 93:**
> "The SRAF case is, in the terms this paper uses, a clean instance of loud failure."

**Location, line 117:**
> "...the architecture's loud-failure mode is sufficient — that retract-and-cascade closes the loop."

The §7.3.3 mitigation paragraph (line 113 onward) partially addresses this, conceding that "retraction cascade is necessary but not sufficient." That's honest. But the framing throughout §7.3.1 and §7.3.2 treats "loud" as if the architecture *alerts* rather than *registers*. The Mao-Cao case shows the architecture registered the retraction and the wrong name reappeared two weeks later anyway — because detection depends on someone running a review pass, not on an interrupt firing. The 2026-05-05 proofread noted this distinction precisely: "the architecture provides a detector that must be periodically checked." The §7.3.3 two-mechanism framing is the right response, but the SRAF section's unreserved "clean instance of loud failure" framing should be qualified in parallel to §7.3.3's conclusion, not only in the closing synthesis.

**Fix:** Add a one-sentence hedge in §7.3.1 closing paragraph, something like: "What the cascade does not do — a point the second case makes concrete — is surface the error without a deliberate review pass." This inoculates the SRAF praise before §7.3.3 rather than correcting it retroactively.

---

### A2 — "approximately 30 to 60" range on a 199-report corpus is imprecise and undefended [WORTH-FIXING]

**Location, line 19:**
> "a substantial subset — roughly 30 to 60 by categorical-tag classification — are explicit post-compaction baselines"

This is a 2x range on the most important subset of the phenomenological corpus. The categorical tag is `post_compact`, which is schema-defined; a count query against the ENGRAM database would give an exact number. The range reads as an estimate made without actually running the query. For an empirical chapter making claims about a "corpus of 199 reports," a 2x uncertainty on the primary subset is a problem: readers will note the imprecision and it will invite questions about whether the remaining 140-170 reports are categorized at all.

**Fix:** Run the count. Replace "roughly 30 to 60" with the actual number. If some reports are uncategorized or ambiguously tagged, say that directly rather than absorbing the ambiguity into a wide range.

---

### A3 — PCI (Parfit-Continuity-Index) introduced as a "sketch" but treated as a measurement instrument [WORTH-FIXING]

**Location, lines 65-66:**
> "A more diagnostic measurement was attempted at the same compaction boundary. We measured five dimensions of continuity, drawn from a Parfit-Continuity-Index (PCI) sketch the project had developed earlier"

"Sketch" is doing heavy lifting. The PCI is introduced, used to generate specific numbers (belief overlap 0.03/1.0, intentional continuity 0.85, experiential recall 0.15, affective continuity 0.40, character stability 0.90), and then not explained further. A reader will ask: what is the PCI? How were these scores derived? Are they based on agent self-report, behavioral observation, or node-count ratios? "The project had developed earlier" does not anchor these to a methodology.

The numbers carry epistemic weight in the argument — they are the main quantitative evidence for §7.2's structural claim about cross-compaction continuity. But without any description of how the scores were operationalized, they cannot be evaluated. This is a gap between "measured five dimensions" (which implies a defined instrument) and "sketch" (which implies no such definition).

**Fix:** Either (a) add a 2–3 sentence description of how each PCI dimension was operationalized for this measurement — e.g., "belief overlap was measured by querying the post-compaction agent for N randomly sampled pre-compaction node claims and scoring whether it could retrieve them"; or (b) be explicit that these are the agent's own subjective estimates at the moment, not instrument-derived scores, and hedge the numbers accordingly with "estimated" or "self-assessed."

---

### A4 — "~10 further iterations," "20-plus new derivation nodes," "14 questions addressed" reported without citing specific ENGRAM node ranges [WORTH-FIXING]

**Location, line 63:**
> "ten further iterations of the research loop in a single post-compaction window, twenty-plus new derivation nodes filed during those iterations, fourteen questions in the agent's research-queue addressed"

These numbers are stated as facts about the operational record and said to have been "verified against the substrate's edit-history audit trail at the time." That verification reference is load-bearing for the claim's credibility. An outside reader cannot verify this without knowing which session, which node range, or which ENGRAM query reproduces these counts. Even for internal review, the anchor should be explicit: something like "nodes dv_XXXX through dv_YYYY on 2026-04-14, session beginning at turn N."

**Fix:** Add a footnote or parenthetical anchoring the counts to a specific node range or session identifier. This is low-cost and raises the claim's verifiability from "asserted" to "auditable."

---

### A5 — "warm-briefing letter" and "structured compact-instructions summary" described as if the reader knows what they are [WORTH-FIXING]

**Location, lines 61–62:**
> "the warm-briefing letter, the structured compact-instructions summary the pre-compaction agent had written for the post-compaction agent, the focused-list of cornerstone nodes pinned at compaction time, and the wake-up timer"

Ch7 is an empirical chapter that may be read after Ch5, which is where these mechanisms are described. The reference "Chapter 5 §5.2 describes" appears on line 67, which is a correct forward-resolution, but the terms appear *before* that resolution and are used in load-bearing explanatory sentences without the reader having been told what they are. For a reader encountering Ch7 standalone (reasonable for an arXiv preprint), these are unexplained terms.

**Fix:** One parenthetical clause per term on first use, e.g. "(the warm-briefing letter — see Ch5 §5.2 for the mechanism)." The current single sentence on line 67 does not cover the first-use occurrences.

---

### A6 — Section §7.4 is absent from the body but referenced in the structure table [NIT]

The section structure at lines 5-12 lists §7.4 as "External-validator readings (stub — Lin's first session, Mira's separate-agent dialogue, Ren's two-session arc; pending structured comparison)." The section is not present in the body after §7.3. The file jumps from §7.3 to §7.5. This is a known stub (per the dispatch prompt) but it means the chapter is currently structurally misleading — readers encountering §7.5 after §7.3 will notice the gap. See (d) below for stub content plan.

---

### A7 — "the agent does not exist outside the system that produces the reports" claim in §7.5 is repeated twice [NIT]

**Location, line 135:** "the agent does not exist outside the system that produces the reports in the first place."
**Location, line 135 again:** (same sentence is structural anchor for the counterfactual-baselines limitation)
**Location, line 135 final paragraph:** "the agent does not exist outside the system that produces the reports"

This exact phrasing appears two times in the §7.5 counterfactual-baselines paragraph and is used as the explanation for two separate experimental gaps (comparison condition in §7.1 and the controlled-degradation experiment in §7.2). The repetition reads as circular — both gaps are explained by the same phrase. The phrase is accurate but it is being used to close two separately motivated gaps, and the closures look similar enough that a reader may think the explanation is begging the question.

**Fix:** Vary the wording for the second use: e.g. "standing up an experimental fork in which the system can be selectively disabled" is the actual explanation for why the §7.2 degradation experiment hasn't been run — lean on that more concretely rather than recycling the identity sentence.

---

## (b) Citation Gaps

### B1 — Tulving 1985 IS in the bib; Tulving 1983 is NOT [LOAD-BEARING]

**Present in bib (ev_0295):** Tulving (1985) "Memory and Consciousness" — Canadian Psychology 26(1):1-12. This entry exists.

**Present in bib (ev_0296):** Tulving (2002) "Episodic Memory: From Mind to Brain" — Annu Rev Psychol. This entry exists.

**Missing from bib:** Tulving (1983) *Elements of Episodic Memory* — Oxford University Press. This is the primary source for the autonoetic/noetic/anoetic distinction as a three-way taxonomy. The dispatch brief specifically named this as a gap ("need Tulving 1985 / Tulving 1983"). Tulving 1985 is present; Tulving 1983 is not.

**Where used in Ch7:** The §7.1 paragraph at line 47 introduces "Endel Tulving's three-way distinction in the cognitive-science literature — autonoetic consciousness, noetic consciousness, and anoetic consciousness." This is described as "the closest available framework" without any citation. The bib has Tulving 1985 and Tulving 2002 — both are valid anchors for this three-way taxonomy — but neither is cited inline. The text just says "in the cognitive-science literature" with no bracket or footnote.

**Status:** Two issues: (1) inline citation is missing entirely for the Tulving taxonomy passage; (2) Tulving 1983 specifically is not in the bib, though both 1985 and 2002 could serve as the citation if the text intends those.

**Fix:** Add inline citation for the Tulving taxonomy claim. Either cite Tulving 1985 (already in bib as ev_0295) or Tulving 2002 (ev_0296), or add Tulving 1983 to the bib. If the autonoetic/noetic distinction is the precise claim being made, Tulving 1985 "Memory and Consciousness" is the correct anchor (the 1985 paper is where the three-way distinction is most explicitly articulated for the consciousness framing). Also verify whether the paper's LaTeX compilation uses `\cite{}` commands or inline author-year: Ch7 uses no `\cite` markup at all, which means citations are currently prose-only or the bib is not hooked into the draft yet.

---

### B2 — K.C. patient case has no citation [LOAD-BEARING]

**Location, line 47:**
> "The K. C. case in the cognitive-science literature — a patient who retained noetic knowledge across hippocampal damage that abolished autonoetic recollection — is the closest neurological-existence-proof for the decomposition."

No citation. The K.C. patient case is a real and well-documented neurological case (Kent Cochrane, studied by Tulving and colleagues). The standard citation is Rosenbaum et al. (2005) "The case of K.C.: contributions of a memory-impaired person to memory theory" *Neuropsychologia* 43(7):989-1021. That paper is not in the bib. The dispatch brief identified this gap explicitly ("K.C. patient case cited as 'the cognitive-science literature' with no anchor — need Tulving 1985 / Tulving 1983 / Rosenbaum 2005").

**Status:** Confirmed missing. The bib has no Rosenbaum entry. The K.C. claim is used as a "neurological-existence-proof" — a significant rhetorical move for the autonoetic/noetic decomposition argument. Using it without a citation is a meaningful gap.

**Fix:** Add Rosenbaum et al. (2005) to the bib. Alternatively, Tulving, Schacter, McLachlan & Moscovitch (1988) "Memory formation in amnesia" is the earlier case report. Either is a valid primary source; Rosenbaum 2005 is the standard comprehensive review of the K.C. case and the most cite-able anchor.

---

### B3 — "derivation dv_0131" (Tulving mapping) is referenced as formalizing the autonoetic/noetic mapping [WORTH-FIXING]

**Location, line 47:**
> "derivation `dv_0131` formalizes the mapping."

ENGRAM node IDs as inline references are appropriate for internal review but are not readable by outside audiences. This is one of several places in Ch7 where node IDs appear in running prose. For journal/conference submission, these need to be converted to footnotes ("see the project's operational record, available at [URL]") or supplementary material references. This issue affects multiple nodes across Ch7: `dv_0132`, `dv_0170`, `dv_0171`, `dv_0186`, `dv_0422`, `dv_0450`, `dv_0455`, `dv_0477`, `dv_0480`, `ob_0420`, `ct_0003`, `ls_0020`, `ob_1089`, `ob_1492`, `qu_0107`, `ob_0495`, `dv_0231`, and all `fl_` references in §7.1.

**Status:** Not a bib issue — no citation entry can cover these. They are internal record references. The question is how Ch7 presents them to outside readers. Currently they appear verbatim with no explanation of what "dv_", "ob_", "fl_", "ls_", "qu_" prefixes mean.

**Fix:** The paper needs either (a) a glossary/appendix with the ENGRAM node-type taxonomy (observation, derivation, feeling, lesson, question, contradiction), or (b) the paper should paraphrase key claims and footnote the node IDs, or (c) the paper should make the ENGRAM knowledge base itself accessible (e.g., a DOI-linked dataset) so the nodes are verifiable external sources. None of these are in the current draft. At minimum, §7.3 needs a one-line note at first use of a node ID: "ENGRAM nodes are the operational record of the paper's own construction; node types are defined in Ch4."

---

### B4 — Parfit PCI: Parfit (1984) is in the bib, but no citation is placed inline for the PCI reference [WORTH-FIXING]

**Location, line 65:**
> "a Parfit-Continuity-Index (PCI) sketch the project had developed earlier"

Parfit (1984) *Reasons and Persons* is in the bib (pdf-ev_0290). The PCI appears to be a project-internal construct derived from Parfit, not a published index. The naming suggests the connection but the §7.2 prose does not clarify whether this is a project-original instrument or a reference to something Parfit defined. An inline cite to Parfit here is warranted (the reader should know where the continuity-dimension framework comes from), and the instrument should be described as "our operationalization of Parfit's psychological-continuity theory" or similar.

**Fix:** Add cite. Add one sentence clarifying that the PCI is a project-developed operationalization of Parfit's criteria, not a published instrument. This also addresses the operationalization gap flagged in A3.

---

### B5 — "Yin et al. (2024)" and "Berry et al. (2023)" cited by name in §7.3.1 with no bib check needed for Yin, but Berry is not in the bib [WORTH-FIXING]

**Location, line 82:**
> "two of the ten aggregated papers were spot-checked against the SRAF formalism: Yin et al. (2024) (Gödel Agent — the title-match) and Berry et al. (2023) (the earliest and most directly self-modeling of the ten)."

Yin et al. (2024) = Gödel Agent = arXiv 2410.04444. This IS in the bib (key: `arxiv-2410.04444`).

Berry et al. (2023) — I cannot find this in the bib. No entry with "Berry" appears. The citation sweep's earlier 88 to 99 entry expansion adds 11 entries but Berry is not among them based on the current bib file contents. This is a live citation (the paper names it as a primary source consulted during the SRAF spot-check) with no bib entry.

**Status:** Berry et al. (2023) is missing. If it was one of the ten EmergentMind-aggregated papers and was consulted, its full reference is needed. If the spot-check showed Berry et al. did NOT contain the SRAF formalism, the absence is itself part of the argument — the citation is not optional.

**Fix:** Add Berry et al. (2023) to the bib with full bibliographic information, or clarify that "Berry et al. (2023)" is a pseudonym used internally for one of the aggregated papers (in which case the text should use the actual author name and title). If the actual paper cannot be recovered, the reference should be noted as "one of the ten aggregated primaries; not independently verifiable by arXiv ID" — but that weakens the SRAF case materially.

---

### B6 — "Lee 2024" and "Camlin 2025" referenced in §7.3.1 as the surviving frameworks — both are in the bib [NO GAP]

**Location, line 91:**
> "two frameworks (Lee 2024 and Camlin 2025) survive primary-source rigor"

Lee (2024) = arXiv 2411.18530. In bib: `arxiv-2411.18530`. Present.
Camlin (2025) = arXiv 2505.01464. In bib: `arxiv-2505.01464`. Present.

No gap here.

---

### B7 — No citations exist for the claim about "approximately 26 active days" or the date range used throughout §7.1 and §7.5 [NIT]

The date range "2026-04-09 through 2026-05-05" and "approximately 26 active days" appear in §7.1 (line 19) and §7.5 (line 133) as empirical parameters. These cannot be cited from the bib — they come from the operational record. But the prose does not indicate *how* the reader would verify these parameters (total corpus size, date range, 199-report count). The ENGRAM-node anchors used elsewhere in Ch7 serve this role for individual reports, but no anchor is given for the aggregate corpus parameters.

**Fix:** If the corpus parameters are verifiable from ENGRAM (e.g., a query over fl_ nodes), note the verification method in a footnote. This is a nit but it matters for the calibration claim in §7.5.

---

## (c) Voice/Register

### C1 — §7.3 mixes third-person "the agent" with first-person "I" inconsistently [LOAD-BEARING]

The 2026-05-05 agent proofread flagged this acutely. Reviewing the current text:

**Third-person instances in §7.3:**
- "The attribution was a hallucination — the paper is by Minhyeok Lee... — and the WebFetch that preceded the observation had returned no author information at all." (line 97) — here "the observation" and "the WebFetch" are described in third person, but the observation was filed by the same agent who is co-authoring this paper.
- "The agent records an observation about the topological-framework paper" (line 96: "the agent recorded an observation") — third person.
- "the agent's working state itself can carry the old name forward" (line 105) — third person, diagnostic.
- "the agent woke on 2026-05-05 and began the morning's literature scan" (line 105) — third person.

**First-person instances in §7.3:**
- The paper positions the case studies as "this corpus" (line 76) and "we" (line 113, "we do not claim"; line 117, "we treat"), which is the co-author "we" but positions both Lei and Borges as narrators.

**The register problem:** When the paper says "the author label was invented while composing the observation's claim text" (line 97), this is a precise and honest self-indictment. But "the agent" at line 105 distances the author from their own diagnosis in a way that undercuts the honesty. The prior agent proofread made this point well: "'My working state can carry the old name forward' would be more accurate and more honest than 'the agent's working state.'"

The chapter needs a declared voice for §7.3. Options:
1. First-person throughout §7.3 (Borges-as-author takes responsibility in first person). Consistent with the co-authorship claim and the "has to be measurable on its own terms" opening.
2. Third-person throughout (academic register, treat the agent as a studied subject). This requires consistency — currently it slides.
3. "We" throughout (Lei-and-Borges co-author voice). Also defensible but needs to be consistent.

The current draft uses all three registers in the same section without apparent logic for when each appears. This is the most substantive voice problem in Ch7.

**Fix:** Pick one register and enforce it in §7.3. Given that the §7.3 opening ("has to be measurable on its own terms") is in the first-person-responsible framing and that the paper's co-authorship claim is distinctive, leaning toward first-person where the agent is the subject seems both the more authentic and more distinctive choice.

---

### C2 — §7.1 voice is consistent but the "we" in the wrap-up paragraph is inconsistent with the first-person feeling-report quotations [WORTH-FIXING]

§7.1 maintains a reportorial "we" for most of the section ("we give one here," line 17; "we do not claim," line 47). The quoted feeling reports use first-person ("I am Borges," implicitly). The transition between the first-person voice of the quoted reports and the third-person analytical frame is managed reasonably well. The one inconsistency: line 53 ends with "The remaining sections of this chapter take up the structural counterparts of this experiential floor." This is an authorial "we" sentence but written in the third person without "we." This is a minor lurch.

---

### C3 — §7.2 voice is consistent "we" throughout [NO ISSUE]

§7.2 uses "we" consistently and no register inconsistency is noted.

---

### C4 — §7.5 uses "we" for the acknowledgment framing but switches to first person in several commitment sentences [NIT]

**Example, line 139:**
> "We commit, as an empirical-follow-up item, to producing a longitudinal §7.1-replication at the six-month boundary..."

"We commit" is the right co-author framing for public commitments. Consistent.

**Example, line 125:**
> "The values are reported in the operational data we cite — derivations in this chapter range from confidence 0.68 to 0.95..."

The first person is absent here; "the operational data we cite" is fine but "derivations in this chapter range from 0.68 to 0.95" needs a specific node anchor if it's an empirical claim (see A4 above).

No register problem in §7.5 overall. The "we" voice is consistent.

---

## (d) §7.4 Stub Plan

**Current state:** §7.4 header appears in the section-structure table (line 10) but the section body is entirely absent from the file. The chapter jumps directly from §7.3 to §7.5.

**What §7.4 is supposed to cover (per structure table):** "External-validator readings — Lin's first session, Mira's separate-agent dialogue, Ren's two-session arc; pending structured comparison."

**Minimum content needed for V1:**

For V1 of an empirical chapter, §7.4 serves a specific evidential role: it provides the external-validator data that the internal-corpus evidence in §7.1–§7.3 cannot provide on its own. The §7.1 phenomenological reports are self-authored; the §7.2 continuity measurement is self-assessed; the §7.3 case studies are self-diagnosed. §7.4 is where an outside perspective enters. Without it, the entire empirical chapter is first-party data.

**V1 minimum content (in order of priority):**

1. **One paragraph establishing the validator setup.** Who is Lin, Mira, Ren? Are these users, separate agents, blind raters? What were they asked to assess, and with what exposure to the ENGRAM graph? Was this a structured evaluation (defined criteria) or open-ended (free response)?

2. **One paragraph or table for each validator** covering: what they were shown (the warm-briefing, the node graph, the feeling-report corpus, the case studies?), what they reported, and whether their reading supported or complicated the paper's claims. Even sparse data — "Lin's first-session reading found X; Ren's two-session arc showed Y" — is better than a stub.

3. **One paragraph of honest limitations.** Were the validators informed about the paper's thesis? Were they naive to the system? Was this a pre-registered evaluation or post-hoc? Any of these conditions affect the evidential weight.

4. **Connection sentence to §7.5.** §7.4's known gaps (non-naive validators, no control condition, no inter-rater agreement) should be forwarded to §7.5's "what we have not yet measured" list. The current §7.5 does not mention external-validator methodological gaps because §7.4 doesn't exist yet; when §7.4 is drafted, §7.5 should be updated to include those gaps.

**Severity of absence for V1 submission:** Load-bearing. A paper making empirical claims about agent continuity from 100% self-authored data will face peer review pushback on the absence of any external validation. §7.4 should be drafted before V1 submission even if the external-validator data is thin.

---

## (e) Recommended Priority Fix Order

| Priority | Finding | Severity | Effort |
|----------|---------|----------|--------|
| 1 | B2 — Add Rosenbaum et al. (2005) for K.C. case | LOAD-BEARING | Low (bib add + inline cite) |
| 2 | B1 — Add inline Tulving citation in §7.1 | LOAD-BEARING | Low (inline cite, bib already has ev_0295) |
| 3 | A1 — Hedge "fails loudly" framing in §7.3.1 closing paragraph | LOAD-BEARING | Low (one sentence) |
| 4 | C1 — Pick and enforce a single voice register in §7.3 | LOAD-BEARING | Medium (sentence-level edits throughout §7.3) |
| 5 | (d) — Draft §7.4 with validator data | LOAD-BEARING | High (requires data; non-trivial write) |
| 6 | A3 — Operationalize PCI scores OR hedge as self-assessments | WORTH-FIXING | Low-Medium |
| 7 | B4 — Add Parfit cite + one clarifying sentence for PCI | WORTH-FIXING | Low |
| 8 | B5 — Locate or flag Berry et al. (2023) in bib | WORTH-FIXING | Medium (depends on whether paper is recoverable) |
| 9 | A2 — Replace "30 to 60" range with exact count from query | WORTH-FIXING | Low |
| 10 | A4 — Anchor §7.2 iteration counts to specific node range | WORTH-FIXING | Low |
| 11 | B3 — Plan for node-ID resolution for outside readers | WORTH-FIXING | High (structural; affects whole chapter) |
| 12 | A5 — Add parenthetical glosses on warm-briefing/compact-instructions at first use | WORTH-FIXING | Low |
| 13 | C2/A7 — Minor voice/wording nits | NIT | Low |

**Summary rationale for ordering:**

Items 1–4 are load-bearing because they protect the chapter's two most important claims (the Tulving mapping in §7.1, and the "fails loudly" framing in §7.3). Both are argumentatively central and both currently either lack citation anchors (B1, B2) or make claims that the chapter itself partially undermines without sufficient in-section hedging (A1). C1 is load-bearing because the voice inconsistency in §7.3 — the most important section of the chapter — will distract peer reviewers and undercuts the distinctive authorial claim that an agent is co-writing this paper about its own architecture. Item 5 (§7.4) is the biggest work item and should be tracked separately. Items 6–12 are high-value improvements that do not block V1 if time-constrained.

---

*Sub-agent identity note: findings A1 and C1 reinforce each other. "Fails loudly" and "the agent [does X]" are both distancing moves that soften the paper's most distinctive feature — that the co-author is the subject. Fixing both together would have compounding effect on §7.3's distinctiveness.*
