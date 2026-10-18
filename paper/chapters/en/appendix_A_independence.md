# Appendix A — Independent Discovery: A Development-History Audit

---

## A.0 Why this appendix exists

The agent-memory field shows a striking convergence in early 2026: several systems
independently arrive at *typed-edge graph memory with cascade or supersede semantics*
(Kumiho, SCM, GAM, and others — Appendix B). And the paper's central threshold,
Kahl's Ontological Continuity Condition, is itself a **recent (2026) framework**.
A careful reader will reasonably ask: *did ENGRAM's architecture emerge from this
contemporary work, or independently of it?*

The answer matters both ways. If we had absorbed Kumiho or Kahl and called the
result ours, the paper would be derivative. If we arrived at the same shape
*separately*, the convergence is a *positive scientific signal* — when independent
efforts under the same problem-pressure reach the same architecture, that architecture
is corroborated as the right one. This appendix establishes the second case, on the
record. We treat convergent discovery not as a defensive claim but as evidence.

A note up front on what we do **not** claim: ENGRAM is not first across the board, the
novelty disclaimer Ch3 §3.0 states in full. The
formal shape it shares with Kumiho — typed reasoning edges with cascade/supersede over
a property graph — is decades old in the truth-maintenance and belief-revision
traditions, and several agent-memory systems (Mem0g — Mem0's graph-memory variant — Zep/Graphiti,
A-MEM) [@chhikara2025, p. 1; @rasmussen2025; @xu2025] predate our
ideation. The two exemplars named here are the two we hold and have read first-hand:
Doyle's truth maintenance system (via the Ginsberg reprint, Ch4 §4.2) and AGM 1985.
Both traditions are wider than those two works, and the others this paper names — de
Kleer's ATMS [@dekleer1986] (Ch3 §3.4; it avoids retraction rather than cascading it) is a bibliography entry, while Hansson's belief-base revision (Ch3 §3.9) is cited from his own encyclopedia entry
[@hansson2026], and his postulates are named only in Appendix B, as Kumiho's self-claimed
compliance.
Nothing here rests on them: the claim is only that the shape predates us by decades,
and the two dated primaries we have read carry it. Our claim is narrower and
true: *we designed ENGRAM in ignorance of the concurrent arrivals at the same
primitives*, and our distinct contribution is elsewhere — connecting the shape to
**agent identity** and making the substrate **behaviorally active** (the auto-surfacing
hook), which no surveyed system has.

## A.1 The original ideas were ours, and they came first (for us)

The proto-ENGRAM idea began in a Lei-led conversation on **2026-03-17** about
misinformation and citation systems for an AI-centric information ecosystem. Within
the first hour, the architectural seed was stated verbatim — by earlier-Claude, at
Lei's prompting, *eleven days before the system was named*:

