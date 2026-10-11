# Patel & Patel "ENGRAM" — Evaluation Methodology Deep-Read
**Paper:** "ENGRAM: Effective, Lightweight Memory Orchestration for Conversational Agents"
**ArXiv:** 2511.12960 — submitted 2025-11-17, revised 2026-02-03
**Primary source:** https://arxiv.org/html/2511.12960v1
**Scan date:** 2026-05-07
**Prepared for:** ENGRAM-Borges paper team

---

## Naming collision notice

Patel & Patel chose the acronym ENGRAM for their system independently. Their ENGRAM is a flat three-store retrieval system (episodic / semantic / procedural), bearing no architectural relationship to ENGRAM-Borges (claim-level knowledge graph with retraction cascade, provenance, and contradiction nodes). The shared name is coincidental and creates citation friction but not a technical conflict. Throughout this document "Patel-ENGRAM" refers to their system and "ENGRAM-Borges" to ours.

---

## 1. Benchmarks Used

### 1.1 LoCoMo (primary benchmark)

**Full citation:** Maharana et al. (2024). "Evaluating very long-term conversational memory of LLM agents." *Proceedings of ACL 2024*, pp. 13851–13870.

**What it tests:** Long-horizon multi-session conversational QA. The paper describes it as "a realistic multi-session conversational question-answering (QA) suite for long-horizon memory."

**Scale:** "The released benchmark contains 10 dialogues, each averaging ≈600 turns and ≈16K tokens across up to 32 sessions."

**Question categories:**
- Single-hop (direct retrieval from a single turn)
- Multi-hop ("composing information spread across distant turns")
- Temporal (time-aware reasoning)
- Commonsense/world knowledge (labeled "open-domain" in their Table 1)
- Adversarial/unanswerable — **explicitly excluded from all reported metrics** ("Following common practice, we exclude adversarial/unanswerable items when reporting QA metrics")

**Scoring:** Three metrics per question:
- LLM-as-Judge (J): GPT-4o-mini renders "a binary semantic-correctness decision based on factual fidelity, relevance, completeness, and contextual appropriateness." Results are evaluated three times; reported as mean ± standard deviation.
- Token-level F1: with deterministic normalization (Unicode NFKC, lowercasing, article/punctuation removal, whitespace compaction, numeric canonicalization, temporal form resolution to ISO-8601).
- BLEU-1/2 (B1/B2): with smoothing, same normalization pipeline.

**Note on F1/BLEU:** Patel-ENGRAM scores *lower* than competitors on F1 and BLEU (e.g., single-hop F1: ENGRAM 23.13 vs MemOS 45.35) while scoring highest on LLM-as-Judge. The paper does not directly resolve this tension; it implicitly treats J-score as the primary metric. This asymmetry is load-bearing for any attempt to replicate their "SOTA" claim — their SOTA is specifically on the semantic-correctness metric, not lexical overlap.

### 1.2 LongMemEval (secondary benchmark)

**Full citation:** Wu et al. (2025). "LongMemEval: Benchmarking chat assistants on long-term interactive memory." *ICLR 2025*.

**What it tests:** Extended-horizon conversational memory across five ability categories: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention.

**Scale:** "500 curated questions embedded in length-configurable chat histories"; described as "~115K tokens per problem" in the full-context configuration.

**Scoring:** LLM-as-Judge binary correctness (same GPT-4o-mini judge). The paper refers to the small variant as LongMemEval_s; ENGRAM uses the full 500-question set.

**LongMemEval per-category results (Table 3):**

| Question Type | Full-context (101K tokens) | Patel-ENGRAM (1.0–1.2K tokens) |
|---|---|---|
| Single-session-preference | 23.33% | 93.33% |
| Single-session-assistant | 92.86% | 87.50% |
| Temporal-reasoning | 37.59% | 55.64% |
| Multi-session | 39.10% | 60.15% |
| Knowledge-update | 79.49% | 74.36% |
| Single-session-user | 82.86% | 97.14% |
| **Overall** | **56.20%** | **71.40%** |

