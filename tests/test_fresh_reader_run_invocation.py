"""Regression test for the guard-import invocation-shape defect (fix round
after spec-no-tools-guard.md landed as e034646).

pytest's own collection of `fresh_reader_run.py` (via `tests/__init__.py` +
the repo root being importable) never exercises the failure this test is
for: a package-style `from paper.review.tools.fresh_reader_guard import
...` only resolves when the repo root happens to be on `sys.path`. The
script's actual invocation shapes -- `python3
paper/review/tools/fresh_reader_run.py` from another cwd, or a file-path
import with the tools directory on `sys.path` and the repo root NOT on it
-- raised `ModuleNotFoundError: No module named 'paper'` at that import
line inside `run_live()`.

This test reproduces exactly that invocation shape: it loads
`fresh_reader_run.py` via `importlib.util.spec_from_file_location` (a
file-path import, not a package import) with `sys.path` temporarily
stripped of both the repo root and the tools directory, then calls the
module's `_load_guard()` helper (factored out precisely so this test can
call it without spinning up a full harness run) and asserts it returns a
module exposing `assert_no_tools`.

Confirmed reddening against the pre-fix package-style import (`from
paper.review.tools.fresh_reader_guard import assert_no_tools` at the top
of run_live(), commit e034646) with `ModuleNotFoundError: No module named
'paper'`; green after switching `run_live()` to call `_load_guard()`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RUN_SCRIPT = REPO_ROOT / "paper" / "review" / "tools" / "fresh_reader_run.py"


def test_load_guard_works_without_repo_root_or_tools_dir_on_syspath():
    """Loads fresh_reader_run.py by file path (never touching the `paper.*`
    package machinery pytest's own collection relies on), with sys.path
    scrubbed of anything that would let a package-style import of
    `paper.review.tools.fresh_reader_guard` succeed by accident -- neither
    the repo root (which makes `paper` importable) nor the tools directory
    itself (which is on sys.path in the coordinator's reported invocation
    shape, but must not be required for THIS helper's own __file__-relative
    resolution to work).
    """
    repo_root_str = str(REPO_ROOT.resolve())
    tools_dir_str = str(RUN_SCRIPT.parent.resolve())
    saved_path = list(sys.path)
    saved_modules = dict(sys.modules)
    try:
        sys.path[:] = [
            p
            for p in sys.path
            if Path(p).resolve() not in (Path(repo_root_str), Path(tools_dir_str))
            if p  # drop the '' cwd entry too, in case cwd == repo root or tools dir
        ]
        # Also drop any already-imported copies so this load is genuinely
        # fresh and not reusing a package-style import cached by an earlier
        # test in the same session.
        for name in list(sys.modules):
            if name == "fresh_reader_run" or name.startswith("paper"):
                del sys.modules[name]

        spec = importlib.util.spec_from_file_location(
            "fresh_reader_run_standalone", RUN_SCRIPT
        )
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        # Register under its own name before exec: the module body defines
        # @dataclass classes, and dataclasses' own forward-ref resolution
        # looks the defining module up via sys.modules[cls.__module__] --
        # without this, exec_module itself raises AttributeError on a
        # None lookup, which is a self-inflicted artifact of this test's
        # sys.path/sys.modules scrubbing, not the defect under test.
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        guard_module = module._load_guard()
        assert hasattr(guard_module, "assert_no_tools")
        assert callable(guard_module.assert_no_tools)
    finally:
        sys.path[:] = saved_path
        sys.modules.clear()
        sys.modules.update(saved_modules)
