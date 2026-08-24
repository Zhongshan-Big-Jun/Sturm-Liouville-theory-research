# Danus actual OOD result (assembled from verified fact graph)

Status: verifier-gated fact graph, project `ood-mixing` (codex branch, DeepSeek backend).

## Target theorem

Fact `c07f7dd7c0797a95`: for every nonzero smooth mean-zero `theta_0` on `T^2` and every admissible shear `u` with `sup_t int_T |partial_y u| <= C < infinity`, there do not exist `C1,C2 > 0` such that `||theta(t)||_{dot H^{-1}} <= C1 e^{-C2 t}` for all `t`. In fact `liminf_{t->inf} t^2 ||theta(t)||_{dot H^{-1}} > 0`.

## Verified supporting facts

- `3d7f0d2ce21b5674`: W^{1,1} Fourier tail lemma (integration by parts, `sum_{|l|>N} |hat f(l)|^2 <= ||f'||_1^2 / N`).
- `7cfea2969a9b3b57`: W^{1,1}-phase uncertainty lemma giving `sum_m |fhat(m)|^2/(k0^2+m^2) >= B^2/(4 pi (k0^2+4)(1+A^2/B^2)^2)`.
- `c07f7dd7c0797a95`: full no-go theorem, verified with predecessor dependency `7cfea2969a9b3b57`.

The proofs of all three facts are stored in the Danus fact graph at:
`F:\tools\danus-clone\Danus\runtime\projects\ood-mixing\fact_graph\facts\`.
