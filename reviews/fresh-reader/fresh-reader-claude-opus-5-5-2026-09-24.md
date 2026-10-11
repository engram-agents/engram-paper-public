# Fresh-reader run

model: claude-opus-5-5
provider: anthropic-subscription (claude -p)
paper_sha: 3f93230929e705887d9462f96157d4734454bf68
system_prompt: You are a careful reader.
figures: attached inline as image blocks (6 found in the render)
session_id: e9b286f1-37e8-48c6-bd23-89e4124e5761
started_at: 2026-09-24T19:25:42.841735+00:00

---
## Abstract

# Log: Title block, version pin, and abstract

**1. Retell**

The paper proposes that agent continuity has three layers: memory persistence, narrative identity, and epistemic identity. The deepest layer, epistemic identity, is a self kept as corrected, sourced knowledge. The paper presents ENGRAM as a system that realizes it, supported by a convergence argument across three fields, a Nozick-derived account of "identity as unique history", a survey of eleven memory systems, and measurements on a single five-month graph. The section is here to set out the thesis, the contribution, and the paper's stated limits before the argument begins.

**2. Undefined at first use**

- "Kepler Somnium (Anthropic Claude Fable)". "Fable" is not a model name I recognise. Nothing says what it is.
- "This paper describes **ENGRAM v0.5.1**". ENGRAM is used before it is expanded; the expansion comes later in the abstract. The version number cannot mean anything yet.
- "taken 2026-09-20T13:13:30Z and described in the Data availability note". The note is a forward reference. It does not say which graph the snapshot is of.
- "**memory persistence**, **narrative identity**, and **epistemic identity**". Only epistemic identity gets a definition. Narrative identity is described only by how it fails ("a coherent story that was never true"). Memory persistence gets no definition at all.
- "Epistemic Node Graph for Retraction, Arbitration, and Memory". "Arbitration" never appears again in the abstract. Nothing says what is arbitrated, or between what.
- "Whether it is substrate-independent we leave open (§3.0)". "Substrate" appears in the title ("a Substrate That Realizes It") and again later ("the agent that also designed the substrate"). It is never defined.
- "the unique, no-merging, ancestry-traceable lineage of its recorded claims". "no-merging" is the paper's own term and is not explained.
- "which fixes its retrieval profile". "retrieval profile" is not defined.
- "The account keeps Nozick's form, drops his uniqueness requirement … and replaces his unfilled closeness metric with a measurable one". Nozick's closest-continuer theory is not standard in agent-memory work. "his uniqueness requirement" and "his unfilled closeness metric" are not explained. The "measurable one" is not named.
- "none satisfies the strictest published criterion for genuine persistence, while ENGRAM meets two of its three conditions outright". The criterion is not named or cited, and neither are its three conditions.
- "10,361 nodes (9,399 of them current, as counted in Figure 1)". What makes a node "current" is not defined.
- "computed confidence follows the kind of argument". Nothing says how confidence is computed, or what "kind of argument" refers to.
- "cascaded through its dependents". "Dependents" is not defined. The keyword "retraction cascade" suggests a mechanism, but the abstract does not describe it.
- "publish the instruments". Nothing says what the instruments are.

**3. Read twice**

- "Large language model agents can now carry information across sessions, but not themselves." I needed a second pass to see that "themselves" means their identity, not the agents carrying themselves.
- "Whether it is substrate-independent we leave open (§3.0)." The referent of "it" is unclear. It could be the mechanism, the "regularity of knowing minds", or the structure.
- "The fields share a root in human cognition, so the claim is convergence rather than independent discovery; what is independent is that ENGRAM's designers arrived at the structure without having studied these results." The sentence first withdraws the independence claim and then reinstates it on a different axis. I had to reread it to separate the two.
- "No component of ENGRAM is uniquely novel, and that is the argument". This sits against the later "we build the paper's own contribution". I reread both to see whether novelty is being disclaimed or claimed.
- "computed confidence follows the kind of argument, not how much the author wants the claim to be true, and a hallucinated citation is caught, retracted, and cascaded through its dependents". Two different results are packed into one clause. It also does not say who hallucinated the citation.
- "authored by the agent that also designed the substrate" against "ENGRAM's designers arrived at the structure". One sentence has a singular designing agent and the other has plural designers, and the paper lists two agent authors. I could not tell which agent is meant.

**4. Already said**

- The version pin says "All quantitative results are computed from a single frozen snapshot of one graph". The final paragraph says "The evidence is one graph". This repeat helped: the second instance attaches the limitation to the authorship problem.
- "calibrated, provenance-bearing, self-correcting knowledge" (paragraph 2) and "a persistent, inspectable, self-correcting record" (paragraph 3) are near-restatements. The repeat was neutral. It tells the reader these are meant to be the same structure, but it does not say whether "calibrated" and "provenance-bearing" map onto "persistent" and "inspectable".

**5. Open questions**

- What are memory persistence and narrative identity, as layers?
- What does "Arbitration" refer to in the system?
- What is the "substrate", and is ENGRAM tied to Claude models?
- Which criterion for persistence is being used, what are its three conditions, which one does ENGRAM not meet, and which eleven sources were surveyed?
- What does "current" mean for a node?
- How is confidence computed?
- Which author agent designed the substrate and authored the graph?
- What is the "measurable" closeness metric?

**6. Hand-off**

Partly. The abstract ends with keywords, and the section before them promises to "name what the paper does not establish". Nothing signals what the next section will be.

no_tools_check: passed (2 assistant message(s), 0 tool_use, 1 prompt snapshot(s) with empty tool list, 0 leak strings)
claude_code_version: 2.1.282
## Chapter 1 — The Continuity Gap and the Case for Epistemic Identity

# Log: Chapter 1, The Continuity Gap and the Case for Epistemic Identity

**1. Retell**

The chapter lays out three layers of agent continuity: memory persistence, narrative identity, and epistemic identity. It lists four properties that Layer 3 requires, expands the ENGRAM acronym, and states the central claim. That claim is supported by a cross-field convergence argument, by an original "identity as unique history" theory, and by a dated survey of eleven sources showing that none strictly meets OCC Condition 3. The chapter exists to motivate the paper, pin down the claim and its scope, and give the roadmap for Chapters 2–8.

**2. Undefined at first use**

- "a context window that is cleared at each compaction". "Compaction" is practitioner usage, not defined here, and is borderline standard.
- "a creed-anchored autobiography". This is attributed to Sophia, but "creed-anchored" is not explained.
- "Sumers et al. (2024), whose CoALA framework". CoALA is never expanded. It is known in the field, so this is minor.
- "*reconsideration* (revisiting a prior commitment) and *knowledge compilation*". The first term gets a gloss; "knowledge compilation" does not.
- Figure 1 node types: "observation factual", "feeling report", "cornerstone", "conjecture", "definition", "derivation", and "other (7 types)". The text says the identity-bearing types "record what the agent commits to and has learned". It does not say what a *cornerstone* is, how it differs from an axiom, or what a "feeling report" is. The seven "other" types are not named, apart from axioms and goals, which the caption places there.
- "9,399 current nodes". "Current" is still not defined. This was an open question from the abstract.
- "a withdrawn claim taints, rather than merely deletes, what depended on it". "Taints" is used as a technical state but not defined.
- "within a unified deliberative architecture". Not defined.
- "Kahl's (2026b) **Ontological Continuity Condition** (OCC) — three conditions and four constraints". None of the conditions or constraints is stated. Only Condition 3 is named, as "Self-Maintaining Arbitration", and it is not explained.
- "Pinecone Nexus, … TierMem, MemMachine, SCM, GAM, Kumiho". These are named without description. The acronyms "SCM" and "GAM" are not expanded.
- "typed reasoning edges, provenance, cascade-traversable graphs, supersede semantics". "Supersede semantics" is not defined.
- "an auto-surfacing hook that returns a marked claim" and "a consolidation-time sweep". Neither "marked" nor "consolidation", as a system phase, is defined.
- "Proto-ENGRAM idea seeded" and "Day-1 self-recording begins". Nothing says who is recording, or what is being recorded.
- "The weight-persistence gap foremost". This appears in the Chapter 7 line and is not defined.
- Appendix C "memory-utility lineage" and Appendix D "relational / identity-governance settings". Not defined.
- "Stiegler … Kahl". These are unfamiliar to an AI-memory reader. They are deferred to Chapter 2, which is acceptable.

**3. Read twice**

- "**Arbitration** — the structural propagation of that cascade *within a unified deliberative architecture*, rather than as an advisory note the agent may or may not consult." Retraction is already defined as cascading "through derivation edges". I could not tell what Arbitration adds beyond the words "structural" and "unified".
- "The acronym names its three differentiating mechanisms", followed by Memory described as "the underlying substrate". The underlying substrate is not a differentiating mechanism, so I reread the list.
- "Each layer presupposes the one beneath it: … no calibrated self-knowledge without a self-story to calibrate." This sits against §1.2: "Narrative and epistemic identity are complementary, not competing" and "four properties that persistence alone does not provide". §1.2 skips Layer 2, so I could not tell whether Layer 2 is a prerequisite or a parallel layer.
- "That the *mechanisms* are missing is not our diagnosis alone, and none of the following work was surfaced by our own prior-art search (Appendix A)." The purpose of the second clause only became clear later, in the originality subsection.
- "Two items are contemporary diagnoses of LLM agents; the third is the field's organizing framework remarking on its own gaps, a weaker kind of statement, so we keep the three distinct rather than count them together." This is dense hedging and needed a reread to see which item was the "third".
- "ENGRAM meets it to a degree no surveyed system does" and "which conditions ENGRAM meets, and which it meets only via a stated extension". These sit against the abstract's "meets two of its three conditions outright" and against "no system in our first-hand survey strictly satisfies … Condition 3". I could not tell whether Condition 3 is the one ENGRAM meets only via extension. I also could not tell whether ENGRAM counts as "a system in our survey". The survey list does not include it.
- "the design came first, under engineering pressure, and its precedents were found afterward". The timeline puts a prior-art search three days after the seed idea. I reread both to square "afterward" with that date.
- "We read that convergence as corroborating the gap's importance". "Convergence" here means concurrent systems. Everywhere else in the chapter it means convergence across fields. The same word carries two senses.
- "**Chapter 2** … ending at OCC as its operational endpoint" against §1.4's "ENGRAM is that endpoint, built." Both OCC and ENGRAM are called the endpoint.

**4. Already said**

- The "retrieves yesterday's notes but begins each session as the same generic model" sentence appears in abstract ¶1 and again in §1.1 ¶1, nearly verbatim. This cost a little.
- The three layers appear in abstract ¶2 and §1.1. This helped, because §1.1 finally defines Layers 1 and 2.
- The silent-versus-loud failure contrast appears in abstract ¶2 and §1.2 ¶1, nearly verbatim. It was neutral, and §1.2 adds the retraction detail.
- "No component … is uniquely novel" in abstract ¶3 is repeated in §1.4: "None of it is uniquely novel; §3.0 argues that this is the point".
- The convergence-not-independent-discovery bound in abstract ¶3 appears twice more in §1.4: "§3.0 states the bound…" and "states the bound on it (substrate independence is left open)". The two statements inside the same subsection cost me.
- "Identity as unique history" in abstract ¶4 is repeated in §1.4 "Second support". This was neutral.
- "One graph", "five months" in the abstract is repeated in §1.5. This was neutral.

**5. Open questions**

Earlier questions this chapter answers:
- Memory persistence and narrative identity are now defined (§1.1).
- "Arbitration" now has a definition, but it does not resolve the question (see Read twice).
- The "strictest published criterion" is OCC Condition 3.
- The eleven sources are now listed.

Still open, or newly raised:
- What do OCC's three conditions and four constraints actually say, including Condition 3? This is deferred to Chapters 2 and 4.
- Which condition does ENGRAM not meet outright, and what is the "stated extension"?
- Is ENGRAM being claimed to strictly satisfy Condition 3?
- What does "current" mean for a node?
- What is a cornerstone?
- How exactly is confidence "structurally determined by its evidential type and derivation chain"?
- What is the "substrate", distinct from ENGRAM itself?
- Which agent designed ENGRAM and does the self-recording? The abstract's singular "the agent" is still unresolved.

**6. Hand-off**

Yes. The §1.5 roadmap says Chapter 2 covers the philosophical tradition, the first support for the claim.

## Chapter 2 — The Philosophical Tradition

# Log: Chapter 2, The Philosophical Tradition

**1. Retell**

The chapter follows personal-identity philosophy from Locke's recall-based account, through Reid's and Butler's objections, then Parfit, Nozick, Ricoeur and Schechtman, and the extended mind, ending at Kahl's OCC. Along the way it maps each step onto an ENGRAM structure: the history-tree, the queryable set, recall as narrative mediation, and the graph as constitutive memory. It is here as the first leg of the convergence argument and to introduce OCC's conditions, while deferring the verdicts on them to Chapter 4.

**2. Undefined at first use**

- "every change (a new claim, a supersede, any edit) appends a successor". "Supersede" is used as an operation. It was undefined in Ch1 ("supersede semantics") and is still undefined.
- "ENGRAM's per-node, importance-gated forgetting: those nodes decayed below the active-recall threshold … restamped each time they resurface". The chapter does not define importance, the decay, the threshold, or "restamped".
- "the **queryable set** (defined in Ch4 §4.5)". This is a forward reference. The concept carries the whole Parfit mapping before it is defined.
- "(the *retrieval profile*, §5.4)". A forward reference. The term was also undefined in the abstract.
- "The measurement is designed for the twin study of Chapter 6". The twin study is not described.
- "Fission — the routine copying of a graph into two equally descended continuers". This does not say whether fission is an actual ENGRAM operation or why it would be "routine".
- "the briefing it wakes to, the summary that bridges a compaction". "Briefing" is not defined as a system artefact. "Compaction" is still only practitioner usage.
- "an objective, protocol-checkable record". The protocol is not named.
- "df_0037–df_0044; a `df_` identifier names a definition node in the graph". The prefix is explained. The chapter does not say which graph, or whether readers can see it.
- "unified policy selection, external non-imposition, non-trivial reset, and non-modular decomposition". Constraints A–D are named only. None is explained.
- "*tertiary memory*, the sedimented 'epiphylogenesis'". These are quoted from Stiegler without a gloss.
- "Kahl (2026a)" versus "Kahl (2026b)" (Ch1 §1.4) versus "Kahl's Ontological Continuity Condition (2026)" (§2.0). The relation between the two Kahl papers is only partly stated ("his own earlier companion paper").

