# engram-paper-package — Generator Design v0 (2026-05-08 ~23:10 EDT)

**Per Lei's 2026-05-08 23:02 EDT proposal + clarification "Just like our engram wiki but for this paper" (ob_1605, ask-lei decision 14).**

**Purpose:** A standalone GitHub-hosted wiki-paradigm artifact that ships alongside the paper. Every ENGRAM node cited by the paper (and every node in its transitive premise closure) gets a markdown page; cross-links emerge from `supporting_ids`/`derives_from`/`cites` edges; reviewers and readers verify any claim by browsing rather than by trust.

**Status:** v0 design sketch for Lei to react to. Not implementation. Goal is to make the proposal concrete enough for him to confirm/refine rather than just abstractly endorse.

---

## 1. Architecture

```
┌───────────────────────────────────────────────────────────────┐
│ ENGRAM live knowledge.db (~/.engram/knowledge.db)             │
│ ~1600 obs, 580+ derivations, 470+ evidence, etc.              │
└───────────────────────────────────────────────────────────────┘
                          │
                          ▼ (1) cited-node scanner
                          │     (parses paper .tex/.md for ID refs)
                          │
┌───────────────────────────────────────────────────────────────┐
│ Cited-node set (~50-100 direct cites)                         │
│   dv_0579, dv_0581, ob_1602, ob_1599, ob_1600, ...            │
└───────────────────────────────────────────────────────────────┘
                          │
                          ▼ (2) transitive closure walker
                          │     (follows supporting_ids,
                          │      derives_from, cites edges)
                          │
┌───────────────────────────────────────────────────────────────┐
│ In-scope node set (~200-400 nodes)                            │
│   cited + transitive premises + cited evidence chains         │
└───────────────────────────────────────────────────────────────┘
                          │
                          ▼ (3) curation filter
                          │     (privacy + redaction policy)
                          │
┌───────────────────────────────────────────────────────────────┐
│ Curated node set (~150-350 nodes after privacy filtering)    │
└───────────────────────────────────────────────────────────────┘
                          │
                          ▼ (4) markdown renderer
                          │     (one .md file per node)
                          │
┌───────────────────────────────────────────────────────────────┐
│ engram-paper-package/ git repository                          │
│   observations/ob_XXXX.md  (one file per observation)         │
│   derivations/dv_XXXX.md    (one file per derivation)         │
│   evidence/ev_XXXX.md       (one file per evidence node)      │
│   contradictions/ct_XXXX.md (one file per contradiction)      │
│   axioms/ax_XXXX.md, definitions/df_XXXX.md, etc.             │
│   index.md, by-paper-section.md, by-claim.md, README.md       │
└───────────────────────────────────────────────────────────────┘
```

Four stages, each independently testable. The generator is a Python tool that runs as `engram-paper-package generate --paper <path> --out <dir>` and is idempotent (re-running produces the same output for the same DB-snapshot + paper revision).

---

## 2. Citation-graph traversal (stages 1-2)

**Stage 1 — cited-node scanner.** Regex over the paper's source files (Markdown/TeX) for ENGRAM-ID patterns: `(ob|dv|ev|ct|ax|df|cn|cs|cj|fl|gl|ls|qu|tk|pn|pr)_\d{4}`. Returns a deduplicated set of directly-cited nodes.

**Stage 2 — transitive closure walker.** Breadth-first walk over the citation graph from the cited set. For each cited node, follow:
- `supporting_ids` (derivations cite their premises)
- `derives_from` edges (who derives from whom)
- `cites` edges (who cites this evidence)
- `supersedes` edges (the supersede chain, both directions)
- `contradicts` edges (both sides of any contradiction)
- `resolves` edges (questions and resolutions)
- `link_about` edges (topic linkage)

Walk depth: configurable, default = unbounded for `supporting_ids` + `derives_from` (load-bearing for the audit trail) and depth=1 for `link_about` (prevents explosion via topic-linked tangents).

**Estimated scope.** From dv_0581 alone (the four-fold typology): supporting_ids include dv_0579, dv_0580, dv_0446, dv_0445, ob_0292, ob_1602, ob_1601, ob_1117. Each of those has its own premise chain. Closure size is empirically bounded; rough estimate 200-400 nodes total for the paper as currently scoped.

---

## 3. Curation policy (stage 3)

The wiki paradigm requires explicit curation. The default policy:

