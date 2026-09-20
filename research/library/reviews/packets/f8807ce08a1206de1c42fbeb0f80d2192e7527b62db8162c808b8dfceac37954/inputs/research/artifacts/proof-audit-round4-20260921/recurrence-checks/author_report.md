CANDIDATE_COMPLETE_PROOF

# Recurrence source repair author handoff

The only repository file written by this author is `docs/SL_third_order_recurrence_theory.tex`. All other author artifacts are in this external scratch directory. No commit, push, PDF build, TeX compilation, Lean claim, canonical/card/navigation/AGENTS write, or historical artifact edit occurred. Existing coordinator and other-author changes were preserved.

## Exact scope and changes

For c>0, epsilon=0 or 1, and exactly the three coefficient functions displayed in the source, the source gives self-contained candidate proofs of:

- Exact factorial reduction d_j=theta_j*d_(j-1), the positive kernel a_j, and all solutions v_j=A+B*j+C*Phi_j.
- Positive finite backward formula with the *raw* normalization z_N=1, z_(N+1)=z_(N+2)=0, nonzero z_0, fixed-index normalized convergence, and unique normalized minimality.
- Both-parity K(c) formulas, positivity of their denominators, their c->0+ limits, the even K(1)=e/4 anchor, and the rigorously controlled leading minimal asymptotic terms.
- All eventual rational adjacent ratios, with no degree bound; a leftmost finite-pole and polynomial-degree obstruction also excludes a rational minimal branch.
- All monic quadratic parameter representations, including every shared linear factor and the A=0 tail with d possibly nonzero. Normalization E0=1, eventual ratios, raw denominator domains and removable rational-function singularities are kept distinct.
- R4-F04: every reference term must be nonzero; corrected intermediate identity; reverse data r0,s1,s2; variation-of-constants includes t1=0, w2=1 and its missing nonzero assumptions and exact Casoratian argument.
- Beta classification and root-1 asymptotics derived from exact theory, without replacing a first-order limit by an assumed full asymptotic expansion.
- Existing 2026-08-22 root-1 proof and its original REPAIRABLE_GAP audit are linked with accurate scope; the all-order diagonal proof is explained, and the new finite-pole proof is independent of that argument.

The false assertion that every homogeneous root-1 solution has rational ratio was withdrawn. The exact even c=1 example z0=1,z1=2,z2=5/2 has delta1=1/2, delta2=0, delta3=-1/480 and B>2 in the general solution, refuting the old degenerate-configuration exclusion within the actual homogeneous root-1 class. No universal box-invariance claim remains. Historical high-order coefficients and the even K numerical table are explicitly unreaudited records, with no asserted error order or inherited precision.

## Additional coordinator alignment issue

Read-only review of `/mnt/f/tools/math-audit-round4-20260921/third-order-card-content.md` found that its six d=0 rows do not exhaust *all* monic quadratic representations of eventual ratios. For sigma=epsilon-1/2, the cancelled tau=-1 tail has the entire family

    (a,b,gamma,d)=(sigma+t, sigma*t, t-1, -t), t arbitrary,

representing `(j+sigma)/(j-1)`. For example, even `(3/2,-1,1,-2)` is valid. The source includes this family and its exhaustive coprimality proof. The card was not edited. The coordinator should align its table before release. Odd E+ is explicitly `(t+3/2,3*t/2,t,0)` in the source.

## Author checks actually executed

Command:

    python3 /mnt/f/tools/math-audit-round4-20260921/recurrence-author/check_recurrence.py

Exit code 0. Versions: Python 3.14.4, SymPy 1.14.0, mpmath 1.3.0. No project-local Python tools were run.

- 66 symbolic identity/representation/degree checks.
- 1600 exact assertions for 50 backward terminal problems: two parities, c in {1/7,1,3,10,100}, N in {2,3,5,10,20}. 550 raw z entries independently compared against direct original-coefficient backward recursion; normalized and second-difference endpoint identities also checked.
- 976 exact reduction/reverse/variation assertions, including arbitrary initial data and both positive reference solutions.
- 157 exact cancellation/zero-domain/negative-control checks. Old incorrect intermediate identity gives 69/224; the old absolute-value branch fails; negative-even beta factors are rejected; d!=0 tails are checked.
- 5 symbolic K denominator/endpoint identities.
- 32 high-precision diagnostics comparing the two closed Phi0 values against positive sums and checking explicit tail bounds. These are not analytic proofs.
- TeX environment, braces, labels, citations, preserved historical inputs and legacy label checks; final count 1413 static assertions. `git diff --check -- docs/SL_third_order_recurrence_theory.tex` returned 0.

There are 2804 exact/symbolic assertions and 32 numerical assertions; do not describe the 1413 static assertions as mathematical tests. Initial full-run stdout reports 4243 assertions including the then-current 1407 static assertions. A final text-only patch added explicit odd E+ parameters and evidence provenance; only static checks were repeated, now 1413, and results.json was rebound to the final source hash. The mathematical checks were not needlessly rerun. Raw stdout remains unchanged and static_final.stdout.txt records the final static pass.

## Coordinator evidence, not executed here

The coordinator reported an independently rewritten active d4 run covering four forms, five rational c values, j=3..40, symbolic all-j candidate identities, Eplus reduction for four c values and both parities through j=119, and finite positive-difference backward N=2000. The coordinator also reported a 23-check behavior harness, 624 original rational-mu backward comparisons and 8 failure-exit controls including python -O, with a fresh software reviewer running at the time of the message. The old full d4 actually exited 0 despite false closed forms/reduction and nan; its output was preserved by the coordinator. These are coordinator-supplied facts, not author-executed verification. Do not combine their counts or review status with this author's results. The source makes that separation explicit.

## Review gate and remaining scope

Author status: candidate complete for the stated recurrence repair, **not independently audited**. A distinct fresh-context mathematical reviewer remains required before release. No spawn-agent tool was exposed in this author's session, and no new user-owned task was created as a substitute.

Recommended reviewer focus: (1) exact input-coefficient fidelity for both epsilons, (2) raw terminal normalization and all lower endpoints, (3) interchange/positivity/tail estimate, (4) rational S!=0 and finite-pole argument, (5) coprime classification including both cancellation loci tau=sigma,-1, (6) nonzero hypotheses and reverse initialization, (7) rational-only rigidity and homogeneous box counterexample. The complete theorem proofs are in the frozen source; exact computations are auxiliary.

Remaining outside scope: arbitrary coefficient families, nonhomogeneous source control, new box-invariance theorems, all-order remainders for historical expansions, historical program reruns, full H3/M3/KP proof chains, and full Lean formalization. Novelty status UNKNOWN; no novelty claim. External primary source checked only for elementary sinh/cosh series: https://dlmf.nist.gov/4.33 equations 4.33.1-2. All recurrence claims are explicitly derived from the displayed coefficients.

## Reproducibility and contributions

Input hashes and baseline commit are in inputs.json; original TeX bytes in before.tex. This author wrote the new source proofs and scratch checks. Attachments suggested the factorial and pole routes; the existing root-1 proof and audit supplied historical provenance. No independent-review credit is claimed for author checks. Final source, script, logs, and review locations are bound in handoff_manifest.json. This file is a report, not a canonical receipt.
