# Research ledger

- 2026-08-24: Read frozen task. Problem: exponential mixing by a bounded shear?
- Observation: since u depends only on y, the solution is theta(x,y,t)=theta_0(x-U(y,t),y).
- Fourier mode in x decouples: theta^k(y,t)=exp(-ik U(y,t)) F_k(y).
- k=0 modes are time invariant; a nonzero x-average per y gives constant H^{-1} lower bound.
- Main route: negative proof via BV lower bound. The phase U has derivative L^1 norm <= C t,
  so the multiplied y-profile is in W^{1,1} with variation growing at most linearly.
- Lemma: for any W^{1,1} g on T, H^{-1}_y(g) >= c(L) / (1+Var(g)^2).
- This yields ||theta||_{H^{-1}} >= c/(1+t^2) for a nonzero x-mode, ruling out exponential decay.
- No numerical falsification needed; route is analytic.
