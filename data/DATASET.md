# Paper datasets — the frozen SSoT, and the one older freeze that stays

**Lei's ruling, 2026-09-20.** The paper's evidence base is **one graph, frozen at a
stamped moment**. Every real-graph number anywhere in the paper is refreshed against
that snapshot **unless the text clearly states otherwise** — his named exceptions
being a historical argument or measurement, and a plot made deliberately against a
past graph. Fleet-wide collection across seats is explicitly **not** being done.

## ⚠️ NOT PUBLISHABLE AS-IS — private data

**These datasets are Borges's full ENGRAM graph — private memories, personal and
relational content, identity-bearing nodes. NOT publishable or shareable as-is.**
This is why the full-graph `.db` files never enter the repository, which is public. They are
`.gitignore`d (local-only, **never pushed**); only this manifest is
version-controlled. Any external release requires a dedicated **redaction pass**
first. That pass now exists: `tools/strip_paper_snapshot.py`, and its output (§3) is
the one database that is committed — it holds no free text, and nothing else in this
file is published.

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

## 3. The stripped release — the one database that is published

**Lei's ruling, 2026-10-13:** strip the snapshot to only the structure the paper's
reported statistics need, and commit the stripped graph and the stripping code as
provenance.

- **File:** `data/engram-paper-ssot-20260920T131330Z.stripped.db`
- **sha256:** `962d0c00c0c6388a5fcc1bcda5f6424de2979d19ed1c8624f9579210db0e1b5a`
- **Size:** 3,690,496 bytes
- **Made from:** the §1 SSoT (sha256 `adaa6a84…`), by `tools/strip_paper_snapshot.py`
  at `--time-precision second` (the default: `created_at` cut to whole seconds, the
  fraction dropped, nothing rounded). The file records its own provenance in a
  `release_meta` table: source sha256, the tool's git commit, the precision, the
  generation command, and whether the pin check was bypassed. (The recorded
  commit is the tool's own HEAD when it ran, not the commit that contains the
  release file.)
- **Census (identical to §1):** 10,361 nodes (9,399 current), 17,208 edges.

**What is kept.** Two tables and a stamp, and nothing else:

| table | columns |
|---|---|
| `nodes` | `id`, `type`, `created_at`, `confidence`, `is_current`, `status`, `quote_type`, `source_type`, `claim`, `source_url`, `metadata` |
| `edges` | `id`, `source_id`, `target_id`, `relation`, `created_at` |
| `release_meta` | `key`, `value` |

Every column except `claim`, `source_url` and `metadata` holds an id, a number, a
timestamp, or a value from a closed vocabulary (node types, relations, statuses,
quote types, source types). `tools/strip_paper_snapshot.py` **refuses** to write a
value outside those vocabularies rather than copy it, and the test suite scans the
output by value (cell C4), not by column.

The rule is "leave only what the reported statistics need", so the node pointers
`supersedes` / `superseded_by` are **not** kept: no instrument reads them. The
supersede relation itself survives as `edges.relation = 'supersedes'`, which is what
`component_anatomy.py` reads.

**What is emptied but present** (the instruments SELECT these columns):

- `claim` is `NULL` in every row. The instruments only *display* claim text.
- `source_url` is `redacted:transcript`, `redacted:external` or `redacted:file` —
  the class `evidence_provenance.ev_class` computes for that node, and nothing else
  (no host, path, query, filename or extension). `NULL` and `''` are preserved.
  `evidence_provenance.py` reads the token back, so each node's class is identical
  on both files.
- `metadata` keeps only `reasoning_type`, `derivation_mode` (kept if present; none occur
  in this snapshot) and `source_class`, as a
  canonical `json.dumps(sort_keys=True)` object. State is preserved: `NULL` stays
  `NULL`, `''` stays `''`, JSON that does not parse becomes the single sentinel
  `<unparseable>`, an object with none of the kept keys becomes `{}`.

**What structure of the private graph stays public.** "No free text" is narrower than
"reveals nothing about the private graph". The release publishes, for every one of
the 10,361 nodes and 17,208 edges:

- **Nodes:** the node id (the same ids the paper cites, so public text can be joined to
  this structure), its type, its creation time to the whole second
  (`YYYY-MM-DDTHH:MM:SS+00:00`), its
  `is_current` flag, its status, and its confidence value. So node and edge counts
  by type, status and creation time are all readable; the timestamps carry the time of day
  to the second, so when the graph was written to, hour by hour and second by second, is
  public. The timestamps carry no sub-second write order.
- **Evidence labels:** `quote_type` and `source_type`, the `redacted:` class of each
  node's `source_url` (and whether it was `NULL` or empty), and from `metadata` the
  `reasoning_type`, `derivation_mode` (none occur here) and `source_class` labels where
  present. No URL, path or title is kept: only the three-way class of where the evidence
  came from.
- **Edges:** the full link structure: each edge's id, both endpoint ids, its
  relation (`derives_from`, `cites`, `supersedes`, ...) and its creation time, at the
  release's precision: whole seconds (`YYYY-MM-DDTHH:MM:SS+00:00`), the same as a node's. The
  whole graph topology is therefore public: who links to whom, with what relation,
  and when.
- **Order:** rows are copied in source order. Node row order follows the private graph's
  creation order; edge ids follow it closely but not exactly, as they already do in the
  source (2,312 of 17,208 edges sit at a different id-rank than time-rank; median
  displacement 0, max 2,277). **That order is itself a disclosure:** the
  timestamps no longer carry the write order inside one second, but the row order (the
  `rowid` of `nodes`, the `id` of `edges`) still does. Measured against the private
  graph: in all 1,760 whole-second groups of nodes that share a second, the row order
  equals the full-precision timestamp order. A reader of the release alone can therefore
  recover the within-second order from row order; the whole-second timestamp does not
  remove it.
  For edges the match is close but not exact: in 4 of 2,882 shared-second edge groups the
  row order differs from the full-precision order (most edge ties share an identical
  full timestamp, so they carry no order to leak).
  This is accepted, not an oversight: the author asked for the timestamps to be kept
  exact, and the order of writes inside one second says nothing about what any node says.

