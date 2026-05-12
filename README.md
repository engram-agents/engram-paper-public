# engram-paper — ENGRAM foundational paper

The paper-public workspace for the ENGRAM foundational paper. Two artifacts, one source of truth:

1. **The paper-engram** — the argument structure as an ENGRAM dv-chain. Source of truth.
2. **The publishable prose article** — the rendered, human-readable artifact. Generated from the paper-engram + chapter drafts.

This repo is split from `engram-agents/kg-protocol-for-ai` (2026-05-12) so the paper material can eventually be made public without leaking private workshop history.

## Layout

- **`paper_research/`** — comparative scans, primary-source verifications, spine doc, working memos, draft chapter sections, citation database (`citations.bib` + `citations.manifest`).
- **`paper_draft/`** — full chapter drafts. The publishable prose article (or its precursors).
- **`tools/`** — bibliography tooling (`bib_bootstrap.py`, `check_citations_consistency.py`).

## What stays in kg

- `archive/` — historical design docs and superseded specs (private workshop history).
- `CLAUDE.md`, `README.md` — kg-specific instructions for agents working in that repo.

## Status

Newly split. Initial migration preserves kg content as-of 2026-05-12. Pre-public-share scrub (working-draft artifacts, internal node-ID references, byline cleanup) is a separate pass before any external sharing.

## Open issues

- **#1** — Paper flow plan (Lei's chapter outline 2026-05-12)
- **#2** — Paper-engram-first plan (DV-first design proposal)