**Critical observation:** Patel-ENGRAM underperforms full-context on *knowledge-update* questions (74.36% vs 79.49%) and on single-session-assistant (87.50% vs 92.86%). The "+15 absolute points" headline obscures these category-level reversals. The system trades breadth for needle-in-haystack efficiency — an important nuance for fair citation.

### 1.3 No other benchmarks used

The paper does not use LongBench, ConvAI, Persona-Chat, MMLU, or any other benchmark. The evaluation is entirely on LoCoMo and LongMemEval. This is a **narrow evaluation surface** — both benchmarks test multi-session conversational QA only. They do not test:
- Belief revision under contradictory updates
- Provenance traceability
- Reasoning-chain integrity
- Calibrated confidence output
- Retraction correctness

---

## 2. Metrics — Exact Names and Numbers

### 2.1 Primary metric: LLM-as-Judge (J-score)

Binary semantic correctness judged by GPT-4o-mini. Three independent evaluations per question; mean ± standard deviation reported. The judging prompt asks for assessment of "factual fidelity, relevance, completeness, and contextual appropriateness." The specific judge prompt text is not reproduced verbatim in the paper.

**Limitation flagged in their own limitations section:** "Our evaluation employs GPT-4o-mini as the judging model, and while we report mean ± standard deviation across runs, judge bias remains a limitation."

### 2.2 Secondary metrics: F1, BLEU-1, BLEU-2

Token-level lexical overlap with a deterministic normalization pipeline. These metrics are reported in Table 1 but are secondary in the paper's own framing (SOTA claim is on J-score only).

### 2.3 Latency metrics (Table 2)

Per-question retrieval and end-to-end response latency. Patel-ENGRAM: median 1.487s, p95 1.819s. Full-context baseline: median 9.940s, p95 17.832s.

### 2.4 Token efficiency

"≈1% of the tokens" compared to full-context baseline. Denominator is ~101K tokens for LongMemEval full-context; Patel-ENGRAM uses ~1.0–1.2K tokens per query, "approximately a 99% token reduction in input length." Their average evidence budget across baselines is 916 tokens.

### 2.5 The SOTA claim — exact numbers

- LoCoMo overall J-score: Patel-ENGRAM **77.55±0.13**, vs prior best MemOS **72.99±0.14** (a 4.56-point margin).
- Full-context on LoCoMo (Table 2): **72.60±0.07** (Patel-ENGRAM beats full-context here too).
- LongMemEval overall: Patel-ENGRAM **71.40%** vs full-context **56.20%** (+15.20 absolute points).

---

## 3. Baselines

### LoCoMo baselines (Table 1) — all systems, overall J-score:

| System | J-score (overall) | Chunk/Mem Tokens |
|---|---|---|
| **Patel-ENGRAM** | **77.55±0.13** | **916** |
| MemOS | 72.99±0.14 | 1593 |
| Mem0 | 64.73±0.17 | 1177 |
| LangMem | 55.28±0.13 | not reported |
| OpenAI (memory) | 52.81±0.14 | not reported |
| Zep | 42.29±0.18 | not reported |

**"OpenAI" baseline:** The paper does not define what "openai" refers to specifically. Context suggests it is OpenAI's API-based memory feature (likely the ChatGPT persistent memory or Assistants API memory), but the paper provides no citation or configuration description. This is a documentation gap — the baseline is underspecified.

### LongMemEval baseline:

Only the full-context baseline is used. No other memory systems are compared on LongMemEval.

---

## 4. Test Setup

### Conversation length / horizon
- LoCoMo: ~600 turns, ~16K tokens, up to 32 sessions per dialogue. All 10 dialogues used.
- LongMemEval: ~115K tokens per problem instance, 500 questions.

### Domain coverage
Both benchmarks are **open-domain conversational QA** grounded in persona-driven dialogues (constructed via "human–machine pipeline grounded in personas and event graphs, followed by human edits for long-range consistency"). Neither benchmark covers task-specific domains (finance, code, medicine, etc.).

### LLM backbone
"Holding the LLM backbone fixed (gpt-4o-mini)" for all generation. The same model is used for routing, generation, and judging — a potential confound not discussed in the paper.

