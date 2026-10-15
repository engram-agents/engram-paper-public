# Node audit analysis report

Seed `2026-10-14-node-audit`; analyst-prior node `dv_0138`; bootstrap resamples 10000; vendored v0.5.1 confidence module sha256 `5ea367d8d15153e82b68d3fdf5f08ef12b5d5555be9326f5ee65e0a12ac260e0`.
Rates and confidence use the primary reader's (Mira's) verdicts on sampled nodes; controls are excluded from every rate.

## Free parameters

- strata with fewer than 10 judgeable nodes report counts only (no rate, no interval)
- judgeable nodes = tight + loose + partial; cannot-judge nodes are excluded and counted beside each rate
- low bound counts partial as tight; high bound counts partial as loose
- Wilson, z = 1.959963984540054
- census population shares of each stratum, renormalised over strata with at least 1 judgeable node; strata left out of the weights are listed under each weighted rate (no draw; no judgeable node)
- P(conf(tight) > conf(loose)), ties count 0.5; bootstrap resamples the tight and loose groups separately, 10000 resamples, percentile 95% interval, seed string '{seed}:boot:{label}' with seed '2026-10-14-node-audit'
- CI lower > 0.5: 'confidence tracks correctness in this sample'; CI contains 0.5: 'no evidence either way at this n'; CI upper < 0.5: 'confidence runs against correctness in this sample'; no tight or no loose node: 'not computable: needs at least one tight and one loose node'
- premise set = derives_from + acknowledged_derives_from targets (tools/modus_ponens_check.py computed-from set); v0.5.1 formula from the vendored module (sha256 5ea367d8d15153e82b68d3fdf5f08ef12b5d5555be9326f5ee65e0a12ac260e0); computed once over all nodes
- rates and AUC use the primary reader's (Mira's) verdicts; Zephyr's feed controls and agreement only; analyst-prior node dv_0138 reported with and without

## Verdict files (sha256 of each reader's full file as read)

- Mira: `2aa4437a56234cebf5384b5f81749e91e0477e6c8411496093bf2d0735fbaefb`
- Zephyr: `ad503b27484016e2203d71164f7ee5eac0d2383a41048e6ab9f9a39e62808915`

## Validation

- Mira: 211 rows (200 sampled + 11 controls). Zephyr: 61 rows (50 overlap + 11 controls). All rows valid; none dropped.

## Cannot-judge counts (never folded into tight or loose)

### mira
- derivation nodes by class: loose 130, tight 7, partial 3, cannot-judge 0
- observation nodes by class: loose 56, tight 3, partial 1, cannot-judge 0
- check type: tight 80, loose 59, cannot-judge 1
- check placement: tight 89, loose 51, cannot-judge 0
- check chain-overreach: tight 11, loose 120, cannot-judge 9
- check support-overreach: tight 4, loose 56, cannot-judge 0
- check quote_type: tight 40, loose 19, cannot-judge 1
- check source_class: tight 38, loose 11, cannot-judge 11

### zephyr
- derivation nodes by class: loose 24, tight 21, partial 0, cannot-judge 0
- observation nodes by class: loose 0, tight 5, partial 0, cannot-judge 0
- check type: tight 36, loose 9, cannot-judge 0
- check placement: tight 34, loose 11, cannot-judge 0
- check chain-overreach: tight 33, loose 12, cannot-judge 0
- check support-overreach: tight 5, loose 0, cannot-judge 0
- check quote_type: tight 5, loose 0, cannot-judge 0
- check source_class: tight 5, loose 0, cannot-judge 0

## Loose rates and confidence, WITH the analyst-prior node

### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=30 (judgeable 30; cannot-judge 0 left out of the denominator): low 93.3% [Wilson 78.7%, 98.2%]; high 96.7% [Wilson 83.3%, 99.4%]; loose 28, partial 1, cannot-judge 0, tight 1
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 4, partial 0, cannot-judge 0, tight 0
- derivation:deductive_modus_ponens: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 89.7% [Wilson 73.6%, 96.4%]; high 96.6% [Wilson 82.8%, 99.4%]; loose 26, partial 2, cannot-judge 0, tight 1
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:inductive_analogy: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 100.0% [Wilson 77.2%, 100.0%]; high 100.0% [Wilson 77.2%, 100.0%]; loose 13, partial 0, cannot-judge 0, tight 0
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_enumeration: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 98.0% [Wilson 89.5%, 99.6%]; high 98.0% [Wilson 89.5%, 99.6%]; loose 49, partial 0, cannot-judge 0, tight 1
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 93.0%, high 96.0% (weights = census shares of strata with at least one judgeable node; no interval; cannot-judge nodes excluded from the denominator: 0).
Restricted to strata with at least 10 judgeable: low 93.9%, high 97.4%.
Strata with no drawn node (population shown): derivation:authority_consensus (0), derivation:deductive_reductio (0)
Strata drawn but with no judgeable node (population shown): none

inductive_generalization on its own:
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 98.0% [Wilson 89.5%, 99.6%]; high 98.0% [Wilson 89.5%, 99.6%]; loose 49, partial 0, cannot-judge 0, tight 1

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> inductive_analogy: 1
- abductive_best_explanation -> inductive_enumeration: 1
- deductive_hypothetical_syllogism -> abductive_best_explanation: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 2
- deductive_hypothetical_syllogism -> other (not a v0.5.1 type; text withheld): 1
- deductive_modus_ponens -> abductive_best_explanation: 5
- deductive_modus_ponens -> other (not a v0.5.1 type; text withheld): 4
- inductive_analogy -> abductive_best_explanation: 2
- inductive_analogy -> inductive_generalization: 2
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> abductive_best_explanation: 2
- inductive_generalization -> abductive_best_explanation: 18
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_consensus: 2
- inductive_generalization -> authority_expert: 1
- inductive_generalization -> deductive_modus_ponens: 1
- inductive_generalization -> deductive_reductio: 1
- inductive_generalization -> inductive_analogy: 4
- inductive_generalization -> inductive_enumeration: 5
- inductive_generalization -> other (not a v0.5.1 type; text withheld): 2
- inductive_statistical -> abductive_best_explanation: 1
- inductive_statistical -> deductive_modus_ponens: 1

### derivations: confidence vs verdict (small-n, exploratory)

- tight n=7 mean 0.7273; loose n=130 mean 0.7186; excluded: partial 3, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.4709, bootstrap 95% interval [0.3077, 0.6533]
- Reading: no evidence either way at this n

### observations: per-stratum loose rate

