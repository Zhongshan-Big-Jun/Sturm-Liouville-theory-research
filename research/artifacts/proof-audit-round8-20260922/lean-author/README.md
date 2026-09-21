# Round 8 local Lean AUTHOR package

This directory is author work. It supplies new machine-checked local mathematics and a replay procedure; it does not supply an independent verifier verdict. A new verifier should copy the frozen inputs, compile in a new output directory, inspect the actual exported declarations and definitions, and independently assess the mathematical correspondence.

## Mathematical scope

`AuditRound8.lean` is a new standalone file with six direct imports. It imports no prior-round theorem or project proof. `local_root` materializes nine conjuncts; `positive-contract.json` spells out the complete intended type, all real/rational domains, and every conditional premise. No `True` placeholder, `sorry`, custom axiom, or assumption of the desired coefficient occurs.

The core definitions, to be compared with the actual Lean readback in each replay's `declarations.json`, are:

| Definition | Meaning |
| --- | --- |
| `phase lambda2` | `(1/1600) * sqrt(1600 * lambda2)`, the phase at exactly R=1600 and u=1/1600. |
| `ell u` | `1/2-u`. |
| `mubar1 u`, `mubar2 a u` | `pi^2/(4*u^2)` and `a^2/u^2`. These are explicit real functions, not undefined eigenvalue symbols. |
| `I2 a u` | `u/2-u*sin(2*a)/(4*a)`, the actual trigonometric expression in the supplement. No integration operator is formalized. |
| `S a u` | `2*mubar1 u/u-mubar2 a u*sin(a)^2/I2 a u`. |
| `C a b u` | `pi^2*b/(2*u^2)-2*a^4*b^3/(3*u^2*(1+b+b^2*a^2))`. This expression is **defined**, not assumed equal to the target stationary coefficient. Identifying it as the spectral expansion coefficient requires the separate analytic argument. |
| `scalarRatio` | An exact rational expression using 0.337, 9, 1.00046, 333/106, 1.56 and 0.99996. Lean's rational literals and arithmetic are exact. |
| `wCritical R` | `1/(2*(1+1/sqrt R))`. |
| `wCap R`, `capGap R w` | `(1/2)/sqrt(1+25/(pi^2*R))` and `pi^2*R*(1/(4*w^2)-1)`, using actual `Real.pi`. |

Every division and square root in these definitions is Lean's total real operation. The relevant theorems explicitly restrict parameters so that the intended denominators are nonzero and square roots positive. The proofs establish those facts; they are not silently inferred from names.

## Detailed author mathematical readback

1. `phase_bound`: for every real lambda2 with `0 <= lambda2 <= 4*pi^2`, the phase is nonnegative and at most `pi/20`, strictly below `pi/2`. The upper bound follows from `sqrt(1600*lambda2) <= 80*pi`; the numerical simplification is proved. The premise `lambda2 <= 4*pi^2` is a **spectral-comparison input**. No operator, density or minmax theorem is formalized. The nonnegative premise is retained to express the spectral domain; because real square root is total, the upper-bound inequality alone does not mathematically need it.
2. `root_trig_reduction`: for any real a,b satisfying only `sin a+b*a*cos a=0`, it proves `sin(a)^2=b^2*a^2/(1+b^2*a^2)` and `sin(2*a)=-2*b*a/(1+b^2*a^2)`. The denominator is positive for all real a,b. This uses the actual trigonometric identity `sin^2+cos^2=1` and explicit multiplication of that polynomial relation.
3. `integral_reduction`: for a>0, u>0, b>0 and that root equation, the defined `I2` equals `u*(1+b+b^2*a^2)/(2*(1+b^2*a^2))` and is positive. This is an algebraic/trigonometric identity for the displayed expression; no integral evaluation or eigenfunction normalization theorem is claimed.
4. `S_reduction`: under the same positivity and root premises, it proves `S=pi^2/(2*u^3)-2*a^4*b^2/(u^3*H)`, H=`1+b+b^2*a^2`. Thus the trigonometric-to-algebraic S bridge is part of this formalization. It is **not** left as an assumed desired identity or as an analytic open leaf.
5. `coefficient_identity`: for a>0, 0<u<1/2, `b=ell u/u`, and the root equation, it proves `C=4*mubar1*ell/(3*u)+(ell/3)*S`. Here b>0 and `b*u=ell` are consequences of the stated hypotheses. The denominator factors are shown nonzero. No C-equation is a premise. The theorem deliberately generalizes beyond a in (pi/2,pi): its algebra needs only a>0 and the root relation. Spectral selection of that particular root is separate.
6. `stationary_coefficient`: adding **only** the stationarity condition `S a u=0`, it proves `C=pi^2*ell/(3*u^3)` and `C>0`. The formula is derived from item 5 and the definition of mubar1. The existence/location of u*, and that its analytic stationarity is expressed by this S, are not established here.
7. `scalar_ratio_bound`: `scalarRatio < 8256/10000` over the rationals, by kernel-checked exact arithmetic. For human comparison the fraction simplifies to `893460803/1082206710`, about 0.8255916312, with positive margin `1132097/135275838750`. The final inequality is formal; estimates supplying Cz<0.337, B<=9 and the other scalar input bounds are outside this file.
8. `B_curved_counterexample`: R=3015/2 lies strictly in (1500,1515), w=48743/100000 lies in (0.19,0.5), and `wCritical(1500)<w<wCritical(R)`. The proof uses rational comparisons for sqrt(1500), sqrt(3015/2) against 48743/1257. It proves the missing curved strip point relative to the described rectangle; it does not formalize the historical Python implementation or the whole regional partition.
9. `D_gap_signs` and `D_curved_counterexample`: with the same R and w=4995815/10000000, the exact gap expression is <25 at R and >25 at 1515. Mathlib's actual `3.1415<pi<3.1416` bounds suffice. The proved cap-square formula and positive-denominator comparisons give `wCap(R)<w<wCap(1515)`. R is inside the first cell and 0<w<1/2. This is a curved-coverage counterexample, **not** a spectral example with G<25.

