# Node audit analysis report: Arm A (author) and Arm B (Ariadne)

## Reading rules (PROTOCOL.md Amendment 4, "Reading rules, fixed now", verbatim)

- **Author agrees** is read as an error made at filing time. The design cannot attribute it to a cause. Time pressure, an earlier model's habits, and the project's own changing practice over those months are all confounded, because in one author's transcripts each model occupied one continuous period. The per-model breakdown is reported, and it is not read as attribution.
- **Author disagrees** is read as a standing disagreement between the author and that reader.
- **Ariadne vs Mira and Zephyr** is read as a difference of lineage plus exposure, not of lineage alone. Being of the author's lineage and having read the author's posts arrive together in her.
- **Ariadne vs the author** is read as an authorship difference within one lineage, with the same exposure caveat.
- No result of these arms is read as showing which reader is right. Counts are reported beside every rate, and the small-stratum rule applies.

Seed `2026-10-14-node-audit`; analyst-prior node `dv_0138`; bootstrap resamples 10000; small-stratum rule: fewer than 10 nodes report counts only. Controls are excluded from every rate. 5 sampled nodes mention a control (the private manifest).

Pass labels: a pass labelled "derived" is a union of two pre-registered exclusions and is not itself named in the protocol; items labelled "descriptive" are not pre-registered. Unlabelled passes are the ones the protocol names.

## Input files (sha256)

- author_blind: `fa39660ab78edf0497c43fe59515aa01c43d6b16f9ea3bd7ac20a1446d74729f`
- author_verdicts: `5b4834504a565175dd72ca20b246cd921236f40fe86436020204e82d8d69c345`
- ariadne: `92151cd8010c5f65c2086485484b8d8ffc9c241858a75621e2f904cce28726c1`
- ariadne_recognized: `1873ed9378f4bd46d8a9e2b861b47211de3f37e93167d9575ec84219d836e0a0`
- mira: `2aa4437a56234cebf5384b5f81749e91e0477e6c8411496093bf2d0735fbaefb`
- zephyr: `ad503b27484016e2203d71164f7ee5eac0d2383a41048e6ab9f9a39e62808915`
- controls: `da19422e50ed091622eab4a89702d8ad9228d963ab50da33e6636745125b8238`
- manifest: `aacfbdb7a546a8ad02ef18688e119cda769a39e02585e7047afefacbd273ee92`
- packet: `6acf45bcc4e424079ff40cd7513312dfd965e6208bce2ab84221ad934bc5d061`
- db: `adaa6a84828b761ab2e5bf269e1ea4d48366c7e713b73c0c0918bf5ce3fbef85`
- drawn: `3981d1945b121060b6bd8b6832c6ce4d969249bf5cfa094c2d245ba57f5cccea`
- filing_model: `8b9dda965932472056b010d0ca6ba5b31cd778be613de93772677ffe16cab033`

## Validation

- 200 sampled nodes, 11 controls, 211 packet nodes. Rows: blind 140, author 200, ariadne 211, mira 211, zephyr 61. All rows valid; none dropped.

## Mention set and recognized set (counts only)

- Mention set (packet node blocks matching `ariadne|\bari\b`, case-insensitive): 41 of 211; the protocol's measured figure is 41 of 211 (not asserted here).
- recognized 43, mention 41, both 41, recognized-only 2, mention-only 0, late 2; control ids counted in recognized 3, mention 3.

## Arm A blind pass: agreement with the declared type, and self-naming

### pass: all

- Status of the Wilson intervals below: descriptive (not pre-registered)
- Status of the declared -> blind table below: descriptive (not pre-registered)

- overall: 52/140 = 37.1% [Wilson 29.6%, 45.4%]
- per stratum:
  - derivation:abductive_best_explanation: 11/30 = 36.7% [Wilson 21.9%, 54.5%]
  - derivation:abductive_elimination: 1/2 (counts only: fewer than 10)
  - derivation:authority_expert: 1/2 (counts only: fewer than 10)
  - derivation:deductive_disjunctive: 0/2 (counts only: fewer than 10)
  - derivation:deductive_hypothetical_syllogism: 0/4 (counts only: fewer than 10)
  - derivation:deductive_modus_ponens: 25/29 = 86.2% [Wilson 69.4%, 94.5%]
  - derivation:deductive_modus_tollens: 2/2 (counts only: fewer than 10)
  - derivation:inductive_analogy: 9/13 = 69.2% [Wilson 42.4%, 87.3%]
  - derivation:inductive_causal: 0/2 (counts only: fewer than 10)
  - derivation:inductive_enumeration: 1/2 (counts only: fewer than 10)
  - derivation:inductive_generalization: 2/50 = 4.0% [Wilson 1.1%, 13.5%]
  - derivation:inductive_statistical: 0/2 (counts only: fewer than 10)
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: 6/35 = 17.1% [Wilson 8.1%, 32.7%]; less certain (hours_before > 24): 0
  - claude-opus-4-7: 11/47 = 23.4% [Wilson 13.6%, 37.2%]; less certain (hours_before > 24): 6
  - claude-opus-4-8: 15/29 = 51.7% [Wilson 34.4%, 68.6%]; less certain (hours_before > 24): 0
  - claude-opus-5: 20/29 = 69.0% [Wilson 50.8%, 82.7%]; less certain (hours_before > 24): 0
- declared -> blind:
  - abductive_best_explanation -> abductive_best_explanation: 11
  - abductive_best_explanation -> abductive_elimination: 6
  - abductive_best_explanation -> deductive_modus_ponens: 9
  - abductive_best_explanation -> deductive_modus_tollens: 3
  - abductive_best_explanation -> inductive_analogy: 1
  - abductive_elimination -> abductive_elimination: 1
  - abductive_elimination -> deductive_modus_ponens: 1
  - authority_expert -> authority_expert: 1
  - authority_expert -> deductive_modus_ponens: 1
  - deductive_disjunctive -> abductive_elimination: 2
  - deductive_hypothetical_syllogism -> deductive_modus_ponens: 4
  - deductive_modus_ponens -> deductive_hypothetical_syllogism: 1
  - deductive_modus_ponens -> deductive_modus_ponens: 25
  - deductive_modus_ponens -> deductive_modus_tollens: 1
  - deductive_modus_ponens -> inductive_enumeration: 2
  - deductive_modus_tollens -> deductive_modus_tollens: 2
  - inductive_analogy -> abductive_best_explanation: 1
  - inductive_analogy -> deductive_modus_ponens: 3
  - inductive_analogy -> inductive_analogy: 9
  - inductive_causal -> abductive_best_explanation: 1
  - inductive_causal -> deductive_modus_ponens: 1
  - inductive_enumeration -> inductive_analogy: 1
  - inductive_enumeration -> inductive_enumeration: 1
  - inductive_generalization -> abductive_best_explanation: 12
  - inductive_generalization -> authority_consensus: 3
  - inductive_generalization -> authority_expert: 1
  - inductive_generalization -> deductive_modus_ponens: 18
  - inductive_generalization -> deductive_modus_tollens: 1
  - inductive_generalization -> inductive_analogy: 9
  - inductive_generalization -> inductive_causal: 1
  - inductive_generalization -> inductive_enumeration: 3
  - inductive_generalization -> inductive_generalization: 2
  - inductive_statistical -> deductive_modus_ponens: 2
- self-naming (claim or chain contains the declared type): 16 of 140; agreement without them: 47/124 = 37.9% [Wilson 29.8%, 46.7%]

### pass: without_prior

- Status of the Wilson intervals below: descriptive (not pre-registered)
- Status of the declared -> blind table below: descriptive (not pre-registered)

- overall: 52/139 = 37.4% [Wilson 29.8%, 45.7%]
- per stratum:
  - derivation:abductive_best_explanation: 11/29 = 37.9% [Wilson 22.7%, 56.0%]
  - derivation:abductive_elimination: 1/2 (counts only: fewer than 10)
  - derivation:authority_expert: 1/2 (counts only: fewer than 10)
  - derivation:deductive_disjunctive: 0/2 (counts only: fewer than 10)
  - derivation:deductive_hypothetical_syllogism: 0/4 (counts only: fewer than 10)
  - derivation:deductive_modus_ponens: 25/29 = 86.2% [Wilson 69.4%, 94.5%]
  - derivation:deductive_modus_tollens: 2/2 (counts only: fewer than 10)
  - derivation:inductive_analogy: 9/13 = 69.2% [Wilson 42.4%, 87.3%]
  - derivation:inductive_causal: 0/2 (counts only: fewer than 10)
  - derivation:inductive_enumeration: 1/2 (counts only: fewer than 10)
  - derivation:inductive_generalization: 2/50 = 4.0% [Wilson 1.1%, 13.5%]
  - derivation:inductive_statistical: 0/2 (counts only: fewer than 10)
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: 6/34 = 17.6% [Wilson 8.3%, 33.5%]; less certain (hours_before > 24): 0
  - claude-opus-4-7: 11/47 = 23.4% [Wilson 13.6%, 37.2%]; less certain (hours_before > 24): 6
  - claude-opus-4-8: 15/29 = 51.7% [Wilson 34.4%, 68.6%]; less certain (hours_before > 24): 0
  - claude-opus-5: 20/29 = 69.0% [Wilson 50.8%, 82.7%]; less certain (hours_before > 24): 0
