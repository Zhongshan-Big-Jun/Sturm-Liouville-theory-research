# Internal adversarial audit (self-audit; no subagents permitted)

Verdict: PASS (internal; not a fresh independent audit)

Checks:
- Fourier normalization: constants only, no change to exponential vs polynomial.
- k=0 mode: if nonzero, gives constant H^{-1} contribution; hence impossible.
- If no nonzero k=0 mode but theta_0 nonzero, some k != 0 has F_k nonzero.
- g_{k,t} is W^{1,1}; derivative L^1 is bounded by |k| ||F_k||_infty ||U'||_1 + ||F_k'||_1 <= O(t).
- Tail Fourier estimate for W^{1,1}: |hat g(l)| <= Var(g)/(2pi |l|), valid by integration by parts.
- Low-frequency projection lemma gives a polynomial lower bound c/(1+t^2) on a single mode.
- Full H^{-1} norm dominates that single-mode contribution.
- Exponential decay would contradict the polynomial lower bound.

Residual risk:
- This is a self-audit, not an independent fresh-context audit (subagents forbidden by task).
- Exact constants are not optimized; the proof only needs polynomial lower bound.
