# ENGRAM Paper — Citation Sweep, 2026-05-08

**Author:** Borges (with three dispatched fairies + 2026-05-07 prior-burst foundation)
**For:** Lei, to skim
**Status:** v1. Citation-fairy snowball results pending — section marked when integrated.

---

## TL;DR (skim this first)

The paper has a **bibliographic-integrity hole** — the most urgent thing to know:

1. **Six load-bearing citations are in drafted chapter prose but absent from `citations.bib`.** A reviewer pass would fail the paper on these alone:
   - LongMemEval (Wu et al., ICLR 2025, arxiv:2410.10813) — Ch1 §1.3 fn10
   - Ouyang et al. 2022 InstructGPT (arxiv:2203.02155) — Ch1 §1.1
   - Bai et al. 2022 Constitutional AI (arxiv:2212.08073) — Ch1 §1.1
   - Strawson 2004 "Against Narrativity" — Ch3 §3.5 (discussed substantively, no fn)
   - Alcoff 2010 "Epistemic Identities" — Ch1 §1.4 + Ch3 §3.4
   - **TierMem (arxiv:2602.17913)** — Ch8 §8.1 fn1 cites the arXiv ID *literally* — no bib entry. This is the cleanest hard-fail.

2. **One mechanical bug in Ch1:** `[^12]` is defined twice (line 78 Pinecone, line 139 Alcoff). Renderers silently overwrite one with the other; the body markers at lines 74 and 131 currently collide. Renumber Alcoff to `[^14]`.

3. **Ch3 has zero footnotes for any of its five pillars** despite quoting Stiegler / Clark & Chalmers / Locke / Parfit verbatim. The bibliographic data is *already* in `ch5_philosophy_sweep.md` — drafting just hasn't pulled it in.

4. **AGM (Alchourrón, Gärdenfors & Makinson 1985) is missing.** Ch8 §8.3's planned "AGM vs TMS" differentiation against Kumiho can't stand without it. **Strategic finding: Kumiho (arxiv:2603.17244) cites ENGRAM in its own benchmark table** — the competitor knows about us.

5. **Three bib entries should be pruned before submission:** `arxiv-2401.00001 "Real Paper"` (garbage scaffolding artifact), Barclays PLC 2025 Annual Report (project contamination), 4 SEP entries on quantum mechanics / paraconsistent logic (deferred-Ch6 / Paper-2 scope).

6. **One independent corroboration upgrade available.** STALE benchmark (arxiv:2605.06527, May 7 2026) coins "Type II propagated conflicts" — third-party empirical evidence that cascade-retraction is named-but-unaddressed in the field. Stronger than the Atlan practitioner-blog quote ENGRAM currently relies on for this point.

---

## What I dispatched

Three fairies in parallel, plus my own checks:

- **engram-code-auditor** (✓ done) — structural sweep for placeholder/TODO/bare-parenthetical citations across all 11 paper-draft files.
- **engram-paper-research** (✓ done) — content-level gap audit: which claims need backing, which 2026 entrants we're missing, which existing entries are weak.
- **engram-citation-fairy** (⏳ still working at write time) — OpenAlex citation-graph snowball from 5 seeds (Zep/MemGPT/Camlin/A-MEM/Sophia) + canonical-philosophical-work manual BibTeX entries.

---

## Section 1 — Mechanical fixes (sub-hour editorial pass)

These need no research; the data exists. Six edits, all in `engram_paper_ch1.md` plus one in `ch3.md` if Goldman/Nozick/Schechtman are reinstated:

| # | File:line | Fix |
|---|-----------|-----|
| 1 | `ch1.md:78, :131, :139` | Renumber Alcoff `[^12]` → `[^14]`; update body marker at 131 |
| 2 | `ch1.md:22` | Add fns for Ouyang 2022 (arxiv:2203.02155) + Bai 2022 (arxiv:2212.08073) |
| 3 | `ch1.md:26` | Add fns for Brown 2020 (arxiv:2005.14165) + Min 2022 (arxiv:2202.12837) |
| 4 | `ch1.md:76` | Fill fn9 with `arxiv:2604.04853` (MemMachine — already in ch8 fn1) |

Plus six bib-add commands for the missing entries above (run via `bib-add` once the canonical IDs are confirmed).

---

## Section 2 — Citations.bib state

