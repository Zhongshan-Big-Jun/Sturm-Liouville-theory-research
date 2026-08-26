RIGOROUS_PARTIAL_RESULT

# Fresh validation of `range_translation.md`

## Frozen inputs and scope

- `problem_contract.md`: SHA-256 `98d6ea8d4da0a5f121c36d7c0b2cc895ec81d7b30f6e9b2d079f212825f667f5` (matches the packet).
- `subagents/range_translation.md`: SHA-256 `07f2c63d3a0670fff434b78778c35ddfecc1ffdb41dc8c7c1b3fa70b9890d5e7` (matches the packet).
- `subagents/direct_coupling.md`: SHA-256 `70315032fdc32eb1c171089ebcb9a08eb04dc9cf7e8127cb5cace9f77feee80c` (matches the packet).
- This was a fresh module audit from the files only. No internet, external theorem, or source edit was used. The proposed inequality (MC) was attacked only for counterexamples; finite success below is not treated as a proof.

## Overall verdict

`REPAIRABLE_GAP`.

The substantive proved partial results are correct: (1), (3)--(5), the implication (AVI) => (6), the one-sided bounds (7), the hitting/depth lemmas, and the reflection coupling calculation all survive the audit, with their stated domains and constants. The open estimates (AVI) and (MC) remain explicitly open and therefore do not establish the requested constant-order triple upper bound.

There is one actual false displayed formula: recurrence (13) omits paths whose last step creates a new minimum or maximum. The prose immediately following it describes the right forward-update procedure, and independent exact enumeration reproduces every displayed small-time value, so this is a local, repairable error rather than a failure of the proved estimates. There is also a compressed justification at (8): the formula is correct, but reflection only at `-a-1` gives a killed-half-line probability, not directly the exact-minimum formula; one must subtract the analogous formula for the next half-line.

## Claim-by-claim verdicts

