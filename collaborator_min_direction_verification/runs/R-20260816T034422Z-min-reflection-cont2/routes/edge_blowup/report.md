RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-E final report

Conditional on the frozen R14/R17 common-angle reduction, this route closes
the two requested nonzero-`t` `y`-high edges and the entire `t->1` boundary
collar.

The exact stable identity

```text
rB=(T^2-s^2)/[XT(1+s^2)+ps(1+T^2)]
```

implies `rB<T/X` and `rB<1/(ps)`.  It makes the edges
`(k,y)->(0,1)` and `(1,1)` retained-empty, uniformly for positive `t`
away from zero.  It also shows that every `t->1` limit is retained-empty
except the compensating vertex `(k,t,y)->(0,1,0)`.

At that vertex put

```text
h=pi/2-Aplus,   k^2=kappa h,   a/b=1-alpha h,
R=4/pi-alpha-(pi^2/2)kappa.
```

The retained conditions compactify to `kappa,alpha,R>=0`.  With
`rho_i=Pplus Nhat_i/(g Knew cp^4)`, exact algebra gives

```text
rho_1/h^2 -> R(R+pi^2 kappa),
rho_2/h^2 -> (2R/3)(2R+3pi^2 kappa),
rho_3/h^2 -> R(R+3pi^2 kappa),
rho_4/h^2 -> 4pi^2 R kappa.
```

All four are nonnegative on the complete retained boundary triangle, while
`g Knew cp^4->1/2`.  Therefore `rho_i->0` uniformly and one common
existential neighborhood has all four `G_i>0`.  This includes all relative
rates at all four `t=1` cube vertices.

The result replaces the old Arb atomic-dependency failures by analytic
compactifications; raw subdivision was not repeated.  It is a complete
coefficient lemma inside R14/R17 but remains non-propagating because that
physical bridge is not canonical.  It is not a certificate for the whole
dyadic high slab and does not prove global reflection symmetry.

```text
route_id: MIN-REFL-C2-E
status: rigorous_partial_result
local_result: complete conditional side-edge and t-up collar proof
propagation_status: non_propagating
first_failing_step: noncanonical R14/R17 physical bridge
formalization_status: not_requested
```

