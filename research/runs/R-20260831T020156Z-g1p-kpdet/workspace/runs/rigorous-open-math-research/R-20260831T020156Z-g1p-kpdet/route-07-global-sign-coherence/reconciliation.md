# Sequence 14 global sign-coherence reconciliation

## Integrity

- W10 session: `/root/global_sign_prover`.
- W11 session: `/root/global_sign_falsifier`.
- Valid research-model responses: 2.
- Worker restarts: 0.
- Duplicate dispatches: 0.
- Transcript replays: 0.
- Both workers verified all five bound input hashes before use.

## Immutable returns

- W10 returned `PARTIAL` in `prover_result.md`, SHA-256
  `8f5c381223b476fcf2b2d6af7f1a51e90086c3146b45a48bdd8362ad126f11aa`.
- W11 returned `PARTIAL` in `falsifier_result.md`, SHA-256
  `18f2e57dfd18784527dac95d07477e89da935fff4065658f2a847af9137e4ba8`.
- The deterministic exact factorization replay emitted three `PASS` lines.
  Numerical searches remain labeled `EVIDENCE` and are not proof.

## Candidate mathematical delta

W10 proposes the exact factorization

```text
G=X [M Dtheta/P] (q-E),
```

with positive prefactor apart from `X<0` and `E>=0`. Thus `G<0` is reduced
to `q>E`. It also proposes an exact `B`-to-`H` identity and the complete-system
chamber exclusion `B<0`. If accepted, a negative-`G` complete tuple must
satisfy the orientation-sensitive remainder

```text
q>E, B<0, and not yet proved: Lalpha<0 and H<0.
```

W11 promotes the old W5 point to an exact one-parameter spectral-band family
with `G<0`, `(A,B,H)` in the strict positive orthant, and an explicit strict
positive mass residual. This is a candidate rigorous no-crossing obstruction
for that family, not a complete-system counterexample.

## Reconciliation decision

The two returns are compatible. W11 gives a regression family in the chamber
predicted by the open sign-coherence mechanism, while W10 reduces the complete
problem to the common-`beta` orientation discarded by squared energy
identities. Neither return closes global `(SC)`, `G>=0`, `PHI-SIGN`, or
`KP-DET`.

Both returns are `UNREVIEWED`. The only authorized next model response is one
fresh independent joint audit of the exact factorization, the `B<0` chamber
exclusion, and the W11 family. No repair or third solver is authorized before
that audit.

