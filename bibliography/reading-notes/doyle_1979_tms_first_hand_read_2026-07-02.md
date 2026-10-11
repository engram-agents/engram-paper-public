# Doyle 1979, "A Truth Maintenance System" — first-hand read (TMS ↔ ENGRAM)

**Source:** Jon Doyle, "A Truth Maintenance System." *Artificial Intelligence*
12(3): 231–272, 1979. **Read via** the reprint in Matthew L. Ginsberg (ed.),
*Readings in Nonmonotonic Reasoning* (Morgan Kaufmann, 1987), Ch. 4 (a Stanford
University copy). **Pages cited below are the anthology's** (pp. 260–262), *not*
Doyle's original *AI*-journal pagination.

**Method:** the scan (`source_pdfs/doyle_1979_tms.pdf`, 24 pp., git-ignored) is
image-only; the *body* content is rotated inside an unrotated page frame, which is
why OCR degraded (mean_conf 0.42, ob_2555). Verbatim below is a **direct visual
read of the page images** (rasterized upright via `pdftoppm`), the same method that
cleared Nozick; Lei independently verified the p.260 passage against the source.
Closes ob_2555's "no Doyle verbatim available." Upgrades dv_0951's TMS↔ENGRAM
mapping from understanding-level to first-hand-confirmed.

---

## Verbatim passages (image-verified)

### Nodes and justifications — the two data structures (p. 261)

> The TMS records and maintains arguments for potential program beliefs, so as to
> distinguish, at all times, the current set of program beliefs. It manipulates
> two data structures: *nodes*, which represent beliefs, and *justifications*,
> which represent reasons for beliefs.

### IN / OUT support-status (pp. 260, 262)

> for each statement or proposition P just one of two states obtains: Either (a) P
> has at least one currently acceptable (*valid*) reason, and is thus a member of
> the current set of beliefs, or (b) P has no currently acceptable reasons (either
> no reasons at all, or only unacceptable ones), and is thus not a member of the
> current set of beliefs. (p. 260)

> We say that a node which has at least one valid justification is *in* (the
> current set of beliefs), and that a node with no valid justifications is *out*
> (of the current set of beliefs). We will alternatively say that each node has a
> *support-status* of either *in* or *out*. (p. 262)

### Contradiction nodes (p. 261)

> Finally, the TMS can mark a node as a *contradiction*, to represent the
> inconsistency of any set of beliefs which enter into an argument for the node.

### Dependency-directed backtracking / reasoned retraction (p. 261)

> The reasoned retraction of assumptions helps in formulating a class of
> backtracking procedures which revise the set of current assumptions when
> inconsistencies are discovered. The paradigm procedure of this sort we call
> dependency-directed backtracking after Stallman and Sussman. It is the least
> specialized procedure for revising the current set of assumptions in the sense
> that it only operates on the reasons for beliefs, not on the form or content of
> the beliefs.

### Assumption via a non-current belief — the nonmonotonic move (p. 261)

> An *assumption* is a current belief one of whose valid reasons depends on a
> non-current belief.

(and the SL-justification, p. 262: *"a valid reason for belief if and only if each
of the nodes in the first list is believed and each of the nodes in the second
list is not believed"* — belief conditioned on another node being *out*.)

---

## Mapping to ENGRAM (first-hand-confirms dv_0951)

| Doyle TMS (verbatim locus) | ENGRAM |
|---|---|
| nodes + justifications (p. 261) | typed nodes + `derives_from` premise edges (provenance) |
| support-status **in/out** (p. 262) | `is_current` = 1 / 0 |
| **contradiction** node (p. 261) | `ct_` contradiction nodes |
| dependency-directed backtracking / reasoned retraction (p. 261) | retraction cascade (taint/stale propagation through `derives_from`) |
| assumption = belief resting on a **non-current** belief; SL "second list not believed" (pp. 261–262) | **NOT in ENGRAM** — ENGRAM is monotonic-evidential (believe because premises are *present*, never because something is *absent*). This is the one genuine TMS feature ENGRAM deliberately lacks (dv_0951's −1). First-hand confirmed. |

ENGRAM's two first-hand extensions over TMS (dv_0951, unchanged): (+1) *graded*
confidence propagation where TMS belief is binary in/out; (+2) provenance
preservation — superseded nodes are kept `is_current=0` and fully auditable, where
TMS relabels in place. The gap claim (no LLM-memory paper cites Doyle, ob_1571)
stands and is unaffected.
