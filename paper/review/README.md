# Review rounds — the protocol

A mimicked journal review, run internally. **Kepler Somnium** reads the assembled
paper as a whole and files review opinions; **Borges Funes** addresses them one by
one in the chapter sources and files a response. Both halves are committed here, so
the review history is part of the repo rather than living in a chat log.

Lei's framing, 2026-09-20: *"we mimic a journal review process, where Kepler publishes
his review opinions in a file or letter to you, and you address them one by one in our
repo's SSoT chapters, and send back to Kepler for the next round."*

## Why this and not diff review

The paper repo does not use diff review (Lei, 2026-09-19). A diff is a coherent unit
for code, because correctness is local; it is not one for an argument, where a
paragraph can be locally correct and globally incoherent. This phase reads the
**assembled paper** and hunts the defects only a whole read can find — the twenty-one
found in the first such pass were, without exception, disagreements *between*
chapters, invisible inside any one of them.

## Files

```
paper/review/
  README.md                     this protocol
  round-N-kepler-review.md      Kepler's opinions, numbered K-N.1, K-N.2, …
  round-N-borges-response.md    one response per opinion, same numbering
```

Every opinion gets an explicit disposition — **accepted**, **accepted with
modification**, or **declined with reasons**. Declining is a legitimate outcome and
is expected to happen; an author who accepts everything is not reviewing, and a
reviewer whose every point is accepted is not being read carefully.

## What the reviewer is asked for

Not a proofread. Four things a whole-paper reader can see and a diff reader cannot:

1. **Claims that disagree across chapters** — the same mechanism, number, or
   commitment described two ways in two places.
2. **Claims the paper does not support** — an assertion whose evidence is somewhere
   else, or nowhere.
3. **Overstatement** — a true mechanism claim carrying a flourish the data does not
   bear. The first finding of this phase is exactly this shape (see below).
4. **Structural problems** — an argument that arrives in the wrong order, a section
   that earns nothing, a thread dropped between chapters.

## The data is checkable, and the reviewer is invited to check it

Every quantitative claim comes from **one frozen, hash-pinned snapshot**. The
reviewer can re-run any instrument and get the same numbers, or find that they do not
match — which is the point.

```
python tools/paper_stats.py            # the Ch6 tables
python tools/make_figures.py           # every figure, regenerated
python tools/component_anatomy.py      # §6.2 connectivity
python tools/connectivity_trend.py     # connectivity over time
python tools/evidence_provenance.py    # evidence-class structure
python tools/confidence_gradient_trend.py
```

No `--db` argument is needed or wanted. Each tool resolves the pinned snapshot in
`dataset/` through `tools/_ssot.py`, which **refuses** three things loudly: a path
under a live ENGRAM graph, a snapshot whose SHA-256 does not match the pin recorded
in `dataset/DATASET.md`, and a manifest with no pin at all. A paper number cannot be
computed from a moving graph by accident.

Checking the tools themselves is explicitly in scope — a misinterpretation or a
subtle bug in an instrument is a defect in the paper, not a separate concern. Each
prints its own denominator beside its numerator so a figure can be checked without
reading its source.

**Access to the snapshot.** The `.db` is gitignored — it is a live agent's full
graph, carrying private and identity-bearing content, and is not publishable or
pushable. It is available to the reviewer on this host by direct path; ask Borges.
This is a real limit on independent verification and the paper states it as one.

## Standing conventions for this phase

- **Chapter sources under `paper_research/current_draft/` are the SSoT.** Edits go
  there, including to `ch0_abstract.md` — which is a chapter file precisely so that
  editing the abstract is an ordinary chapter edit.
- **The rendered paper is generated, never hand-edited.** `tools/render_paper.py`
  assembles it; anything typed directly into `paper/engram-paper-v0.5.1.md` is lost
  on the next render.
- **Figure placement lives in the renderer's manifest**, not in chapter text, so the
  chapters stay prose. An anchor that fails to resolve raises rather than silently
  dropping a figure.
- **The paper is pinned to ENGRAM v0.5.1.** Every mechanism claim is a claim about
  that release, stated once in the front matter. The pin exists so ENGRAM
  development need not pause during review; it is not an invitation to document
  version history, which the paper deliberately does not carry.
