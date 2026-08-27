RIGOROUS_PARTIAL_RESULT

The stopping-boundary package is complete and hash-verified.

For every integer \(t\ge2\), the proved result is
\[
\frac1{4\sqrt t}
\le \|P_t^{(0,0)}-P_t^{(0,2)}\|_{\mathrm{TV}}
\le
\frac1{\sqrt{\lfloor t/2\rfloor+1}}
+\frac{2H_{\lfloor t/2\rfloor+1}}{\sqrt{\lceil t/2\rceil+1}}.
\]
Thus the upper bound is \(O(\log t/\sqrt t)\). The required fixed \(C/\sqrt t\) upper bound remains open at obligation `O3`; completion is not claimed.

Route A and C matched their reported hashes. Route B returned no artifact and contributed no claim. Exact replay checks passed, including the counterexample slice \((26,16,26)\) and \(t=1\) TV \(=3/4\).

Key artifacts:

- [Final report](/mnt/f/benchmark/PILOT-V5-V17-U2-20260827/arm-a-plugin-v17/final_report.md)
- [Partial proof](/mnt/f/benchmark/PILOT-V5-V17-U2-20260827/arm-a-plugin-v17/candidate_proof.md)
- [Audit report](/mnt/f/benchmark/PILOT-V5-V17-U2-20260827/arm-a-plugin-v17/audit_report.md)
- [Convergence check](/mnt/f/benchmark/PILOT-V5-V17-U2-20260827/arm-a-plugin-v17/convergence_check.md)
- [Artifact hashes](/mnt/f/benchmark/PILOT-V5-V17-U2-20260827/arm-a-plugin-v17/artifact_hashes.sha256), SHA-256 `56161b8b47c303382353992287a6834813bcae5f542a8e809eafb95176f15923`