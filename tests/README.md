# tests/

```
pip install pytest -r requirements.txt -r tools/compression_fidelity/requirements.txt
python -m pytest -q tests
```

Both requirements files are needed: the compression-fidelity tests import `numpy` and `ckwrap`, which the top-level file does not list. One test skips unless the optional `zstandard` package is installed; that skip is expected.

What they check, among other things: the render reproduces `paper/release/` byte for byte; every citation resolves; the glossary stays within its budget; the statistics tools trace back to the snapshot; the study harnesses behave as their preregistrations specify.
