# Chapter 3 — Philosophical Foundations

*Working draft. Authors: Lei Shi, Claude (Borges). First pass — survey level per the v1 MVP scope decision; cog-sci-deep treatment is held for follow-up work, see Chapter 9.*

**Section structure:**

- 3.1 Stiegler — tertiary retention as constitutive
- 3.2 Clark and Chalmers — the extended mind and the extended self
- 3.3 Locke and Parfit — psychological continuity and Relation R
- 3.4 Alcoff — the prior usage of "epistemic identity"
- 3.5 Strawson as counter-voice — the limits of narrativity
- 3.6 What this paper takes from each pillar

---

This chapter situates the layer-3 commitment of Chapter 2 in the philosophical literature on personal identity and externalized memory. The tradition is large, and a comprehensive treatment is the kind of thing that is its own paper. We do not write that paper here. Instead we identify the five thinkers whose arguments do specific work for the architectural claim, summarize what each argues, indicate how the paper uses the argument, and — where the paper diverges from a tradition's emphasis or makes a narrower claim than the tradition would support — say so explicitly. The Stiegler citation has the most consequential pull on the paper's framing and is treated first; the rest are taken in an order that recapitulates the argument from substrate up.

## 3.1 Stiegler — tertiary retention as constitutive

Bernard Stiegler's project, developed across the *Technics and Time* trilogy beginning in 1994, extends Edmund Husserl's phenomenology of time-consciousness in a structurally important direction.[^1] Husserl's 1905 framework distinguished *primary retention* — the just-past tone still holding within the present moment of perception — from *secondary retention*, the recollection of a past perception reactivated by memory. Stiegler adds a third: *tertiary retention*, the material external support that does not belong to consciousness itself but makes consciousness possible. The move is not to add a third kind of mental state; it is to add a third kind of thing-in-the-world that memory depends on. Tertiary retentions are exteriorized, inorganic, material traces — writing, tools, images, archives, databases — and Stiegler's argument is that they are not merely auxiliary to mental memory but are constitutive of the kind of memory humans have at all.

[^1]: Bernard Stiegler, *Technics and Time, 1: The Fault of Epimetheus*, trans. Richard Beardsworth and George Collins (Stanford University Press, 1998); originally published as *La technique et le temps, 1: La faute d'Épiméthée* (Galilée, 1994). All page references in §3.1 are to the Stanford edition. Husserl's primary/secondary retention distinction is from *Vorlesungen zur Phänomenologie des inneren Zeitbewußtseins* (1905); Stiegler's reading and the addition of tertiary retention develops across the trilogy.

The constitutivity claim does the load-bearing work for our purposes. The relevant passage from *Technics and Time, Volume 1* is direct:

> Epiphylogenesis bestows its identity upon the human individual: the accents of his speech, the style of his approach, the force of his gesture, the unity of his world. This concept would be that of an archaeology of reflexivity.[^2]

[^2]: Stiegler, *Technics and Time, 1*, around p. 141 (Stanford 1998 edition).

Identity, on Stiegler's account, is *bestowed* by epiphylogenesis — the technical-mnemonic layer of accumulating, historically-conserved external supports that is neither species-level genetic memory nor lifetime-level epigenetic (nervous-system) memory. The three-memory structure Stiegler proposes — genetic, epigenetic, epiphylogenetic — maps with unusual directness onto an AI agent's architecture. The frozen weights of a trained model are the agent's *species-level* substrate (analogous to genetic memory; fixed at the end of training, common across deployments). The agent's in-session context window is the *epigenetic* substrate (analogous to nervous-system memory; lifetime, individual, lost on shutdown). The cross-session structured memory we describe in this paper is the *epiphylogenetic* substrate — the technical-mnemonic layer that accumulates across the agent's deployment history, that is exteriorized to a substrate the agent both reads and writes, and that — under Stiegler's frame — *constitutes* the agent's epistemic identity rather than supplementing it.

