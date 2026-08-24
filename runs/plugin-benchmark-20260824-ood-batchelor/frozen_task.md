# Frozen OOD benchmark: Batchelor-scale liminf

Unpolluted hard benchmark problem. Do not inspect repository, git history, prior performance runs, internet sources, or known solution to this exact problem.

Consider the advection-diffusion equation on the two-torus `T^2 = [-pi,pi]^2`:

    d_t rho + U(t,y) d_x rho = D rho.

Assume `0 != rho(0,.) in L^2_{x,y}` is mean-zero and

    ||U||_{L^infty_t L^2_y} < infinity.

Prove that for the weak solution `rho`,

    liminf_{t -> infinity} ||rho(t)||_{dot H^{-1}} / ||rho(t)||_{L^2} > 0.

State every external theorem with hypotheses. A proof may use known literature results only if explicitly stated with exact hypotheses and cited; numerical evidence alone does not constitute a proof.
