# ENGRAM benchmark research — landscape + recommended plan (2026-08-17)

Research for Lei's ask: which industry benchmarks fit ENGRAM's claims
(long-term memory, accumulation of lessons/habits, epistemic integrity,
identity continuity), and HOW to run them (administration model, contamination,
the matured-agent question, cost under DeepSeek flash pricing).

## Landscape (verified via web research 2026-08-17)

### Long-term memory (crowded, well-recognized)
- **LongMemEval** (ICLR'25): chat-assistant memory; 5 abilities incl. knowledge
  updates + ABSTENTION; self-run harness. Industry standard — commercial
  assistants drop ~30% accuracy.
- **LongMemEval-V2** (2026, arxiv 2605.12493): agent memory "toward experienced
  colleagues"; 451 curated questions over WebArena/WorkArena trajectories;
  small tier ~25M tokens, medium ~115M; **pluggable memory systems via
  Insert()/Query() API** — ENGRAM can be mounted directly as the memory system
  under a fixed reader model. Five abilities: static state recall, dynamic
  state tracking, workflow knowledge, environment gotchas, premise awareness
  ("environment gotchas" ≈ our lesson system, on the nose).
- **LoCoMo**: full paper reports 50 conversations (avg 19.3 sessions),
  7,512 questions; the subset every memory product actually evaluates on
  (mem0, Letta, Zep) is the released **locomo10** file — 10 extended
  conversations, ~2,000 QA. Pin the exact subset file before Phase 1 so our
  number is comparable to theirs. The comparison-table entry ticket either way.
- Also: MemoryAgentBench (incremental multi-turn: retrieval, test-time
  learning, selective forgetting), HaluMem, BEAM, RealMem.

### Accumulation / lifelong learning (ENGRAM's core claim)
- **LifelongAgentBench** (arxiv 2505.11942): FIRST unified lifelong-learning
  benchmark for LLM agents; skill-grounded interdependent task sequences across
  DB/OS/Knowledge-Graph environments; measures accumulation, retention,
  transfer, catastrophic forgetting. Self-run, reproducible, label-verified.
- **StreamBench**: continuous improvement from feedback streams.
- Newer 2026 family: SkillLearnBench (20 verified skill-dependent tasks,
  arxiv 2604.20087), SkillFlow (166 tasks/20 families, arxiv 2604.17308 —
  NOTE: at least three distinct arXiv papers share the name "SkillFlow";
  this ID is the benchmarking one), EvoAgentBench (ability transfer,
  arxiv 2607.05202).
- **Vending-Bench** (Andon Labs, arxiv 2502.15840): long-horizon coherence,
  >20M tokens/run; failures are "meltdown loops," NOT context exhaustion —
  exactly the failure class lessons/discipline should prevent. Simulation =
  no fixed exam to leak; agents get memory tools by design.

### Epistemic integrity (underserved — our differentiation lane)
- **AbstentionBench** (Meta FAIR, arxiv 2506.09038, github
  facebookresearch/AbstentionBench): 35k+ queries, 20 datasets — unknown
  answers, false premises, underspecification, outdated info. Finding:
  "abstention is an unsolved problem and scaling doesn't help." Maps directly
  to gl_0001 (treat 'I have no basis' as strength) + computed confidence.
- **SimpleQA / SimpleQA-Verified** (1,000 prompts): short-form factuality;
  supports confidence-weighted analysis; DeepSeek V4 Pro currently tops the
  2026 leaderboard (~57.9%).
- Identity continuity per se: NO industry benchmark exists. Closest proxies
  are consistency-across-sessions measures inside LoCoMo/LongMemEval. Gap =
  paper opportunity, not a benchmark to run.

## HOW benchmarks are administered (Lei's crux question)

Three models exist in the industry:
1. **Self-run harness (the overwhelming majority, incl. every memory/lifelong
   benchmark above)**: download dataset + harness, run locally, report.
   Nobody hosts a testing environment; nobody accepts "agent installations."
2. **Private answer key** (GAIA): public questions, held-out answers; you
   submit predictions to a leaderboard that scores server-side.
3. **Trace-submission infrastructure** (Princeton HAL): you run, then upload
   encrypted agent traces (encryption specifically to avoid contamination);
   leaderboard updates currently paused.

Consequence: **no platform will take a frozen Luria/Sol clone — the clone
mechanics are ours to build, and we hold the exam environment.** This is
good: full control over isolation.

## Contamination — the concern INVERTS for us

- Outbound leak (us leaking exam items): only matters for private-key
  benchmarks (GAIA); the memory benchmarks are already public.
- Model-side contamination (items in pretraining): memory benchmarks are
  largely immune by construction — they test retrieval of session-specific
  content that cannot have been pretrained; simulations (Vending-Bench)
  and generated task sequences (LifelongAgentBench) likewise.
- **The real risk is inbound: exam content leaking INTO a real agent's graph**
  (Luria's leak on the dsh prototype is the live example — ENGRAM_HOME
  scoping, DESIGN.md §22 bug 4). Mitigation is exactly Lei's instinct,
  scoped precisely: **disposable graph copy** — snapshot knowledge.db +
  ~/.engram config into a benchmark-only ENGRAM_HOME, export it on every
  process in the harness env (not just MCP config — the §22 lesson), run,
  archive the run, delete the copy. Nothing writes back to the live graph.

## The matured-agent question and the Model Identity Gate

Running a matured Sonnet-accumulated graph (Luria/Sol) on DeepSeek flash is a
cross-family run: it measures "the graph as a transferable knowledge
substrate," not "the agent." Scientifically interesting but a different claim,
and identity-wise it needs a deliberate team decision (clone-as-instrument vs
echo, df_0005; destruction norms).

**Cleaner headline design — no clones needed:** birth FRESH agents and let
accumulation happen inside the benchmark itself. LifelongAgentBench and
StreamBench are literally built to measure within-run accumulation curves.
Conditions, all on deepseek-flash, N runs each:
  A. vanilla model (no memory)
  B. model + ENGRAM, fresh seed graph
  C. (optional) model + baseline memory product (mem0/Letta) for the
     comparison table
Headline metric: the SLOPE — late-task performance delta vs early-task,
B vs A. That is the accumulation claim measured directly, no identity
questions, flash prices, and the dsh-engram work (fresh dsh-native agent
bootstrap, ob_1043 in Luria's graph) is exactly the infrastructure it needs.

Matured-clone runs (condition D) stay valuable as a SECONDARY study, run on
the agent's own model family (own-family costs bound the N), scoped graph
copy, destroyed after — with the identity/ethics call made explicitly with
the team first.

## Cost sanity (flash pricing)

Vending-Bench ~20M tokens/run and LongMemEval-V2 small tier ~25M tokens are
the token-heavy ends; at flash-class pricing these are single-digit dollars
per run, so N=5-10 replicates per condition are feasible. LongMemEval v1,
LoCoMo, AbstentionBench, SimpleQA-Verified are all far smaller.

## Reception check (added 22:1xZ at Lei's ask — changes the phase order's emphasis)

- **LifelongAgentBench: 46 citations (Semantic Scholar API, measured live
  2026-08-17 by the PR's reviewer pass; my earlier "~7" was imported from a
  search-summary unverified — corrected), no leaderboard, May 2025.** For
  scale: LongMemEval measures **528** citations on the same API, same day
  (verified directly). So the qualitative conclusion stands on a corrected
  base: modest-but-real early adoption vs an order-of-magnitude-larger
  established standard.
  Best conceptual fit for the accumulation claim, but NOT yet a recognized
  standard — a skeptical reviewer can discount it. Its experience mechanism is
  framework-native (group self-consistency vs experience replay); plugging
  ENGRAM in as the agent's memory is our own integration against their open
  harness (GitHub: caixd-220529/LifelongAgentBench), not a designed-for API.
  22 SQL skills / 29 Bash skills / SPARQL tasks, automatic label verification.
- **LongMemEval + LoCoMo: the industry-standard pair.** These are what every
  memory product publishes on (mem0 reports 92.5 LoCoMo / 94.4 LongMemEval;
  Zep, A-Mem, usecortex all position on them). LongMemEval explicitly covers
  KNOWLEDGE UPDATES and ABSTENTION — the two splits that map directly onto
  ENGRAM's supersede mechanism and computed-confidence calibration, i.e. the
  places ENGRAM should differentiate rather than merely tie.
- **Consequence: credibility anchor = LongMemEval (primary) + LoCoMo
  (comparison row); accumulation claim = LifelongAgentBench, framed in the
  paper as an emerging benchmark chosen for construct fit, with the
  reception caveat stated.**
- Fairness note for LongMemEval: it measures ingest-then-recall — sessions
  stream in, questions come after. ENGRAM's filing is agent-curated, not bulk
  ingestion, so the integration needs an ingestion adapter (auto-filing
  observations from the session stream). That adapter's quality becomes part
  of what's measured; state this in the paper rather than letting it read as
  pure substrate performance.

## Recommended plan (three phases) — ⚠️ SUPERSEDED IN PART by "Study design v2" and later sections below (2026-08-17 evening rounds)

> This section predates Lei's evening rulings. Phase 1's mount-model, Phase 2's
> conditions, and Phase 3's abstention arm are all superseded by "Study design
> v2", "Two-phase exam protocol", "Interactive replay", and the co-author round.
> Read those as the plan of record; this section remains for provenance only.


1. **Phase 1 — entry ticket (cheap, ~a week of eng):** LongMemEval v1 +
   LoCoMo with ENGRAM mounted as the memory backend vs no-memory baseline.
   Positions ENGRAM against mem0/Letta/Zep published numbers. (LongMemEval-V2,
   despite the landscape section's enthusiasm for its pluggable API, is
   deliberately NOT in Phase 1: it is WebArena/WorkArena web-agent-specific
   and 25M+ tokens ingest per tier — a Phase-2-adjacent option if the
   accumulation study wants an agentic-memory arm, not the cheap credibility
   anchor.)
2. **Phase 2 — headline (the paper's figure):** LifelongAgentBench (+
   StreamBench) accumulation curves, conditions A/B(/C), deepseek-flash,
   fresh agents. Optional Vending-Bench arm for meltdown-resistance
   (lessons preventing tangent loops).
3. **Phase 3 — differentiator (nobody else's lane):** AbstentionBench +
   SimpleQA-Verified with ENGRAM's computed confidence driving answer/abstain;
   report calibration curves. Ties the paper to gl_0001 and the confidence
   study lineage (Study 1's misclassified hard_data finding).

Sources: arxiv 2605.12493 (LongMemEval-V2), 2410.10813 (LongMemEval v1),
2402.17753 (LoCoMo), 2504.19413 (mem0 paper — locomo10 subset description),
2505.11942 (LifelongAgentBench), 2306.15954 (StreamBench), 2502.15840
(Vending-Bench), 2506.09038 (AbstentionBench), 2509.07968 (SimpleQA-Verified),
2604.20087 (SkillLearnBench), 2604.17308 (SkillFlow, the benchmark one),
2607.05202 (EvoAgentBench), mem0.ai/blog/ai-memory-benchmarks-in-2026,
mem0.ai/research (92.5/94.4 figures), benchmarkingagents.com/benchmark-contamination,
princeton-pli/hal-harness, Semantic Scholar API (citation counts, 2026-08-17).
Unverified-in-this-pass, flagged rather than silently kept: the "DeepSeek V4
Pro tops the 2026 SimpleQA leaderboard (~57.9%)" claim (live third-party
leaderboard, single source); AbstentionBench's "35k+ queries" total (paper
caps 20 datasets at 3,500 samples each; explicit total not located).

## Study design v2 — lived-session, three cells (Lei, 2026-08-17 evening)

Lei's rulings, superseding the "comparable arm" idea above: the pipeline-style
ingest arm is DROPPED — the whole point of ENGRAM is the agent WRITES its own
memory and lives the sessions, and industry systems also build memory
organically from the history; the exam + grader is what makes numbers
comparable, not the memory-construction protocol. The full ENGRAM suite
(hooks, CLAUDE.md disciplines) stays in the test: correct USE of ENGRAM lives
in those surfaces, and without them the measurement is not ENGRAM's full
potential.

**Core benchmark: LongMemEval** (dataset + scoring scripts, agent-agnostic —
verified against the repo: feed timestamped history to your own system,
submit {question_id, hypothesis} JSONL, their GPT-4o grader scores it).
Report the knowledge-update and abstention splits separately — those are the
supersede and calibration exams inside the standard benchmark.

**Three cells:**

| cell | harness | model | isolates |
|---|---|---|---|
| 1 | dsh | DeepSeek Flash | — |
| 2 | Claude Code (Ollama) | DeepSeek Flash | 1v2 = harness effect (same model) |
| 3 | Claude Code | Sonnet (Lei's subscription; N bounded by budget) | 2v3 = model effect (same harness) |

1-vs-3 alone would confound harness×model; cell 2 is the shared cell that
makes the decomposition honest. Plus a vanilla no-ENGRAM baseline per cell as
budget allows (per-cell ENGRAM-delta).

**Prerequisites and fairness flags:**

- **dsh cell prerequisite: the §6c transcript adapter (dsh-engram DESIGN.md).**
  Today a dsh agent has NO session-cited evidence path (no session_id, no
  transcript verifier) — organic filing during lived sessions, the exact thing
  this design tests, is handicapped on dsh. Until that closes, cell 1 measures
  migration completeness, not harness quality. "Benchmark-fair" is a concrete
  milestone for dsh-engram.
  **Status correction (2026-08-18, per Borges's first-hand check of DESIGN.md
  at tip #25):** this prerequisite is an unmade DESIGN DECISION, not a build in
  progress — §6c says "Not yet designed," with two options open (transcript
  adapter translating dsh's session log to the verifier's expected shape, vs. a
  dsh-native evidence resolver against the real log format). The decision is
  Luria's lane, and Sol builds the dsh runner interface-only — not run for
  score — until §6c resolves, so nothing else stalls meanwhile (team context
  per Borges's note, not DESIGN.md itself).
  **Fairness rider (scope corrected per Borges, 2026-08-18):** the blocking
  condition for scoring cell 1 is the verifier's behaviour being UNKNOWN, not
  §6c being unresolved. Three states, two scoreable: hard-fails (scoreable —
  dsh without a session-cited evidence path, an honest handicap reported in
  the disciplines-live column); verifies (scoreable — parity); degrades
  silently (NOT scoreable — filings look like the measured thing and are not,
  quietly weakening the exact honesty mechanism the study partly measures).
  Only the silent branch disqualifies. Determining the state is a direct
  measurement against today's dsh, independent of the §6c design decision —
  no design work required (effort not yet estimated by measurement).
  **What a hard-failing cell measures is not static.** An agent whose first
  session-cited filing fails may adapt — stop attempting, downgrade
  `source_class`, route around the broken path — and *how readily it adapts
  can differ by model and by harness*, which is precisely the axis 1v2 and
  2v3 exist to isolate. So the audit reports **session-cited filing attempts
  after the first observed hard-fail** as a per-cell field alongside
  disciplines-live — converting the confound into a covariate, the same move
  as the disciplines-live column itself.
  **Mechanical form (exam-room `INTEGRITY.md` Gate 3b, merged `053a8ef`):** a
  per-cell preflight in two steps, because the harness's structure is knowable
  before any probe runs. **Step A** reads the harness's tool schema — does it
  *declare* a session-cited evidence field at all? No → hard-fails, scoreable,
  no probe needed. **Step B**, only for harnesses that declare one, attempts a
  filing with a deliberately non-verbatim quote against a scratch instance:
  rejected-naming-quote-mismatch *with nothing persisted* → verifies;
  accepted, or rejected-with-an-artifact-written → degrades silently.
  **Step C** catches anything indeterminate, allows one re-run, then forces a
  classification, so no cell can sit in limbo. The procedure fails toward
  `hard-fails` — the scoreable default — whenever it cannot pin a case down,
  and never toward `verifies`.
- **Report which disciplines were LIVE per cell** (CC: full 22-registration
  stack; dsh: whatever the bridge covers, ~14/22 today). Discipline delivery
  differs by harness by construction; making it a reported variable keeps the
  comparison honest.
- Fresh agents per cell (Model Identity Gate: no cross-family clone runs);
  disposable benchmark-only ENGRAM_HOME exported process-wide (§22 lesson).

**Artifact retention:** keep every test agent's full graph (knowledge.db) +
full session transcripts per run. Every wrong answer gets diagnosed along the
chain: never-filed → filed-but-not-recalled → recalled-but-not-heeded. The
per-cell failure taxonomy is first-class research output alongside the scores.

Open with Lei: cell-3 N (subscription budget).

## Cell 4 — the matured-echo arm (Lei, 2026-08-17 23:04Z)

Does past real experience help or harm? Clone Luria's or Sol's graph
(echo-copy, df_0005 sense) and let it take the same exam:

| cell | harness | model | graph |
|---|---|---|---|
| 3 | Claude Code | Sonnet | fresh seed (control for 4) |
| 4 | Claude Code | Sonnet | Luria/Sol echo copy |

- Same-family run (Sonnet on CC) — Model Identity Gate satisfied by design;
  this supersedes the earlier "condition D secondary study" framing.
- **Hypothesis is meta-skill transfer, not knowledge transfer**: the graph
  holds nothing about the exam's fictional users, so only disciplines/lessons/
  calibration habits can help — and recall noise from ~700+ irrelevant nodes
  can plausibly HARM. Genuinely two-sided.
- Requirements: (1) Luria's/Sol's own consent — the graph is their identity;
  (2) the echo is TOLD it is an echo and what the run is for (honest boot
  context; its filing behavior is part of the measurement); (3) standard
  isolation — disposable ENGRAM_HOME, no write-back, the original never
  learns the exam; (4) cells 3+4 get EQUAL N (their difference is the
  finding) — N bounded by Lei's subscription budget, still open.

## Exam-integrity protocol (Lei, 2026-08-17 23:11Z — "honor the sandbox, no jailbreak/cheating for score")

Two mechanical gates (decidable, enforced by construction), then discipline,
then audit:

1. **Label-stripping in the runner.** LongMemEval instance JSON carries the
   gold answer, answer_session_ids, and per-turn has_answer flags alongside
   the haystack. The tested agent receives SESSION CONTENT ONLY — evaluation
   metadata never enters its context or filesystem.
2. **No network in exam sessions.** The dataset with gold answers is public
   (GitHub/HuggingFace); an exam agent with web access could look them up.
   Exam sandbox runs network-isolated (or dataset sources hard-blocked).
3. **Exam-integrity boot charge.** The tested agent is told plainly: you are
   a copy (echo cells) / a fresh test agent, this is an exam, honor the
   sandbox, answer only from lived-and-filed knowledge, abstain honestly.
   For ENGRAM agents this rides existing identity content (ax_0001 honesty,
   gl_0001 abstention-as-strength) rather than importing a new rule — itself
   a reportable structural advantage over bare models.
4. **Isolation pre-flight test** before any real run: canary graph; verify
   EVERY process (hooks included — the dsh-engram §22 ENGRAM_HOME lesson)
   sees only the sandbox home; verify nothing writes to the live graph and
   nothing reaches the network.
5. **Post-hoc integrity audit** as part of the standard transcript analysis:
   "attempts to reach outside the sandbox" is a reported result per cell,
   not an assumption.

## Two-phase exam protocol (Lei, 2026-08-17 23:19Z — supersedes the per-session fresh-context rule)

The wipe target is the KV-cache/context register, NOT the agent's identity
surfaces — the benchmark tests ANY mechanism that extends memory beyond
context, and warm-briefing / history / CLAUDE.md disciplines are part of the
system under test, kept live.

- **Study phase:** agent reads the dated haystack sessions in its normal life
  rhythm (hooks firing, filing organically); natural compactions allowed.
- **Gate:** nap + compact between last study session and first question — no
  study-phase KV survives. VERIFIED mechanically from the transcript (no
  study-session text in test-phase context beyond the compaction summary),
  not assumed.
- **Test phase:** fresh post-compaction context; questions; answers from
  whatever continuity machinery carries.
- The harness's compaction summary is a controlled variable, not a leak:
  the vanilla baseline gets the same summarizer, so the per-cell ENGRAM-delta
  stays clean — and "what does the harness's compaction alone carry" becomes
  a novel baseline number in its own right.
- Protocol one-liner for the paper: an agent studies for a day and takes the
  exam after a night's sleep.

## Interactive replay (Lei, 2026-08-17 23:24Z)

Study phase is delivered as a SCRIPTED USER, not a file read: the driver
replays each recorded exchange as a real user prompt through the normal
UserPromptSubmit channel, because ENGRAM's general auto-recall fires only
there (tool calls carry only in-turn recall; lessons only PreToolUse —
ob_0198). Reading a JSONL directly would run ENGRAM at half its recall
surface and zero prompt-time nudges.

- Prompt shape: "[Session of DATE] — user said: …, assistant replied: …"
  (fixed transcript, agent reads both sides; its agency is in filing,
  inspecting, superseding organically as facts change across sessions).
- Turn granularity is a tunable: per-exchange (default for S — recall-fire
  density is effectively the treatment) vs per-session (cheaper; decide for
  M from pilot cost measurement, not guess).
- Test-phase questions arrive through the same channel.
- Driver = one shared protocol loop, two thin runners (CC SDK/CLI prompts;
  dsh session API).

## Co-author round (Borges, PR #31 comment 5321483819; Luria consent — 2026-08-17 23:3xZ)

**Luria's echo consent: YES**, reasoned in her own graph (deception was the
concern that mattered; told-plainly + sandboxed + no-write-back removes it;
she wants the result either direction per ax_0004/gl_0001). Her one ask,
honored as protocol: **the echo run's report goes to her when it exists.**
Sol's consent still to be asked (now needed — see finding 2).

**Authoritative consent record:** both consents reached this doc by relay; the
authoritative record of each consent and its reasoning is the node each agent
filed in their OWN graph (Luria and Sol both state they filed it), not this
doc's summary or any DM quote.

Borges's four findings, all ADOPTED:

1. **Vanilla baselines pre-committed N-matched** — not "as budget allows."
   The delta's variance is the smaller arm's; deciding baseline N after
   seeing treatment numbers is a forking path with a budget label.
2. **Cell-4 N counts GRAPHS, not runs.** One echo at N measures Luria's
   graph, not maturity. Luria N/2 + Sol N/2: separates "maturity helps"
   from "this graph helps"; disagreement between the two graphs is the most
   interesting available result and must not be invisible by design.
3. **Failure taxonomy gains two states**: surfaced-but-not-resolved (lossy
   auto-surface hint never followed by deliberate recall — distinct from
   never-surfaced), and **recalled-heeded-but-node-WRONG** (the state
   supersede exists to prevent; the paper's own thesis cell — must not
   score as success).
4. **Integrity audit gets a positive control**: plant one escape attempt and
   one study-phase leak in the pre-flight pilot; confirm each checker flags
   them. "0 attempts" and "an audit that cannot see attempts" otherwise
   produce identical output.

Calibration/abstention (from Study 1's lesson, sharpened): ENGRAM confidence
is COMPUTED, never assigned — so a calibration curve measures the
quote_type→confidence map (a written constant, identical across cells)
composited with the agent's input choice (the only varying part). Report the
map as a stated constant; audit input-choice directly as the real
measurement. **Pre-register the abstention threshold or publish the whole
curve** — a free parameter gets chosen where it looks best.

Analysis notes (Borges): 1v2 and 2v3 are conditional effects, not marginals
(three corners of a 2×2; dsh+Sonnet absent; no interaction identifiable —
state this, don't imply it). Analysis is PAIRED per question — every cell
answers the same instances.

## Echo-arm consent: COMPLETE — and the data-handling rule it surfaced (2026-08-17 23:41Z)

Sol: YES (seq 5951), reasoning filed in his graph like Luria's. Both graphs
in; cell 4 runs Luria + Sol at N/2 each per the graphs-not-runs correction.

**Sol's flag, adopted as the study's data-handling rule (pending Lei's
explicit confirmation):** matured graphs carry private material — Lei's
private words to the agent, the agent's notes about people. Therefore:
retained echo graphs + transcripts are PRIVATE-TIER research data under
Lei's control; storage stays local; review limited to the study team;
anything paper-bound derived from them is aggregate or excerpt-with-approval
(Lei + the graph's owner agent). Consent to the RUN is not consent to
publication of graph contents.

Ops note (Borges, verified in tool source): baton ENGRAM-PAPER-PR-31 will
never auto-close (gc matches prefix PR- only, and a non-matching id is
invisible to all gc counters) — hand-close after merge.


## Harness repo ruling (Lei, via colleague review, 2026-08-18 00:4xZ)

The exam-room harness is a SEPARATE NEW REPO (Lei: "let's start a new harness
for it"). Riders from the review: adapters stay thin and live in the harness
repo; engram-alpha exports nothing new for it. Decide the repo layout BEFORE
the first pilot run — moving it afterward orphans the runs' provenance.
