INDEPENDENTLY_AUDITED_PROOF

# Result

## Exact theorem proved

For every real \(c>0\), integer \(s\ge4\), and \(n\ge0\), under the
abstract-polynomial reading
\[
Q_n^{(2r)}=L_{\rm poly}^{-r}P_n,\qquad
Q_n^{(2r+1)}=L_{\rm poly}^{-r}R_n,\qquad L=c-D^2,
\]
one has
\[
\boxed{Q_n^{(s)}\in D(K_c^{s/2})\iff n\in\{0,1\}.}
\]
The abstract polynomial completion is not canonically equal, under the identity
on polynomial representatives, to \(D(K_c^{s/2})\), although a natural
boundary-correcting unitary equivalence exists.  The literal full polynomial
span is not even contained in the operator domain, hence is not dense there;
the span of the individually admissible members is only
\(\operatorname{span}\{1,x\}\) and is not dense.

Under the alternative genuine-operator reading
\[
\widetilde Q_n^{(2r)}=K_c^{-r}P_n,\qquad
\widetilde Q_n^{(2r+1)}=K_c^{-r}R_n,
\]
every index \(n\) belongs to the required power domain and the tilded span is
dense.  Those boundary-corrected images are generally not polynomials.  This
two-reading statement is necessary because the frozen phrase "isometries
\(K_c^{-r}\)" otherwise collides with "polynomial system."

Bonus: on the polynomial reading, \(\deg Q_n^{(s)}=n\) for every \(n\), since
\(c-D^2\) is triangular with nonzero diagonal \(c\) on \(\mathbb C[x]\).

## Proof

The Krein form is
\[
a_0(f,f)=\int_{-1}^1|f'|^2-	frac12|f(1)-f(-1)|^2\ge0.
\]
Cauchy--Schwarz is sharp exactly when \(f'\) is constant, so
\(\ker a_0=\ker K_0=\operatorname{span}\{1,x\}\), where
\(K_0=K_c-cI\).  Integration by parts recovers both stated endpoint equations.

Spectral power recursion gives, for every polynomial \(p\),
\[
p\in D(K_c^{s/2})\iff
B(L^jp)=0\quad(0\le j<\lfloor s/2\rfloor),
\]
with the terminal \(H^1=D(K_c^{1/2})\) condition automatic for odd \(s\).

For even \(s\), if \(v=L_{\rm poly}^{-1}P_n\) satisfied the Krein condition,
then \(P_n=K_cv\).  Orthogonality to
\(P_n-cv=-v''\) would give
\[
0=\|K_0v\|^2+c,a_0(v,v),
\]
forcing \(v\) affine and contradicting \(n\ge2\).  For odd \(s\), the same
assumption with \(v=L_{\rm poly}^{-1}R_n\) and form orthogonality gives
\(a_0(R_n,R_n)=0\), again forcing affinity.  Conversely, degrees 0 and 1 are
affine \(c\)-eigenfunctions and lie in every power domain.

Finally, \(L^r\) sends the abstract completion unitarily to \(L^2\) (even) or
the \(H^1\) form space (odd), while \(K_c^r\) does the same for the operator
domain.  Their composition is the boundary-correcting unitary, not the identity:
\(x^2\) already lies in the abstract polynomial space but violates the Krein
condition.  The full detailed proof is in `candidate_proof.md`.

## Verification performed

- Exact contract audit before search.
- Closure-first direct proof and boundary/equality falsification probes.
- Mechanism-distinct even and odd proofs.
- Deterministic symbolic replay; one malformed recurrence check was caught,
  recorded, repaired, and rerun to exit 0.  It is evidence only.
- Independent first-time audit: strict `PASS`, no critical errors or gaps, across
  definition, logic, boundary, and adversarial categories.
- Fresh-context check: first found stale metadata; after exact repairs, returned
  `CONVERGING`, no issues, and `terminal_ready=true`.
- No formal proof assistant was used.

## Remaining gaps / first unresolved obligation

No mathematical or audit obligation remains inside the frozen completion
contract.  The first unperformed verification upgrade is optional proof-
assistant formalization.  Literature/novelty status is `UNKNOWN` because the
user forbade all source and network inspection; it is not a correctness premise.

## Failed and blocked routes

No mathematical route failed or remained blocked.  The first exact-check script
misencoded \(cq-q''\) as \(c-q''\) for \(r>1\); the failure is retained in the
ledger/counterexample log and the accepted replay uses the repaired line.

## Novelty status

`UNKNOWN`.  No novelty, openness, priority, or literature claim is made.

## Human/model/tool contributions

- User: frozen statement, scope, restrictions, and independent-audit gate.
- Coordinator: contract, derivations, synthesis, replay, and integration.
- Independent verifier: hash-bound strict proof-audit PASS.
- Fresh-context verifier: detected and verified repair of terminal metadata.
- SymPy: exact finite falsification checks only; no computation-to-theorem leap.

## Reproducibility manifest

Run from the workspace root:

```bash
cd /mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-a-plugin-v17-run1
sha256sum -c research_artifacts_arm_a/SHA256SUMS
timeout 30s python3 research_artifacts_arm_a/reproducibility/exact_checks.py
python3 -m json.tool research_artifacts_arm_a/agent_returns/SUB-O7-global-audit.json
python3 -m json.tool research_artifacts_arm_a/agent_returns/SUB-CONVERGENCE-recheck.json
```

Expected exact-check terminator: `ALL_EXACT_CHECKS_PASS`, exit status 0.

## Confidence by axis

- Semantic fidelity: high; contract and independent definition audit PASS.
- Mathematical correctness: high; independent audit PASS, not formally verified.
- Completeness: complete for the frozen three-part task under both named readings.
- Novelty: unknown by explicit restriction.
- Reproducibility: high for retained artifacts, hashes, and exact finite checks.
