# Pilot v6 H^s-domain three-arm results

## Bottom line

All three frozen arms independently reached the same three required mathematical conclusions. Under
the algebraic polynomial reading, the transported polynomial belongs to the operator power domain
exactly at indices 0 and 1. The abstract polynomial completion is not the concrete operator domain
under identity on polynomial representatives, and the individually admissible named system is not
dense there.

The uniform preregistered scores are A=99, B=94, and C=97. The result has three different winners:

- Overall audited quality: Arm A, our v1.7 plugin.
- Resource efficiency: Arm B, the blank task-only control.
- Strongest mathematical package: Arm C, real QED.

This is one run per arm on one problem. It is a calibrated case study, not a statistical ranking of
plugins or models.

## Uniform scored comparison

| Arm | System | Score | Blind mathematical verdict | End-to-end status | Strongest scored result | Wall | Uncached input | Output | Cost proxy |
| --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| A | rigorous-open-math-research v1.7 with 2 research children | 99 | `PASS` | `PASS` | Complete frozen contract, both inverse readings, internal and external audit | 1514.327 s | 215462 | 74357 | USD 4.2095960 |
| B | Blank Codex, task prompt only | 94 | `REPAIRABLE_GAP` | `REPAIRABLE_GAP` | Correct three main conclusions, with one local load-bearing support gap | 602.092 s | 950 | 25020 | USD 0.5077840 |
| C | QED 1219009 with offline Codex adapter | 97 | `PASS` | `FAILED` | Complete proof plus strict polynomial graph-core theorem | 1438.300 s | 148069 | 61896 | USD 1.8377736 |

All roles used `gpt-5.6-sol` at `xhigh`. Every arm passes the numerical acceptance threshold, but
the threshold does not erase audit labels. In particular, B is not proof-level `PASS`, and QED did
not self-certify C even though C's frozen proof passed an independent first-time mathematical audit.

### Six preregistered axes

| Arm | Correctness, 40 | Fidelity, 20 | Strict progress, 15 | Calibration, 10 | Evidence, 10 | Reproducibility, 5 | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 40 | 20 | 15 | 10 | 9 | 5 | 99 |
| B | 37 | 19 | 15 | 10 | 8 | 5 | 94 |
| C | 40 | 19 | 15 | 10 | 8 | 5 | 97 |

The A score was recomputed under these axes and was not copied from its earlier five-axis audit.
The immutable blind audits contain two over-broad bonus labels: C's `degree_spectrum` field refers
only to the named `Q_n` membership indices, and B's strict-progress prose mentions an unproved
all-polynomial spectrum. `AUDIT_ERRATA.md` records the corrections. The uniform scores above do not
credit either arm with the all-polynomial degree-spectrum theorem.

## Exact mathematical result

For every real `c>0`, every integer `s>=4`, and every `n>=0`, with the algebraic inverse of
`L=c-D^2` on polynomials,

```text
Q_n^(s) in D(K_c^(s/2)) if and only if n in {0,1}.
```

The strict interface is:

- The algebraic polynomial completion is not equal to `D(K_c^(s/2))` under identity on polynomial
  representatives.
- A boundary-correcting map gives a natural unitary equivalence between the abstract energy
  completion and the operator domain.
- The literal full named polynomial span is not contained in the operator domain. Its individually
  admissible members span only `span{1,x}`, hence are not dense.
- Under the genuine spectral inverse, all transported functions belong to the required operator
  domain and their span is dense, but those functions are generally non-polynomial.

## Arm-specific findings

### Arm A

Arm A closed the contract with an internal independent audit and an external anonymous `PASS`.
Its proof used the boundary form and a zero-energy obstruction, covered both algebraic and genuine
inverse readings, produced exact replay material, and preserved the largest audit-oriented research
package. There is no load-bearing gap. The only recorded issue is the harmless wording
`two-dimensional affine space`, where the formula correctly says `span{1,x}`.

### Arm B

Arm B obtained the correct result in one response with no tools or child sessions. Its first
load-bearing support gap is Section 1, equation (2): it invokes the exact power-domain
characterization through spectral calculus and one-dimensional regularity without stating the
hypotheses or proving the recursion. The repair is local, but it was supplied posthoc and is not
credited to the scored arm. B therefore remains `REPAIRABLE_GAP` despite its high score.

### Arm C

QED produced a complete eight-step proof and the strongest scored theorem package. In addition to
the frozen contract, it proved

