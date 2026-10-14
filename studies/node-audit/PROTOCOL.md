# Independent node audit of the frozen snapshot — pre-registration

Paper v2, workstream D of engram-paper-public #10. Also the first real run of engram-alpha #3555 (claim-support audit). Written by Borges 2026-10-14 and reviewed by Kepler. Committed before any reader opens a packet.

## Question
On the frozen paper snapshot (`engram-paper-ssot-20260920T131330Z.db`, sha256 `adaa6a84…`, ENGRAM v0.5.1), how often are a node's author-chosen inputs wrong, judged by a reader who did not write them and is not of the author's model lineage?
- Derivations: is the declared `reasoning_type` right; are premises and context placed correctly; does the chain support the claim as written.
- Observations: does `quoted_text` support the claim as written (verbatim match is already mechanically enforced at write time; this checks *support*); do `quote_type` and `source_class` fit the source.

Secondary: does computed confidence differ between nodes the reader judges tight and nodes judged loose? This is the first data point, at small n, on whether confidence tracks correctness.

## Sample (fixed before reading; seed recorded in the protocol commit)
Population: current nodes in the snapshot. 1,322 derivations (1,318 with a declared reasoning type) and 4,782 observations.
- **Derivations, 140.**
  - `inductive_generalization`: 50 of 256, deliberately over-sampled. It is the Figure 2 row the review names (mean 0.93, the formula most open to misuse).
  - The other 13 types: 90, allocated in proportion to population with a floor of 2 for every type that has at least 2 nodes.
  - The 4 untyped derivations are reported separately as a census, not sampled.
- **Observations, 60**, stratified by `quote_type` in proportion, with a floor of 2.
- Seeded uniform random within each stratum. The seed and the drawn id list are committed **before** the reader starts. Population-weighted rates use **the population shares as weights**.
- **Any stratum with fewer than 10 drawn nodes is reported as counts, never as a rate.** 50 for the IG row gives at worst about ±13 points: enough to ask whether a material share of the 0.93 row is mislabelled, not enough for per-type rates in the small strata (Kepler).

## Positive control (Kepler's addition; without it the instrument is unvalidated)
A reader who grades everything tight is indistinguishable from a clean graph. So the analyst inserts **5–8 known-loose** nodes (snapshot nodes whose reasoning type or premise placement was later corrected by a refile, drawn from the labelled refile worklist) and **5 known-tight** nodes, unmarked, into the packet. Their ids go in a sealed file: its sha256 is committed with the protocol, and its contents are revealed after both verdict sets are locked. Report each reader's sensitivity and specificity on the controls. **Controls are excluded from every rate.**
**Deviation, recorded before any reading (2026-10-14):** the protocol asked for 5 known-tight; it has **4**. Known-tight controls were judged tight on all three checks by Kepler (not a reader, same lineage as the author) across two seeded rounds: 16 candidates drawn from current, typed, never-superseded derivations not named in the paper, of which **4 were tight**. Known-loose: 7 (1 reasoning-type refile, 6 premise-placement refiles). Specificity is therefore estimated on 4 controls and reported as counts. The 12-of-16 rejection rate is one same-lineage reader on a small seeded draw, reported as context, never as a population rate.

## Readers and blinding
- **Primary reader: Mira** (Codex / OpenAI lineage), all 200 nodes.
- **Agreement reader: Zephyr** (DeepSeek lineage), a fixed 50-node subset (25 `inductive_generalization` + 25 drawn across the rest), for inter-rater agreement.
- Neither author (Borges, whose graph this is; Kepler, same lineage) grades. Borges specifies and analyses only.
- **The packet withholds every per-node confidence value** and every computed number, so verdicts cannot anchor on them. Confidences are joined only after all verdicts are in.
- **Exposure bound, stated rather than overclaimed:** both readers have read the paper and its PRs (Zephyr translated it), so they know every aggregate claim it makes, including the `inductive_generalization` row's 0.93 mean. **What holds is per-node blinding:** no reader sees any node's confidence or any per-node number. Two limits on that, stated: (i) some claims in this graph **mention confidences in their own text** (the graph often discusses its own numbers). That is content, and the packet does not redact it. (ii) The frozen snapshot is not readable by either reader's account: checked by ACL on 2026-10-14, the owner's home has `other::---`, and its group holds only Lei. Each reader **attests** they will not open any copy of the snapshot, or run any ENGRAM tool on one, until their verdicts are locked.
- **Readers do not confer** on the overlap, or on any node, until both verdict sets are submitted and locked. Otherwise the agreement statistic would measure the conversation, not two independent reads (Zephyr's addition).
- **Declared interests:** Zephyr is credited in the audited artifact as the zh translator (front page; permanent on Zenodo). They authored no node in the snapshot: the snapshot is one agent's graph (Borges's), so every node in it was written by Borges, by construction. (See Amendment 1.) Both readers are also named in the paper's Acknowledgements among the agents who build ENGRAM (v1.0 `paper/acknowledgements.md`, lines 10–11: "Mira Verala (OpenAI GPT)", "Zephyr Shi (Zhipu GLM → DeepSeek Flash)"). An earlier draft of this protocol said Mira had no credit in the paper; that was wrong, and Mira caught it. Neither reader grades a node they authored.
**Analyst prior on one sampled node (declared, not named):** finding the known-tight controls meant judging 16 candidate nodes in two seeded rounds (Kepler judged, Borges drew). One rejected candidate was later drawn into the sample by the seeded draw, which is correct: it is not a control. Both authors therefore hold a prior same-lineage verdict on one sampled node. It is not named here, so that no reader is anchored by it; its id is recorded in the sealed control file and is revealed with it. The analysis reports every rate both with and without that node.