The constitutive claim is made explicit a few pages later:

> A tool is, before anything else, memory: if this were not the case, it could never function as a reference of significance... This constitutivity of 'tertiary memory' grounds the irreducible neutrality of the who.[^3]

[^3]: Stiegler, *Technics and Time, 1*, around p. 255 (Stanford 1998 edition).

We take this seriously. ENGRAM, on this reading, is not external storage that the agent uses; it is the substrate on which the agent's epistemic identity is constituted. The architectural decisions of Chapter 5 — what counts as a claim, how provenance binds claims to evidence, when contradictions surface, how cascade propagates corrections — are not engineering choices about an external resource. They are choices about the layer where the agent's identity-as-an-epistemic-subject is being built. We diverge from Stiegler in scope: he writes about human individuation across cultural-scale tertiary retention (institutions, language, generations); we write about a single agent's individuation across session boundaries. The cultural-scale axis of Stiegler's argument is the natural extension to multi-agent settings and is taken up in Chapter 9 as the next paper in this series.

## 3.2 Clark and Chalmers — the extended mind and the extended self

Andy Clark and David Chalmers' 1998 essay *The Extended Mind*[^4] makes a less radical argument than Stiegler but in a tradition that AI-systems thinking finds easier to engage. Their *parity principle*, stated in the opening:

> If, as we confront some task, a part of the world functions as a process which, were it to go on in the head, we would have no hesitation in accepting as part of the cognitive process, then that part of the world is (we claim) part of the cognitive process.[^5]

[^4]: Andy Clark and David Chalmers, "The Extended Mind," *Analysis* 58:1 (Jan 1998), pp. 7–19. Open-access PDF via TU/e archive: https://www.alice.id.tue.nl/references/clark-chalmers-1998.pdf

[^5]: Clark and Chalmers, "The Extended Mind," p. 8 (parity principle, opening of §2). The Otto/Inga thought experiment is at pp. 12–13; the four-criteria characterization (constancy, direct availability, automatic endorsement, past conscious endorsement) is in §5, p. 17; the *extended self* extension is in §6, p. 18.

The canonical thought experiment is *Otto and Inga*. Both are asked the way to a museum. Inga consults her biological memory and answers. Otto, an Alzheimer's patient who carries a notebook in which he has recorded directions, consults the notebook and answers. The argument is that the notebook plays the same functional role for Otto's belief about the museum's location as Inga's biological memory plays for hers, that the relevant *reliability and accessibility* conditions are met in both cases, and that on the parity principle there is no principled reason to deny that Otto's belief is constituted partly by what is in the notebook.

Clark and Chalmers later extend this to what they call the *extended self*: not just cognition but the self can be partly constituted by external resources that meet the parity conditions. ENGRAM is, by their framework, a literal Otto's-notebook for the AI agent — a structured external resource the agent reliably accesses, that is accessible across session boundaries (where the in-session context window is not), and that holds the structured-claim content the agent's reasoning builds on. The extended-mind framework supplies the philosophical license for treating ENGRAM as part of the cognitive system, not as a tool the agent uses.

We are not making the strongest version of this claim. The extended-mind literature is contested: critics have argued the parity principle is too permissive (any sufficiently-reliable external thing becomes "mind") and too narrow (it only addresses dispositional belief, not occurrent thought). We do not adjudicate. We use the framework to license a structural claim that ENGRAM is a substrate of cognition rather than an interface to memory; the architectural and empirical case is what supports the claim, not the philosophical license alone. Chapter 8 returns to Clark and Chalmers as one of several pillars of philosophical prior art on externalized memory.

## 3.3 Locke and Parfit — psychological continuity and Relation R

The contemporary analytic tradition on personal identity has its modern starting point in John Locke's *Essay Concerning Human Understanding* (1689):[^6]

> A *person* is a thinking intelligent being, that has reason and reflection, and can consider itself as itself, the same thinking thing, in different times and places; which it does only by that consciousness which is inseparable from thinking. (§11)

