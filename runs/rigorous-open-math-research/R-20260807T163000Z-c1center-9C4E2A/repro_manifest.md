# Repro manifest - R-20260807T163000Z-c1center-9C4E2A

Scripts and data under reproducibility/ (SHA256 truncated to 16 hex, computed
2026-08-08 with hashlib; additions 2026-08-09 for the R -> 1+ strict push):

## Evidence scripts (new this run)
| file | sha256[:16] | purpose |
|---|---|---|
| s33_e1.py | 6874c6261eb6baa5 | E1-inf constants u, x, gap; generic S(a) table |
| s33_r1base.py | 667252a6977e4b6b | exact R=1 base facts (slope 1/14 at a0) |
| s33_zeros.py | 3752934ccd48fd9f | Phi-1 zero locations vs q + direct cross-check |
| s33_profile.py | 57301e67ed5bcdd3 | clean S3 profile (W, G, Phi, s1, s2) at q=100, 1000 |
| s33_r1plus.py | 6b4bcb23801a30f7 | verified R->1+ sheet: phi(b), phi', h(a0) expansion, b_top (F-016) |
| sym_phi_closedform3.py | 511f1812e7c2bb74 | closed form of phi(b) and phi'(b) by hand antiderivatives (w_k^1 division bug fixed; F-019) |
| verify_phi_closedform2.py | f5a83403e13c626d | closed form vs reference R1_1 (max diff 1.38e-6) and vs s33_r1plus.json |
| verify_sheet_exact.py | 640d0744a2f20197 | sheet a*(b,eps) - a0 - eps phi < 1e-9 at eps=1e-4; phi' closed form vs FD |
| cert_phi_prime.py | 8117ec170874a631 | phi' > 0 on [a0,0.999] via mpmath.iv (200-bit, 4000 cells) + tail bound (0.999,1) |
| tail_bound_phi.py | 4aa33a7a98490b46 | elementary tail bound C_tail >= 9.651926 (independent check) |

Superseded (kept as history): sym_phi_closedform.py, sym_phi_closedform2.py
(first attempts; sym_phi_closedform2.py contained the w_k^1 multiplication
bug, fixed in sym_phi_closedform3.py), verify_phi_closedform.py.

## Data files
| file | sha256[:16] | contents |
|---|---|---|
| s33_e1.json | 5a9e0d3ca6bd5ee9 | u=0.7189759, x=2.0584161, gap=0.2474707, S(a) |
| s33_r1base.json | ee6bb9547f53a48c | R=1 curve facts, slope=1/14 |
| s33_zeros.json | bf481e437775ec34 | z0(q): 4.3, 5.3, 10.5, 20.0 (xi) |
| s33_profile.json | 5e944357a8dd371a | clean branch rows at q=100, 1000 |
| s33_r1plus.json | b50f6bc654b615c8 | phi table, phi' bounds, h(a0) expansion, b_top vs R |
| verify_sheet_exact.json | 7f02c731a065ca55 | verification output: diff table + phi' FD comparison |
| cert_phi_prime.json | feef06fd5310b651 | certification output: worst lower bound 8.896e-6, C_tail >= 9.651926 |
| profile_asym_verify.json | 247015b727fc83a3 | prior fp/profile verification |
| fp_G_data.json | 98f02a24cd949af1 | fp, G(fp), R1a/R1b at 1e4/1e6/1e8 |

## Core library (shared)
| file | sha256[:16] | purpose |
|---|---|---|
| fast_lib.py | 822d276ba6fc8fdf | fast secular/norm/y_at/roots |
| c1trace_lib.py | a4b749fe2a39325d | R1R2, partials, a_fp, branch tracing |
| trace_w.py | b10b618bb6f26a4c | S3 tracer (CAUTION: rows polluted a>1/2; see F-013) |

## Certification machinery (status: not yet achieving bulk coverage)
| file | sha256[:16] | purpose |
|---|---|---|
| cert_lib.py | 7598b4a2dd93090d | mpmath.iv machinery |
| cert_roots.py | d57d6d16b2ae7c49 | sign-based root enclosure (untuned) |
| cert_c1.py | bcd45a7d95cf23e9 | C1 box certification (point tests only) |
| sym_cert_partials.py | e1e14e7bb0eee20c | exact sympy partial expressions |

## Output hashes of key numbers (all float; NOT proofs)
- E1-inf gap: 0.24747068667475103
- u (left) = 0.7189759094079513 ; x (right) = 2.0584160769100017
- xi* = 0.11993721593744928 ; alpha*2 = 16.67539124005561 ; kappa* = 0.3694653455414447
- R=1 slope at a0: 1/14 = 0.07142857142857142  [REFUTED as the fp-component limit (F-016): the branch is nearly vertical, db/da -> +inf; the curve sin(2 pi b) = -sin(pi a)/2 is a phantom.  Kept only as the slope of that curve.]
- Phi-1 left zero (0.5-z0)q: 4.30, 5.32, 10.47, 20.03 at q = 70.7, 100, 316, 1000
- S(a0) = -0.384329 (leading order); measured q(Phi(a0)-1) = -0.374 (q=1000)

## Reproduce
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe s33_e1.py
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe s33_r1base.py
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe s33_zeros.py
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe s33_profile.py
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe s33_r1plus.py
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe sym_phi_closedform3.py
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe verify_phi_closedform2.py
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe verify_sheet_exact.py
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe cert_phi_prime.py
(Python 3.10 with numpy/scipy.  ASCII output.)
