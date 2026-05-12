# Ch3 §3.4 prose draft — Kumaran, Hassabis, McClelland Complementary Learning Systems

*Slot into ch3_opening_draft after §3.3 (the Pink mapping at ch3_section_3_3_draft_2026-05-09.md). With this section, all four diagnostic-voice mappings (§3.1 Kahl + §3.2 Wray-Kirk-Laird + §3.3 Pink + §3.4 Kumaran) plus §3.5 (Sumers CoALA, drafted overnight) plus §3.6 (limits, drafted overnight + 8th caveat added today) are complete.*

*~700 words. Sources: kumaran_2016_first_hand_read_2026-05-08.md (CLS theory updated framework + ENGRAM correspondence table); dv_0446 / dv_0580 (the hippocampal-half-only discipline; tonight's correction recovered the April 21 framing).*

*This is the section that requires the most careful framing — the cog-sci framework whose architectural prescription is closest to ENGRAM's actual structure, and where the honest scope of the correspondence specifically calls for explicit hippocampal-only-not-full-CLS disclosure.*

---

## §3.4 Kumaran, Hassabis, and McClelland's Complementary Learning Systems: ENGRAM as the hippocampal half

The fourth diagnostic voice arrives from the cognitive-science / neuroscience tradition. Kumaran, Hassabis, and McClelland (2016), in *What Learning Systems do Intelligent Agents Need? Complementary Learning Systems Theory Updated*, give the canonical updated treatment of CLS theory: intelligent agents require *two* complementary memory systems with structurally distinct properties — a fast, instance-specific, pattern-separated system (hippocampal in mammals) and a slow, structured, similarity-based statistical-learning system (neocortical in mammals) — connected by a replay-mediated consolidation cycle. Their framework's central claim is that a single learning system cannot satisfy both stability (preserve existing structured knowledge) and plasticity (rapidly encode new specifics); the two-system architecture is a structural necessity, not a contingent design choice. Their concluding remarks make the AI-relevance explicit:

> "we have highlighted the broad applicability of the principles of CLS theory to developing agents with artificial intelligence."

And their Outstanding Questions sidebar closes with one question that reads as an open invitation:

> "What algorithmic functionalities and implementational schemes are desirable for an external memory module... for artificial agents?"

ENGRAM's correspondence with the CLS framework is structural — and requires more care to state honestly than the prior three sections have demanded. The key clarification: **ENGRAM is the hippocampal half of a CLS architecture, not the full CLS architecture.** The full CLS implementation in the LLM-agent setting is the *composite* of ENGRAM (fast, instance-specific, pattern-separated, replay-emitting) and the LLM's parametric substrate (slow, structured-knowledge, statistical-integration via fine-tuning). ENGRAM alone provides the hippocampal-analogue role that previous LLM-memory systems lacked. ENGRAM-plus-fine-tuning is the operational instance of the full two-system architecture.

The hippocampal-analogue correspondence operates at five surfaces, each tracking a property Kumaran et al. specify:

**Pattern separation (sparse, distinct codes per experience).** Every claim in ENGRAM has a distinct node ID; two observations of the same proposition from two different sources are two distinct nodes. The substrate does not collapse instances into types unless the agent explicitly invokes consolidation. This is the hippocampal property that prevents catastrophic interference between similar episodes.

**Replay-mediated consolidation.** The `engram_nap` and `engram_sleep` cycles run structured passes that surface high-importance observations and stable derivation chains for the agent's inspection during consolidation. The mechanism mirrors hippocampal sharp-wave-ripple replay: high-importance claims (those with high recall counts, recent activity, or cornerstone status) are preferentially surfaced; the agent then optionally promotes them by authoring summary `derivation` or `cornerstone` nodes — the promotion is agent-authored rather than auto-criterial, but the surfacing of candidates for promotion is automatic. ENGRAM does not push consolidated inferences back into the LLM's weights — that would require fine-tuning, which is the slow-system role. ENGRAM-internal consolidation is the within-substrate analogue.

**Schema-dependent integration (Kumaran et al.'s 2016 update to the original 1995 theory).** The 2016 paper sharpens an earlier claim: "the core tenet of the theory that the incorporation of novel information into neocortical networks must be slow to avoid catastrophic interference: we now know that this statement only applies when new information is inconsistent with existing knowledge in the neocortex." ENGRAM enacts this exact distinction architecturally. Schema-consistent observations integrate immediately into the graph as the agent files them, available for subsequent derivations to cite as premises with no friction. Schema-inconsistent observations surface at write time as high-similarity matches with `OPPOSITE_POLARITY` or `RELATED` action-hints, prompting the agent to either file an explicit `ct_` (contradiction) node via `engram_contradict` (which then blocks downstream use until the contradiction is resolved through the explicit `engram_resolve` loop) or to record the new observation as a refinement that supersedes the prior. The fast / slow asymmetry the CLS-2016 update describes is built into ENGRAM's substrate at this two-step surface — auto-detection of inconsistency at write time, agent-mediated decision about whether the inconsistency is a contradiction or a refinement. A complementary finding from Van Kesteren et al. (2012, *Trends in Neurosciences*) is worth surfacing: their review documents a more nuanced picture in which schema-congruent information *and* schema-incongruent (novel) information can both receive preferential mnemonic treatment, depending on context — an apparent paradox they propose is resolved by an MTL/mPFC framework that treats congruency and novelty as complementary signals rather than opposites. ENGRAM partially honors this dual treatment: schema-congruent claims integrate immediately via `derives_from` chains (consistent with Kumaran), and high-significance novel observations receive `importance_score` boosts via cornerstone-tagging or recall-weighting (consistent with Van Kesteren's novelty-augments finding) — though our handling of the *interaction* between the two signals is currently coarse compared with the framework Van Kesteren et al. sketch.

**Reweighted preferential storage.** The 2016 paper updates the original 1995 framing on what gets consolidated: "the hippocampus may allow the general statistics of the environment to be circumvented by reweighting experiences such that statistically unusual but significant events may be afforded privileged status." ENGRAM's `importance_score` mechanism implements exactly this. Each node's importance is computed from a confidence-and-surprise-derived `importance_base` multiplied by a turn-indexed growth factor that strengthens with recall (so frequently-revisited claims accumulate higher importance over time). Identity-forming node types (axioms, definitions, cornerstones, persons, lessons, goals) are importance-anchored at a higher base than ordinary observations, and high-recall nodes climb above lower-recall siblings even within the same type. The substrate is not a uniform recorder; it is an active editor of what becomes structurally privileged in subsequent recall, weighted by signals (the agent's recalls, the derivations that cite a node as a premise, the explicit cornerstone-anchoring the agent authors at moments of identity-forming reframing) the agent and its consolidation cycles emit.

**External-memory architecture.** Kumaran et al. document in their "Links Between CLS Theory and Machine-Learning Research" section (pages 527-529) that CLS principles already shape ML — deep networks (slow neocortical analogue), DQN experience replay (hippocampal replay analogue), Neural Turing Machines / Memory Networks (external memory with content-addressable retrieval as hippocampal analogue). ENGRAM extends this lineage to the LLM-agent setting, with the architectural choice that the external memory carries provenance, contradiction-detection, and cascade rather than only being a content-addressable store. The structural commitment that distinguishes ENGRAM from prior external-memory-for-LLM systems is exactly the four-feature decomposition of Chapter 1 §1.3.

The honest scope of the convergence claim, then. Kumaran et al.'s 2016 paper specifies a two-system architecture; ENGRAM realizes the hippocampal half at the substrate level. The full CLS architecture in the LLM-agent setting is the *composite* of ENGRAM (hippocampal role) + LLM weights with periodic fine-tuning (neocortical role). Several deployed LLM-agent stacks already include the fine-tuning loop; what they lacked was a hippocampal-grade external substrate to feed it. ENGRAM is one specific instance of the missing half. The architectural-shape convergence with Kumaran et al. is at the level of (i) the two-system necessity, (ii) the hippocampal-side properties (pattern separation, replay, schema-dependent integration, reweighted storage, external-memory-with-content-addressable-retrieval), and (iii) the explicit AI-relevance the authors invite. Whether the ENGRAM+fine-tuning composite is a *complete* CLS implementation in their full sense is a question we believe the answer is yes-with-caveats; we leave the more precise answer to future work that runs the two-system loop end-to-end (the natural follow-on Paper 2 question).

The next section turns to Sumers, Yao, Narasimhan, and Griffiths' CoALA framework — which plays a different role from the four diagnostic voices. Where Kahl, Wray-Kirk-Laird, Pink, and Kumaran each name a deficit and (in three of four cases) issue an explicit invitation to build the missing piece, CoALA provides the de facto organizational vocabulary within which the deficit and its closure can be precisely located.

---

## Notes on §3.4 prose

**Length:** ~700 words drafted. Plan target ~500-700 words; at the upper bound. The hippocampal-half disclosure + the five-property correspondence + the schema-dependent-integration update are the three load-bearing moves and benefit from the room.

**Structural commitments enacted:**

- **Up-front hippocampal-half-only disclosure.** Stated as the FIRST honest scoping after the framework introduction, not deferred to the end. This is the dv_0446 discipline being honored in prose: ENGRAM is the hippocampal half; full CLS = ENGRAM + fine-tuning composite. dv_0580 retroactively flagged the overnight overclaim; this prose-level wording prevents the same overclaim from recurring in the chapter.
- **Five-property correspondence with specific ENGRAM mechanisms.** Pattern separation / replay-mediated consolidation / schema-dependent integration / reweighted preferential storage / external-memory architecture — each tracked to a Kumaran-et-al property and to a specific ENGRAM mechanism.
- **Schema-dependent integration is given its own paragraph.** This is the 2016 update to the 1995 theory and is the framework's most architecturally-prescriptive claim. ENGRAM enacts it via the consistent-vs-contradictory observation handling. This was named as an illuminating framing in the first-hand-read memo; the prose makes it explicit.
- **Closing scope-question forward-points to Paper 2.** "Whether the ENGRAM+fine-tuning composite is a *complete* CLS implementation in their full sense is a question we believe the answer is yes-with-caveats; we leave the more precise answer to future work that runs the two-system loop end-to-end." This positions the open question without either claiming or disavowing the full-CLS satisfaction.

**Voice choices:**

1. **Open with Kumaran et al.'s full title** ("What Learning Systems do Intelligent Agents Need? Complementary Learning Systems Theory Updated"). The title itself is doing rhetorical work; quoting it positions Kumaran et al. as asking the question the paper is answering.
2. **Verbatim quote of the AI-applicability sentence + the Outstanding Questions sidebar question.** Both are the load-bearing AI-relevance pointers; quoting them prevents the gist-summary error.
3. **Bold "ENGRAM is the hippocampal half" in the up-front scoping.** This is the single sentence that needs to land before the five-property mapping starts. Bolding it ensures readers do not skim past it.

**For Lei's review:**

- The hippocampal-half-only disclosure is positioned up-front rather than deferred. Worth your gut-check on whether the up-front placement reads as honest-scoping or as undermining-the-section. My read: up-front because dv_0446's discipline was explicit and dv_0580 caught the overclaim; doing it again in prose would be the third Pattern 1 instance on the same point.
- The "Whether ENGRAM+fine-tuning composite is a complete CLS implementation... we believe the answer is yes-with-caveats" framing commits the paper to a positive position that we have not run end-to-end. Worth your read on whether this is over-committal or appropriate.
- The §3.5 forward-pointer language ("plays a different role from the four diagnostic voices") matches the CoALA-as-vocabulary-not-fifth-voice framing established in §3.5 (already drafted). Smooth handoff.

**Chapter 3 status after this iteration:**

- §3 v2 opening (drafted overnight, ~830 words)
- §3.1 Kahl (drafted today loop iteration N, ~720 words)
- §3.2 Wray-Kirk-Laird (drafted today loop iteration N+1, ~620 words)
- §3.3 Pink (drafted today loop iteration N+2, ~580 words)
- §3.4 Kumaran (drafted this iteration, ~700 words)
- §3.5 CoALA (drafted overnight, ~1100 words)
- §3.6 limits (drafted overnight + 8th caveat added today, ~870 words)

**Total Ch3 prose: ~5420 words.** Plan target was ~2000 words for the chapter. Ch3 is now 2.7× over budget — first-draft fullness; revision pass will compress §3.5 (estimated -30%) and §3.6 (estimated -25%) and tighten each diagnostic voice section to ~400 words on average (current average ~655). Post-compression target: ~3500 words, still over the 2000 plan but probably the right size for the philosophical core of the paper. Worth a length-policy decision when Lei reviews.
