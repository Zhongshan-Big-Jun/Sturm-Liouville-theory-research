INDEPENDENTLY_AUDITED_PROOF

For every \(c>0\), integer \(s\ge4\), and \(n\ge0\), under the abstract-polynomial interpretation,

\[
Q_n^{(s)}\in D(K_c^{s/2})
\quad\Longleftrightarrow\quad
n\in\{0,1\}.
\]

Consequently:

1. The operator domain and abstract polynomial completion are not canonically equal. They are naturally unitarily equivalent via a boundary-correcting map.
2. The literal polynomial span is not contained in \(D(K_c^{s/2})\), so it is not dense there. Its individually admissible members span only \(\{1,x\}\).
3. If \(K_c^{-r}\) instead means the genuine operator inverse, every resulting function belongs to the required domain and their span is dense—but these functions are generally not polynomials.

The proof uses the equality case of the Krein form, exact power-domain recursion, and separate \(L^2\)- and form-orthogonality arguments for even and odd \(s\).

The independent audit returned strict `PASS` with no gaps. The repaired fresh-context check returned `CONVERGING` and `terminal_ready=true`. No frozen-task obligation remains; formalization is the first optional verification upgrade, while novelty remains unknown by the no-search restriction.

Artifacts:

- [Final result](/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-a-plugin-v17-run1/research_artifacts_arm_a/result.md)
- [Complete proof](/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-a-plugin-v17-run1/research_artifacts_arm_a/candidate_proof.md)
- [Independent audit](/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-a-plugin-v17-run1/research_artifacts_arm_a/audit_report.md)
- [Replay instructions](/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-a-plugin-v17-run1/research_artifacts_arm_a/reproducibility/REPLAY.md)
- [SHA256 manifest](/mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-a-plugin-v17-run1/research_artifacts_arm_a/SHA256SUMS)

`SHA256SUMS` hash:

```text
9646f21d574b527214cc6e34330cec7509ddb1d59a94d4dc63e83d6e324614fd
```

All checksum, JSON, and exact symbolic replay checks passed.