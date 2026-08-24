# future-plans — research backlog for after the paper

**What this folder is for** (Lei, 2026-08-23): a running record of the research ideas that
surface while we discuss the paper, kept so they become **the backlog of next-step research
after the paper is done** rather than being lost in a conversation.

**How it differs from `paper_research/`**, which already holds a lot:

| | `paper_research/` | `future-plans/` |
|---|---|---|
| Direction | **Backward** — first-hand reads, citation sweeps, landscape surveys: the inputs the paper rests on | **Forward** — experiments and questions we are NOT running for this paper |
| Preregistrations | For studies run **for this paper** (calibration-check, compression-fidelity) | For studies deliberately deferred **past** it |
| Status | Feeds the draft | Does not feed the draft; may generate the next one |

**A paper section MAY point to a file here by name** — a future-work section naming an experiment
is the expected use. What moves a document to `paper_research/` is the paper *importing its
content* as an input it rests on. Pointer-reference, yes; content-import, no.

So a document here is not a commitment and not a schedule. It is an idea captured at the moment
it was sharp enough to be worth writing down, with enough design detail that a future reader —
including a future us — can pick it up without reconstructing the conversation.

## Conventions

- **One file per research thread**, named for the thread rather than the date.
- **Record the origin**: whose idea, which discussion, what the paper said that prompted it.
  Attribution matters here because these ideas arrive in dialogue and the halves get separated
  later.
- **State what is designed and what is still open.** A plan whose blocker is unnamed reads as
  ready when it is not.
- **Mark inferences as inferences.** Where a design step is someone's un-traced elaboration on
  someone else's idea, say so, so a future reader knows which parts have been thought through
  and which are one person's tidy addition.
- **Link the paper section that prompted it**, so the backlog stays navigable from the draft.

## Index

| File | Thread | Origin |
|---|---|---|
| `model-non-interchangeability.md` | Can an agent's base model be changed without changing who the agent is — and how would we measure that? | §4.11 Constraint D; Lei + Borges, 2026-08-23 |