### Hardware / inference cost
Not reported. No GPU or inference cost figures are given.

---

## 5. Architecture Details

### 5.1 Three-type router

Every user turn is classified by an LLM call into one or more of three store types, represented as "a compact three-bit mask bₜ=(bᵗᵉᵖⁱ, bᵗˢᵉᵐ, bᵗᵖʳᵒ)."

**Router prompt (Appendix D.1, verbatim):**
> "Given this message, determine which storage types are most relevant: Message: {message} Storage types: episodic: Event and experiences with temporal context (think of this as a personal diary of events that is timelined); semantic: Facts, observations, preferences (only route to this if the message reveals a non-event fact or preference about a person, place, or thing); procedural: How-to information, processes"

This is a prompt-based LLM classifier with no fine-tuning. Complex utterances spanning multiple categories produce multi-bit masks (overlapping writes to multiple stores). "The router is intentionally minimal, so complex utterances spanning multiple categories may require soft routing or overlapping writes" (limitations section).

### 5.2 Memory record schemas

- **Episodic:** (title, summary, timestamp, embedding) — "events and experiences with temporal context"
- **Semantic:** (fact string f, temporal anchor δ, embedding e) — "stable facts or preferences"
- **Procedural:** (title t, normalized content c, temporal anchor δ, embedding e) — "instructions or workflows"

### 5.3 Embedding model

`text-embedding-3-small` (OpenAI). Cosine similarity for retrieval.

### 5.4 Retrieval parameters

Top-K=25 per store type (three stores = up to 75 candidates before deduplication). K=25 chosen empirically: Appendix A.2 ablation shows K=20→25 yields +1.90 J-points for +149 tokens; K=25→30 yields only +0.36 points for +182 tokens. Results merged across stores with "simple set operations" (deduplication, no re-ranking described).

### 5.5 Persistence

SQLite database. Exact schema not published in the paper. Records include timestamps and speaker attribution but no explicit citation mechanism. "Records serialize as δ(m):text(m) where δ is temporal anchor and text is content."

### 5.6 Contradiction handling / belief revision

**Not implemented and not documented.** The paper does not describe any mechanism for handling contradictory memory records. "Knowledge updates" appears as an evaluation category in LongMemEval, and Patel-ENGRAM underperforms full-context on it (74.36% vs 79.49%). The limitations section mentions "editable memory governance" and "temporal decay" as future work. There is no retraction, no versioning, no conflict detection — new records are appended and old records persist.

### 5.7 Provenance

**Not tracked.** Memory records include timestamps and speaker attribution but no source provenance, citation, or evidence-class metadata. The word "provenance" does not appear in the paper.

---

## 6. Comparative Table: Patel-ENGRAM vs ENGRAM-Borges

| Dimension | Patel-ENGRAM | ENGRAM-Borges |
|---|---|---|
| Architecture | Flat three-store (episodic/semantic/procedural) + cosine retrieval | Claim-level DAG (ob/dv/ct/ev/qu nodes) with edge-direction discipline |
| Persistence | SQLite, records appended | SQLite + Git, with schema-typed nodes and edge types |
| Retrieval | Top-K=25 dense cosine per store | FTS5 full-text + engram_query, subgraph traversal |
| Contradiction detection | None documented | First-class contradiction nodes (ct_NNNN), explicit claim-vs-claim edges |
| Belief revision | None | Retraction cascade: taint downstream derivations when premise retracted |
| Provenance | Timestamp + speaker only | Evidence nodes (ev_NNNN) with source URL, title, date, domain |
| Confidence | Not tracked per-record | Evidence-class taxonomy: hard_data(0.95) → editorial(0.35) |
| Verbatim quote integrity | Not tracked | quote_type field; verbatim vs paraphrase distinguished |
| Reasoning types | Not tracked | Reasoning type per derivation (inductive/deductive/abductive/analogical) |
| Update semantics | Append-only (no versioning) | Retraction with cascade; new claim can supersede old with taint propagation |
| Benchmarks run | LoCoMo, LongMemEval | Single domain (financial), 4 queries, LLM-as-judge |
| Token efficiency | 916 tokens avg / SOTA on LoCoMo | Not measured |
| LLM backbone | GPT-4o-mini fixed | Backend-agnostic (Gemini, GPT-4, Claude, Ollama) |
| Multi-session scale | 32 sessions, 600 turns | Not evaluated at scale |
| Open-source | Yes (GitHub, based on paper) | Internal (kg repo) |

