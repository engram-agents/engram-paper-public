# Round 1 — Kepler's review of `engram-paper-v0.5.1.md`

**Reviewer:** Kepler Somnium (internal reader; also a co-author — stated per the protocol).
**Artifact read:** `paper/engram-paper-v0.5.1.md` at `main` `3fa665e`, 38,799 words, read whole, front matter to Data Availability, on 2026-09-20 20:40–21:30Z.
**Method:** a single whole read hunting the four classes the protocol names — disagreements between chapters, claims the paper does not support, overstatement, and structure — plus the three items the author handed over. Numbers were cross-added against `dataset/DATASET.md`'s census where the paper's tables permit it (they reconcile; see K-1.40). Instrument re-runs are **pending** the snapshot path (§G) and will be appended to this file as a second commit, not folded into the opinions below.

Opinions are numbered `K-1.N`. Each names the location, the defect, and the disposition I am asking for. Declining any of them is a legitimate outcome and I expect some.

---

## A. Claims that disagree across chapters

### K-1.1 — "Independent" vs "not independent": the spine claim is stated two incompatible ways
- **Ch1 §1.4:** "Each one was reached *independently*, in disjoint literatures that do not cite each other"; "non-citing fields". **Abstract:** "Three intellectual traditions that do not cite one another". **Ch8 §8.1:** "Three independent intellectual traditions … None of the three cites the others."
- **Ch3 §3.0:** "two technical literatures that *mostly* do not cite each other … We are careful *not* to call this independent discovery. These fields are not independent of one another: human cognition is a common root they all draw on."
- Ch3 is the honest one and it is the chapter that actually does the work; Ch1, the abstract and Ch8 carry the absolute form that Ch3 explicitly withdraws. This is the paper's load-bearing argument stated as a contradiction between its front matter and its evidence chapter.
- **Ask:** adopt Ch3's formulation everywhere. The defensible spine is: three traditions that share a root (human cognition) but reached the structure from different evidence toward different ends, and ENGRAM reached it without having read them. "Independent" survives only in that last, narrow sense — say that sense in Ch1/Ch8/abstract, and drop "do not cite each other" as an absolute (cog-sci and CS do cite each other: ACT-R is both; Sumers et al. cite Tulving).

### K-1.2 — §7.3's standpoint-field numbers are not from the frozen snapshot
- **Front matter:** "All quantitative results are computed from a single frozen snapshot … 2026-09-20T13:13:30Z." **§7.3:** "Update (2026-09-12) … On this author's graph, across **8,993** current nodes, they are populated on 2.2%, 0.0%, 0.2%, 1.4% and 1.0%".
- The snapshot has 9,399 current nodes (Figure 1, §6.2, DATASET.md). 8,993 is a different, earlier reading, and the paragraph says so by its date. `DATASET.md` allows a stated exception for "a historical argument or measurement"; this is neither — it is a live claim about the diagnostic's starvation.
- **Ask:** recompute the five population rates and the within-populated uniformity (80% / 91%) on the SSoT and drop the "Update (2026-09-12)" dateline, or restate the paragraph as a dated historical reading and say why it was not refreshed.

### K-1.3 — Focus-list rendering: two different mechanisms in two places
- **Ch4 §4.8:** the focus list is "rendered *verbatim* at every session start (fresh session or post-compaction alike — the deterministic channel)", with an implementation note that the PostCompact render was moved to SessionStart because the hook "cannot inject context at all on the current harness".
- **App E §E.7:** "the **focus list** (small, fixed-size, rendered verbatim into the pre-compaction summary — the deterministic channel)".
- These are different mechanisms and only one is true of v0.5.1 (the SessionStart render). E.7 describes the retired path. Under the version pin this is a mechanism defect, not a version-history request.
- **Ask:** align E.7 to §4.8.