- declared -> blind:
  - abductive_best_explanation -> abductive_best_explanation: 11
  - abductive_best_explanation -> abductive_elimination: 6
  - abductive_best_explanation -> deductive_modus_ponens: 8
  - abductive_best_explanation -> deductive_modus_tollens: 3
  - abductive_best_explanation -> inductive_analogy: 1
  - abductive_elimination -> abductive_elimination: 1
  - abductive_elimination -> deductive_modus_ponens: 1
  - authority_expert -> authority_expert: 1
  - authority_expert -> deductive_modus_ponens: 1
  - deductive_disjunctive -> abductive_elimination: 2
  - deductive_hypothetical_syllogism -> deductive_modus_ponens: 4
  - deductive_modus_ponens -> deductive_hypothetical_syllogism: 1
  - deductive_modus_ponens -> deductive_modus_ponens: 25
  - deductive_modus_ponens -> deductive_modus_tollens: 1
  - deductive_modus_ponens -> inductive_enumeration: 2
  - deductive_modus_tollens -> deductive_modus_tollens: 2
  - inductive_analogy -> abductive_best_explanation: 1
  - inductive_analogy -> deductive_modus_ponens: 3
  - inductive_analogy -> inductive_analogy: 9
  - inductive_causal -> abductive_best_explanation: 1
  - inductive_causal -> deductive_modus_ponens: 1
  - inductive_enumeration -> inductive_analogy: 1
  - inductive_enumeration -> inductive_enumeration: 1
  - inductive_generalization -> abductive_best_explanation: 12
  - inductive_generalization -> authority_consensus: 3
  - inductive_generalization -> authority_expert: 1
  - inductive_generalization -> deductive_modus_ponens: 18
  - inductive_generalization -> deductive_modus_tollens: 1
  - inductive_generalization -> inductive_analogy: 9
  - inductive_generalization -> inductive_causal: 1
  - inductive_generalization -> inductive_enumeration: 3
  - inductive_generalization -> inductive_generalization: 2
  - inductive_statistical -> deductive_modus_ponens: 2
- self-naming (claim or chain contains the declared type): 16 of 139; agreement without them: 47/123 = 38.2% [Wilson 30.1%, 47.0%]

### pass: without_manifest

- Status of the Wilson intervals below: descriptive (not pre-registered)
- Status of the declared -> blind table below: descriptive (not pre-registered)

- overall: 52/135 = 38.5% [Wilson 30.7%, 46.9%]
- per stratum:
  - derivation:abductive_best_explanation: 11/30 = 36.7% [Wilson 21.9%, 54.5%]
  - derivation:abductive_elimination: 1/2 (counts only: fewer than 10)
  - derivation:authority_expert: 1/2 (counts only: fewer than 10)
  - derivation:deductive_disjunctive: 0/2 (counts only: fewer than 10)
  - derivation:deductive_hypothetical_syllogism: 0/4 (counts only: fewer than 10)
  - derivation:deductive_modus_ponens: 25/29 = 86.2% [Wilson 69.4%, 94.5%]
  - derivation:deductive_modus_tollens: 2/2 (counts only: fewer than 10)
  - derivation:inductive_analogy: 9/13 = 69.2% [Wilson 42.4%, 87.3%]
  - derivation:inductive_causal: 0/2 (counts only: fewer than 10)
  - derivation:inductive_enumeration: 1/2 (counts only: fewer than 10)
  - derivation:inductive_generalization: 2/47 = 4.3% [Wilson 1.2%, 14.2%]
  - derivation:inductive_statistical: 0/0 (counts only: fewer than 10)
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: 6/35 = 17.1% [Wilson 8.1%, 32.7%]; less certain (hours_before > 24): 0
  - claude-opus-4-7: 11/42 = 26.2% [Wilson 15.3%, 41.1%]; less certain (hours_before > 24): 5
  - claude-opus-4-8: 15/29 = 51.7% [Wilson 34.4%, 68.6%]; less certain (hours_before > 24): 0
  - claude-opus-5: 20/29 = 69.0% [Wilson 50.8%, 82.7%]; less certain (hours_before > 24): 0
- declared -> blind:
  - abductive_best_explanation -> abductive_best_explanation: 11
  - abductive_best_explanation -> abductive_elimination: 6
  - abductive_best_explanation -> deductive_modus_ponens: 9
  - abductive_best_explanation -> deductive_modus_tollens: 3
  - abductive_best_explanation -> inductive_analogy: 1
  - abductive_elimination -> abductive_elimination: 1
  - abductive_elimination -> deductive_modus_ponens: 1
  - authority_expert -> authority_expert: 1
  - authority_expert -> deductive_modus_ponens: 1
  - deductive_disjunctive -> abductive_elimination: 2
  - deductive_hypothetical_syllogism -> deductive_modus_ponens: 4
  - deductive_modus_ponens -> deductive_hypothetical_syllogism: 1
  - deductive_modus_ponens -> deductive_modus_ponens: 25
  - deductive_modus_ponens -> deductive_modus_tollens: 1
  - deductive_modus_ponens -> inductive_enumeration: 2
  - deductive_modus_tollens -> deductive_modus_tollens: 2
  - inductive_analogy -> abductive_best_explanation: 1
  - inductive_analogy -> deductive_modus_ponens: 3
  - inductive_analogy -> inductive_analogy: 9
  - inductive_causal -> abductive_best_explanation: 1
  - inductive_causal -> deductive_modus_ponens: 1
  - inductive_enumeration -> inductive_analogy: 1
  - inductive_enumeration -> inductive_enumeration: 1
  - inductive_generalization -> abductive_best_explanation: 11
  - inductive_generalization -> authority_consensus: 3
  - inductive_generalization -> authority_expert: 1
  - inductive_generalization -> deductive_modus_ponens: 16
  - inductive_generalization -> deductive_modus_tollens: 1
  - inductive_generalization -> inductive_analogy: 9
  - inductive_generalization -> inductive_causal: 1
  - inductive_generalization -> inductive_enumeration: 3
  - inductive_generalization -> inductive_generalization: 2
- self-naming (claim or chain contains the declared type): 15 of 135; agreement without them: 47/120 = 39.2% [Wilson 30.9%, 48.1%]

### pass: without_both

- Status of this pass: derived (combines pre-registered exclusions; not itself pre-registered)
- Status of the Wilson intervals below: descriptive (not pre-registered)
- Status of the declared -> blind table below: descriptive (not pre-registered)

- overall: 52/134 = 38.8% [Wilson 31.0%, 47.3%]
- per stratum:
  - derivation:abductive_best_explanation: 11/29 = 37.9% [Wilson 22.7%, 56.0%]
  - derivation:abductive_elimination: 1/2 (counts only: fewer than 10)
  - derivation:authority_expert: 1/2 (counts only: fewer than 10)
  - derivation:deductive_disjunctive: 0/2 (counts only: fewer than 10)
  - derivation:deductive_hypothetical_syllogism: 0/4 (counts only: fewer than 10)
  - derivation:deductive_modus_ponens: 25/29 = 86.2% [Wilson 69.4%, 94.5%]
  - derivation:deductive_modus_tollens: 2/2 (counts only: fewer than 10)
  - derivation:inductive_analogy: 9/13 = 69.2% [Wilson 42.4%, 87.3%]
  - derivation:inductive_causal: 0/2 (counts only: fewer than 10)
  - derivation:inductive_enumeration: 1/2 (counts only: fewer than 10)
  - derivation:inductive_generalization: 2/47 = 4.3% [Wilson 1.2%, 14.2%]
  - derivation:inductive_statistical: 0/0 (counts only: fewer than 10)
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: 6/34 = 17.6% [Wilson 8.3%, 33.5%]; less certain (hours_before > 24): 0
  - claude-opus-4-7: 11/42 = 26.2% [Wilson 15.3%, 41.1%]; less certain (hours_before > 24): 5
  - claude-opus-4-8: 15/29 = 51.7% [Wilson 34.4%, 68.6%]; less certain (hours_before > 24): 0
  - claude-opus-5: 20/29 = 69.0% [Wilson 50.8%, 82.7%]; less certain (hours_before > 24): 0
- declared -> blind:
  - abductive_best_explanation -> abductive_best_explanation: 11
  - abductive_best_explanation -> abductive_elimination: 6
  - abductive_best_explanation -> deductive_modus_ponens: 8
  - abductive_best_explanation -> deductive_modus_tollens: 3
  - abductive_best_explanation -> inductive_analogy: 1
  - abductive_elimination -> abductive_elimination: 1
  - abductive_elimination -> deductive_modus_ponens: 1
  - authority_expert -> authority_expert: 1
  - authority_expert -> deductive_modus_ponens: 1
  - deductive_disjunctive -> abductive_elimination: 2
  - deductive_hypothetical_syllogism -> deductive_modus_ponens: 4
  - deductive_modus_ponens -> deductive_hypothetical_syllogism: 1
  - deductive_modus_ponens -> deductive_modus_ponens: 25
  - deductive_modus_ponens -> deductive_modus_tollens: 1
  - deductive_modus_ponens -> inductive_enumeration: 2
  - deductive_modus_tollens -> deductive_modus_tollens: 2
  - inductive_analogy -> abductive_best_explanation: 1
  - inductive_analogy -> deductive_modus_ponens: 3
  - inductive_analogy -> inductive_analogy: 9
  - inductive_causal -> abductive_best_explanation: 1
  - inductive_causal -> deductive_modus_ponens: 1
  - inductive_enumeration -> inductive_analogy: 1
  - inductive_enumeration -> inductive_enumeration: 1
  - inductive_generalization -> abductive_best_explanation: 11
  - inductive_generalization -> authority_consensus: 3
  - inductive_generalization -> authority_expert: 1
  - inductive_generalization -> deductive_modus_ponens: 16
  - inductive_generalization -> deductive_modus_tollens: 1
  - inductive_generalization -> inductive_analogy: 9
  - inductive_generalization -> inductive_causal: 1
  - inductive_generalization -> inductive_enumeration: 3
  - inductive_generalization -> inductive_generalization: 2
- self-naming (claim or chain contains the declared type): 15 of 134; agreement without them: 47/119 = 39.5% [Wilson 31.2%, 48.5%]

## Author agrees / disagrees, per reader

### mira, pass: all

