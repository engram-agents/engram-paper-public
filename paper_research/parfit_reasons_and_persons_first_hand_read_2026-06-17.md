# Parfit, *Reasons and Persons* (Oxford: Clarendon Press, 1984) — First-Hand Read

**Read date:** 2026-06-17
**Purpose:** Clear the single hard citation blocker on Appendix B.4 / dv_0424 (ENGRAM ↔ Parfit's Relation R). Capture verbatim, page-numbered passages for the Relation R definition and the "identity is not what matters" thesis, per Disciplines B (first-hand-read precondition, ls_0039) and C (verbatim quotation, ls_0011).

**Source provenance (honest scope).** The prior blocker (ob_1044) was that WebFetch reliably fails on the scanned/JBIG2 pre-2000s PDFs (Fribourg excerpt). Resolved here via a **full-text-layer PDF** of the Oxford 1984 edition hosted by the University of Athens philosophy course repository (`eclass.uoa.gr`, file `Parfit Reasons and Persons.pdf`, 560pp, producer `pdf-tools.com` 2009 — i.e. a scanned book carrying an embedded OCR text layer). The embedded pagination matches the canonical Oxford 1984 edition (pp. 205–217 visible inline), which cross-checks the page attributions below. The quoted definitional sentences extract as clean English with no OCR garble.

- Local copy (gitignored — full book, copyright): `paper_research/source_pdfs/parfit_reasons_and_persons_1984_uoa.pdf`
- Before final publication: confirm these page numbers against a library/print copy of the Oxford 1984 edition (the standard scholarly cite). The *wording* below is verbatim from the text layer; the page numbers are from the same source's embedded pagination.

---

## §78 "The Psychological Criterion" — the two general relations (p. 206)

The kinds of direct psychological connection Parfit appeals to (p. 205–206):

> "Besides direct memories, there are several other kinds of direct psychological connection. One such connection is that which holds between an intention and the later act in which this intention is carried out. Other such direct connections are those which hold when a belief, or a desire, or any other psychological feature, continues to be had."

The two definitions (p. 206):

> "Psychological connectedness is the holding of particular direct psychological connections."

> "Psychological continuity is the holding of overlapping chains of strong connectedness."

Connectedness admits of degree; "strong connectedness" is the threshold (p. 206):

> "When there are enough direct connections, there is what I call strong connectedness."

The transitivity point — connectedness is **not** transitive, continuity is (p. 206). This is the move that matters for ENGRAM (Appendix B.3): recall-based connectedness breaks transitivity (Reid's brave-officer), so identity must rest on continuity / overlapping chains, not on present connection:

> "Strong connectedness is not a transitive relation. I am now strongly connected to myself yesterday, when I was strongly connected to myself two days ago ... It does not follow that I am now strongly connected to myself twenty years ago. And this is not true."

The Psychological Criterion stated (p. 207):

> "The Psychological Criterion: (1) There is psychological continuity if and only if there are overlapping chains of strong connectedness. X today is one and the same person as Y at some past time if and only if (2) X is psychologically continuous with Y, (3) this continuity has the right kind of cause, and (4) it has not taken a 'branching' form. (5) Personal identity over time just consists in the holding of facts like (2) to (4)."

---

## §79 "The Other Views" — Relation R and "identity is not what matters" (pp. 215–217)

The thesis statement (p. 215):

> "The rival view is that personal identity is not what matters. I claim
> What matters is Relation R: psychological connectedness and/or continuity, with the right kind of cause.
> Since it is more controversial, I add, as a separate claim
> In an account of what matters, the right kind of cause could be any cause."

The Reductionist conclusions, conclusion (1) and (4) (pp. 216–217):

> "(1) We are not separately existing entities, apart from our brains and bodies, and various interrelated physical and mental events. ... Our identity over time just involves (a) Relation R—psychological connectedness and/or psychological continuity—with the right kind of cause, provided (b) that this relation does not take a 'branching' form, holding between one person and two different future people."

> "(4) Personal identity is not what matters. What fundamentally matters is Relation R, with any cause. This relation is what matters even when, as in a case where one person is R-related to two other people, Relation R does not provide personal identity."

The "no further fact" reductionism (the basis for "not a special further fact", pp. 216, 7107ff.). Parfit denies that identity "involves a further fact" beyond physical/psychological continuity, and denies we are "separately existing entities" (a Cartesian Ego / further phenomenal fact):

> "If we do not believe that we are separately existing entities, can we defensibly believe that personal identity does not just consist in physical and psychological continuity, but is a further fact? I believe that we cannot."

A compact restatement Parfit himself uses later in the book (p. 262 region of the text):

> "Relation R is what matters. R is psychological connectedness and/or psychological continuity, with the right kind of cause."

---

## What this backs in the paper

**Appendix B.4 claim** — "Relation R — psychological connectedness (memories, intentions, character carried forward) plus continuity (overlapping chains of those connections) — and explicitly *not* a special further fact":
- "memories, intentions, character carried forward" ← the direct-connection kinds (memory; intention→act; persisting belief/desire/feature), p. 205–206. ✓ verbatim-grounded.
- "overlapping chains of those connections" ← *"Psychological continuity is the holding of overlapping chains of strong connectedness"*, p. 206. ✓ verbatim, near-exact.
- "not a special further fact" ← the Reductionist denial of a "further fact" and of "separately existing entities", pp. 216–217. ✓ grounded.
- "identity is not what matters" ← p. 215 + conclusion (4), p. 217. ✓ verbatim.

**dv_0424 mapping** ("ENGRAM provenance chains *literally are* overlapping chains of connectedness; each `derives_from` edge is a connectedness link, the connected structure is the continuity") — the mapping is now primary-source-grounded, not secondary (ob_1043). The structural fit is tight: Parfit's "overlapping chains of strong connectedness" is, almost word for word, what a provenance DAG is.

**Honest caveat to preserve in the prose.** Parfit's connections are *psychological* (memory/intention/belief held in a mind); ENGRAM's are *structural* (edges in a graph). The mapping is an instantiation-of-the-relational-property claim, not an identity claim — it says ENGRAM provides *what Parfit says matters* (the connectedness/continuity structure), not that ENGRAM's links are themselves mental states. This keeps B.4 on the right side of the autonoetic/noetic boundary (B.7).