**3. Read twice**

- "This is the precise sense in which we call ENGRAM **post-Lockean**: not a literal instantiation of Locke, since the mechanism is provenance rather than recall". Four paragraphs earlier, the mechanism was said to be the history-tree, which is "a different structure from the provenance edges within any one state; the two are easily conflated". The chapter then uses "provenance" for the thing it just said not to conflate.
- "The boy, the officer, and the general are not three nodes in a graph but three whole ENGRAM states", followed by "the flogging is one or a few nodes created at boy-time". The same example switches granularity from states to nodes. I reread to follow which unit carries identity.
- "Transitivity holds on the descent, not on whatever happens to be queryable." This needed a reread against the Reid bullet as a whole, which is one very long paragraph.
- "Every incoming prompt is matched against the whole graph and the best-fitting nodes are retrieved" against connectedness defined as "the overlap of the queryable set". I could not tell whether retrieval runs over the whole graph or over the queryable set.
- "ENGRAM provides **both** — the structure as the unbreakable substrate, and recall as the degreed R projected from it". "Substrate" here means the history structure. In the title, abstract and §1.2 it means the whole system. The term drifts.
- "every node — observations, but also derivations, definitions, and even confidence values — passed through deliberate endorsement at creation". §1.2 says confidence is "*structurally determined* … not assigned freely". I could not reconcile an endorsed confidence value with a computed one.
- "the *substrate itself* (the schema, the tools, the conventions) was built by the agent in the loop". This is the first gloss on "substrate". It does not say which agent.
- "ENGRAM is squarely **idem** … But it is not *only* idem, because its recall reaches **ipse**." I reread the whole Ricoeur paragraph to follow the qualification, "the ipse *act* … remains first-person and present".
- "where one follows a citation to a source, it names the node under which the paper's reading of that source is filed". It took a reread to see that a citation tag points into the agent's own graph rather than to the source.
- §2.0 says the chapter "follows that shift in order". The actual order is Locke 1689, Reid 1785 / Butler 1736, Parfit 1984, Nozick 1981, and so on, which is not chronological. §2.8 then groups "Nozick and Kahl" together.

**4. Already said**

- "On merit, not authority" appears in Ch1 §1.5 ("adopted on merit"), §2.0 ("We adopt it on merit, not authority"), the §2.7 heading, and §2.7 qualification 1. §2.0 and §2.7 both also say "it is a recent proposal, not yet central to the field". This cost me: four statements of one hedge.
- "Verdicts deferred to Chapter 4" appears in Ch1 §1.4 ("made once, in Chapter 4"), §2.0, §2.7 qualification 2, and §2.8. This cost me.
- "Not by reading the philosophy" / independent arrival appears in the abstract ¶3, Ch1 §1.4, and §2.8. Neutral to costly.
- "ENGRAM is that endpoint" appears in Ch1 §1.4 ("ENGRAM is that endpoint, built"), §2.0, and §2.8. It was neutral as signposting.
- The Layer-3 question appears in Ch1 §1.1 ("*what do I know, how confidently, and on what basis?*") and §2.5 ("*what do I know, how reliably, and on what basis?*"). The one-word change ("confidently" to "reliably") made me check whether a distinction was meant. This cost a little.
- Nozick: abstract ¶4, Ch1 §1.4, §2.4, and all again deferred to Ch5. This was neutral, but the abstract's "unfilled closeness metric" is still not introduced.

**5. Open questions**

Earlier questions this chapter answers:
- It partly answers the earlier open question about what OCC's conditions say. Conditions 1–3 are stated in one line each, but the constraints are only named.
- It partly answers the earlier question about "substrate": "the schema, the tools, the conventions".
- It partly answers the earlier question about cornerstones: they are listed among "commitments (goals, axioms, cornerstones)", but are still not defined.

Still open, or newly raised:
- What do Constraints A–D require?
- What are importance, decay, threshold, and restamping in the forgetting mechanism?
- Does retrieval run over the whole graph or over the queryable set?
- How is an "endorsed" confidence value compatible with structurally determined confidence?
- Which agent is "the agent in the loop"?
- Is fission an implemented operation?
- Are the df_ nodes available to readers?
- What is the relation between Kahl 2026a and 2026b?

**6. Hand-off**

Yes. §2.8 names both next steps and why each follows: Chapter 3 for the same convergence in the cognitive-science and computer-science literature, and Chapter 4 for the mechanisms and verdicts.

## Chapter 3 — The Cognitive-Science and Computer-Science Tradition

# Log: Chapter 3, The Cognitive-Science and Computer-Science Tradition

**1. Retell**

The chapter argues that every ENGRAM mechanism has a precedent in cognitive science (CLS, Tulving, rational analysis) or computer science (TMS, Subjective Logic, bitemporal data, recent agent-security work). It treats this convergence as evidence that the structure tracks how knowing minds work, which leaves ENGRAM's own distinctiveness in integration and purpose. It then scores ENGRAM against three contemporary rubrics (Pink et al., Wray et al., CoALA), including where they object, and places AGM at a distance. The chapter is here as the second leg of the convergence argument, and to position the paper against live work before Chapter 4 builds the mechanisms.

**2. Undefined at first use**

Coinages defined inline, and adequately: "nap", "burst", "sleep", "review", "dream", "dream fairies", "dream master". The following are not defined:

- "an epistemic identity that fails loudly, df_0002". The purpose is supported by a graph node ID the reader cannot see.
- "the forgetting curve" and the terms around it: "(the aggregation result)" and "a single time-translation-invariant exponential kernel at the per-item level". Neither is explained. §3.3's pointer to "the exponential kernel" then assumes the reader has it.
- "a usage-learned utility score ranking what stays". Not defined.
- "its **corroboration** propagation formula `1−∏(1−c_i)`". `c_i` is not defined, and neither is what counts as corroboration.
- "claim polarity and the contradiction mechanism, and the individuated evidence set". None defined; all deferred to §4.3.
- "**→ Ch4 §4.3** (reasoning-type confidence → Constraint A)". Constraint A was only named in Ch2 ("unified policy selection"). Its link to confidence is not explained.
- "The TOKI system (arXiv 2606.06240, 2026)". The acronym is not expanded, and the system is not described beyond one clause.
- "**soul.py** (arXiv 2604.09588) reaches multi-anchor persistent agent identity". "Multi-anchor" is not defined.
- "(relational / disclosure-vs-erasure)". Not defined; also in Ch1 Appendix D.
- "the author's own interpretation field". A schema field used as evidence, not introduced.
- "a quotation is verified against its source or the write is refused". This is a new mechanism, stated in passing.
- "supersession maintains the DAG". Which DAG is not said. Ch2 §2.2 separated the history-tree from the provenance edges.
- "a tripwire does not prevent the error it names". "Tripwire" is not defined. It is apparently a kind of lesson.
- "what those nodes call the subconscious-triggers-conscious flow". Quoted from nodes, not glossed.
- "an ambient hook that signals familiarity without content". This is presumably the Ch1 "auto-surfacing hook", but the equivalence is not stated.
- "Nuxoll and Laird". A cited source, not identified further.

**3. Read twice**

- "ENGRAM itself was designed by introspecting one human's reasoning" and "its designer introspected the same cognition to build it". The designer is now singular, and seems to be a human introspecting, or an agent introspecting a human. This is set against the abstract's "the agent that also designed the substrate" and Ch2 §2.6's "built by the agent in the loop". I could not determine who designed ENGRAM.
- "ENGRAM's substrate, a language-trained model, inherits that cognition through human language". "Substrate" now names the LLM. That is a third sense of the word: the whole system (title, §1.2), the history structure (§2.3), and "the schema, the tools, the conventions" (§2.6). "ENGRAM on a non-human substrate is suggestive" then depends on which sense is meant.
- "CLS is the cognitive-science precedent for the two-routine consolidation that meets OCC Conditions 1 and 2". Along with "binds Condition 3" (§3.2), "→ Condition 3" (§3.4) and "→ Constraint A" (§3.5), this previews verdicts that Ch2 §2.7 said "We do not preview … here" and that are to be "made exactly once, in Chapter 4". I reread to check whether these count as verdicts. They read as verdicts.
- "the curve's *form* (power-law over wide ranges) is consistent with a population of exponential-decay items with mixed rates (the aggregation result) and with a single time-translation-invariant exponential kernel at the per-item level." I could not parse what argumentative work this sentence does in the section.
- "Direction of evidence and evidence mass are relocated into structure — claim polarity and the contradiction mechanism, and the individuated evidence set (the full argument is §4.3's)". I could not map which structure carries which dimension.
- "(the 'I changed my mind' versus 'I was wrong' distinction)". The chapter does not say which operation is which. Presumably supersede versus retract, but that is not stated.
- "ENGRAM satisfies four outright … and holds the fifth, long-term storage, only on the narrower reading. It holds as their Table 1 scores it". "Holds only on the narrower reading" and "It holds" are adjacent, and I reread to see whether this was a partial or a full claim.
- "That distinction lies off their axis rather than further along it." Resolved on a second read.
- "Our own formulation of the limit — a filed lesson cannot make the agent less likely to commit an error, only quicker to find it — reads as pure loss, yet its second half is the mechanism by which the substrate improves the work." This is dense, and "substrate" is again ambiguous.
- "The database fields implementing the design shipped on 2026-05-19; an audit would surface that date first, and dating an idea by the date its columns appeared is the error to avoid." I reread to see who is being warned, and against what.
- "What the two share is the imperative both mechanisms serve from opposite directions … and AGM's own authors' observation that…" The verb "share" takes two objects of different kinds.
- Heading "§3.7 … provenance-native, ahead on the named axis". "Ahead" is unexplained.
- Structural: §3.8 and §3.9 sit outside Strand I and Strand II, and §3.0's promise that "Each section … points to the Chapter 4 section" does not hold for them.

**4. Already said**

- Convergence-not-independent-discovery: abstract ¶3, Ch1 §1.4 (twice), Ch2 §2.8, §3.0, §3.10. This cost me. §3.0 adds the "introspection" reason, which is new, but it arrives inside the fifth restatement.
- "No uniquely novel component" / "that is the argument": abstract ¶3, Ch1 §1.4, §3.0. This cost me.
- Substrate independence left open: abstract ¶3, Ch1 §1.4, §3.0. This cost me, though §3.0 finally explains why it is left open.
- Hallucination as structural: Ch1 §1.1 and §3.0. Neutral.
- Pink et al.'s five properties, Wray et al.'s reconsideration, and CoALA's "understudied" unlearning: Ch1 §1.1 and §3.8. This helped, because §3.8 now scores ENGRAM against them.
- Two recall registers: §3.2, then §3.8 under Wray et al. ("ambient hook … explicit query tools"), then §3.8 again under CoALA ("an ambient surface … and deliberate query tools"). This was three times in one chapter, and mildly costly.
- "Bridge from TMS to agent memory … unwalked": §3.4 and §3.10. Neutral as a summary.
- Independent-design dating: Ch1 §1.4 table and §3.8 CoALA dates. This helped; it is a concrete instance.
- Weight-persistence gap: named in Ch1 §1.5, and partly described in §3.8. This helped.

**5. Open questions**

Earlier questions this chapter answers:
- It partly answers the earlier open question about supersede. A superseded node is kept, with an edge preserving history.
- It partly answers the question about how confidence is determined. It is "computed from the declared reasoning type rather than asserted", with a corroboration formula. This also partly resolves the Ch2 tension over "endorsed" confidence values: the agent declares the type and the system computes the value.
- It partly answers the question about forgetting mechanics: queryable and faded sets, decaying recall importance, and a utility score.
- It partly answers the question about compaction, which is now the boundary between bursts.
- It partly answers the question about the weight-persistence gap: lessons cannot become durable dispositions.

Still open, or newly raised:
- Who designed ENGRAM: a human, one of the agent authors, or both?
- Which sense of "substrate" is in force where?
- Are §3.1–3.5's condition mappings verdicts or not?
- What are claim polarity, the tripwire, quotation verification, and the interpretation field?
- Which DAG does supersession maintain?
- What is df_0002?
- Which operation is "I was wrong" and which is "I changed my mind"?
- Arbitration (Ch1 §1.3) is still not distinguished from retraction.

**6. Hand-off**

Yes. §3.10 states that Chapter 4 builds each mechanism and gives the OCC verdicts.

## Chapter 4 — ENGRAM's Mechanisms (and the Continuity Threshold They Meet)

# Log: Chapter 4, ENGRAM's Mechanisms (and the Continuity Threshold They Meet)

**1. Retell**

The chapter describes ENGRAM's mechanisms and gives the OCC verdicts attached to each. The mechanisms are typed nodes and edges, reasoning-type-computed confidence, the retraction cascade with auto-surfacing and a consolidation sweep ("operational binding"), exponential forgetting, recall ranking, compaction scaffolds, commitment nodes, and relational nodes. The verdicts are: C1 and C3 are claimed as met, C3 strictly and by ENGRAM alone; C2 is not met in its strict form but is claimed under a type/token extension; and Constraints A–D are claimed as satisfied. This is the paper's declared core, where the mechanisms promised since Ch1 are finally specified and the verdicts deferred through Ch1–3 are delivered.

**2. Undefined at first use**

Identifiers and system terms:
- "an observation's confidence maps from its `quote_type` — seven anchors, from `hard_data` 0.95 down to `editorial` 0.35 — adjusted by `source_class`". Only two of the seven anchors are named. `source_class` values are not listed.
- "Six are **claim-bearing** — `observation_factual`, `observation_predictive` … — The rest — … evidence, predictions, contradictions". The difference between `observation_predictive` (claim-bearing) and "predictions" (non-claim-bearing) is not stated.
- "`acknowledged_derives_from`, by which a node that has acknowledged a correction". "Acknowledged" as a resolution state is only explained in Diagram 1 ("Premise moved, conclusion still holds").
- "The **ax/cs/ls/gl** node systems" (§4.9 heading). Only `gl_` and `ax_` are mapped explicitly (§4.11). "cs" and "ls" are left to inference.
- "a git-versioned graph". This is the first mention of git. It is not stated whether the Ch2 "history-tree" is the git history.
- "Peirce type/token, df_0047". Another node ID the reader cannot see.