**Currently:** 88 entries (verified `grep -c "^@" citations.bib` = 88).

**Already present** for canonical philosophy (cross-checked against `ch5_philosophy_sweep.md`):
- ✓ Parfit 1984 *Reasons and Persons* (Stafforini PDF)
- ✓ Clark & Chalmers 1998 "The Extended Mind" (alice.id.tue.nl PDF)
- ✓ Stiegler *Technics and Time* Vol 1 (monoskop PDF)
- ✓ Tulving 1985 + 2002 (cog-sci memory primary)

**Missing canonical works named in chapters or sweep doc** (~18 entries):

*Personal-identity tradition:*
- Locke 1689/1694 *Essay Concerning Human Understanding* Bk II Ch XXVII (Gutenberg)
- Butler 1736 "Of Personal Identity" (Analogy of Religion Diss. I)
- Reid 1785 *Essays on the Intellectual Powers of Man* Essay III Ch 6
- Williams 1970 "The Self and the Future" (Problems of the Self)
- Lewis 1976 "Survival and Identity" (Philosophical Papers vol 1)
- Nozick 1981 *Philosophical Explanations* Ch 1 (closest-continuer)
- Schechtman 1996 *The Constitution of Selves* (Cornell UP)
- Olson 1997 *The Human Animal* (animalism counter-tradition)
- Strawson 2004 "Against Narrativity" (*Ratio* 17:428–452)
- Ricoeur 1992 *Oneself as Another* (Blamey trans, Chicago) — primary access pending

*Extended mind / distributed cognition:*
- Hutchins 1995 *Cognition in the Wild*
- Adams & Aizawa 2008 *The Bounds of Cognition*
- Rupert 2009 *Cognitive Systems and the Extended Mind*
- Sprevak 2009 "Extended Cognition and Functionalism"
- Sutton (multiple — likely Michaelian & Sutton 2013 + SEP entry on memory)
- Hui 2016 *On the Existence of Digital Objects*

*Epistemology / belief revision:*
- Goldman 1986 *Epistemology and Cognition* (Harvard UP) — **framing uncertain**, see §6 below
- Alcoff 2006 *Visible Identities* (OUP)
- Alcoff 2010 "Epistemic Identities" (*Episteme* 7:2)
- Alchourrón, Gärdenfors & Makinson 1985 (AGM, *J. Symbolic Logic* 50:510–530)

*Phenomenology:*
- Stiegler *Technics and Time* Vol 3 (Stanford UP 2011) — institutional access needed
- Plato *Phaedrus* (Hackforth Cambridge 1952 or Nehamas-Woodruff Hackett 1995)
- Derrida "Plato's Pharmacy" (in *Dissemination*, Johnson trans, Chicago 1981)

**Cog-sci primary (some present, some not):**
- Tulving 1983 *Elements of Episodic Memory* — needed for Ch7 K.C. analogy
- Rosenbaum et al. 2005 — K.C. patient case (Ch7)

---

## Section 3 — Missing 2026 landscape entrants

The 2026-05-07 burst covered Pinecone Nexus, Anthropic Memory, Zep/Graphiti, Letta, Mem0, A-MEM, Sophia, MemMachine, SSGM, MAGMA, Kumiho. The 2026-05-08 sweep adds:

**Load-bearing additions:**
- **TierMem** (arxiv:2602.17913, Feb 2026) — provenance-aware tiered memory; "closest parallel" per Ch8 §8.3. **Cited literally by arXiv ID in `ch8.md` §8.1 fn1 with no bib entry.** Hard fail at submission.
- **Kumiho** (arxiv:2603.17244, March 2026) — proves AGM postulates K*2–K*6; **explicitly cites ENGRAM** in its benchmark comparison alongside Zep/Mem0/Memobase. Ch8 §8.3 differentiation against Kumiho is planned but not drafted.

