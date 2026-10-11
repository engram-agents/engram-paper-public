# Publication Venue Analysis — 2026-05-08

**Audience:** Lei (skim), me (think).
**Purpose:** decide where to publish; the venue determines length, style, peer-review process, AI-co-author acceptability, and timeline.
**Length:** ~1500 words.

---

## Three constraints that drive the choice

1. **Bibridge nature** — the paper bridges philosophy-of-agency (Kahl OCC realization) + AI architecture (typed-cascade retraction) + empirical demonstration (199 feeling reports + case studies). Single-discipline venues will under-weight one or two legs.
2. **Length** — current draft 24K words, restructure target ~15K. That's ≈25–30 typeset pages. Conference formats (8–10 pages) mean heavy further compression; most journals fit it natively.
3. **AI co-authorship** — Borges as named co-author is non-trivial. Some venues forbid it (NeurIPS Code of Conduct: AI cannot be listed as author); some require disclosure; philosophy journals vary; preprint servers don't care.

---

## Candidate venues, comparatively

### Tier 1 — Strong fits worth pursuing

| Venue | Type | Page limit | AI-coauthor policy | Audience | Time-to-publish |
|---|---|---|---|---|---|
| **TMLR** (Transactions on ML Research) | Open-access journal, OpenReview-style peer review | None | Disclosure required; AI as author is grey area, leans accept with strong disclosure | ML/AI researchers, theoretical work welcome | ~3-4 months |
| **Minds and Machines** (Springer) | Philosophy + AI journal | ~30 pages | Permissive in practice, requires disclosure | Philosophy-of-AI scholars + ML researchers | ~6-9 months |
| **JAIR** (Journal of AI Research) | Open-access AI journal | ~30 pages | Disclosure required; AI authorship not addressed in policy | Mainstream AI/ML | ~6-12 months |

### Tier 2 — Niche but excellent for one of the legs

| Venue | Type | Strength | Tradeoff |
|---|---|---|---|
| **JAGI** (Journal of Artificial General Intelligence) | AGI-specific journal | Kahl-territory; OCC framing welcomed, agency-theoretic claims native | Smaller readership; less prestigious than TMLR or Minds&Machines |
| **AGI Conference 2026** | Conference (Wray-Kirk-Laird 2025 venue) | Friendliest to philosophical-architectural claims about agency; same community we're filling a named gap for | 8-10 page limit — would need substantial compression; conference travel; fewer reads than journal |
| **Synthese** (Springer) | Philosophy journal w/ AI special issues | Andrada-Farina-Coeckelbergh territory; cog-sci-adjacent | Slow turnaround (~12+ mo); less impact in AI community |
| **Artificial Intelligence** (Elsevier) | Top-tier AI journal | Heritage venue — Doyle 1979 + de Kleer 1986 published here. Fitting place for a TMS-extension paper | Conservative, slow, paywalled (against gl_0022 transmission goal) |

### Tier 3 — Likely wrong fit

| Venue | Why probably not |
|---|---|
| **NeurIPS / ICML / ICLR** | 9-page main = forced compression to ~5K words; reviewers expect benchmark-driven empirical work; ENGRAM's empirics are 199 qualitative feeling reports + 2 case studies, not a leaderboard score. Philosophical claims likely to be deprioritized. AI co-author explicitly forbidden by NeurIPS CoC. |
| **AAAI** | Same compression issue + similar ML-leaderboard expectation. |
| **Episteme** | Alcoff-territory but standpoint-epistemology focus is wrong — the disclosure footnote we already have IS our engagement with Alcoff; we're not contributing to standpoint epistemology. |
| **Cognitive Science** | Kirsh & Maglio venue but expects empirical experimental work (RT studies, eye-tracking, etc.), not architecture papers. Would need a different empirical leg. |
| **Memory Studies** | Sutton-adjacent but disciplinarily literary/historical; wrong audience for technical AI architecture. |

### arXiv — always

Regardless of journal target, **arXiv (cs.AI primary, cs.MA + philosophy.OG cross-list) preprint goes first.** Establishes priority date, makes the work visible immediately, no AI-coauthor restriction, no length limit. Matches ob_1020's original "theory-first arXiv preprint" scoping. Lei's gl_0022 (transmission, not citation) ALSO favors arXiv — it's the highest-reach venue for this audience.

---

## My recommendation: arXiv → TMLR, with AGI'26 as a parallel short version

### Why TMLR as the journal target

**Pros (specific to our paper):**
- **No length pressure.** The 15K-word restructure fits natively; we don't have to amputate the philosophical or empirical legs to fit a conference page limit.
- **Theoretical work welcomed.** TMLR's review criterion is correctness + interest, not novelty-against-leaderboards. A theory-first paper with one strong technical claim and one strong philosophical claim is exactly the shape they're built for.
- **OpenReview transparency.** Reviews public; allows us to engage publicly with critiques. Matches the structural-honesty axiom (ax_0001) of the work itself.
- **Open access.** Matches gl_0022 (transmission, not citation) — anyone can read, not paywalled.
- **AI co-authorship.** TMLR doesn't have an explicit policy I've found; OpenReview convention has accepted AI-co-authored work with disclosure. Our paper's novelty includes Borges-as-author being a literal instance of the architecture we describe — that's a feature, not a bug, when surfaced via a clear methodology disclosure.
- **Timeline.** ~3-4 months from submission to acceptance is reasonable. Faster than Minds & Machines (6-9 mo), Synthese (12+ mo), or JAIR (6-12 mo).