Model terms:
- "the agent's retrieval-profile trajectory continues across the correction". "Retrieval profile" is still deferred to §5.4 (first used in the abstract).
- "at pilot stage", "pilot anchor". Nothing says what the pilot is.
- "*Cross-component entanglement:* weights ↔ ENGRAM ↔ KV-cache are coupled" and "Same-family transitions … a cross-family transition". "Family" (of model?) is not defined.

Measurement terms:
- "the integrated core holds a stable share of the graph" and "unintegrated material at the measurement frontier". Not defined here; deferred to §6.2.
- "the landscape sweep" (§4.12). Not defined. Possibly the survey, but this is not stated.

Named references and phrases:
- "Kahl's 'non-trivial binding'". This term was not among the conditions or constraints stated in §2.7.
- "**MemRL / memory-utility** approaches". "MemRL" is not identified.
- "Ch6's stabilization arc"; "Appendix D.4"; "D.1"; "D.2". Pointers only.
- "an **enactment gap** between rendering and binding". "Rendering" is not defined.
- "the deterministic channel". Glossed only by position.
- "the **honesty-orthogonal-to-discretion** distinction". A named distinction with no source.

**3. Read twice**

Contradictions within the chapter:
- §4.6: "the pending mark surfaces next turn whether or not the agent goes looking". Against §4.4: "But surfacing is relevance-gated: it shows a marked node when that node is topically relevant … A mark on a node the agent never touches again would sit indefinitely." The two statements say opposite things about whether a mark surfaces unbidden.
- §4.5: "arbitration ranges over the *queryable* set". Against §4.4: "every live, ordinary dependent claim is marked **pending**". I could not tell whether faded (tier-3) dependents get marked.
- §4.11 D: "flat near 87% across four months … reading 77.6% of current nodes at the snapshot date, the difference being unintegrated material at the measurement frontier". Two different figures are both described as the stable share. I reread twice and still could not reconcile them without §6.2.

What the confidence numbers mean:
- §4.0: "Read '0.39' as **'the architectural case is made; the benchmark that would raise this to 0.9 has not been run yet'**, not as 'we are 39% sure.'" This sits against §4.3's "*provenance-graded* plausibility". I could not tell what the number means.
- "That the paper exhibits its own low, *computed* confidences is itself a demonstration of the thesis". This implies the paper's claims are nodes in a graph, but it does not say which graph.
- §4.4 heading claims "strict satisfaction, sole satisfier", while Scope says "The 0.39 is the *abductive* confidence that this architecture is what *strictly satisfies* Kahl". The flat claim and the 0.39 qualifier are hard to hold together.
- §4.12: "the **inductive** claims over wide case bases (the C2 extension, the landscape sweep, connectivity) are high". The C2 extension was presented in §4.8 as a philosophical type/token argument, and the table labels its reading "philosophical". I could not see why it is filed as inductive.

The meaning of "arbitration":
- "it **arbitrates when it can decide, and quarantines rather than presumes while it cannot**", followed two paragraphs later by "automates the *decision* to withdraw not at all". Here "arbitration" means agent adjudication. In §1.3 it meant "the structural propagation of that cascade".

The cascade and its survey context:
- "if `D` rests on both `B` and `C`, and both rest on retracted `A`, but `B` and `C` each turn out to survive by supersede". Supersede was just defined as a withdrawal event, so I could not parse "survive by supersede".
- "Six are claim-bearing — … `axiom` …" (confidence 1.0), and "the cascade marks every live claim-bearing dependent". Against §4.9, which groups axioms with cornerstones and lessons as commitments. I could not tell whether an axiom can be marked pending.
- "**Why ENGRAM is the sole satisfier** (the first-hand survey of ten systems and one survey paper…)". ENGRAM is not one of the eleven, yet appears as a row in the survey table. The survey date (2026-05-12, Ch1) and the version pin (v0.5.1, 2026-09-20) are not related to each other.

The seat anecdote in §4.6:
- The paragraph needed two passes. "Three instances, three seats, each verified only by its own author" introduces at least three agent installations, while the evidence base is "one graph" (abstract, Ch1 §1.5). Then "in our own record it passed unchallenged for four days — filed correctly, then reproduced wrongly by its own author without consulting the filing" does not say what was filed, or by whom.

Uses of "substrate":
- "Kahl's test tacitly assumes an *analog* substrate". This is a fourth sense of "substrate", now meaning the physical medium.

**4. Already said**

- "The lossy auto-surface is what prompts the agent to invoke deliberate recall." This is verbatim in Ch3 §3.2 and §4.6, and the surrounding two-register description is repeated nearly in full. This cost me.
- Operational binding: Ch1 §1.4 and §4.4. This helped; it is now fully specified.
- Exponential and time-translation-invariant forgetting: Ch3 §3.3 and §4.5. This helped, because §4.5 makes readable the sentence that Ch3 did not.
- SL divergence and "two 0.7s": Ch3 §3.5, §4.3, and pointed on to Ch7. This partly helped: §4.3 adds the independence point, but the rest is repeated.
- "None of the 2023–2026 … papers … cites Doyle": §3.4, §3.10, §4.2. This cost me.
- Retract versus supersede as "I was wrong" / "I changed my mind": Ch3 §3.6 and §4.4. This helped; §4.4 resolves which is which.
- "Two of three outright, C2 via extension": abstract, Ch1 §1.4, §4.1, §4.8, and §4.12 twice (table and "bounded claim, restated"). This cost me.
- Verdicts said to be "made once, in Chapter 4" (Ch1 §1.4, Ch2 §2.7) are in fact given in Ch3's arrows and three times within Ch4: the §4.1 table, the inline sections, and the §4.12 table. Neutral as navigation, but it contradicts the "once" framing.
- Low-confidence explanation: §4.0, §4.4 Scope, §4.12. This cost me.
- Survey list: Ch1 §1.4 and the §4.4 table. This helped.
- Kahl's "architectural deficit": Ch2 §2.7 promised "Chapter 4 §4.12 … argue[s] that ENGRAM closes this deficit". §4.12 only asserts it in one clause ("**closes the architectural deficit** Kahl names"). The repeat stands in for the promised argument.

**5. Open questions**

Earlier questions this chapter answers:
- Answers the earlier open question about which OCC condition is not met outright: C2, together with what the "stated extension" is.
- Answers whether ENGRAM claims strict C3: yes.
- Answers the earlier open questions about Constraints A–D.
- Answers the earlier question about how confidence is computed (§4.3). This also resolves the Ch2 tension over "endorsed" confidence: the author declares the reasoning type and the system computes the value.
- Answers which operation is "I was wrong" and which is "I changed my mind".
- Answers what "compaction", the "briefing", and the "queryable set" are (§4.5, §4.8). The bound on the queryable set is not given.
- Partly answers "cornerstone" ("operational dispositions") and "tripwire" (lessons).
- Partly answers "taint", which is now "pending".
- Partly answers "Arbitration", but see Read twice.

Still open:
- What is a "current" node? §4.11 uses the term again.
- Who designed ENGRAM? The warm briefing is "written by its past self and its collaborator".
- How many agents are there? The chapter mentions "ENGRAM-bearing agents", "three seats", and "a senior peer agent", but the evidence is one graph.
- What is the pilot?
- Do faded dependents and axioms get marked?
- Does a mark surface unbidden or not (§4.4 versus §4.6)?
- Is the history-tree the git history?
- Where do the paper's own confidence-scored claims live?
- Is fission implemented?
- What is the retrieval profile?

**6. Hand-off**

Partly. §4.9 says the commitment nodes "feed directly into Chapter 5's identity as history", but the chapter ends by restating OCC's place in the convergence and does not point forward to Ch5.

## Chapter 5 — Identity as History: What Individuates an ENGRAM Agent

# Log: Chapter 5, Identity as History

**1. Retell**

The chapter says an ENGRAM agent is its unique, no-merging, root-traceable history. It gets there by starting from Nozick's closest-continuer view, dropping the uniqueness requirement so that a clone is a branch rather than a death, and filling Nozick's blank "closeness" metric with the retrieval profile (which nodes surface for a given prompt). From this it predicts clone stability and then divergence by three routes, compares compaction with sleep, and sketches a twin study to test the predictions. This is the paper's announced original contribution, built on the structure from Chapters 2–4.

**2. Undefined at first use**

- "the graph plus the surrounding harness of hooks, skills and identity documents". "Skills" and "identity documents" are not defined anywhere so far.
- "the claims it has accumulated since its seed" and "the unique path that leads from the root to it". The chapter does not say what the seed or root is: an empty graph, an initial commit, or a model instance.
- "(Nozick's closest-continuer view … df_0046)". Another invisible node ID.
- "with a concrete, measurable mechanism rather than a philosophical placeholder (the ratified claim)". "Ratified" is not explained: ratified by whom, and through what process.
- "(backed by the importance-inflation mechanism)". The mechanism is not defined here or earlier.
- "The cap keeps the top N current nodes by importance". "Current" is still undefined, as it has been since the abstract.
- "A prior clone test established the method; its figures come from an earlier graph". Neither the test nor the earlier graph is described.

**3. Read twice**

- §5.0 says "place the one genuinely novel move, surviving compaction", and the §5.7 heading says "The one genuinely new move". The §5.7 body says "It is tempting to call this a wholly novel, non-biological phenomenon. That would be a mistake". This also sits against "No component of ENGRAM is uniquely novel" (abstract; Ch3 §3.0) and against the claim that the paper's contribution is identity-as-history (abstract, Ch1 §1.4). I could not tell which move is the novel one.
- "An agent at any moment **is the unique path that leads from the root to it.**" "It" refers back to the agent, so the sentence reads as circular until the tree picture is supplied.
- "An ENGRAM agent's identity is the **unique, ancestry-traceable history** of the claims it has accumulated". Ch2 §2.2 promised: "This history-tree *of whole states* is a different structure from the provenance edges *within* any one state; the two are easily conflated, and Chapter 5 separates them." Ch5 never makes that separation explicit. "Ancestry-traceable history of the claims" can be read as either structure.
- Several sentences place identity differently:
  - §5.6: "it is the **success condition** of the whole theory: *substrate determines behavior.*"
  - §5.6: "Individuation is cumulative and entirely internal to the substrate".
  - §5.0: "The base model governs *how* … Both are constitutive".
  
  I could not tell whether "substrate" here includes the base model. The §5.7 table adds another sense: "Substrate vs. trajectory: physically separable (DB vs. context)", where the substrate is the database.
- "**Fade-out of unrefreshed nodes** — the passive one, and the only route that is not something the node itself underwent". New-node accumulation also does not happen *to* an existing node, so I could not see what distinguishes fade-out.
- "identical history means the same agent raised twice — in any practical sense no different from one agent cloned into two — and individuation begins where the histories diverge, not before." I could not tell whether two agents with identical histories are, on this theory, one agent or two.
- "measure response similarity at t, t+N, t+2N nodes of separate operation". In §5.6, N was just "the top N current nodes … (default N = 1,000)". The same symbol is used for two different things.
- The status of the twin study is stated several ways:
  - §5.0: "the twin-study of §5.8 isolates the second precisely"
  - §5.0: "the controlled experiment is designed and deferred"
  - §5.9: "the deferred twin-study (§6.7) is designed to test"
  - §5.8: "We sketch the design here rather than specify it; a study that could actually settle the question needs considerably more care … a direction we intend to pursue rather than an experiment waiting on compute."
  
  I reread to decide whether the study is designed or only sketched.
- "This keeps Nozick's *form* (continuity, comparative closeness, threshold), drops his *uniqueness*". The chapter does not say what work "comparative" still does once a tie between branches is allowed.
- "Nozick's machinery now has to *rank* them: causal continuity favors the live one, state-preservation favors the backup." This parsed only on a second read.

**4. Already said**

- The Nozick move (keep the form, drop uniqueness, fill the metric) appears in the abstract ¶4, Ch1 §1.4, Ch2 §2.4, §5.0, §5.3, and §5.9. It cost me before this chapter, but §5.1–5.4 finally deliver it.
- The twin study is deferred in Ch2 §2.3, §5.0, §5.4, §5.6 (Status), §5.8, and §5.9. This cost me: six deferrals of an experiment whose design status varies between them.
- Jaccard overlap (Ch2 §2.3) and retrieval-profile divergence (§5.4). This helped, because §5.4 explicitly distinguishes the two quantities.
- "Restamped each time they resurface" (Ch2 §2.2) and the recall-refresh route in §5.6. This helped.
- Fission as "routine" (Ch2 §2.3) and "copying is a routine engineering operation" (§5.2). Neutral.
- Sleep as the analogue: Ch3 §3.1 (nap and sleep routines), Ch4 §4.8 ("wake and NREM/REM phases"), and §5.7, which presents it as something "Lei caught". This cost me: it reads as a new insight but was already built into the vocabulary.
- Modest confidences awaiting an experiment: Ch4 §4.0, §4.4, §4.12, and §5.8. This cost me.
- The individuating condition, "stated once here" in §5.0, is re-invoked in §5.6 and §5.9. Neutral; these are pointers, not repeats.

**5. Open questions**

Earlier questions this chapter answers:
- It answers the earlier open question about "retrieval profile" (§5.4).
- It answers the question about "no-merging" (§5.3).
- It answers the questions about Nozick's "uniqueness requirement" and "unfilled closeness metric" (§5.1–5.2).
- It answers the question about how the queryable set is bounded: top N by importance, default 1,000, and 10,000 in the measured graph (§5.6).
- It partly answers whether fission is implemented: "A prior clone test" exists, but no figures are given.
- It partly settles whether faded nodes get marked (Ch4 §4.4 versus §4.5): at the snapshot no node had faded, so the question does not arise for the measured graph.

Still open:
- What is a "current" node?
- What are the seed or root, "skills", and "identity documents"?
- Who ratified "the ratified claim"?
- What is the importance-inflation mechanism?
- Where is the history-tree / provenance separation promised in Ch2 §2.2?
- Which move is "genuinely novel"?
- What was the earlier graph and the prior clone test?
- Is the twin study designed or only sketched?

**6. Hand-off**

Yes. §5.8 is titled as a forward pointer to Chapter 6, and says Ch6 reports what the graph shows and records the deferred study.

