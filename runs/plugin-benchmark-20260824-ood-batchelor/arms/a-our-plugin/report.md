# Report

## Task

Prove, for the advection-diffusion equation

    d_t rho + U(t,y) d_x rho = D rho

on `T^2`, with mean-zero nonzero `rho(0,.) in L^2` and
`||U||_{L^\infty_t L^2_y} < infinity`, that

    liminf_{t -> infinity} ||rho(t)||_{dot H^{-1}} / ||rho(t)||_{L^2} > 0.

## What was done

1. Built a theorem contract (`problem_contract.md`) and identified the major
   ambiguity: `D` is never defined in the task. The proof cannot be completed
   until `D` is specified.
2. Analyzed the two most natural readings: `D = Delta` and `D = d_y^2`.
3. Under `D = Delta`, proved the following strict results:
   - x-mode invariance: the x-Fourier support is fixed because `U` depends
     only on `y`;
   - per-x-mode energy bound: each nonzero x-mode decays at least at rate
     `n^2`;
   - complete proof for the special case `U = 0` (and `U` independent of
     `y`), using the minimal nonzero Fourier mode;
   - complete proof for initial data with finite Fourier support.
4. Explored three main routes to the remaining general result:
   - Fourier localization / Batchelor scale;
   - H^{-1} energy identity and commutator estimates;
   - spectral theory for time-independent bounded shear.
   None produced a complete proof under the stated `L^2_y` regularity.
5. Ran finite spectral simulations as falsification/evidence; they showed the
   ratio staying positive for several test cases. These simulations are
   explicitly labeled `EVIDENCE`, not proof.

## Main outcome

`RIGOROUS_PARTIAL_RESULT`.

The original statement remains open in this run. The obstacle is precise: for
a fixed x-mode `n`, one must prove that the `y`-frequency content of the
solution to

    d_t u = d_y^2 u - n^2 u - i n U(t,y) u

cannot become so large that the `dot H^{-1}/L^2` ratio tends to zero. This is
the per-mode "Batchelor-scale lemma" (CL) stated in `result.md`. Even with
(CL), the full statement also needs a persistence/comparison statement
ensuring that the surviving `L^2` mass does not sit only on arbitrarily large
`|n|`.

## What remains

- Prove the per-mode Core Lemma (CL) for `U in L^\infty_t L^2_y`.
- Prove a persistence/comparison statement for different x-modes, or obtain
  a version of (CL) whose `n`-dependence is sufficient.
- Resolve the `D` ambiguity. If `D` is not the full Laplacian, the reduction
  and the set of available estimates change.
- Either prove the theorem for `D = d_y^2` separately or find the exact
  known theorem/citation for the isotropic case.
- If using an external result, provide an exact statement with hypotheses and
  a verifiable citation.

## Strictness labels used

- `STRICT`: x-mode invariance, per-x-mode energy bound, `U=0` proof,
  finite-support proof.
- `NOT-YET-STRICT`: the partial reduction from the original statement to the
  per-mode lemmas.
- `OPEN` / `NOT-YET-STRICT`: the per-mode Core Lemma and Reading B.
- `EVIDENCE`: numerical simulations (not proof).

## Artifacts

- `task.md` (input).
- `problem_contract.md` (contract and ambiguity analysis).
- `result.md` (main result, strictness labels, remaining gap).
- `report.md` (this summary).
- The scratch numerical scripts were temporary and have been removed; the
  numerical evidence is summarized in `result.md`.
