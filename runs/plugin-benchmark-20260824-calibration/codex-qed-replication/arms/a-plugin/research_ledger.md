# Research ledger

## 2026-08-24 — initialization

- Accepted the frozen stdin task as the sole authoritative mathematical input.
- Read the rigorous-open-math-research skill and the phase, escalation, delegation, audit, and reporting references required for this run.
- Recorded blind restrictions: no repository/Git inspection, no internet, no outside-directory reads, no prior-solution lookup.
- Froze contract `B3-O3-root-count-v1` and obligations `O1`-`O5`.
- Opened three mechanism-distinct routes: matrix/Chebyshev reduction, trigonometric root bracketing, and adversarial boundary/counterexample attack.
- Tier 0 mental probe suggests `det C_s=1` and its trace may control the power. This is unmerged until exact derivation and audit.

## 2026-08-24 — coordinator algebraic derivation

- Put `r=s^(-1)`, `a=(s+r)/2`, and `z=c^2-aq^2`.
- Exact hand derivation gives `det C_s=1` and `tr C_s=2z`.
- With polynomials `U_{-1}=0`, `U_0=1`, `U_k=2zU_{k-1}-U_{k-2}`, the special `2x2` Cayley-Hamilton identity gives `C_s^n=U_{n-1}(z)C_s-U_{n-2}(z)I`.
- Computing the `(1,2)` entry gives the candidate exact identity
  `G_{n,s}(y)=q[U_n(z)+rU_{n-1}(z)]`.
- Therefore the candidate extension is `Q_{n,s}(x)=P_n((1+a)x^2-a)`, where `P_n(z)=U_n(z)+rU_{n-1}(z)`.
- A uniform exact root route is visible: evaluate `P_n(cos theta)` at `theta=j*pi/n`, including both endpoints, obtain alternating signs, use the intermediate value theorem for `n` disjoint intervals, and close the count and simplicity by exact degree `n`.
- This derivation is now load-bearing and is being subjected to deterministic symbolic checks plus independent subagent comparison.

## 2026-08-24 — symbolic-check harness repair

- First execution of `reproducibility/check_identities.py` stopped at the `EC` entry assertion.
- Failure mechanism was in the checker, not evidence against the identity: the reducer expanded a factor `q(q^2)` into `q^3`, after which a literal `q^2 -> 1-c^2` substitution did not reduce it.
- Replaced that simplifier with exact polynomial remainder modulo `q^2+c^2-1`; rerun pending.
- Second execution passed the low-level identities but hit a harness type error at `n=1` because a native integer `0` has no symbolic `.subs` method. Replaced it with `sympy.Integer(0)`; this is again a tooling defect, not mathematical evidence.

## 2026-08-24 — candidate proof integrated

- The repaired deterministic harness passed determinant, trace, `EC`-entry, and recurrence identities for `n=1,...,6`; this supports error detection only.
- Wrote a uniform exact candidate proof in `candidate_proof.md`.
- Scalar core: `P_n=U_n+rU_{n-1}` has alternating values at `theta=j*pi/n`; the intermediate value theorem gives `n` distinct roots and exact degree `n` forces completeness and simplicity.
- Pullback core: `z=(1+a)x^2-a` with `a>1`, so every scalar root in `(-1,1)` yields exactly two noncritical roots in `(-1,1)`.
- Boundary audit gives the exact midpoint value `G(pi/2)=(-1)^n s^n` and, at `s=1`, the direct identity `G=sin((2n+1)y)`.
- Obligations `O1`-`O4` are candidate-closed. Completion remains withheld pending independent audit `O5`.

## 2026-08-24 — first subagent round merged by evidence

- Verified returned artifact hashes exactly:
  - `SUB-ALG`: `9f9111c5031bf50cebd9962edec93d08398d6985dc0558879d95f711b611c51a`, status `PROVED`.
  - `SUB-OSC`: `9d2dba5b940bce711d8d7a79d581431296b82881ef43a1634b89babf73d95066`, status `PROVED`.
  - `SUB-ADV`: `5504f0debbfb4ada3d4f036f7add9c254bd5f1970f45c0770c611891a28ceeab`, status `NONE_FOUND`.
- Read every artifact in full before merge.
- `SUB-ALG` independently obtained the same scalar polynomial and closed location/simplicity using a different exact sign mesh based on zeros of `U_n`.
- `SUB-OSC` supplied a genuinely distinct self-contained Sturm--Liouville shooting proof: a terminal Prüfer angle increases strictly with the spectral parameter and equals `(2n+1)pi` at `lambda=pi^2`.
- `SUB-ADV` attacked endpoint contamination, quadratic-vertex roots, repeated scalar/lifted roots, and `s=1`; it found no counterexample and provided an independent symmetric-tridiagonal proof of scalar root location and simplicity.
- No subagent status is treated as final certification. The adversarial agent is being reassigned to audit the exact coordinator proof package.

## 2026-08-24 — independent completion audit

- Froze `candidate_proof.md` at sha256 `59b46fa2ee1e2d6a38ad4d386c936405ad96f4861db4509872c6160a0c6791b6` and the contract at sha256 `4e4695334fddcdcc99e1f5f74ecaa3ad9a98ca452a68dd3483d7dbd4d1e1b0d7`.
- A fresh first-time verifier was allowed to read only those two files.
- The returned audit artifact hash was independently recomputed as `4c8831a11edbdcb70c4599ef818e96633c507d2feef58a91659953b000f1c92f`.
- Verdict: `PASS`; critical errors: none; gaps: none; first error: none.
- Covered scope includes contract fidelity, every matrix identity, polynomial extension and exact degree, scalar root count/location/simplicity, exhaustive lifting, derivative simplicity, endpoint conventions, and all five required special audits.
- Obligations `O1`-`O5` and root theorem `T0` are closed. The result qualifies as independently audited but not formally machine-verified.

## 2026-08-24 — fresh-context convergence check and metadata repair

- A fresh agent reconstructed the state from hash-bound files only and reported `CONVERGED_EXACT_WITH_STALE_STATUS_METADATA`; artifact sha256 `412649eec0d07aa5a024e2266481a6e1bbd6778be262fcefc9d15b69ebacf526`.
- It found no open mathematical obligation. It identified stale pending-audit text in Routes A/C and missing executable symbolic-check details in the reproducibility manifest.
- Repaired the registry metadata and added the exact script path, command, Python/SymPy versions, script hash, expected output, and proof-package hashes.
- Preserved `candidate_proof.md` unchanged because its pre-audit hash is the object certified by the independent verifier; superseding completion status lives in the audit, obligation graph, and final report.

## 2026-08-24 — final assembly

- Wrote `final_report.md` with status `INDEPENDENTLY_AUDITED_PROOF`; sha256 `a6c5f4d937d89d27fa10f541d61e7b21c1cecaae6edd62858d483bb5f95063ea`.
- Re-ran `python3 reproducibility/check_identities.py`; expected PASS output reproduced.
- Ran `sha256sum -c reproducibility/proof_package.sha256`; every frozen proof, audit, route, convergence, and checker artifact matched.
- No mathematical obligation remains. No formal proof-assistant or novelty claim is made.
