# Exact computation contract

- Objects: rational identities for the two-momentum interface, `Phi`, the
  `g` split, quartic Bernstein coefficients, stable scalings, and Schur/
  continuant sign bridges.
- Predicate: every asserted identity reduces exactly to zero over the
  declared rational-function ring; no sampled sign is promoted.
- Transcendental domain: exact common-angle coordinates
  `k,t,y in (0,1)` with analytic sign proofs for sine/cosine factors.
- Arithmetic: SymPy 1.14 exact symbolic arithmetic.  No random seed.
- Certificate: `exact_checker.py` and captured JSON output.
- The external C2-I coefficient cover is an explicit missing certificate;
  this route neither reruns nor assumes an incomplete cover.
- Proof bridge: `G_i=cp^4 B_i` with `cp>0`, then positivity of every
  Bernstein coefficient of the quartic `D(r)`.

