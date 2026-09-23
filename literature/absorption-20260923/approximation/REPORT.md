# L07-L09 / bounded P2-P4 author report

Status: **AUTHOR SUBMISSION, PENDING FRESH INDEPENDENT REVIEW**. No accepted-knowledge release, final-verifier verdict, Lean identity, commit or remote write is claimed.

All outputs are under `/mnt/f/tools/sl-literature-absorption-20260923/author-approximation`. Current project input HEAD was `902d2a931a76dae5fe1ef6d7dacdcfa230897f9c`. Both supplied attachments and the project AGENTS were read. Installed workflow/research/manage 2.0.1 guided the work; the unmodified capture-source API recorded all three full texts in the private workspace. No project-local program or canonical gateway was executed. Project sources, plugins, old evidence and other authors' outputs were not edited.

## Result status and exact scope

| Result | Status | Concrete content |
|---|---|---|
| L07 | PRIMARY STATEMENT CHECKED | Legal author full text obtained; distinct real exponent range, integrability, unweighted norm and lower-density hypothesis checked. The weighted project map is derived explicitly. |
| L08 | BOUNDED ORIGINAL FORMULAS CHECKED | Dirichlet/clamped constructions, derivative and mass sparsity and source regularity hypotheses checked. Generic Robin (4.1) needs its boundary term rederived. |
| L09 | THRESHOLD AND FINITE PROOF CHECKED | Original (5.2) keeps Gram singular values/eigenvalues strictly greater than epsilon; Theorem5.3 has sqrt(epsilon), not epsilon, penalty. |
| P2 / T1-T4 | AUTHOR-PROVED, REVIEW PENDING | General finite synthesis TSVD theorem, dependent columns allowed; synthesis versus Gram cutoffs, coefficient estimate and moment noise separated. Conditional true-domain transfer at s=2 or4. |
| P2 / L1-L4 | AUTHOR-PROVED, REVIEW PENDING | Boundary-compatible integrated Legendre systems: 3-term high modes plus 2 affine lifts for s=2; 5-term high modes plus 4 explicit lifts for s=4. Exact polynomial span, graph-Gram band and positive uniform-in-degree Riesz bounds at fixed c>0. |
| P4 / D3 | AUTHOR-PROVED, REVIEW PENDING | Full arithmetic progressions in both parity index sets give exactly the affine central-trace closure, including proper infinite deletions. |
| P4 / D4 | AUTHOR-PROVED USING L07, REVIEW PENDING | Reciprocal-summable retained parity is non-dense; in particular the dyadic example has an actual L2/Hc2 annihilator existence proof. |

The two prescribed examples retain 0 and1: `{4j,4j+1:j>=1}` is dense in Hc2; `{2^(j+1),2^(j+1)+1:j>=1}` is not. These are selected-generator sets, not asserted actual membership sets of closed spaces. Existing full-family density `0<=s<7/2` and the s=2 cofinite classification remain established inputs. There is no claim that these author adaptations are new to all literature.

## What remains conditional or unresolved

The general retained difference-family criterion for divergent nonarithmetic sets is not settled. D10 specifies the all-polynomial bound needed to realize a formal moment sequence by an actual L2 vector. The next task is a chosen divergent nonarithmetic index set with a Sobolev-density proof or an annihilator satisfying that bound. The exact dyadic closure is not described.

The constructed Legendre systems have analytic uniform-in-N stability constants, so there is no missing such premise for those systems. Uniformity in c->0, other s, modified constraints, quadrature/Gram perturbations and arbitrarily large-degree floating-point stability are not proved. Smoothness alone is not converted into exponential convergence; L4 uses a quantified derivative-coefficient condition. The original nonaffine named p_n remain inadmissible at s=4.

## Actual reading, not just capture

- L07: PDF p3 Theorem1.3 and norm/lower-density definitions; p4 Theorem2.2; targeted statements on pp10-11; pp14-15 sufficiency proof text; final Theorem3.6 proof paragraph on p20. Original page3 inspected. The remaining auxiliary/quasi-Banach chain was not fully audited.
- L08: PDF pp3-4 / printed1491-1492, (2.1)-(2.8), Lemma2.1; pp7-8 /1495-1496, (3.1)-(3.7), Lemma3.1; §4.1 on pp11-12 /1499-1500; coefficient/quadrature limitation passages pp12-13. Original pages4,7,8,11,12 inspected. Multidimensional solvers and benchmark tables were not audited.
- L09: arXiv v4 p10 definitions; §5.2 pp18-19; Theorem5.3 and proof p20; first coefficient-bound argument pp20-21; Theorem5.5 and proof p22. Original pages10,19,20 inspected. This is not a whole-paper verification.