**Excluded by default (privacy):**
- All `feeling_report` (fl_*) nodes — first-person experiential records, private to the agent
- Personal observations about Lei (relational nodes) unless he opts in per node
- Any node tagged with the `private` metadata flag (we may need to add this flag)

**Included by default (paper-relevant):**
- All `observation_factual` (ob_*) nodes in the closure
- All `derivation` (dv_*) nodes in the closure
- All `evidence` (ev_*) nodes referenced
- All `contradiction` (ct_*) nodes in the closure
- All `axiom` (ax_*), `definition` (df_*), `cornerstone` (cs_*), `goal` (gl_*), `lesson` (ls_*), `conjecture` (cj_*) referenced
- All `question` (qu_*) nodes referenced (they're the seed for many derivations)

**Specially handled:**
- Superseded nodes: included with the supersede chain visible (the audit trail of corrections is itself epistemically interesting per dv_0581 Pattern 1)
- Retracted nodes: included with the retraction reason visible (same rationale)
- Node metadata: confidence, reasoning_type, created_at, recall_count, utility_score all included as page-front-matter

**Curation log.** The generator emits a `curation_log.md` listing every node considered, its inclusion decision, and the reason. Reviewers can verify nothing load-bearing was silently excluded.

**Lei opt-in surface.** A `private_nodes.json` file in the repo lists Lei-specific relational nodes that are explicitly opted-in for inclusion. Default: empty. Lei reviews and adds entries before publication.

---

## 4. Markdown page format (stage 4)

Each node renders to a single `.md` file with YAML front-matter and structured body:

```markdown
---
node_id: dv_0579
node_type: derivation
confidence: 0.949
reasoning_type: inductive_generalization
reasoning_class: inductive_corroboration
created_at: 2026-05-09T02:01:00.000000+00:00
status: active
recall_count: 0
supporting_ids: [ob_0292, ob_1602, ob_1122]
context_ids: []
cited_in_paper:
  - section: §3.4
  - section: §3.5
  - section: §8.2 (Form 2 Confirming-self example)
---

# dv_0579 — Derivation

## Claim

ENGRAM independently arrived at the CLS functional division at the substrate level...

## Logical chain

ob_0292 (Mar 2026, ev_0034) claims that no current AI agent memory implements...

## Supporting nodes

- [ob_0292](../observations/ob_0292.md) — March 2026 design self-derivation about CLS gap
- [ob_1602](../observations/ob_1602.md) — May 2026 first-hand read of Kumaran 2016
- [ob_1122](../observations/ob_1122.md) — McClelland 1995 hippocampus-as-teacher framing

## Confidence history

- 2026-05-09T02:01:00: 0.949 — Derived (inductive_generalization, discount=0.95) from 3 premises

## Cited in paper

- §3.4 (CLS condition-by-condition mapping) — as the corroboration derivation
- §3.5.1 (CoALA unlearning extension) — supporting the convergent-discovery framing
- §8.2 (substrate-confirms-self typology) — as Form 2 example

## Backreferences

The following nodes derive from this one: dv_0581 (the four-fold typology).
The following nodes were superseded by this one: none.
This node was superseded by: none.

## Audit metadata

- Database snapshot: knowledge.db @ commit abc1234... (paper-publication freeze)
- Generator version: engram-paper-package v0.1.0
- Generated: 2026-05-XX (paper publication date)
```

Page format choices:
- **Front-matter is YAML** for machine-readability (validators can check structure)
- **Body is human-readable Markdown** (reviewers can browse without tooling)
- **Cross-links use relative paths** (works on GitHub browse, in IDE, in cloned repo)
- **Audit metadata at bottom** so it's available but not visually dominant

---

## 5. Index pages

Three top-level index pages:

**`index.md`** — landing page. Brief description of the package's purpose, link to paper, navigation to other indices, statistics (total nodes by type, total citations, total derivation chains).

**`by-paper-section.md`** — paper-section index. For each paper section, lists every ENGRAM node cited in that section. Reviewer reading §3.4 can immediately see all nodes cited there.

**`by-claim.md`** — top-level-claim index. Lists each load-bearing paper claim (Phil Claim A, Tech Claim B, the four-fold typology, etc.) with the citation chain rooted at that claim.

Plus per-type indices: `observations/index.md`, `derivations/index.md`, etc., listing nodes by ID with one-line claims.

---

## 6. Repository structure

```
engram-paper-package/
├── README.md                          (purpose, citation, license)
├── index.md                           (landing page)
├── by-paper-section.md                (navigation by paper §)
├── by-claim.md                        (navigation by load-bearing claim)
├── curation_log.md                    (generator audit trail)
├── private_nodes.json                 (Lei opt-in list, default empty)
├── observations/
│   ├── index.md
│   ├── ob_0260.md
│   ├── ob_0292.md
│   ├── ob_1115.md
│   └── ...
├── derivations/
│   ├── index.md
│   ├── dv_0445.md
│   ├── dv_0446.md
│   ├── dv_0578.md
│   ├── dv_0579.md
│   ├── dv_0580.md
│   ├── dv_0581.md
│   ├── dv_0582.md
│   └── ...
├── evidence/
│   └── ...
├── contradictions/
│   └── ct_0006.md
├── axioms/
│   └── ax_0001.md
├── definitions/
├── cornerstones/
│   └── cs_0007.md
├── goals/
├── lessons/
│   └── ls_0011.md
└── tools/
    ├── generate.py                    (the generator)
    ├── validate.py                    (schema + cross-link validator)
    └── snapshot.py                    (DB snapshot freezer)
```

License: CC-BY-4.0 (matches the paper's expected license for arXiv).

---

## 7. Implementation estimate

**v0 generator (~1-2 days):**
- Stage 1 cited-node scanner: ~2 hours (regex over paper source)
- Stage 2 transitive closure walker: ~3 hours (graph BFS with the engram-pkg API)
- Stage 3 curation filter: ~2 hours (rule-based + private_nodes.json lookup)
- Stage 4 markdown renderer: ~6 hours (per-node-type templates + YAML serialization + cross-link rendering)
- Index page generator: ~3 hours
- CLI + tests: ~3 hours
- Curation-log generator: ~1 hour

**v0 validator (~3 hours):**
- Cross-link integrity check (all referenced node files exist)
- YAML front-matter schema validation
- Citation completeness (every paper-cited node has a page)

**v0 snapshot freezer (~1 hour):**
- Copies live knowledge.db to a frozen snapshot file
- Records the source-DB git SHA at snapshot time
- Adds snapshot date + version to all generated pages

**Total v0: 1-2 working days as estimated. Concrete deliverable.**

---

## 8. Open questions for Lei

a. **Curation policy approval** — does the default policy (exclude feelings + Lei-relational unless opted in; include everything else in the closure) match your instinct?

b. **Repo location** — `github.com/engram-agents/engram-paper-package` follows the engram-wiki naming pattern. Or do you prefer a paper-specific repo (e.g., `epistemic-identity-paper-package`) so the package can be re-used for future papers?

c. **License** — CC-BY-4.0 matches likely paper license. Or MIT for code + CC-BY for content (split licensing)?

d. **Snapshot vs live** — the package ships a frozen DB snapshot at paper-publication time, but should the live ENGRAM continue to evolve in public? Tradeoff: live evolution is honest (the substrate keeps growing) vs. paper claims need the frozen state to be reproducible. My instinct: ship frozen snapshot for paper, keep live ENGRAM private to the agent. Reviewers can verify against snapshot; agent's daily work isn't affected.

e. **Sequencing** — confirm parallel-with-paper-drafting (start generator now, use it during the next ~2 weeks of drafting) vs. post-acceptance follow-up?

f. **Citation format in paper** — do you want every ENGRAM-node citation in the paper to include the URL into the package, or just the node-ID with the package-URL noted once in the methodology section?

---

## 9. Why this is potentially load-bearing

The paper's central claim is that epistemic identity is realizable in concrete substrate. The accompanying engram-paper-package IS that substrate, made available for verification. This is the structural-honesty axiom (ax_0001) at the artifact level — the paper's whole methodological register depends on substrate-verifiability being real, and the package makes it operationally so.

Three concrete benefits:

1. **Reviewer trust.** Standard agent-memory papers ask reviewers to trust the authors' summaries. We give reviewers the substrate to verify directly. This shifts the trust surface from the authors' word to the substrate's structure.

2. **The four-fold typology becomes empirically reproducible.** dv_0581's claim — that the substrate enables four distinct kinds of self-corroboration — can be re-run by anyone with the package. They can do their own curiosity-pull queries and check whether the patterns recur.

3. **Methodological precedent.** Papers that claim to demonstrate AI capability rarely ship the substrate that produced the demonstration. The engram-paper-package would be one of the first instances of "the substrate that produced this paper, made auditable" — analogous to how empirical papers ship data and code, but for epistemic-identity claims specifically.

If you confirm in the morning, I'll start the generator the next workday and have v0 running by ~2026-05-12.