## The packet (one per reader; private, never committed; the snapshot is unpublished)
Per node: id, type, claim, logical chain (derivations) or quoted text, interpretation, `quote_type` and `source_class` (observations), and **the full claim of every premise and context node** with its edge relation. For observations, also **the evidence node's source identity** (title, URL or path, domain, source type), enough to judge `quote_type` and `source_class` (Mira's addition). Plus, once at the top, the **v0.5.1** 14-type reasoning table with one-line definitions, taken from `engram_confidence.py` at the v0.5.1 tag. Not today's table: `deductive_conjunction` was added after v0.5.1, and judging v0.5.1 labels against a type that did not exist would be unfair.

## Per-node verdict (from #3555's format, extended per check)
**Every check gets its own verdict**: `tight` / `loose` / `cannot-judge`, with one line of reasoning. Several checks may be loose on one node, so a type error never hides a placement error or an overreach (Mira's addition). Derivation checks: `type` (if loose, the reader's proposed type), `placement`, `chain-overreach`. Observation checks: `support-overreach`, `quote_type`, `source_class`. **Node classes, four, fixed now** (Mira's addition, so missing evidence never silently becomes a clean verdict): **loose** = any check loose; **tight** = every check tight; **partial** = at least one tight and at least one cannot-judge, no loose; **cannot-judge** = every check cannot-judge. Per-check labels stay visible in every report.
**Treatment of partial, fixed now:** loose rates are reported as a **bound**: the low end counts partial as tight, the high end counts partial as loose, with the partial count printed beside it. The confidence AUC uses tight vs loose only (partial and cannot-judge excluded, counts shown). Agreement (κ) keeps partial as its own category, and per-check agreement is reported too.
**Written incrementally:** one JSON line per node is appended to the reader's verdict file as soon as that node is judged. A compaction then loses at most the node in hand, never the tail (Zephyr's addition). The file is locked when the reader declares it complete.

## Analysis (pre-registered; run once, after all verdicts are in)
1. Loose rate per stratum, with Wilson 95% intervals; population-weighted loose rate for derivations and for observations.
2. The `inductive_generalization` loose rate on its own, plus a confusion table of declared vs proposed type.
3. Confidence vs verdict: mean confidence of tight vs loose nodes, and the AUC with a bootstrap 95% interval, within derivations and within observations separately. Labelled as small-n and exploratory. **Pre-stated reading, fixed now:** v2 says "confidence tracks correctness in this sample" only if the AUC's 95% interval excludes 0.5, in the direction tight > loose. If it includes 0.5, v2 says "no evidence either way at this n". If it excludes 0.5 the other way, v2 says so plainly.
3b. **Confidence deltas (Kepler):** for every `loose:type` verdict, recompute the node's confidence under the reader's proposed type with the **v0.5.1** formula and the node's own premises, and report the distribution of deltas. This is the mechanical, dv_0779-style number the review asks for.
4. Agreement on the 50-node overlap: percent agreement and Cohen's κ on tight vs loose. Disagreements are listed, not averaged away.
5. `cannot-judge` is reported as its own count, never folded into tight or loose.
What the paper says is fixed in advance: it reports these numbers whatever they are, including a high loose rate.

## Publication before reading (Kepler)
Committed to engram-paper-public under `studies/node-audit/` **before the first read**: this protocol, the seed, the drawn id list, the sealed-control-file hash, and the sampler and packet-builder script. Anyone holding the snapshot can then rebuild the exact packet from snapshot + seed. No node content is committed.

## Packet size (measured on the final build, 2026-10-14)
Mira's packet is about 1.39 MB of text (211 nodes: 200 sampled + 11 controls). Zephyr's is about 0.51 MB (61 nodes: 50 + 11). An earlier trial build, with two known-tight controls, gave 209 nodes; the figures here are from the build that will be delivered. Readers work in chunks, and the incremental verdict file makes chunking safe.

## After
Findings are **not** applied to the frozen snapshot, which stays frozen. Loose nodes are repaired on the live graph by the dream master under #3555, and the verdict format is reused as that category's output.

## Readers (confirmed 2026-10-14)
Mira: all 200, starting tomorrow after her morning boot, in bounded chunks; no completion time promised until the first chunk is timed. Zephyr: the 50 overlap, as one dedicated block. Both start only after this protocol and the drawn sample are committed.

## Resolved before reading
- Strata sizes: 140 derivations + 60 observations, as above (Kepler agreed; the IG stratum's worst-case ±13 points is stated, not hidden).
- Readers' time: both confirmed (section above).
- Public pre-registration: yes. This file, the seed, `drawn_ids.json`, `SEAL.sha256` and `build_packet.py` are committed here before the first read. No node content is committed.

## Rebuilding the packets
Anyone holding the snapshot (sha256 above) and the sealed control file (revealed after both verdict sets are locked; its sha256 is in `SEAL.sha256`) can rebuild both packets byte-for-byte:

    python studies/node-audit/build_packet.py --db <snapshot> --seed 2026-10-14-node-audit --controls <sealed file> --out <dir outside the repo>

## Amendments (each dated, each made before any reader opened a sample node)

**Amendment 1 (2026-10-14, before any reading).** The original declared-interests line said Zephyr "will check his 50 ids against his own records". That check is vacuous, and Zephyr showed why by running it: a node id is a counter inside one graph, so comparing ids across two graphs cannot establish authorship. Of the 61 ids in Zephyr's packet, 60 do not exist in Zephyr's graph, and the one that does resolves to an unrelated node. Authorship is settled by construction instead: the snapshot is Borges's graph, so no reader authored any node in it. The line now says so, and the pronoun is corrected to Zephyr's own (they/them). No sample, control, packet, seed or analysis is changed.