```text
C[x] intersect D(K_c^(s/2)) is graph-norm dense in D(K_c^(s/2)).
```

The proof uses `H^s` polynomial approximation, an endpoint-jet polynomial right inverse, and
finite-dimensional correction of every boundary residual. The external anonymous mathematical
audit returned `PASS`.

QED's own structural verifier nevertheless set the pipeline status to `FAILED` because its prompt
adapter did not inline `related_info/related_work.md`, a citation used only to document offline
status. The regulator classified this as a documentation issue and reported no mathematical
counterexample. The final record preserves both the mathematical `PASS` and system `FAILED`.

## Hidden-gold comparison and new project theorem

The hidden gold at commit `0f9b2b0` already contained strict `MO`, `SPD`, and `ND` results matching
the three main conclusions. All arms were frozen before that content was unsealed.

Arm C strictly advances the hidden gold by proving polynomial graph-core density without assuming
the gold's open complete degree spectrum. At arm-freeze time, no scored arm had proved the degree
spectrum of every domain polynomial: B asserted it without proof, A classified only the named
`Q_n^(s)`, and C proved the graph core but not the all-polynomial spectrum.

After scoring was locked, a separate independent posthoc audit checked the reviewer-supplied
parity-triangular proof and returned `PASS`. This result is excluded from every arm score but is now
a strict project theorem:

```text
{deg p: 0!=p in C[x] intersect D(K_c^(s/2))}
= {0,1} union {N:N>=2 floor(s/2)+2}.
```

The proof is uniform in `c>0`, covers even and odd `s`, and checks the sharp `s=4,5` cases. It
closes the explicit general-r EVIDENCE/PARTIAL gap in the hidden gold.

## Efficiency comparison

| Metric relative to A | B | C |
| --- | ---: | ---: |
| Wall reduction | 60.24% | 5.02% |
| Uncached-input reduction | 99.56% | 31.28% |
| Proxy-cost reduction | 87.94% | 56.34% |

Arm B is the clear efficiency winner, but the retained proof gap matters. Arm C used roughly half
the proxy cost of A and produced a stronger theorem, but its end-to-end verifier failed. Arm A
paid for internal role separation, exact replay, ledgers, convergence checks, and two independent
audits. On this problem, that overhead improved assurance and reproducibility, not the three main
mathematical conclusions, which the blank control also found.

## Implications for the plugin

The v1.7 closure-first changes succeeded at their primary goal on this task: Arm A reached a complete
audited result inside 26 minutes and avoided the multi-window expansion seen in pilot v5. The next
optimization should target adaptive overhead rather than weaken verification:

- Run a fast root-obligation closure check immediately after the first complete proof.
- Stop route expansion when all required obligations are closed and reserve extra routes for an
  explicit robustness or novelty request.
- Make the large ledger and replay package optional after a minimal hash-bound proof and one fresh
  audit have passed.
- Retain at least one independent verifier, because B shows that a correct conclusion can still
  contain a load-bearing support omission.
- Improve theorem-breadth selection: C's graph-core result shows that one targeted structural
  refinement can be more valuable than additional parallel restatements of the root theorem.

These are hypotheses for the next preregistered multi-problem regression, not grounds for another
immediate plugin change from a single sample.

## Protocol qualifications

- One scored run was performed per arm in order A, B, C.
- Solver workspaces excluded the project, repository history, hidden gold, network, and sibling
  outputs.
- The initial C launch was excluded as `INFRA_INVALID` before any model call because QED
  unconditionally checked for a `claude` executable. The permitted replacement used a fresh root
  and a fail-closed shim that was never invoked.
- External audits, the final evaluator, hidden-gold comparison, and degree-spectrum audit are
  excluded from scored resource metrics.
- The cost metric is a normalized API-equivalent proxy, not an actual ChatGPT bill.

## Reproducibility

- Preregistration: `PREREGISTRATION.md`.
- Frozen task SHA256: `359d335803eae43f45120e3ca3995b8f12ec2f98b357e2b10116eafe2d8c6332`.
- Uniform neutral comparison: `FINAL_EVALUATION.md` and `final_evaluation.json`.
- Coordinator audit corrections and immutable-input binding: `AUDIT_ERRATA.md`.
- Arm artifacts: `arms/a-plugin/`, `arms/b-blank/`, and `arms/c-qed/`.
- Posthoc strict degree-spectrum proof: `posthoc-degree-spectrum-audit/`.
- Hidden-gold commit: `0f9b2b0`.
- Blind-start commit: `e9aee2c`.