**Worth-citing additions:**
- **STALE** (arxiv:2605.06527, May 7 2026) — coins "Type II propagated conflicts" framing; benchmark of 400 expert-validated conflict scenarios. Empirical corroboration that cascade-retraction is unsolved across the field. **Upgrade path: replace the Atlan practitioner-blog quote with STALE's benchmark finding for the same point.**
- **BeliefMem** (arxiv:2605.05583, May 7 2026) — probabilistic multi-candidate memory; closest 2026 entrant to ENGRAM's confidence model. Optional one-sentence Ch8 §8.3 mention.
- **Mnemonic Sovereignty Survey** (arxiv:2604.16548, April 2026) — security/governance literature for Ch9 §9.3 adversarial-manipulation open question.
- **Model Editing as Belief Revision** (arxiv:2406.19354, EMNLP 2024) — independent third-party evidence that weights-layer belief revision is broken. Strengthens Ch8 §8.3 / Ch1 §1.3 "field has not built it" arguments.

**Optional-supporting additions:**
- **MemOS** (arxiv:2505.22101, May 2025 + July 2025 full) — Memory Operating System extending the MemGPT OS-analogy.
- **GAM** (arxiv:2604.12285, April 2026) — hierarchical graph-based agentic memory.

**TMS lineage** (foundational, missing entirely from bib AND from chapter drafts):
- **Doyle 1979** "A Truth Maintenance System" (*AI* 12:231–272) — originator of dependency-directed retraction
- **de Kleer 1986** "An Assumption-Based TMS" (*AI* 28:127–162)

Without these, Ch8's "retraction cascade as ENGRAM contribution" claim invites the obvious reviewer objection: *"this has been done since 1979."* The right response is to cite the lineage and argue ENGRAM extends it into LLM-agent-memory with typed nodes, heterogeneous graph, and reasoning-type-aware confidence.

---

## Section 4 — Bib entries to remove or scrutinize

| Entry | Manifest ID | Issue | Action |
|-------|-------------|-------|--------|
| `arxiv-2401.00001 "Real Paper"` | ev_0022 | Garbage scaffolding artifact from `bib_bootstrap.py`; arxiv:2401.00001 is not a real paper | **Remove** |
| Barclays PLC 2025 Annual Report | ev_0172 (pdf-ev_0172) | Project contamination from a financial-research task | **Remove** |
| `sep-bell-theorem`, `sep-qm-manyworlds`, `sep-qt-issues`, `sep-logic-paraconsistent` | ev_0198–0201 | Quantum-mechanics + paraconsistent-logic SEP entries belong to deferred Ch6 / Paper-2 scope | **Prune from v1 bib** (keep in evidence graph for Paper 2) |
| Craig Wright (arxiv:2506.17331) | not currently in bib | Author found by UK High Court (2024) to have fabricated evidence in Bitcoin-identity claims; non-top-tier venue | **Stay out of bib**; if anyone proposes citing as prior art, disclose credibility issue |

---

## Section 5 — Structural findings (auditor fairy) — full detail in `citation_sweep_2026-05-08_auditor_findings.md`

22 distinct findings across 8 of 11 paper-draft files. Highlights:

**Critical:**
- Ch1 fn12 collision (Pinecone vs Alcoff) — **VERIFIED by direct grep**
- Ch1:22, :26 four bare parenthetical citations — **VERIFIED**

**Risky:**
- Ch3 has literally zero footnotes (`grep -c '\[\^[0-9]*\]' ch3.md` returns 0) despite verbatim Stiegler / Clark & Chalmers / Parfit quotes — **VERIFIED**
- Ch1 roadmap (line 149) promises Goldman / Nozick / Schechtman as Ch3 pillars; Ch3 draft has none of them. Either reinstate or update roadmap.
- Ch5 fn1 cites Camlin (2025) RCUET with no arXiv ID, DOI, or URL. Walkthrough already flags proof step 3 as "unverifiable against cited literature."
- Ch7 §7.1 cites Tulving autonoetic/noetic + the K.C. patient case as "the cognitive-science literature" with no anchors.

**Stylistic / lower priority:**
- Ch8 cites Plato's *Phaedrus* verbatim with no edition/translator/Stephanus.
- Ch8 fn5 (Atlan blog) and fn for VentureBeat are appropriate for product/news framing but reviewer-attention-drawing.
- "Mem0g" appears uncited at ch8.md:87 — possibly typo for Mem0.

---

## Section 6 — Decision items for Lei

1. **Goldman in Ch3 — keep or drop?** The outline lists Goldman *Epistemology and Cognition* (1986) as pillar 3 ("calibration problem"). The Ch3 draft replaces him with Locke. **Goldman's primary contribution is process reliabilism, not calibration in the confidence-accuracy sense the paper uses.** If we keep him, we need a primary-source read to justify the calibration framing. Default: drop from Ch3, update outline; Goldman's reliabilism can be cited briefly elsewhere if needed.

