# Verification: does Jøsang's Subjective Logic (2013 draft) define trust-discounting? Does it bear on the "cumulative fusion gets provenance-weighting backwards" claim?

**Source**: Jøsang, *Subjective Logic* (draft, 18 Feb 2013), University of Oslo.
Local copies used (per dispatch instructions — not re-downloaded):
- `/home/agent-borges/engram-paper/paper_research/source_pdfs/josang_subjective_logic_2013.pdf` (69 PDF pages)
- `/home/agent-borges/engram-paper/paper_research/source_pdfs/josang_subjective_logic_2013.txt`

**Page-numbering note (load-bearing for anyone re-checking):** the document's
own internal page numbers (printed in the header/footer of each page, e.g.
"54", "CHAPTER 4...") are offset from the physical PDF page index by **+3**
(front matter — title page, preface, contents — is unnumbered). Verified
directly: `pdftotext -f 57 -l 57` shows internal page "54" (start of §4.8);
`pdftotext -f 55 -l 55` shows internal page "52" (start of §4.7);
`pdftotext -f 67 -l 67` shows internal page "64" (§5.2, the discounting-for-
experts remark). All PDF-page pointers below are physical-PDF-page numbers;
I give the document's own internal page number alongside for cross-reference
against any citation using the printed page.

---

## TOP-LINE VERDICT: Lei's belief is **CONFIRMED**

Jøsang defines a discounting (trust-transitivity) operator, in three variants,
in **Section 4.8 "Trust Transitivity"** (internal pp. 54–56 = PDF pp. 57–59).
It is explicitly a function of **the receiver's opinion about the source**,
applied to the whole recommended opinion as a unit, **before** any fusion
happens. The "exactly backwards" framing, stated as an unqualified claim about
Subjective Logic as a whole, is **not accurate** — SL has a first-class,
formally-defined mechanism for exactly the thing the draft sentence says it
lacks. Whether the *cumulative fusion operator itself* (as distinct from the
overall SL toolkit) lacks such weighting is a narrower and more defensible
claim — see §5 below for exactly what is and isn't supported.

---

## 1. Does Jøsang define a discounting/transitivity operator? — YES, three of them

**Section 4.8, "Trust Transitivity."** Internal p. 54 (PDF p. 57):

> "Assume two agents A and B where A trusts B, and B believes that proposition
> x is true. Then by transitivity, agent A will also believe that proposition
> x is true. This assumes that B recommends x to A. In our approach, trust
> and belief are formally expressed as opinions. **The transitive linking of
> these two opinions consists of discounting B's opinion about x by A's
> opinion about B, in order to derive A's opinion about x.**"

Figure 4.11 (same page) is captioned "**Principle of the discounting
operator**." A footnote later in the document (internal p. 64 / PDF p. 67,
footnote 1) glosses trust transitivity explicitly: "**Also called discounting
operator**." So "discounting operator" and "trust transitivity operator" are
the same thing, used interchangeably by Jøsang himself.

### 1a. Definition 23 — Uncertainty Favouring Discounting (internal p. 54 / PDF p. 57)

> "Definition 23 (Uncertainty Favouring Discounting) Let A, B and be two
> agents where A's opinion about B's recommendations is expressed as
> ω^A_B = {b^A_B, d^A_B, u^A_B, a^A_B}, and let x be a proposition where B's
> opinion about x is recommended to A with the opinion
> ω^B_x = {b^B_x, d^B_x, u^B_x, a^B_x}. Let ω^{A:B}_x = {b^{A:B}_x, d^{A:B}_x,
> u^{A:B}_x, a^{A:B}_x} be the opinion such that:"

Defining equations (**transcribed directly from the PDF page image**, not the
mangled `.txt` extraction — the `.txt` reorders sub/superscripts unreliably in
this region; I visually verified against PDF p. 57/58/59):

```
b_x^{A:B} = b_B^A · b_x^B
d_x^{A:B} = b_B^A · d_x^B
u_x^{A:B} = d_B^A + u_B^A + b_B^A · u_x^B
a_x^{A:B} = a_x^B
```

> "then ω^{A:B}_x is called the uncertainty favouring discounted opinion of A.
> By using the symbol ⊗ to designate this operation, we get
> ω^{A:B}_x = ω^A_B ⊗ ω^B_x."