The materialized root includes the phase theorem, I2 and S bridges, coefficient identity, stationary positive formula, scalar comparison, B witness, D gap signs and D witness. Supporting lemmas remain public and are included in actual declaration/axiom extraction.

## Replay and trust boundary

Use an existing WSL environment able to execute the pinned Windows Lean installation and resolve the external paths recorded in `runtime-config.json`. No package download or library build occurs. The small frozen input archive depends on these **installed, hash-bound external artifacts**; it is self-contained in task sources, contracts, controls and replay code, not a bundled Lean/Mathlib distribution.

Copy/extract the final frozen input package into the new verifier's own authorized work directory, then run:

```bash
python3 -B /absolute/path/to/copied-package/replay.py /absolute/path/to/new-verifier-output
```

The output directory must be new. The runner writes only to that output directory and reads the copied package/external installation. Its labels identify machine execution, never independent semantic review. The coordinator/new verifier must determine and record independence separately.

The replay checks frozen inputs, actual Lean version and Mathlib revision, exports the environment's actual loaded-module paths, hashes every imported olean/private/server/IR artifact and runtime binary, compiles a copied **current source** to a fresh olean, typechecks the full positive contract, exports all public declarations and definitions, compares the complete elaborated root type, traverses all type/body dependencies, checks transitive axioms and unsafe/unknown constants, and checks `--deps` resolves the fresh root olean. It then runs three negative controls and rehashes external artifacts and inputs. The final frozen external-environment inventory additionally requires a new replay to match the author's actual pinned installation.

Allowed foundational axioms are the subset of `propext`, `Classical.choice`, `Quot.sound` actually reached. The exporter uses a proved expected-type declaration, not a synthetic custom axiom. Public definitions have pretty and structural expression readbacks; all public theorem types and transitive axiom sets are exported. Proof dependency traversal includes imported theorem bodies and definitions. The compact dependency inventory omits huge proof-expression dumps while retaining every reached declaration's kind, unsafe status and direct type/body edges.

Raw command receipts include run UUID, PID, UTC start/end, argv, cwd, relevant environment, immutable source snapshots, executable hash, complete stdout/stderr and their hashes, exit code and produced-artifact hashes. Each run's receipt manifest binds its raw files. The Windows compiler, standard mathematical foundations and installed compiled Mathlib remain the trust boundary; this is not a second independent kernel implementation.

The genuine wrong-target controls demand the old all-parameter phase branch, change the stationary denominator from 3 to 2, and assert the false rational bound scalarRatio<4/5. Expected failures must be mathematical/type errors, not missing imports or unknown declarations.

## Explicit exclusions and review status

Excluded: full spectral minmax; analytic implicit-function expansions and remainders; derivation of mode identity, spectral root selection and existence/stationarity of u*; evaluation of I2 as an actual integral; full T1/deep-sliver certification and global coverage; global convergence, exchange of infimum and limit, and rates for globally minimizing parameters; the analytic/scalar estimates feeding the rational ratio other than its final comparison. This local package proves no unconditional expansion of G, no full INF theorem, and no reliable replacement of the complete historical interval library.

All readback above is by this author. New verifier execution and independent semantic review are pending. See REPORT.md for actual final run identities/counts/hashes and the preserved-failure inventory after completion.