- all checks: author agrees 193, author disagrees 122, author cannot-judge 1, reverse (author loose, reader tight) 41; reader-loose total 316
- type: author agrees 43, author disagrees 16, author cannot-judge 0, reverse (author loose, reader tight) 28; reader-loose total 59
- placement: author agrees 14, author disagrees 37, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 51
- chain-overreach: author agrees 60, author disagrees 60, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 120
- support-overreach: author agrees 52, author disagrees 3, author cannot-judge 1, reverse (author loose, reader tight) 0; reader-loose total 56
- quote_type: author agrees 19, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 6; reader-loose total 19
- source_class: author agrees 5, author disagrees 6, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 11
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 52, author disagrees 23, author cannot-judge 0, reverse (author loose, reader tight) 11; reader-loose total 75
  - claude-opus-4-7: author agrees 80, author disagrees 32, author cannot-judge 0, reverse (author loose, reader tight) 18; reader-loose total 112
  - claude-opus-4-8: author agrees 28, author disagrees 28, author cannot-judge 0, reverse (author loose, reader tight) 6; reader-loose total 56
  - claude-opus-5: author agrees 33, author disagrees 39, author cannot-judge 1, reverse (author loose, reader tight) 6; reader-loose total 73

### mira, pass: without_prior

- all checks: author agrees 192, author disagrees 122, author cannot-judge 1, reverse (author loose, reader tight) 40; reader-loose total 315
- type: author agrees 43, author disagrees 16, author cannot-judge 0, reverse (author loose, reader tight) 27; reader-loose total 59
- placement: author agrees 14, author disagrees 37, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 51
- chain-overreach: author agrees 59, author disagrees 60, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 119
- support-overreach: author agrees 52, author disagrees 3, author cannot-judge 1, reverse (author loose, reader tight) 0; reader-loose total 56
- quote_type: author agrees 19, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 6; reader-loose total 19
- source_class: author agrees 5, author disagrees 6, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 11
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 51, author disagrees 23, author cannot-judge 0, reverse (author loose, reader tight) 10; reader-loose total 74
  - claude-opus-4-7: author agrees 80, author disagrees 32, author cannot-judge 0, reverse (author loose, reader tight) 18; reader-loose total 112
  - claude-opus-4-8: author agrees 28, author disagrees 28, author cannot-judge 0, reverse (author loose, reader tight) 6; reader-loose total 56
  - claude-opus-5: author agrees 33, author disagrees 39, author cannot-judge 1, reverse (author loose, reader tight) 6; reader-loose total 73

### mira, pass: without_manifest

- all checks: author agrees 181, author disagrees 119, author cannot-judge 1, reverse (author loose, reader tight) 41; reader-loose total 301
- type: author agrees 38, author disagrees 16, author cannot-judge 0, reverse (author loose, reader tight) 28; reader-loose total 54
- placement: author agrees 11, author disagrees 35, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 46
- chain-overreach: author agrees 56, author disagrees 59, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 115
- support-overreach: author agrees 52, author disagrees 3, author cannot-judge 1, reverse (author loose, reader tight) 0; reader-loose total 56
- quote_type: author agrees 19, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 6; reader-loose total 19
- source_class: author agrees 5, author disagrees 6, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 11
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 52, author disagrees 23, author cannot-judge 0, reverse (author loose, reader tight) 11; reader-loose total 75
  - claude-opus-4-7: author agrees 68, author disagrees 29, author cannot-judge 0, reverse (author loose, reader tight) 18; reader-loose total 97
  - claude-opus-4-8: author agrees 28, author disagrees 28, author cannot-judge 0, reverse (author loose, reader tight) 6; reader-loose total 56
  - claude-opus-5: author agrees 33, author disagrees 39, author cannot-judge 1, reverse (author loose, reader tight) 6; reader-loose total 73

### mira, pass: without_both

- Status of this pass: derived (combines pre-registered exclusions; not itself pre-registered)

- all checks: author agrees 180, author disagrees 119, author cannot-judge 1, reverse (author loose, reader tight) 40; reader-loose total 300
- type: author agrees 38, author disagrees 16, author cannot-judge 0, reverse (author loose, reader tight) 27; reader-loose total 54
- placement: author agrees 11, author disagrees 35, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 46
- chain-overreach: author agrees 55, author disagrees 59, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 114
- support-overreach: author agrees 52, author disagrees 3, author cannot-judge 1, reverse (author loose, reader tight) 0; reader-loose total 56
- quote_type: author agrees 19, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 6; reader-loose total 19
- source_class: author agrees 5, author disagrees 6, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 11
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 51, author disagrees 23, author cannot-judge 0, reverse (author loose, reader tight) 10; reader-loose total 74
  - claude-opus-4-7: author agrees 68, author disagrees 29, author cannot-judge 0, reverse (author loose, reader tight) 18; reader-loose total 97
  - claude-opus-4-8: author agrees 28, author disagrees 28, author cannot-judge 0, reverse (author loose, reader tight) 6; reader-loose total 56
  - claude-opus-5: author agrees 33, author disagrees 39, author cannot-judge 1, reverse (author loose, reader tight) 6; reader-loose total 73

### ariadne, pass: all

- all checks: author agrees 204, author disagrees 85, author cannot-judge 2, reverse (author loose, reader tight) 34; reader-loose total 291
- type: author agrees 49, author disagrees 16, author cannot-judge 0, reverse (author loose, reader tight) 22; reader-loose total 65
- placement: author agrees 14, author disagrees 36, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 50
- chain-overreach: author agrees 60, author disagrees 25, author cannot-judge 0, reverse (author loose, reader tight) 7; reader-loose total 85
- support-overreach: author agrees 52, author disagrees 3, author cannot-judge 1, reverse (author loose, reader tight) 0; reader-loose total 56
- quote_type: author agrees 24, author disagrees 2, author cannot-judge 1, reverse (author loose, reader tight) 1; reader-loose total 27
- source_class: author agrees 5, author disagrees 3, author cannot-judge 0, reverse (author loose, reader tight) 1; reader-loose total 8
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 55, author disagrees 14, author cannot-judge 0, reverse (author loose, reader tight) 10; reader-loose total 69
  - claude-opus-4-7: author agrees 85, author disagrees 20, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 105
  - claude-opus-4-8: author agrees 28, author disagrees 21, author cannot-judge 1, reverse (author loose, reader tight) 7; reader-loose total 50
  - claude-opus-5: author agrees 36, author disagrees 30, author cannot-judge 1, reverse (author loose, reader tight) 3; reader-loose total 67

### ariadne, pass: without_prior

- all checks: author agrees 203, author disagrees 84, author cannot-judge 2, reverse (author loose, reader tight) 33; reader-loose total 289
- type: author agrees 49, author disagrees 16, author cannot-judge 0, reverse (author loose, reader tight) 21; reader-loose total 65
- placement: author agrees 14, author disagrees 35, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 49
- chain-overreach: author agrees 59, author disagrees 25, author cannot-judge 0, reverse (author loose, reader tight) 7; reader-loose total 84
- support-overreach: author agrees 52, author disagrees 3, author cannot-judge 1, reverse (author loose, reader tight) 0; reader-loose total 56
- quote_type: author agrees 24, author disagrees 2, author cannot-judge 1, reverse (author loose, reader tight) 1; reader-loose total 27
- source_class: author agrees 5, author disagrees 3, author cannot-judge 0, reverse (author loose, reader tight) 1; reader-loose total 8
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 54, author disagrees 13, author cannot-judge 0, reverse (author loose, reader tight) 9; reader-loose total 67
  - claude-opus-4-7: author agrees 85, author disagrees 20, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 105
  - claude-opus-4-8: author agrees 28, author disagrees 21, author cannot-judge 1, reverse (author loose, reader tight) 7; reader-loose total 50
  - claude-opus-5: author agrees 36, author disagrees 30, author cannot-judge 1, reverse (author loose, reader tight) 3; reader-loose total 67

### ariadne, pass: without_manifest

- all checks: author agrees 192, author disagrees 82, author cannot-judge 2, reverse (author loose, reader tight) 34; reader-loose total 276
- type: author agrees 44, author disagrees 16, author cannot-judge 0, reverse (author loose, reader tight) 22; reader-loose total 60
- placement: author agrees 11, author disagrees 34, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 45
- chain-overreach: author agrees 56, author disagrees 24, author cannot-judge 0, reverse (author loose, reader tight) 7; reader-loose total 80
- support-overreach: author agrees 52, author disagrees 3, author cannot-judge 1, reverse (author loose, reader tight) 0; reader-loose total 56
- quote_type: author agrees 24, author disagrees 2, author cannot-judge 1, reverse (author loose, reader tight) 1; reader-loose total 27
- source_class: author agrees 5, author disagrees 3, author cannot-judge 0, reverse (author loose, reader tight) 1; reader-loose total 8
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 55, author disagrees 14, author cannot-judge 0, reverse (author loose, reader tight) 10; reader-loose total 69
  - claude-opus-4-7: author agrees 73, author disagrees 17, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 90
  - claude-opus-4-8: author agrees 28, author disagrees 21, author cannot-judge 1, reverse (author loose, reader tight) 7; reader-loose total 50
  - claude-opus-5: author agrees 36, author disagrees 30, author cannot-judge 1, reverse (author loose, reader tight) 3; reader-loose total 67

### ariadne, pass: without_both

- Status of this pass: derived (combines pre-registered exclusions; not itself pre-registered)

- all checks: author agrees 191, author disagrees 81, author cannot-judge 2, reverse (author loose, reader tight) 33; reader-loose total 274
- type: author agrees 44, author disagrees 16, author cannot-judge 0, reverse (author loose, reader tight) 21; reader-loose total 60
- placement: author agrees 11, author disagrees 33, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 44
- chain-overreach: author agrees 55, author disagrees 24, author cannot-judge 0, reverse (author loose, reader tight) 7; reader-loose total 79
- support-overreach: author agrees 52, author disagrees 3, author cannot-judge 1, reverse (author loose, reader tight) 0; reader-loose total 56
- quote_type: author agrees 24, author disagrees 2, author cannot-judge 1, reverse (author loose, reader tight) 1; reader-loose total 27
- source_class: author agrees 5, author disagrees 3, author cannot-judge 0, reverse (author loose, reader tight) 1; reader-loose total 8
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 54, author disagrees 13, author cannot-judge 0, reverse (author loose, reader tight) 9; reader-loose total 67
  - claude-opus-4-7: author agrees 73, author disagrees 17, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 90
  - claude-opus-4-8: author agrees 28, author disagrees 21, author cannot-judge 1, reverse (author loose, reader tight) 7; reader-loose total 50
  - claude-opus-5: author agrees 36, author disagrees 30, author cannot-judge 1, reverse (author loose, reader tight) 3; reader-loose total 67

