# Audit Report: `min_direction_progress.tex`

## Verdict

**ACCEPT_WITH_CAVEATS**

The collaborator's progress report is mathematically consistent in all portions
that could be independently verified, honestly labels its trust layers, and
does not overclaim the general problem. It is accepted into the repository as a
research progress document with explicit caveats about external-certificate
dependence and minor documentation gaps.

## Independent adversarial audit

An independent fresh sub-agent reviewed the document and returned
`ACCEPT_WITH_CAVEATS`. Its key findings are summarized below; the full report
is preserved in this run directory's history.

### Findings from independent audit

- **[ERROR / Undefined symbol]** `\kappa_0` (and `\kappa_D`) are used in the
  n>=3, mu=2 contraction section without definitions. `\kappa_D` is inferable
  as the D_a=0 threshold; `\kappa_0` is inferable as the N_b>0 lower bound.
  Should be defined in the source or marked as external-cert quantities.
- **[WARN]** The Bernstein positivity certificate (539 coefficients) and the
  finite Arb covers for the coefficient cube are attributed to an external
  frozen proof package at `E:/ai_auto_solve/...`, which is not available on
  this machine. Those claims are therefore "unverifiable from provided
  materials", not independently verified here.
- **[WARN]** Several `Trusted`-labeled results (n=2, mu=2 local twist/global
  reflection; n>=3, mu=2 non-existence; compact mu=2 strip) chain through the
  external Bernstein certificate. They are trustworthy only if that frozen
  certificate is sound. The document's own scope statement is honest about the
  finite-cert vs global-theorem distinction.
- **[WARN]** The full relay equivalence theorem's reverse implication is
  structurally sound but the complete bijectivity is sketched; flagged as a
  proof-completeness caveat, not a demonstrated error.
- **[INFO]** A cosmetic LaTeX typo at line 247: `\omega(\xi,eta)` should be
  `\omega(\xi,\eta)`.

### Independently verified correct (this audit + sub-agent)

- n=2, mu=2 interface formulas for a,b satisfy the general interface momentum
  equations (symbolic).
- General-mu interface mapping formulas satisfy the momentum equations
  (symbolic/numeric).
- Xi identity in the n=3 shared-contrast section (symbolic).
- Determinant parity sign identity (random matrix tests).
- n>=3, mu=2 contraction algebra: D_a factorization, kappa_N bracket identity,
  kappa_D - kappa_N identity, and 0<a<1 on the physical domain.
- Weak-contrast Phi rearrangement, square-completion, and positive-margin
  inequalities (symbolic/numeric).
- t=0 boundary analytic derivative and rational inequalities (exact).
- n=3 four-margin identity as a formal consequence of the reconstructed matrix
  definitions (10000 random tests; assumes gamma endpoints zero, which the
  source does not state explicitly).
- Path-forest formulas for N=2 and N=3 and the charged-forest reduction.
- Reflection involution identities and the symplectic derivative formula.
- The document compiles with xelatex (43 pages).

## Caveats recorded in repository

- README entry points to this audit run.
- The added `docs/SL_gap_nge2_min_direction_progress.tex` is the collaborator's
  text, kept verbatim. The undefined `\kappa_0`/`\kappa_D` and the external-cert
  dependence are recorded here rather than silently altered.

## Open items after acceptance

- Full Bernstein positivity certificate for Q_box and the finite Arb covers
  remain externally hosted; re-verification requires access to the frozen
  proof package.
- General n>=2 global reflection symmetry remains Open, as the document states.