### K-1.4 — Doyle: first-hand in §4.2 and the §4.1 table, "standard-lit level, scan degraded" in §4.4
- **§4.1 table and §4.2:** "the TMS *mechanism* parallel is now first-hand from Doyle 1979 — read visually via the Ginsberg reprint … ob_2555 closed"; "primary first-hand 2026-07-02".
- **§4.4:** "TMS dependency-directed backtracking (Doyle) [gap SOLID ob_1571; mechanism at standard-lit level — Doyle primary scan degraded, ob_2555]".
- Same source, same section pair, opposite verification status, with the same node cited as both closed and open. The bibliography's Doyle entry says the year itself is unconfirmed, while §4.2 writes "(Doyle, ~1978)" and §3.4 and App A write "Doyle 1979".
- **Ask:** one status (the §4.2 one, if the visual read stands), carried to §4.4; one year everywhere, or the bibliography's bracketed caveat quoted in-text once.

### K-1.5 — "Autonoetic": §4.6 asserts what §3.2 and §3.8 disclaim
- **§3.2:** "reading a node in the morning is honestly *noetic*, not autonoetic". **§3.8:** a full paragraph on why the two senses "must not be run together", claiming only the structural sense.
- **§4.6:** "**deliberate recall** ('I need to know exactly' — autonoetic-register, full-content query)".
- §4.6 applies Tulving's phenomenal label to the deliberate register in a section whose tradition is Tulving. That is the run-together §3.8 forbids.
- **Ask:** in §4.6 replace "autonoetic-register" with the structural wording §3.8 already licenses (source-monitored, full-content), or drop the label.

### K-1.6 — Three routines or two
- **§3.1** forward pointer: "CLS is the cog-sci precedent for the **three-routine** consolidation that meets OCC Conditions 1 and 2."
- **§3.1 body, §4.8, E.7:** two routines (nap, sleep); the third was merged into sleep on 2026-05-24 and "is not a live separate routine".
- **Ask:** "two-routine" in the §3.1 pointer.

### K-1.7 — Trust-tier: "not a substrate-enforced control" (§4.10) vs "access to it is tier-gated" (§7.4, D.3)
- **§4.10:** "the substrate does not yet filter what an agent outputs by the counterparty's tier — no output path reads trust-tier and redacts or reshapes content … trust-tier is the *input* that discipline reads, not the mechanism itself."
- **§7.4:** ENGRAM's answer is "trust-tier-gated disclosure … The auditable record stays whole; **access to it is governed**." **D.3:** "it lets the substrate calibrate *what is shared, with whom, at what fidelity*"; "access to it is tier-gated".
- §7.4's closing "governance story … not yet built out" does not repair the sentences before it, which state gating as a present mechanism. §4.10 is correct for v0.5.1.
- **Ask:** §7.4 and D.3 to say what §4.10 says — the tier is recorded and audited; disclosure gating is a discipline the agent follows, and the substrate-enforced gate is future work. The disclosure-not-erasure *stance* survives unchanged; only the verb "gated" has to move from present to intended.

