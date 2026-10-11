# Fresh-reader review rubric (final, part of #55)

The last review pass on the paper, after the content rounds converge. A reader with
no ENGRAM knowledge reads the rendered paper once, linearly, and reports how it reads
for an average researcher in the AI-agent-memory domain. Persona: `fresh-reader-persona.md`
(the agent-instructions file of the run). Input: the rendered paper only, one section
per turn, delivered by `tools/fresh_reader_run.py`.

## Sources this rubric borrows from (re-checked 2026-09-23)

- NeurIPS reviewer form (2025): four 1–4 scores, each labelled 4 excellent / 3 good /
  2 fair / 1 poor — Quality, **Clarity**, Significance, Originality — plus Overall and
  Confidence. Clarity is the field this pass wants. The 2023–2024 forms called the same
  field Presentation; both names appear in this repo and mean this score.
- ACL Rolling Review form: Paper Summary, Strengths, Weaknesses, Comments, plus
  Soundness (1 Major Issues – 5 Excellent) and Excitement (1–5); clarity is graded
  inside Soundness ("does it clearly state scientific claims"), not as its own score.
- TMLR's two acceptance questions: "Are the claims made in the submission supported by
  accurate and convincing evidence?" and "Would some individuals in TMLR's audience be
  interested in the findings of this paper, and does the paper communicate those
  findings clearly to its intended audience?" The second names the audience and the
  communication standard explicitly.
- Retell protocols from usability testing: the reader retells each section in their
  own words; a section that cannot be retold was not understood.

None of these is a readability rubric on its own. This one composes them: the
per-section retell and logs from the usability tradition, the end-of-paper score from
the NeurIPS Clarity field, the audience question from TMLR.

## Protocol: one linear read, logging as you go

Read start to end, once, in order. Do not skip ahead. At every section boundary,
before the next section arrives, write:

1. **Retell** — two sentences, your own words: what this section claimed and why it
   is here. If you cannot, write "could not retell" and say where you lost the thread.
2. **Undefined at first use** — every term, acronym, or made-up name or ID you met
   without a definition you could point to earlier in the text, unless it is standard
   in the field. Quote the sentence.
3. **Read twice** — sentences or paragraphs you had to re-read to parse. Quote them.
4. **Already said** — anything you recognised as a restatement of an earlier passage.
   Cite both locations. Say whether the repeat helped or cost you.
5. **Open questions** — what you expected the paper to answer here and it did not.
   When a later section answers one, say so there ("answers the §X question").
6. **Hand-off** — did the end of this section tell you why the next one comes next?
   Yes / no / partly.

The driver appends these six items to every section turn, so the reader sees them
beside the text rather than having to remember them.

## At the end of the paper

- Whole-paper retell, one paragraph. This is the headline signal: what an average
  reader in the domain takes away.
- Ordering: would you move any chapter? Which, where, and what it would fix.
- Clarity score 1–4 on the NeurIPS scale (4 excellent, 3 good, 2 fair, 1 poor), with
  one sentence of justification.
- Top five edits that would most improve the read, ranked.
- What you still do not understand about the system after reading everything.

## What the reader is NOT asked

Correctness of numbers, novelty, related-work coverage, or whether the claims are
true. Those are the internal rounds' job. This pass measures only the read.

## Output

`paper/review/fresh-reader-<model>-<date>.md`: the reader's log verbatim under a
header with the model id, the harness version, and the paper commit read. The team
reads it as data about the text, not as a verdict on the work.
