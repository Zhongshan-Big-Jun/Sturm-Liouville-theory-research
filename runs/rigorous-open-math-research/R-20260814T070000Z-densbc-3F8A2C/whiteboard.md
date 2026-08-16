# Run whiteboard (Planner memory)

- **Run ID:** `R-20260814T070000Z-densbc-3F8A2C`
- **Task packet ID:** `Q-20260814-densbc-3F8A2C`
- **Last updated:** `2026-08-16T08:00:00Z`
- **Note:** This whiteboard was reconstructed retrospectively at manager stage-close
  because the original run was executed during a subagent-provider outage and did not
  leave a whiteboard file. It records only facts present in the run artifacts.

## Current plan

Run is closed with upstream status `RIGOROUS_PARTIAL_RESULT` (STRICT theorems A-H,
two packet conjectures falsified, F-densbc-01 corrected). No active solver plan.

## Route history

- Diagonal/coordinate-constraint analysis `[SUCCEEDED]`: complete diagonal
  classification dense iff beta <= 3/2 AND R has no finite run; candidate_proof.md.
- Constraints-restore-density mechanism `[PARTIAL]`: correct in non-coordinate
  setting, falsified in coordinate/diagonal setting; candidate_proof.md.
- General non-diagonal H / L_j expansions `[BLOCKED]`: open core O1-O3.
- Fresh-agent independent audit `[BLOCKED]`: subagent provider outage; coordinator
  audit with F-densbc-01 correction (recorded in audit_report.md).

## Ideas to return to

- General non-diagonal H exact low-moment-survival criterion (O1).
- General constraint-functional expansion killing free parameters in all beta (O2).
- Fractional left-definite window 3/2 <= s < 2 (O3, inherited).

## Open obligations

- O1: exact criterion for general non-diagonal H under constraints.
- O2: general L_j expansions killing free parameters for all beta.
- O3: fractional window 3/2 <= s < 2.

## Key artifacts

- `runs/.../problem_contract.md` -- normalized contract; sha256 C8AFDAF4CFDC452E...
- `runs/.../candidate_proof.md` -- STRICT theorems A-H and falsifications; sha256 C2B78E77B8F70BD1...
- `runs/.../audit_report.md` -- coordinator audit, F-densbc-01 correction; sha256 14EB2934B90E3A42...
- `runs/.../research_ledger.md` -- run ledger; sha256 5BE3A16D7FA1AD56...
- `runs/.../run-manifest.json` -- manager manifest; sha256 97A76E10AC07292B...
