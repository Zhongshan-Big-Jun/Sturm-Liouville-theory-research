# L10 / L11 / bounded P3 author delivery

Date: 2026-09-23. Role: literature/adaptation AUTHOR. Independent acceptance: **pending coordinator-supplied fresh reviewer**. No subdelegation was performed.

Write root: `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces`.
Read project: `/mnt/f/LaTeX/BVE research`, HEAD observed `902d2a931a76dae5fe1ef6d7dacdcfa230897f9c`.

## Result and mathematical boundary

Delivered two original source-to-claim notes, three proposed tool-card JSONs, a finite-interface proof, exact calibration derivations, executable author checks, private original sources and a response/coverage/hash manifest. These are proposals for review, not library releases or canonical accepted knowledge.

The main author result is Theorem P: for finitely many fixed positive block values and a C2 path of distinct interior interfaces, a fixed simple normalized eigenvalue has

`lambda''=2lambda A²-2lambda² E-lambda B`,

where `A=<mu,u²>`, `B=<eta,u²>`, `E=double integral u Gtilde u dmu dmu`,

`mu=-sum s_i d_i delta_i`,

`eta=sum s_i d_i² delta'_i-sum s_i e_i delta_i`.

The proof establishes the local eigenvalue branch and first H0^1/uniform eigenfunction derivative by finite transfer matrices before using any distributional notation. The normalized derivative includes `-A u/2`; the Green finite part uses the weighted gauge. For the gap, the extra term is `-sum s_i[d_i² f'(a_i)+e_i f(a_i)]`, and **every term is halved for Q=D''/2**. Fixed-density Hessians, geometric interface terms, coordinate acceleration, mass constraints, gap tangency and box feasibility remain separate.

This author theorem is limited to its stated finite family. General coefficient/distribution paths have an explicit conditional analytic contract. A general L10 application remains unproved: the natural unitary fixed-block pullback changes the principal coefficient to `1/(c_j ell_j(t)²)`, so it is not automatically an extension path of one fixed symmetric operator. The paper's bounded-additive remark does not close this gap.

L11 accommodates positive weight atoms. Its delta-prime interactions are encoded by a different coefficient-measure atom, not by a Radon weight equal to delta-prime. Weak-star concentration, bounded signed total variation and convergent signed masses control a fixed continuous-kernel quadratic form. They do not alone justify changing-kernel limits or interchanging shape differentiation and concentration.

**G1', global Hessian sign/inertia, global uniqueness and interface collisions remain open.** No claim of global novelty or whole-project certification is made.

## Exact reading and access coverage

| Source | Acquired | Actually read | Original formulas inspected |
| --- | --- | --- | --- |
| L10 arXiv 2110.07434v1 | Full 18-page primary PDF, HTTP 200 | PDF pp.1-9,12-13,16; p.17 Remark 2.14 continuation only. Theorem 2.9 proof continuation pp.10-11 and Theorem 2.11 proof pp.14-15 were not read. | pp.4,5,13,16 |
| L11 arXiv 1105.3755v2 | Full 61-page primary PDF, HTTP 200 | PDF pp.3-7,9-11,24,27-28,32-33. Other pages extracted only; no full extension-classification or Appendix C audit. | pp.4,5,11,32 |
| L11 author PDF / TeX | HTTP 200, both preserved privately | Capture only, not another whole-source read | None beyond arXiv images |
| Bibliographic metadata | arXiv landing pages, author index entry, publisher-deposited Crossref records | Title/authors/version/journal/volume/pages/dates/DOIs; L10 is the 2022 journal paper, L11 the 2013 paper | Not applicable |

Twelve direct response records preserve requested/final URLs, redirects, real response status, headers, UTC start/finish times, byte counts and raw/text SHA-256. Wiley direct and abstract requests both returned **403**; Springer returned **200 with a browser-challenge page**, not article text. These three responses remain recorded as failed full-text access. The L11 landing comment says 58 pages, whereas both downloaded PDFs contain 61 pages; all locators refer to the retrieved arXiv PDF. No claim that the journal and arXiv formula pagination agree is made.

Metadata and formula locators are in the two notes and `source-manifest.json`. Full source originals, full extracted text, TeX and paper-page renders live only in `private/` and should remain outside public project content.

| Primary full text | Raw SHA-256 | Extracted full-text SHA-256 |
| --- | --- | --- |
| L10-arxiv-pdf | `9bdca92caa8f7d91dd13067034a552fe506f0abd8760c69f95ecf0992117b732` | `6a8d2b9bfa8a93b65ef8455a30115dd44d474d16d5cf424a0a1920a98ef415e4` |
| L11-arxiv-pdf | `9c748bd9ec74523f5bbea9391ea96016bdb7c953982afd0b303e4f15505ac9e5` | `dfd269c714a749ba17e494ffb2b19d0492ca930a8369791dcf126abf26449d09` |

## Analytical calibration and actual execution

For the exact single interface `(c_left,c_right,a)=(1,4,1/2)`, set `theta=acos(1/sqrt(3))`, `w1=2theta`, `w2=2(pi-theta)`. Both first eigenvalues have `lambda_a=2lambda` and

`lambda_aa=6lambda+(3/2)w³ tan(w/2)`.

