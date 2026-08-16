# Computation contract

- Objects: exact identities in the normalized interface variables and
  discovery-only scans of the exact common-angle parameterization.
- Validity predicate: every symbolic residual is identically zero over the
  declared rational-function ring; every claimed sign proof is analytic.
- Domain: `mu>1`, strict phase chamber, physical branch `r in (1,r_B)`.
- Arithmetic: SymPy exact rational algebra for identities; binary64/mpmath
  values, if used, are only scouts and never proof inputs.
- Seed: none.  Enumeration grids, when used, are recorded in source.
- Adversarial checks: `mu->1+`, large `mu`, both phase endpoints, `r->1+`,
  `r->r_B-`, and left/right phase asymmetry.
- Certificate: executable exact checker with a PASS/FAIL JSON record.
- Blind spot: exact algebra does not sign transcendental common-angle
  functions without an explicit analytic inequality.
- Universal proof bridge: ordered inequalities with every denominator and
  boundary sign audited in the route report.