The author PDFs are primary institutional sources: [L07](https://people.tamu.edu/~terdelyi/papers-online/bill.pdf), [L08](https://www.math.purdue.edu/~shen7/pub/LegendreG.pdf); L09 is [arXiv v4](https://arxiv.org/pdf/1612.04464v4). Publisher direct fetches returned a challenge/403 and are preserved as such, not mislabelled full texts. A browser-extracted L07 preview corrupted the analytic-closure comparison; the original PDF correctly has a convergent sum. This is an extraction anomaly, not an established publisher erratum.

## Actual execution evidence

`python3 -B private/checks/check_author_results.py` completed with `PASS_AUTHOR_CHECKS_ONLY`: 250/250 checks, elapsed 2.995s. The exact timestamped record is `private/checks/execution-20260923T071045038414Z.json`, SHA256 `b9bf731a7aedf012d8ff8754f9cfb049cb5681c22b2584dd5e39d567fcf45a40`. The console log is `private/checks/checks-run-01.log`; script identity is embedded in the record.

Checks cover exact endpoint jets, Legendre support and operator-image band for r=2,4 through n=14; selected exact span dimensions through degree16; moment rows and complex moments m=2,...,11; the power-weight norm factor; arithmetic antiderivatives; complex rank-deficient TSVD and a deliberately wrong epsilon-penalty negative control. Numerical Gram spectra used c=1/4,1,3 and degrees12,24,48. These are finite author checks. The all-degree span, analytic Riesz inequalities and closure arguments are in the written proofs, not inferred from those samples. No Lean was run. No independent reviewer was created or consulted by this author.

The separately saved package validator initially failed because a loop variable shadowed the Python Path class. The failed version is preserved as `private/validate_delivery.v1.failed.py`, and the actual failure replay as `private/delivery-validator-failure-replay.log`. The corrected wrapper's latest run is `private/delivery-validation.json`. This packaging failure did not alter the mathematical check record or any project source.

## Handoff paths and hashes

Public/proposed files:

| Relative path | SHA256 |
|---|---|
| `notes/01_primary_sources.md` | `73b2658d31fcd57c90f2d878fc2410322848f81b6597f937c34961eed57eabb8` |
| `notes/02_finite_tsvd.md` | `0ef305e28720f16f5961620af2aa180c6c8fb5ccfb6f396d6ae4a83d68e2ada1` |
| `notes/03_legendre_krein_construction.md` | `9bb12829ca36fbbb28b10d0d3b23f656a06dba762755847da0c82098bbc07dab` |
| `notes/04_infinite_deletions.md` | `8dd35ebe86e67eb301716869b7d312b87667ba927bd287b1ffc153e872d60fe0` |
| `tool-cards/01-finite-tsvd.json` | `72897fb85bacbfe8523425d90e6a2eaa3f8024b63cb3d72d4deac6c3a927ba2d` |
| `tool-cards/02-krein-integrated-legendre.json` | `95cd23d8c29d61d71e1b01e8717dd7100671a8a98b600b7e16b0bda4a3e02f2a` |
| `tool-cards/03-full-muntz-moment-interface.json` | `72005ae3f05f8990f2341f8a75c2b04cbb85553c55514114efe43c35046d8154` |
| `tool-cards/04-infinite-deletion-subclasses.json` | `b297392c60a00a5f5e3327d1f46a1aa430be426f24a4e988e147ed6f36dc53de` |
| `source-manifest.json` | `9655cd07a272116ece6660d6122672fa353f105c39e3a8d2a7241cd969d2e9df` |

Private primary originals (do not publish their contents):

| Source | Relative path | SHA256 |
|---|---|---|
| L07 | `private/raw/L07-author.pdf` | `923025280f4f1c018ea0330f4f70739cd3dec8d68816cbfe5f178882e2ac19f4` |
| L08 | `private/raw/L08-author.pdf` | `b4681fc1c9aa1cc86f3e589ddb2ecadfd9d3965f22f62017ab752ff3383e0c9f` |
| L09 | `private/raw/L09-arxiv-v4.pdf` | `7216e8f13713562927b7a6fd1fcd318697614656acecfb1410e3d41dff767b9e` |

`source-manifest.json` binds raw/text bytes, retrieval dates/statuses, exact reading locators, inspected pages, private 2.0.1 capture records and frozen project inputs. `private/input-manifest.json` records the original read snapshot; current read-source drift, if any, is reported in the source manifest without modifying anyone's work. Four proposed card JSONs include all requested title/summary/conditions/scope/evidence_status/content/sources fields and point to exact proof/source hashes.

Paths changed concurrently relative to the frozen input at handoff: `/mnt/f/LaTeX/BVE research/AGENTS.md`. The frozen mathematical proof inputs matched when this manifest was built. No attempt was made to restore or overwrite concurrent work. Package file/schema/hash validation is recorded separately in `private/delivery-validation.json`; it is not a mathematical review.

Fresh isolated review should check T1-T4's adjoint/cutoff/noise conventions; L2/L3 endpoint lifts and uniform lower bounds; D3's central cutoff and C1-to-H2 approximation; and D4's deduplicated integrability/summability plus inverse-isometry annihilator. The proposed cards must remain candidates until that review and coordinator-controlled integration. Full downloaded texts and extraction caches must remain private.
