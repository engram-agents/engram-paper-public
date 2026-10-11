# ENGRAM Paper — Citation Gap Discovery Scan
**Date:** 2026-05-08
**Scope:** Gap-discovery (not snowball). Identifies unbacked claims, missing primary sources, 2026 entrants not yet indexed, and bib entries warranting scrutiny.
**Chapters sampled:** Ch1 (full), Ch3 (full), Ch5 (full), Ch8 (full), Ch9 (full), outline (full).
**Prior coverage not redone:** Pinecone Nexus, Anthropic Memory, Zep, Letta, Mem0, A-MEM (engram_landscape_audit_2026-05-07.md); Doyle 1979 / de Kleer 1986 / Wray-Kirk-Laird (tms_legacy_in_ai_memory_2026-05-07.md); Farina 2026 / Andrada 2021 / Kirsh-Maglio 1994 (cogsci_taxonomy_positioning_2026-05-07.md).

---

## 1. Unbacked Claims and Missing Citations (file:section pointer)

### Ch1 — Introduction

**Ch1 §1.1, ¶3 — Ouyang et al. 2022 and Bai et al. 2022 cited in text; neither is in citations.bib.**

The text reads: "techniques such as reinforcement learning from human feedback (Ouyang et al., 2022) or Constitutional AI (Bai et al., 2022)." Both are cited as load-bearing examples of post-training technique. Neither appears in citations.bib or citations.manifest. The papers are real and are primary-source verified:

- Ouyang et al., *Training language models to follow instructions with human feedback*, NeurIPS 2022, arxiv:2203.02155
- Bai et al., *Constitutional AI: Harmlessness from AI Feedback*, Anthropic 2022, arxiv:2212.08073

