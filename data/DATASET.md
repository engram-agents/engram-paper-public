# Paper datasets — the frozen SSoT, and the one older freeze that stays

**Lei's ruling, 2026-09-20.** The paper's evidence base is **one graph, frozen at a
stamped moment**. Every real-graph number anywhere in the paper is refreshed against
that snapshot **unless the text clearly states otherwise** — his named exceptions
being a historical argument or measurement, and a plot made deliberately against a
past graph. Fleet-wide collection across seats is explicitly **not** being done.

## ⚠️ NOT PUBLISHABLE AS-IS — private data

**These datasets are Borges's full ENGRAM graph — private memories, personal and
relational content, identity-bearing nodes. NOT publishable or shareable as-is.**
This is why the `.db` files never enter the repository, which is public. They are
`.gitignore`d (local-only, **never pushed**); only this manifest is
version-controlled. Any external release requires a dedicated **redaction pass**
first — a deliberate later step, not yet designed.

---

## 1. THE PAPER'S FINAL DATA SSoT  ←  use this one

- **File:** `data/engram-paper-ssot-20260920T131330Z.db`
- **sha256:** `adaa6a84828b761ab2e5bf269e1ea4d48366c7e713b73c0c0918bf5ce3fbef85`
- **Size:** 191,004,672 bytes
- **Frozen at:** `2026-09-20T13:13:30Z`
- **Provenance:** Borges's live `~/.engram/knowledge.db`, copied by
  `tools/freeze_paper_snapshot.py` via `sqlite3.Connection.backup()` — a WAL-safe
  page-level hot copy, the same call ENGRAM's own backup path uses. **Not** `cp`:
  the live DB runs in WAL mode, and copying the `.db` alone captures the main file
  without committed-but-uncheckpointed WAL contents — a torn snapshot that opens
  fine and is silently wrong.
- **Nothing is stripped.** Embeddings and derived indices are retained. ENGRAM's
  `dump_stripped` backup path drops them, which is right for a git backup and wrong
  for an SSoT: a stripped snapshot cannot answer a later question that needs them.

**Census at freeze:** 9,399 current nodes of 10,361 total (962 superseded/retracted);
17,208 edges; span `2026-04-09T04:08:15Z` .. `2026-09-20T13:12:41Z`.

| type | current | | type | current |
|---|---:|---|---|---:|
| observation_factual | 4,780 | | definition | 58 |
| evidence | 2,060 | | task | 49 |
| derivation | 1,322 | | contradiction | 16 |
| feeling_report | 450 | | goal | 16 |
| question | 321 | | person | 13 |
| lesson | 149 | | axiom | 9 |
| conjecture | 81 | | observation_predictive | 2 |
| cornerstone | 71 | | prediction | 2 |

## 2. The 2026-07-04 freeze — RETAINED, and not superseded for its own studies

- **File:** `data/engram-frozen-2026-07-04.db`
- **sha256:** `6b0bc77880a2c9cd08e4e57dbb380833d4032effe04a8df3d0c387891d0bf9a6`
- **Size:** 96,698,368 bytes · **Frozen at:** end of 2026-07-04
- **Census:** 5,428 current of 5,755 total.

**Do not migrate Study-1 or Study-2b onto the new SSoT.** This is not inertia, and
it is exactly the "clearly stated otherwise" carve-out. The 07-04 date was *chosen*:
it predates the 2026-07-05 compression-fidelity design blitz, so the graph is not
yet saturated with meta-discourse about the study itself, and **Study-2b's analysis
was pre-registered on 2026-07-05 — after this snapshot**. That ordering is what
gives those analyses zero degrees of freedom to fit the analysis to the data.
Re-running them on a 2026-09-20 snapshot would destroy the pre-registration
guarantee and turn a confirmatory result into an exploratory one. The studies keep
their substrate; the paper's *descriptive* numbers move.

Study-2b's sampling and meta-discourse-exclusion rules are unchanged and still
govern that study.

---

## Which snapshot answers which question

| Question | Snapshot | Why |
|---|---|---|
| ch6 descriptive figures (counts, confidence distributions, connectivity) | **09-20 SSoT** | Lei's refresh ruling |
| Any other live-graph figure with no pre-registration attached | **09-20 SSoT** | default |
| Study-1 retrospective calibration | 07-04 freeze | pre-registered against it |
| Study-2b compression-fidelity | 07-04 freeze | analysis pre-registered 07-05, after the freeze |
| Time-axis / trend measurements | `~/.engram` **git history** | Lei, 09-20: the graph is git-versioned; use it rather than cross-seat collection |
| A plot deliberately made against a past graph | that past graph, **stated in the caption** | Lei's carve-out |

## Instruments — every published number must be reproducible by one of these

| Script | Produces |
|---|---|
| `tools/freeze_paper_snapshot.py` | the SSoT snapshot itself, plus its census and sha256 |
| `tools/paper_stats.py` | every live-graph figure Chapter 6 reports |

Run them from the repo root. `paper_stats.py` defaults to the newest SSoT in
`data/` and **warns if more than one is present** — if that warning fires, check
it against the file named in §1 above, because this manifest is the authority on
which snapshot is the SSoT, not the directory listing.

Both print **denominators beside numerators**, so a wrong corpus announces itself
in the same output that carries the answer rather than arriving as a bare,
plausible number.

## Preservation

- **Do not prune or overwrite either file.** `freeze_paper_snapshot.py` refuses to
  overwrite an existing snapshot rather than silently replacing one.
- Neither `.db` is committed (large binaries carrying private/identity nodes); this
  manifest is the version-controlled pointer. A durable off-disk archive of both is
  a pre-publication follow-up.