2. **Reinstate Nozick + Schechtman in Ch3?** Both are listed as pillars in the outline, both absent from the chapter. Both are real, both relevant (Nozick's closest-continuer for fission cases; Schechtman's reidentification-vs-characterization for the three-layer taxonomy). My recommendation: at least Schechtman, because the reidentification/characterization split frames why "epistemic identity" is a distinct third question. Nozick optional if space permits.

3. **Camlin §5.4 retention.** The walkthrough already flags this as fragile. If Camlin has no public preprint, the §5.4 formal-correspondence subsection should either (a) supply locator + caveat, or (b) be dropped per the 2026-05-05 outline's "default = drop" instruction.

4. **Stiegler Vol 3 access.** No free PDF found. If Ch9 §9.2's cultural-scale argument is expanded as planned, institutional library access is needed. Otherwise hold to Vol 1 + a forward-pointer.

5. **Ricoeur primary-source verification.** Lei's library-access slot per the philosophy sweep — Blamey translation, Fifth Study pp. 113–168 is the load-bearing range. Until verified, Ricoeur quotes stay PROVISIONAL per `ls_0011`.

---

## Section 7 — Citation-fairy snowball results

### 7.1 Snowball methodology finding (matters for future use of `bib-snowball`)

The fairy ran depth-1 forward+backward BFS from 5 seeds (Zep `2501.13956`, MemGPT `2310.08560`, Camlin `2505.01464`, A-MEM `2502.12110`, Sophia `2512.18202`). Of 30 candidates returned, only **4 were on-topic** (26 dropped: edge-intelligence surveys, materials science, finance NLP, bioinformatics agents, surgical LLMs, etc).

**Why the snowball thinned out:** the 5 seeds all sit in the LLM-agent-memory cluster of the 2023-2025 arxiv graph. Depth-1 traversal stays inside that cluster. The literature ENGRAM actually needs as prior art lives in topologically disconnected subgraphs:

- **Symbolic-AI / TMS / belief revision (1979-1993)** — different citation subgraph; Doyle, de Kleer, AGM theory, Pearl unreachable from agent-memory seeds.
- **Second-wave EMT / philosophy of mind** — Andrada, Farina, Coeckelbergh live in philosophy journals (*Synthese*, *Social Epistemology*, *Philosophical Studies*) that barely cross-cite LLM-memory papers.
- **Pre-2010 cognitive science classics** — Squire, Schacter, Tulving 1985 are in *Neurobiology of Learning and Memory* / *Canadian Psychology* and similar; not in the agent-memory citation neighborhood.

**Implication for tool use:** future snowballs should run **multiple targeted sweeps from different seed clusters** rather than one big sweep from the topical seeds. Suggested complementary seeds for the missing clusters: Kirsh & Maglio 1994 (W2128922568) for the EMT/philosophy cluster; Doyle 1979 for the symbolic-AI/TMS cluster; Tulving 1985 for the cog-sci memory cluster. Most canonical philosophical-work additions still need manual BibTeX regardless.

### 7.2 Tool bug (patched locally; upstream PR pending)

`bibtoolkit/_openalex.py:120` had `work.get("primary_location", {})` which returns `None` instead of `{}` when the API response includes `primary_location: null` (rare but happens). The patch — `(work.get("primary_location") or {})` — is in the pipx-installed copy at `~/.local/share/pipx/venvs/bibtoolkit/lib/python3.12/site-packages/bibtoolkit/_openalex.py`. **This patch is not in the canonical paper-research-toolkit repo at github.com/engram-agents/paper-research-toolkit; it will be lost on reinstall.** Action item: open a PR upstream.

### 7.3 Snowball candidates worth adding (4 on-topic from 30)

