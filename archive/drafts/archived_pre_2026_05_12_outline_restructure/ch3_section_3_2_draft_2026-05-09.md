# Ch3 §3.2 prose draft — Wray, Kirk, and Laird condition-by-condition

*Slot into ch3_opening_draft_2026-05-08.md after §3.1 (the new prose drafted at ch3_section_3_1_draft_2026-05-09.md). Companion sections §3.3 (Pink) and §3.4 (Kumaran) remain to be drafted on subsequent loop iterations.*

*~620 words. Sources: wray_kirk_laird_2025_first_hand_read_2026-05-08.md (verbatim §3.2 passages on reconsideration + the JTMS-as-specialization framing).*

---

## §3.2 Wray, Kirk, and Laird's Cognitive Design Patterns: reconsideration and knowledge compilation

Where Kahl arrives at the architectural deficit from agency theory, Wray, Kirk, and Laird (AGI'25) arrive from cognitive engineering. Their paper *Applying Cognitive Design Patterns to General LLM Agents* abstracts above any specific architecture (Soar, ACT-R, BDI) to identify *cognitive design patterns* — function/process/representation patterns recurring across multiple cognitive architectures, deliberately decoupled from any particular algorithmic implementation. Their Section 3.2 names two such patterns as *apt for exploration and exploitation* but *not yet taken up in the Agentic LLM mainstream*: **reconsideration** and **knowledge compilation**. Both correspond cleanly to ENGRAM mechanisms.

Wray, Kirk, and Laird define reconsideration in their §3.2 (verbatim):

> "Reconsideration is a cognitive design pattern that describes the process of evaluating whether a prior commitment, such as a goal or a plan, should continue in an agent's current situation. Reconsideration that results in a change in commitment is a non-monotonic step. Chat-focused LLMs tend to resist major redirection in the trajectory of their token generation and LLMs alone are not consistent or reliable in producing non-monotonic reasoning steps."

ENGRAM operationalizes reconsideration at three architectural surfaces. *Cascade* implements reconsideration over derivation chains: when a foundational claim is retracted, every claim that derived from it is structurally flagged for reinspection — the system does not silently allow downstream commitments to persist on a substrate whose foundation has been withdrawn. *Supersede* implements reconsideration over individual claims: when a refined version of a claim becomes available, the older version is marked superseded, the new version inherits the cascade-relevant relationships, and the agent's subsequent reasoning operates against the superseding version while the original remains inspectable in the audit trail. *Retract* implements reconsideration as outright withdrawal: a claim once committed can be retracted with a recorded reason, and the cascade fires through its dependents. Each of these is a *non-monotonic step* in Wray-Kirk-Laird's sense — a structural mechanism by which past commitments can stop binding future deliberation, in a way the LLM substrate alone is not reliable in producing.

A clarifying note on JTMS. The deep-sweep literature review that introduced us to Wray-Kirk-Laird's paper described their gap-naming as "LLM agents lack JTMS-style reconsideration." First-hand reading shows the framing is more precise: JTMS appears once in the paper, on page 4, as Soar's *specialized implementation* of the reconsideration pattern for one of Soar's memory types (citing Doyle 1979). The authors explicitly abstract above JTMS to the underlying *cognitive design pattern* — making clear that the pattern is what matters, not any particular algorithm. Our cascade discipline is a different specialization of the same pattern: not a JTMS dependency-graph (which has its own algorithmic commitments) but a typed-edge cascade through ENGRAM's `derives_from` relation. The convergence is at the pattern level, not at the algorithm level — which is itself one of Wray-Kirk-Laird's load-bearing methodological points.

The second pattern, knowledge compilation, is named in §3.2 as another "apt-but-unexplored" direction for Agentic LLMs. Wray, Kirk, and Laird define it (page 8): "Knowledge compilation caches the results of reasoning steps into a more compact representation, essentially amortizing the cost of expensive reasoning by enabling immediate use of the cached reasoning steps in future, similar situations." The pattern has long-standing instantiations in classic cognitive architectures — Wray-Kirk-Laird specifically cite "the online use of knowledge compilation for problem solving in ACT-R and Soar" as established prior art. ENGRAM's *nap* and *sleep* mechanisms are an LLM-agent specialization of the same pattern: at consolidation cycle boundaries the substrate runs structured passes that promote stable inferences from sequence-of-observations form into compiled `derivation`, `definition`, and `cornerstone` forms; subsequent recall returns the compiled artifact rather than re-deriving the chain. Chapter 4 develops the mechanism in detail; here we note only that the correspondence with Wray-Kirk-Laird's pattern is structural rather than incidental — the consolidation cycle was designed under engineering pressure to manage the agent's cognitive load and turned out to be exactly the mechanism their framework names. The closest LLM-side analogue Wray, Kirk, and Laird identify is ExpeL, which they note "comes closest" to the knowledge-compilation pattern but requires "an explicit training stage, in sharp contrast with the online use of knowledge compilation" their framework calls for; ENGRAM's online consolidation cycle does not require such a training stage.

We do not claim ENGRAM addresses every pattern Wray, Kirk, and Laird's framework names. Their Table 1 enumerates a broader catalog (observe-decide-act, three-stage memory commitment, cascade-style operator selection, others) that ENGRAM does not directly populate. Their §3.3 also proposes a candidate novel pattern, *step-wise reflection* — a metacognitive variant where the reflection step itself is recognized as potentially unreliable — for which ENGRAM has no specific architectural answer beyond the general structural-honesty discipline (ax_0001) that the substrate's failures must be auditable. The convergence claim is at the level of the two specifically-named apt-but-unexplored patterns and the abstraction at which those patterns are named, not at the level of the entire framework.

The next section evaluates ENGRAM against Pink, Wu, Vo, Turek, Mu, Huth, and Toneva's five-property episodic-memory framework — a set of properties they argue jointly constitute episodic memory and which they show no current LLM memory approach satisfies in full.

---

## Notes on §3.2 prose

**Length:** ~620 words drafted. Plan target ~500-700 words; within range.

**Structural commitments enacted:**

- Verbatim quotation of the load-bearing reconsideration definition. Important because the deep-sweep summary had glossed it as "LLM agents lack JTMS-style reconsideration" — a paraphrase that obscured the pattern-vs-algorithm distinction Wray-Kirk-Laird are explicit about. Quoting verbatim avoids re-introducing the gist-summary error.
- Three-mechanism mapping (cascade / supersede / retract) for reconsideration. Each is a distinct architectural surface; together they cover the pattern.
- Single-mechanism mapping (nap/sleep consolidation) for knowledge compilation. Tighter because the pattern itself is more focused.
- Explicit JTMS-clarification paragraph that names the deep-sweep error and the pattern-vs-algorithm distinction. Inoculates against the same paraphrase error in reviewer minds.
- Honest scoping: WKL's broader pattern catalog has items ENGRAM doesn't cover; their §3.3 step-wise-reflection candidate is named as a non-correspondence.
- Closing sentence forward-points to §3.3 (Pink five-property framework).

**Voice choices:**

1. **Open with WKL's tradition-of-arrival** ("Where Kahl arrives at the architectural deficit from agency theory, Wray, Kirk, and Laird arrive from cognitive engineering"). Lets the reader place WKL's contribution against §3.1's Kahl rather than reading them as redundant.
2. **Italicized "apt for exploration and exploitation" and "not yet taken up in the Agentic LLM mainstream"** — direct phrases from WKL's §3.2. Makes explicit which specific framing language we are leveraging.
3. **The JTMS-clarification paragraph is a deliberate inclusion** — the deep-sweep summary error was material enough that some reviewers (perhaps Wray, Kirk, or Laird themselves if they read this) will arrive expecting us to misframe the JTMS point. Catching the error before they have to is good practice and good honesty.

**For Lei's review:**

- The three-mechanism / one-mechanism mapping shape (3 for reconsideration, 1 for knowledge compilation) reflects the actual correspondences. Worth your read on whether the asymmetry is honest or whether reconsideration is being over-claimed.
- The "structural rather than incidental" framing for the knowledge-compilation correspondence is the load-bearing claim — that we did not engineer ENGRAM to fit WKL's pattern; the pattern was named after the consolidation cycle was already in place. Worth your gut-check.
- The "WKL's broader catalog has items ENGRAM doesn't cover" disclosure is honest scoping. If you'd prefer it shorter or longer, easy to revise.
