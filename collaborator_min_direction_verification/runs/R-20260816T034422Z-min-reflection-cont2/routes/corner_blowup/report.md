RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-C final report

## Result

Conditional on the frozen R14/R17 common-angle reduction, the two open
`t -> 0` triple corners admit a uniform exact positivity proof.  Combined
with the already frozen non-triple `t=0` analysis, this proves:

> There exists an unspecified `t_*>0` such that, for every exact
> common-angle retained point with `0<t<t_*`, `g<1`, and `rB>1`, all four
> centered R17 gaps `G_i=g Knew cp^4-Pplus Nhat_i` are strictly positive.

No value of `t_*` is claimed, and this result is not a certificate for the
whole dyadic slab `t<=1/64`.

## Exact mechanism

Put

```text
epsilon=1-kb,       u=1/rB.
```

At `k->0`, use `x=z/(k epsilon)`.  The exact physical relation gives
`u->x/(2pi)`, so `rB>1` makes `x` compact.  For the normalized coefficient
ratios

```text
rho_i=Pplus Nhat_i/(g Knew cp^4),
```

the exact boundary limits are

```text
rho_i/(k^2 epsilon) ->
  3pi^2 u(1-u),
  pi^2(1-u)(1+5u),
  3pi^2(1-u)(1+2u),
  6pi^2(1-u^2).
```

At `k->1`, put `d=1-k`, `v=epsilon/d`, and
`x=z/(d epsilon)`.  The retained condition forces `limsup v<=1`, while
`u->4x/pi` again compactifies every physical rate.  The four limits are

```text
rho_i/(d^4 v) ->
  3pi^2(1-v)u(1-u)/32,
  pi^2(1-v)(1-u)(1+5u)/32,
  3pi^2(1-v)(1-u)(1+2u)/32,
  3pi^2(1-v)(1-u^2)/16.
```

All are nonnegative on the complete physical boundary rectangle.  More
strongly, one common exact upper bound satisfies

```text
rho_i <= T=k^2 epsilon Psi_0        at k->0,
rho_i <= T=d^4 v Psi_1              at k->1,
```

with `Psi_0,Psi_1` continuous and bounded on the compact physical charts.
This removes the former non-uniform remainder; no sign-indefinite chart
remains.

## Coverage and limitation

The five earlier finite face certificates cover only boxes in which the
other two coordinates stay in `I=[1/64,63/64]`; they cover no genuine
multi-face intersection.  The two new charts themselves cover only

```text
(k,t,y)=(0,0,1), (1,0,1).
```

The conditional small-`t` collar uses their union with the other frozen
analytic `t=0` strata.  It does not close the non-`t=0` side/high-face
intersections listed in `cover_audit.md`.

The original physical problem also has `1<r<rB`.  R14's Bernstein fiber
coordinate signs the entire contrast interval once a base point is
certified.  The strict fiber is empty at `rB=1`, and the `rB=infinity`
closure is handled by the removable face `u=0`.

Most importantly, R14/R17 remain non-canonical conditional artifacts.  No
canonical physical `n=2` theorem, determinant orientation, or global
reflection symmetry follows until the full physical bridge is independently
re-proved and hash-bound.

## Reproduction

From the project root run

```powershell
& 'E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe' `
  'runs\R-20260816T034422Z-min-reflection-cont2\routes\corner_blowup\exact_replay.py'
```

The replay is exact symbolic algebra over `QQ(pi)`, exits with `PASS`, and
matches `exact_replay_output.json`.  Full derivation, boundary-stratum audit,
logic audit, route ledger, and artifact hashes are frozen beside this report.

## Route status

```text
route_id: MIN-REFL-C2-C
local_result: complete conditional uniform small-t proof
status: rigorous_partial_result
propagation_status: non_propagating
first_failing_step: non-canonical physical R14/R17 bridge
restart_condition: independently re-prove and hash-bind that complete bridge
formalization_status: not_requested
```