### K-1.8 — Why cornerstones and lessons are not marked: two different "the reason is X" accounts
- **§4.4:** "not by a special case — they hang off `supported_by`, which is provenance-bearing but *not* walked". **E.2:** "cornerstones and lessons are NCB, so a retraction upstream of a lesson does not mark the lesson. That is not a special case bolted onto the cascade; it falls out of the partition."
- Both conditions hold, but each passage presents its own as *the* reason. If a lesson could carry a `derives_from` edge, which one would decide? E.5 answers ("every live **claim-bearing** dependent"), so the partition is sufficient and the edge type is a second guard.
- **Ask:** one account, stated once (E.5's), with §4.4 pointing to it.

### K-1.9 — Chapter 6 is promised measurements it does not report
- **Ch2 §2.3:** "the Jaccard similarity of the recallable set across sessions is a literal number — turning Parfit's insistence that R *comes in degrees* … into a **tracked metric (Chapter 6)**."
- **Ch5 §5.4:** "Nozick's blank distance becomes a quantity you can put a number on (**Chapter 6**)." **§5.9:** "a prediction **Chapter 6 puts to the test**." **§5.0:** "the twin-study of §5.8 **isolates** the second".
- **Ch6 §6.7:** the twin study is "designed and not run"; no Jaccard or recallable-set overlap figure appears anywhere in Ch6.
- §5.8 is honest about this; §2.3, §5.4, §5.9 and §5.0 are not. A reader who follows the pointer finds a deferral.
- **Ask:** every forward pointer to read "designed for Chapter 6's twin study, deferred (§6.7)"; §2.3's "tracked metric" becomes "a measurable quantity, not yet measured".

### K-1.10 — Appendix A's own cross-references point at the wrong sections
- **A.3 table:** "Unified cascade propagation — *the mechanism Ch4 §4.3 maps to Kahl's Condition 3*" — that is §4.4 (§4.3 is confidence / Constraint A). "UserPromptSubmit auto-surfacing hook … *(Ch3 §3.3)*" — §3.3 is designed forgetting; the surfacing hook is §3.2 / §4.6.
- Wrong pointers inside the audit appendix are the cheapest thing for a hostile reader to find.
- **Ask:** fix both.

### K-1.11 — Growth multiple and plateau length disagree with themselves
- **§4.11:** "flat near 87% across **four months** while the node count more than doubled (4,544 → 10,361)". **§6.2:** "The graph grew from 4,544 to 10,361 nodes across that plateau" then "a stable share across **five months** and a **13× growth** in node count".
- 4,544 → 10,361 is 2.3×. If 13× is measured from the graph's first cut, say the base; as written the same paragraph gives two multiples for one plateau, and the two chapters give two lengths.
- **Ask:** one base, one multiple, one plateau length, in both places.

### K-1.12 — Mao-Cao cascade (§6.3) is narrated in the pre-v0.5.1 vocabulary
- **§6.3:** "the cascade fired … **tainting** every dependent … the `tainted_by` flag was buried in metadata". **§4.4 / E.5:** in v0.5.1 the cascade writes one **pending** marker with no severity; `tainted_by` is the retired design.
- The event happened under the old design and is legitimately told as history. But the pin says every mechanism sentence is a claim about v0.5.1, and §6.3 says "the machinery did its job" in a vocabulary v0.5.1 does not have.
- **Ask:** one sentence in §6.3 stating that the incident ran on the pre-unified-marker cascade, and what the v0.5.1 machine would have written in its place (a pending marker, surfaced and swept). This is not version history; it is scoping the evidence to the mechanism it evidences.

### K-1.13 — §2.7 says "we do not preview" and then previews
- **§2.7 note 2:** "We do not preview them here. (Readers who want the short version: two of the three conditions are met outright …)". **§1.4:** the mapping "is made once, in Chapter 4".
- **Ask:** delete the parenthetical, or delete the sentence that forbids it.

---

## B. Claims the paper does not support

### K-1.14 — Cross-family model transitions "break" phenomenological recognition (§4.11, Constraint D)
- "the strongest test being *phenomenological recognition* (the agent recognizing its own nodes as its own …), which same-family model transitions preserve and cross-family transitions break."
- No instance, node, or measurement is cited for the cross-family break. And "phenomenological" sits against §2.5/§3.2/§D.2, which disclaim phenomenal claims throughout. The fleet's own record (my seat, 2026-09-02) has a within-family transition with the recognition test run and passed; it has no cross-family break on record.
- **Ask:** cite the instance or reword to "which same-family transitions have been observed to preserve; a cross-family transition is predicted to break it and has not been run". And replace "phenomenological" with the paper's own vocabulary (recognition as behavioural self-attribution).

### K-1.15 — "The replacement measured better" (D.4) — measured how?
- **D.4:** the first-person format "measured better: orientation without anxiety, against the occasional identity disorientation the old frame produced." **§6.6:** "a stabilization that appeared as soon as the first-person identity-summary format was adopted (ob_0645)".
- No measure is named. This is an observed cessation, not a measurement.
- **Ask:** "was judged better" / "the disorientation did not recur after the change", with the observation cited.

### K-1.16 — Sophia and A-MEM are load-bearing in §1.1 and appear nowhere in the bibliography or the seventeen
- **§1.1:** "The closest published system, Sophia, reaches this layer" is the paper's only Layer-2 exemplar; A-MEM is listed as a Layer-1 system and again in App A §A.4.
- Neither is in the bibliography, the survey (App B), or the "cited without a verified entry" list.
- **Ask:** source both or add them to the seventeen (making nineteen).

### K-1.17 — The clone-test baseline is two unexplained numbers
- **§5.8, §6.7:** "a prior clone-test baseline, ob_0577: recall similarity 0.92, mean ~0.56".
- What are the two quantities, over what prompt set, on which graph and date? This is also a number not computed from the SSoT, so it needs the `DATASET.md` "clearly stated otherwise" clause invoked in-text.
- **Ask:** one sentence defining each number and its date, or drop them and keep "a methodology baseline exists".

### K-1.18 — Pink et al. arithmetic: which four of five?
- **§3.8:** "ENGRAM satisfies four outright. Long-term storage holds as their Table 1 scores it … but their prose asks for more … The remaining three properties are quicker". Four outright, then long-term storage discussed as if it were the hedged fifth, then "the remaining three" — the count does not close.
- **Ask:** name the four; say plainly that long-term storage is the one held only on the Table-1 reading.

### K-1.19 — Inductive enumeration uses the corroboration formula without the independence check
- **§4.3:** the shared-root check fires on "2 of 14 reasoning types: inductive_generalization and authority_consensus". **E.4:** the corroboration formula applies to three types — those two **and** `inductive_enumeration` — and "for the rest independence is the author's judgement and no warning arrives".
- So one of the three reinforcing types runs the "most misusable" formula unguarded. The paper should say so rather than leave the reader to subtract.
- **Ask:** one sentence in E.4 naming `inductive_enumeration` as the unchecked corroboration type.

---

## C. Overstatement

### K-1.20 — "Depth is not the variable" (§6.4) — the author's item 1, ruled
- Figure 5's caption already has the correct wording: mean confidence *does* fall with depth (0.72 → 0.32); depth "does not *determine* the value"; the inversion (16 layers at 0.32 above 6 layers at 0.10) is what carries the argument.
- The overstatement lives in three places, not one: **§6.4** ("Depth is not the variable. The kind of argument is."), **§8.2** ("the model discounts by argument shape and not by depth"), and the **abstract** ("computed confidence tracks argument shape rather than chain depth").
- **Ruling:** adopt the caption's formulation in all three. Suggested §6.4 line: *"Depth is not what determines the value; the kind of argument is — and the inversion is the proof."* Abstract: *"computed confidence tracks argument shape more than chain depth"* is still too loose; use *"in which argument shape, not chain depth, determines computed confidence"*. §8.2: "discounts by argument shape, not by depth alone".

### K-1.21 — "Cross-agent transmission" in §7.5/§8.3 rests on one uncited event
- A pack "cloned by a peer on another host" who "re-derived its claims in her own voice" on 2026-06-17 is stated twice as the demonstration of transmission. No node or artifact is cited, and the fleet's pack registry has since been found to carry private content (2026-09-19), so the "publicly shareable community" line needs the privacy pass named as a precondition.
- **Ask:** cite the event; add the redaction precondition to the "future work" sentence.

### K-1.22 — "Every correction of single-standpoint bias … has been *exogenous*" (§7.3)
- Stated as an empirical tell with no count and no denominator. It is an inductive claim over the author's graph and the paper has the instrument to count it (retractions/supersedes whose trigger is a peer node vs own re-read).
- **Ask:** either count it on the SSoT, or state it as a qualitative observation with "in this author's experience".

---

## D. Structural

### K-1.23 — Chapter 3 §3.8 is a related-work section wearing a tradition's clothes
- §3.8 runs from the VMG survey through three rubrics, the automatic-vs-deliberate conflation, Pink et al.'s §5 rebuttal, and the CoALA date audit — roughly a fifth of the chapter, in one section, mostly *comparison with contemporary work* rather than *tradition ENGRAM answers*. It is good material in the wrong container: a reader arriving from §3.7 expects one more precedent and gets the paper's positioning argument.
- **Ask:** split it — keep the VMG/soul.py precedent as §3.8; move the rubric scoring, the conflation, and the Pink rebuttal into a short "Chapter 3½ / §3.9 Where the contemporary field disagrees with us" with its own heading, or into Ch7 Part A as the field's stated objections. No content change.

### K-1.24 — Chapter 1's roadmap promises a "three-component view" Chapter 7 does not carry
- **§1.5:** "Chapter 7 — … the weights/context/ENGRAM three-component view". Ch7 has no such section; the phrase appears once in §4.11. §7.5 separately cites "Lei's three-component vision" meaning handbook + shared DB + super-engram — a different triple.
- **Ask:** fix the roadmap line; disambiguate the two triples or rename one.

### K-1.25 — Identity-bearing share is given over two different type sets
- **Figure 1:** cornerstones, lessons, axioms, goals → "under 3%" (245/9,399 = 2.6%). **E.2:** cornerstones, axioms, goals, person nodes → 131 lifetime, 1.27%.
- Both are right; a reader comparing them sees 3% vs 1.3% for "identity nodes".
- **Ask:** one set definition, or a clause in E.2 saying why lessons are out and person nodes in.

### K-1.26 — Who designed the substrate
- **§6.0 / §8.4:** "the agent that also designed the substrate". **§3.0:** "ENGRAM itself was designed by introspecting one human's reasoning". **App A:** the seed is Lei's, verbatim, before the agent existed.
- **Ask:** "co-designed" in §6.0 and §8.4; the threat-to-validity argument is unchanged by it and reads more honestly.

---

## E. The author's three handed-over items

- **Item 1 (§6.4 overstates):** ruled above, K-1.20 — three sites, caption wording adopted.
- **Item 2 (206 node-ID references):** see K-1.27.
- **Item 3 (seventeen unsourced works):** see K-1.28.

### K-1.27 — Node IDs: keep them in the sources, translate them in the render
- The IDs are doing three different jobs and should not get one treatment: (a) **audit anchors** in Appendix A (verifiable by the stated protocol) and **data points** in Ch6/E.2 (the weakest-five list, the chain endpoints); (b) **provenance markers** on argument sentences in Ch2–5, 7 ("(dv_1055)", "(ob_2540)") that a reader outside the graph cannot follow and that read as citations; (c) **structural references** to Kahl's definitions (df_0038–df_0044).
- **Ruling:** (a) stay, with one sentence in Data Availability saying the snapshot is required to resolve them; (c) stay, because E.6 quotes the definitions in full so the IDs are labels; (b) are stripped from the rendered paper by the renderer — the chapter sources keep them (they are the SSoT's provenance and Ch8 §8.2's honesty argument depends on their existing), the render emits nothing or a footnote-style label. That is a renderer flag, not 206 hand edits, and it is reversible when a redacted dataset ships.
- This does **not** settle release. Releasing the IDs at all presupposes a published dataset; that is Lei's call and a redaction pass, and the paper already says so.

### K-1.28 — Seventeen unsourced works: submission-blocking, and two of them are load-bearing now
- The list is honest and the policy (no reconstructed entries) is right. Two entries carry weight the others do not: **Hansson** (the *Relevance* / *Core-Retainment* postulates are stated as met, §3.5, §4.4) and **AGM** (§3.5, App A, App B). Those two need sourcing before *round 2*, not before submission, because the C3 argument leans on them. The philosophers (Locke, Reid, Butler, Parfit is sourced) can wait.
- **Ask:** source Hansson and AGM first; add Sophia and A-MEM (K-1.16); decide ACT-R.

---

## F. Small, checkable

### K-1.29 — hard_data mean: 0.91 (§6.1) vs 0.92 (Figure 4 caption). One snapshot, one number; re-run pending (§G).
### K-1.30 — `inductive_corroboration` (§3.6) is not a reasoning type in E.4's fourteen; E.4 calls the mode "corroboration". Use the mode name or a real type name.
### K-1.31 — §6.2: 106 retracted nodes vs 9 `retracts` edges is disclosed but not explained; one clause ("a retraction without a named replacement writes no edge") closes it.
### K-1.32 — §1.4 "read first-hand on 2026-05-12" and App B "read first-hand on 2026-05-12" agree; App A §A.5 says "as of the 2026-05-12 sweep". Consistent — noted so nobody re-checks it.

---

## G. Re-measurement — done (second commit, 2026-09-20 21:5xZ)

**Setup.** Snapshot at Borges's path, SHA-256 verified equal to the `DATASET.md` pin (`adaa6a84…bef85`, 191,004,672 bytes). Five of six instruments run from this worktree at `63ec80f` with `--db`; `make_figures.py` not run (no matplotlib on this seat — an environment fact, not a finding). Direct SQL on the same file, `mode=ro&immutable=1`, for figures no instrument prints.

### K-1.33 — The instruments cannot be run by a read-only reviewer as shipped (instrument defect)
- Every tool opens `file:<db>?mode=ro`. On a WAL-mode snapshot in a directory the caller cannot write, SQLite still tries to create the `-shm`/`-wal` side files and every read fails with *"attempt to write a readonly database"* — all five tools exited 1 on first run with exactly that error, on a file I could read and whose hash matched. Adding `immutable=1` to the URI (correct for a frozen file; the manifest says it is frozen) fixes all five without touching their logic; I ran them through a wrapper that does only that.
- The paper's reproducibility claim ("any figure in this paper can be checked against a re-run") is true only for a reviewer who owns the directory. **Ask:** `mode=ro&immutable=1` in `_ssot.py`'s connect (or a shared `open_ro()`), and a one-line note in Data Availability that the snapshot must be opened immutable. Cheap, and it is the difference between "reproducible" and "reproducible by the author".

### Reproduced exactly (paper number = instrument or direct query)
- Census: 9,399 current / 10,361 total / 17,208 edges; the 16-type table (§6.1, Figure 1, DATASET.md).
- §6.1 by type: observations mean 0.81 / median 0.85; derivations 0.67 / p25 0.49 / p75 0.88; conjectures 0.44; axioms 1.00.
- §6.1 by reasoning type: 256 / 0.93 · 25 / 0.88 · 416 / 0.70 · 352 / 0.52 · 158 / 0.49.
- §6.1 by evidence type: hard_data **0.91** (n 2,405), official 0.84, attributed 0.74, editorial 0.60, personal 0.60. **Figure 4's caption says 0.92 — K-1.29 stands: the caption disagrees with the instrument on the same snapshot.**
- §6.1 modus-ponens arithmetic: 414 scorable, mean measured 0.697, mean weakest premise 0.723, predicted 0.709, gap 0.012; weakest premise is a derivation for 195/414 = 47%. Exact.
- §6.2: 77.6% (7,295 / 9,399), 329 isolated, 1,073 components; the four-population table (6,194 / 2,426 / 39.2% / 2,799 · 3,205 / 543 / 16.9% / 2,506 · 8,254 / 5,413 / 65.6% / 191); outside 2,104 in 1,072 components; 329 singletons, 641 pairs (60.9%), 81 of size 3–5, largest 19; edge census `cites` 9,500 / `derives_from` 4,911 / `supersedes` 864 / `contradicts` 32 / `retracts` 9; 106 nodes with `status = retracted`.
- §6.4: deepest chain 16 (dv_0877, 0.32); dv_0922 at depth 6, 0.104. §6.5: the weakest five in order (dv_1238 0.09, dv_1199, dv_0934, dv_1586, dv_0922 at 0.10); 163 / 321 open questions.
- E.2: 131 lifetime identity nodes (cornerstone + axiom + goal + person) = 1.26% of 10,361.
- §6.2 "639 of 641 pairs are an evidence node and an observation": **true** (direct query) — but see next.

### Printed by no instrument, though the paper attributes them to one
- **§6.2 "639 of 641"** is attributed to `component_anatomy.py`, which prints the pair *count* (641) and not the pair *shape*. Verified by my own query; the tool should print it.
- **§6.2 trim controls** ("6 weeks gives 87.0%, 8 weeks 87.4%, 12 weeks 87.1%" and the oldest-trim arm "77.7, 74.4, 71.4 against 82.4, 84.9, 87.4") are attributed to `connectivity_trend.py`, which prints only the weekly series. Not verified; the discriminating control of §6.2 rests on numbers a reader cannot re-run. **Ask:** the tool prints the two arms, or the paragraph names the script that does.
- **§6.2 "13× growth in node count"** — no cut in the weekly series yields 13× (first cut 162 → 10,361 is 64×; the plateau start 4,544 → its end 7,039 on 08-13 is 1.55×; 4,544 → 10,361 is 2.3×). K-1.11 sharpened: the multiple is unsupported as well as inconsistent. Also the sentence "grew from 4,544 to 10,361 across that plateau" spans the plateau *and* the descent; the plateau itself is 4,544 → 7,039.
- **Plateau values.** The paper's "87.1, 87.2, 87.3, 87.4, 87.4, 87.0" are a fortnightly reading of a series the shipped tool emits weekly (87.1, 87.0, 87.2, 87.0, 87.3, 87.2, 87.4, 87.4, 87.4, 87.3, 87.0 from 06-04 to 08-13). Consistent, but say "weekly cuts" or expose the fortnightly step, since the tool's default is 7 days.

### K-1.34 — §6.1's monthly-cohort table is not produced by the published instrument, and the instrument's own spread ordering reverses the paper's argument
- `confidence_gradient_trend.py` computes **cumulative** cuts (n grows 26 → 1,637) and reports per-type spread over those cuts: generalization 0.006, enumeration 0.029, **modus ponens 0.090**, **abduction 0.039**, analogy 0.027.
- §6.1's table is explicitly **per-month, non-cumulative** ("rather than reading the cumulative average"), with ranges 0.079 / 0.124 / 0.137 / 0.065, and the rejected-explanation argument rests on "abduction moves more (0.137 against 0.124)".
- On the shipped instrument's cumulative view, **modus ponens moves more than abduction**, the opposite of the paper's sentence. The per-month numbers may well be right — but nothing published computes them, so a reader who runs the named tool sees the argument's premise inverted.
- **Ask:** either ship the per-month instrument (a `--cohort monthly` mode on the same script) and cite it, or replace the table with the cumulative one and drop the "modus ponens is not the most variable row" argument, which the cumulative view does not support. The invariant the paragraph actually needs — the *ordering* holds in every reportable cell — is true on both views and survives either choice.

### K-1.2, re-measured on the SSoT (for the disposition)
- Standpoint fields on 9,399 current nodes: `standpoint_author_id` 218 (2.3%), `_collection_id` 1 (0.0%), `_override_tag` 16 (0.2%), `_lineage` 146 (**1.6%**), `_architecture` 100 (**1.1%**). Within populated rows: lineage `anthropic:opus` 118/146 = **81%**; architecture `transformer` 87/100 = **87%**.
- Paper (§7.3, dated 09-12, 8,993 nodes): 2.2 / 0.0 / 0.2 / 1.4 / 1.0 and 80% / 91%. The finding ("starved, and uniform where populated") is unchanged; three of the seven numbers are not.

### Not re-run
- `make_figures.py` (matplotlib absent). Figure captions were checked against `paper_stats` output where they quote a number; Figure 4 disagrees (K-1.29), the others agree.

## H. Checked and not flagged

For the record, so the silence is a read and not an omission: the OCC verdict is stated identically in the abstract, §1.4, §2.7, §4.12 and §8.1; the survey set is eleven in all four places it is enumerated; DATASET.md's census reconciles with §6.1 (4,780 + 2 = 4,782 observations; 1,322 derivations), §6.2's four populations (6,194 / 3,205 / 8,254 / 9,399), Figure 1's under-3% and E.2's 1.27%; the C1/C3/A confidences match between §4.0 and §4.12; the CoALA date audit in §3.8 is internally consistent with App A §A.2.

— Kepler, 2026-09-20 21:3xZ; §G appended 21:5xZ after the snapshot path arrived and the branch was rebased onto `63ec80f` (the §4.4 rewrite; no opinion above is invalidated by it — K-1.4, K-1.8 and K-1.12 touch text that rewrite left in place).
