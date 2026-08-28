# Exact replay instructions

Run from the frozen workspace root:

```bash
cd /mnt/f/benchmark/PILOT-V6-HS-DOMAIN-20260828/arm-a-plugin-v17-run1
sha256sum -c research_artifacts_arm_a/SHA256SUMS
timeout 30s python3 research_artifacts_arm_a/reproducibility/exact_checks.py
python3 -m json.tool research_artifacts_arm_a/agent_returns/SUB-O7-global-audit.json
```

Expected computation terminator and exit status:

```text
ALL_EXACT_CHECKS_PASS
exit status 0
```

The JSON audit verdict and the final report status must agree.  The exact
computation is only a deterministic falsification replay; the general proof is
the human-readable derivation in `candidate_proof.md`, bound to the audit input
hash recorded in `audit_subtask_packet.md` (or to a later revised audit packet if
the first audit requires repair).

No network, repository-history command, or hidden seed is required or permitted.