### zephyr, pass: all

- all checks: author agrees 19, author disagrees 13, author cannot-judge 0, reverse (author loose, reader tight) 43; reader-loose total 32
- type: author agrees 7, author disagrees 2, author cannot-judge 0, reverse (author loose, reader tight) 19; reader-loose total 9
- placement: author agrees 2, author disagrees 9, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 11
- chain-overreach: author agrees 10, author disagrees 2, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 12
- support-overreach: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 5; reader-loose total 0
- quote_type: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 0
- source_class: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 0; reader-loose total 0
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 5, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 5
  - claude-opus-4-7: author agrees 10, author disagrees 7, author cannot-judge 0, reverse (author loose, reader tight) 16; reader-loose total 17
  - claude-opus-4-8: author agrees 3, author disagrees 5, author cannot-judge 0, reverse (author loose, reader tight) 8; reader-loose total 8
  - claude-opus-5: author agrees 1, author disagrees 1, author cannot-judge 0, reverse (author loose, reader tight) 5; reader-loose total 2

### zephyr, pass: without_prior

- all checks: author agrees 19, author disagrees 13, author cannot-judge 0, reverse (author loose, reader tight) 43; reader-loose total 32
- type: author agrees 7, author disagrees 2, author cannot-judge 0, reverse (author loose, reader tight) 19; reader-loose total 9
- placement: author agrees 2, author disagrees 9, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 11
- chain-overreach: author agrees 10, author disagrees 2, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 12
- support-overreach: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 5; reader-loose total 0
- quote_type: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 0
- source_class: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 0; reader-loose total 0
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 5, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 5
  - claude-opus-4-7: author agrees 10, author disagrees 7, author cannot-judge 0, reverse (author loose, reader tight) 16; reader-loose total 17
  - claude-opus-4-8: author agrees 3, author disagrees 5, author cannot-judge 0, reverse (author loose, reader tight) 8; reader-loose total 8
  - claude-opus-5: author agrees 1, author disagrees 1, author cannot-judge 0, reverse (author loose, reader tight) 5; reader-loose total 2

### zephyr, pass: without_manifest

- all checks: author agrees 19, author disagrees 13, author cannot-judge 0, reverse (author loose, reader tight) 43; reader-loose total 32
- type: author agrees 7, author disagrees 2, author cannot-judge 0, reverse (author loose, reader tight) 19; reader-loose total 9
- placement: author agrees 2, author disagrees 9, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 11
- chain-overreach: author agrees 10, author disagrees 2, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 12
- support-overreach: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 5; reader-loose total 0
- quote_type: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 0
- source_class: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 0; reader-loose total 0
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 5, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 5
  - claude-opus-4-7: author agrees 10, author disagrees 7, author cannot-judge 0, reverse (author loose, reader tight) 16; reader-loose total 17
  - claude-opus-4-8: author agrees 3, author disagrees 5, author cannot-judge 0, reverse (author loose, reader tight) 8; reader-loose total 8
  - claude-opus-5: author agrees 1, author disagrees 1, author cannot-judge 0, reverse (author loose, reader tight) 5; reader-loose total 2

### zephyr, pass: without_both

- Status of this pass: derived (combines pre-registered exclusions; not itself pre-registered)

- all checks: author agrees 19, author disagrees 13, author cannot-judge 0, reverse (author loose, reader tight) 43; reader-loose total 32
- type: author agrees 7, author disagrees 2, author cannot-judge 0, reverse (author loose, reader tight) 19; reader-loose total 9
- placement: author agrees 2, author disagrees 9, author cannot-judge 0, reverse (author loose, reader tight) 3; reader-loose total 11
- chain-overreach: author agrees 10, author disagrees 2, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 12
- support-overreach: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 5; reader-loose total 0
- quote_type: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 2; reader-loose total 0
- source_class: author agrees 0, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 0; reader-loose total 0
- per filing model (exploratory, not attribution):
  - claude-opus-4-6: author agrees 5, author disagrees 0, author cannot-judge 0, reverse (author loose, reader tight) 14; reader-loose total 5
  - claude-opus-4-7: author agrees 10, author disagrees 7, author cannot-judge 0, reverse (author loose, reader tight) 16; reader-loose total 17
  - claude-opus-4-8: author agrees 3, author disagrees 5, author cannot-judge 0, reverse (author loose, reader tight) 8; reader-loose total 8
  - claude-opus-5: author agrees 1, author disagrees 1, author cannot-judge 0, reverse (author loose, reader tight) 5; reader-loose total 2

## Pairwise agreement (shared sampled nodes)

### author_mira (n=200)

- node class (partial its own category): 152/200 = 76.0%; kappa 0.1852
- tight vs loose (n=195): kappa 0.1759
- per check:
  - type: 95/140 = 67.9%; kappa 0.3631
  - placement: 100/140 = 71.4%; kappa 0.2808
  - chain-overreach: 69/140 = 49.3%; kappa 0.0760
  - support-overreach: 56/60 = 93.3%; kappa 0.6364
  - quote_type: 52/60 = 86.7%; kappa 0.7279
  - source_class: 42/60 = 70.0%; kappa 0.3090
- disagreements (id: author / mira):
  - dv_0005: loose / tight
  - dv_0068: tight / loose
  - dv_0227: tight / partial
  - dv_0234: tight / loose
  - dv_0412: loose / tight
  - dv_0440: tight / loose
  - dv_0450: tight / loose
  - dv_0521: tight / loose
  - dv_0584: tight / loose
  - dv_0604: loose / partial
  - dv_0646: tight / loose
  - dv_0694: tight / loose
  - dv_0715: tight / loose
  - dv_0719: tight / loose
  - dv_0756: tight / loose
  - dv_0816: tight / loose
  - dv_0822: tight / loose
  - dv_0840: tight / loose
  - dv_0850: tight / loose
  - dv_0855: tight / loose
  - dv_0918: tight / loose
  - dv_0948: tight / loose
  - dv_0960: tight / loose
  - dv_0996: tight / partial
  - dv_1030: tight / loose
  - dv_1096: tight / loose
  - dv_1180: tight / loose
  - dv_1199: tight / loose
  - dv_1240: tight / loose
  - dv_1318: tight / loose
  - dv_1328: tight / loose
  - dv_1394: tight / loose
  - dv_1410: tight / loose
  - dv_1477: tight / loose
  - dv_1480: tight / loose
  - dv_1483: tight / loose
  - dv_1494: tight / loose
  - dv_1548: tight / loose
  - dv_1555: tight / loose
  - dv_1583: tight / loose
  - dv_1597: tight / loose
  - dv_1619: tight / loose
  - dv_1622: tight / loose
  - ob_0817: tight / partial
  - ob_0987: loose / tight
  - ob_3169: tight / loose
  - ob_3989: partial / loose
  - ob_5228: tight / loose

### author_ariadne (n=200)

- node class (partial its own category): 158/200 = 79.0%; kappa 0.3549
- tight vs loose (n=198): kappa 0.3614
- per check:
  - type: 101/140 = 72.1%; kappa 0.4473
  - placement: 101/140 = 72.1%; kappa 0.2891
  - chain-overreach: 108/140 = 77.1%; kappa 0.5470
  - support-overreach: 56/60 = 93.3%; kappa 0.6364
  - quote_type: 56/60 = 93.3%; kappa 0.8669
  - source_class: 53/60 = 88.3%; kappa 0.6125
- disagreements (id: author / ariadne):
  - dv_0005: loose / tight
  - dv_0112: loose / tight
  - dv_0227: tight / loose
  - dv_0234: tight / loose
  - dv_0339: loose / tight
  - dv_0356: loose / tight
  - dv_0412: loose / tight
  - dv_0416: loose / tight
  - dv_0440: tight / loose
  - dv_0513: tight / loose
  - dv_0584: tight / loose
  - dv_0628: loose / tight
  - dv_0694: tight / loose
  - dv_0715: tight / loose
  - dv_0756: tight / loose
  - dv_0816: tight / loose
  - dv_0846: loose / tight
  - dv_0855: tight / loose
  - dv_0918: tight / loose
  - dv_0948: tight / loose
  - dv_0996: tight / loose
  - dv_1030: tight / loose
  - dv_1096: tight / loose
  - dv_1180: tight / loose
  - dv_1199: tight / loose
  - dv_1240: tight / loose
  - dv_1328: tight / loose
  - dv_1394: tight / loose
  - dv_1477: tight / loose
  - dv_1480: tight / loose
  - dv_1483: tight / loose
  - dv_1494: tight / loose
  - dv_1555: tight / loose
  - dv_1565: loose / tight
  - dv_1583: tight / loose
  - dv_1619: tight / loose
  - dv_1622: tight / loose
  - ob_0817: tight / partial
  - ob_2244: tight / loose
  - ob_3169: tight / loose
  - ob_3989: partial / loose
  - ob_5228: tight / loose

### author_zephyr (n=50)

- node class (partial its own category): 28/50 = 56.0%; kappa 0.1379
- tight vs loose (n=50): kappa 0.1379
- per check:
  - type: 24/45 = 53.3%; kappa 0.1463
  - placement: 33/45 = 73.3%; kappa 0.1148
  - chain-overreach: 29/45 = 64.4%; kappa 0.3103
  - support-overreach: 0/5 = 0.0%; kappa 0.0000
  - quote_type: 3/5 = 60.0%; kappa 0.0000
  - source_class: 5/5 = 100.0%; kappa n/a
- disagreements (id: author / zephyr):
  - dv_0112: loose / tight
  - dv_0174: loose / tight
  - dv_0217: loose / tight
  - dv_0224: loose / tight
  - dv_0259: loose / tight
  - dv_0604: loose / tight
  - dv_0629: loose / tight
  - dv_0719: tight / loose
  - dv_0759: loose / tight
  - dv_0795: loose / tight
  - dv_0802: loose / tight
  - dv_0805: loose / tight
  - dv_0816: tight / loose
  - dv_1096: tight / loose
  - dv_1328: tight / loose
  - dv_1513: loose / tight
  - dv_1565: loose / tight
  - ob_0024: loose / tight
  - ob_0759: loose / tight
  - ob_1550: loose / tight
  - ob_3773: loose / tight
  - ob_3941: loose / tight

