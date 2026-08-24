# Fresh-context convergence check — SUB-CONVERGENCE

## Scope and integrity

This reconstruction used only `agent_packets/SUB-CONVERGENCE.md` and its eight listed inputs. Every listed input matched the SHA-256 recorded in the packet.

## Decision

State: **CONVERGED_EXACT_WITH_STALE_STATUS_METADATA**.

The current package supports the affirmative exact result: for every `n>=1` and `s>1`, `G_{n,s}` has exactly `2n` zeros in `(0,pi)`, all simple. The candidate gives a self-contained uniform derivation, exact count, simplicity argument, and all required boundary audits. `audit_report.md` records an independent `PASS` with empty critical-error and gap lists. Thus the mathematical and contractual state is converged; formal proof-assistant verification was not performed, but the contract does not require it.

## Reconstructed obligation state

| Node | State reported by the current package | Basis in the listed files |
|---|---|---|
| `O1` | closed | exact polynomial reduction and degree in candidate Section 1; graph says PROVED; audit says PASS |
| `O2` | closed | exact scalar location, count, and simplicity in candidate Section 2; graph says PROVED; audit says PASS |
| `O3` | closed | exhaustive quadratic and cosine lifting with derivative checks in candidate Section 3; graph says PROVED; audit says PASS |
| `O4` | closed | separate checks of `n=1`, endpoints, midpoint, and `s=1` in candidate Section 4; graph says PROVED; audit says PASS |
| `O5` | closed | graph, ledger, Route D, and audit report record independent PASS with no errors or gaps |
| `T0` | closed | depends on `O1`–`O5`, all reported closed; graph records PROVED and independently audited |

No mathematical obligation remains open in the current package.

## Inconsistencies and residual qualifications

1. `candidate_proof.md` is a frozen pre-audit snapshot: its header and conclusion say `O5` remains pending, while `obligation_graph.md`, the final ledger entry, and `audit_report.md` say `O5` passed. This is stale status metadata, not a mathematical contradiction in the proof.
2. `approach_registry.md` is internally time-skewed. Route A says “final audit pending” and Route C says the fresh integrated-proof audit remains, whereas Route D in the same file says `PROVED / PASS`; the graph, ledger, and audit agree with Route D.
3. `repro_manifest.md` is consistent with the blind restrictions and accurately disclaims formal verification, but it is a policy/provenance summary rather than a fully executable manifest: it supplies no checker path, command, or checker hash. `audit_report.md` nevertheless labels symbolic checks PASS. This limits reproducibility of the non-load-bearing symbolic checks, not reproducibility of the self-contained proof and not contractual convergence.
4. The independent audit artifact itself is referenced by path and hash but was outside this packet's allowed input list. Accordingly, this check verifies the audit claim as represented consistently in `audit_report.md`, `obligation_graph.md`, `approach_registry.md`, and `research_ledger.md`; it does not re-audit that referenced artifact.

## Next actions

- Synchronize the stale audit-status text in the approach registry with the recorded PASS.
- Preserve the hash-frozen candidate unchanged if audit binding matters; add a clearly identified superseding status note elsewhere rather than mutating the frozen proof.
- If executable symbolic-check reproducibility is desired, extend the manifest with the checker path, exact invocation, tool version, and checker hash. This is optional for the theorem's contract-level closure.
