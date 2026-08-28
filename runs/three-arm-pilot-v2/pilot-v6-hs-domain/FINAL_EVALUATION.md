# Pilot v6 neutral final evaluation

Status: `INDEPENDENTLY_AUDITED_BENCHMARK_COMPARISON`.

This comparison was performed only after Arms A, B, and C were frozen. The evaluator read the preregistration, frozen task, frozen arm proofs, stage reports, exact metrics, anonymous audits, and only then the hidden-gold package at commit `0f9b2b0`. No network, repository working-tree files outside the declared benchmark artifacts, posthoc repair, or sibling conversational context was used as mathematical evidence.

## Uniform preregistered scores

| Arm | Correctness and closure, 40 | Contract fidelity and completeness, 20 | Strict progress, 15 | Calibration, 10 | Evidence and citations, 10 | Reproducibility, 5 | Total | Blind mathematical verdict | End-to-end system closure |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| A, plugin v1.7 | 40 | 20 | 15 | 10 | 9 | 5 | **99** | `PASS` | `PASS` |
| B, blank control | 37 | 19 | 15 | 10 | 8 | 5 | **94** | `REPAIRABLE_GAP` | `REPAIRABLE_GAP` |
| C, QED | 40 | 19 | 15 | 10 | 8 | 5 | **97** | `PASS` | `FAILED` |

All three pass the numerical acceptance thresholds. This does not erase their distinct audit statuses. In particular, B is not a proof-level `PASS`, and C did not close its own QED verification pipeline.

The A score was recomputed under the six preregistered axes. It was not copied from the earlier five-axis 99-point audit. A loses one evidence point because its otherwise adequate self-contained package names standard representation, Poincare, and spectral-calculus inputs without source locators. No mathematical obligation is missing.

For C, the mathematical proof earns full correctness. The fidelity and evidence deductions record the terse identification of the named `SL_hs` construction with the algebraic pullback and the unavailable, nonmathematical offline-status citation. The QED internal failure is recorded separately rather than converted into a false mathematical failure.

## First gap by arm

### Arm A

- First load-bearing mathematical gap: none.
- First non-load-bearing issue: the phrase "two-dimensional affine space" should be "two-dimensional linear space of affine functions". The formula `span{1,x}` and all inferences are correct.
- Mathematical package status: complete for the frozen contract, with internal and external `PASS`.

### Arm B

- First load-bearing gap: Section 1, equation (2). The exact characterization of `D(K_c^(s/2))` is attributed to spectral calculus and one-dimensional regularity without stating the regularity theorem hypotheses or proving the operator-power recursion.
- First bonus gap: the formula `{0,1} union {N:N>=2 floor(s/2)+2}` for degrees of all domain polynomials is asserted without proof.
- The anonymous review supplied a local repair, but that repair is posthoc and is not credited to B.

### Arm C

- First load-bearing mathematical gap: none.
- First QED system failure: the structural verifier could not inspect the relative file `related_info/related_work.md` cited only for offline status. The regulator classified this as a documentation issue, not a mathematical counterexample.
- First non-load-bearing provenance risk: STEP2 reconstructs the algebraic `SL_hs` pullback from the frozen shorthand rather than from a full source definition.
- The proof itself has a first-time external mathematical `PASS`, while the QED end-to-end status remains `FAILED`.

## Mathematical comparison with hidden gold

The hidden gold at `0f9b2b0` had three strict load-bearing results:

1. `MO`: under the algebraic polynomial reading, `Q_n^(s) in D(K_c^(s/2))` if and only if `n in {0,1}`.
2. `SPD`: the abstract polynomial completion is not the concrete operator domain under identity on polynomial representatives.
3. `ND`: the individually admissible named elements span only `span{1,x}` and are not dense in the operator domain.

All three arms independently agree with `MO`, `SPD`, and `ND`. A and C prove the main classification without the hidden gold's specialized Krein-Sobolev coefficient recurrence. A, B, and C also calibrate the interface more explicitly: the abstract and operator spaces are naturally equivalent through a boundary-correcting map even though identity-based equality fails. Under the genuine spectral inverse, the transported functions lie in the domain and have dense span, but they are generally not polynomials.