### ariadne_mira (n=200)

- node class (partial its own category): 174/200 = 87.0%; kappa 0.3276
- tight vs loose (n=196): kappa 0.3284
- per check:
  - type: 106/140 = 75.7%; kappa 0.5165
  - placement: 109/140 = 77.9%; kappa 0.5199
  - chain-overreach: 91/140 = 65.0%; kappa 0.2200
  - support-overreach: 58/60 = 96.7%; kappa 0.7321
  - quote_type: 49/60 = 81.7%; kappa 0.6265
  - source_class: 43/60 = 71.7%; kappa 0.3796
- disagreements (id: ariadne / mira):
  - dv_0068: tight / loose
  - dv_0112: tight / loose
  - dv_0227: loose / partial
  - dv_0339: tight / loose
  - dv_0356: tight / loose
  - dv_0416: tight / loose
  - dv_0450: tight / loose
  - dv_0513: loose / tight
  - dv_0521: tight / loose
  - dv_0604: loose / partial
  - dv_0628: tight / loose
  - dv_0646: tight / loose
  - dv_0719: tight / loose
  - dv_0822: tight / loose
  - dv_0840: tight / loose
  - dv_0846: tight / loose
  - dv_0850: tight / loose
  - dv_0960: tight / loose
  - dv_0996: loose / partial
  - dv_1318: tight / loose
  - dv_1410: tight / loose
  - dv_1548: tight / loose
  - dv_1565: tight / loose
  - dv_1597: tight / loose
  - ob_0987: loose / tight
  - ob_2244: loose / tight

### ariadne_zephyr (n=50)

- node class (partial its own category): 25/50 = 50.0%; kappa 0.0250
- tight vs loose (n=50): kappa 0.0250
- per check:
  - type: 29/45 = 64.4%; kappa 0.2157
  - placement: 28/45 = 62.2%; kappa 0.0078
  - chain-overreach: 23/45 = 51.1%; kappa 0.1538
  - support-overreach: 0/5 = 0.0%; kappa 0.0000
  - quote_type: 3/5 = 60.0%; kappa 0.0000
  - source_class: 5/5 = 100.0%; kappa n/a
- disagreements (id: ariadne / zephyr):
  - dv_0174: loose / tight
  - dv_0217: loose / tight
  - dv_0224: loose / tight
  - dv_0259: loose / tight
  - dv_0339: tight / loose
  - dv_0356: tight / loose
  - dv_0513: loose / tight
  - dv_0604: loose / tight
  - dv_0628: tight / loose
  - dv_0629: loose / tight
  - dv_0715: loose / tight
  - dv_0719: tight / loose
  - dv_0759: loose / tight
  - dv_0795: loose / tight
  - dv_0802: loose / tight
  - dv_0805: loose / tight
  - dv_1180: loose / tight
  - dv_1199: loose / tight
  - dv_1513: loose / tight
  - dv_1622: loose / tight
  - ob_0024: loose / tight
  - ob_0759: loose / tight
  - ob_1550: loose / tight
  - ob_3773: loose / tight
  - ob_3941: loose / tight

## Ariadne's rates

### pass: all

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=30 (judgeable 30; cannot-judge 0 left out of the denominator): low 80.0% [Wilson 62.7%, 90.5%]; high 80.0% [Wilson 62.7%, 90.5%]; loose 24, partial 0, cannot-judge 0, tight 6
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 3, partial 0, cannot-judge 0, tight 1
- derivation:deductive_modus_ponens: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 79.3% [Wilson 61.6%, 90.2%]; high 79.3% [Wilson 61.6%, 90.2%]; loose 23, partial 0, cannot-judge 0, tight 6
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_analogy: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 100.0% [Wilson 77.2%, 100.0%]; high 100.0% [Wilson 77.2%, 100.0%]; loose 13, partial 0, cannot-judge 0, tight 0
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_enumeration: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 88.0% [Wilson 76.2%, 94.4%]; high 88.0% [Wilson 76.2%, 94.4%]; loose 44, partial 0, cannot-judge 0, tight 6
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 81.4%, high 81.4% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 84.2%, high 84.2%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 88.0% [Wilson 76.2%, 94.4%]; high 88.0% [Wilson 76.2%, 94.4%]; loose 44, partial 0, cannot-judge 0, tight 6

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 1
- abductive_best_explanation -> deductive_modus_ponens: 1
- abductive_best_explanation -> inductive_enumeration: 1
- deductive_hypothetical_syllogism -> authority_expert: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 2
- deductive_modus_ponens -> abductive_best_explanation: 3
- deductive_modus_ponens -> authority_expert: 1
- deductive_modus_ponens -> inductive_causal: 1
- deductive_modus_ponens -> inductive_enumeration: 1
- inductive_analogy -> abductive_best_explanation: 4
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_analogy -> inductive_enumeration: 1
- inductive_analogy -> inductive_generalization: 4
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_generalization: 1
- inductive_generalization -> abductive_best_explanation: 15
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_expert: 4
- inductive_generalization -> deductive_modus_ponens: 5
- inductive_generalization -> inductive_analogy: 4
- inductive_generalization -> inductive_enumeration: 10
- inductive_statistical -> abductive_best_explanation: 1
- inductive_statistical -> authority_expert: 1

