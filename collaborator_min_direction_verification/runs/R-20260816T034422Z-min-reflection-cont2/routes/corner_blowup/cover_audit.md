RIGOROUS_PARTIAL_RESULT

# Exact coverage audit for the R14/R17 physical retained domain

## 1. Scope and the fourth coordinate

Everything in this audit is **conditional on the frozen R14/R17
common-angle reduction**.  It is not a statement about the canonical
physical root set.

The exact common-angle base has coordinates

```text
(k,t,y) in (0,1)^3,
```

and the original physical coefficient problem has the additional contrast
coordinate

```text
1<r<rB(k,t,y).
```

Whenever `rB>1`, compactify the contrast fiber by

```text
xi=(r-1)/(rB-1) in (0,1).
```

R14 writes the relevant quartic in the Bernstein basis in `xi`.  Therefore
signing all four nontrivial Bernstein coefficients at one base point signs
the **entire** contrast fiber, including its closure `xi=0,1`.  The base
coverage below should thus be read as its product with the full `xi` fiber.
If `rB=1`, the strict physical fiber is empty.  The limit `rB=infinity` is
the `u=1/rB=0` face handled by the new analytic regularization.

## 2. What the old finite certificates cover

Let

```text
I=[1/64,63/64],   L=[0,1/64],   H=[63/64,1].
```

The frozen R17 inner certificate and the five R35 single-face certificates
cover exactly the following base union (up to shared threshold boundaries):

```text
Omega_finite = I x I x I
  union (L x I x I)       # k down 0
  union (H x I x I)       # k up 1; retained subset certified empty
  union (I x H x I)       # t up 1
  union (I x I x L)       # y down 0
  union (I x I x H).      # y up 1
```

There is no `t down 0` finite box in this union.  More importantly, a
single-face box always keeps the other two coordinates in `I`.  Hence
`Omega_finite` contains **no genuine two-face or three-face collar
intersection**.  In particular it does not cover any `t down 0` edge or
vertex.  This remains true even though the individual one-face checks are
complete on their stated boxes.

## 3. The analytic `t=0` cover, separated from the finite cover

The frozen `t0_asymptotic` artifact supplies the following conditional
boundary pieces:

| `t=0` stratum | Conditional source | Status before this route |
|---|---|---|
| `0<k<1`, negative phase away from `y=1` | positive normalized `z=0` coefficient theorem plus compactness | covered |
| `0<k<1`, `y=1`, all finite `epsilon/z` ratios and the infinite-ratio side | fixed-interior-`k` mixed overlap | covered |
| `k=0`, away from simultaneous `epsilon=0` | declared complement of the two exact restart corners | covered conditionally by the frozen frontier statement |
| `k=1`, retained sequences away from simultaneous `epsilon=0` | declared complement of the two exact restart corners | covered conditionally by the frozen frontier statement |
| `y=0` | retained condition fails on the exact face; its compact complement is inherited from the frozen boundary audit | empty/covered |
| `k=0,t=0,y=1` | low-frequency triple blow-up | **newly covered here** |
| `k=1,t=0,y=1` | high-frequency triple blow-up | **newly covered here** |

The two new charts are therefore neighborhoods only of the two physical
triple-corner points

```text
(k,t,y)=(0,0,1),   (1,0,1),
```

expressed more faithfully by `(k,z,epsilon)=(0,0,0)` and
`(1-k,z,epsilon)=(0,0,0)`.  They do not themselves cover the other
`t=0` strata.  The statement that the whole `t=0` face is closed uses the
**union** of the frozen analytic pieces and these two new charts.

This union yields an existential conditional collar

```text
Omega_t0 = {(k,t,y): 0<t<t_*, 0<k,y<1, g<1, rB>1}
```

for some unspecified `t_*>0`.  It is not the dyadic slab
`t in [0,1/64]`, and it must not be reported as an Arb cover of that slab.

## 4. Boundary-stratum table for the compactified base cube

Here "covered" always means conditional-on-R14/R17.

### Faces

| Face | Coverage |
|---|---|
| `t=0` | fully covered by `Omega_t0` (old analytic pieces plus the two new charts) |
| `k=0` | only its central finite patch `t,y in I`, plus its sufficiently-small-`t` patch from `Omega_t0` |
| `k=1` | same geometry; the central finite patch has empty retained subset |
| `t=1` | only its central finite patch `k,y in I` |
| `y=0` | only its central finite patch `k,t in I`, plus its sufficiently-small-`t` patch |
| `y=1` | only its central finite patch `k,t in I`, plus its sufficiently-small-`t` patch |

### Twelve cube edges

The four edges incident to the `t=0` face are covered by the analytic
collar:

```text
(t=0,k=0), (t=0,k=1), (t=0,y=0), (t=0,y=1).
```

The remaining eight edges are not covered except where one moves back into
the central `I` patch of a single face:

```text
(k=0,t=1), (k=1,t=1),
(k=0,y=0), (k=0,y=1),
(k=1,y=0), (k=1,y=1),
(t=1,y=0), (t=1,y=1).
```

### Eight cube vertices

The four vertices on `t=0` are covered conditionally by `Omega_t0`; the two
vertices with `y=1` are precisely the new blow-up charts.  The four vertices
on `t=1` remain uncovered:

```text
(k,t,y)=(0,1,0),(0,1,1),(1,1,0),(1,1,1).
```

## 5. Exact remaining set after taking the union

The currently justified conditional union is

```text
Omega_current = Omega_finite union Omega_t0.
```

Outside the unknown small-`t` collar, the unresolved base regions are:

1. with `t in I`, all four side-edge boxes where both `k` and `y` lie
   outside `I`;
2. with `t in H`, every intersection where at least one of `k,y` lies
   outside `I`;
3. the portion of the conventional low slab `0<t<1/64` not known to lie
   below the existential `t_*`.

Equivalently, no pairwise-intersection conclusion may be manufactured by
combining five single-face certificates.  The new result removes only the
analytic `t down 0` boundary obstruction; it does not certify the other
side/high-face intersections.

## 6. Propagation warning

Even on `Omega_current`, the result is a coefficient theorem inside frozen
R14/R17.  The following implication is **not** made here:

```text
conditional coefficient coverage
  => every premise-complete physical interface is covered
  => canonical n=2 determinant orientation
  => global reflection symmetry.
```

The full physical/common-angle bridge must first be independently re-proved
and hash-bound.  Until then all coverage in this audit is non-propagating
research memory.
