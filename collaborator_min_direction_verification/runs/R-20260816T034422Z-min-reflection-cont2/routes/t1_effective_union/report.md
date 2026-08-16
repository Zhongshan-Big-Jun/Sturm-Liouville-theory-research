RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-N final report

The C2-L stable certificate now extends to the complete explicit original-
coordinate collar

```text
t >= 1-2^-17.
```

The exact map is

```text
h=(pi/2)(1-t),
kappa=k^2/h,
beta={ (pi/2)y(1-k)/(1+k)-h }/h^2.
```

Every retained point has `beta<0`.  The stable C2-L rectangle covers
`kappa<=3/8,-3/2<=beta<=0`; exact finite certificates exclude
`beta<-3/2` for `kappa<=4` and exclude `3/8<=kappa<=4`; an analytic
`ps>1` estimate excludes every `kappa>=4`.  These cases are exhaustive.

A single preregistered finite run on the three compact complements produced:

- `LHL`: complete finite coefficient certificate;
- `IHL`: one-million-box cap exhausted with 21 residual boxes;
- `LHH`: atomic interval-dependency failure.

Thus the full `t=1` collar and the complete LHL dyadic cell are now effective.
IHL and LHH remain open compact annuli; no rerun or escalation was performed.

The result remains conditional on R14/R17 and non-propagating.

```text
route_id: MIN-REFL-C2-N
status: rigorous_partial_result
explicit_original_collar: t>=1-2^-17
new_complete_dyadic_cell: LHL
remaining_t_high_annuli: IHL, LHH
physical_bridge_status: noncanonical / not reproved
canonical_status: no propagation
formalization_status: not_requested
```