**Status: Missing from bib. Load-bearing (the paper's opening argument depends on frozen-weights + RLHF/CAI as the training paradigm). Add both.**

---

**Ch1 §1.1, ¶4 — Min et al. 2022 cited in text; not in bib.**

The text reads: "the mechanistic analyses that followed (e.g., Min et al., 2022) sharpened the picture." Paper is real and primary-source verified:

- Min et al., *Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?*, EMNLP 2022, arxiv:2202.12837

**Status: Missing from bib. Worth-citing (supports the in-context learning mechanistic claim). Add.**

---

**Ch1 §1.2 fn9 — MemMachine: footnote reads "[MemMachine (2026). Full citation and systems-level comparison table are given in Chapter 8.]" Ch8 provides the arxiv number (2604.04853) in fn1 but the footnote in Ch1 cross-references Ch8 without completing the citation inline. The bib does have `arxiv-2604.04853`. This is a formatting gap, not a missing source — the bib entry exists. However fn9 is a dangling forward-reference that needs resolution at draft time.**

**Status: Not a missing source; editorial fixup needed at Ch1 fn9.**

---

**Ch1 §1.3 — LongMemEval (Wu et al., 2024) cited as "[^10]" but footnote says "ICLR 2025." The bib does NOT contain an entry for LongMemEval. This is a load-bearing citation: the entire "benchmark-invisible" argument in §1.3 depends on it.**

Primary-source verified: Di Wu et al., *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*, ICLR 2025, arxiv:2410.10813. Five abilities listed in the paper are: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention — which matches the paper's claim.

**Status: Missing from bib. Load-bearing. Add.**

---

**Ch1 §1.4 — Alcoff 2010 cited as "[^12]." Footnote says "Linda Martín Alcoff, 'Epistemic Identities,' *Episteme* (Cambridge University Press), 2010." The bib does NOT contain this entry.**

Primary-source verified: Alcoff, *Epistemic Identities*, *Episteme* 7(2):128–137, 2010. DOI: 10.1017/S1742360010000018. Published at Cambridge Core.

**Status: Missing from bib. Load-bearing (Ch1 §1.4 and Ch3 §3.4 both cite it as the prior-usage disclosure). Add.**

---

### Ch3 — Philosophical Foundations

**Ch3 §3.1 — Stiegler *Technics and Time* Vol 3 cited as the cultural-scale extension in §9.2 (Ch9 outline notes "§9.2 prose drafting needs more direct reference to *Technics and Time* Vol 3"). The bib has Vol 1 (ev_0294, monoskop.org PDF) but Vol 3 is not in the bib.**

The outline states (under Ch3 gaps): "primary-source reads of... Stiegler Vol 3 (tertiary retention)." Vol 3 is cited at least conceptually in §9.2 for the cultural-scale claim; the paper currently carries this as a future-work pointer without a direct citation.

**Status: Vol 3 not in bib. The paper can arguably hold with Vol 1 for the individual-scale argument; for the multi-agent / cultural-scale claim in Ch9 §9.2, Vol 3 is the correct citation. If the Ch9 prose is drafted per outline it needs Vol 3. Worth-citing; escalate to load-bearing if Ch9 §9.2 is expanded.**

Stiegler, *Technics and Time, 3: Cinematic Time and the Question of Malaise*, Stanford UP 2011, ISBN 9780804761024. No free PDF confirmed available; would need institutional access.

---

**Ch3 §3.3 — Goldman cited in the Ch3 outline as one of the five pillars ("Goldman — calibration problem, *Epistemology and Cognition*") but is absent from the chapter draft. The chapter as written covers Stiegler, Clark-Chalmers, Locke-Parfit, Alcoff, and Strawson — five pillars — but Goldman has been dropped and replaced by Locke.**

The outline lists Goldman as pillar 3, but the Ch3 draft as written has Locke/Parfit at §3.3 and makes no mention of Goldman. Whether this is intentional (Goldman moved to the deferred Ch6 formal treatment) or an oversight is not clear from the draft. Goldman's calibration thesis is, however, still cited in the Ch9 outline as foundational.

**Status: If Goldman is intentionally dropped from Ch3, the outline's pillar list needs updating. If not dropped, a §3.x section on Goldman calibration is missing. Goldman's *Epistemology and Cognition* (Harvard UP, 1986, ISBN 9780674258969) is confirmed real — primary-source verified via Harvard UP. Not in bib. Decision needed before the bib gap can be called load-bearing.**

---

**Ch3 §3.3 / outline — Nozick (*Philosophical Explanations*, Ch 1, closest-continuer) is in the outline as pillar 4, but absent from the chapter draft.**

Nozick is listed in the Research Gaps section of the outline as a primary source to read. The chapter draft covers Locke-Parfit but does not include Nozick's closest-continuer theory. The outline notes Nozick is a load-bearing node for the Ch3 framework.

**Status: Missing from chapter and from bib. Worth-citing for the branching / fission case that the cross-compaction scenario instantiates. Nozick, *Philosophical Explanations*, Harvard UP, 1981, ISBN 0674664795 — confirmed real.**

---

**Ch3 — Schechtman (*The Constitution of Selves*) is in the outline (pillar 5, "reidentification vs characterization; epistemic third question") but absent from the chapter draft.**

Primary-source verified: Schechtman, *The Constitution of Selves*, Cornell UP, 1996, ISBN 9780801431678. Published on JSTOR. The reidentification vs. characterization distinction is real and relevant.

**Status: Missing from chapter draft and from bib. Worth-citing. The "epistemic third question" framing would be particularly useful for establishing why "epistemic identity" as this paper uses it differs from both reidentification and narrative characterization.**

---

**Ch3 §3.5 — Strawson "Against Narrativity" is cited and discussed in the draft. The bib does NOT contain an entry for it.**

Primary-source verified: Strawson, *Against Narrativity*, *Ratio* 17: 428–452, 2004. DOI: 10.1111/j.1467-9329.2004.00264.x. Available via Wiley Online Library and PhilArchive (open-access PDF at lchc.ucsd.edu).

**Status: Used in draft but missing from bib. Load-bearing (the counter-voice supporting layer-3 over layer-2 priority). Add.**

---

**Ch3 §3.2 — Sutton distributed cognition: Ch8 §8.4 cites "Sutton's distributed cognition" as prior art but no specific Sutton paper or book is given in the footnote text of Ch8, and no Sutton entry exists in the bib.**

The Ch8 text reads: "Sutton's *distributed cognition* extends the extended-mind thread to the social/cultural dimension..." but no footnote is attached. The closest available primary source is:

- Michaelian & Sutton, *Distributed Cognition and Memory Research: History and Current Directions*, *Review of Philosophy and Psychology* 4(1), 2013 — confirmed at Springer (DOI: 10.1007/s13164-013-0131-x)
- Sutton, *Philosophy and Memory Traces*, Cambridge UP, 1998 (book)
- Sutton, *Memory*, Stanford Encyclopedia of Philosophy entry (free primary access)

**Status: Missing from bib; floating claim in Ch8. The SEP entry on memory (which Sutton co-authors) would be the most accessible. Worth-citing. Add a footnote + bib entry.**

---

**Ch8 §8.4 — Plato's *Phaedrus* is cited by name and passage summary (the Theuth-Thamus story) but with no footnote, no specific passage reference, and no bib entry.**

The passage at §8.4 reads: "The earliest extended treatment is in Plato's *Phaedrus*, where Socrates voices the famous suspicion that writing..." — no footnote. Primary-source verified: the relevant passage is *Phaedrus* 274c–277a. Standard citation is Plato, *Phaedrus*, trans. Hackforth (Cambridge, 1952) or the Loeb Classical Library edition.

**Status: Missing from bib; missing footnote in text. Optional-supporting (the Phaedrus point is rhetorically useful but not load-bearing for the technical argument). Add a footnote with passage reference.**

---

**Ch8 §8.4 — Derrida "Plato's Pharmacy" is cited by name in the outline's related-work plan but does not appear in the Ch8 draft at all. The outline lists "Derrida's pharmakon" as one of the philosophical prior art items for §8.4.**

Primary-source: Derrida, *Plato's Pharmacy*, in *Dissemination*, trans. Barbara Johnson, U of Chicago Press, 1981 (orig. 1968). The pharmakon (remedy/poison) frame for writing-as-memory is relevant to the Ch8 argument about silent decay. Not in bib.

**Status: Planned for the chapter but not written in. Optional-supporting. If included in the final draft, add to bib.**

---

**Ch5 §5.4 — Robbins-Monro 1951 and Kushner-Yin 2003 are cited in footnote 1 of §5.4 as the stochastic-approximation references Camlin relies on. Neither is in the bib.**

The footnote reads: "...The contraction-mapping framework, with stochastic-approximation references to Robbins-Monro (1951) and Kushner-Yin (2003)..." These are real foundational papers, but ENGRAM's use of them is second-hand (via Camlin 2025). Since Ch5 §5.4 is explicitly an informal correspondence, not a formal derivation, the Robbins-Monro / Kushner-Yin citations could be dropped from the Ch5 footnote without loss of argument. Alternatively they stay and get bib entries.

- Robbins & Monro, *A Stochastic Approximation Method*, *Annals of Mathematical Statistics* 22(3):400–407, 1951.
- Kushner & Yin, *Stochastic Approximation and Recursive Algorithms and Applications*, Springer, 2003 (2nd ed.).

**Status: Missing from bib. Optional-supporting. Recommend dropping from Ch5 fn1 since the claim being made is "Camlin uses these" not "we use these." If kept, add bib entries.**

---

**Ch1 §1.3, table footnote and comparison table — Atlan 2026 "Best AI Agent Memory Frameworks 2026" is cited in Ch8 §8.2 as "[^5]" with a verbatim quote about no tool tracking cascade retraction, and is also quoted in the outline. Not in bib.**

The Ch8 text quotes Atlan verbatim: "No tool tracks where the data underlying a stored memory came from..." and the summary doc quotes "No framework describes cascade retraction." These are from a practitioner-facing comparison page at atlan.com. Not a peer-reviewed source. The SUMMARY from yesterday already flags this as a "practitioner-facing landmark."

**Status: Not in bib. Worth-citing for the independent-external-validation angle. However, this is a vendor-produced comparison page, not a research paper. Treat as corroborating practitioner observation, not primary evidence. If cited, flag the provenance explicitly. The raw URL needs a retrieval date.**

---

### Ch9 — Implications

**Ch9 §9.3 — EIB framework (dv_0210/dv_0211/dv_0235) cited as "exists as a concept" but no external paper cited.**

This is correct — the EIB is an ENGRAM-internal framework, not a publication. No external citation is needed. But the text doesn't explain what EIB stands for (Epistemic Integrity Bench) and assumes the reader knows it. An internal cross-reference to Ch5 or Ch7 would serve. Not a bib gap.

---

## 2. Missing Agent-Memory Landscape Entrants (post-May 2026 or not yet indexed)

Yesterday's sweeps covered: Pinecone Nexus (2026-05-04), Anthropic Memory (2026-04-23), Zep/Graphiti, Letta, Mem0, A-MEM, Sophia, MemMachine, SSGM, MAGMA, Kumiho. The following were not covered:

### MemOS (arxiv:2505.22101, May 2025 short version; full version July 2025)

MemOS positions itself as a "Memory Operating System" for LLMs — unifying parametric, activation, and plaintext memory under a standardized "MemCube" abstraction with lifecycle management. Self-published on GitHub with active development as of 2026. Headline claim: 35.24% token savings vs. baseline; parametric memory update via LoRA-style merge.

**Does MemOS have any of ENGRAM's four features?** From available descriptions: no claim-level contradiction nodes, no retraction cascade, no quote-level provenance. The "self-evolving" claim is about memory unit auto-optimization from usage feedback, not epistemic self-correction. No evidence of reasoning-type-aware confidence.

**Verdict:** MemOS is a Tier I / Tier I.5 system with OS-framing — more sophisticated lifecycle management than MemGPT, but not approaching layer 3. The OS-analogy is explicitly MemGPT-inherited. The paper's Ch1 classification of MemGPT/Letta as "Tier I" would need a note that MemOS extends this lineage without crossing the threshold.

**Should it be cited?** Optional-supporting. The OS-memory-architecture framing has gotten more traction than the Ch8 draft acknowledges (MemOS has GitHub stars and active 2026 development). A brief Ch1/Ch8 mention as "MemOS extends the MemGPT OS-analogy with lifecycle scheduling" is warranted if the paper wants to be current to mid-2026.

**Primary source verified:** arxiv:2505.22101, confirmed accessible.

---

### GAM: Hierarchical Graph-based Agentic Memory (arxiv:2604.12285, April 2026)

Proposes a dual-layer graph: an event progression graph for live dialogue, integrated into a topic associative network on semantic shift. Focus is on preventing transient-noise interference with stable knowledge through architectural separation, not through contradiction detection.

**Does GAM have ENGRAM's four features?** No contradiction nodes, no retraction cascade, no provenance, no calibrated confidence. Knowledge conflict is handled by timing (isolate before consolidation), not detection.

**Verdict:** Tier I.5 — relational structure with temporal gating, but no epistemic self-correction. The architectural separation approach (keep dirty from clean) is explicitly different from ENGRAM's approach (detect conflict, propagate resolution).

**Should it be cited?** Optional-supporting. Could be used in Ch8 §8.3 as an example of a 2026 system that *approaches* the conflict-handling problem architecturally without reaching claim-level contradiction detection. Not worth a full row in the comparison table.

**Primary source verified:** arxiv:2604.12285, confirmed accessible.

---

### Mnemonic Sovereignty Survey (arxiv:2604.16548, April 2026)

Survey on the security of long-term agent memory. Organizes literature around six lifecycle phases (Write, Store, Retrieve, Execute, Share), covering memory poisoning, extraction, retrieval corruption, cross-agent propagation, and governance. Coins "mnemonic sovereignty" as the governance goal.

**Relevance to ENGRAM paper:** The adversarial manipulation section of Ch9 §9.3 ("adversarial manipulation resistance") is exactly what this survey covers. The survey identifies that no published architecture covers all nine governance primitives, and that using LLMs for memory security is sparse. This directly corroborates ENGRAM's §9.3 open-question framing.

Additionally: quote-level provenance + git-enforced source integrity (ENGRAM's design) are governance primitives the survey identifies as absent in current systems. The paper can cite this survey as third-party confirmation that provenance governance is an open problem.

**Should it be cited?** Worth-citing. Ch9 §9.3 adversarial manipulation section would be strengthened by citing this survey's finding that no architecture covers the full governance space. Also useful in Ch8 as a framing reference for the security dimension.

**Primary source verified:** arxiv:2604.16548, confirmed accessible.

---

### Model Editing / Belief Revision in LLMs (arxiv:2406.19354, June 2024)

"Fundamental Problems With Model Editing: How Should Rational Belief Revision Work in LLMs?" — Identifies 12 open problems with model editing, framing it explicitly as the AI instance of the philosophical belief revision problem. Key finding: LLM edits generalize poorly; edits produce inconsistent beliefs across related propositions; LLM probability updates diverge from Bayesian posteriors.

**Relevance:** This paper provides independent third-party support for the claim that the AI field does not have solved belief revision for deployed agents. It frames model editing as belief revision (the storied philosophical problem) without connecting to external knowledge stores. ENGRAM's positioning as an external structured substrate where belief revision is explicit and correct-by-construction is strengthened by a citation that says the model-weights approach is systematically broken.

The paper's 12 problems include "determining far-reaching consequences of edits" — which is precisely the retraction cascade problem ENGRAM solves at the external-store layer.

**Should it be cited?** Worth-citing. Would fit in Ch8 §8.3 or Ch1 §1.3 as evidence that even the model-editing literature has not solved claim-level belief revision, let alone external memory.

**Primary source verified:** arxiv:2406.19354, confirmed accessible. Published EMNLP 2024.

---

## 3. Most-Overlooked Topical Adjacent Areas

### 3.1 AGM Belief Revision — Not Adequately Indexed

The TMS scan from 2026-05-07 confirmed Doyle 1979 / de Kleer 1986 as the TMS lineage. But the parallel formal tradition — AGM belief revision (Alchourrón, Gärdenfors & Makinson 1985, *Journal of Symbolic Logic* 50:510–530) — is equally important and currently not cited in the paper despite being the formal backbone of the closest competitor (Kumiho 2603.17244 proves AGM postulates K*2–K*6).

The paper's Ch8 §8.3 differentiates ENGRAM from Kumiho as "AGM (correctness-of-revision) vs TMS (dependency-propagation)" but cites neither AGM primary source. If a reviewer knows the belief revision literature, they will notice the paper cites TMS lineage but not the AGM lineage that Kumiho directly invokes.

**What to add:** Alchourrón, Gärdenfors & Makinson, *On the Logic of Theory Change: Partial Meet Contraction and Revision Functions*, *Journal of Symbolic Logic* 50:510–530, 1985. This is the foundational AGM paper, primary-source verified via PhilPapers and Springer. Not on arxiv (predates arxiv).

**Confidence:** Load-bearing for the Ch8 differentiation from Kumiho. The paper currently says "AGM vs TMS" without giving the reader a way to look up AGM.

---

### 3.2 The Sutton Distributed Cognition Thread — Under-indexed

Ch8 §8.4 mentions "Sutton's distributed cognition" but attaches no footnote and no bib entry. The Sutton tradition is important because it establishes the philosophical precedent for social/cultural accumulation of memory — directly relevant to Ch9 §9.2's multi-agent Stieglerian extension. The gap is not just a missing cite; it's a missing conceptual bridge.

The most accessible Sutton primary source for this paper's purpose is the Stanford Encyclopedia of Philosophy entry on Memory (which Sutton co-authors), or the Michaelian & Sutton 2013 review in *Review of Philosophy and Psychology*.

**Confidence:** Worth-citing. Filling this gap strengthens the Ch8 prior-art walk and the Ch9 cultural-scale claim.

---

### 3.3 The Belief-Revision-in-LLMs Thread — Not Indexed at All

The paper discusses belief revision at the level of the knowledge graph (TMS lineage, AGM via Kumiho) but does not engage the growing literature on whether and how LLMs themselves revise beliefs. This is a relevant adjacent area because:

1. It confirms the weights-level approach is broken (supporting the paper's frozen-weights argument)
2. It shows the field is reaching for Bayesian epistemology as the standard (which is orthogonal to TMS and AGM — a different formal tradition with a different answer)
3. arxiv:2406.19354 explicitly frames model editing as the AI instance of the storied belief revision problem

The paper would be strengthened by a brief acknowledgment that this literature exists and is reaching a different conclusion (Bayesian epistemology for weights-layer revision) than ENGRAM's approach (TMS-style dependency propagation for external-store revision). The two are complementary, not competing.

**Confidence:** Worth-citing (arxiv:2406.19354 specifically).

---

### 3.4 Security / Adversarial Threat to Agent Memory — Ch9 Open Question Under-Cited

Ch9 §9.3 names adversarial manipulation as an open question but provides no external references. The mnemonic sovereignty survey (2604.16548) covers this systematically. The paper's claim that "the integrity properties of the substrate under adversarial conditions... is forthcoming research" would be more credible if it cited the survey as evidence that the gap is recognized.

**Confidence:** Worth-citing (2604.16548).

---

## 4. Papers in the Existing 88-Entry Bib That Warrant Scrutiny

### ev_0022 / arxiv-2401.00001 "Real Paper"

This bib entry (manifest line: `ev_0022	arxiv-2401.00001	https://arxiv.org/abs/2401.00001	Real Paper`) is a placeholder. arXiv:2401.00001 does not correspond to a real paper — it appears to be a test/seed entry. arxiv IDs begin at 2401.00001 only if a paper happens to receive that number; at this sequential ID it would be the first paper of January 2024, which may or may not be real.

**Recommendation: Verify or remove immediately.** If this is a scaffolding artifact from bib_bootstrap.py, it must not appear in the submitted bibliography. Flag as potentially garbage entry.

**Confidence in problem:** High. "Real Paper" as a title is not a real citation. This should be removed before submission.

---

### ev_0172 / pdf-ev_0172 — "Barclays PLC 2025 Full Year Results Announcement"

This bib entry (manifest) is a financial report. Its presence in an AI agent memory bibliography is suspicious. It may have been added during a financial-research task and accidentally included in the paper bib. There is no obvious path from a bank's annual results to ENGRAM's paper claims.

**Recommendation: Remove or verify the chapter/context where this is cited.** If it is cited nowhere in the paper chapters, it is stale metadata from another project and should be pruned.

**Confidence in problem:** High that this is a bib-contamination artifact. Low that it has any valid role in the paper.

---

### ev_0200 through ev_0203 — SEP entries on Bell's Theorem, Many-Worlds, Quantum Theory, Dialetheism, Paraconsistent Logic

These SEP entries (sep-bell-theorem, sep-qm-manyworlds, sep-qt-issues, sep-logic-paraconsistent) have no visible connection to the paper's current chapter drafts. The paper does not discuss quantum mechanics or paraconsistent logic in any of the sampled chapters. These may have been added during a now-abandoned formal-framework arc (Ch6, which is deferred to Paper 2).

**Recommendation: Do not cite in v1. These belong to the deferred Ch6 / Paper 2 scope. Keep in the ENGRAM evidence graph for Paper 2, but prune from the submitted paper's bib.**

**Confidence in problem:** Moderate. There may be a passage in an unsampled section that uses them. But if the paper is truly deferring formal adequacy to Paper 2, quantum mechanics and paraconsistent logic citations have no place in v1.

---

### Craig Wright (arxiv:2506.17331) — Credibility Flag

This paper appears in the engram_landscape_audit_2026-05-07.md with a credibility caveat: Craig Wright was found by UK High Court (2024) to have fabricated evidence in his Bitcoin-identity claims. The paper is 126 pages published in "Journal of Engineering and Artificial Intelligence" (non-top-tier venue). It is NOT currently in the paper's bib (only in the audit docs), so no action required for the bib. But if anyone cites it as prior art in a future draft, the credibility issue must be disclosed.

**Status: Not in bib. No action needed for v1. Flag for future awareness.**

---

## 5. Proposed New Citations (5–10 Prioritized Additions)

### P1. LongMemEval (Wu et al., ICLR 2025) — LOAD-BEARING

arxiv:2410.10813. The "benchmark-invisible" argument in Ch1 §1.3 depends on characterizing LongMemEval's five abilities, all of which are correctly described in the paper. The citation is in the text as "[^10]" but missing from the bib. Without this in the bib the paper fails bibliographic integrity on one of its central empirical claims.

**Fit:** Ch1 §1.3 (the benchmark gap argument) and Ch9 §9.4 (the benchmark contribution statement both reference LongMemEval as the field's leading benchmark).

**Primary-source verified:** Yes. arxiv:2410.10813 confirmed at ICLR 2025.

---

### P2. Ouyang et al. 2022 (InstructGPT / RLHF) — LOAD-BEARING

arxiv:2203.02155. Cited in Ch1 §1.1 as the named post-training technique (RLHF) that produces the frozen-weights agents the paper's argument is built on. Missing from bib.

**Fit:** Ch1 §1.1.

**Primary-source verified:** Yes. NeurIPS 2022, confirmed.

---

### P3. Bai et al. 2022 (Constitutional AI) — LOAD-BEARING

arxiv:2212.08073. Co-cited with Ouyang et al. in the same sentence in Ch1 §1.1. Missing from bib.

**Fit:** Ch1 §1.1.

**Primary-source verified:** Yes. Anthropic 2022, confirmed.

---

### P4. Alchourrón, Gärdenfors & Makinson 1985 (AGM) — LOAD-BEARING

"On the Logic of Theory Change," *Journal of Symbolic Logic* 50:510–530. The Ch8 §8.3 differentiation of ENGRAM from Kumiho rests on the "AGM vs TMS" distinction. If the paper names AGM as the Kumiho-competitor's formal framework, it must cite the primary AGM source. Reviewers who know this literature (belief revision, formal epistemology, KR community) will notice the omission immediately.

**Fit:** Ch8 §8.3 (Kumiho differentiation). Also relevant to the TMS scan's gap-analysis in Ch5 prior art.

**Primary-source verified:** Yes. PhilPapers entry confirmed; Springer chapter confirmed (not on arxiv — predates it).

---

### P5. Strawson 2004 "Against Narrativity" — LOAD-BEARING

DOI: 10.1111/j.1467-9329.2004.00264.x, *Ratio* 17:428–452. Cited and discussed substantively in Ch3 §3.5 as the counter-voice supporting layer-3 over layer-2 priority. Present in the chapter draft; absent from bib.

**Fit:** Ch3 §3.5.

**Primary-source verified:** Yes. Confirmed at Wiley Online Library and PhilArchive.

---

### P6. Alcoff 2010 "Epistemic Identities" — LOAD-BEARING

*Episteme* 7(2):128–137. Cited in both Ch1 §1.4 and Ch3 §3.4 as the prior-usage disclosure (the paper's "epistemic identity" terminology diverges from Alcoff's standpoint-epistemology sense). Absent from bib.

**Fit:** Ch1 §1.4, Ch3 §3.4.

**Primary-source verified:** Yes. Cambridge Core confirmed.

---

### P7. Min et al. 2022 "Rethinking the Role of Demonstrations" — WORTH-CITING

arxiv:2202.12837. Cited in Ch1 §1.1 as the mechanistic analysis sharpening the frozen-weights / in-context learning picture. Absent from bib.

**Fit:** Ch1 §1.1 footnote.

**Primary-source verified:** Yes. EMNLP 2022 confirmed.

---

### P8. arxiv:2406.19354 (Model Editing as Belief Revision) — WORTH-CITING

"Fundamental Problems With Model Editing: How Should Rational Belief Revision Work in LLMs?" — Explicitly frames model editing as the AI instance of the philosophical belief revision problem. Identifies 12 open problems including "determining far-reaching consequences of edits" — which is the retraction cascade problem ENGRAM solves externally. Provides independent third-party evidence that the weights-layer approach to belief revision is systematically broken.

**Fit:** Ch8 §8.3 (where field has not built), Ch1 §1.3 (the "field does not see the dimension" argument). A two-sentence acknowledgment suffices: "The model-editing literature has independently characterized belief revision as unsolved at the weights layer (cite); ENGRAM addresses it at the external structured-store layer."

**Primary-source verified:** Yes. Confirmed arxiv:2406.19354, EMNLP 2024 presentation at OpenReview.

---

### P9. arxiv:2604.16548 "Mnemonic Sovereignty" Survey — WORTH-CITING

Security survey on long-term agent memory. Confirms: (a) no published architecture covers the full governance space, (b) provenance governance is unaddressed, (c) adversarial manipulation of persistent memory is a live research gap. Directly corroborates Ch9 §9.3 open-question framing.

**Fit:** Ch9 §9.3 (adversarial manipulation resistance). Could also be cited in Ch8 as an external survey confirming the governance gap.

**Primary-source verified:** Yes. Confirmed arxiv:2604.16548, April 2026.

---

### P10. Schechtman 1996 *The Constitution of Selves* — WORTH-CITING

Cornell UP, 1996. The reidentification vs. characterization distinction maps usefully onto the paper's three-layer taxonomy: reidentification corresponds (roughly) to layer-1 memory persistence questions; characterization to layer-2 narrative; the "epistemic third question" Schechtman names is the opening for layer-3. Currently in the outline as a pillar but absent from the chapter draft and bib.

**Fit:** Ch3 §3.x (if reinstated as a pillar), or as a brief note in Ch2 establishing why "epistemic identity" is a distinct question from both reidentification and characterization.

**Primary-source verified:** Yes. Cornell UP catalog and JSTOR confirmed.

---

## 6. Not Found / Honest Absences

**Goldman *Epistemology and Cognition* (1986):** The paper is real and primary-source verified (Harvard UP). However, from available descriptions, Goldman's primary argument is process reliabilism — the reliability of belief-forming processes as the criterion for justified belief — not "calibration" in the sense of confidence-accuracy correlation. The paper's outline claims Goldman's contribution is "the calibration problem," but Goldman's use of "calibration" in this book is not confirmed from available secondary literature. The reliabilist framework is well-documented; whether calibration specifically (as the paper uses the term) is Goldman's primary contribution vs. reliabilism more broadly is a primary-source question. **Verdict: unresolved — need a primary-source read of the book before committing to the calibration framing. The bib entry is missing regardless; the framing claim is uncertain.**

**Nozick *Philosophical Explanations* Ch 1 (closest-continuer):** Confirmed real, confirmed relevant (closest-continuer theory is explicitly useful for the post-compaction fission case the paper discusses). No primary source was retrieved beyond secondary confirmations. Not in bib.

**Stiegler *Technics and Time* Vol 3:** Confirmed published (Stanford UP 2011). No accessible free PDF was found. The cultural-scale claim in Ch9 §9.2 needs this but the paper could hold with "see Stiegler, *Technics and Time* 1–3" pointing to Vol 1 (already in bib) and noting the cultural-scale extension in Vol 3.

**Forbus & de Kleer 1993 *Building Problem Solvers*:** Mentioned in the TMS scan (2026-05-07) as the canonical TMS textbook. The paper currently plans to cite Doyle 1979 and de Kleer 1986 directly. Forbus & de Kleer 1993 is a synthesizing textbook, not the primary result — useful as a secondary citation for readers wanting TMS background, but not required for the primary-source claim.

**Second 2026 landscape entrant search (MemoryOS variants, GraphRAG variants):** The search surfaced MemOS (already indexed in survey as "EverMemOS" arxiv:2601.02163 is in the bib; MemOS arxiv:2505.22101 is the distinct MemTensor paper). GraphRAG variants (Microsoft 2024) are retrieval-engineering, not memory-architecture contributions — outside the paper's scope. No major missed entrant found beyond those documented above.

---

## 7. Summary Table

| Item | Location in paper | Bib status | Priority |
|------|-------------------|------------|----------|
| LongMemEval (Wu et al. 2024) | Ch1 §1.3 fn10 | MISSING | load-bearing |
| Ouyang et al. 2022 (InstructGPT) | Ch1 §1.1 | MISSING | load-bearing |
| Bai et al. 2022 (Constitutional AI) | Ch1 §1.1 | MISSING | load-bearing |
| AGM (Alchourrón et al. 1985) | Ch8 §8.3 (implicit) | MISSING | load-bearing |
| Strawson 2004 "Against Narrativity" | Ch3 §3.5 | MISSING | load-bearing |
| Alcoff 2010 "Epistemic Identities" | Ch1 §1.4, Ch3 §3.4 | MISSING | load-bearing |
| Min et al. 2022 | Ch1 §1.1 | MISSING | worth-citing |
| Model editing as belief revision (2406.19354) | Ch8 §8.3, Ch1 §1.3 | MISSING | worth-citing |
| Mnemonic sovereignty survey (2604.16548) | Ch9 §9.3 | MISSING | worth-citing |
| Schechtman 1996 | Ch3 (planned pillar) | MISSING | worth-citing |
| Sutton distributed cognition | Ch8 §8.4 | MISSING | worth-citing |
| Plato *Phaedrus* 274c–277a | Ch8 §8.4 | MISSING (footnote) | optional |
| Derrida *Dissemination* | Ch8 §8.4 (planned) | MISSING | optional |
| Goldman *Epistemology and Cognition* | Ch3 outline (pillar) | MISSING + framing uncertain | decision needed |
| Nozick *Philosophical Explanations* | Ch3 outline (pillar) | MISSING | worth-citing |
| Stiegler Vol 3 | Ch9 §9.2 | MISSING | worth-citing if §9.2 expanded |
| MemOS (2505.22101) | Ch1, Ch8 (update) | MISSING | optional |
| GAM (2604.12285) | Ch8 (update) | MISSING | optional |
| arxiv-2401.00001 "Real Paper" | bib only | GARBAGE ENTRY | remove |
| Barclays PLC annual report | bib only | LIKELY CONTAMINATION | remove |
| SEP quantum / paraconsistent entries | bib only | DEFERRED (Paper 2 scope) | prune from v1 |

---

## Executive Summary (~250 words)

The most urgent finding is six load-bearing citations that appear in drafted chapter text but are absent from citations.bib: LongMemEval (Wu et al., ICLR 2025), Ouyang et al. 2022 (InstructGPT/RLHF), Bai et al. 2022 (Constitutional AI), Strawson 2004 ("Against Narrativity"), Alcoff 2010 ("Epistemic Identities"), and — at the inference level — AGM (Alchourrón et al. 1985). All six are referenced in prose that is currently drafted; all six are missing from the bib. The paper would fail citation integrity review on these alone.

A secondary category of worth-citing additions would strengthen existing claims: Min et al. 2022 (mechanistic in-context learning analysis backing the frozen-weights argument), the model-editing-as-belief-revision paper (2406.19354, EMNLP 2024) supporting the claim that the field has not solved belief revision even at the weights layer, the mnemonic sovereignty survey (2604.16548) corroborating Ch9's adversarial-manipulation open question, and Schechtman 1996 for the reidentification vs. characterization distinction that frames the paper's three-layer taxonomy.

What remains uncontested: the 2026 landscape sweep confirms no new entrant (MemOS, GAM, or otherwise) implements claim-level contradiction nodes or retraction cascade. The Atlan quote about no framework describing cascade retraction is still valid as of the 2026-05-08 search.

Two bib contamination risks need immediate removal: arxiv-2401.00001 ("Real Paper") is a garbage scaffolding entry, and the Barclays annual report entry is almost certainly a project-contamination artifact. The SEP quantum mechanics / paraconsistent logic entries belong to the deferred Ch6 / Paper 2 scope and should be pruned from the v1 submission bib.

---

## 8. Supplementary Findings — Second-Pass Verification (2026-05-08, same burst)

This section records gaps found during primary-source verification of the above findings. The items below were not in the original scan above; they are genuinely new findings or corrections to the prior scan's coverage.

---

### S1. TierMem (arxiv:2602.17913) — In Chapter Draft Text, Missing from Bib

TierMem appears explicitly in the Ch8 draft at two locations:
- §8.1 body text: "TierMem (2026-02) layers a summary index with provenance pointers over an immutable append-only log of raw interactions."
- §8.1 fn1: "The systems-paper citations are MemGPT (arXiv:2310.08560), Mem0 (arXiv:2504.19413), A-MEM (Xu et al., 2025), Zep/Graphiti (arXiv:2501.13956), TierMem (arXiv:2602.17913), and MemMachine (arXiv:2604.04853)."
- §8.3: TierMem cited as the "closest parallel" to ENGRAM's provenance feature.

**TierMem is NOT in citations.bib and NOT in citations.manifest.** This is a bibliographic integrity failure: the paper text cites a specific arXiv ID in a footnote with no corresponding bib entry.

**Primary-source verified:** arxiv:2602.17913, "From Lossy to Verified: A Provenance-Aware Tiered Memory for Agents," Qiming Zhu et al., February 20, 2026. Confirmed accessible. Key claim: two-tier memory hierarchy with a runtime sufficiency router that escalates to an immutable raw-log store; provenance linking verified findings back to raw sources. Does NOT have claim-level contradiction nodes, retraction cascade, or quoted-span provenance.

**Status: Missing from bib. Load-bearing (cited in draft fn1 by arXiv ID; will fail bib validation at submission). Add immediately.**

---

### S2. Kumiho (arxiv:2603.17244) — In Audit Docs, Absent from ALL Chapter Drafts and from Bib

The existing landscape_gaps file (§3.1) discusses Kumiho as the competitor that proves AGM postulates K*2–K*6, and the file refers to "Ch8 §8.3 differentiates ENGRAM from Kumiho as 'AGM (correctness-of-revision) vs TMS (dependency-propagation)'." That differentiation passage does NOT exist in the Ch8 draft. A full-text search of all chapter drafts finds zero occurrences of "Kumiho" or "2603.17244."

Kumiho is also NOT in citations.bib and NOT in citations.manifest.

This is a double gap: the system being compared to ENGRAM by the tms_legacy scan and the landscape audit has not been incorporated into any chapter prose, and the contrast that makes ENGRAM's TMS lineage defensible against the AGM lineage is not drafted.

Additional finding during verification: the Kumiho paper explicitly cites ENGRAM (the system this paper presents) in its benchmark comparison on the LoCoMo scoring function — Kumiho, Zep (2025), Mem0, Memobase (2025), and ENGRAM (2025) are compared. This means Kumiho is aware of ENGRAM as a competitor, which is relevant for the paper's novelty framing.

**Status: Missing from bib and from chapter draft. Load-bearing for the Ch8 §8.3 differentiation that is planned but not yet written. Add bib entry; the Ch8 §8.3 drafting needs to address the AGM vs. TMS distinction explicitly.**

---

### S3. Doyle 1979 and de Kleer 1986 — Absent from Bib AND from All Chapter Drafts

The tms_legacy_in_ai_memory_2026-05-07.md scan confirmed both papers as primary TMS sources. The existing landscape_gaps file (§3.1) argues they are load-bearing for the Ch8 positioning. A full-text search of all chapter drafts finds zero occurrences of "Doyle," "de Kleer," "Truth Maintenance," or "TMS."

Neither Doyle 1979 nor de Kleer 1986 is in citations.bib or citations.manifest.

The paper's Ch8 draft uses the language "retraction cascade" and describes ENGRAM's cascade as its most defensible technical contribution (quoting Atlan: "No framework describes cascade retraction"). Without citing Doyle 1979 as the originator of dependency-directed retraction, and de Kleer 1986 as the ATMS extension, the paper exposes itself to a straightforward reviewer objection: "this has been done since 1979." The correct response is not to avoid citing them; it is to cite them as the lineage and argue ENGRAM implements the concept in the modern LLM-agent-memory context with typed nodes, a heterogeneous graph, and a reasoning-type-aware confidence system. That response requires both bib entries.

**Primary-source verified (both):** Doyle, "A Truth Maintenance System," *Artificial Intelligence* 12: 231–272, 1979 — confirmed at ScienceDirect and Semantic Scholar (2,104 citations). de Kleer, "An Assumption-Based TMS," *Artificial Intelligence* 28: 127–162, 1987 — confirmed at ScienceDirect.

**Status: Both missing from bib and from chapter drafts. Load-bearing. The paper cannot position retraction cascade as a contribution without citing TMS lineage.**

---

### S4. BeliefMem (arxiv:2605.05583) — New May 2026 Entrant, Not in Existing File

"Belief Memory: Agent Memory Under Partial Observability," Junfeng Liao et al., May 7, 2026.

BeliefMem replaces deterministic single-conclusion storage with probabilistic multi-candidate memory: instead of storing "API X failed," it stores multiple candidate conclusions with their probabilities, updated via Noisy-OR rules as new observations arrive. The system is explicitly framed as a departure from the deterministic-commitment paradigm.

**Does BeliefMem have ENGRAM's four features?**
- Claim-level provenance: No. Probabilities are over conclusions, not source-attributed.
- Contradiction nodes: No explicit contradiction representation; conflicting observations produce updated probability distributions rather than a contradiction node.
- Retraction cascade: No cascade through derivation chains. Probabilities update for the direct observation; no derivation graph.
- Calibrated confidence: PARTIAL. Noisy-OR probability updates are a form of calibrated confidence update, though not reasoning-type-differentiated.

**Positioning relevance:** BeliefMem is the closest 2026 entrant to ENGRAM's confidence model — it acknowledges that deterministic memory is wrong and proposes a probabilistic alternative. The difference is architectural: BeliefMem's uncertainty lives in probability distributions over conclusions; ENGRAM's confidence is reasoning-type-aware with provenance to sources. BeliefMem does not derive new claims from prior ones and does not cascade corrections. It is Tier I.5 with a probabilistic twist, not Tier III.

The paper provides independent 2026 evidence that the field recognizes the deterministic-commitment problem — useful as corroboration for the paper's claim that existing systems "commit to a conclusion and lose the evidence."

**Should it be cited?** Optional-supporting. Could be mentioned in one sentence in Ch8 §8.3 alongside the confidence discussion: "Even probabilistic approaches (BeliefMem, 2026) address uncertainty at the observation level without a derivation graph or retraction cascade." Adds currency to the comparison table.

**Primary-source verified:** arxiv:2605.05583, confirmed accessible. May 7, 2026.

---

### S5. STALE (arxiv:2605.06527) — New May 2026 Entrant with "Propagated Conflicts" Framing

"STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?", Hanxiang Chao et al., May 7, 2026.

STALE introduces a benchmark (400 expert-validated conflict scenarios) and a prototype (CUPMem) for testing whether LLM agents can detect and adapt to outdated memories. The paper explicitly distinguishes "Type I" conflicts (direct contradiction between two facts) from "Type II propagated conflicts" (a new observation updates one attribute, and the consequences cascade to invalidate a related memory whose dependency chain is implicit).

**Does STALE have ENGRAM's four features?**
- Claim-level provenance: No.
- Contradiction nodes: The benchmark tests whether *existing* systems detect conflicts; CUPMem uses "structured state consolidation and propagation-aware search" but no contradiction-as-node representation.
- Retraction cascade: The "Type II propagated conflicts" framing is the closest thing to cascade in the 2026 landscape — but the STALE paper identifies the lack of this as a *problem in existing systems*, not a feature CUPMem implements. The cascade concept is in the benchmark design (testing whether systems handle it), not in CUPMem as a mechanism.
- Calibrated confidence: No.

**Positioning relevance:** STALE is independently valuable to ENGRAM's paper in two ways. First, the "Type II propagated conflicts" framing is the closest the 2026 benchmark literature comes to naming cascade retraction — the very property ENGRAM implements. Second, the benchmark paper explicitly identifies that models "struggle to recognize when a change in one aspect of the user's state should invalidate related memories," which is a third-party confirmation (from a May 2026 benchmark paper) that cascade is unaddressed. This corroborates the Atlan quote more strongly because it comes from an empirical benchmark result rather than a practitioner comparison page.

**Should it be cited?** Worth-citing. Ch1 §1.3 (benchmarks section) and/or Ch8 §8.3 (retraction cascade differentiation). The "Type II propagated conflicts" finding strengthens the argument that the field has named but not solved the cascade problem.

**Primary-source verified:** arxiv:2605.06527, confirmed accessible. May 7, 2026.

---

### Summary of Supplementary Additions

| Item | Location in paper | Bib status | Priority |
|------|-------------------|------------|----------|
| TierMem (2602.17913) | Ch8 §8.1 fn1 (already cited by ID), §8.3 | MISSING FROM BIB | load-bearing |
| Kumiho (2603.17244) | Ch8 §8.3 (planned, not yet drafted) | MISSING FROM BIB AND DRAFT | load-bearing |
| Doyle 1979 TMS | Ch8 §8.3 (planned, not yet drafted) | MISSING FROM BIB AND DRAFT | load-bearing |
| de Kleer 1986 ATMS | Ch8 §8.3 (planned, not yet drafted) | MISSING FROM BIB AND DRAFT | load-bearing |
| BeliefMem (2605.05583) | Ch8 §8.3 (optional mention) | Not in bib | optional-supporting |
| STALE (2605.06527) | Ch1 §1.3 benchmarks, Ch8 §8.3 | Not in bib | worth-citing |

---

## Sources

- [LongMemEval — arxiv:2410.10813](https://arxiv.org/abs/2410.10813)
- [InstructGPT / Ouyang et al. 2022 — arxiv:2203.02155](https://arxiv.org/abs/2203.02155)
- [Constitutional AI / Bai et al. 2022 — arxiv:2212.08073](https://arxiv.org/abs/2212.08073)
- [Min et al. 2022 — arxiv:2202.12837](https://arxiv.org/abs/2202.12837)
- [AGM — PhilPapers entry](https://philpapers.org/rec/ALCOTL-2)
- [AGM — Springer chapter](https://link.springer.com/chapter/10.1007/978-90-481-9609-8_1)
- [Strawson 2004 "Against Narrativity" — Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-9329.2004.00264.x)
- [Strawson 2004 — open-access PDF via UCSD](https://lchc.ucsd.edu/mca/Paper/against_narrativity.pdf)
- [Alcoff 2010 "Epistemic Identities" — Cambridge Core](https://www.cambridge.org/core/journals/episteme/article/abs/epistemic-identities/E0C2BC2D4FBC6C139DF9437912BB5C42)
- [Goldman 1986 "Epistemology and Cognition" — Harvard UP](https://www.hup.harvard.edu/books/9780674258969)
- [Schechtman 1996 "The Constitution of Selves" — Cornell UP](https://www.cornellpress.cornell.edu/book/9780801431678/the-constitution-of-selves/)
- [Schechtman 1996 — JSTOR](https://www.jstor.org/stable/10.7591/j.ctv75d3xw)
- [Nozick 1981 "Philosophical Explanations" — PhilPapers](https://philpapers.org/rec/NOZPE)
- [Sutton distributed cognition — Springer](https://link.springer.com/article/10.1007/s13164-013-0131-x)
- [Model editing as belief revision — arxiv:2406.19354](https://arxiv.org/abs/2406.19354)
- [Mnemonic sovereignty survey — arxiv:2604.16548](https://arxiv.org/abs/2604.16548)
- [GAM — arxiv:2604.12285](https://arxiv.org/abs/2604.12285)
- [MemOS — arxiv:2505.22101](https://arxiv.org/abs/2505.22101)
- [Andrada 2021 — Springer](https://link.springer.com/chapter/10.1007/978-3-030-72644-7_12)
- [Farina et al. 2026 — Springer](https://link.springer.com/article/10.1007/s13164-026-00800-8)
- [Kirsh & Maglio 1994 — Wiley](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1804_1)
- [Wray, Kirk, Laird 2025 — arxiv:2505.07087](https://arxiv.org/abs/2505.07087)
- [Kumiho / Park 2026 — arxiv:2603.17244](https://arxiv.org/abs/2603.17244)
- [Doyle 1979 — Semantic Scholar](https://www.semanticscholar.org/paper/A-Truth-Maintenance-System-Doyle/f08f699374a27cdbc2c1ecf050ae285b01bda723)
- [de Kleer 1986 — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0004370286900809)
- [TierMem — arxiv:2602.17913](https://arxiv.org/abs/2602.17913)
- [Kumiho — arxiv:2603.17244](https://arxiv.org/abs/2603.17244)
- [BeliefMem — arxiv:2605.05583](https://arxiv.org/abs/2605.05583)
- [STALE — arxiv:2605.06527](https://arxiv.org/abs/2605.06527)
- [STALE full text — arxiv:2605.06527](https://arxiv.org/html/2605.06527)