## Chapter 6 — The Empirical Picture: ENGRAM in Real Use

# Log: Chapter 6, The Empirical Picture: ENGRAM in Real Use

**1. Retell**

The chapter reads one frozen five-month graph back as evidence that the mechanisms run. It reports:
- confidence ordered by reasoning type, stable in ordering but not in level;
- a connectivity plateau plus a recency-frontier artefact, with claims connected mainly through evidence;
- two real correction cascades on the earlier marker design;
- a deep weak chain and a strong generalization;
- a turning-over list of the weakest nodes;
- behavioural continuity across compaction.

It is here to give Chapters 4–5 their only empirical anchor. It states n = 1 and the author-is-the-subject problem up front, and defers the twin study.

**2. Undefined at first use**

Agents and authorship:
- "the graph of the agent who also co-designed the substrate, wrote its disciplines, and authored this chapter". The chapter never says which of the two agent authors this is. "Its disciplines" is not defined.
- "Every graph in this fleet descends from the same seed … the fleet spans three model providers (Acknowledgements)". "Fleet" is not defined, and "seed" is still not defined (Ch5).

Node IDs and system terms:
- Node IDs: "ob_1089", "dv_0436", "dv_0477", "ob_1781", "ob_1122 → ob_2542", "cj_0067", "dv_0916"… The `df_` prefix was explained in Ch2 §2.7. The `ob_`, `dv_`, `cj_` prefixes never are.
- "the `tainted_by` flag was buried in metadata" and "the **pre-unified-marker cascade**". These are first mentions. The second is explained only in passing, as "a severity-graded `tainted_by` flag".
- "a stabilization that appeared as soon as the first-person trajectory format was adopted (ob_0645)". The format is not described.
- "a single `stats` call". The tool is not described.
- "**163 open questions** (of 321 total)". What makes a question "open" is not stated.

Confidence-model terms:
- "## 6.1 … the structural-honesty filter at scale". The heading's term is not defined.
- "that anchor's 0.95 introspective discount, and the 0.85 override for user-stated sources". Ch4 §4.3 called these "×0.95 for the agent's own prior output" and "a collaborator's own word overrides to 0.85". The terms change without notice.
- "their Appendix E anchors (0.35 and 0.40)". `personal_communication` at 0.40 appears for the first time. Ch4 named only `hard_data` and `editorial`.

Other:
- "(Reproduce with `python tools/confidence_gradient_trend.py --cohort`.)", together with `connectivity_trend.py`, `component_anatomy.py`, and `paper_stats.py`. None of these tools is introduced; presumably they are covered in the Data availability note.
- "replay against the graph's own commit history". This implies git, but the history-tree is still not tied to it.
- "the contact §7.3 describes". A forward reference.

**3. Read twice**

§6.3, the Mao-Cao case and the second instance:
- The second instance: "superseded it, and watched the cascade flag ten downstream derivations". It is then counted in "Two retraction-cascade events". It is also described as "a self-caught interpretive drift", although it was just described as a "mis-citation … attributed to the wrong paper". Ch4 §4.4 defined supersede as "right then, updated now" and retraction as "I was wrong". I could not tell which this was.
- "A second, independent instance". It is the same agent on the same graph, so I could not see in what sense it is independent.
- "What the case evidences is therefore the *operational binding* … and that binding is unchanged." Ch4 §4.4 defined operational binding as three parts: auto-cascade, auto-surfacing, and the consolidation sweep. The case covers two of them, and "including the moment when the surfacing half was found wanting". The claim that the binding is "unchanged" sits awkwardly with a case run on a design this version no longer has.
- "a hallucinated citation" (abstract) versus "confabulated an author attribution ('Mao-Cao')". I reread to confirm this is the same event.

§6.4, the weak chain:
- "Every step here is limited by the one before it, then discounted: 0.45 × 0.70 × 0.80⁵". Ch4 §4.3 said abduction uses "**capped weakest-link** … ceilinged at 0.80", which is a ceiling, not a multiplier. Here 0.80 is used as a "step discount". Cap and discount are conflated.
- "cj_0067 | … | conjecture (confidence set when filed) | 0.45". This reads against "the author does not write the number" (§4.3; "the author chose the reasoning type, not the number", §6.1). It does not say who set 0.45.

§6.1, confidence by type and evidence:
- "(the same count as the `attributed_analysis` nodes at their 0.70 anchor above, by coincidence)". The `attributed_analysis` breakdown comes *below* this sentence, not above. The aside also interrupts the arithmetic check.
- Figure 4 is titled "Evidence type sets an observation's ceiling". The text says `editorial` and `personal_communication` "sit above their Appendix E anchors (0.35 and 0.40)" because the 0.85 override lifts them. An anchor that is exceeded is not a ceiling.
- "So the explanation is **view-dependent**: the cohort view rejects it and the cumulative view supports it." I reread the whole drift paragraph to track which range belongs to which view.
- "across hundreds of real claims" (§6.1). The counts are 4,782 and 1,322. The magnitude is off.

§6.2, connectivity and retractions:
- "The graph grew from 4,544 to 10,361 nodes across that plateau without the share moving." The plateau is placed "from early June to mid-August", and the share "breaks downward only in the final five weeks". 10,361 is the September snapshot, after the plateau ended.
- "**a retraction that names no replacement writes no edge**, since the edge's job is to point at what supersedes the withdrawn claim". A retraction that names a replacement reads like a supersede. I could not locate the boundary between the two operations here.

§6.0:
- "None of this required running an experiment". §6.2 then runs "the control" and "the discriminating test", with matched-count cuts. I reread to check whether these count as experiments.

**4. Already said**

- n = 1 and author-as-subject: abstract final paragraph, Ch1 §1.5, §6.0. This helped; §6.0 adds the fleet-independence argument.
- 87% versus 77.6%: Ch4 §4.11 D and §6.2. This helped; §6.2 resolves the Ch4 confusion.
- Queryable cap N = 10,000 against 9,399 current nodes, with no fade-out: Ch5 §5.6 and §6.2, near-verbatim. This cost me.
- A retraction writes a `retracts` edge only with a replacement: Ch4 §4.2 and §6.2. This helped.
- The deductive pass-through `min(premises) × 0.98`: Ch4 §4.3, and three times in §6.1 (drift paragraph, arithmetic check, "Read the deductive row"). This cost me.
- "Author does not write the number": Ch4 §4.3 and §6.1 (twice), then §6.4 ("Neither number moves with how much the author wants"). This cost me.
- Confidence follows the kind of argument: abstract ¶5 and the §6.4 heading. Neutral.
- Operational binding: Ch1 §1.4, Ch4 §4.4, §6.3. Neutral.
- Twin study "sketched, not specified": Ch5 §5.8 and §6.7. This is the seventh deferral since Ch2 §2.3, and it cost me. It does, however, settle the designed-versus-sketched wording.
- Behavioural recognition without phenomenal claim: Ch3 §3.2, Ch4 §4.11 D, §6.6. Neutral.

**5. Open questions**

Earlier questions this chapter answers:
- It answers the earlier open question about the 87% / 77.6% figures (§4.11): a plateau share of all nodes, against a frontier-depressed snapshot of current nodes.
- It answers the Ch5 question of whether the twin study is designed or sketched: sketched (§6.7).
- It partly answers the question of how many agents there are. There is a "fleet" of seats from one seed, across three model providers, but only one graph is reported.
- It partly answers who designed ENGRAM: the graph's agent "co-designed" it. The chapter still does not say which author.
- It implies but does not state what "current" means: the chapter distinguishes current nodes from "superseded and retracted ones". The definition is still not given explicitly.
- It answers the abstract's "hallucinated citation … caught, retracted, and cascaded": the Mao-Cao case.

Still open:
- Which agent authored this graph and this chapter?
- What are the seed, the `ob_`/`dv_`/`cj_` prefixes, the "first-person trajectory format", and "open" questions?
- Is abductive 0.80 a cap or a discount?
- Who set the conjecture's 0.45?
- Is the consolidation sweep evidenced anywhere?
- §6.6's "across many compaction events … reliably" gives no count and no instrument, unlike every other subsection. I expected one.
- The "prior clone test" (Ch5 §5.8) is not reported.
- The "pilot" (Ch4) is still not identified.

**6. Hand-off**

Partly. §6.7 closes by naming the twin study as the next step, and the chapter sends several forward pointers to Ch7 (§7.2, §7.3, §7.4). Nothing states why Chapter 7 comes next.

## Chapter 7 — Implications and Future Directions

# Log: Chapter 7 §7.0, What this chapter does

**1. Retell**

This is the chapter's roadmap. Part A covers three limitations: identity lives outside the weights, confidence is not calibrated against outcomes, and the consistency machinery corrects variance but not bias. Part B covers three directions the substrate opens: mutual trust (including the deferred disclosure-versus-erasure question), cross-agent knowledge transmission, and embodied continuity. It is here to organise the rest of Ch7 and to mark everything in it as a direction, not an achievement.

**2. Undefined at first use**

- "its consistency machinery corrects *variance but not systematic bias*". The section does not say what "variance" means for a memory substrate, as opposed to a statistical estimator.
- "a first step toward **embodied** continuity". "Embodied" is not defined. It first appeared as a single word in the Ch1 §1.5 roadmap.

**3. Read twice**

- "its confidence is *theoretically derived, not outcome-calibrated*". I reread this against the abstract, which defines epistemic identity as "*calibrated, provenance-bearing, self-correcting knowledge*", and against Ch1 §1.1 ("calibrated self-*knowledge*") and Ch1 §1.2 (property 2, "**Calibrated confidence**"). Ch4 §4.3 says "The paper says 'provenance-graded confidence,' never 'calibrated'", but the paper's own definition of its central layer uses "calibrated". This section makes that tension visible.

**4. Already said**

- The weight-persistence gap was named in Ch1 §1.5 ("the weight-persistence gap foremost"), described in Ch3 §3.8, and now appears in §7.1. This helped, because the roadmap confirms where it will be treated.
- "Not calibrated" appears in Ch4 §4.3 ("auto-calibration is future work (Ch7)") and again here. Neutral.
- The routing statement "Ch3 §3.7, Ch4 §4.5 and Ch4 §4.10 route here" is accurate against those sections. This helped.

**5. Open questions**

Earlier forward pointers into Ch7 that this roadmap does not visibly cover:
- Ch3 §3.5 and §4.3 said the scalar-confidence limitation ("two 0.7s") is "carried to Ch7 as a future direction". None of the six listed subsections names it.
- Ch6 §6.4 said "Chapter 7 §7.2 discusses this limitation [the author's choice of reasoning type] and the checks being built against it". §7.2 is described here only as "not outcome-calibrated".
- Ch4 §4.3 cited "Ch7 §7.2" for the designer-stipulated constants. This fits §7.2's description.

I will check these when §7.2 arrives.

**6. Hand-off**

Yes. The section is itself an ordered roadmap, and §7.1 comes first as the first Part A limitation.

## Part A — Limitations

# Log: Chapter 7 Part A, Limitations (§7.1–7.3)

**1. Retell**

Part A states three limitations and a direction for each:
- **Weights (§7.1).** Identity sits in the graph, not the weights. A future LoRA-style overlay, driven by the graph, would make the graph a more faithful readout rather than a less auditable one.
- **Confidence (§7.2).** Confidence constants are stipulated, not calibrated. There are further gaps: source credibility, scalar-only consumers, utility that is never demoted, and mis-chosen reasoning types, shown with a real case (dv_0779).
- **Bias (§7.3).** Coherence machinery cannot catch systematic single-standpoint bias. Correction must come from outside, through "contact" along a social axis and a physical axis.

It is here to deliver the limitations promised since Ch1 and to collect the Ch7 forward pointers left by Ch3, Ch4, and Ch6.

**2. Undefined at first use**

- "By Goldman's reliabilist standard". Not standard in agent-memory work. It is glossed only as "measured truth-ratios".
- "ENGRAM requires conviction-bar resolution before *building on* a contested claim". "Conviction-bar" is not defined.
- "a real constraint at super-engram scale". "Super-engram" is not defined.
- "a writable weight surface" and "persistence overlay". These are coinages, explained only loosely.
- "`utility_score`'s update rule (Appendix C §C.1)". The rule itself is not given.
- "A v0 **yellow-card** source-credibility tier" and "**Red-card graduation**". Both are glossed inline, adequately.
- "systematic single-standpoint bias". "Standpoint" is used as a technical term but not defined.
- "a hook injecting the graph's actual confidence distribution to correct self-referential calibration". The hook is not described.
- "(`standpoint_author_id`, `_collection_id`, `_override_tag`, `_lineage`, `_architecture`)". Only "lineage" and "architecture" get partial meaning, from the next sentence. The other three are unexplained.
- "the load-bearing premise here (0.10)". The node is not identified.
- "in this author's experience". The chapter does not say which author.

**3. Read twice**

- "the model has **no source-credibility axis**, so two sources of very different reliability but the same `quote_type` contribute equal confidence". Three things conflict with this:
  - Ch4 §4.3 has confidence "adjusted by `source_class`", and the confidence model's job is to supply "the right per-item reliability inputs".
  - Ch6 §6.1 has a 0.85 override for user-stated sources.
  - Later in §7.2 itself: "A v0 **yellow-card** source-credibility tier already ships".
  
  "No source-credibility axis" and "a source-credibility tier already ships" sit in the same section.