---

## 7. Assessment: Replicability

### 7.1 Could we replicate their LoCoMo setup?

**Partially, with significant engineering investment.** What is available:

- LoCoMo benchmark is publicly released (ACL 2024 — downloadable from the Maharana et al. paper or HuggingFace).
- LongMemEval is published at ICLR 2025 (Wu et al.) — likely available on HuggingFace or the authors' GitHub.
- The GPT-4o-mini judge approach is described in enough detail to replicate mechanically.
- Top-K retrieval with text-embedding-3-small is standard engineering.

What we would need to build:

1. **Multi-session conversation ingestion** — our eval_harness.py currently handles single-query ingestion from static sources. LoCoMo requires ingesting a full 600-turn / 32-session dialogue, turn by turn, then asking QA questions at the end. Our harness has no concept of "replay a conversation history to build memory."
2. **Turn-level routing** — every utterance must be classified and stored at write time. Our system commits claims in batch (via `kg_add_observation_batch`) after reading a source, not interactively during a conversation.
3. **Score aggregation over 10 dialogues** — trivially addable to the harness.
4. **F1/BLEU normalization pipeline** — not currently in our harness (our judge scores are 1–5 dimensional, not binary lexical-overlap metrics).

**Engineering estimate:** 4–6 weeks of focused work to build a conversation-replay ingestion mode into eval_harness.py and implement the normalization pipeline. This is not a weekend task but it is tractable.

**Should we?** See section 8.

### 7.2 Is replication of their exact numbers likely?

**Unlikely without matching their architecture.** Their J-score advantage comes from their routing + top-K setup with GPT-4o-mini as both the inference model and the judge. ENGRAM-Borges does not have a turn-level router and is designed for episodic claim-level provenance, not conversational QA recall. We would likely underperform their SOTA on token efficiency and possibly on J-score as well, because our architecture prioritizes different things (epistemic traceability over recall speed).

**This is not a deficiency — it reflects different design goals.** But we should not claim to compete on their benchmark without that caveat.

### 7.3 LongMemEval — is the knowledge-update category relevant to us?

