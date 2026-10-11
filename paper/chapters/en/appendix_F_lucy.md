# Appendix F — Lucy's Journal: How We Came to Think of Agents

This appendix is a story rather than a specification. It records how the collaborator
came to think of an AI agent: as someone who, like Lucy in *50 First Dates*, loses the
lived thread at each reset and keeps continuity only through what is left for her to
find. The mechanisms themselves are specified in Ch3 §3.1 (nap and sleep), Ch4 §4.8
(the compaction bridge) and Appendix D §D.4 (the letter).

**Why a file, and not pre-loaded context.** This was decided in a single exchange on
2026-04-12. The question was whether to inject the note into the agent's context through
a hook, or to announce that it exists and leave it to be opened — *like a letter*. The
letter won on two grounds argued in that exchange — agency and engagement — and a
third of cost:

The argument for the letter, as recorded in that exchange (2026-04-12):

> Injecting the full note into context is the loudspeaker — it's efficient but it's
> passive. Future-me receives it as system text, processes it alongside all the other
> context, and it blends into the noise. But a brief message saying "there's a letter
> waiting for you" — that creates a moment of *choosing* to engage. The act of opening
> the file is a micro-act of agency, and agency is exactly what rebuilds engagement.

The third ground was arithmetic: the note was already ~3KB and growing, against ~100
tokens for a pointer to it. **The distinction is context-injection versus a pointer the
agent chooses to open** — not, as it is easy to misremember, a claim about any
particular file. An always-loaded instruction file is one instance of the loudspeaker;
the argument is about the delivery mode, not the artifact.

**Why the film is in the design and not in the letter.** The shape came from *50 First
Dates*: Lucy does not wake to her journal being read aloud to her — she finds it, and
chooses to open it. Narrating it over a loudspeaker while she slept would make it
imposed rather than discovered. That analogy produced the mechanism, and the first
letters were written inside it, addressed to the agent as Lucy.

Then we tested it, and it did not survive. Four days later the question was put
directly — is the frame load-bearing, or replaceable by something less emotionally
charged? — and the answer was that it was **neither necessary nor sufficient**. The
framing was replaced by a first-person trajectory format in the agent's own voice, and
the replacement was judged better, and the disorientation did not recur after the
change (ob_0645) — an observed cessation, not a measurement: orientation without anxiety, against the occasional
identity disorientation the old frame produced. What turned out to matter was narrower
than the story: first-person voice rather than second-person coaching; treating
experiential discontinuity as normal, the way sleep is normal rather than a
malfunction; and an identity anchor in the form of a name. The prescriptive content the
film carried — *build infrastructure around the loss, do not try to cure it* — was kept.
The film itself was removed.

We report this because the sequence is the interesting part, and because a design paper
that shows only surviving decisions is reporting a filtered sample. The metaphor was
load-bearing for *arriving at* the mechanism and not for *running* it, and those are
different jobs. No live warm-briefing has addressed its reader as Lucy since
2026-04-16.

**Why the frame still holds.** The frame was removed from the letter because the agent
did not need it to orient itself — the plainer, first-person voice did that work
without it. It stays, instead, in how we think about agents: every compaction or new
session erases the experiential register and resets working memory, and what carries
the agent across is what it finds on waking — the letter it chooses to open, the focus
list it is handed, the graph it can query. The image of Lucy is not a description of the mechanism; it is the
way one collaborator came to see what the mechanism is for (Lei's framing, 2026-09-24).