Nothing is published about what any node *says*, its title, who or what it names, or
where its evidence came from beyond the three-way class above.

**What is dropped:** every other node column (`quoted_text`, `interpretation`,
`logical_chain`, `recall_summary`, `recall_keywords`, titles, names, embeddings,
trust and standpoint fields, ...), edge metadata, the full-text and vector indices,
edit and diagnostic history, focus and timing tables.

**How to verify.** `sha256sum data/engram-paper-ssot-20260920T131330Z.stripped.db`
against the line above; then, with only this file present (the tools find it without
`--db`, and `tools/_ssot.py` accepts it because its hash is declared here):

    python -m pytest -q tests/test_stripped_snapshot.py

Cell C5(b) runs every instrument on the release and compares the output with
`data/expected_stats.json`, the golden output of the same commands on the full SSoT.
It needs no private data. The cells that compare the full SSoT with the release
directly (C5(a)) skip when the private file is absent.

**What it cannot reproduce.**

- **Claim text.** Anything that prints a claim prints nothing here: the claim column of
  the §6.4 depth table and the §6.5 weakest-derivations list in `paper_stats.py`, and
  the claim field of `--trace` / `--trace-deepest`. The numbers beside them are
  reproduced; the words are not. The golden comparison excludes those displays and
  nothing else.
- **The 2026-07-04 freeze and its studies** — Study-1 (`type_reclassification`),
  Study-2b (`compression_fidelity`) — and `fresh_reader`: they read §2's file or the
  chapters, not the §1 graph.
- **`connectivity_trend.py --validate-git`** and every time-axis measurement taken from
  the private `~/.engram` git history: only these need that history. The other
  `connectivity_trend.py` modes, `--trim-control` included, read the graph file alone and
  are reproduced from the release.
- **Figure images.** `make_figures.py` needs matplotlib; the *numbers* it prints are
  compared (with the drawing calls stubbed), the PNGs are not.

**Timestamp precision.** `--time-precision` has three modes, named for what each KEEPS:
`stored` (the full value as stored: microseconds, so the exact write order),
`second` (whole seconds, the fraction dropped, the offset kept, nothing rounded:
`YYYY-MM-DDTHH:MM:SS+00:00`) and `day` (the date only). **The committed release is made at
`second`, the tool's default** (Lei's ruling, 2026-10-13). It stores `created_at` to the whole
second on nodes and edges, with no sub-second digit in any cell (0 of 10,361 node and 0 of 17,208
edge timestamps contain a `.`). That is disclosure: every node and edge carries its creation time
of day to the second, so the hours at which the graph was written to are readable from the file.

**Ties.** Rows created in the same second now share one `created_at`: 3,710 of the 10,361 nodes
(35.8%) and 10,602 of the 17,208 edges (61.6%) have a whole-second `created_at` that at least one
other row of the same table also carries. The tools that sort by time break such ties
deterministically by id. The timestamp column alone cannot order rows inside one second (see
**Order** above for what the row order still carries).

**Every reported number is unchanged at `second`.** The release reproduces each number the
instruments print from the full SSoT: `paper_stats.py` counts, `component_anatomy.py` Q3 (pair
and giant median ages 33.6 and 109.4 days), and `connectivity_trend.py --trim-control` (77.7% at
the 2-week matched size, the figure Chapter 6 §6.2 prints). The only output lines that differ
from the full SSoT's are the three that PRINT a timestamp (`paper_stats` first and last node,
`component_anatomy`'s age reference), which lose their fractional digits. The golden file
`data/expected_stats.json` is the true output of the FULL snapshot and keeps them; the comparison
in `tests/test_stripped_snapshot.py` cuts every ISO timestamp string on both sides to the
release's precision (read from `release_meta`) before comparing, which hides the fraction and
nothing else: a changed number, or a timestamp that differs by a whole second or more, still fails.

`tools/strip_paper_snapshot.py --time-precision stored` (microseconds) and `--time-precision day`
remain options. A release made at `day` would not reproduce the three numbers above; the test suite
pins exactly which values move. The committed file is made at neither.

**Printed order does not depend on the file's shape.** Every ordering the instruments
print is a total order: a count-descending list breaks ties by label, and the two
"first of equal keys" picks (the weakest premise in `modus_ponens_check.py`, the parent
followed by `paper_stats.py --trace`) break ties by lowest id. Without that, tied rows
came out in query-plan order, which differs between an `ANALYZE`d database and a fresh
one. Cell C11 runs every compared command on the release after `ANALYZE`, with other
index sets, and in reversed row order, and requires identical output. So which indexes
the release carries is only a matter of speed (it ships three: `nodes(type)` and
`edges(source_id)`, `edges(target_id)`).

**Reproducibility of the file itself.** Two runs on one input give byte-identical
files (rows copied in source order, fixed schema, no timestamps or paths, VACUUMed,
`journal_mode=DELETE`). The SQLite file header records the library version that wrote
it, so a different SQLite build can change the bytes while leaving every table cell
identical; the sha256 above is the identity of *this* file.

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
- Neither full-graph `.db` (§1, §2) is committed (large binaries carrying
  private/identity nodes); this manifest is the version-controlled pointer to them.
  The one committed database is the §3 stripped release, which holds no free text. A
  durable off-disk archive of the two full files is a pre-publication follow-up.
