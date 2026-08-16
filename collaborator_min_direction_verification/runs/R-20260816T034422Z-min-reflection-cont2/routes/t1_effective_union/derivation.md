RIGOROUS_PARTIAL_RESULT

# MIN-REFL-C2-N: effective union for the complete `t=1` collar

## 1. Exact chart-to-cube map

Let `c=pi/2`.  The R17 cube coordinates satisfy

```text
z=Aplus=ct,
theta=Aminus=c+y[pi/(1+k)-c].
```

Hence the C2-L variables are exactly

```text
h=c(1-t),
kappa=k^2/h,
eta=theta-c=c y(1-k)/(1+k),
beta=(eta-h)/h^2.                                      (1.1)
```

No identification of `h` with `1-t` is made.  Since `pi<4`,

```text
t>=1-2^-17  =>  h=c(1-t)<2^-16.                        (1.2)
```

Thus the rational original-coordinate collar in this route is

```text
Omega_up={1-2^-17 <= t < 1}.                            (1.3)
```

## 2. Every retained point has `beta<0`

Use the exact C2-E variables

```text
u=a/b=pT/(sX),       0<u<1
```

on `g<1`.  The stable formula for `rB` gives

```text
rB <= (s/p)u.
```

Therefore `rB>1` forces `u>p/s`.  Since

```text
u=(p/s) tan(h)/tan(eta),
```

strict monotonicity of `tan` yields `eta<h`, hence `beta<0`.  The face
`eta=0` is already nonretained (`b=0<a`).

## 3. Exhaustive escape classification

### 3.1 Stable rectangle

If

```text
0<=kappa<=3/8,       -3/2<=beta<=0,                    (3.1)
```

C2-L proves `rho_i<1` for all four coefficients.

### 3.2 Escape `beta<-3/2` with `kappa<=4`

For fixed `h,k`, the negative endpoint quantity

```text
b=tan(k theta)tan(eta)/k
```

is strictly increasing in `eta`, hence in `beta`.  A 256-cell exact Arb
cover at the boundary `beta=-3/2`, over `0<=kappa<=4`, proves

```text
alpha=(1-a/b)/h < 0,
max directed upper <= -0.2264618456.                    (3.2)
```

Thus `a>b` at the boundary and throughout `beta<-3/2`; `g<1` fails.

### 3.3 Escape `3/8<=kappa<=4`, `-3/2<=beta<=0`

A fixed tensor cover of 22,272 exact dyadic boxes proves

```text
S=(rB-1)/h < 0,
max directed upper <= -0.3503997959.                    (3.3)
```

Hence the strict contrast fiber is empty.

### 3.4 Escape `kappa>=4`

Here `k^2>=4h`.  Because `0<=eta<h`,

```text
sigma-q <= 2h sec^2(k theta).
```

Also `q>3/2`, `sigma>3/2`, and `k<1`, so

```text
2q sigma^2 > 3 sigma^2 > 1+sigma^2
                              >=1+k^2 sigma^2.
```

Consequently

```text
q k^2 sigma^2 >=4h q sigma^2
               >2h sec^2(k theta)>=sigma-q,
```

or

```text
p(1+s^2)>s.
```

On `g<1`, C2-E gives `rB<s/[p(1+s^2)]<1`.  Thus every `kappa>=4` point is
retained-empty, independently of `beta`.

Sections 3.1--3.4 exhaust `beta<0` and every `kappa>=0`.  Combining with
(1.2) proves that every retained point of the complete original-coordinate
collar (1.3) is signed by C2-L or is retained-empty.

## 4. One preregistered compact-annulus computation

After removing (1.3), the three formerly incomplete high-`t` boxes have the
exact compact `t` interval

```text
[63/64,1-2^-17].
```

The preregistered run used at most 1,000,000 visited boxes per target and no
escalation.

```text
LHL: complete; 75,781 visited, zero unresolved, zero singular;
IHL: cap exhausted; 21 residual stack boxes, no atomic unresolved;
LHH: cap exhausted; 125,130 atomic unresolved and 47 residual boxes.
```

Together with the analytic collar, `LHL` is now a complete effective dyadic
cell.  `IHL` and `LHH` remain incomplete.  The LHH failure is no longer a
`t=1` issue; it is the independent `(k,y)->(0,1)` side-edge dependency on a
compact `t` annulus.  No second subdivision run is allowed or performed.

## 5. Scope

The complete collar and LHL cell are coefficient results conditional on the
noncanonical R14/R17 reduction.  They do not prove the premise-complete
physical bridge, determinant orientation, or global reflection symmetry.

