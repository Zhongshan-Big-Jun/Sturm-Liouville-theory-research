STRICT

# Accepted near-one alpha-zero exclusion

## Audit bindings

- W7 source SHA256:
  `191b0a1cd621b8f8451647a5273a2f79efd0d57b71e3a7ba570e8644cae6e044`.
- Independent audit SHA256:
  `e34da0e0bbf78f569706a095c19d3eb524b0be5f0c5e7fe9361de328c3bb9fdb`.

## Theorem

There is no sequence of complete admissible tuples satisfying

```text
m_j->1+,
alpha_j->0.
```

Equivalently, there exist `epsilon_0>0` and `delta_0>0` such that the
complete phase system has no tuple in

```text
1<m<1+epsilon_0,
0<alpha<delta_0.
```

The contradiction is exact. The spectral and transfer limits give

```text
X/alpha->-1,
Y/alpha->2/3.
```

After the apparent left-layer norm singularities are removed with the exact
spectral equations, the full mass equation gives

```text
s/C->3/2.
```

The exact band equation instead forces

```text
Y/alpha=(s/C)(-X/alpha),
```

which would imply `2/3=3/2`.

## Consequence and precise boundary inventory

Along any existing complete sequence with `m->1+`, the empty wedge implies

```text
alpha/(m-1)->+infinity.
```

This statement is conditional on such tuples existing and does not establish
branch existence.

The fixed-separation near-one theorem in the preceding accepted package uses

```text
eta<=alpha<=pi-eta.
```

The present theorem closes only the `alpha->0` face. It does not cover a
possible joint limit `alpha->pi`, which may couple to `theta->pi/2` and makes
the norm and mass endpoint analysis singular. That face must be analyzed
separately before the mechanism-level near-one argument is global.

Arbitrary finite `R`, global `G>=0`, `PHI-SIGN`, and KP-DET remain open.