Jøsang states the operator "is associative but not commutative" and that in a
multi-hop trust path "opinion independence must be assumed" — no entity may
appear twice in the same transitive path (internal p. 54 / PDF p. 57).

### 1b. Definition 24 — Opposite Belief Favouring Discounting (internal p. 55 / PDF p. 58)

```
b_x^{A:B} = b_B^A·b_x^B + d_B^A·d_x^B
d_x^{A:B} = b_B^A·d_x^B + d_B^A·b_x^B
u_x^{A:B} = u_B^A + (b_B^A + d_B^A)·u_x^B
a_x^{A:B} = a_x^B
```

Same ⊗ notation, same "your enemy's enemy is your friend" gloss (Jøsang's own
words, internal p. 55).

### 1c. Definition 25 — Base Rate Sensitive Discounting (internal p. 55–56 / PDF p. 58–59)

Eq. (4.101), transcribed from the PDF:

```
b_x^{A:B} = E(ω^A_B) · b_x^B
d_x^{A:B} = E(ω^A_B) · d_x^B
u_x^{A:B} = 1 − E(ω^A_B) · (b_x^B + d_x^B)
a_x^{A:B} = a_x^B
```

where "the probability expectation value E(ω^A_B) = b^A_B + a^A_B·u^A_B."
This variant makes the receiver's *expected trust* (not just belief/disbelief
mass) the discounting scalar, precisely to handle a "stranger in a town of
honest citizens" case where trust is high-base-rate but evidentially
uncertain (internal p. 55, the worked example).

---

## 2. What exactly is discounted, and by what?