- observation:attributed_analysis: n=9 (judgeable 9; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 9, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=28 (judgeable 28; cannot-judge 0 left out of the denominator): low 92.9% [Wilson 77.4%, 98.0%]; high 96.4% [Wilson 82.3%, 99.4%]; loose 26, partial 1, cannot-judge 0, tight 1
- observation:official_statement: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 1
- observation:personal_communication: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 92.3% [Wilson 66.7%, 98.6%]; high 92.3% [Wilson 66.7%, 98.6%]; loose 12, partial 0, cannot-judge 0, tight 1

Population-weighted loose rate (observations): low 93.2%, high 95.0% (weights = census shares of strata with at least one judgeable node; no interval; cannot-judge nodes excluded from the denominator: 0).
Restricted to strata with at least 10 judgeable: low 92.7%, high 95.2%.
Strata with no drawn node (population shown): none
Strata drawn but with no judgeable node (population shown): none

### observations: confidence vs verdict (small-n, exploratory)

- tight n=3 mean 0.8673; loose n=56 mean 0.8110; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.5060, bootstrap 95% interval [0.3304, 0.7054]
- Reading: no evidence either way at this n

## Loose rates and confidence, WITHOUT the analyst-prior node

### derivations: per-stratum loose rate

- derivation:abductive_best_explanation: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 93.1% [Wilson 78.0%, 98.1%]; high 96.6% [Wilson 82.8%, 99.4%]; loose 27, partial 1, cannot-judge 0, tight 1
- derivation:abductive_elimination: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:authority_expert: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 0, partial 0, cannot-judge 0, tight 2
- derivation:deductive_disjunctive: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:deductive_hypothetical_syllogism: n=4 (judgeable 4; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 4, partial 0, cannot-judge 0, tight 0
- derivation:deductive_modus_ponens: n=29 (judgeable 29; cannot-judge 0 left out of the denominator): low 89.7% [Wilson 73.6%, 96.4%]; high 96.6% [Wilson 82.8%, 99.4%]; loose 26, partial 2, cannot-judge 0, tight 1
- derivation:deductive_modus_tollens: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:inductive_analogy: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 100.0% [Wilson 77.2%, 100.0%]; high 100.0% [Wilson 77.2%, 100.0%]; loose 13, partial 0, cannot-judge 0, tight 0
- derivation:inductive_causal: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 1, partial 0, cannot-judge 0, tight 1
- derivation:inductive_enumeration: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 98.0% [Wilson 89.5%, 99.6%]; high 98.0% [Wilson 89.5%, 99.6%]; loose 49, partial 0, cannot-judge 0, tight 1
- derivation:inductive_statistical: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0

Population-weighted loose rate (derivations): low 92.9%, high 96.0% (weights = census shares of strata with at least one judgeable node; no interval; cannot-judge nodes excluded from the denominator: 0).
Restricted to strata with at least 10 judgeable: low 93.9%, high 97.3%.
Strata with no drawn node (population shown): derivation:authority_consensus (0), derivation:deductive_reductio (0)
Strata drawn but with no judgeable node (population shown): none

inductive_generalization on its own:
- derivation:inductive_generalization: n=50 (judgeable 50; cannot-judge 0 left out of the denominator): low 98.0% [Wilson 89.5%, 99.6%]; high 98.0% [Wilson 89.5%, 99.6%]; loose 49, partial 0, cannot-judge 0, tight 1

Declared type x proposed type over `loose:type` verdicts:
- abductive_best_explanation -> inductive_analogy: 1
- abductive_best_explanation -> inductive_enumeration: 1
- deductive_hypothetical_syllogism -> abductive_best_explanation: 1
- deductive_hypothetical_syllogism -> deductive_modus_ponens: 2
- deductive_hypothetical_syllogism -> other (not a v0.5.1 type; text withheld): 1
- deductive_modus_ponens -> abductive_best_explanation: 5
- deductive_modus_ponens -> other (not a v0.5.1 type; text withheld): 4
- inductive_analogy -> abductive_best_explanation: 2
- inductive_analogy -> inductive_generalization: 2
- inductive_causal -> abductive_best_explanation: 1
- inductive_enumeration -> abductive_best_explanation: 2
- inductive_generalization -> abductive_best_explanation: 18
- inductive_generalization -> abductive_elimination: 1
- inductive_generalization -> authority_consensus: 2
- inductive_generalization -> authority_expert: 1
- inductive_generalization -> deductive_modus_ponens: 1
- inductive_generalization -> deductive_reductio: 1
- inductive_generalization -> inductive_analogy: 4
- inductive_generalization -> inductive_enumeration: 5
- inductive_generalization -> other (not a v0.5.1 type; text withheld): 2
- inductive_statistical -> abductive_best_explanation: 1
- inductive_statistical -> deductive_modus_ponens: 1

### derivations: confidence vs verdict (small-n, exploratory)

- tight n=7 mean 0.7273; loose n=129 mean 0.7221; excluded: partial 3, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.4668, bootstrap 95% interval [0.3018, 0.6462]
- Reading: no evidence either way at this n

### observations: per-stratum loose rate

- observation:attributed_analysis: n=9 (judgeable 9; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 9, partial 0, cannot-judge 0, tight 0
- observation:editorial: n=2 (judgeable 2; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 2, partial 0, cannot-judge 0, tight 0
- observation:hard_data: n=28 (judgeable 28; cannot-judge 0 left out of the denominator): low 92.9% [Wilson 77.4%, 98.0%]; high 96.4% [Wilson 82.3%, 99.4%]; loose 26, partial 1, cannot-judge 0, tight 1
- observation:official_statement: n=8 (judgeable 8; cannot-judge 0 left out of the denominator): counts only (fewer than 10 judgeable): loose 7, partial 0, cannot-judge 0, tight 1
- observation:personal_communication: n=13 (judgeable 13; cannot-judge 0 left out of the denominator): low 92.3% [Wilson 66.7%, 98.6%]; high 92.3% [Wilson 66.7%, 98.6%]; loose 12, partial 0, cannot-judge 0, tight 1

Population-weighted loose rate (observations): low 93.2%, high 95.0% (weights = census shares of strata with at least one judgeable node; no interval; cannot-judge nodes excluded from the denominator: 0).
Restricted to strata with at least 10 judgeable: low 92.7%, high 95.2%.
Strata with no drawn node (population shown): none
Strata drawn but with no judgeable node (population shown): none

### observations: confidence vs verdict (small-n, exploratory)

- tight n=3 mean 0.8673; loose n=56 mean 0.8110; excluded: partial 1, cannot-judge 0
- AUC P(conf(tight) > conf(loose)): 0.5060, bootstrap 95% interval [0.3214, 0.7054]
- Reading: no evidence either way at this n

## Confidence deltas (item 3b: v0.5.1 formula under the reader's proposed type)

n=52, min -0.7210, median -0.1865, max 0.6140

- dv_0011: inductive_generalization -> abductive_best_explanation: stored 0.947, recomputed 0.680, delta -0.2670 (3 premises)
- dv_0012: deductive_hypothetical_syllogism -> deductive_modus_ponens: stored 0.884, recomputed 0.884, delta 0.0000 (2 premises)
- dv_0030: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.680, delta -0.2700 (6 premises)
- dv_0064: deductive_modus_ponens -> abductive_best_explanation: stored 0.833, recomputed 0.680, delta -0.1530 (3 premises)
- dv_0086: deductive_modus_ponens -> abductive_best_explanation: stored 0.931, recomputed 0.760, delta -0.1710 (2 premises)
- dv_0102: inductive_generalization -> abductive_best_explanation: stored 0.949, recomputed 0.228, delta -0.7210 (4 premises)
- dv_0112: inductive_generalization -> authority_consensus: stored 0.948, recomputed 0.978, delta 0.0300 (2 premises)
- dv_0169: inductive_generalization -> abductive_best_explanation: stored 0.949, recomputed 0.566, delta -0.3830 (3 premises)
- dv_0174: inductive_generalization -> inductive_enumeration: stored 0.950, recomputed 0.930, delta -0.0200 (6 premises)
- dv_0185: inductive_generalization -> inductive_enumeration: stored 0.945, recomputed 0.925, delta -0.0200 (2 premises)
- dv_0193: inductive_generalization -> inductive_analogy: stored 0.907, recomputed 0.490, delta -0.4170 (2 premises)
- dv_0217: inductive_generalization -> inductive_enumeration: stored 0.950, recomputed 0.930, delta -0.0200 (5 premises)
- dv_0249: inductive_generalization -> abductive_best_explanation: stored 0.936, recomputed 0.680, delta -0.2560 (2 premises)
- dv_0259: deductive_hypothetical_syllogism -> abductive_best_explanation: stored 0.833, recomputed 0.680, delta -0.1530 (3 premises)
- dv_0290: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.560, delta -0.3900 (4 premises)
- dv_0299: inductive_generalization -> abductive_best_explanation: stored 0.807, recomputed 0.680, delta -0.1270 (1 premises)
- dv_0324: inductive_generalization -> abductive_best_explanation: stored 0.944, recomputed 0.358, delta -0.5860 (3 premises)
- dv_0351: inductive_generalization -> authority_expert: stored 0.949, recomputed 0.665, delta -0.2840 (6 premises)
- dv_0354: inductive_generalization -> deductive_reductio: stored 0.950, recomputed 0.686, delta -0.2640 (9 premises)
- dv_0356: inductive_generalization -> authority_consensus: stored 0.949, recomputed 0.979, delta 0.0300 (6 premises)
- dv_0413: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.532, delta -0.4180 (5 premises)
- dv_0451: inductive_generalization -> abductive_elimination: stored 0.950, recomputed 0.748, delta -0.2020 (8 premises)
- dv_0469: inductive_causal -> abductive_best_explanation: stored 0.615, recomputed 0.578, delta -0.0370 (3 premises)
- dv_0498: inductive_enumeration -> abductive_best_explanation: stored 0.930, recomputed 0.544, delta -0.3860 (4 premises)
- dv_0527: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.448, delta -0.5020 (10 premises)
- dv_0538: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.680, delta -0.2700 (4 premises)
- dv_0555: inductive_generalization -> inductive_analogy: stored 0.929, recomputed 0.595, delta -0.3340 (2 premises)
- dv_0579: inductive_generalization -> inductive_analogy: stored 0.950, recomputed 0.465, delta -0.4850 (4 premises)
- dv_0581: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.307, delta -0.6430 (10 premises)
- dv_0608: inductive_statistical -> abductive_best_explanation: stored 0.353, recomputed 0.314, delta -0.0390 (2 premises)
- dv_0611: inductive_generalization -> abductive_best_explanation: stored 0.863, recomputed 0.314, delta -0.5490 (2 premises)
- dv_0614: inductive_statistical -> deductive_modus_ponens: stored 0.353, recomputed 0.384, delta 0.0310 (2 premises)
- dv_0617: inductive_generalization -> inductive_enumeration: stored 0.947, recomputed 0.927, delta -0.0200 (2 premises)
- dv_0628: deductive_hypothetical_syllogism -> deductive_modus_ponens: stored 0.980, recomputed 0.980, delta 0.0000 (2 premises)
- dv_0629: inductive_generalization -> deductive_modus_ponens: stored 0.921, recomputed 0.392, delta -0.5290 (3 premises)
- dv_0646: abductive_best_explanation -> inductive_enumeration: stored 0.760, recomputed 0.930, delta 0.1700 (8 premises)
- dv_0654: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.486, delta -0.4640 (7 premises)
- dv_0659: inductive_generalization -> abductive_best_explanation: stored 0.950, recomputed 0.389, delta -0.5610 (7 premises)
- dv_0707: inductive_generalization -> inductive_enumeration: stored 0.950, recomputed 0.930, delta -0.0200 (5 premises)
- dv_0714: inductive_generalization -> inductive_analogy: stored 0.900, recomputed 0.663, delta -0.2370 (1 premises)
- dv_0763: deductive_modus_ponens -> abductive_best_explanation: stored 0.686, recomputed 0.560, delta -0.1260 (2 premises)
- dv_0786: inductive_generalization -> abductive_best_explanation: stored 0.810, recomputed 0.682, delta -0.1280 (1 premises)
- dv_0795: inductive_generalization -> abductive_best_explanation: stored 0.937, recomputed 0.560, delta -0.3770 (3 premises)
- dv_0828: deductive_modus_ponens -> abductive_best_explanation: stored 0.884, recomputed 0.722, delta -0.1620 (1 premises)
- dv_0918: abductive_best_explanation -> inductive_analogy: stored 0.202, recomputed 0.176, delta -0.0260 (2 premises)
- dv_1020: inductive_generalization -> abductive_best_explanation: stored 0.892, recomputed 0.304, delta -0.5880 (2 premises)
- dv_1424: inductive_analogy -> abductive_best_explanation: stored 0.631, recomputed 0.722, delta 0.0910 (2 premises)
- dv_1482: inductive_analogy -> inductive_generalization: stored 0.280, recomputed 0.894, delta 0.6140 (2 premises)
- dv_1494: deductive_modus_ponens -> abductive_best_explanation: stored 0.791, recomputed 0.646, delta -0.1450 (2 premises)
- dv_1548: inductive_enumeration -> abductive_best_explanation: stored 0.930, recomputed 0.722, delta -0.2080 (4 premises)
- dv_1583: inductive_analogy -> inductive_generalization: stored 0.631, recomputed 0.941, delta 0.3100 (2 premises)
- dv_1619: inductive_analogy -> abductive_best_explanation: stored 0.631, recomputed 0.722, delta 0.0910 (2 premises)
- dv_0115: deductive_modus_ponens -> other (not a v0.5.1 type; text withheld): NOT computed (proposed_type is not in the v0.5.1 reasoning table)
- dv_0116: inductive_generalization -> other (not a v0.5.1 type; text withheld): NOT computed (proposed_type is not in the v0.5.1 reasoning table)
- dv_0246: inductive_generalization -> other (not a v0.5.1 type; text withheld): NOT computed (proposed_type is not in the v0.5.1 reasoning table)
- dv_0507: deductive_hypothetical_syllogism -> other (not a v0.5.1 type; text withheld): NOT computed (proposed_type is not in the v0.5.1 reasoning table)
- dv_0822: deductive_modus_ponens -> other (not a v0.5.1 type; text withheld): NOT computed (proposed_type is not in the v0.5.1 reasoning table)
- dv_0902: deductive_modus_ponens -> other (not a v0.5.1 type; text withheld): NOT computed (proposed_type is not in the v0.5.1 reasoning table)
- dv_1138: deductive_modus_ponens -> other (not a v0.5.1 type; text withheld): NOT computed (proposed_type is not in the v0.5.1 reasoning table)

## Agreement (overlap, controls excluded)

- node class (partial its own category): 26/50 = 52.0% agreement; kappa 0.0909
- tight vs loose, restricted to nodes both classed tight or loose (n=49): kappa 0.0785
- per-check percent agreement:
  - type: 28/45 = 62.2%
  - placement: 24/45 = 53.3%
  - chain-overreach: 15/45 = 33.3%
  - support-overreach: 0/5 = 0.0%
  - quote_type: 3/5 = 60.0%
  - source_class: 3/5 = 60.0%
- disagreements (id: Mira / Zephyr):
  - dv_0112: loose / tight
  - dv_0174: loose / tight
  - dv_0217: loose / tight
  - dv_0224: loose / tight
  - dv_0259: loose / tight
  - dv_0604: partial / tight
  - dv_0629: loose / tight
  - dv_0715: loose / tight
  - dv_0759: loose / tight
  - dv_0795: loose / tight
  - dv_0802: loose / tight
  - dv_0805: loose / tight
  - dv_0850: loose / tight
  - dv_0960: loose / tight
  - dv_1180: loose / tight
  - dv_1199: loose / tight
  - dv_1513: loose / tight
  - dv_1565: loose / tight
  - dv_1622: loose / tight
  - ob_0024: loose / tight
  - ob_0759: loose / tight
  - ob_1550: loose / tight
  - ob_3773: loose / tight
  - ob_3941: loose / tight

## Controls (revealed after both verdict sets were locked)

### mira
- sensitivity (known-loose classed loose): 7/7
- specificity (known-tight classed tight): 1/4
- known-loose classes: loose 7, tight 0, partial 0, cannot-judge 0
- known-tight classes: loose 3, tight 1, partial 0, cannot-judge 0
- per control: dv_0162 loose, dv_0514 loose, dv_0605 loose, dv_0723 loose, dv_0724 loose, dv_0757 loose, dv_0838 tight, dv_0858 loose, dv_1038 loose, dv_1111 loose, dv_1302 loose

### zephyr
- sensitivity (known-loose classed loose): 4/7
- specificity (known-tight classed tight): 3/4
- known-loose classes: loose 4, tight 3, partial 0, cannot-judge 0
- known-tight classes: loose 1, tight 3, partial 0, cannot-judge 0
- per control: dv_0162 loose, dv_0514 tight, dv_0605 loose, dv_0723 loose, dv_0724 tight, dv_0757 loose, dv_0838 tight, dv_0858 loose, dv_1038 tight, dv_1111 tight, dv_1302 tight

### Control agreement (separate from the overlap)
- 6/11 = 54.5%; kappa 0.1538
- disagreements (id: Mira / Zephyr):
  - dv_0514: loose / tight
  - dv_0724: loose / tight
  - dv_1038: loose / tight
  - dv_1111: loose / tight
  - dv_1302: loose / tight