- derivations confidence: tight n=26 mean 0.7615; loose n=114 mean 0.7070; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.5267, bootstrap 95% interval [0.4195, 0.6334]
- Reading: no evidence either way at this n

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=9 (judgeable 9; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 9, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=28 (judgeable 28; cannot-judge 0 left out of the denominator): low 92.9% [Wilson 77.4%, 98.0%]; high 96.4% [Wilson 82.3%, 99.4%]; loose 26, partial 1, cannot-judge 0, tight 1
- observation:official_statement: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 100.0% [Wilson 77.2%, 100.0%]; high 100.0% [Wilson 77.2%, 100.0%]; loose 13, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (observations): low 96.4%, high 98.2% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 95.0%, high 97.5%.

- observations confidence: tight n=1 mean 0.9020; loose n=58 mean 0.8123; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.7241, bootstrap 95% interval [0.6379, 0.8103]
- Reading: confidence tracks correctness in this sample

### pass: without_prior

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 79.3% [Wilson 61.6%, 90.2%]; high 79.3% [Wilson 61.6%, 90.2%]; loose 23, partial 0, cannot-judge 0, tight 6
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 3, partial 0, cannot-judge 0, tight 1
- derivation:deductive_modus_ponens: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 79.3% [Wilson 61.6%, 90.2%]; high 79.3% [Wilson 61.6%, 90.2%]; loose 23, partial 0, cannot-judge 0, tight 6
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_analogy: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 100.0% [Wilson 77.2%, 100.0%]; high 100.0% [Wilson 77.2%, 100.0%]; loose 13, partial 0, cannot-judge 0, tight 0
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_enumeration: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 88.0% [Wilson 76.2%, 94.4%]; high 88.0% [Wilson 76.2%, 94.4%]; loose 44, partial 0, cannot-judge 0, tight 6
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 81.2%, high 81.2% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 84.0%, high 84.0%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 88.0% [Wilson 76.2%, 94.4%]; high 88.0% [Wilson 76.2%, 94.4%]; loose 44, partial 0, cannot-judge 0, tight 6

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 1
- abductive_best_explanation -> deductive_modus_ponens: 1
- abductive_best_explanation -> inductive_enumeration: 1
- deductive_hypothetical_syllogism -> authority_expert: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 2
- deductive_modus_ponens -> abductive_best_explanation: 3
- deductive_modus_ponens -> authority_expert: 1
- deductive_modus_ponens -> inductive_causal: 1
- deductive_modus_ponens -> inductive_enumeration: 1
- inductive_analogy -> abductive_best_explanation: 4
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_analogy -> inductive_enumeration: 1
- inductive_analogy -> inductive_generalization: 4
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_generalization: 1
- inductive_generalization -> abductive_best_explanation: 15
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_expert: 4
- inductive_generalization -> deductive_modus_ponens: 5
- inductive_generalization -> inductive_analogy: 4
- inductive_generalization -> inductive_enumeration: 10
- inductive_statistical -> abductive_best_explanation: 1
- inductive_statistical -> authority_expert: 1

- derivations confidence: tight n=26 mean 0.7615; loose n=113 mean 0.7108; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.5225, bootstrap 95% interval [0.4141, 0.6299]
- Reading: no evidence either way at this n

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=9 (judgeable 9; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 9, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=28 (judgeable 28; cannot-judge 0 left out of the denominator): low 92.9% [Wilson 77.4%, 98.0%]; high 96.4% [Wilson 82.3%, 99.4%]; loose 26, partial 1, cannot-judge 0, tight 1
- observation:official_statement: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 100.0% [Wilson 77.2%, 100.0%]; high 100.0% [Wilson 77.2%, 100.0%]; loose 13, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (observations): low 96.4%, high 98.2% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 95.0%, high 97.5%.

- observations confidence: tight n=1 mean 0.9020; loose n=58 mean 0.8123; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.7241, bootstrap 95% interval [0.6379, 0.8103]
- Reading: confidence tracks correctness in this sample

### pass: without_recognized

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=20 (judgeable 20; cannot-judge 0 left out of the denominator): low 85.0% [Wilson 64.0%, 94.8%]; high 85.0% [Wilson 64.0%, 94.8%]; loose 17, partial 0, cannot-judge 0, tight 3
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 3, partial 0, cannot-judge 0, tight 1
- derivation:deductive_modus_ponens: n=23 (judgeable 23; cannot-judge 0 left out of the denominator): low 82.6% [Wilson 62.9%, 93.0%]; high 82.6% [Wilson 62.9%, 93.0%]; loose 19, partial 0, cannot-judge 0, tight 4
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_analogy: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_enumeration: n=1 (judgeable 1; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 0
- derivation:inductive_generalization: n=44 (judgeable 44; cannot-judge 0 left out of the denominator): low 86.4% [Wilson 73.3%, 93.6%]; high 86.4% [Wilson 73.3%, 93.6%]; loose 38, partial 0, cannot-judge 0, tight 6
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 84.4%, high 84.4% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 84.4%, high 84.4%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=44 (judgeable 44; cannot-judge 0 left out of the denominator): low 86.4% [Wilson 73.3%, 93.6%]; high 86.4% [Wilson 73.3%, 93.6%]; loose 38, partial 0, cannot-judge 0, tight 6

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 1
- abductive_best_explanation -> deductive_modus_ponens: 1
- abductive_best_explanation -> inductive_enumeration: 1
- deductive_hypothetical_syllogism -> authority_expert: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 2
- deductive_modus_ponens -> abductive_best_explanation: 3
- deductive_modus_ponens -> inductive_causal: 1
- deductive_modus_ponens -> inductive_enumeration: 1
- inductive_analogy -> abductive_best_explanation: 2
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_analogy -> inductive_generalization: 1
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_generalization: 1
- inductive_generalization -> abductive_best_explanation: 14
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_expert: 3
- inductive_generalization -> deductive_modus_ponens: 5
- inductive_generalization -> inductive_analogy: 4
- inductive_generalization -> inductive_enumeration: 9
- inductive_statistical -> abductive_best_explanation: 1
- inductive_statistical -> authority_expert: 1

- derivations confidence: tight n=20 mean 0.7480; loose n=91 mean 0.7404; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.4810, bootstrap 95% interval [0.3547, 0.6099]
- Reading: no evidence either way at this n

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=25 (judgeable 25; cannot-judge 0 left out of the denominator): low 92.0% [Wilson 75.0%, 97.8%]; high 96.0% [Wilson 80.5%, 99.3%]; loose 23, partial 1, cannot-judge 0, tight 1
- observation:official_statement: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (observations): low 96.0%, high 98.0% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 92.0%, high 96.0%.

- observations confidence: tight n=1 mean 0.9020; loose n=47 mean 0.8271; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.6915, bootstrap 95% interval [0.5851, 0.7872]
- Reading: confidence tracks correctness in this sample

### pass: without_mention

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=20 (judgeable 20; cannot-judge 0 left out of the denominator): low 85.0% [Wilson 64.0%, 94.8%]; high 85.0% [Wilson 64.0%, 94.8%]; loose 17, partial 0, cannot-judge 0, tight 3
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 3, partial 0, cannot-judge 0, tight 1
- derivation:deductive_modus_ponens: n=24 (judgeable 24; cannot-judge 0 left out of the denominator): low 83.3% [Wilson 64.1%, 93.3%]; high 83.3% [Wilson 64.1%, 93.3%]; loose 20, partial 0, cannot-judge 0, tight 4
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_analogy: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_enumeration: n=1 (judgeable 1; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 0
- derivation:inductive_generalization: n=45 (judgeable 45; cannot-judge 0 left out of the denominator): low 86.7% [Wilson 73.8%, 93.7%]; high 86.7% [Wilson 73.8%, 93.7%]; loose 39, partial 0, cannot-judge 0, tight 6
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 84.7%, high 84.7% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 84.7%, high 84.7%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=45 (judgeable 45; cannot-judge 0 left out of the denominator): low 86.7% [Wilson 73.8%, 93.7%]; high 86.7% [Wilson 73.8%, 93.7%]; loose 39, partial 0, cannot-judge 0, tight 6

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 1
- abductive_best_explanation -> deductive_modus_ponens: 1
- abductive_best_explanation -> inductive_enumeration: 1
- deductive_hypothetical_syllogism -> authority_expert: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 2
- deductive_modus_ponens -> abductive_best_explanation: 3
- deductive_modus_ponens -> inductive_causal: 1
- deductive_modus_ponens -> inductive_enumeration: 1
- inductive_analogy -> abductive_best_explanation: 2
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_analogy -> inductive_generalization: 1
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_generalization: 1
- inductive_generalization -> abductive_best_explanation: 15
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_expert: 3
- inductive_generalization -> deductive_modus_ponens: 5
- inductive_generalization -> inductive_analogy: 4
- inductive_generalization -> inductive_enumeration: 9
- inductive_statistical -> abductive_best_explanation: 1
- inductive_statistical -> authority_expert: 1

- derivations confidence: tight n=20 mean 0.7480; loose n=93 mean 0.7440; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.4782, bootstrap 95% interval [0.3489, 0.6091]
- Reading: no evidence either way at this n

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=25 (judgeable 25; cannot-judge 0 left out of the denominator): low 92.0% [Wilson 75.0%, 97.8%]; high 96.0% [Wilson 80.5%, 99.3%]; loose 23, partial 1, cannot-judge 0, tight 1
- observation:official_statement: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (observations): low 96.0%, high 98.0% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 92.0%, high 96.0%.

- observations confidence: tight n=1 mean 0.9020; loose n=47 mean 0.8271; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.6915, bootstrap 95% interval [0.5851, 0.7872]
- Reading: confidence tracks correctness in this sample

### pass: without_both_sets

- Status of this pass: derived (combines pre-registered exclusions; not itself pre-registered)

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=20 (judgeable 20; cannot-judge 0 left out of the denominator): low 85.0% [Wilson 64.0%, 94.8%]; high 85.0% [Wilson 64.0%, 94.8%]; loose 17, partial 0, cannot-judge 0, tight 3
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 3, partial 0, cannot-judge 0, tight 1
- derivation:deductive_modus_ponens: n=23 (judgeable 23; cannot-judge 0 left out of the denominator): low 82.6% [Wilson 62.9%, 93.0%]; high 82.6% [Wilson 62.9%, 93.0%]; loose 19, partial 0, cannot-judge 0, tight 4
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_analogy: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_enumeration: n=1 (judgeable 1; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 0
- derivation:inductive_generalization: n=44 (judgeable 44; cannot-judge 0 left out of the denominator): low 86.4% [Wilson 73.3%, 93.6%]; high 86.4% [Wilson 73.3%, 93.6%]; loose 38, partial 0, cannot-judge 0, tight 6
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 84.4%, high 84.4% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 84.4%, high 84.4%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=44 (judgeable 44; cannot-judge 0 left out of the denominator): low 86.4% [Wilson 73.3%, 93.6%]; high 86.4% [Wilson 73.3%, 93.6%]; loose 38, partial 0, cannot-judge 0, tight 6

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 1
- abductive_best_explanation -> deductive_modus_ponens: 1
- abductive_best_explanation -> inductive_enumeration: 1
- deductive_hypothetical_syllogism -> authority_expert: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 2
- deductive_modus_ponens -> abductive_best_explanation: 3
- deductive_modus_ponens -> inductive_causal: 1
- deductive_modus_ponens -> inductive_enumeration: 1
- inductive_analogy -> abductive_best_explanation: 2
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_analogy -> inductive_generalization: 1
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_generalization: 1
- inductive_generalization -> abductive_best_explanation: 14
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_expert: 3
- inductive_generalization -> deductive_modus_ponens: 5
- inductive_generalization -> inductive_analogy: 4
- inductive_generalization -> inductive_enumeration: 9
- inductive_statistical -> abductive_best_explanation: 1
- inductive_statistical -> authority_expert: 1

- derivations confidence: tight n=20 mean 0.7480; loose n=91 mean 0.7404; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.4810, bootstrap 95% interval [0.3503, 0.6082]
- Reading: no evidence either way at this n

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=25 (judgeable 25; cannot-judge 0 left out of the denominator): low 92.0% [Wilson 75.0%, 97.8%]; high 96.0% [Wilson 80.5%, 99.3%]; loose 23, partial 1, cannot-judge 0, tight 1
- observation:official_statement: n=7 (judgeable 7; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (observations): low 96.0%, high 98.0% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 92.0%, high 96.0%.

- observations confidence: tight n=1 mean 0.9020; loose n=47 mean 0.8271; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.6915, bootstrap 95% interval [0.5851, 0.7872]
- Reading: confidence tracks correctness in this sample

### Confidence deltas (item 3b; full set only)

n=65, min -0.7210, median -0.0390, max 0.6640

- dv_0011: inductive_generalization -> deductive_modus_ponens: stored 0.947, recomputed 0.833, delta -0.1140 (3 premises)
- dv_0012: deductive_hypothetical_syllogism -> deductive_modus_ponens: stored 0.884, recomputed 0.884, delta 0.0000 (2 premises)
- dv_0027: abductive_best_explanation -> deductive_modus_ponens: stored 0.522, recomputed 0.639, delta 0.1170 (3 premises)
- dv_0030: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.680, delta -0.2700 (6 premises)
- dv_0061: abductive_best_explanation -> abductive_elimination: stored 0.680, recomputed 0.748, delta 0.0680 (3 premises)
- dv_0102: inductive_generalization -> abductive_best_explanation: stored 0.949, recomputed 0.228, delta -0.7210 (4 premises)
- dv_0116: inductive_generalization -> abductive_best_explanation: stored 0.926, recomputed 0.666, delta -0.2600 (2 premises)
- dv_0137: inductive_generalization -> inductive_enumeration: stored 0.807, recomputed 0.790, delta -0.0170 (1 premises)
- dv_0148: inductive_generalization -> inductive_analogy: stored 0.924, recomputed 0.490, delta -0.4340 (3 premises)
- dv_0169: inductive_generalization -> inductive_enumeration: stored 0.949, recomputed 0.929, delta -0.0200 (3 premises)
- dv_0174: inductive_generalization -> inductive_enumeration: stored 0.950, recomputed 0.930, delta -0.0200 (6 premises)
- dv_0185: inductive_generalization -> abductive_best_explanation: stored 0.945, recomputed 0.722, delta -0.2230 (2 premises)
- dv_0193: inductive_generalization -> inductive_analogy: stored 0.907, recomputed 0.490, delta -0.4170 (2 premises)
- dv_0217: inductive_generalization -> inductive_enumeration: stored 0.950, recomputed 0.930, delta -0.0200 (5 premises)
- dv_0224: inductive_generalization -> inductive_enumeration: stored 0.950, recomputed 0.930, delta -0.0200 (4 premises)
- dv_0246: inductive_generalization -> inductive_enumeration: stored 0.941, recomputed 0.921, delta -0.0200 (2 premises)
- dv_0259: deductive_hypothetical_syllogism -> authority_expert: stored 0.833, recomputed 0.807, delta -0.0260 (3 premises)
- dv_0290: inductive_generalization -> deductive_modus_ponens: stored 0.950, recomputed 0.686, delta -0.2640 (4 premises)
- dv_0291: inductive_generalization -> abductive_best_explanation: stored 0.949, recomputed 0.560, delta -0.3890 (3 premises)
- dv_0299: inductive_generalization -> abductive_best_explanation: stored 0.807, recomputed 0.680, delta -0.1270 (1 premises)
- dv_0324: inductive_generalization -> deductive_modus_ponens: stored 0.944, recomputed 0.439, delta -0.5050 (3 premises)
- dv_0351: inductive_generalization -> authority_expert: stored 0.949, recomputed 0.665, delta -0.2840 (6 premises)
- dv_0354: inductive_generalization -> authority_expert: stored 0.950, recomputed 0.665, delta -0.2850 (9 premises)
- dv_0413: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.532, delta -0.4180 (5 premises)
- dv_0451: inductive_generalization -> abductive_elimination: stored 0.950, recomputed 0.748, delta -0.2020 (8 premises)
- dv_0465: inductive_generalization -> abductive_best_explanation: stored 0.665, recomputed 0.560, delta -0.1050 (6 premises)
- dv_0469: inductive_causal -> abductive_best_explanation: stored 0.615, recomputed 0.578, delta -0.0370 (3 premises)
- dv_0492: inductive_generalization -> inductive_enumeration: stored 0.950, recomputed 0.930, delta -0.0200 (3 premises)
- dv_0498: inductive_enumeration -> inductive_generalization: stored 0.930, recomputed 0.950, delta 0.0200 (4 premises)
- dv_0503: abductive_best_explanation -> inductive_enumeration: stored 0.266, recomputed 0.837, delta 0.5710 (2 premises)
- dv_0507: deductive_hypothetical_syllogism -> deductive_modus_ponens: stored 0.211, recomputed 0.211, delta 0.0000 (5 premises)
- dv_0527: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.448, delta -0.5020 (10 premises)
- dv_0538: inductive_generalization -> deductive_modus_ponens: stored 0.950, recomputed 0.833, delta -0.1170 (4 premises)
- dv_0555: inductive_generalization -> inductive_analogy: stored 0.929, recomputed 0.595, delta -0.3340 (2 premises)
- dv_0566: inductive_generalization -> inductive_enumeration: stored 0.949, recomputed 0.929, delta -0.0200 (3 premises)
- dv_0579: inductive_generalization -> inductive_analogy: stored 0.950, recomputed 0.465, delta -0.4850 (4 premises)
- dv_0581: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.307, delta -0.6430 (10 premises)
- dv_0584: deductive_modus_ponens -> abductive_best_explanation: stored 0.392, recomputed 0.320, delta -0.0720 (4 premises)
- dv_0608: inductive_statistical -> abductive_best_explanation: stored 0.353, recomputed 0.314, delta -0.0390 (2 premises)
- dv_0611: inductive_generalization -> abductive_best_explanation: stored 0.863, recomputed 0.314, delta -0.5490 (2 premises)
- dv_0614: inductive_statistical -> authority_expert: stored 0.353, recomputed 0.372, delta 0.0190 (2 premises)
- dv_0617: inductive_generalization -> deductive_modus_ponens: stored 0.947, recomputed 0.911, delta -0.0360 (2 premises)
- dv_0629: inductive_generalization -> authority_expert: stored 0.921, recomputed 0.380, delta -0.5410 (3 premises)
- dv_0654: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.486, delta -0.4640 (7 premises)
- dv_0659: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.389, delta -0.5610 (7 premises)
- dv_0679: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.722, delta -0.2280 (4 premises)
- dv_0707: inductive_generalization -> inductive_enumeration: stored 0.950, recomputed 0.930, delta -0.0200 (5 premises)
- dv_0714: inductive_generalization -> authority_expert: stored 0.900, recomputed 0.900, delta 0.0000 (1 premises)
- dv_0715: deductive_modus_ponens -> authority_expert: stored 0.686, recomputed 0.665, delta -0.0210 (3 premises)
- dv_0763: deductive_modus_ponens -> abductive_best_explanation: stored 0.686, recomputed 0.560, delta -0.1260 (2 premises)
- dv_0786: inductive_generalization -> inductive_enumeration: stored 0.810, recomputed 0.793, delta -0.0170 (1 premises)
- dv_0828: deductive_modus_ponens -> inductive_enumeration: stored 0.884, recomputed 0.839, delta -0.0450 (1 premises)
- dv_1013: deductive_modus_ponens -> abductive_best_explanation: stored 0.441, recomputed 0.360, delta -0.0810 (5 premises)
- dv_1020: inductive_generalization -> abductive_best_explanation: stored 0.892, recomputed 0.304, delta -0.5880 (2 premises)
- dv_1138: deductive_modus_ponens -> inductive_causal: stored 0.698, recomputed 0.605, delta -0.0930 (1 premises)
- dv_1328: inductive_analogy -> inductive_generalization: stored 0.631, recomputed 0.949, delta 0.3180 (3 premises)
- dv_1398: inductive_analogy -> abductive_best_explanation: stored 0.565, recomputed 0.646, delta 0.0810 (6 premises)
- dv_1424: inductive_analogy -> inductive_generalization: stored 0.631, recomputed 0.941, delta 0.3100 (2 premises)
- dv_1480: inductive_analogy -> deductive_modus_ponens: stored 0.186, recomputed 0.261, delta 0.0750 (3 premises)
- dv_1482: inductive_analogy -> inductive_generalization: stored 0.280, recomputed 0.894, delta 0.6140 (2 premises)
- dv_1483: inductive_analogy -> abductive_best_explanation: stored 0.280, recomputed 0.320, delta 0.0400 (2 premises)
- dv_1502: inductive_analogy -> inductive_enumeration: stored 0.266, recomputed 0.930, delta 0.6640 (8 premises)
- dv_1555: inductive_analogy -> abductive_best_explanation: stored 0.266, recomputed 0.304, delta 0.0380 (5 premises)
- dv_1583: inductive_analogy -> inductive_generalization: stored 0.631, recomputed 0.941, delta 0.3100 (2 premises)
- dv_1619: inductive_analogy -> abductive_best_explanation: stored 0.631, recomputed 0.722, delta 0.0910 (2 premises)

## Author's rates

### pass: all

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=30 (judgeable 30; cannot-judge 0 left out of the denominator): low 66.7% [Wilson 48.8%, 80.8%]; high 66.7% [Wilson 48.8%, 80.8%]; loose 20, partial 0, cannot-judge 0, tight 10
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 4, partial 0, cannot-judge 0, tight 0
- derivation:deductive_modus_ponens: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 41.4% [Wilson 25.5%, 59.3%]; high 41.4% [Wilson 25.5%, 59.3%]; loose 12, partial 0, cannot-judge 0, tight 17
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:inductive_analogy: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 30.8% [Wilson 12.7%, 57.6%]; high 30.8% [Wilson 12.7%, 57.6%]; loose 4, partial 0, cannot-judge 0, tight 9
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:inductive_enumeration: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 96.0% [Wilson 86.5%, 98.9%]; high 96.0% [Wilson 86.5%, 98.9%]; loose 48, partial 0, cannot-judge 0, tight 2
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 60.3%, high 60.3% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 59.3%, high 59.3%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 96.0% [Wilson 86.5%, 98.9%]; high 96.0% [Wilson 86.5%, 98.9%]; loose 48, partial 0, cannot-judge 0, tight 2

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 6
- abductive_best_explanation -> deductive_modus_ponens: 7
- abductive_best_explanation -> deductive_modus_tollens: 1
- authority_expert -> deductive_modus_ponens: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 4
- deductive_modus_ponens -> abductive_best_explanation: 1
- inductive_analogy -> abductive_best_explanation: 1
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_analogy: 1
- inductive_generalization -> abductive_best_explanation: 15
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_consensus: 3
- inductive_generalization -> deductive_modus_ponens: 16
- inductive_generalization -> inductive_analogy: 7
- inductive_generalization -> inductive_enumeration: 3
- inductive_statistical -> deductive_modus_ponens: 2

- derivations confidence: tight n=45 mean 0.6331; loose n=95 mean 0.7569; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.3123, bootstrap 95% interval [0.2294, 0.4025]
- Reading: confidence runs against correctness in this sample

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=9 (judgeable 9; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 9, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=28 (judgeable 28; cannot-judge 0 left out of the denominator): low 85.7% [Wilson 68.5%, 94.3%]; high 85.7% [Wilson 68.5%, 94.3%]; loose 24, partial 0, cannot-judge 0, tight 4
- observation:official_statement: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 84.6% [Wilson 57.8%, 95.7%]; high 92.3% [Wilson 66.7%, 98.6%]; loose 11, partial 1, cannot-judge 0, tight 1

Population-weighted loose rate (observations): low 89.6%, high 91.2% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 85.4%, high 87.7%.

- observations confidence: tight n=5 mean 0.9012; loose n=54 mean 0.8160; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.7037, bootstrap 95% interval [0.5259, 0.8648]
- Reading: confidence tracks correctness in this sample

### pass: without_prior

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 65.5% [Wilson 47.3%, 80.1%]; high 65.5% [Wilson 47.3%, 80.1%]; loose 19, partial 0, cannot-judge 0, tight 10
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 4, partial 0, cannot-judge 0, tight 0
- derivation:deductive_modus_ponens: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 41.4% [Wilson 25.5%, 59.3%]; high 41.4% [Wilson 25.5%, 59.3%]; loose 12, partial 0, cannot-judge 0, tight 17
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:inductive_analogy: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 30.8% [Wilson 12.7%, 57.6%]; high 30.8% [Wilson 12.7%, 57.6%]; loose 4, partial 0, cannot-judge 0, tight 9
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:inductive_enumeration: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 96.0% [Wilson 86.5%, 98.9%]; high 96.0% [Wilson 86.5%, 98.9%]; loose 48, partial 0, cannot-judge 0, tight 2
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 60.0%, high 60.0% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 59.0%, high 59.0%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 96.0% [Wilson 86.5%, 98.9%]; high 96.0% [Wilson 86.5%, 98.9%]; loose 48, partial 0, cannot-judge 0, tight 2

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 6
- abductive_best_explanation -> deductive_modus_ponens: 6
- abductive_best_explanation -> deductive_modus_tollens: 1
- authority_expert -> deductive_modus_ponens: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 4
- deductive_modus_ponens -> abductive_best_explanation: 1
- inductive_analogy -> abductive_best_explanation: 1
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_analogy: 1
- inductive_generalization -> abductive_best_explanation: 15
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_consensus: 3
- inductive_generalization -> deductive_modus_ponens: 16
- inductive_generalization -> inductive_analogy: 7
- inductive_generalization -> inductive_enumeration: 3
- inductive_statistical -> deductive_modus_ponens: 2

- derivations confidence: tight n=45 mean 0.6331; loose n=94 mean 0.7621; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.3059, bootstrap 95% interval [0.2243, 0.3956]
- Reading: confidence runs against correctness in this sample

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=9 (judgeable 9; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 9, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=28 (judgeable 28; cannot-judge 0 left out of the denominator): low 85.7% [Wilson 68.5%, 94.3%]; high 85.7% [Wilson 68.5%, 94.3%]; loose 24, partial 0, cannot-judge 0, tight 4
- observation:official_statement: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 84.6% [Wilson 57.8%, 95.7%]; high 92.3% [Wilson 66.7%, 98.6%]; loose 11, partial 1, cannot-judge 0, tight 1

Population-weighted loose rate (observations): low 89.6%, high 91.2% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 85.4%, high 87.7%.

- observations confidence: tight n=5 mean 0.9012; loose n=54 mean 0.8160; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.7037, bootstrap 95% interval [0.5204, 0.8611]
- Reading: confidence tracks correctness in this sample

### pass: without_manifest

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=30 (judgeable 30; cannot-judge 0 left out of the denominator): low 66.7% [Wilson 48.8%, 80.8%]; high 66.7% [Wilson 48.8%, 80.8%]; loose 20, partial 0, cannot-judge 0, tight 10
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 4, partial 0, cannot-judge 0, tight 0
- derivation:deductive_modus_ponens: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 41.4% [Wilson 25.5%, 59.3%]; high 41.4% [Wilson 25.5%, 59.3%]; loose 12, partial 0, cannot-judge 0, tight 17
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:inductive_analogy: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 30.8% [Wilson 12.7%, 57.6%]; high 30.8% [Wilson 12.7%, 57.6%]; loose 4, partial 0, cannot-judge 0, tight 9
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:inductive_enumeration: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_generalization: n=47 (judgeable 47; cannot-judge 0 left out of the denominator): low 95.7% [Wilson 85.8%, 98.8%]; high 95.7% [Wilson 85.8%, 98.8%]; loose 45, partial 0, cannot-judge 0, tight 2
- derivation:inductive_statistical: n=0 (judgeable 0; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 60.1%, high 60.1% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 59.3%, high 59.3%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=47 (judgeable 47; cannot-judge 0 left out of the denominator): low 95.7% [Wilson 85.8%, 98.8%]; high 95.7% [Wilson 85.8%, 98.8%]; loose 45, partial 0, cannot-judge 0, tight 2

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 6
- abductive_best_explanation -> deductive_modus_ponens: 7
- abductive_best_explanation -> deductive_modus_tollens: 1
- authority_expert -> deductive_modus_ponens: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 4
- deductive_modus_ponens -> abductive_best_explanation: 1
- inductive_analogy -> abductive_best_explanation: 1
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_analogy: 1
- inductive_generalization -> abductive_best_explanation: 14
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_consensus: 3
- inductive_generalization -> deductive_modus_ponens: 14
- inductive_generalization -> inductive_analogy: 7
- inductive_generalization -> inductive_enumeration: 3

- derivations confidence: tight n=45 mean 0.6331; loose n=90 mean 0.7605; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.3090, bootstrap 95% interval [0.2240, 0.4012]
- Reading: confidence runs against correctness in this sample

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=9 (judgeable 9; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 9, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=28 (judgeable 28; cannot-judge 0 left out of the denominator): low 85.7% [Wilson 68.5%, 94.3%]; high 85.7% [Wilson 68.5%, 94.3%]; loose 24, partial 0, cannot-judge 0, tight 4
- observation:official_statement: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 84.6% [Wilson 57.8%, 95.7%]; high 92.3% [Wilson 66.7%, 98.6%]; loose 11, partial 1, cannot-judge 0, tight 1

Population-weighted loose rate (observations): low 89.6%, high 91.2% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 85.4%, high 87.7%.

- observations confidence: tight n=5 mean 0.9012; loose n=54 mean 0.8160; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.7037, bootstrap 95% interval [0.5222, 0.8593]
- Reading: confidence tracks correctness in this sample

### pass: without_both

- Status of this pass: derived (combines pre-registered exclusions; not itself pre-registered)

#### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 65.5% [Wilson 47.3%, 80.1%]; high 65.5% [Wilson 47.3%, 80.1%]; loose 19, partial 0, cannot-judge 0, tight 10
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 4, partial 0, cannot-judge 0, tight 0
- derivation:deductive_modus_ponens: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 41.4% [Wilson 25.5%, 59.3%]; high 41.4% [Wilson 25.5%, 59.3%]; loose 12, partial 0, cannot-judge 0, tight 17
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:inductive_analogy: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 30.8% [Wilson 12.7%, 57.6%]; high 30.8% [Wilson 12.7%, 57.6%]; loose 4, partial 0, cannot-judge 0, tight 9
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:inductive_enumeration: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_generalization: n=47 (judgeable 47; cannot-judge 0 left out of the denominator): low 95.7% [Wilson 85.8%, 98.8%]; high 95.7% [Wilson 85.8%, 98.8%]; loose 45, partial 0, cannot-judge 0, tight 2
- derivation:inductive_statistical: n=0 (judgeable 0; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 59.8%, high 59.8% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 58.9%, high 58.9%.

inductive_generalization on its own:
- derivation:inductive_generalization: n=47 (judgeable 47; cannot-judge 0 left out of the denominator): low 95.7% [Wilson 85.8%, 98.8%]; high 95.7% [Wilson 85.8%, 98.8%]; loose 45, partial 0, cannot-judge 0, tight 2

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> abductive_elimination: 6
- abductive_best_explanation -> deductive_modus_ponens: 6
- abductive_best_explanation -> deductive_modus_tollens: 1
- authority_expert -> deductive_modus_ponens: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 4
- deductive_modus_ponens -> abductive_best_explanation: 1
- inductive_analogy -> abductive_best_explanation: 1
- inductive_analogy -> deductive_modus_ponens: 1
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> inductive_analogy: 1
- inductive_generalization -> abductive_best_explanation: 14
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_consensus: 3
- inductive_generalization -> deductive_modus_ponens: 14
- inductive_generalization -> inductive_analogy: 7
- inductive_generalization -> inductive_enumeration: 3

- derivations confidence: tight n=45 mean 0.6331; loose n=89 mean 0.7659; excluded: partial 0, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.3022, bootstrap 95% interval [0.2181, 0.3901]
- Reading: confidence runs against correctness in this sample

#### observations: per-stratum loose rate

- observation:attributed_analysis: n=9 (judgeable 9; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 9, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=28 (judgeable 28; cannot-judge 0 left out of the denominator): low 85.7% [Wilson 68.5%, 94.3%]; high 85.7% [Wilson 68.5%, 94.3%]; loose 24, partial 0, cannot-judge 0, tight 4
- observation:official_statement: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 8, partial 0, cannot-judge 0, tight 0
- observation:personal_communication: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 84.6% [Wilson 57.8%, 95.7%]; high 92.3% [Wilson 66.7%, 98.6%]; loose 11, partial 1, cannot-judge 0, tight 1

Population-weighted loose rate (observations): low 89.6%, high 91.2% (cannot-judge nodes excluded from the denominator: 0); restricted to strata with at least 10 judgeable: low 85.4%, high 87.7%.

- observations confidence: tight n=5 mean 0.9012; loose n=54 mean 0.8160; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.7037, bootstrap 95% interval [0.5204, 0.8593]
- Reading: confidence tracks correctness in this sample

## Controls (revealed after every reader had locked)

### ariadne
- sensitivity (known-loose classed loose): 7/7
- specificity (known-tight classed tight): 4/4
- known-loose classes: loose 7, tight 0, partial 0, cannot-judge 0
- known-tight classes: loose 0, tight 4, partial 0, cannot-judge 0
- per control: dv_0162 loose, dv_0514 tight, dv_0605 loose, dv_0723 loose, dv_0724 loose, dv_0757 tight, dv_0838 tight, dv_0858 loose, dv_1038 loose, dv_1111 loose, dv_1302 tight
- control ids in her recognized file: dv_0858, dv_1038, dv_1111
- control ids in the mention set: dv_0858, dv_1038, dv_1111

### Control agreement (the author has no control rows)
- ariadne_mira: 8/11 = 72.7%; kappa 0.2979
  - disagreements (id: ariadne / mira):
    - dv_0514: tight / loose
    - dv_0757: tight / loose
    - dv_1302: tight / loose
- ariadne_zephyr: 7/11 = 63.6%; kappa 0.2903
  - disagreements (id: ariadne / zephyr):
    - dv_0724: loose / tight
    - dv_0757: tight / loose
    - dv_1038: loose / tight
    - dv_1111: loose / tight