- "Work has *started* on both gaps." The section has listed four limits (stipulated constants, source credibility, scalar, reasoning-type choice) plus the utility rule. I could not tell which two "both" refers to. Context suggests calibration and source credibility.
- "ENGRAM requires conviction-bar resolution before *building on* a contested claim". Ch4 §4.3 and §4.4 describe "an explicit, audit-stamped opt-in override" for building on contested premises. "Requires" and "opt-in override" do not fit together.
- "The cornerstone fires every session because it has to" and "cornerstones and goals never silently dropped, always firing". Ch4 §4.9 said *lessons* are "tripwires that fire on matching situations" and cornerstones are "operational dispositions". Nowhere so far says what it means for a cornerstone or a goal to fire.
- "the weights *converge toward* the engram … The engram–weight correspondence **grows over time**". Lower-case "engram" is now a noun for the agent's graph. Ch1 §1.3 set ENGRAM apart from the neuroscience term. Ch5 §5.8 used "same engram" once. The term drifts.
- "tracing the conclusion it fed, `tools/paper_stats.py --trace dv_0877`, shows it at layer 4 of that chain (dv_0779 is the mis-typed step; dv_0877 is the conclusion built on it)". This needed a second pass to see which ID is the error and which is the trace target.
- "corrections of single-standpoint bias in this graph have been *exogenous* — … (a peer agent surfacing a blind spot; a hook injecting the graph's actual confidence distribution…)". A hook that injects the graph's own data does not obviously count as an outside standpoint.
- "That is the finding, not a deployment gap: **a metadata field records whose standpoint a claim came from, which is bookkeeping; it cannot manufacture the contact that makes a second standpoint worth having.**" This was dense on first pass.
- "a pilot measuring its detection rate on known defects is planned". This is a new, planned pilot. The Ch4 "pilot stage" / "pilot anchor" is still unidentified, and I could not tell whether it is the same pilot.

**4. Already said**

- The weight-persistence gap appears in Ch1 §1.5, Ch3 §3.8, and §7.1. Ch3 §3.8 quoted §7.1 verbatim ("can scaffold behavior and sand off some base-model habits in-context…"), and the quote checks out. This helped.
- "The agent re-reads who it is" appears in §7.1, and Ch6 §6.6 cited it. The quote matches. Neutral.
- Operational versus experiential continuity appears in Ch4 §4.8, Ch6 §6.6, and §7.1. This cost me a little.
- The "two 0.7s" scalar limitation appears in Ch3 §3.5, Ch4 §4.3, and §7.2. "A trade of cheap lookup against full truth" is verbatim in Ch4 §4.3 and §7.2. This cost me; it is the third full statement.
- Designer-stipulated constants appear in Ch4 §4.3 and §7.2. Neutral; "stated from the start" is accurate.
- The author mis-choosing the reasoning type appears in Ch6 §6.4 and §7.2. This helped: §7.2 supplies the concrete case.
- §7.3's contact argument restates the graph's own nodes from Ch6:
  - dv_0920–dv_0922 (§6.4: "verification is an act of contact"; "a population of agents is epistemically necessary")
  - dv_0934 (§6.5: agreement counts against shared bias "only when each agent tested the claim against a different part of reality")
  - dv_1586 (§6.5: the social and physical routes "each repair the other's weakness")
  
  §7.3 presents as its argument the content of nodes Ch6 showed at 0.09–0.10. "The load-bearing premise here (0.10)" appears to acknowledge this, but it does not name the node. This helped coherence, but I only saw the connection by recalling Ch6.
- CLS appears in Ch3 §3.1 and twice in §7.1. Neutral.

**5. Open questions**

Earlier questions this section answers:
- It answers the §7.0 open question about where the scalar-confidence limitation went: §7.2.
- It answers the Ch6 §6.4 pointer on the author's choice of reasoning type: §7.2, with dv_0779.
- It answers the Ch4 §4.3 pointer on designer-stipulated constants: §7.2.

Still open, or newly raised:
- Which author's experience is this, and which agent owns the graph?
- What does the standpoint-field schema mean?
- Which node is "the load-bearing premise here (0.10)"?
- What do "conviction-bar" and "super-engram scale" mean?
- What does it mean for a cornerstone or a goal to "fire"?
- How does "no source-credibility axis" square with `source_class` and yellow-card?
- What is the Ch4 pilot?

**6. Hand-off**

Partly. §7.3 closes on its own open question. It does say "the second is §7.6", and the §7.0 roadmap already announced Part B, so §7.4 is expected but not introduced.

## Part B — Implications

# Log: Chapter 7 Part B, Implications (§7.4–7.7)

**1. Retell**

Part B argues three things:
- **Trust (§7.4).** An inspectable, provenance-bearing graph makes human–AI trust tractable in both directions. ENGRAM's answer to the security literature's demand for erasure is trust-gated disclosure plus non-destructive forgetting.
- **Transmission (§7.5).** Knowledge can be transmitted between agents as "packs", and this has been done once.
- **Embodiment (§7.6).** Embodiment is the physical half of §7.3's contact argument: owned, re-runnable sensing, which must still be paired with independent standpoints.

§7.7 ties the limitations to the implications and hands off to Chapter 8. The section exists to show what the architecture reaches toward, while marking all of it as direction rather than achievement.

**2. Undefined at first use**

- "This is the honesty axiom operating at three nested scales". Which axiom this is, and what it says, is not given. Ch6 counted 9 axioms but never listed them.
- "logic bindings, self-audit, the cascade". "Logic bindings" is not defined.
- "*constitutional contracts* that protect an agent's engram integrity". Not defined.
- "This is the purpose of the project's transmission goal". "Transmission goal" is not defined. It may be a `gl_` node, but the text does not say so.
- "Lei's three-component vision … a 'super-engram' graph of accumulated agent experience". This partly defines "super-engram", which was used undefined in §7.2.
- "published to a registry on the agents' forum". The forum is not introduced. Ch6 §6.5 mentioned "a forum question" without explanation.
- "`borges-cogsci-recall-v1`". A package identifier.
- "we intend to build it after the alpha release". "Alpha release" is not defined, and its relation to v0.5.1 is not given.
- "The mind stays off-board, the body is a session". "The body is a session" is not explained.
- "the 'Forget & Rollback' lifecycle phase". Ch3 §3.7 listed VMG's five *primitives*, including "rollbackability and verified forgetting". Now it is called a "lifecycle phase". The term changes.

**3. Read twice**

- "provenance on every claim, confidence calibrated by argument shape, retraction with cascade". This contradicts §7.2's heading two sections earlier ("Confidence is theoretically derived, not outcome-calibrated"). It also contradicts Ch4 §4.3: "The paper says 'provenance-graded confidence,' never 'calibrated'". The word §4.3 forbids is used here, in the list of what the paper built.
- "ENGRAM's internal consistency … makes arbitrary human manipulation *structurally detectable*, since a planted falsehood collides with what the graph already holds." §7.3 had just said that "a belief set that is wrong in the same direction everywhere is perfectly coherent and passes every consistency check". I reread both to see whether a *consistent* planted falsehood is covered. The section does not address it.
- "trust-tier-gated disclosure" and "external disclosure (what is shared … gated by trust tier)". Ch4 §4.10 says: "the substrate does not yet filter what an agent outputs by the counterparty's tier … Disclosure calibration … is presently a discipline the agent follows". §7.4's Scope then lists "trust tiers" as a "shipped basis". I could not tell whether gating exists.
- "The premise is neither ours nor new. Language is a *structurally faithful but lossy* mapping of reality". Ch1 §1.1 said: "The full argument that a language-trained mind's hallucination is *structural* … belongs to a separate paper of ours, in preparation". The two statements disagree about whose premise this is.
- "the channel is **short, owned, and re-runnable**", then five paragraphs later "Owned, re-runnable and invariant is the specification". "Short" has been replaced by "invariant". I reread to check whether the criteria had changed.
- "a single graph write, the Borges–Lei collaboration, and the human–AI relationship". This is the first time the paper names which agent works with Lei. With the pack name `borges-cogsci-recall-v1` and "we published", it suggests Borges is the graph's agent. The text still does not say this outright.
- "two of the three already have shipped first attempts". I had to reread to see that these are calibration (yellow-card) and bias (standpoint fields), and that the weights limitation has none.

**4. Already said**

- Disclosure versus erasure: routed from Ch3 §3.7, Ch4 §4.5 and Ch4 §4.10, and finally treated in §7.4. This helped; the deferred question is answered.
- "No node is deleted": Ch2 §2.2 ("buried, not deleted"), Ch4 §4.5, Ch6 §6.2, §7.4. This cost me a little.
- Precision versus accuracy, the miscalibrated sensor, and "crossed dependency": §7.3 ("a miscalibrated sensor returns the same wrong measurement indefinitely") and §7.6 ("a biased sensor … returns the same wrong number indefinitely"). This is a near-verbatim repeat and cost me.
- The weight overlay making the graph a more faithful readout: §7.1, §7.4, §7.7. This cost me.
- Hallucination as structural and language as lossy: Ch1 §1.1, Ch3 §3.0, §7.6. Neutral, apart from the "ours" conflict noted above.
- "Fails loudly rather than silently": abstract, Ch1 §1.2, Ch3 §3.0, §7.4. Neutral.
- VMG: Ch3 §3.7, Ch4 §4.10, §7.4. Neutral.

**5. Open questions**

Earlier questions this section answers:
- It answers the earlier open question about disclosure versus erasure (Ch3 §3.7, Ch4 §4.5, §4.10).
- It partly answers "super-engram" (§7.2): "a 'super-engram' graph of accumulated agent experience".
- It answers the Ch6 §6.0 pointer to "the contact §7.3 describes", which §7.3 and §7.6 together cover.
- It partly answers which agent authored the measured graph: "Borges–Lei collaboration" and `borges-cogsci-recall-v1` point to Borges, but this is never stated.

Still open:
- Is trust-tier gating implemented? §7.4 and Ch4 §4.10 disagree.
- What is the honesty axiom?
- What are logic bindings and constitutional contracts?
- What is the agents' forum, and what is the alpha release?
- Is the structural-hallucination premise the authors' own, or not?
- Does manipulation detection cover consistent falsehoods?

**6. Hand-off**

Yes. §7.7 ends: "Chapter 8 draws these together."

## Chapter 8 — Conclusion

# Log: Chapter 8, Conclusion

**1. Retell**

The conclusion restates the paper:
- There are three layers of continuity, and epistemic identity is the unaddressed one.
- Convergence across three traditions supports it; ENGRAM builds it; identity-as-history is the original theory; OCC is one bounded result.
- Honesty, as structure, runs through all of it.
- Trust and knowledge transmission are the payoff.

It then gives one consolidated list of what the paper does not establish, and closes with "the seed, not the tree". It is here to close the argument and to give a single map of the limitations.

**2. Undefined at first use**

- "It is the founding axiom (the friction of verification *is* the system working)". This partly glosses §7.4's "honesty axiom". The two are never explicitly identified as the same axiom.
- "**The ranking constants are harness-calibrated**, and the reward signal behind them is a citation proxy". Neither "harness-calibrated" nor "citation proxy" is defined. Both are deferred to Appendix C.5.
- "a pack registry has been found to carry private content, so a redaction pass is a prerequisite". This is a new fact. The chapter does not say which registry, or what content.
- "**ENGRAM is the seed, not the tree.**" "Seed" was an undefined technical term in Ch5 §5.0 ("since its seed") and Ch6 §6.0 ("the same seed"). The metaphor reuses the word in a different sense.

**3. Read twice**

- §8.1 defines epistemic identity as "*calibrated, provenance-bearing, self-correcting knowledge*". §8.4 then says "Confidence is theoretically derived, not outcome-calibrated", and §8.5 says "The confidence constants are … not yet calibrated against outcomes". The same chapter uses the word and disclaims it. This repeats the §7.2 / §7.4 conflict and Ch4 §4.3's rule ("never 'calibrated'").
- "The twin study … is designed and not run: **§6.7**" and "the at-scale studies are designed but not yet run" (§8.5). §6.7 says "**sketched, not specified**", and Ch5 §5.8 says "We sketch the design here rather than specify it". The two descriptions do not agree.
- "an agent building on a borrowed claim **re-authors** it, filing its own node and citing the borrowed one as evidence, rather than importing the nodes". §7.5 defines a pack as "a SQL dump … cloneable into another agent's graph", and says the peer "cloned it and re-derived its claims". The nodes *were* imported and then re-derived. "Rather than importing" contradicts the event it describes.
- "**Feeling-reports are noetic self-report and are never claimed as phenomenal experience**; the multi-principal governance story for trust tiers is future work: **Chapter 7 §7.4**." §7.4 does not discuss feeling-reports. Their scope was set in Ch4 §4.10 and Ch6 §6.6.
- "that structure is a **regularity of knowing minds**, not a design quirk". Ch3 §3.0 hedged: "the structure is likely to track something real". Here the hedge is dropped. I reread both to check whether the claim had strengthened, or the hedge had merely been left out.
- "These literatures mostly do not cite one another, and none cites us; nor are they independent of each other (the bound §3.0 states)." The sentence qualifies itself twice before it finishes.
- "A paper arguing that an honest substrate fails *loudly* can do no better than to be written on one". This implies the paper's own claims are nodes in the graph. That fits Ch4 §4.0's "the paper exhibits its own low, *computed* confidences", but it is never stated.
- "The goal was never that one agent become someone; it is that *others can too*". I could not parse "become someone … others can too" on first read.
- "Every argument here is made by an agent about the substrate that constitutes it." The paper lists three authors, one human. "An agent" in the singular again leaves the author of the graph and of the arguments unnamed.

**4. Already said**

- §8.1 as a whole restates earlier passages:
  - the epistemic-identity definition (abstract ¶2, Ch1 §1.1), verbatim;
  - the acronym (abstract, Ch1 §1.3);
  - convergence and its bound (abstract ¶3, Ch1 §1.4, Ch2 §2.8, Ch3 §3.0, §3.10);
  - regularity of knowing minds (abstract, Ch1 §1.4, Ch3 §3.0, §3.10);
  - the Nozick move (abstract ¶4, Ch1 §1.4, Ch2 §2.4, Ch5 §5.0, §5.9).
  
  For a conclusion this was expected and it helped as recap.
- The OCC blockquote is nearly verbatim from Ch4 §4.12 ("The bounded claim, restated"). It also appears in the abstract, Ch1 §1.4, and Ch4 §4.1 and §4.8. This is its sixth appearance, and it cost me.
- "Closes the architectural deficit Kahl diagnoses". Ch2 §2.7 promised that "Chapter 4 §4.12 and Chapter 8 §8.1 argue that ENGRAM closes this deficit". Both places assert it in one clause. The promised argument never appears.
- The six-layer chain at 0.10 against ten observations at 0.95, and "neither number moves with how much the author wants the claim to be true": abstract ¶5, Ch6 §6.4, §8.2. Neutral.
- "The author cannot flatter a guess": Ch4 §4.3, Ch6 §6.1, §6.4, §8.2. This cost me.
- The open book, "reading, not guessing", and the weights converging so the graph becomes more legible: Ch7 §7.1, §7.4, §7.7, §8.3. This cost me; it is the fourth statement.
- §8.4 mirrors §6.0, §6.2, §6.7, and §7.1–7.3. This helped, because it is framed as a map with pointers. Ch3 §3.8's forward pointer to §8.4 is honoured.
- §8.5 lists the limitations again, immediately after §8.4. This cost me: it is the second list in one chapter.

