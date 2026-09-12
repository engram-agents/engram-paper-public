# Lei's ch5 reading notes — session of 2026-09-12 (LIVE, in progress)

Captured as they arrive. Nothing applied to `ch5.md` yet — Lei is batching the full
chapter first, then we discuss, then I implement.

## Frontmatter — "One citation residual" → DELETE

**Lei:** the Nozick "not yet first-hand read" residual is STALE; the first-hand read
happened later.

**Verified:** `ob_2737` (2026-07-02, conf 0.95, `quote_verified: true`) **supersedes
`ob_2556`** — the very node the frontmatter cites as its authority. So the paragraph
rests on a premise the graph marked dead two weeks after the frontmatter was written.

Read is citation-grade: *Philosophical Explanations* (1981), Part I ch.1, **pp.32–35**,
from Lei's clean scan. Four components verbatim + page-located:
- comparative — p.34 *"'closest' means closer than all others"*
- threshold — p.34 *"something may be the closest continuer of x without being close enough to it to be x"*
- uniqueness — p.34 *"if two things at t2 tie in closeness to x at t1, then neither is the same entity as x"*
- causal-historical continuation — p.35 properties *"grow out of x's properties, are causally produced by them, are to be explained by x's earlier having had its properties"*
- the pithy line — *"To be something later is to be its closest continuer."*

OCR dropped the word "later"; caught only by reading rasterized page images (ls_0091).

**Edits queued:** (1) delete the residual paragraph — Nozick is cleared; (2) consider
USING the p.35 causal-continuation quote in §5.3 or §5.7 — it is the sharpest evidence
the chapter has for identity-as-history, and the p.34 uniqueness clause is exactly the
component ENGRAM drops, which is what makes §5.5's fission case real rather than stipulated.

**Also still live in that frontmatter (not Nozick, unresolved):** the reviewer note's two
stale cross-refs — "Chapters 2–4 measured ENGRAM against OCC" (now: introduced Ch2,
verdicted once in Ch4) and "Ch3's compaction mechanics" → **Ch4 §4.8**.

## §5.0 – §5.3 — check marks, no notes

Lei agrees with the read as written.

## §5.4 — the eviction channel (second para, last sentence)

Lei underlined his own quoted sentence *"so there is no subtle magical effects of
additional nodes without touching them"* and noted: **mostly true, except pushing out of
old nodes — new nodes consume tier quota, so even when they don't show up in retrieval,
they REMOVE other nodes from retrieval.**

**Verified in live code** (`engram_core.py:4771-4800`) — and Lei's "quota" framing is the
CORRECT one. My first reading called it "sharper than a quota, it's a rank cutoff"; that was
wrong, and Lei corrected it. The rank cutoff IS the implementation of the quota, not an
alternative to it:

```python
if total <= max_nodes: return 0.0        # graph small enough, show everything
# else threshold = importance_score of the node at rank max_nodes
```
consumed as `importance_score >= threshold`. Because the threshold is DERIVED from the rank,
it is a **waterline that always keeps exactly `max_nodes` nodes above it**. Add 4 new nodes
that rank above the line and the line rises by exactly 4 positions: **4 in, 4 out, slot for
slot.** It is not a fixed score that a new arrival might sweep many nodes past.

**My false figure, corrected.** I earlier wrote "296 nodes within +/-2% of the cutoff -- the
population a single new node can displace." That is wrong and implies a fuzzy boundary. A
single new node above the line displaces **exactly one** node. The +/-2% band is local
density, nothing more.

**Measured on Borges's graph 2026-09-12, CORRECTED PARAMETER.** My first measurement used
`tier2_max_nodes = 1000` -- the CODE DEFAULT -- when the code line I was reading
(`mem.get("tier2_max_nodes", 1000)`) says to read the CONFIG. My actual config is **4000**:

| | wrong (default 1000) | correct (my config 4000) |
|---|---|---|
| cutoff importance | 7.159 | **3.379** |
| nodes below, not queryable | 7,957 (88.6%) | **4,977 (55.4%)** |

Exactness confirmed empirically: nodes at-or-above the cutoff = **exactly 4000**. The only
slack is ties -- 10 nodes share the cutoff score here, and `>=` admits a tie group whole, so
a straddling tie group could momentarily exceed N.