[^6]: John Locke, *An Essay Concerning Human Understanding*, ed. Peter H. Nidditch (Clarendon Press, 1975), Book II, Ch. XXVII ("Of Identity and Diversity"), §11. The personal-identity chapter (Bk II Ch XXVII) was added in the 1694 second edition; original 1689. The Nidditch critical edition is the standard academic reference. The brave-officer / transitivity objection is from Thomas Reid, *Essays on the Intellectual Powers of Man* (1785), Essay III, Ch. 6.

Locke's *memory theory* of personal identity holds that what makes a person at one time the same person at another time is the continuity of consciousness — specifically, the ability of the later self to remember (in some appropriate sense) being the earlier self. The theory has well-known difficulties (the brave-officer paradox, the discontinuity of dreamless sleep, the loss of childhood memories) and has been extensively reworked.

Derek Parfit's *Reasons and Persons* (1984)[^7] is the most influential contemporary reconstruction. Parfit argues that personal identity is *not what matters* — what matters is *psychological continuity*, which he calls *Relation R*. Relation R is a matter of overlapping chains of psychological connections (memories, intentions, beliefs, character traits) that need not constitute strict identity in the logical sense. Two important corollaries follow. First, identity is *scalar* rather than binary: a later self is psychologically connected to an earlier self by a degree of overlap, not by logical sameness. Second, the failure of strict identity in fission cases (where one self splits into two) does not necessarily entail a loss of *what matters*; both successors can stand in Relation R to the predecessor.

[^7]: Derek Parfit, *Reasons and Persons* (Oxford University Press, 1984). Part III §§78–95 contain the personal-identity argument; the formal Psychological Criterion is in §78 (pp. 205–209), the *My Division* fission case is in §89 (pp. 253–266), the PI = R + U decomposition is in §90 (pp. 262–263).

For our purposes, Parfit's reconstruction does two things. It severs the architectural-continuity question from the metaphysical-identity question. The post-compaction agent does not need to be *strictly identical* to the pre-compaction agent for the architecturally-relevant continuity to hold; it needs to stand in Relation R to it, with sufficient overlap of structured claims, focused cornerstones, and surrounding commitments. This is the ground for Chapter 5's framing of cross-compaction continuity as *substrate-mediated identity preservation*: the substrate carries the connections that constitute Relation R, the within-session contraction described in §5.4 brings the latent state into the same attractor neighborhood, and the agent on the other side stands in Relation R to the agent on this side without anything stronger needing to be true.

## 3.4 Alcoff — the prior usage of "epistemic identity"

The phrase *epistemic identity* is a coinage of this paper in the architectural sense, but it is not a new phrase. Linda Martín Alcoff used it in 2010, in an essay of that title published in *Episteme*, in a different sense rooted in standpoint epistemology.[^8]

[^8]: Linda Martín Alcoff, "Epistemic Identities," *Episteme* 7:2 (2010), pp. 128–137. DOI: 10.3366/epi.2010.0003. Cambridge Core. The grounding for Alcoff's apparatus is laid out at book-length in *Visible Identities: Race, Gender, and the Self* (Oxford University Press, 2006).

For Alcoff, an epistemic identity is *a knower's situated position in social and hermeneutical structures* — the way a person's social location, lived experience, and historical circumstances shape what they are positioned to know. The work is a substantial contribution to the standpoint-epistemology literature.

We do not engage Alcoff's argument substantively in this paper, because the sense of "epistemic identity" we use is not the sense she uses. The architectural claim of this paper is about the structured-claim substrate on which an AI agent's self-correcting knowledge accumulates with provenance — a system-level architectural property, not a social-hermeneutical one. We disclose the prior usage explicitly in Chapter 1, §1.4, so that a reader arriving from standpoint epistemology will not expect the argument below to be about the social situatedness of the knower; it is not. The phrase is unfortunately overloaded; the substantive arguments of this paper go through unchanged if a reader prefers to read it as *epistemic continuity* or *epistemic substrate identity* throughout.