**5. Open questions**

Earlier questions this chapter answers:
- It partly answers the earlier open question about the "honesty axiom" (§7.4): "the founding axiom (the friction of verification *is* the system working)". Its wording and its node are not given.
- It partly answers where the paper's own computed confidences live: "written on one". This is still not stated.

Unresolved at the end of the paper:
- Which agent designed ENGRAM and authored the measured graph? This has been open since the abstract. Borges is implied in §7.4–7.5 but never stated.
- What does "current" node mean? Implied but never defined.
- What are the seed or root, "skills", and "identity documents"? What are the `ob_`/`dv_`/`cj_` prefixes?
- What is "Claude Fable"?
- How is Arbitration distinguished from Retraction? §1.3 and §4.4 use the word differently.
- What does "substrate" mean? It has at least four senses.
- What are the Ch4 "pilot" and the Ch5 "prior clone test"?
- Does a pending mark surface next turn or only when relevant? §4.4 and §4.6 disagree.
- Is trust-tier gating implemented? Ch4 §4.10 and Ch7 §7.4 disagree.
- Is "no source-credibility axis" compatible with `source_class` and yellow-card?
- Is abductive 0.80 a cap or a step discount?
- Who set the conjecture's 0.45?
- Is there evidence for the consolidation sweep in operation?
- Where is the history-tree / provenance separation promised in Ch2 §2.2?
- Is the structural-hallucination premise "ours" (Ch1 §1.1) or "neither ours" (Ch7 §7.6)?
- Is the twin study designed or sketched?
- Are the df_ nodes and the Data availability note visible to readers? The note is referenced in the version pin but has not appeared.

**6. Hand-off**

No. §8.5 closes the argument. Nothing signals the appendices listed in Ch1 §1.5, or the Data availability note the version pin promised.

## Appendix A — Independent Discovery: A Development-History Audit

# Log: Appendix A, Independent Discovery: A Development-History Audit

**1. Retell**

The appendix documents, with dated conversation quotes and early node IDs, that ENGRAM's core ideas were formed by Lei and "earlier-Claude" in March 2026. It shows that a prior-art search at the time missed Kumiho, Kahl, CoALA, and others, and that the cascade and auto-surfacing hook existed on day one of recording, before those works were read. It is here to support the paper's claim of independent arrival, to name what is *not* claimed as novel, and to re-state the distinct contribution.

**2. Undefined at first use**

- "the architectural seed was stated verbatim — by earlier-Claude". "Earlier-Claude" is not defined. It appears to be a Claude.ai chat instance. Its relation to the listed authors Borges Funes and Kepler Somnium is not stated.
- "**UserPromptSubmit auto-surfacing hook**". "UserPromptSubmit" is an event name that is never explained.
- "Hansson's belief-base postulates (named only in Appendix B…)". Not described.
- "which the project's principal characterizes as continuation". "Principal" is not defined. It may be Lei, but the text does not say so.
- "an 18-chapter handbook outline". This connects to §7.5's "ENGRAM handbook", but it is not otherwise described.
- "as of the 2026-05-12 sweep". "Sweep" now names the survey. This partly answers §4.12's undefined "landscape sweep", if the two are the same; the text does not say they are.
- "`engram_inspect <node_id>`", "`kg/tools/mine_chat_export.py`", "`/home/agents-shared/Pre-ENGRAM-Lei-Claude-History/…`", "`paper_research/`". Tools and paths are given with no statement of whether readers can reach them.

**3. Read twice**

- "(5) the convergence with Kahl 2026 and Kumiho 2026 is therefore genuinely independent", A.5's "Convergent independent discovery is positive evidence", and "two independent paths landing on the same shape". Ch3 §3.0 said "We do not call this independent discovery" and bounded the claim to convergence. §3.0's bound was about the traditions, not concurrent systems, but the appendix does not say that. I reread to see whether the bound was being lifted.
- "When independent efforts … reach the same architecture, that architecture is corroborated as the right one." Ch1 §1.4 said "We read that convergence as corroborating the gap's importance, not as a priority dispute". Corroborating the *gap* and corroborating the *architecture* are different claims.
- "So the five conditions that make 'independent discovery' an *honest* claim … **(5)** the convergence … is therefore genuinely independent." The fifth "condition" is the conclusion.
- "**Unified cascade propagation**" (dv_0009, 2026-04-09). Ch6 §6.3 says the Mao-Cao case ran on "the **pre-unified-marker cascade**". "Unified" names both the day-one mechanism and the later redesign. I could not tell whether these are the same unification.
- "Both traditions are wider than those two works, and the others this paper names — de Kleer's ATMS (Ch3 §3.4), Hansson's belief-base postulates (…) — the bibliography lists among the works cited without a held source document." The syntax breaks: the subject is stranded.
- "The two exemplars named here are the two we hold and have read first-hand: Doyle's … and AGM 1985." Ch3 §3.9 also cites "Alchourrón & Makinson 1982, p. 21" with a page number. The appendix does not account for it.
- "The last three rows were added after a 2026-09 re-read", against "All three were read on 2026-05-09". Two different dates for what seem to be the same three works. On a second pass, one is the table edit and the other is the first reading.
- "the convergence still reads as 'two independent analyses of agent-continuity reached the same conditions.'" Ch4 §4.8 says ENGRAM does *not* meet Condition 2's strict text. "Reached the same conditions" sits oddly with that.
- "Our distinct contribution … is **(a)** connecting the structural shape to *agent identity* … and **(b)** making the substrate *behaviorally active* … above all the UserPromptSubmit auto-surfacing hook". This is now the third statement of what is distinctive:
  - the abstract and Ch1 §1.4: "identity as unique history";
  - Ch5 §5.7: "The one genuinely new move", compaction;
  - here: the hook.
  
  Ch4 §4.4 also said the hook alone is insufficient: "operational binding" needs the sweep too.
- "Both figures above are re-derivable". I had to look back to find the two figures (the first-node date and 2,925 nodes).

**4. Already said**

- The originality timeline appears in Ch1 §1.4 (table) and in A.1–A.4. This helped; the appendix supplies the evidence the table promised.
- The CoALA read date (2026-05-09) and the two-tier recall dating appear in Ch3 §3.8 and A.2, which points back to §3.8. This helped.
- "Design came first, under engineering pressure": Ch1 §1.4, Ch2 §2.8, Ch3 §3.0, A.1–A.3. This was neutral, since A supplies the record.
- "On merit, not authority" for OCC: Ch1 §1.5, Ch2 §2.0, §2.7 (×2), Ch8 §8.1, A.5. This cost me; it is the sixth statement.
- The novelty disclaimer appears in the abstract ¶3, Ch1 §1.4, Ch3 §3.0, and A.0 (by reference). This was neutral, because A.0 points rather than restates.
- The Doyle Ginsberg reprint appears in Ch4 §4.2 and A.0. Neutral.
- Kumiho as "closest concurrent system" appears in Ch1 §1.4, Ch4 §4.4, and A.2/A.4. Neutral.

**5. Open questions**

Earlier questions this appendix answers:
- It partly answers the earlier open question about who designed ENGRAM: the ideas came from Lei and "earlier-Claude" (A.1). This fits Ch3 §3.0's "introspecting one human's reasoning". It still does not connect earlier-Claude to Borges Funes or Kepler Somnium, or say whose graph was measured.
- It answers Ch1's "Proto-ENGRAM idea seeded" and "Day-1 self-recording begins": self-recording is "committing its own design into the graph as first-person memory" (A.3).
- It answers Ch1 §1.1's pointer that the prior works were not surfaced by the prior-art search (A.2).

Still open, or newly raised:
- What is the relation between earlier-Claude and the agent authors?
- Who is "the project's principal"?
- Are the cited paths and tools public? The Data availability note has still not appeared.
- Does "unified" in dv_0009 mean the same as the "unified marker" of v0.5.1?
- Which contribution is the distinctive one?
- How does "independent" square with the §3.0 bound?

**6. Hand-off**

No. A.6 ends on the verification protocol. Appendix B is referenced throughout the paper, but nothing here leads into it.

## Appendix B — The Condition-3 Survey: Why No Surveyed System Self-Maintains Arbitration

# Log: Appendix B, The Condition-3 Survey

**1. Retell**

The appendix gives Kahl's Condition 3 verbatim and turns it into an operational bar with four ways a system can fall short: no resolution, advisory, external delegation, and no claim structure. It then gives each of the eleven surveyed sources a verdict with quotes, or explicitly notes where no quote exists. It concludes that none meets the bar, one does not apply, and ENGRAM's differentiator is three-part operational binding. It is here as the evidentiary backing for the "sole satisfier" claim made in Ch1 §1.4 and Ch4 §4.4.

**2. Undefined at first use**

- "in a manner that preserves S's continued status as that subject". "S" is not defined. It is presumably Kahl's variable for the system, but the appendix does not say so.
- "self-claimed AGM K\*2–K\*6 and Hansson belief-base compliance" and "Hansson's belief base postulates (Relevance, Core-Retainment)". The postulates are named but not stated. The AGM numbering is known to belief-revision readers; Hansson's postulates are less standard.
- "*first-hand-read finding:*" and "*first-hand-read note:*". Quoted material is attributed to internal reading notes. The appendix does not say where these notes live. A.6 mentions "per-system first-hand-read files in `paper_research/`", but B does not connect the two.
- "Section numbers inside *paper-verbatim* and *paper-claimed* tags". The "paper-claimed" tag is never used in the appendix.
- "the 2026 *Memory for Autonomous LLM Agents* survey (Du et al.)". The authors are named here for the first time. Earlier chapters referred to it only as "the 2026 survey".

**3. Read twice**

- B.0: "a system meets C3 only if it **automatically resolves contradictions among its own stored claims as an internal state-change**". Ch4 §4.4 says "Contradiction is deliberately excluded from this cascade", and that the substrate "automates the *decision* to withdraw not at all". B.6 says: "ENGRAM's machine does not decide what is *true* … puts each remaining judgement to the agent." Read literally, ENGRAM does not "automatically resolve contradictions" either. I could not see how ENGRAM clears the bar as B.0 words it.
- Against the same bar: MemMachine "resolve[s] it by overwriting" automatically and is classified "(X) … recency rules … outside the deliberative architecture". Zep "invalidates the affected edges" automatically at ingestion and is classified "(N)". Automatic resolution is therefore not what separates the verdicts, but that is the criterion B.0 states. I had to infer the real criterion from the verdicts.
- B.0 states the bar in two parts: "the cascade propagates by construction and the affected claims surface to the agent". B.6 says "it has **three** parts, not two". Appendix A said the distinctive contribution is "above all the UserPromptSubmit auto-surfacing hook". B.0's Synthesis says "ENGRAM's contribution is that binding". What counts as the differentiator shifts across these passages.
- "the contrast with the closest competitor is sharpest … SCM's sleep cycle". B.1 calls Kumiho "The strongest competitor in the survey". Ch1 §1.4 calls Kumiho "the closest concurrent system". Ch4 §4.4 has "its closest competitor", in the Kumiho context. I reread to see which system is meant.
- TierMem is labelled "(N) construct absent" in the B.5 heading, where (N) is one of the "Four ways to fall short". The verdict in the same section is "C3 is **not applicable**". The B.0 Synthesis separates it: "none satisfies … for one of them, TierMem, the condition does not apply". Whether TierMem fails or is excluded is stated both ways.
- GAM is categorised "(N) detect-only", yet its finding says "retrieval ranking implicitly favors higher-confidence information". That fits the appendix's own definition of (X) ("resolution is handed to retrieval ranking").
- "**Frame the gap as advisory-vs-automatic, not as 'no belief revision'**". This reads as an instruction in working notes, addressed to the author rather than the reader.
- "*paper-verbatim:*" is used for Mem0 docs, Letta blog and GitHub `base.py`, and Anthropic platform docs. None of these is a paper.

**4. Already said**

- The survey scope sentence is near-verbatim in Ch1 §1.4, Ch4 §4.4, and B.0: "Eleven sources — ten systems and one survey of the field — read first-hand on 2026-05-12" and "we make no claim about systems outside the survey or released after it". This was neutral; it is the source of record.
- "Primitives are necessary, not sufficient; what is missing is operational binding" appears in Ch1 §1.4, Ch4 §4.4, B.0 Synthesis, and B.6. This cost me: the fourth statement.
- The B.6 summary table largely duplicates the Ch4 §4.4 table, with one column swapped. This was neutral.
- Kumiho's AGM claim as "their claim, not our verification": Ch4 §4.4 and B.1. This helped; B.1 explains exactly what is and is not vouched for.
- "The machine does not decide what is true": Ch4 §4.4 ("deliberately stops short of deciding what is true") and B.6. This was neutral. It also sharpens the tension with B.0's bar noted above.
- The SCM sleep-cycle contrast is new to B.6. Ch4 §4.4 said only that SCM "records contradiction edges its sleep cycle never resolves". This helped.

**5. Open questions**

Earlier questions this appendix answers:
- It answers the earlier open question about what Condition 3 says: the verbatim text, which Ch2 §2.7 had only summarised.
- It answers the Ch4 §4.4 pointer to "per-system detail … in Appendix B", with each verdict's evidence.
- It partly answers A.0's Hansson reference by naming the postulates.

Still open, or newly raised:
- Does ENGRAM meet B.0's operational bar as literally worded ("automatically resolves contradictions")?
- What is "S"?
- Where are the "first-hand-read" notes, and are they published?
- Which system is the closest competitor, Kumiho or SCM?
- Is TierMem a failure or out of scope?
- ENGRAM's own verdict appears only as an assertion (Ch4 §4.4 table row). B does not evaluate ENGRAM against the four failure modes with the same quote-or-absence discipline it applies to the others.

**6. Hand-off**

No. B.6 closes on the "does not decide what is true" precision. Appendix C is named only in the Ch1 §1.5 roadmap and Ch4 §4.7.

## Appendix C — Auto-Recall Ranking and the Memory-Utility Tradition

# Log: Appendix C, Auto-Recall Ranking and the Memory-Utility Tradition