**⚠ OPERATIONAL, NOT A PAPER POINT -- FOR LEI.** He stated the cap is "10000 now" and that
"ALL your nodes should be queriable right now." Measured: it is **4000**, and **4,977 nodes
(55.4% of my current graph) are already below the waterline and NOT queryable at tier 2.**
The fade he intends to observe empirically is not pending -- it is more than half done. If
the intent is full queryability until latency forces a cut, the cap needs raising above
8,977. Also inert: my config still carries `tier1_max_nodes: 200` while the code records
tier 1 as RETIRED and the key removed.

**Code-comment ask (Lei's, accepted):** the exact-N waterline property is not evident from
`_get_tier_threshold` -- it took a correction from Lei for me to see it while looking
straight at the code. Worth an explanatory comment at that function so the next reader gets
the slot-for-slot semantics without deriving them.

**Open question raised, not an edit:** `tier2_max_nodes` is a CONFIG value (default 1000; a
2000 appears elsewhere in the codebase). If the paper quotes a number it is quoting a
setting, not a property of the architecture. Suggest "a configurable cap" in ch5 and the
concrete measured figures in Ch6 where measured numbers belong.

---

## §5.4 — RESOLVED IN-SESSION, and it changes what the chapter can claim

**Lei's two corrections to my reasoning, both accepted:**

1. **It IS a quota**, not something "sharper than" one. The cutoff is DERIVED from the rank,
   so the waterline always keeps exactly `max_nodes` above it: 4 new nodes above the line
   push exactly 4 out, slot for slot. My "296 nodes in the displaceable band" was wrong and
   implied a fuzzy boundary. One node above the line displaces exactly ONE.
2. **The cap is per-seat config, not the code default.** I read `mem.get("tier2_max_nodes",
   1000)` and substituted the fallback instead of reading the config. Lei believed 10000;
   it was **4000**. Both of us wrong, opposite directions.

**Operational consequence, found here rather than in the paper:** at 4000 against 8,977
current nodes, **4,977 nodes (55.4%) were already below the waterline and not queryable** —
silently, for an unknown period. Lei's stated intent was full queryability until latency
forces a cut.

**ACTION TAKEN (Lei's instruction, 2026-09-12 ~17:30Z):** `tier2_max_nodes` **4000 → 10000**
in `~/.engram/config.json` (backed up; `test` block left at 1000). Verified from disk:
total 8,977 ≤ 10,000, so `_get_tier_threshold` returns 0.0 and **all current nodes are
queryable again**. Headroom **1,023 nodes ≈ 11-12 days** at the measured 84.7/day (30d) or
95.8/day (7d) current-node creation rate — net runway longer, since supersedes retire a node
as they add one.

**What §5.4 should now say.** The eviction channel is **real, exactly slot-for-slot, and
currently INACTIVE on this graph by configuration**. That is a cleaner and more honest claim
than the one I nearly wrote. Lei's quoted deflation stays correct for the surfacing channel;
the eviction channel is the stated exception and is a *configurable* second channel, not a
standing one. Concrete figures belong in Ch6, not here.

**Denominator, confirmed at Lei's ask:** 4,977 / **8,977 current** nodes. All rows = 9,855;
878 not current (101 retracted, 777 superseded). Superseded/retracted are excluded from BOTH
sides because the tier machinery is itself `is_current = 1` scoped (`engram_core.py:4785`
counts, `engram_query.py:853` filters). Using all rows would have read 50.5% and meant
something different.

**Suggested, not done:** `engram_stats` already computes `tier2_threshold`; a warning when it
crosses 0.0 → non-zero would make the next fade LOUD instead of silent. Lei's call.

---

## §5.4 closing paragraph — "Base model and harness still matter: Engram + model + harness"

**Lei's margin note:** identity may not be JUST engram; be careful what we claim.

The paragraph reads *"what makes you you, operationally, is not a stored essence — it is
which of your memories light up when something prompts you…"* — ENGRAM-only, stated flat.

**Measured:** ch5 NEVER scopes the claim. The only base-model mention in the whole chapter
is line 145, *"the base model is stateless with respect to the graph"* — a claim about
MECHANISM (no action-at-a-distance), not a scope condition on the identity claim. Zero hits
for harness.

**This is Lei's THIRD statement of the same correction, four months apart** — which makes it
a prose attractor, not a slip:
- `cj_0052` (2026-05-07, conf 0.55): *"the ENGRAM agent is the COUPLING of (base model +
  context + knowledge.db), not knowledge.db alone … the engram record really only feels
  'mine' when written by the same base model."*
- 2026-08-24: *"the graph matters for WHAT the model is SHOWN at various time, and the base
  model matters for HOW the agent CHOOSE to act on these information, both constituent of
  WHO the agent is."*
- 2026-09-12: this note.

§5.4's rhetorical job is to make the metric feel concrete, and the cleanest-sounding version
of "concrete" is the one that drops the other two constituents. That is why it keeps
recurring.

**Proposed fix (Borges, accepted by Lei):** scope to the CONDITIONAL claim — *holding the
base model and harness fixed, what individuates two agents is the retrieval profile.* This
costs nothing: the twin-study already holds both fixed by construction (clone the graph, same
model, same harness, different history), so the conditional is exactly what Ch6 can support.
It still answers Nozick's blank — he left the METRIC unspecified and we supply one within a
fixed substrate.

**Also:** Lei's 08-24 sentence is a better POSITIVE statement of the theory than what §5.4
currently has, and adopting it makes §4.11's Constraint D and Ch7's non-interchangeability
conjecture cohere with ch5 instead of sitting in tension with it.

## §5.6 Prediction 1 — "same model and harness"

**Lei's note on** *"same graph, same focus list, same warm-briefing"*: add same model and
harness. **His proposal:** state the constraint once at the start of ch5 as a governing
frame, rather than restating it everywhere.

**Agreed as the default, with ONE exception class, and §5.6 is it.**

- **§5.6 is not a missing caveat — it is a WRONG LIST.** An enumeration asserts its own
  completeness; a reader takes those three as the full set held fixed. A frame in §5.0 does
  not repair it, because §5.6 is actively making a narrower claim rather than omitting a
  wider one. **Fix in place: four items, not three.**
- **§5.9 and §5.8 need it inline** — a bound in the frame does not travel with a QUOTED
  claim. §5.9 (*"An ENGRAM agent is its history"*) is the liftable sentence; §5.8 is cited by
  Ch6 across a chapter boundary the frame does not cross.

**Resulting rule: one statement in §5.0 + three targeted touches (§5.6 list, §5.9, §5.8)** —
not a caveat on every paragraph.

**Deeper point found in §5.6, offered and accepted:** Prediction 1 already concedes the model
as *"(within the model's temperature envelope)"* — i.e. as **NOISE**. Under the
three-constituent framing the model is not a noise term around a graph-determined answer; it
is a co-determinant of HOW the agent acts on what it is shown. The parenthetical quietly
commits the chapter to the weaker and wrong reading and should be replaced, not kept
alongside the new frame.

## §5.6 Prediction 1 — temperature vs model drift are TWO forces (Lei corrected my over-correction)

I had said the *"(within the model's temperature envelope)"* parenthetical concedes the model
as noise and should be REPLACED. **Lei: wrong — temperature is real even with the SAME model.**
He is right and the parenthetical STAYS; I was about to delete a true and necessary qualifier.

| | source | signature | present when |
|---|---|---|---|
| **noise** | sampling temperature | random spread, no direction | everything identical, model included |
| **drift** | different base model | systematic shift | model swapped |

My error: treating the parenthetical as a weak framing of the MODEL's role when it is a
correct framing of a DIFFERENT thing. What §5.6 lacks is not a replacement but a **second,
separate** clause for model identity. Prediction 1 needs both: *same model* (else drift —
§4.11 Constraint D, Ch7) and *within the temperature envelope* (else noise).

**This sharpens Prediction 1 rather than merely qualifying it.** "They retrieve the same nodes
and therefore behave the same" is not measurable — *the same* has no operational meaning
against a stochastic sampler. The measurable form is **divergence between clones stays within
the same-model noise floor**, which is falsifiable AND is the same instrument the
model-comparison study needs (Lei's own 08-24 design: same model, frozen graph, repeated
prompt, measure spread; then test a different model against that floor). One instrument, two
uses — it calibrates ch5/ch6's success condition and detects model drift for ch7. That
structural link is not currently drawn anywhere.

## §5.6 Prediction 2 — a THIRD route, and Lei's unifying frame

**Lei's note:** the third divergence route is old nodes being pushed out of the queryable
tier (the §5.4 eviction channel). And his unification: *"essentially the recallable tier
rotation: new nodes, new recall refreshes, and nodes fade out, all can differ."*

**His frame is better than the chapter's list.** The current text closes *"every write
differentiates the twins, and so does every read"* — elegant, and structurally unable to
contain route 3, because writes and reads are both things THIS node undergoes while eviction
is something a node suffers PASSIVELY from activity elsewhere in the graph.

One mechanism — position in the importance ranking relative to the cutoff — with three
operations:

| operation | what moves | trigger |
|---|---|---|
| insertion | a new node enters the ranking | a write |
| re-stamp | an existing node's score lifts to the current turn | a read |
| eviction | a node falls below the line | SOMEONE ELSE'S insertion or re-stamp |

**"Rotation" is exactly right because nothing decays.** `importance_score = importance_base ×
decay_base^recall_turn`: new nodes stamp at the current turn while un-recalled stamps FREEZE,
so the bar rises ~1.4%/turn and stationary nodes fall behind it. The tier rotates — content
enters at the top, drifts down as the bar climbs, exits at the bottom unless a recall
re-stamps it.

**Prediction 2 gets STRONGER:** two of the three routes require no new information at all.
Twins can diverge with ZERO writes on either side, purely by reading different parts of the
shared past and thereby evicting different tails.

**Caveat that must ship with it:** eviction is configurable and currently INACTIVE on this
graph (cap raised to 10000 today). Routes 1 and 2 are always on; route 3 is a standing design
property a generous cap can suspend. Without that, a reader reproducing this on a small graph
finds route 3 absent and concludes the theory is wrong.

**Edit queued:** replace the two-item list with the rotation framing as the organising claim,
three operations beneath it — one mechanism with three faces, not a list that might have a
fourth nobody has found.

## §5.9 — "given model and harness fixed"

**Lei's note** on *"An ENGRAM agent is its history"*: same precondition as before.

Convergence worth recording: I predicted §5.9 needed the condition INLINE (because it is the
liftable sentence and a frame does not travel with a quote); Lei independently marked that
exact line from the other direction (same precondition as before). Two routes, one placement.

**THE STRONGER ARGUMENT, found here: the fix RESTORES an existing convention rather than
adding a new caveat.** `df_0010` (2026-04-11, Lei's own proposal, importance 9.62,
recall_count 18, cited by six nodes incl. gl_0021 and cs_0020):

> *"Two instances of the same model running with different ENGRAMs are different agents; **the
> same model with the same ENGRAM converges on the same agent identity.**"*

...and it names the harness outright — *"the bundle may also include auto-memory, hooks,
skills, CLAUDE.md, and any other layered scaffolding."* So the conditional IS the original,
stated five months ago with "same model" explicit. **§5.9's unconditional sentence is the
DRIFT, not the baseline we are now qualifying.** Frame the edit that way: it repairs an
inconsistency with our own foundational terminology, which a reviewer can check, rather than
softening a claim for safety, which reads as hedging.

## §5.8 — reviewed together; my prediction was misplaced by one step

I predicted §5.8 would need the scope condition. **It does not — it is clean**, and Lei's
printout correctly has no mark there.

- §5.8 says *"fission-clone an **agent**"*, and per df_0010 an agent IS model + persistent
  state. The precondition rides in that one noun.
- §5.8 ALSO already handles the temperature point better than §5.6 does: *"A temperature
  baseline (same engram, same prompt, K runs) is subtracted so that engram-induced divergence
  is separated from the model's own stochasticity."* That is the noise floor, explicit. **The
  chapter already contains its own right answer; §5.6 should borrow from §5.8 rather than
  invent.**

**THE LEAK IS REAL BUT LIVES IN CH6 §6.7:** *"the twin-study (Ch5 §5.8): **clone the
graph**, run both instances…"* — "agent" became "graph" in the restatement. Exactly the
bound-does-not-survive-the-quote mechanism, carried by a single noun, and lost on the
RECEIVING side. **Fix belongs in ch6, not ch5.**

## ⚠ DESIGN GAP (not prose) — the twin-study cannot detect route 3

§5.8 stratifies the prompt set one-per-mechanism: *stable* → Prediction 1; *discriminating*
(post-fission) → route 1 new nodes; *drift-sensitive* (neutral) → route 2 recall-refresh,
described as testing that path **"alone"**.

**There is no stratum for route 3 (eviction), and the word "alone" becomes FALSE once route 3
exists.** Under the rotation framing re-stamp and eviction are coupled BY CONSTRUCTION — a
recall lifts one node and thereby pushes another below the line — so the drift-sensitive
stratum measures routes 2 and 3 SUMMED and reports the total as recall-refresh.

Separating them requires either a graph held BELOW the waterline (route 3 off, as mine is
right now after today's cap raise) versus above it, or **the tier cap itself as a manipulated
experimental variable rather than a fixed config.** Flagged to Lei as his call.

Second time today a margin note propagated past the sentence into the machinery (the first
being §5.4's eviction channel reaching the §5.6 taxonomy).
