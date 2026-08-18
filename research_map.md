# Research map: BVE research

Last updated: 2026-08-18T14:45:41.907861Z








> This is a living, human-readable map of everything explored on this problem.
> It is updated continuously at stage boundaries and whenever a new route,
> intermediate result, surprise, or failure appears. Partial progress counts.
> It reads like a survey/paper note, not a machine log.

## 1. Problem and target

- Problem statement (original, complete):
- Target:
- Status summary (best result so far, verified/partial/open):

## 2. Routes and methods tried
| densbc-o1p-audit|independent|REPAIRABLE_GAP-fixed|5 localized issues (conjugation/alpha/N-set/injectivity/r=0) repaired; main theorem sound |
| densbc-o1p|solver|PARTIAL|O1' closed on H_beta + finite polynomial constraints (candidate_proof.md) |

| Route / method | Who (agent/human/ai) | Status | Outcome / evidence |
| --- | --- | --- | --- |
| <route_key> | separately-verified | `PROVED/PARTIAL/BLOCKED/REFUTED` | path + hash |

## 3. Intermediate results and unexpected findings
- O1' decided on diagonal H_beta w/ finite-degree polynomial representers: density <=> ker(T|B_adm)={0}; infinite-run admissibility iff beta>3/2; Example 7 non-coordinate obstruction; coordinate case reproduces Theorem E

- (One bullet per finding; include where it lives in the ledger/tools.)

## 4. Failed attempts and failure reasons
- single zero-column criterion rejected as incomplete (non-coordinate constraints couple free bases)

- (One bullet per failure: what was tried, why it failed, what NOT to repeat.)

## 5. Tools and method library

- Pointer to `tools/` / `knowledge/tools/` (every reusable method registered there).

## 6. Open directions and next-generation plans

- (Current decomposition plans, missing bridges, candidate directions.)

## 7. Avoid list (dead ends)
- do not assume density fails only when a single admissible free-base column A m_b is zero; use ker(T|B_adm)
- do not re-derive upstream Theorems A-H; do not claim general non-diagonal resolution

- (Routes that are confirmed dead; do not re-walk without a materially new mechanism.)

## 8. Human / other-agent contributions
- DensBC O1' (continued from R-20260816T000000Z-densbc-o1): decide free run-base moment realizability + membership in H; focus on diagonal/banded structured subclass

- (Routes, insights, or references supplied by humans or other agents; they are
  treated as leads to verify, not as proven facts. Merged here continuously so
  the agent does not rediscover or re-optimize them too early.)
