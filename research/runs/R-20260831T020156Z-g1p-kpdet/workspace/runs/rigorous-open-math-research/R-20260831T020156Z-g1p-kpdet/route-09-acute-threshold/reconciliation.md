# Sequence 18 acute-threshold reconciliation

## Integrity

- W14 session: `/root/acute_threshold_prover`.
- W15 session: `/root/acute_threshold_falsifier`.
- Valid research-model responses: 2.
- Worker restarts: 0.
- Duplicate dispatches: 0.
- Transcript replays: 0.
- Both workers verified all six bound input hashes before use.

## Immutable returns

- W14 returned `PARTIAL` in `prover_result.md`, SHA-256
  `ef7ad48667026a5eb672c8d4bd48718903fd6dcf2102d9f16b8a6883ece948c2`.
- W15 returned `PARTIAL` in `falsifier_result.md`, SHA-256
  `c961bcba5931957beb2e2e60baed90e9517d2af0d3015efa8605a86e985160a2`.
- W15's bounded searches remain `EVIDENCE` only.

## Candidate mathematical delta

W14 proposes strict monotonicity of the fully constrained intrinsic
compatibility scalar. It excludes the remaining acute branch for `c<=2/3`
and therefore extends complete `PHI-SIGN` and KP-DET to `0<c<=2/3`. It also
proposes the exact scalar mass collapse

```text
D(alpha+theta+m beta)
=k(1-c^2)[alpha sin(A)^2+theta sin(d)^2],
```

reducing the `c>2/3` remainder to one explicit scalar implication at a unique
intrinsic root.

W15 proposes a uniform all-`m` blow-up classification near
`(alpha,beta,theta,c)=(pi,0,pi/2,2/3)`. In that collar, the strong threshold
holds with fixed positive margin, but the normalized mass residual is
strictly negative, so the negative-`G` spectral-band tuples cannot be
complete. Its search found no counterexample elsewhere but is non-exhaustive.

## Reconciliation decision

The two returns are compatible: W14 excludes the strict acute branch up to
`c=2/3`, while W15 classifies the adjacent boundary collar as mass-defective.
Both analytic packages are `UNREVIEWED`.

The only authorized next model response is one fresh independent joint audit
of W14's constrained derivative, endpoint sign, `c<=2/3` exclusion, exact mass
collapse, and W15's uniform compactified collar expansions. No repair or third
solver is authorized before that audit.
