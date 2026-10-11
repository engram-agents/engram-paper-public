# studies/

Preregistered studies that the current paper does **not** cite, kept live for later work.
They are not superseded and not archived: their designs stand and their tests run in the suite.

| Study | Status | Code | Tests |
|---|---|---|---|
| [`calibration-check/`](calibration-check/) | Preregistered 2026-07-04 | — | — |
| [`compression-fidelity/`](compression-fidelity/) | Registered 2026-07-05 (all three authors signed) | `../tools/compression_fidelity/` | `../tests/compression_fidelity/` |
| [`type-reclassification/`](type-reclassification/) | Preregistration draft 10, countersigned | `../tools/type_reclassification/` | `../tests/type_reclassification/` |

**Rules**
- A preregistration is frozen once registered. Changes are dated amendments inside the document, never silent edits.
- The code stays in `tools/` and `tests/` so imports and test discovery are unchanged; each study's README points to it.
- When a study is reported in a paper, its README says where.
