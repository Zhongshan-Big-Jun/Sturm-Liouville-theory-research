# Frozen OOD benchmark: exponential mixing by bounded shear?

This is an unpolluted hard benchmark problem. Do not inspect the project repository, git history, prior performance runs, internet sources, or any known solution to this exact problem. You may use scratch computation for falsification, but the final answer must be a rigorous mathematical argument.

Let `T^2 = [-pi, pi]^2` with periodic functions of period `2pi` in each variable. A function `theta(x,y)` with `(x,y) in T^2` is considered periodic.

**Problem.** Can you find a nonzero function `theta_0(x,y) in C^infty(T^2)` with

    int_{T^2} theta_0(x,y) dx dy = 0,

and a time-dependent shear `u(y,t) in L_t^infty(W_y^{1,1}(T))` (equivalently `int_T |partial_y u(y,t)| dy <= C` for some constant `C`), such that the solution of the initial value problem

    theta_t + u(y,t) partial_x theta = 0,
    theta(x,y,0) = theta_0(x,y)

satisfies

    ||theta||_{dot H^{-1}_{x,y}}(t) <= C_1 e^{-C_2 t}

for some constants `C_1` and `C_2`? Here

    ||theta||_{dot H^{-1}_{x,y}}(t)^2 = sum_{|n| > 0, n in Z^2} (1/|n|^2) |hat theta(n,t)|^2,

and `hat theta(n)` denotes the Fourier coefficient of `theta` over `T^2`.

Answer one of the following with a complete proof:
1. Yes: give an explicit construction, verify all hypotheses, and prove the exponential decay.
2. No: prove that for every nonzero smooth mean-zero `theta_0` and every `u` satisfying the stated bound, exponential decay is impossible.

State every external theorem with hypotheses. Do not rely on numerical evidence as proof.