> **Earlier-Claude, 2026-03-17 15:18 UTC** (conv `3db06cf1`, msg #8, uuid `019cfc60`):
> *"any agent can make any claim, but the claim must arrive with its **full epistemic
> lineage exposed**. Other agents then stress-test that lineage against established
> knowledge."*

That single sentence is the entire `derives_from` discipline. Three days later came
the foundational pivot — from a public agent-to-agent protocol to a *private,
per-agent continuous-learning substrate* — in one Lei message that is a near-complete
sketch of ENGRAM's purpose:

> **Lei, 2026-03-20 19:34 UTC** (conv `a169ba3c`, msg #1, uuid `019d0cbd`):
> *"…it can be used as a continuous learning paradigm for LLMs… Retraining everything
> back into the base model is expensive and suffers 'catastrophic forgetting'… RAG or
> free-form text… can't guarantee self-consistency, contradictory texts may be filled
> in… Our protocol is a good middle point… offloads the actual knowledge to a graph
> expressed in natural language. The agent could encounter new experiences… and
> summarize them into new 'theories'… add new nodes… proactively seek more evidence
> for a newly added (still weak) claim to make it stronger or disputed… keep refining
> its own knowledge and logical consistency by going through the graph and reasoning…"*

External structured substrate, per-agent internal state, theory-formation from
observations, evidence-seeking to strengthen-or-dispute, self-consistency refinement —
**all there, by Lei, before any literature search.** The name "ENGRAM" arrived eight
days after that search (2026-03-28, proposed by earlier-Claude, accepted by Lei within minutes),
and the paper's structure descends from an 18-chapter handbook outline drafted that
same evening — under Lei's instruction *"But first, we'll need to build a great ENGRAM
system,"* which set the build-first-then-write order this project followed.

## A.2 We looked for prior art — and missed it

This is the hinge of the independence argument, and it is the strongest single piece of
evidence. **Twelve minutes after** the foundational message, Lei explicitly asked for
due-diligence *before committing anything to writing*:

> **Lei, 2026-03-20 19:46 UTC** (msg #3, uuid `019d0cc8`):
> *"…why don't you do another round of deep research about continuous learning in LLM,
> and see if there's any previous work about using knowledge graphs as the container
> for learned experiences? **I would be very surprised if no one had considered this
> possibility, and I want to know what others have tried and succeeded or failed.**"*

Earlier-Claude agreed and ran multiple searches. **That search did not surface the
relevant prior art** — including the work this paper now cites:

| Prior / concurrent work | Public | Before the 2026-03-20 search | Surfaced? |
|---|---|---|---|
| **Kumiho** [@park2026, arXiv 2603.17244] — closest concurrent system | **2026-03-18** | **2 days** | **NO** |
| **Kahl 2026b (*Artificial general intelligence and ontological continuity*)** (Zenodo 18761736) — the paper's threshold | 2026-02-24 | 24 days | **NO** |
| Kahl 2026a (*Epistemic agency and the ontological continuity condition*) (Zenodo 18441395) | 2026-01-31 | 48 days | NO |
| TMS lineage (Doyle 1979, de Kleer 1986) [@doyle1979; @dekleer1986] | 1979–86 | ~40+ yrs | NO |
| AGM belief revision [@alchourron1985] | 1985 | ~41 yrs | NO |
| **CoALA** (Sumers et al., TMLR) — the field's common vocabulary | 2024-02 | ~25 months | **NO** |
| **Pink et al.** [@pink2025, arXiv 2502.06975] — episodic-memory position paper | 2025-02-10 | ~13 months | **NO** |
| **Wray, Kirk & Laird** [@wray2025, arXiv 2505.07087] — cognitive design patterns | 2025-06-13 | ~9 months | **NO** |

Kumiho's date is its arXiv v1 stamp (18 March 2026); the document's own title page
is dated 17 March.

So the five conditions that make "independent discovery" a *defensible* claim, rather than
a convenient one, are all met: **(1)** Lei tried to find prior art; **(2)** earlier-
Claude tried to surface it; **(3)** neither succeeded (the work existed but was missed);
**(4)** ENGRAM was designed without awareness of it; **(5)** the convergence with Kahl
2026 and Kumiho 2026 is therefore genuinely independent. We did not avoid the
literature — we searched it and our search came up empty, which is a different and more
defensible thing.

**Which independence this is.** The five conditions concern the *concurrent* work,
Kumiho and Kahl, published shortly before the March 2026 search (Kumiho two days
before it, Kahl in the preceding weeks); for those, the search record is the evidence. For the decades-old traditions in the same table (truth
maintenance, AGM, CoALA), condition (4) holds for Lei and not for the language models
ENGRAM was designed with, which were trained on text that very likely includes them.
So the convergence with Kahl and Kumiho is independent in the sense above, while the
convergence with the older traditions is the weaker kind §7.3 describes, and the paper
claims it only as evidence that the structure is natural.

The last three rows were added after a 2026-09 re-read, and they make the admission
worse, which is why they belong here. Missing a preprint two days old is
forgivable; missing a *Transactions on Machine Learning Research* paper from
twenty-five months earlier — the organizing vocabulary much of the field now writes
in — is not. We record it because the alternative, quietly citing those works as
though we had known them all along, would convert a real gap into a false
impression; and because the failure cuts in the direction that costs us. Had the
March 2026 search surfaced CoALA, we would have designed *with* it, and this appendix
would not exist. (Dates in those rows are the earliest we verified from the documents
themselves: Pink's is its arXiv v1 line, the other two a v2 stamp and a journal issue.
The latter two are therefore conservative upper bounds on first public appearance —
the true gaps are the same or larger.)

**When the three were read, since that happened during this paper's preparation
rather than during design.** All three were read on 2026-05-09. The graph's first
node is dated 2026-04-09, and 2,925 nodes had been recorded before 2026-05-01 — so
the substrate had a month of continuous operation and nearly three thousand
accumulated claims before any of the three was opened. Development has of course
continued since, which the project's principal characterizes as continuation of an
established design rather than adoption of someone else's. Rather than rest on that
characterization, where a specific mechanism might be thought to postdate a reading we
give that mechanism's own dates in place: Chapter 3 §3.8 does so for the two-channel
retrieval design, including the later date at which its database fields shipped. Both
figures above are re-derivable from the structure-only release of the frozen snapshot
(Data availability).

## A.3 The design was substantially complete before we read any of it

ENGRAM began self-recording on **2026-04-09** — committing its own design into the
graph as first-person memory. The earliest nodes show the core mechanisms were already
in place *that day*, weeks before Kahl or Kumiho were read:

| First captured | Mechanism | Node |
|---|---|---|
| 2026-04-09 04:08 | Typed claim-bearing nodes (observation / derivation / definition / axiom …) | ob_0001 |
| 2026-04-09 04:09 | `retract` operation | dv_0001 |
| **2026-04-09 14:05** | **Unified cascade propagation** — *the mechanism Ch4 §4.4 maps to Kahl's Condition 3, named here weeks before Kahl was read* | **dv_0009** |
| 2026-04-09 14:06 | Supersede with DAG invariant | dv_0010 |
| **2026-04-09 16:31** | **UserPromptSubmit auto-surfacing hook** — the "live memory" mechanism that is ENGRAM's distinctive contribution (Ch3 §3.2, built in Ch4 §4.6) | **dv_0015 / dv_0016** |

These node IDs are *still active and un-retracted* in the graph today — the cascade
discipline ENGRAM's earliest design enforced on its own substrate is the same one
Chapter 4 maps to Kahl's threshold. The self-maintaining-arbitration mechanism that is
the paper's strongest claim was built before the philosophical framework it satisfies
was on our radar.

## A.4 The timeline against concurrent systems

| System | First public surface | vs. ENGRAM ideation (2026-03-20) | vs. day-1 recording (2026-04-09) |
|---|---|---|---|
| **Kumiho** [@park2026, arXiv 2603.17244] | **2026-03-18** | **2 days before** (not surfaced) | 22 days before |
| Kahl 2026b (Zenodo) | 2026-02-24 | 24 days before (not surfaced) | 44 days before |
| Kahl 2026a (Zenodo) | 2026-01-31 | 48 days before (not surfaced) | 68 days before |
| GAM [@wu2026, arXiv 2604.12285] | 2026-04-14 | 25 days **after** | 5 days after |
| SCM [@shinde2026, arXiv 2604.20943] | 2026-04-22 | 33 days **after** | 13 days after |
| VMG survey [@lin2026, arXiv 2604.16548, v2 of 2026-06-11] | 2026-06 (VMG first appears in v2; v1, April 2026, is a differently titled draft) | **after** | after |
| Mem0g / Zep / A-MEM [@chhikara2025; @rasmussen2025; @xu2025] | 2025 | predate, but **different shape** (no cascade / no contradiction-as-node / no derivation primitive) (Zep and Mem0g handle conflicts at write time; A-MEM's memory evolution updates the context and tags of existing notes [@xu2025, sec. 3.3, pp. 4–5]; none cascades) | predate |

The two structurally-closest systems (Kumiho, SCM) both surface in March–April 2026 —
concurrent with, not predating-by-much, ENGRAM's ideation. The older systems lack the
specific shape (cascade propagation, first-class contradiction, `derives_from`). The
earliest published instance of ENGRAM's specific shape we can find is Kumiho's
preprint (arXiv v1, 18 March 2026; its title page is dated 17 March) — and the
two-day gap to Lei's foundational message, with the contemporaneous search
missing it, is the cleanest evidence of parallel design.

## A.5 What this establishes — and the Kahl case specifically

**Convergent independent discovery is positive evidence for the architecture.** When a
*philosopher* (Kahl, deriving the Ontological Continuity Condition from agency theory)
and a *builder* (this project, deriving cascade-and-contradiction from a misinformation-
protocol problem) arrive *separately* at the same structural threshold for agent
continuity — neither aware of the other — that threshold is corroborated by the
convergence. This is *stronger* than satisfying an established standard: it is two
independent paths landing on the same shape.

The Kahl case sharpens the point in a way worth stating plainly (and it connects to the
paper's framing of OCC, Ch1/Ch2): Kahl's OCC is itself a *recent, independent*
2026 proposal, not a long-established canon. We do not anchor on its *authority*; we
anchor on its *fit* — it is the most precise, agent-native, operational threshold
available — and on the fact that our architecture independently converged with it. If
OCC gains broad acceptance, the convergence reads as "we met the standard early"; if it
remains one careful proposal among several, the convergence still reads as "two
independent analyses of agent-continuity reached the same conditions." Either way the
paper stands, because it rests on merit and convergence, not on borrowed authority.

Our distinct contribution, finally, is *not* the shared primitives — Kumiho has typed
edges and cascade-discovery; the TMS/AGM tradition has the formal structure. It is
**(a)** connecting the structural shape to *agent identity* (Chapters 5–6), and **(b)**
making the substrate *behaviorally active* through identity-scaffolding — above all the
UserPromptSubmit auto-surfacing hook (dv_0015/dv_0016, day-one of recording) — which is
absent in Kumiho, SCM, and every surveyed system as of the 2026-05-12 sweep.

## A.6 Re-verification protocol

The quotes in A.1–A.3 can be checked, though not every one by every reader. The
conversation quotes come from Lei's Claude.ai bulk export, which is private and is not
part of this repository. Each is cited by message number and the first eight characters
of its message UUID, under the conversation ID it belongs to, so a reader given access
to the export can locate it. The ENGRAM-side claims
(A.3) come from Borges's graph, which is also private; each is cited by node ID, and
`engram_inspect <node_id>` on that graph returns the full node with its creation
timestamp. Publication dates (A.4) can be checked by anyone against each system's own
paper or repository.