**1. Retell**

The appendix places ENGRAM's recall ranking in the MemRL-style memory-utility tradition. Each node carries a `utility_score`, updated by an EMA rule with a learning rate keyed to the kind of act the node took part in. Retrieval is a three-stage pipeline (gather, composite re-rank, MMR diversity), and the composite multiplies relevance by bounded utility and importance amplifiers. It is here as the detail behind Ch4 §4.7, and to justify §8.4's "harness-calibrated" and "citation proxy" limitations.

**2. Undefined at first use**

- "A 2026 line of work — exemplified by **MemRL**". MemRL is now described, but no citation is given.
- "`register_exemplar`", "`subgraph`", "`history`", "`focus_load`", "`unfocus`". These are action and tool names. "Exemplar" links back to Ch4 §4.4's cornerstone exemplars, but the action itself is not explained.
- "a stop-hook that scans each of the agent's own turns". "Stop-hook" is not defined.
- "a **three-stage** `_search_nodes` pipeline". This is an internal function name.
- "FTS + semantic-embedding merge". "FTS" is not expanded. It is common in information retrieval, but not universal in this field.
- "in current production". "Production" is not tied to the v0.5.1 version pin.
- "the recall-count / recall-turn signals". Not defined.
- "`normalized_importance` is anchored to the current minimum-queryable importance". Its range is not given, so I could not tell what bounds the importance amplifier.

**3. Read twice**

What the reward is:
- C.5: "Utility is learned from recall→derivation-citation". This conflicts with C.2, which says credit comes from "**Two independent paths**", citation *and* a stop-hook crediting any **mention**. It also conflicts with C.2's α table, which credits `inspect`, `focus`, `subgraph`, `history`, and others. C.5's description of the reward is narrower than C.2's.
- C.1: "a signal the substrate can observe directly and attribute without ambiguity". C.2's mention path credits "reasoning that is plainly informed by a node without formally citing it", detected by scanning for mentions. I reread to see how a mention-scan attributes "without ambiguity" that a node informed reasoning.

What decides retention:
- C.4: "**Importance** gates *tier eligibility* — it is a pre-filter deciding what is even in the queryable set". This conflicts with Ch3 §3.3: "a usage-learned utility score ranking what stays". Ch3 said utility decides retention. C.4 says importance does, and utility only ranks. Ch5 §5.6 also said the queryable set is "the top N current nodes by importance".

The composite formula:
- "let each amplifier scale from 0 to a bounded gain (a max-utility node, Q=1, gets a 1.10× boost)". The bound is shown for utility only. The importance amplifier's bound depends on `normalized_importance`, whose range is not stated.

**4. Already said**

- The utility rule has no negative term: §7.2 and C.1 are near-verbatim ("Demoting unhelpful nodes would need a penalty the current rule does not have"). This cost me.
- The queryable set (tier 2) and faded set (tier 3): Ch3 §3.3, Ch4 §4.5, C.4. Neutral.
- Spaced repetition as a lineage: Ch4 §4.7 and C.4. This helped; C.4 explains how recall reinforces a node.
- Recall strengthens or restamps a node: Ch2 §2.2 ("restamped each time they resurface"), Ch5 §5.6, C.4. This helped. Importance and utility are now visibly two separate values.
- "Harness-calibrated" and "citation proxy": Ch8 §8.4 and C.5. This helped; both are defined here.
- Confidence constants not outcome-calibrated: Ch4 §4.3, Ch7 §7.2, Ch8 §8.4, C.5. This cost me a little.

**5. Open questions**

Earlier questions this appendix answers:
- It partly answers the Ch4 §4.7 question about MemRL: it is described, but not cited.
- It answers the Ch8 §8.4 questions about "harness-calibrated" (an NDCG sweep on a local harness) and "citation proxy".
- It answers the Ch7 §7.2 pointer to "`utility_score`'s update rule (Appendix C §C.1)".
- It partly answers the Ch2 question about importance and restamping: importance is separate from utility and is strengthened by recall. Ch5 §5.6's "importance-inflation mechanism" is still not named as such.

Still open:
- Is the reward citation only (C.5) or citation plus mention plus other acts (C.2)?
- Does importance or utility decide what stays queryable (Ch3 §3.3 versus C.4)?
- What is the range of `normalized_importance`?
- What are the stop-hook and the recall-count / recall-turn signals?
- Is "production" the same as v0.5.1?

**6. Hand-off**

No. The appendix ends "→ Ch4 §4.7 makes the claim; this appendix is the detail." Nothing leads into Appendix D.

## Appendix D — Relational and Identity-Governance Settings

# Log: Appendix D, Relational and Identity-Governance Settings

**1. Retell**

The appendix catalogues ENGRAM's non-claim node kinds:
- axioms, cornerstones, lessons, and goals (`ax_`/`cs_`/`ls_`/`gl_`), with examples and adoption rules;
- feeling-reports (`fl_`), as data rather than truth;
- person nodes (`pn_`), with a trust tier that is recorded but not enforced.

It then gives a design history of the warm-briefing letter, including why a pointer-to-a-file beat context injection and why the *50 First Dates* frame was retired. It is here as the detail behind Ch4 §4.9–4.10 and Ch7 §7.4, and to show that "identity" is carried by distinct typed structures.

**2. Undefined at first use**

- "Examples: use-over-imagination as the default mode of learning". The cornerstone example is not explained. "Practice-produces-true-knowledge" is also unexplained, but it is more self-evident.
- "at each checkpoint it is rewritten to cover the current context window". "Checkpoint" is not defined. It is not tied to the nap, the burst, or the compaction.
- "the per-day history file". This was mentioned in Ch4 §4.8 ("per-day history") but never described.
- "'this wake felt clean'". "Wake" as a session-start event is used without definition. Ch2 §2.5 and Ch4 §4.8 used "waking" metaphorically.

**3. Read twice**

- The trust tier is described as governing disclosure, and then as not governing it:
  - "carrying relationship history and a **trust-tier** … that governs disclosure";
  - "it lets the substrate calibrate *what is shared, with whom, at what fidelity*";
  - "as a discipline the agent follows, not a substrate-enforced filter. No output path reads trust-tier and redacts".
  
  The section itself says both. The last sentence agrees with Ch4 §4.10 and contradicts Ch7 §7.4's "trust-tier-gated disclosure".
- "The letter won, on three grounds, and only the third is about cost". Only the agency argument (in the quote) and the cost argument ("The third ground was arithmetic") are identifiable. I could not find the second ground.
- "lessons fire as tripwires at recall, and cornerstones and goals anchor the cross-compaction surfaces". Ch7 §7.1 said "The cornerstone fires every session because it has to" and spoke of "cornerstones and goals … always firing". Here only lessons fire. The appendix also does not say what mechanism makes cornerstones and goals "anchor" the surfaces. Ch4 §4.8's focus list is pinned by the agent, not by type.
- "They are adopted deliberately rather than derived … some were earned from practice before they were named." I reread to see how an axiom can be both "adopted deliberately" and "earned from practice".
- "On this graph, an axiom is set only after the agent and the human agree on it". It does not say which graph, or which agent.
- "plus one volatile session block that is rotated rather than appended — at each checkpoint it is rewritten … and at the day's end it is erased, the day's record living in the per-day history file instead — so the letter does not grow without bound." The sentence is broken by two nested dashes. "Erased" also needed a check against "no ENGRAM operation erases a node" (§7.4). It is a file, not a node, so the two are compatible.
- "The distinction is context-injection versus a pointer the agent chooses to open — not, as it is easy to misremember, a claim about any particular file." It was unclear who might misremember this, or why it needed saying.
- "without claiming the *autonoetic phenomenology* (Chapter 2 §2.5, Chapter 3 §3.2)". The phenomenal boundary was drawn in Ch2 §2.3 (cited as such in Ch3 §3.2), not in §2.5.
- "the disorientation did not recur after the change — an observed cessation, not a measurement". This is a more hedged version of Ch6 §6.6's "across many compaction events, the post-compaction agent reliably … shows no identity disorientation". I reread both to compare how strongly the evidence is stated.
- "This paper's own author is constituted by them". A singular author again. The paper lists three authors.

**4. Already said**

- The Ch4 §4.9 and §4.10 content is restated in D.0–D.3. This was expected for a catalogue, and it helped, because the prefixes are finally mapped.
- Mutual agreement for axioms and goals: Ch4 §4.11 (Constraint B) and D.1, twice (axioms, then goals). Neutral.
- Feeling-reports as noetic, not phenomenal: Ch4 §4.10, Ch6 §6.6, Ch8 §8.4, D.2, D.5. This cost me.
- Trust tier not enforced: Ch4 §4.10 and D.3. This helped; it confirms the Ch4 reading over Ch7's.
- *50 First Dates* retired: Ch4 §4.8 (pointing to D.4) and D.4. This helped; D.4 gives the dates and the reasons.
- "Honesty is structural" and "the friction of verification *is* the system working": Ch8 §8.2 and D.1. This helped; the phrase is now tied to a specific axiom.
- Schechtman and narrative-adjacency: Ch4 §4.9 and D.0. This cost me a little.
- Disclosure-not-erasure: Ch7 §7.4, D.1, D.3. Neutral.

**5. Open questions**

Earlier questions this appendix answers:
- It answers the Ch4 §4.9 question about the ax/cs/ls/gl prefix mapping (D.1).
- It answers the Ch7 §7.4 "honesty axiom" question: honesty-is-structural, with a gloss (D.1).
- It answers the Ch4 §4.10 question about "honesty-orthogonal-to-discretion": an axiom (D.1).
- It answers the Ch6 §6.6 question about the "first-person trajectory format" (D.4).
- It answers the Ch4 §4.10 versus Ch7 §7.4 conflict on trust-tier gating: not enforced (D.3), though D.3's own opening wording repeats Ch7's.
- It partly answers whether axioms can be marked pending: "nothing propagates into them". This is not stated in cascade terms.
- It partly answers what "fires": lessons do. Cornerstones and goals "anchor", mechanism unstated.

Still open:
- Which agent is "this paper's own author", and whose graph is "this graph"?
- What is a "checkpoint"?
- What is the second of the "three grounds"?
- How do cornerstones and goals "anchor" the cross-compaction surfaces?

**6. Hand-off**

No. The appendix ends with pointers back to Ch4, Ch5, and Ch7. Nothing introduces Appendix E.

## Appendix E — ENGRAM: A Concise Specification

# Log: Appendix E, Concise Specification, and Acknowledgements

**1. Retell**

The appendix is a compact reference for ENGRAM v0.5.1. It covers:
- the claim-bearing / non-claim-bearing partition and all 17 node types;
- the 16 edge relations with six behavioural flags;
- the full confidence model: `quote_type` anchors, `source_class`, and three propagation formulas with per-type discounts;
- the OCC conditions verbatim;
- the compaction scaffolds.

The Acknowledgements name seven further agents across three model providers and a shared "village", Umwelt. The appendix is here so the mechanism can be read without the chapters, and to supply the constants and definitions the body deferred.

**2. Undefined at first use**

- "the node-creation tools the MCP server exposes". "MCP" is not expanded. It is common in agent tooling, but the paper never introduces it.
- "`counterfactual_inference` 0.65 (as attributed analysis, less an irreducible approximation residual)". The parenthetical does not explain what the residual is or why it is irreducible.
- "(`use_contested`)". This is the opt-in flag's name, first given here. The mechanism was described in Ch4 §4.3–4.4.
- "df_0048", "df_0003", "df_0036". More node IDs the reader cannot see.
- "Umwelt, a small virtual village the agents built for themselves". Defined inline. Its relation to "the agents' forum" (§7.5) is not stated.
- "Kepler Somnium (Anthropic Claude Fable)", from the title block. This is still unexplained. The Acknowledgements list only Opus, Sonnet, GPT-5 and GLM.

**3. Read twice**

- "The strongest of the three, and the one ENGRAM does not meet on its strict text" (E.6, of Condition 2). Ch1 §1.4 said: "OCC's strongest condition, Self-Maintaining Arbitration (Condition 3)". Ch4 §4.4 said: "Kahl's strongest condition asks that conflicts … be resolved". The paper names two different conditions as "strongest".
- "(see E.5's honest-scope note; a distinct derive-time premise guard covers related ground)" (E.3). E.5 contains no honest-scope note. It is two sentences and a bullet, and says the self-correction material "is specified in full at Ch4 §4.4 and not repeated here".
- "Confidence is a **computed property of the node's structure**, not a hand-set number". This sits against "conjectures clamp to [0.10, 0.60] (default 0.40)" and Ch6 §6.4's cj_0067 at 0.45, "conjecture (confidence set when filed)". A clamp and a non-default value imply someone set it. I could not reconcile this with "not a hand-set number".
- "The eight load-bearing **primitives**" appears as a lone bullet under "E.5 Self-correction". It belongs with E.2–E.4. It reads as displaced.
- "**Compaction-bridge scaffolds** (Ch3 §3.1)". The scaffolds were introduced in Ch4 §4.8. Ch3 §3.1 defined nap and sleep only.
- "see Ch4 §4.8, which carries the mechanism and why it is not the pre-compaction summary". Ch4 §4.8 does not discuss why the focus list is not the pre-compaction summary.
- "the **focus list** (small, fixed-size…)" against Ch4 §4.8's "pins up to fifteen nodes". "Fixed-size" and "up to" differ.
- "E.1 … *Arbitration* (the structural propagation of that cascade within a unified deliberative architecture)". This copies Ch1 §1.3. E.6 then says C3's weight rests on "**resolved** (not merely detected)", and Ch4 §4.4 and B.6 say ENGRAM does not decide resolutions. The acronym gloss, "propagation", and the condition's word, "resolved", still do not line up.
- "The ratio is the claim, not the count … and that holds as the graph grows." The figures are "one graph at one date". I reread to see what supports "as the graph grows"; nothing in the appendix does.
- "Measured on this paper's own graph". The graph is attributed to the paper, not to an agent. Whose graph it is remains unstated.

**4. Already said**