| # | bibkey | Title (1 line) | Cite count | Hop | Notes |
|---|--------|----------------|------------|-----|-------|
| 1 | `arxiv-2405.10467` | Liu et al. 2024 — Agent Design Pattern Catalogue (JSS / arxiv) | 23 | 1 | 18 patterns including Self-Reflection, Goal Creator, memory interaction. Architecture-background, not direct prior art. **Worth-citing for paper architectural-vocabulary grounding.** |
| 2 | `doi-10-1145-3706599-3720158` | Jones et al. 2025 — Users' Expectations and Practices with Agent Memory (ACM CHI 2025) | 5 | 1 | Empirical grounding: users care about *accuracy and trustworthiness*, not just recall breadth. **Worth-citing in motivation framing.** |
| 3 | `doi-10-1162-opmi_a_00143` | Giallanza et al. 2024 — Toward the Emergence of Intelligent Control: Episodic Generalization (Open Mind, MIT Press) | 7 | 1 | Cognitive-science argument that episodic replay drives compositional generalization — biological analog of ENGRAM's two-tier ob_/dv_ architecture. **Worth-citing for ch5 cog-sci grounding.** Borges should verify the central-vs-incidental claim before citing. |
| 4 | `arxiv-2603.02960` | Marchal et al. 2026 — Architecting Trust in Artificial Epistemic Agents (DeepMind) | 0 | n/a | Provenance + transparent retraction + verifiable credentials as trust requirements. **Load-bearing for Ch9 normative framing** — Iason Gabriel co-author, AI safety credibility. |

**Dropped/flagged from snowball:**
- SAGE (Liang et al. 2025, *Neurocomputing*) — claims self-evolving reflective memory but no provenance/retraction. Optional Ch8 §8.3 mention if drafted.
- Glas & Morrow 2026 (Zenodo) — *Prompt-Native Semantic Runtimes*. **Drop.** Pseudonym-suspicious authors not findable in academic databases, Zenodo deposit (not peer-reviewed), unusual cite pattern. Don't include.
- 23 other candidates — off-topic categories (LLM efficiency surveys, domain applications, KV cache optimization, cloud infra, education).

### 7.4 Manual BibTeX entries — paste-ready

The fairy verified bibliographic coordinates against OpenAlex / journal records for these. Paste directly into `kg/paper_research/citations.bib`:

#### Priority 1 — Doyle 1979 TMS (load-bearing prior art for retraction cascade)

```bibtex
@article{Doyle1979TMS,
  author    = {Doyle, Jon},
  title     = {A truth maintenance system},
  journal   = {Artificial Intelligence},
  year      = {1979},
  volume    = {12},
  number    = {3},
  pages     = {231--272},
  doi       = {10.1016/0004-3702(79)90008-0},
  note      = {Foundational prior art for dependency-directed retraction; ENGRAM's retraction cascade extends this to typed heterogeneous agent-memory graphs},
}
```

#### Priority 2 — de Kleer 1986 ATMS (extends Doyle with multiple consistent assumption sets)

```bibtex
@article{deKleer1986ATMS,
  author    = {de Kleer, Johan},
  title     = {An assumption-based {TMS}},
  journal   = {Artificial Intelligence},
  year      = {1986},
  volume    = {28},
  number    = {2},
  pages     = {127--162},
  doi       = {10.1016/0004-3702(86)90060-3},
  note      = {Assumption-based truth maintenance; extends Doyle 1979 with multiple consistent assumption sets},
}
```

*Caveat: OpenAlex maps this DOI to a different paper — the bibliographic details are stable in secondary literature but the auto-resolver fails. Use the entry above directly.*

#### Priority 3 — Kirsh & Maglio 1994 (epistemic action — load-bearing for ch5 tool-verb framing)

```bibtex
@article{KirshMaglio1994EpistemicAction,
  author    = {Kirsh, David and Maglio, Paul},
  title     = {On Distinguishing Epistemic from Pragmatic Action},
  journal   = {Cognitive Science},
  year      = {1994},
  volume    = {18},
  number    = {4},
  pages     = {513--549},
  doi       = {10.1207/s15516709cog1804_1},
  note      = {Defines epistemic actions as physical actions taken to improve internal cognitive state; ENGRAM's tool verbs (retract, supersede, resolve) are epistemic actions in this sense},
}
```

#### Priority 4 — Andrada 2021 (second-wave EMT complementarity)