Direct matrix differentiation and the complete Green/normalization/interface expression agree. The geometric contributions are approximately 19.7277237638 and -236.455795807; omitting them fails. The curved path `a(t)=1/2+(2/5)t-(1/14)t²` tests nonzero coordinate acceleration. Constant-density scaling tests the missing normalization component. A unit base density plus a midpoint mass independently gives physical right derivatives `lambda1''=6pi²`, `lambda2''=0`, hence `Q=-3pi²`. A separate power-series argument proves the bounded layer's transfer-matrix limit to the atomic jump matrix on bounded spectral sets.

Actual command: `/usr/bin/python3 -B scripts/run_checks.py`, cwd this write root. It executed the standalone `check_calibrations.py` with no project imports. Run began 2026-09-23T07:02:50.445125+00:00; subprocess completed with **exit 0, 39/39 author checks PASS**, mpmath 70 digits, Python 3.14.4, mpmath 1.3.0, SymPy 1.14.0. The exact argv, version/platform, timestamps, stdout/stderr and script hashes are retained in `evidence/run-20260923T070250443181Z/`.

The maximum high-precision equality residual was about 4.64e-69. Central-difference errors fell by approximately four on halving step size in both modes. Finite-layer/atom discrepancies at the smallest tested half-width 0.0125 were about 0.01327 and 0.03303, so they are convergence samples, not exact atom equality. No interval-certified spectral computation, all-parameter numerical claim, Lean execution or independent review is asserted.

Author artifact-integrity check: **193 file/hash bindings checked, 3 valid cards, 39 retained numerical checks, zero problems**. This includes the current read source identities and does not claim an untouched byte audit of the entire project. No project patch, project-code execution, library/canonical mutation, commit, push or remote write was issued by this author. The initial working tree already contained unrelated changes; none was incorporated here.

## Review packet and open obligations

Read the two source notes for attribution and the remaining L10/L11 applicability gaps. For the new project claim, review `P3-interface-chain-rule.md`, especially the interface-strip argument for H1 differentiation, the finite-part identities (P8), the material derivative of the interface values, and the restrictions on admissible directions. Cross-check signs and normalization using `calibrations.md` and the executed script/output. Proposed cards cite these exact author bytes and remain marked pending independent review.

The reviewer should not infer a general distributional Hessian from Hbar, treat the one-sided mass path at M=0 as a two-sided positive-measure path, or promote finite samples to G1'. Wider claims would need new analytic hypotheses and review. This packet deliberately contains no acceptance receipt.

## Exact authored artifact paths and hashes

The table identifies the main reviewable outputs. `FILE-HASHES.sha256` enumerates **every written file except itself**, using absolute paths, including private sources, per-page extraction files, rendered pages, helper scripts, logs, this report and AGENTS. Its own digest is returned to the coordinator separately to avoid a self-hash cycle.

| Exact path | SHA-256 |
| --- | --- |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/notes/L10-source-to-claim.md` | `a6b81d598e0bf3a8717f946a683438e65214473998dc2fe4a4334ec5086950f2` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/notes/L11-source-to-claim.md` | `77e0637e97d48745eae29fdf60053e2d26a840cec8697821ae244fe80fa202e7` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/derivations/P3-interface-chain-rule.md` | `92eba63b76df55ea4280ff78de20b47d1a6941e3daeb69c21be0a9b0a78b77c6` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/derivations/calibrations.md` | `1d568b2149ddf54ece55b5d761a34fe5a93f0e549b7236ec6f52b632173514c9` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/cards/L10-fixed-operator-bridge.json` | `4a6d2c4f494f6cf11c64ce6405e3ff9d981e503d4396ef9ecf58b06adbb453ff` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/cards/L11-measures-and-concentration.json` | `c9725d110862f6cf9519e988a9a512578a11701e84f3af436e50d990d58aa1fd` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/cards/P3-bounded-interface-chain-rule.json` | `b3f7a76670dc4aa09b322b77a03d53bd168bc036018c548b34a7e9d83d828113` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/source-manifest.json` | `ab9007249aef77a4facbb9a83b83a63d94a93b1ea22e929faf52d3ea2437a2d8` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/scripts/check_calibrations.py` | `8c51b2d5f718b7382eeab0f9a8ca9e95eeaebd1e2ac3eac5c9155e9ca634806c` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/scripts/run_checks.py` | `acd54253ddf64abbf6e588d0337443d2f7d13f2f9036f4d2a835011ec8952119` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/evidence/run-20260923T070250443181Z/execution.json` | `c3c97fdd01adfb81cc4b2774972d64ca4288374817f40ee15bc77d4b93469ac1` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/evidence/run-20260923T070250443181Z/stdout.json` | `df1b01c80717ebc569cf70d7ff190ce7ff7fdd0d274440fe87dff86966adee58` |
| `/mnt/f/tools/sl-literature-absorption-20260923/author-interfaces/evidence/artifact-integrity.json` | `e102df4e9c6bbb040638373a2b854d24dc04d4202f010690b95d447824d82731` |

Current project/input paths, bytes, hashes and actual read ranges are recorded under `local_read_sources` in `source-manifest.json`. The three candidate cards have the required title/summary/conditions/scope/evidence_status/content/sources fields. Acceptance and integration are the coordinator's later responsibilities.