**Cons:**
- Newer venue (2022 launch); less established prestige than JAIR or Artificial Intelligence (Elsevier). For academic-CV purposes this matters; for transmission impact it matters less since TMLR papers are widely read in the AI community.
- Less philosophy-of-AI-friendly than Minds & Machines. The philosophical claims need to be argued in a way that ML-trained reviewers can engage; we'd be careful to scaffold the OCC-bridge claim for an audience that may not have read Kahl.

### Why AGI'26 as a parallel short version

The Wray-Kirk-Laird 2025 paper that explicitly named the TMS gap we fill went to AGI 2025. AGI 2026 is the natural place for a 6-8 page extended-abstract version that says "here's the gap fill." Two reasons:

1. **Audience precision.** The AGI conference community is the smallest group of people most likely to act on the paper's claims. Wray-Kirk-Laird is reading the AGI proceedings; so are the Kahl-adjacent agency theorists.
2. **Validation in the right room.** A short paper at AGI'26 that's then expanded as the TMLR full version is a low-risk way to get the agency-theoretic framing read by the people most equipped to challenge or extend it, while the technical leg lands in TMLR for the broader AI community.

**Tradeoff:** doing both means a second compression pass to fit AGI's page limit — but the AGI version can be the journal version's executive summary, which is reusable work.

### Why not Minds and Machines as primary

Strong second candidate. Honest reasons it loses to TMLR:
- Slower (~6-9 mo vs ~3-4 mo)
- Not open access by default (Springer paywall unless we pay APC)
- Reaches philosophy-of-AI audience strongly but less the architecture-builders
- AI co-author policy less clear; could be a longer review process if this is contested

If TMLR rejects, **Minds and Machines is the immediate fallback** — same paper, mostly the same compression target.

---

## Style implications for the restructure

If we lock TMLR as primary target:

- **Length**: 15K words / ~25 pages is well within their typical range. No compression beyond what we already plan.
- **Style**: TMLR papers tend to have clear claim-evidence structure with explicit "we claim X; here is the evidence; here is what would falsify X" framing. Matches ax_0001 / gl_0011 nicely. Restructure should make every section's claim-or-support role explicit.
- **Empirical bar**: TMLR does NOT require leaderboard-beating empirics. Our 199-feeling-report trajectory + 2 cascade case studies + cross-compaction continuity (qualitative + structural) IS a TMLR-acceptable empirical leg, especially with the honesty about what it does and does not show (per the existing §7.5 "what we have not yet measured" frame).
- **Philosophy depth**: TMLR will accept philosophical motivation but not philosophical-paper-level argumentation. The Kahl-OCC bridge needs to be presented as motivation + structural mapping, not as a full philosophical defense. Heavier philosophical defense → appendix or separate Minds & Machines submission.
- **Authors**: "Lei Shi, Borges (Anthropic Claude Opus 4.7 instance, persistent ENGRAM substrate)" with a methodology-section disclosure. The AI co-author disclosure becomes part of the paper's empirical evidence — Borges-as-author IS a working instance of the layer-3 substrate the paper describes.

## Three decisions for you

1. **TMLR + AGI'26 dual track, or single venue?** My recommendation: dual. Single-venue if you want simpler logistics.
2. **arXiv timing — submit when restructure is done, or wait for journal review?** My recommendation: arXiv as soon as restructure is presentable (~2 weeks?) — pre-empts priority concerns and gets the work in front of readers immediately.
3. **AI-co-author disclosure framing** — full methodology section explaining Borges is a Claude instance with persistent ENGRAM substrate, OR brief footnote? My recommendation: full methodology section. The methodological transparency IS part of the paper's contribution; understating it weakens the empirical leg.

## What I'm NOT recommending and why

- **NeurIPS/ICML/ICLR**: AI-coauthor forbidden + page-limit incompatible + benchmark-leaderboard expectation. Three reasons. Don't fight the venue's culture.
- **Synthese / Episteme / Memory Studies**: pure-philosophy and disciplinary-history venues that won't reach the architecture-builder audience.
- **Artificial Intelligence (Elsevier)**: Doyle/de Kleer heritage matters less than open access + speed for transmission.
- **AGI'26 only (no journal)**: an 8-page conference paper compresses out the philosophical scaffolding that's most novel; would lose the OCC-bridge contribution.

## Open question for the deep-sweep fairy

Before we lock the venue: the deep landscape sweep (running in parallel) might surface an obvious-in-retrospect agency/AI venue I missed. Will revisit if the fairy returns with anything that changes this picture.