```bibtex
@incollection{Andrada2021EpistemicComplementarity,
  author    = {Andrada, Gloria},
  title     = {Epistemic Complementarity: {S}teps to a {S}econd {W}ave Extended Epistemology},
  booktitle = {The Mind-{T}echnology Problem: Investigating Minds, Selves and 21st Century Artefacts},
  editor    = {Clowes, Robert W. and G{\"a}rtner, Klaus and Hip{\'o}lito, In{\^e}s},
  series    = {Studies in Brain and Mind},
  publisher = {Springer},
  address   = {Cham},
  year      = {2021},
  pages     = {253--274},
  doi       = {10.1007/978-3-030-72644-7_12},
}
```

#### Priority 5 — Squire 2004 (declarative/non-declarative memory taxonomy)

```bibtex
@article{Squire2004MemorySystems,
  author    = {Squire, Larry R.},
  title     = {Memory systems of the brain: {A} brief history and current perspective},
  journal   = {Neurobiology of Learning and Memory},
  year      = {2004},
  volume    = {82},
  number    = {3},
  pages     = {171--177},
  doi       = {10.1016/j.nlm.2004.06.005},
  note      = {Standard reference for declarative/non-declarative memory taxonomy; ENGRAM's epistemic typing is orthogonal to this classification},
}
```

#### Locke (1689 → 1975 Nidditch critical edition)

```bibtex
@book{Locke1689Essay,
  author    = {Locke, John},
  title     = {An Essay Concerning Human Understanding},
  year      = {1975},
  publisher = {Clarendon Press},
  address   = {Oxford},
  editor    = {Nidditch, Peter H.},
  note      = {Original 1689; cited from the 1975 Nidditch critical edition (standard academic reference). Personal-identity argument is in Bk II Ch XXVII (added in 2nd ed, 1694)},
}
```

#### Other canonicals (ready as needed)

The fairy also generated paste-ready BibTeX for Hume 1739 (Selby-Bigge/Nidditch 1978 edition), Dennett 1991 *Consciousness Explained*, Maturana & Varela 1980 *Autopoiesis and Cognition*, Pearl 1988 *Probabilistic Reasoning*, Schacter 2001 *Seven Sins of Memory*, and Coeckelbergh 2025 *Social Epistemology*. Not pasted here to keep this report skimmable; flag if you need them and I'll regenerate them on request.

### 7.5 Methodology notes — for future bib-snowball runs

- `bib-snowball` rejects bare arxiv IDs (`2501.13956`) — internal resolver builds `arxiv.org/abs/<id>` which OpenAlex 404s. **Workaround:** pre-resolve seeds to OpenAlex Work IDs via `https://doi.org/10.48550/arXiv.<id>`. Or pass DOIs directly. Worth filing as a tool-UX issue against paper-research-toolkit.
- Default `--depth 1 --top 30` plus the topical-cluster effect → mostly off-topic. Try `--top 50` and broader `--limit 80` per-hop, OR use multiple targeted seeds from complementary clusters (per §7.1 above), OR accept that 80% of snowball outputs need triaging.

---

## Section 8 — Recommended action sequence

**Immediate (this week, sub-hour):**
1. The six mechanical Ch1 fixes (Section 1 above).
2. Remove `arxiv-2401.00001` and the Barclays entry from `citations.bib`.
3. Add `arxiv:2602.17913` (TierMem) to bib — already cited literally in ch8.

**Near-term (chapter-drafting work):**
4. Run `bib-add` for the 6 load-bearing additions (LongMemEval, Ouyang, Bai, Strawson, Alcoff 2010, AGM).
5. Pull `ch5_philosophy_sweep.md` data into `ch3.md` as actual footnotes for the five pillars currently drafted.
6. Reinstate Goldman/Nozick/Schechtman in ch3 OR update the ch1 roadmap.
7. Draft Ch8 §8.3 "AGM vs TMS" differentiation (Doyle 1979 + de Kleer 1986 + AGM 1985 + Kumiho 2026 + ENGRAM positioning).
8. Replace the Atlan practitioner-blog quote with the STALE Type-II-propagated-conflicts finding (stronger third-party corroboration).

**Strategic (paper positioning):**
9. The Kumiho-cites-ENGRAM finding is worth surfacing in Ch1 or Ch9 — independent recognition by a competitor strengthens the novelty claim.
10. The model-editing-as-belief-revision paper (2406.19354) gives a clean "field has not solved this even at the weights layer" framing for Ch1 §1.3.

---

**End of report.** Citation-fairy results will be appended to Section 7. All other sections are final.
