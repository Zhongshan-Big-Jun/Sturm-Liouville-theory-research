RIGOROUS_PARTIAL_RESULT

The frozen target remains incomplete. The strongest independently audited result is

\[
\frac1{4\sqrt t}\le \|P_t^x-P_t^y\|_{\rm TV}
\le \frac{2\log t+15}{\sqrt t},\qquad t\ge16,
\]

with the lower bound valid for every \(t\ge1\). Both one-sided range/endpoint marginals also satisfy explicit \(12/\sqrt t\) upper bounds.

The first unresolved obligation is an explicit constant bound

\[
\sum_{R,K,A}|h_t(R,K,A)-h_t(R,K,A+2)|
\le C_0\binom{t}{\lfloor t/2\rfloor}.
\]

A fresh adversarial audit returned `PASS` for the stated partial theorem, while explicitly withholding completion of the original \(C/\sqrt t\) upper bound.

Key artifacts:

- [final_report.md](/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-a-plugin-wsl-run2/final_report.md)
- [candidate_proof.md](/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-a-plugin-wsl-run2/candidate_proof.md)
- [audit_report.md](/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-a-plugin-wsl-run2/audit_report.md)
- [obligation_graph.md](/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-a-plugin-wsl-run2/obligation_graph.md)
- [repro_manifest.md](/mnt/f/benchmark/PILOT-V5-CODEX-U2-20260825/arm-a-plugin-wsl-run2/repro_manifest.md)

All recorded hashes verified, and the exact finite replay passed through \(t=100\).