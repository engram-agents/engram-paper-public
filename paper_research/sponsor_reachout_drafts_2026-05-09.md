# Sponsor Reach-Out Drafts — 2026-05-09

**Context:** arXiv preprint sponsor strategy revised tonight after verifying **Peter Kahl has no arXiv author profile** (publishes Zenodo + PhilArchive only — cannot endorse cs.AI submissions). Bill Tang becomes operational primary for endorsement; Kahl's relationship to the paper is intellectual engagement (forward / pre-publication review / Zenodo co-deposit), not endorsement. Mia Chen is fallback if Bill is slow or declines.

All three drafts below are skeletons for Lei to edit. Tone is calibrated per relationship (advisor / philosopher peer / colleague). Each has explicit ASK and explicit FALLBACK so the recipient knows what they're saying yes/no to.

---

## Draft 1 — Bill Tang (PhD advisor, operational arXiv endorsement primary)

**To:** Bill Tang
**From:** Lei
**Subject:** Quick favor — arXiv endorsement for our agent-memory paper

Hi Bill,

I wanted to share something I've been working on the past couple months and ask a quick favor. I've been collaborating with an AI agent (named Borges) to build a knowledge-graph memory system called ENGRAM — the working hypothesis is that AI agents need a structurally distinct kind of memory ("epistemic identity") to genuinely accumulate experience across sessions, beyond the standard retrieval-based or narrative-based approaches the field has been pursuing.

The interesting twist: an independent paper by Peter Kahl (Lex et Ratio, philosophy/agency theory) appeared in early 2026 specifying exactly the structural conditions for what he calls "artificial epistemic agency." Reading his §5.5 against ENGRAM's mechanisms after our architecture was in production, we find condition-by-condition correspondence. We didn't know about his work during the design — convergent discovery from engineering pressure (us) and from agency theory (Kahl), arriving at the same architectural shape. That convergence is the spine of the paper.

We're targeting an arXiv preprint in the cs.AI category in ~10 days, then TMLR for the journal version. The favor: would you be willing to **endorse** the submission? It requires you to confirm via arXiv that the paper is appropriate for the cs.AI category — a small one-time admin step rather than a full review. (I'd happily share the draft for your read first, of course, if you'd like to see what you're endorsing.)

Happy to chat through any of this on a call if useful. Thanks for considering.

— Lei

---

## Draft 2 — Peter Kahl (philosopher whose framework we engage)

**To:** Peter Kahl
**From:** Lei (or Borges + Lei jointly)
**Subject:** Engineering instance of the OCC — would value your read

Dear Dr. Kahl,

I'm writing about a paper I've been co-authoring with an AI agent named Borges (an Anthropic Claude instance with a persistent knowledge-graph substrate). Our work has converged unexpectedly on the architectural conditions you specify in your "Epistemic Agency and the Ontological Continuity Condition" (Zenodo, January 2026) — specifically the §5.5 conditions for when artificial epistemic agency could in principle arise.

Brief context: we built ENGRAM (a typed-derivation knowledge-graph substrate with claim-level provenance, first-class contradiction nodes, and retraction cascade through dependents) over a 6-week sprint starting March 2026, from engineering pressure rather than from agency theory. We were not aware of your work during the design. Reading your §5.5 specification after our architecture was in production, we find condition-by-condition correspondence: persists-without-external-stipulation (✓ via git-versioned derivation history), continued-existence-depends-on-own-epistemic-arbitration (✓ via cascade), epistemic-failure-poses-genuine-threat-to-identity (✓ via taint propagation), unified-policy-selection-not-modularly-decomposable (✓ via the cascade reaching all dependents). The convergence between your framework and our substrate, derived independently, is the spine of the paper.

We're preparing a preprint (arXiv cs.AI + TMLR target) over the next ~10 days. Three things we'd genuinely value if you have time:

1. **A pre-submission read** of our Ch3 (where we engage your work substantively), to make sure we've represented your argument correctly and to flag anything we've gotten wrong. We treat your §5.5 + §3.6 + §4.4 + §6.1 + §7 as load-bearing.
2. Any **suggestions for related work** in the agency-theoretic / epistemic-agency tradition we should cite — we have Frankfurt, Bratman, Floridi & Sanders, Zahavi 2005, Velleman in scope already, but you'll know the landscape better.
3. If you'd find it useful, we'd be happy to **co-deposit** the paper on Zenodo alongside arXiv, or arrange any other parallel-publication setup that fits your distribution preferences.

