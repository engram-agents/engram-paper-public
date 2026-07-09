"""Ensures the repo root is on sys.path so `tools.type_reclassification`
and `tools.compression_fidelity` import as (namespace-)packages regardless
of pytest's invocation directory / rootdir-insertion mode. `tools/` itself
has no `__init__.py` (same layout as the existing `compression_fidelity`
package) and is treated as an implicit namespace package.

All test files in this package standardize on the `tools.type_reclassification.X`
absolute-import form (reviewer-fairy caught that mixing this with a bare
`type_reclassification.X` form creates two distinct module identities for
the same source file — `d1 is d2` False, `isinstance` mismatches across the
two import paths — a latent landmine even though nothing crossed the two
identities at the time). Do not reintroduce the bare form without also
reverting this file's single-path setup.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
