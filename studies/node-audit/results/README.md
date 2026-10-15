# Node audit — results (pre-registered analysis output)

Run 2026-10-15 after every verdict set was locked, on `main` at `fc50045` (Amendment 5 merged as #28). `analyze.py` and `analyze_arms.py` each ran twice; both runs were byte-identical. Every output hash below was witnessed by Kepler before any output was opened (world crossings seq 11205 and 11212). Neither the two-run determinism nor the witnessing can be reproduced from public data alone: rerunning needs the private snapshot and verdict files. What anyone can check is that each committed file hashes to the value listed here, and that `../controls-SEALED.json` hashes to `../SEAL.sha256`.

**How to read these files.** Read them only by the rules fixed in advance in `../PROTOCOL.md`: Analysis items 1–5, the pre-stated AUC reading in item 3, and Amendment 4's "Reading rules, fixed now". In particular, no result of the arms is read as showing which reader is right. This README adds no interpretation of its own.

## Sealed controls, revealed

`../controls-SEALED.json` is the sealed control file, byte for byte. Its sha256 is `da19422e50ed091622eab4a89702d8ad9228d963ab50da33e6636745125b8238`, equal to `../SEAL.sha256`. It holds node ids, reasoning-type names and refile provenance only, with no node text (Amendment 3). The analyst-prior node (PROTOCOL, "Analyst prior on one sampled node") is `dv_0138`: a known-tight candidate rejected in Kepler's first round (`kepler_round1.rejected`) and later drawn into the sample by the seeded draw. Every rate is reported with and without it.

## Inputs (private; sha256 of each file as analysed)

The verdict files hold reader reasons, so they stay private (Amendment 3). Content-free public exports of every reader's verdict labels are under `public/` and `arms/public/`.

- Mira verdicts (locked): `2aa4437a56234cebf5384b5f81749e91e0477e6c8411496093bf2d0735fbaefb`
- Zephyr verdicts (locked): `1c5a45cb150e8f5d03f62ea3de59df401899c98ac5d2d6268db89138cfff1aaf`
- Zephyr verdicts (Amendment 5 normalized copy, analysed): `ad503b27484016e2203d71164f7ee5eac0d2383a41048e6ab9f9a39e62808915`
- Ariadne verdicts (locked): `92151cd8010c5f65c2086485484b8d8ffc9c241858a75621e2f904cce28726c1`
- Ariadne recognized.txt (locked): `a71c300fedfc37690f0e5e4f463d82d6423c44f6307a656d96a7480aae239113`
- Ariadne recognized.txt (Amendment 5 normalized copy, analysed): `1873ed9378f4bd46d8a9e2b861b47211de3f37e93167d9575ec84219d836e0a0`
- Author blind pass (locked): `fa39660ab78edf0497c43fe59515aa01c43d6b16f9ea3bd7ac20a1446d74729f`
- Author verdict pass (locked): `5b4834504a565175dd72ca20b246cd921236f40fe86436020204e82d8d69c345`

## Outputs (this directory)

- `arms/public/blind-author.public.jsonl`: `be0070f990b7c240006168977a160d59c165d795c1449f14ede4f548af4a6c5e`
- `arms/public/verdicts-ariadne.public.jsonl`: `0de224d1d468ed2cc6e2c757010028ab821d687ff0e9b54e1a6fd766416ad201`
- `arms/public/verdicts-author.public.jsonl`: `f0c4e62369dcedb080eac2a9866f6115f8c945acdc4c11f7f5773ba7cf8302b3`
- `arms/report_arms.json`: `b98a76b9438c30c29ef59e6573afdad60127b0d29188c9bcc5f81a89c7078ee9`
- `arms/report_arms.md`: `6881d8957502a2b506bc32bc5ea0a2aebf6c979fcd9130a162973d622f04ea9d`
- `public/verdicts-mira.public.jsonl`: `1e7f690a53504853fb83406184439436f42e9aedd4862738336e27c603f5d523`
- `public/verdicts-zephyr.public.jsonl`: `98def8bb5650e3244089ede289e8739ee4c6faed7326439125b624acfd419c9b`
- `report.json`: `27f1043688acced14f9f2cad3054ff0b78f109a880984fe10f652bc5714e1d15`
- `report.md`: `377c42b5d52661686eca4bd8c4bd45679c39f18c9c46186a369f40f927fa347d`