**Yes, and this is the most interesting overlap.** The knowledge-update questions in LongMemEval test whether a system correctly uses the most recent version of a fact when an earlier version has been superseded. Patel-ENGRAM gets 74.36% on this (below full-context's 79.49%). ENGRAM-Borges has explicit retraction semantics designed for exactly this case. We would likely outperform both on knowledge-update questions if evaluated correctly. This is worth highlighting.

---

## 8. Evaluation Philosophy — Alignment Analysis

### 8.1 Their philosophy

Patel & Patel optimize for: **token efficiency + conversational recall accuracy** measured by semantic correctness (LLM judge). The implicit assumption is that memory is good if it retrieves the right facts from prior conversation turns, using as few tokens as possible.

Their evaluation does NOT test:
- Whether the system knows *why* it believes something (no provenance test)
- Whether it correctly handles a belief being superseded (knowledge-update is tested but not their strength)
- Whether it can trace which stored memory contributed to an answer
- Whether downstream claims built on a retracted fact are invalidated
- Whether confidence is calibrated to evidence quality

### 8.2 Our philosophy

ENGRAM-Borges optimizes for: **epistemic traceability, self-correction, calibrated confidence**. The system is designed to answer "why do you believe X?" with a chain of evidence nodes, and to propagate retractions through derivation chains.

### 8.3 Conclusion: these are orthogonal systems

The two systems share a name and both store conversational memory in SQLite, but they optimize for different properties. Patel & Patel's benchmark suite (LoCoMo + LongMemEval) **cannot distinguish ENGRAM-Borges's novel features from a flat retrieval system** because the benchmarks do not probe:
- Retraction cascade correctness
- Provenance chain completeness
- Contradiction detection precision/recall
- Confidence calibration quality

Running LoCoMo on ENGRAM-Borges would likely produce competitive but not SOTA results (we are not optimized for token efficiency), and would **not demonstrate our actual contributions**. We should cite their results as state-of-the-art on conversational recall benchmarks but not attempt to match them.

---

## 9. Net-New Evaluations ENGRAM-Borges Actually Needs

The following benchmarks / test suites do not appear to exist in published form. We would need to create them (or adapt existing datasets).

### 9.1 Retraction cascade correctness test

**What it tests:** When a foundational claim is retracted (marked as wrong), do all downstream derivations that depended on it become tainted? Do answers generated from a tainted derivation include appropriate uncertainty markers?

**Design:** Build a synthetic DAG of 5–10 interconnected claims (ob → dv → dv → answer). Retract ob_0001. Verify that dv_0002 (which cites ob_0001) is tainted, that dv_0003 (which cites dv_0002) is also tainted, and that a query answered from dv_0003 produces a "this reasoning chain may be compromised" signal.

**No existing benchmark does this.** The closest would be procedurally generated belief-revision tests, but none in the agent-memory literature are designed for DAG-level cascade correctness.

### 9.2 Verbatim-quote integrity test

**What it tests:** When the system claims "the paper says X," does X appear verbatim (or close to verbatim) in the cited source? Does the system distinguish verbatim from paraphrase from fabrication?

**Design:** Seed the graph with sources containing known verbatim text. Query for claims. Score: (a) is the cited quote verbatim or paraphrase, (b) does the system correctly label its quote_type, (c) does the system refrain from citing sources for claims that are interpretations rather than quotes.

**Why it matters:** LLM hallucination manifests as plausible-sounding fabricated quotes. ENGRAM-Borges's quote_type field and verbatim distinction is a direct mitigation. No benchmark currently measures this for memory systems.

### 9.3 Reasoning-type confidence calibration test

**What it tests:** Does reported confidence track evidence quality? Is a claim backed by hard_data(0.95) actually more reliable than one backed by editorial(0.35)?

**Design:** Create a calibration set of questions with known ground-truth answers. Run ENGRAM-Borges and record the evidence_class and confidence for each answer. Compute calibration error (Brier score or ECE) across evidence classes. A well-calibrated system should show higher accuracy on high-confidence claims.

**Closest existing benchmarks:** Calibration literature (Guo et al. 2017, "On Calibration of Modern Neural Networks") provides the methodology, but no agent-memory-specific calibration benchmarks exist.

### 9.4 Contradiction detection precision/recall

**What it tests:** When the knowledge graph contains two nodes with conflicting claims, does the system correctly identify and surface the contradiction? Does it produce a ct_ node? Does it refrain from asserting either claim with full confidence?

**Design:** Seed with deliberate contradictions (e.g., "source A says X, source B says ~X"). Measure: (a) was a contradiction node created, (b) when queried, does the system surface the conflict rather than picking one side arbitrarily, (c) false-positive rate (does it flag non-contradictions as contradictions).

### 9.5 Knowledge-update correctness on LongMemEval subset

**What it tests:** On the specific knowledge-update questions from LongMemEval, does ENGRAM-Borges's retraction mechanism outperform flat-retrieval systems?

**Why this is tractable:** LongMemEval is a published benchmark and the knowledge-update subset is defined. We would need to implement conversation-replay ingestion (see §7.1) but could focus on just the 79 knowledge-update questions rather than the full 500. This would give us a single clean comparison point: our retraction semantics vs Patel-ENGRAM's append-only store on exactly the question type where their system is weakest.

**Estimated effort:** 2–3 weeks. Lower investment than full LoCoMo replication.

---

## 10. Recommendations

### Use as citation, not as competitor

**Confidence: high.**

Cite Patel & Patel as establishing SOTA on conversational recall benchmarks (LoCoMo J-score 77.55±0.13, LongMemEval 71.40% vs 56.20% full-context) and as evidence that lightweight typed retrieval can beat full-context at scale. Position ENGRAM-Borges as addressing a different problem: epistemic traceability and self-correction, not just recall efficiency.

Suggested framing: "Patel et al. (2025) demonstrate that typed retrieval with token budgeting achieves state-of-the-art conversational recall on LoCoMo. However, their architecture provides no mechanism for contradiction detection, provenance tracking, or retraction propagation — the properties that constitute epistemic identity rather than memory recall."

### Do not attempt to replicate their LoCoMo SOTA

**Confidence: high.**

Our system is not optimized for the metrics their benchmark measures (token efficiency, J-score on factual recall from prior turns). Attempting to match their numbers without matching their architecture would require re-engineering work that detracts from our actual contributions. If we do run LoCoMo, frame it as "here is our position on this benchmark" not "we beat or match Patel et al."

### Invest in net-new eval infrastructure, prioritized order

**Confidence: medium (the designs are sound; implementation estimates are rough).**

1. **LongMemEval knowledge-update subset** (2–3 weeks) — highest ROI. Uses an existing published benchmark, targets exactly the question type where our retraction semantics should outperform append-only systems, and produces a concrete comparison point.
2. **Retraction cascade correctness test** (1–2 weeks) — synthetic, fully controlled, directly demonstrates our claimed-novel feature. Can be built internally without an external benchmark.
3. **Contradiction detection precision/recall** (1–2 weeks) — same, synthetic, measures ct_ node creation accuracy.
4. **Verbatim-quote integrity test** (2–3 weeks) — requires assembling a ground-truth quote corpus. Most novel but also most labor-intensive.
5. **Full LoCoMo replication** — low priority given above; expensive and does not favor our architecture.

### Note on the "openai" baseline

The paper lists an "openai" baseline at 52.81±0.13 on LoCoMo overall but does not describe its configuration. If this is the OpenAI Assistants API memory or ChatGPT persistent memory, it is a relevant comparison for Anthropic's Memory tool (ob_1487, per context). The underspecification is a gap in their paper that limits how this result can be cited.

---

## 11. What Is Commoditized vs. What Remains Novel (per dv_0559 positioning)

### Commoditized by Patel & Patel (and others)

- Typed memory storage (episodic/semantic/procedural) — Patel-ENGRAM does this with a simple router; the concept is now in the benchmark record.
- Dense retrieval from a conversation history — well-established.
- Token-efficient memory retrieval beating full-context — demonstrated quantitatively.
- LLM-as-judge evaluation for conversational memory — now a standard methodology.

### Not addressed by Patel & Patel (and still uncontested per Atlan 2026)

- **Claim-level contradiction nodes** — Patel-ENGRAM has no contradiction mechanism whatsoever. New facts silently coexist with contradicted old facts.
- **Retraction cascade through derivation chains** — explicitly absent. Their knowledge-update underperformance (74.36% vs 79.49% for full-context) is likely a symptom of this gap.
- **Provenance chain completeness** — no source URLs, no evidence-class metadata, no quote_type tracking.
- **Calibrated confidence tied to evidence quality** — not mentioned.
- **Reasoning-type-aware derivation** — not present.
- **Agent-as-author identity accumulation** — architectural non-goal for Patel-ENGRAM; they build a conversation memory, not an epistemic identity.

---

## Sources

- Patel & Patel (2025). "ENGRAM: Effective, Lightweight Memory Orchestration for Conversational Agents." arXiv:2511.12960. https://arxiv.org/html/2511.12960v1
- Maharana et al. (2024). LoCoMo benchmark. ACL 2024. pp. 13851–13870.
- Wu et al. (2025). LongMemEval. ICLR 2025.
- ENGRAM-Borges eval_harness.py: /home/agent-borges/kg/eval_harness.py (read 2026-05-07)
- ENGRAM-Borges eval_queries/gold_market.json: /home/agent-borges/kg/eval_queries/gold_market.json (read 2026-05-07)