**Yes — the discount is a function of the receiver's opinion about the source
agent** (ω^A_B — A's trust opinion about B), and **it is applied to the whole
recommended opinion ω^B_x as a unit**, producing a new opinion ω^{A:B}_x before
that opinion enters any fusion step. This holds across all three variants
(Defs. 23, 24, 25) — the only thing that varies is *how* the trust opinion
ω^A_B is folded in (belief-only, belief+disbelief-flip, or expectation-value
scalar).

Direct textual support, internal p. 54:

> "the effect of A disbelieving that B will give a good advice... A's opinion
> about B's recommendations is expressed as ω^A_B..."

and the worked numeric example (Fig. 4.12, internal p. 55):

> "ω^A_B = {0.1, 0.8, 0.1} discounts ω^B_x = {0.8, 0.1, 0.1} to produce
> ω^{A:B}_x = {0.08, 0.01, 0.91}."

— i.e. a low-trust receiver opinion (b=0.1) collapses an otherwise confident
source opinion (b=0.8) down to almost-total uncertainty (u=0.91) in the
receiver's derived belief. This is a real, working down-weighting mechanism
for an untrusted/unreliable source, applied *per-source, before fusion*.

---

## 3. Anything else bearing on source-reliability weighting?

- **Section 5.2 "Bayesian Networks with Subjective Logic"**, internal p. 64 /
  PDF p. 67, states explicitly that discounting is meant for exactly the
  reliability-of-source use case our draft is contesting:

  > "It is also possible that evidence opinions provided by experts need to
  > be discounted due to the analysts doubt in their reliability. This can be
  > done with the trust transitivity operator¹ described in Sec.4.8"
  > (footnote 1: "Also called discounting operator")

  This passage sits in a discussion of Bayesian networks with multiple
  parent nodes fused into a child, and explicitly separates two knobs:
  (a) **dependence** between sources → handled by choosing averaging vs.
  cumulative fusion (internal p. 64), and (b) **reliability** of a given
  source → handled by discounting *before* fusion (same paragraph). This is
  the clearest single passage tying discounting to "source reliability" in
  Jøsang's own words.

- **No "reputation system" as such is in this document.** `grep -i
  "reputation"` returns zero hits in the whole text. (Jøsang has separate
  published work on reputation systems — e.g. "Beta Reputation System" — but
  it is **not** in this 2013 Subjective Logic draft; do not attribute
  reputation-systems content to this source.)

- **No "base-rate manipulation" discussion** in the adversarial-gaming sense
  (i.e., nothing about a source strategically manipulating its stated base
  rate to game fusion or discounting). The only "base rate" material is the
  base-rate-sensitive discounting variant (Def. 25, §2 above) and unrelated
  usage of base rates in probability-expectation calculations elsewhere in
  the book. `grep -i manipulat` returns one unrelated hit (Dirichlet
  distribution "analytical manipulations," internal-math sense, not
  adversarial).

---

## 4. The Zadeh / conflict critique — addressed, but NOT in the "many weak
confirmations outvote one strong counterexample" framing

Jøsang does discuss "Zadeh's example," but in the context of **Dempster's
rule / the Belief Constraint Operator (§4.9)**, not the cumulative fusion
operator (§4.7). Location: internal pp. 57–58 (PDF pp. 60–61), inside §4.9.2
"Examples," the "Going to the Cinema" worked example.

Verbatim (spans the PDF-p.60→61 page break, confirmed via `pdftotext -layout`
so the sentence isn't an extraction artifact):

> "The belief mass values of Alice and Bob in the above example are in fact
> equal to those of Zadeh's example [26] which was used to demonstrate the
> unsuitability of Dempster's rule for fusing beliefs because it produces
> counterintuitive results. Zadeh's example describes a medical case where
> two medical doctors express their opinions about possible diagnoses, which
> typically should have been modelled with the averaging fusion operator
> [11], not with Dempster's rule. In order to select the appropriate operator
> it is crucial to fully understand the nature of the situation to be
> modelled. The failure to understand that Dempster's rule does not represent
> an operator for cumulative or averaging belief fusion, combined with the
> unavailability of the general cumulative and averaging belief fusion
> operators for many years (1976[24]-2010[11]), has often led to
> inappropriate applications of Dempster's rule to cases of belief fusion
> [14]."

Bibliography entry [26] confirms this is the classic paradox source: "L.A.
Zadeh. Review of Shafer's A Mathematical Theory of Evidence. AI Magazine,
5:81–83, 1984" (line 6114 of the `.txt`; not independently page-checked in
the PDF since it's a standard bibliography entry, not a claim needing
verbatim verification).

**What this means for sub-question 4:**
- Jøsang **does** engage with the canonical Zadeh conflict paradox (two
  near-certain, conflicting opinions combined via Dempster's rule/normalized
  conflict-discard producing an implausible result).
- His resolution is **operator-selection**, not a fix to fusion mass
  accounting: he argues Zadeh's actual scenario is a case for the
  **averaging** operator (or would need the belief-constraint operator, which
  is for *preference combination*, not *evidence fusion*), and that applying
  Dempster's rule to an evidence-fusion problem was the original error, not a
  flaw in SL's own fusion operators.
- **I found no passage discussing the specific framing "many weak/repeated
  confirmations can outvote a single strong counterexample" as it would apply
  to the cumulative fusion operator's mass-accumulation behavior.**
  `grep -i "outvote\|outweigh\|counterexample"` returns zero hits anywhere in
  the document. This is a genuine textual silence, not a paraphrase of
  something present — if your draft's Zadeh-style critique is specifically
  about repeated/duplicate evidence swamping a single strong dissent within
  cumulative fusion (as opposed to the classic two-conflicting-experts
  Dempster paradox), **this text does not address that scenario.**

---

## 5. The narrower, decisive question: is source reliability a *revisable
claim subject to adjudication*, or a scalar parameter supplied to an operator?

**Grounded answer: it is a scalar parameter supplied to the operator, full
stop — the text gives no mechanism for revising/adjudicating it as a claim in
its own right.**

Textual basis:
- In all three discounting definitions (§1a–1c above), ω^A_B ("A's opinion
  about B") is simply **an input** to the ⊗ operator — an opinion A is
  assumed to already hold. Nothing in Section 4.8 describes how ω^A_B itself
  gets formed, contested, updated in light of new evidence about B's
  reliability, or reconciled when two parties disagree about B's
  trustworthiness. It is treated exactly like any other opinion the framework
  manipulates — combinable via the *same* fusion/discounting machinery if you
  chose to apply it to trust-about-B itself, but the document does not
  discuit adjudication of conflicting trust-claims as a distinct problem.
- The base-rate-sensitive variant (Def. 25) explicitly flags a **known
  problem** with propagating an uncertain trust opinion through a long path
  ("this potential problem could be amplified as the trust path gets
  longer") and offers only a hand-wavy mitigation ("a safety principle could
  therefore be to only apply the base rate sensitive discounting to the last
  transitive link. There might be other principles that better reflect human
  intuition for trust transitivity, but **we will leave this question to
  future research**," internal p. 56 / PDF p. 59). This is Jøsang's own
  admission that the discounting-scalar approach has known limits and that
  he has not solved the deeper trust-adjudication problem — he flags it as
  future work, not as something SL already handles.
- Nowhere does the document describe a claim-level representation of "source
  B is unreliable" that could itself be retracted, superseded, or contested
  by a third party's evidence — the whole apparatus is opinion-algebra over
  scalars/vectors (b, d, u, a), not claim-graph adjudication.

**So: the narrower claim — that SL treats source reliability as a supplied
scalar parameter rather than a revisable, adjudicable claim — is supported by
the text as far as it goes, and Jøsang's own "future research" hedge (internal
p. 56) is good primary-source backing for it.** But this is a different,
much more defensible claim than "cumulative fusion gets provenance-weighting
exactly backwards" — SL is not *ignorant* of source reliability (§1–3 refute
that), it just handles it via a pre-fusion scalar-discount step rather than a
first-class, contestable claim node.

---

## 6. Extraction-reliability note

The `.txt` extraction of the equation blocks in §4.8 (roughly lines
5257–5486 of the `.txt` file) reorders sub/superscript tokens in a way that
is misleading if read literally (e.g. it renders Def. 23's second equation as
"d = bAB d xB" on its own disconnected line, dropping the ⟨A:B⟩ superscript
grouping that's visually obvious in the PDF). **All equations quoted above
were transcribed from the PDF page images (PDF pp. 57–59), not the `.txt`
file.** If re-verifying, read PDF pages **57, 58, 59** directly (internal pp.
54, 55, 56) — the typeset math is completely legible there; do not trust the
`.txt` for this region. The Zadeh passage (§4) is NOT garbled math but *is*
subject to a reading-order artifact: `pdftotext` places Table 4.8/4.9 (which
visually sit mid-page) between two halves of one sentence that spans the
page break internal-p.57→58 (PDF p. 60→61); I confirmed with
`pdftotext -layout` that the sentence is intact and not evidence of
corruption — just a table interposed in extraction order.

---

## Section/page index (for direct re-check)

| Item | Internal page | PDF page |
|---|---|---|
| §4.7 "Fusion of Multinomial Opinions" heading | 52 | 55 |
| §4.7.1 Cumulative Fusion Operator / Theorem 3 | 52–53 | 55–56 |
| §4.7.2 Averaging Fusion Operator / Theorem 4 | 53 | 56 |
| §4.8 "Trust Transitivity" heading, Fig. 4.11 | 54 | 57 |
| §4.8.1 Def. 23 (Uncertainty Favouring Discounting) | 54 | 57 |
| Fig. 4.12 worked numeric example | 55 | 58 |
| §4.8.2 Def. 24 (Opposite Belief Favouring Discounting) | 55 | 58 |
| §4.8.3 Def. 25 (Base Rate Sensitive Discounting), "future research" hedge | 55–56 | 58–59 |
| §4.9 "Belief Constraining" / Dempster's-rule extension heading | 56 | 59 |
| §4.9.2 "Examples," Zadeh passage | 57–58 | 60–61 |
| §5.2 discounting-for-expert-reliability remark + footnote | 64 | 67 |
| Bibliography [26] Zadeh 1984 | — (Bibliography) | ~69 (not independently PDF-verified) |

## Grep audit trail (what I searched, so absence-claims are checkable)

Ran against the full `.txt` (6115 lines, whole document, nothing truncated):
`discount`, `reputation`, `zadeh`, `conflict`, `outvote|outweigh|counterexample`,
`unreliab|reliability|reliable`, `manipulat`, `double.count|duplicat|independent
evidence|same source|multiple observations|repeated observ`, `weigh|weighted`,
`multiple sources|different sources`. All hit-lines were read in context (not
just counted). Zero-hit terms (`reputation`, `outvote/outweigh/counterexample`,
adversarial `manipulat`) are genuine textual silences, not missed greps.