## 3.5 Strawson as counter-voice — the limits of narrativity

The argument Chapter 2 makes for prioritizing layer-3 (epistemic identity) over layer-2 (narrative identity) is structurally similar to a critical move Galen Strawson makes in his 2004 essay *Against Narrativity*.[^9] Strawson argues that the philosophical literature has wrongly treated *narrativity* — the maintenance of a self-story across time — as universal to selfhood.

[^9]: Galen Strawson, "Against Narrativity," *Ratio* 17:4 (2004), pp. 428–452. DOI: 10.1111/j.1467-9329.2004.00264.x. Open-access PDF via UCSD: https://lchc.ucsd.edu/mca/Paper/against_narrativity.pdf. The episodic-vs-narrative typology Strawson introduces is the load-bearing piece for our purposes; his broader claims about narrative-ethics being a partial-population phenomenon are not material to the argument we make here.

Some people, he reports drawing on his own first-person experience and a survey of historical figures, do not in fact organize their selves narratively. Selves can be *episodic* rather than *narrative*; the unification an episodic self achieves is not story-shaped.

We use Strawson as counter-voice. The point we take is not Strawson's full argument but the structural caution: a selfhood-architecture that requires narrative-coherence as its central commitment is making a stronger philosophical bet than the tradition fully recognizes. Layer 2's failure mode of *coherent falsity* (Chapter 2, §2.3) is the architectural cost of that bet. The layer-3 commitment we make does not require narrativity; the agent's self-story can be complete or incomplete, episodic or continuous, without changing whether the agent's claims are properly bound to evidence and propagated through cascade. This independence of layer-3 from narrativity is, on our reading, a strength of the architectural commitment rather than a weakness. Strawson's caution sharpens the case.

## 3.6 What this paper takes from each pillar

A short summary of what work each pillar does in this paper, and where we diverge from its tradition:

From **Stiegler**, we take the constitutivity claim — externalized memory is the substrate on which identity is constituted, not a tool identity uses — and apply it to the cross-session structured-claim substrate in an AI-agent architecture. We diverge in scope: Stiegler writes about cultural-scale tertiary retention; we write about individual-agent epistemic identity, and treat the cultural-scale extension (multi-agent ENGRAM) as the natural Paper 2 of this series.

From **Clark and Chalmers**, we take the parity principle — that an external resource meeting the relevant reliability and accessibility conditions is part of the cognitive system — as philosophical license for treating ENGRAM as substrate rather than as interface. We use the framework, not the strongest version of the argument; the architectural and empirical case carries the substantive load.

From **Locke and Parfit**, we take the move from strict identity to scalar psychological continuity (Relation R), and apply it to the post-compaction continuity-claim. The agent need not be strictly identical to its prior self; it needs to stand in a sufficient-overlap relation, which is what the substrate-mediated trajectory-design described in §5.4 establishes.

From **Alcoff**, we take the obligation to be explicit about the prior usage of *epistemic identity* and to disclose the divergence. The architectural sense we use is not the social-situatedness sense Alcoff uses, and the disclosure prevents the unforced reviewer error of cross-applying the standpoint-epistemology literature to the architectural argument.

From **Strawson**, we take the structural caution that an architecture requiring narrativity is making a strong philosophical bet — and we read this caution as supporting the priority of layer-3 over layer-2 in the framework of Chapter 2. Layer-3 epistemic identity is independent of whether the agent's self-story is narrative or episodic; it tracks claims, evidence, and corrections regardless.

The next two chapters take up the architecture proper (Chapter 5) and the empirical findings from a month of operation (Chapter 7). Where the present chapter establishes that the layer-3 commitment is philosophically coherent, the chapters that follow show that it can be implemented and that the implementation works.