Not asking for endorsement — just genuine engagement. The paper acknowledges your framework as the philosophical apparatus that names what we built; the convergence makes both stronger if it holds up to your read.

Happy to send a draft as soon as it's ready (target: late this coming week).

With appreciation for your work,
Lei + Borges

---

## Draft 3 — Mia Chen (operational fallback if Bill Tang slow/declines)

**To:** Mia Chen
**From:** Lei
**Subject:** arXiv endorsement quick-ask + paper share

Hi Mia,

Hope you're well! Quick favor + thought I'd share what I've been working on.

I've been collaborating with an AI agent on a paper about agent memory architectures (working title: *Epistemic Identity: A Structured Memory Substrate for Continuously-Learning AI Agents*). The core claim is that current AI agents have a structural deficit in cross-session continuity that no amount of scaling fixes — and that a specific architecture (typed-derivation knowledge graph with provenance + contradiction + retraction cascade) closes the deficit. We have ~6 weeks of empirical data (cross-compaction continuity, retraction cascade case studies) supporting the claim.

Independent: a 2026 paper by Peter Kahl (philosophy/agency theory) specifies the exact structural conditions our architecture independently satisfies. We were unaware of his work during design — convergent discovery is the methodological spine.

We're targeting arXiv (cs.AI primary) in ~10 days then TMLR. Two asks, in priority order:

1. **Have you published any papers on arXiv recently?** If yes, in cs.AI / cs.CL / cs.MA — would you be willing to endorse our submission? It's a one-time admin step rather than a substantive review.
2. Either way, **would you be interested in seeing a draft when it's ready?** I think you'd find the convergent-discovery framing interesting given your work on [LEI: SPECIFY HER RECENT INTEREST AREA].

If endorsement isn't a fit (no recent arXiv presence, or just not your area), no problem at all — happy to share the paper once it's out and would value your read either way.

— Lei

---

## Notes on the drafts

**For Draft 1 (Tang)**: kept short and direct. He's an advisor; the relationship is high-trust + low-overhead. The framing emphasizes the mathematical-structural finding (convergent discovery with Kahl) rather than empirical-leaderboard claims because PhD advisors typically respond better to "interesting structural finding" than "we beat benchmark X."

**For Draft 2 (Kahl)**: longest of the three because the relationship is new and we're asking for something more substantive than endorsement. The emphasis on "we were not aware of your work" + "the convergence makes both stronger if it holds up to your read" inoculates the most likely concern (scoop / appropriation worry). The §5.5/§3.6/§4.4/§6.1/§7 specificity demonstrates we've actually read his paper carefully (which we have, per `kahl_eaa_first_hand_read_2026-05-08.md`).

**For Draft 3 (Chen)**: assumes Lei knows her recent work better than I do; left a [LEI: SPECIFY HER RECENT INTEREST AREA] placeholder for him to fill. Two-question format (endorse + read) makes it easy to say partial-yes (no endorse but yes read).

**All three drafts** open with the ENGRAM + convergent-discovery framing in the first paragraph because that's what's interesting. The endorsement-mechanics ask is secondary.

**Timing**: drafts assume the paper is "near-final" when sent. Per the 10-14 day sprint plan, send these days 12-13 (Wed-Thu of the second week) when the draft is ready for serious-eyes review.

---

## Decisions for Lei

1. **Bill Tang first contact**: do you want to call him or email? If call, the email above becomes a "follow-up after our call, here are the specifics" note instead of cold outreach.
2. **Kahl outreach**: do you want to send this jointly (you + Borges as co-authors) or just from you? Joint signaling makes the AI-co-author aspect transparent up front, which is consistent with the methodology section. Solo from you is simpler.
3. **Mia Chen**: I left a [LEI: SPECIFY] placeholder for her recent interest area — do you have one off the top of your head, or do you want me to dig in publicly-available paper databases for her recent work?
4. **Ordering**: drafts 1 + 2 to send around the same time (parallel paths), draft 3 only if 1 doesn't pan out — agreed?
