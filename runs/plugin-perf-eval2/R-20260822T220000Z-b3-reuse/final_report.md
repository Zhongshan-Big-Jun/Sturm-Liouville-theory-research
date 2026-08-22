# Final report

Status label: `RIGOROUS_PARTIAL_RESULT`

Run root: `F:\LaTeX\BVE research\runs\plugin-perf-eval2\R-20260822T220000Z-b3-reuse`

## Summary

This reuse-gate run produced/validated two STRICT mathematical results on the
fixed-n adjacent ratio supremum problem (B3):

1. **Ratio extremizer structure theorem (STRICT).**
   For every R>1 and n>=1, every global maximizer of lambda_{n+1}/lambda_n over
   the measurable box 1<=rho<=R is a bang-bang configuration with exactly 2n
   effective switches and material order [1,R,1,...,1]. The proof uses the
   ratio switch function H=u_n^2-u_{n+1}^2 and a ratio energy invariant
   K_ratio=0 (equivalently E=bE_n-aE_{n+1}=0), which forces
   q0=sqrt(lambda_{n+1}/lambda_n)>1 and q1=-sqrt(lambda_{n+1}/lambda_n)<-1,
   hence exactly 2n zeros of H.

2. **2n-root count theorem (STRICT).**
   For the balanced alternating bang-bang configuration [1,R,1,...,1] with
   w_1/w_2=sqrt(R), the secular function F_n(y) has exactly 2n simple roots in
   (0,pi) for every n>=1 and R>1. This run's proof uses an elliptic-zone phase
   lemma: in the elliptic region the secular equation reduces to
   sin((n+1)phi)+(1/s)sin(nphi)=0, whose phase function is strictly increasing;
   the hyperbolic region has no roots.

After the independent derivation, the run discovered that the baseline run
(runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline) already contains the
same two STRICT results, with a different (Jacobi-matrix) proof for the
2n-root count. Therefore this reuse-gate run confirms the baseline conclusions
rather than adding new mathematical results beyond baseline.

## Exact remaining gaps

- **O1 (global extremality to equal-width alternating family/value).**
  The structural theorem reduces O1 to optimization over all [1,R,1,...,1]
  bang-bang configurations with exactly 2n switches. It does not prove that
  the maximizer has equal widths or that the value is c_n(R).
- **O2 (alternating-family monotonicity/uniqueness).**
  Inside the equal-within-type alternating family, the ratio peaks numerically
  at w_1/w_2=sqrt(R), but no proof is provided.
- **O3** is closed by this run and by the baseline run.

## Numerical evidence (not proof)

- R1 root counts matched for n=1..6, R in {2,4,10,100}; all roots lie in the
  elliptic zones.
- R2 expected q0/q1 match on balanced configurations.
- Self-consistency probes found at least one asymmetric [1,R,1,...,1]
  self-consistent solution for n=2,R=4 with a lower ratio (~2.55) than the
  balanced point (~4.28), showing that self-consistency alone does not force
  equal widths or global maximality.
- Web search found no direct equivalent fixed-n ratio result in the first pass.

## Reuse hit/miss counts

- Pre-scan REUSE hits: 8
- Pre-scan REUSE_MISS entries: 5
- Mid-run REUSE hits (baseline): 2
- Mid-run REUSE_MISS_EXISTING: 1 (baseline not pre-scanned)

## Next actions

1. Attack O2/O1 in the alternating family using the Jacobi-matrix form of
   Q_n and/or the ratio self-consistency system.
2. Determine whether the balanced point is the unique global maximizer among
   all [1,R,1,...,1] configurations, possibly via a comparison/monotonicity
   theorem for the ratio over the 2n-dimensional width simplex.
3. Consider Lean scaffolding for the ratio structure theorem and the
   2n-root-count theorem.
4. Update research_map.md and register the new tool entries if these results
   are accepted into the project knowledge base (note baseline already has
   them).