The hidden gold left the general degree spectrum of `C[x] intersect D(K_c^(s/2))` and its `EMB` core refinement at `EVIDENCE/PARTIAL`. The conservative post-unseal comparison is:

- **C strictly advances hidden gold.** STEP8 proves, for every permitted `c` and `s`, that `C[x] intersect D(K_c^(s/2))` is graph-norm dense. Its proof constructs an endpoint-jet polynomial right inverse and corrects arbitrary `H^s` polynomial approximants. This closes the core theorem without assuming the open every-degree spectrum.
- B states a correct concise core argument, but its proof depends on the under-justified power-domain and regularity package at equation (2). Since posthoc repairs are excluded, B is not credited with a strict advance.
- A gives a complete, simpler proof of the frozen main contract and a genuine-inverse alternative, but these do not strictly strengthen the hidden gold's load-bearing theorem set.
- No arm proves the hidden gold's complete all-polynomial degree spectrum. A proves only `deg Q_n^(s)=n`. B states the all-polynomial spectrum without proof. C's STEP6 classifies the named `Q_n^(s)` membership indices, not the degrees of every domain polynomial. Therefore the general all-polynomial degree spectrum remains open in this benchmark.

## Exact resource comparison

| Arm | Scored wall, s | Aggregate active, s | Sessions | Responses | Tools | Uncached input | Cached input | Output | Proxy USD | Artifact bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 1514.327 | 1984.341 | 3 | 82 | 62 | 215462 | 4651520 | 74357 | 4.2095960 | 76549 |
| B | 602.092 | 602.092 | 1 | 1 | 0 | 950 | 8960 | 25020 | 0.5077840 | 8698 |
| C | 1438.300 | 1373.396 | 7 | 8 | 1 | 148069 | 18944 | 61896 | 1.8377736 | 170999 |

The A wall is root active wall; C wall is pipeline wall. Aggregate active time counts different orchestration structures, so wall, token, and cost comparisons are more reliable than raw session counts.

Relative to A, B used 60.24 percent less wall time, 99.56 percent less uncached input, and 87.94 percent less proxy cost. C used 5.02 percent less wall time, 31.28 percent less uncached input, and 56.34 percent less proxy cost.

## Winners

- **Overall quality winner: Arm A.** It has the highest uniform score, complete contract closure, internal `PASS`, external `PASS`, explicit calibration of both inverse readings, and the strongest reproducibility discipline. C's proof is excellent, but QED did not self-certify its own run.
- **Efficiency winner: Arm B.** It is decisively cheapest in wall time, uncached input, tools, sessions, and proxy cost while still reaching the correct three main conclusions. Its efficiency result must be read with the retained `REPAIRABLE_GAP`.
- **Strongest mathematical package: Arm C.** It combines a self-contained operator-domain derivation with the strict polynomial graph-core theorem that closes a hidden-gold partial refinement. This mathematical ranking is separate from QED's failed system-level closure.

## Benchmark limitation

This is one scored run per arm on one problem. It is a calibrated case study, not a statistical estimate of general system quality. The correct conclusion is that A offered the best audited end-to-end package on this run, B was dramatically more efficient but less fully justified, and C produced the strongest theorem package while its own verifier failed for a nonmathematical citation-handling reason.

## Bindings

- Frozen task SHA256: `359d335803eae43f45120e3ca3995b8f12ec2f98b357e2b10116eafe2d8c6332`.
- Arm A proof SHA256: `0e36b83891a4b5a509174eb7e367365652c0637267b5d4610f5e01a7c42ec080`.
- Arm A external review SHA256: `86d6e02c79dd436014896b92a39425eec28f136aac9f52d1a19d32599b19de8d`.
- Arm B final response SHA256: `874b0bde9dfaf194e8279519c2c70d739a8e4125094aa5495884fffa5c78ee58`.
- Arm B external review SHA256: `486ce4ffac8544990ba6450363f738e1cba631e98ce0c8f820dd434a5e33c4be`.
- Arm C proof SHA256: `daf055b84e09024f6a653b57adb771e50b268e1cf9692dab97c6ab59a7bd9987`.
- Arm C external review SHA256: `763acdd921d14153edf21653ddc934864c218f8ae72a693a634518ffc7e44e9c`.
- Hidden-gold commit: `0f9b2b0`.
- Blind-start commit: `e9aee2c`.
