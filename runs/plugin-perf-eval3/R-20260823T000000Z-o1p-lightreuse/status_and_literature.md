# Status and Literature

Current global status (honest): RIGOROUS_PARTIAL_RESULT.
O1' remains open for general non-diagonal H; this run adds a STRICT exact
criterion for the weighted shift family H_{beta,lambda}.

## Known prior sub-results (reused, not re-derived)

| Result | Source | Status |
| --- | --- | --- |
| Master criterion: density iff V cap Q_sp^perp = {0} | constrained-denseness-runs (Theorem A) | STRICT / audited |
| Diagonal H_beta O1' criterion: dense iff ker(T|B_adm)=0 | R-20260816T210000Z-densbc-o1p | STRICT |
| H_lambda (bandwidth 1) O1' criterion: dense iff ker(T|B_fin)=0 | R-20260816T220000Z-densbc-o1p2 | STRICT |
| Run/rho formula and first-obstruction structure | R-20260816T000000Z-densbc-o1 | STRICT |
| Corrected run ratio rho_b(k)=floor(k/2)/floor(b/2) | F-densbc-01 / R-20260816T000000Z | STRICT |

## Parallel baseline result (R-20260823T000000Z-o1p-baseline)

The baseline run proves a strict finite-rank criterion for the stable
banded-shift Toeplitz family H_shift(m,lambda).  That is a different
non-diagonal family: it varies the shift bandwidth but has no diagonal
weighting.  It is complementary to this run's H_{beta,lambda}.

## New result this run

For beta >= 0, lambda in (-1,1), H_{beta,lambda} = l^2(N_0) with
x^k = (k+1)^beta e_k + lambda e_{k+1}, finite polynomial representers:
O1' is decided by ker(T|_{B_adm}) = {0}, where B_adm includes finite runs and
infinite runs only when beta > 3/2.  This contains both H_beta (lambda=0)
and H_lambda (beta=0).  For beta > 0 the family is not Toeplitz and is not
covered by the baseline H_shift(m,lambda) criterion.

## Literature novelty

The H_{beta,lambda} family is a natural interpolation between the two prior
closed families.  No external paper is known to us that states the O1'
criterion in this exact abstract form.  The resulting theorem should be
treated as project-internal, not as a claim of external novelty until a
literature audit is run.

## Open after this run

- General banded or fully non-diagonal H with non-weighted-shift moment map.
- Arbitrary representers not finite polynomials.
- The abstract moment-representability core of O1'.
