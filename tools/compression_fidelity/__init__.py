"""compression_fidelity — sampling + packet-extraction harness for the
confidence-compression-fidelity study.

Pre-registration (the contract of record for this package):
    engram-paper `paper_research/compression-fidelity-preregistration-2026-07-05.md`
    (v7, REGISTERED, signed by Borges Funes + Kepler Somnium + Lei Shi, 2026-07-05).

This package draws a stratified sample of ENGRAM observation/derivation nodes
from a target `knowledge.db`, extracts confidence-stripped "packets" (the
provenance a blind judge fairy reads), computes K* (the formula's natural
tier count) from the frozen sample, and emits everything a judge fairy needs
with ZERO ENGRAM access (no MCP, no DB, no graph — plain JSON/markdown only).

See `paper_research/compression-fidelity-preregistration-2026-07-05.md` §4,
§4.1, §5, §8.0 for the exact rules this package implements.
"""