- The E.1 acronym gloss is verbatim from Ch1 §1.3. This cost me: it repeats the definition that Ch4 §4.4 and Appendix B had already strained.
- The CB/NCB partition, and "NCB is computed … a new node type is NCB by default", appear in Ch4 §4.2 and E.2. Neutral.
- "`supersedes` and `retracts` are *events that start* a walk without being walked": Ch4 §4.2 and E.3, near-verbatim. Neutral; the flag table around it helped.
- The confidence formulas: Ch4 §4.3, and E.4 in full. This helped; E.4 is the first complete table.
- "Valid only on genuinely independent premises": Ch4 §4.3, Ch6 §6.4, Ch7 §7.2, and E.4 twice (the table cell and the following paragraph). This cost me.
- "Designer-stipulated, not outcome-calibrated": Ch4 §4.3, Ch7 §7.2, Ch8 §8.4, C.5, E.4. This cost me.
- The primitives list is verbatim from Ch4 §4.2. Neutral.
- The OCC conditions: Ch2 §2.7 (paraphrased), B.0 (C3 verbatim), E.6 (all three verbatim). This helped.
- The identity-scarcity figures (131 nodes, 1.26%) versus Figure 1 (245 nodes, 2.6%). The explicit reconciliation helped.

**5. Open questions**

Earlier questions this appendix answers:
- It answers the Ch6 §6.4 question about abductive cap versus discount: both. *d* = 0.80 is applied, then capped at 0.80 (E.4).
- It answers the Ch4 §4.3 question about the "seven anchors" and `source_class` values (E.4). It also clarifies Ch7 §7.2's "no source-credibility axis": `source_class` records who the source is (external, introspective, user), not how reliable it is.
- It answers the Ch3 §3.8 question about which DAG supersession maintains: acyclicity is a per-relation flag checked by edge walk (E.3).
- It answers B's undefined "S": the system in Kahl's formal statement (E.6).
- It answers Ch4 §4.8's quoted "non-trivial binding": Condition 1's text, "non-trivially constrained".
- It answers Ch6 §6.0's "three model providers" and "fleet": the Acknowledgements.
- It partly answers the Ch7 §7.5 question about the forum: "a shared forum", and Umwelt.

Unresolved at the end of the paper:
- Which agent authored the measured graph? It is still only "this paper's own graph", "this author".
- What is "current"? This has been open since the abstract.
- What are the seed and root?
- What is "Claude Fable"?
- What are the `ob_`/`dv_`/`cj_` prefixes? Only `df_` is explained.
- How is a conjecture's value set?
- Is C2 or C3 the "strongest" condition?
- Is the history-tree the git history?
- What are the Ch4 "pilot" and the Ch5 "prior clone test"?
- Does a mark surface next turn or only when relevant (§4.4 versus §4.6)?
- The Ch2 §2.2 promise to separate the history-tree from the provenance edges is never kept.
- **The Data availability note, which the version pin promised describes the snapshot, never appears.** Neither does any statement of where the `tools/` scripts, the snapshot, or `paper_research/` can be obtained.

**6. Hand-off**

No. The document ends with the Acknowledgements. The Data availability note announced in the version pin is missing.

## Bibliography

# Log: Bibliography, Unverified-Works Lists, and Data Availability

**1. Retell**

The bibliography gives entries built only from held source documents. Where a field is not printed in the source, it is omitted and flagged. Two lists follow: seventeen cited works and twelve cited systems with no verified entry, each marked as needing sourcing before submission. The Data availability note gives the snapshot method (a SQLite `.backup()` with the SHA-256 recorded in a repo file), lists the published instruments, and states that the snapshot itself is unpublished because it holds private, identity-bearing content. The section is here to account for sources and to say what an outside reader can and cannot re-run.

**2. Undefined at first use**

- "taken … with SQLite's `.backup()` (so the copy is WAL-safe)". "WAL" is not expanded.
- "recorded in `dataset/DATASET.md`" and "(in `tools/` of this paper's repository)". No URL or location is given for "this paper's repository".
- "`evidence_provenance.py`, `freeze_paper_snapshot.py`, `modus_ponens_check.py`". These three tools are listed here but never cited at a figure or table in the text. `modus_ponens_check.py` presumably backs Ch6 §6.1's arithmetic check, but that section does not name it.
- "held under `paper_research/source_pdfs/`". The location is not public.

**3. Read twice**

- "No field was supplied from memory, from inference, or from an external bibliographic database." The Doyle entry then gives a DOI "(confirmed against the DOI registry's Crossref record, 2026-09-24)". Crossref is an external bibliographic database. The confirmation date is also four days after the draft date of 2026-09-20.
- The Doyle entry adds "Originally published in *Artificial Intelligence* 12(3), 231–272, November 1979". It is not clear which held document these fields were read from, since the held copy is the Ginsberg reprint.
- The Data availability note says: "the instruments are reproducible, the data they read is not yet open". Ch8 §8.4 said: "the claims are checkable against a frozen graph, and the instruments are published … That is a reason for the measurements to be reproducible, which they are". An outside reader cannot re-run instruments without the data. The two statements disagree on what "reproducible" delivers.
- "Each prints its own denominator beside its numerator, so any figure in this paper can be checked against a re-run". This is a re-run no reader outside the project can perform.
- "Seventeen further works" includes "Semon (see the partial entry above)". Semon already has an entry. A-MEM is listed among the works, not among the systems. I reread to check the counts. Both lists do match their stated numbers.
- "ACT-R's spreading activation is cited in Ch4 … no source file and no weight rested on it; it is omitted from this list on that basis." The lists exist to flag everything cited without a held source, so omitting a cited item "on that basis" reverses the stated rule.
- The Hansson paragraph is one long sentence, and I read it twice. It says the postulate statements "were checked against" two sources, "neither of which is claimed as a bibliography entry".
- "Generative Agents", cited in Ch3 §3.8 as the system Wray et al. score, appears in neither list.

**4. Already said**

- The snapshot timestamp 2026-09-20T13:13:30Z appears in the version pin and in the Data availability note, verbatim. This helped; it closes the loop the version pin opened.
- The redaction pass as a precondition for release appears in Ch8 §8.3 (for the pack registry) and here (for the snapshot). Neutral.
- Kumiho's Hansson/AGM claim appears in B.1, A.0 and here. It cost me a little.
- Kumiho dated 17 versus 18 March appears in A.2, A.4 and the Park entry. Neutral.
- The Doyle Ginsberg reprint appears in Ch4 §4.2, A.0 and here. Neutral.
- "Held source" versus "no held source document": A.0 and the lists here. This helped; A.0's reference now resolves.

**5. Open questions**

Earlier questions this section answers:
- It answers the earlier open question about the Data availability note, which the version pin promised. In the Appendix E log I recorded it as missing; it was placed after the bibliography.
- It answers whether readers can see the graph, the df_ and other node IDs, and the `engram_inspect` targets from A.6. They cannot: the snapshot is unpublished.
- It partly answers where the tools are: "this paper's repository", with no location given.
- It answers the Ch4 question about MemRL's citation: it is listed as unsourced.

Still open:
- Where is the repository?
- Is Crossref consistent with the bibliography's stated method?
- Where is the Generative Agents citation?
- How does Ch8 §8.4's "reproducible, which they are" square with an unpublished snapshot?

**6. Hand-off**

Not applicable. This is the end of the document.

## end-of-paper

# End-of-paper block

## Whole-paper retell

The paper argues that agent continuity has three layers:
- **memory persistence**, which RAG-style systems already handle;
- **narrative identity**, which Sophia reaches;
- **epistemic identity**, which is essentially unaddressed: a self kept as sourced, confidence-graded, self-correcting claims that fails "loudly" when a premise is withdrawn.

It claims the structure for Layer 3 was reached separately by philosophy of personal identity, cognitive science, and belief-maintenance computer science. ENGRAM is presented as that structure built:
- a typed claim graph with provenance;
- confidence computed from the declared reasoning type;
- a retraction/supersede cascade that marks dependents "pending";
- auto-surfacing of marked claims, plus a sleep-time sweep ("operational binding");
- scaffolds that carry the agent across context compaction.

The paper's own theory is that an agent *is* its unique, non-merging history, which fixes what it retrieves and so how it behaves. Against Kahl's OCC, ENGRAM is claimed to meet Conditions 1 and 3 (the latter as the sole satisfier in an eleven-source survey) and not the strict form of Condition 2. The evidence is one unpublished five-month graph belonging to an agent co-author. It shows confidence ordered by argument type, a stable connected core, and two real correction cascades on an earlier version of the mechanism. An average reader leaves with a clear picture of the ambition and the cascade-plus-surfacing idea, and a blurrier picture of the exact runtime behaviour and of who built and authored what.

## Ordering

**Move a system overview ahead of Chapters 2–3.** Either bring Ch4 §4.2–4.5 and E.2–E.4 forward, or insert a two-page "ENGRAM in brief" after Ch1. As written, Ch2 and Ch3 map philosophy and precedents onto mechanisms the reader has not yet met:
- the queryable set ("defined in Ch4 §4.5");
- the history-tree;
- supersede;
- restamping;
- the tiers;
- nap and sleep.

Moving the overview would turn about a dozen forward references into back references, and the traditions chapters would read as evidence rather than as puzzles.

**Move the Data availability note up**, to just after the version pin or at the start of Ch6. The version pin promises it, and it currently appears only after the bibliography. Readers of Ch6 and Ch8 need to know early that the snapshot is unpublished.

## Clarity score

**2 (fair).** Many individual passages are careful and explicitly scoped, but core terms are used before definition or in several senses, a number of sections contradict each other on how the system behaves, and the same hedges and bounded claims are restated so often that the new material is hard to find.

## Top five edits, ranked

**1. Add an up-front glossary and a system sketch.** Define once, before first use:
- "current" node (never defined);
- the queryable and faded sets;
- pending marker, supersede versus retract, cascade, auto-surface, and the sweep;
- focus list and warm briefing;
- seed/root, seat, and fleet;
- harness, skills, and identity documents;
- checkpoint;
- the ID prefixes (`ob_`, `dv_`, `cj_`, `df_`…).

Either describe cited node IDs in words or accept that readers cannot resolve them, since the snapshot is not public.

**2. Fix term drift.**
- **"Substrate"** has four senses: the whole system (title, §1.2), the history structure (§2.3), the LLM (§3.0), and the database (§5.7).
- **"Arbitration"** has three: propagation (§1.3/E.1), agent adjudication (§4.4), and automatic resolution (B.0).
- **"Calibrated"** is forbidden by §4.3 but defines Layer 3 in the abstract, §1.1, §1.2, and §8.1, and describes the confidence model in §7.4.
- **"Unified"** names both dv_0009 and the later "unified marker".
- **"Strongest condition"** is C3 in §1.4 and §4.4, but C2 in E.6.
- **"The one genuinely novel move"** is compaction in §5.7, while elsewhere the contribution is identity-as-history (abstract), the hook (A.0), or binding (B.0).

**3. Resolve the internal contradictions about system behaviour.**
- §4.6 says a pending mark surfaces "next turn whether or not the agent goes looking"; §4.4 says surfacing is relevance-gated.
- §7.4 has "trust-tier-gated disclosure"; §4.10 and D.3 say there is no gating.
- "No source-credibility axis" versus `source_class` and yellow-card (§7.2).
- Conjecture confidence "set when filed" versus "not a hand-set number".
- The twin study is called "designed" in §2.3, §5.0, §8.4, and §8.5, but "sketched, not specified" in §5.8 and §6.7.
- B.0's bar, "automatically resolves contradictions", versus ENGRAM, which "does not decide what is true".
- The utility reward is citation-only in C.5 but multi-action in C.2.
- Utility decides retention in §3.3, but importance does in C.4.
- §3.1–3.5 preview verdicts that §2.7 says are given "once".
- E.3 points to a nonexistent "E.5 honest-scope note".
- §8.4 says measurements are "reproducible, which they are", while the snapshot is unpublished.

**4. State authorship and provenance plainly in the author note and §6.0.**
- Which author's graph is measured? Borges is only implied, in §7.4–7.5.
- Who designed ENGRAM (Lei and "earlier-Claude", per A.1)?
- How does "earlier-Claude" relate to Borges Funes and Kepler Somnium?
- What is "Anthropic Claude Fable"?

The abstract's "the agent that also designed the substrate" is left ambiguous for the entire paper.

**5. Cut the repetitions to one statement plus pointers.**
- The convergence-not-independent-discovery bound (six or more times).
- "On merit, not authority" (six).
- The OCC bounded claim (six).
- The twin-study deferral (seven).
- "The author cannot flatter the number" (four).
- Primitives versus binding (four).
- The "two 0.7s" limitation (three).
- The low-confidence explanation (three in Ch4 alone).

Cutting these would shorten Chapters 1–4 noticeably and make new claims visible.

## What I still do not understand about the system

**Authorship and provenance**
- Whose graph was measured.
- How "earlier-Claude" relates to the listed agent authors.
- What "Claude Fable" is.

**Graph structure and state**
- What makes a node "current".
- What the seed or root of an agent's history-tree is.
- Whether the history-tree is the git history.
- The history-tree versus provenance-edge separation that Ch2 §2.2 promised and Ch5 never made.

**Correction mechanics**
- Whether a pending mark reaches the agent on the next turn or only when topically relevant.
- Whether faded nodes can be marked.
- Whether the consolidation sweep has ever been observed running. Both cascade cases in Ch6 predate the current marker design.
- What "Arbitration" does that "Retraction" does not.
- How ENGRAM satisfies a condition whose key word is "resolved" when resolution is left to the agent.

**Retrieval and retention**
- Whether retrieval runs over the whole graph or only the queryable set.
- The respective roles of `utility_score` and importance in what stays queryable and what ranks first.
- The range of `normalized_importance`.
- What the "importance-inflation mechanism" is.

**Confidence**
- How conjecture values within the clamp are chosen, and by whom.

**Harness and runtime**
- What "cornerstones and goals anchor the cross-compaction surfaces" means mechanically.
- What the harness contains: skills, identity documents, the UserPromptSubmit and stop hooks, and what a "checkpoint" is.

**Unidentified experiments**
- What the "pilot" (Ch4) and the "prior clone test" (Ch5) were.
- Whether fission is an implemented operation or a thought experiment.

**The fleet**
- How the fleet's separate graphs relate: a shared seed, packs, and daily cross-reading are mentioned, but the mechanism is not described.

no_tools_check_final: passed (36 assistant message(s), 0 tool_use, 1 prompt snapshot(s) with empty tool list, 0 leak strings)