| Location / claim | Verdict | Validation or exact correction |
|---|---|---|
| Lines 15--20, translation of the physical triples | `PASS` | A walk from 2 has physical triple `(2+L_t,2+U_t,2+Z_t)`, so the problem is exactly comparison of a triple law with its translation by 2. |
| Definition (2) and stated support | `PASS` | Translating by `-L_t` gives `0<=A,K<=R`; endpoint parity is `t+K-A` even. These are necessary support conditions, as claimed. |
| Exact identity (3) | `PASS` | For a physical `(l,u,z)`, `(R,K,A)=(u-l,z-l,-l)` is bijective. The zero-start count is `h_t(R,K,A)` and the start-2 count is `h_t(R,K,A+2)`. The TV normalization is therefore exactly `2^{-(t+1)}` times the displayed integer sum, including `t=0`. |
| Aggregate identity (4) | `PASS` | For fixed `A=-L_t`, each path has a unique `(R,K)`, so summation gives the exact count of `-L_t=A`. |
| Path reversal (5) | `PASS` | Time reversal `S_{t-j}-S_t` sends `(R,K,A)` to `(R,A,K)`; sign reversal sends it to `(R,R-K,R-A)`. Their composition gives `h_t(R,K,A)=h_t(R,R-A,R-K)`, exactly as displayed. |
| (AVI) and its implication (6) | `PASS_AS_REDUCTION` | (AVI) is not proved and is not presented as proved. If assumed, (3) gives `4 binom(t,floor(t/2))/2^t`, hence (6). It remains a sufficient open obligation, not a theorem of the artifact. |
| Central-atom bound after (6) | `PASS` | For `c_q=binom(2q,q)/4^q`, the polynomial inequality used in the induction has right-minus-left equal to `q>=0`; hence `c_q<=(3q+1)^(-1/2)`. For `t=2q`, this is at most `t^(-1/2)` (with `q=0` harmless); for `t=2q+1`, the modal atom is `[(2q+1)/(2q+2)]c_q<=c_q<=(2q+1)^(-1/2)`. Thus the final constant 4 in (6) is valid for all `t>=1`. |
| Non-unimodal fiber at `(t,R,K)=(6,4,2)` | `PASS` | On the compatible `A=0,2,4` lattice, exact counts are `[1,0,1]`. The further claim that four monotonicity runs can occur is also reproducible: `(t,R,K)=(48,8,4)` gives counts `[1000894788882,1029170933020,1017584921004,1029170933020,1000894788882]` on `A=0,2,4,6,8`, with successive signs `+,-,+,-`. |
| Reflection formula (8) | `PASS_WITH_LOCAL_REPAIR` | The formula `P(L_t=-a,Z_t=z)=p(z+2a)-p(z+2a+2)` is correct for `a>=0,z>=-a`, with parity encoded by `p`. A fully correct derivation is: `P(L_t>=-a,Z_t=z)=p(z)-p(z+2a+2)` by reflection at `-a-1`, then subtract `P(L_t>=-a+1,Z_t=z)=p(z)-p(z+2a)` (the boundary case `z=-a` also works by symmetry). The text's attribution to only the first reflection is too compressed but does not change the identity. |
| Same-cell start-2 shift following (8) | `PASS` | At physical `(l,z)=(-a,z)`, the relative start-2 variables have depth `a+2` and endpoint `z-2`; their reflection index is `(z-2)+2(a+2)=z+2a+2`. |
| Support and multiplicity identity (9) | `PASS` | With `s=z+2a`, `a>=0` and `z>=-a` are exactly `0<=a<=s`; hence there are precisely `s+1` physical `(l,z)` cells. Parity is unchanged because `s-z=2a`. The start-2-only part is exactly physical minima 1 or 2, of mass `P_0(L_t>=-1)=P_0(T_{-2}>t)<=2p_t^*`. |
| Algebraic identities and unimodality (10) | `PASS` | Both displayed formulas follow from `p(s+2)/p(s)=(t-s)/(t+s+2)`. The ratio is at least 1 exactly when `t>=s^2+4s+2`, so `D_s` is unimodal on its parity lattice. Comparing a maximizer with its predecessor gives `s_*^2<=t+2`; consequently `(s_*+1)^2<=5t` for `t>=2`. |
| Bounds (11)--(12) and one-sided constant 12 | `PASS` | (11) follows from the preceding square bound and `p(s_*)<=p_t^*`. Weighted summation by parts on the two monotone sides gives (12), including plateaus. Since `sum_s D_s=p_t^*`, `I_t<=22p_t^*`; adding the disjoint start-2-only mass gives L1 at most `24p_t^*`, hence TV at most `12p_t^*<=12/sqrt(t)`. The proof covers `t>=2`, and `t=1` follows from TV `<=1`; sign reversal gives the `UZ` version. |
| Proposed mixed comparison (MC) | `OPEN; NO_COUNTEREXAMPLE_FOUND` | Exact integer forward enumeration found no counterexample for every `0<=t<=160`. The comparison was checked as the denominator-free inequality `L1(triple)<=L1(LZ)+L1(UZ)`, so there was no floating-point issue. This finite search neither proves MC nor reduces the stated gap. The smallest observed relative slack in this range was still positive (about `0.2676` of the marginal-L1 sum, at `t=142`). |
| Lemma 1, one-sided hitting tail | `PASS` | Reflection gives the exact parity-sensitive identity `P(T_d>n)=P(-d<=S_n<d)`. The half-open interval has `d` compatible lattice atoms, so the probability is at most `d p_n^*`. The central-atom audit above gives `p_n^*<=n^(-1/2)`. For `d=1`, the interval contains one modal atom, proving the exact survival identity. |
| Lemma 2, depth law and harmonic moment | `PASS` | Gambler's ruin on `[-a,1]` gives `P(A>=a)=1/(a+1)`. On `{tau<=m}`, necessarily `A<=m`, so truncation and the tail-sum formula give `E[(A+1)1_{tau<=m}]<=H_{m+1}` exactly. |
| Lemma 3 and coupling inequality (12) | `PASS` | The adaptive sign rule leaves each coordinate increment conditionally fair, hence preserves both SRW marginals. At meeting, the historical ranges are exactly `[-A,1]` and `[1,2+A]`. Failure to visit either missing endpoint in the common continuation is bounded by the two one-sided hitting tails, giving `1/sqrt(m)+2H_{m+1}/sqrt(N)`. For `m=floor(t/2)`, `m>=t/4`, `N>=t/2`, and `2 sqrt(2)<=4`, yielding the first inequality in (1). |
| Logarithmic upper bound (1) | `PASS` | The coupling inequality gives `(2+4H_{floor(t/2)+1})/sqrt(t)` for every `t>=2`. Since `H_n<=1+log n` and `floor(t/2)+1<=t+1`, this is at most `(6+4log(t+1))/sqrt(t)`. All constants and the threshold `t>=2` are valid. |
| Displayed recurrence (13) | `REPAIRABLE_ERROR` | It is false as written: for example, from `C_0(0,0,0)=1`, the true value is `C_1(-1,0,-1)=1`, while the displayed RHS at `(l,u,z)=(-1,0,-1)` is zero. The exact forward recurrence is: every current `(l,u,z)` of count `c` contributes `c` to `(min(l,z-1),u,z-1)` and to `(l,max(u,z+1),z+1)`. This is also the procedure described in the parenthetical prose. |
| Small exact table, `t=0,...,6` | `PASS` | Independent integer enumeration gives L1 numerators `2,4,8,14,28,50,100`, hence TVs `1,1,1,7/8,7/8,25/32,25/32`, exactly as displayed. The table is therefore unaffected by the erroneous shorthand recurrence. |
| Final audit/status lines 363--371 | `PASS_WITH_CORRECTION` | The status `PARTIAL` and the identification of an open aggregate diagonal-variation bound are calibrated. The audit should add the local correction to (13) and should not call its displayed recurrence exact. |

## Exact remaining gap and failure mechanism

The desired `C/sqrt(t)` triple-TV upper bound is not proved in this module. It would follow from (AVI), from (MC) combined with (7), or from another uniform bound on the diagonal variation in (3), but none is supplied. The proved reflection/synchronization coupling incurs `H_{floor(t/2)+1}` because the pre-meeting depth has tail `1/(a+1)` while the elementary repair cost grows as `(a+1)/sqrt(t)`; averaging produces the harmonic factor. This is a genuine load-bearing open obligation, accurately disclosed by the source.

The only false proved-looking displayed item found by this audit is (13), whose failure mechanism is omission of new-extremum transitions. Replacing it by the exact forward update above repairs the computational description without altering any audited theorem or table.

## Residual risk

- No proof of (AVI) or (MC) was found or assumed.
- The MC check is exhaustive only through `t=160`; it is counterexample evidence, not a general certificate.
- No external literature/status claim was audited or used, consistently with the frozen blind contract.
