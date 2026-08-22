# Approach Registry

| Route ID | Route | State | Exact gap / outcome |
| --- | --- | --- | --- |
| R1 | Weighted-shift family H_{beta,lambda}: find a Hilbert-space interpolation between H_beta and H_lambda and repeat the run/moment criterion with an explicit realizability lemma | PARTIAL-SUCCEEDED (STRICT for this family) | The realizability threshold for infinite runs remains beta > 3/2; finite runs always realizable; general non-diagonal H remains open |
| R2 | Pure abstract O1' restatement via moment representability | PARTIAL | Already known from R-20260816T000000Z; no new closure |
| R3 | General banded H with non-shift moment map | BLOCKED | Need an explicit range characterization of a general banded moment map; not attempted in this run |
| R4 | Infinite-band/weighted-l^2 arbitrary representer | NOT STARTED | Requires a new infinite moment-problem technique |

## Route decisions

- R1 was selected because it is the smallest step that both uses the existing
  run/free-base machinery and visibly goes beyond bandwidth 1 in a
  non-diagonal direction.  In the end the criterion is actually proved on a
  bandwidth-1 weighted family, but it unifies and extends both prior closed
  families.
- R2 was not pursued as a standalone proof; it is the known remaining core.
