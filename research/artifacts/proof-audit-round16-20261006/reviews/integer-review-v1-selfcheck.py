"""Independent finite algebra checks; not the all-integer analytic proof."""
import json
import sys
from pathlib import Path

import sympy as sp

x = sp.Symbol("x", real=True)
c = sp.Symbol("c", positive=True, real=True)
checks = []


def record(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def at(poly, endpoint):
    return sp.expand(poly).subs(x, endpoint)


def integ(poly):
    terms = sp.Poly(sp.expand(poly), x).terms()
    return sp.expand(sum(coeff * (sp.Rational(2, degree[0] + 1) if degree[0] % 2 == 0 else 0)
                         for degree, coeff in terms))


def j_integrate(poly, times):
    for _ in range(times):
        primitive = sp.integrate(poly, x)
        poly = sp.expand(primitive - primitive.subs(x, -1))
    return poly


def b_test(poly, level=0):
    even = sp.diff(poly, x, 2 * level)
    delta = (at(even, 1) - at(even, -1)) / 2
    return [sp.expand(at(sp.diff(even, x), side) - delta) for side in (-1, 1)]


def k_power(poly, times):
    for _ in range(times):
        poly = sp.expand(c * poly - sp.diff(poly, x, 2))
    return poly


def gram(poly, other, r):
    a, b = k_power(poly, r // 2), k_power(other, r // 2)
    if r % 2 == 0:
        return integ(a * sp.conjugate(b))
    delta_a, delta_b = at(a, 1) - at(a, -1), at(b, 1) - at(b, -1)
    return sp.expand(integ(sp.diff(a, x) * sp.conjugate(sp.diff(b, x)))
                     + c * integ(a * sp.conjugate(b))
                     - delta_a * sp.conjugate(delta_b) / 2)


for r in range(1, 7):
    free = [(order, side) for order in range(0, r, 2) for side in (-1, 1)]
    jets = [(order, side) for order in range(r) for side in (-1, 1)]
    matrix = sp.Matrix([[at(sp.diff(x**degree, x, order), side)
                         for degree in range(2 * r)] for order, side in jets])
    lifts = []
    for selected in free:
        values = {index: sp.Integer(index == selected) for index in free}
        data = []
        for order, side in jets:
            data.append(values[(order, side)] if order % 2 == 0 else
                        (values[(order - 1, 1)] - values[(order - 1, -1)]) / 2)
        coefficients = matrix.inv() * sp.Matrix(data)
        lift = sp.expand(sum(coefficients[degree] * x**degree for degree in range(2 * r)))
        lifts.append(lift)
        for (order, side), prescribed in zip(jets, data):
            record(f"r{r}:Hermite:{selected}:{order}:{side}",
                   at(sp.diff(lift, x, order), side) == prescribed)
        for level in range(r // 2):
            record(f"r{r}:lift-boundary:{selected}:{level}", b_test(lift, level) == [0, 0])
    record(f"r{r}:free-count", len(lifts) == 2 * ((r + 1) // 2))

    for n in (r, r + 1, r + 3):
        high = j_integrate(sp.legendre(n, x), r)
        record(f"r{r}:n{n}:degree", sp.degree(high, x) == n + r)
        record(f"r{r}:n{n}:top-derivative", sp.expand(sp.diff(high, x, r) - sp.legendre(n, x)) == 0)
        for order, side in jets:
            record(f"r{r}:n{n}:clamped:{order}:{side}", at(sp.diff(high, x, order), side) == 0)
        permitted = set(range(n - r, n + r + 1, 2))
        for degree in range(n + r + 1):
            legendre_coefficient = integ(high * sp.legendre(degree, x)) * sp.Rational(2 * degree + 1, 2)
            if degree not in permitted:
                record(f"r{r}:n{n}:support-zero:{degree}", legendre_coefficient == 0)

    for degree_cap in (2 * r - 1, 2 * r, 2 * r + 2):
        columns = lifts + [j_integrate(sp.legendre(n, x), r)
                           for n in range(r, degree_cap - r + 1)]
        column_matrix = sp.Matrix([[sp.Poly(poly, x).nth(degree) for poly in columns]
                                   for degree in range(degree_cap + 1)])
        constraints = sp.Matrix([[b_test(x**degree, level)[side_index]
                                  for degree in range(degree_cap + 1)]
                                 for level in range(r // 2) for side_index in range(2)])
        expected = degree_cap + 1 - 2 * (r // 2)
        record(f"r{r}:N{degree_cap}:column-rank", column_matrix.rank() == expected)
        constraint_rank = constraints.rank() if r // 2 else 0
        record(f"r{r}:N{degree_cap}:kernel-dimension", degree_cap + 1 - constraint_rank == expected)
        if r // 2:
            record(f"r{r}:N{degree_cap}:all-columns-in-domain", constraints * column_matrix == sp.zeros(2 * (r // 2), len(columns)))

    n = r
    high_n = j_integrate(sp.legendre(n, x), r)
    for offset in (1, 2 * r + 1, 2 * r + 2):
        high_l = j_integrate(sp.legendre(n + offset, x), r)
        record(f"r{r}:Gram-offset-{offset}", gram(high_n, high_l, r) == 0)
    remote = j_integrate(sp.legendre(3 * r, x), r)
    for index, lift in enumerate(lifts):
        record(f"r{r}:low-high-cutoff:{index}", gram(lift, remote, r) == 0)

high_3 = sp.sqrt(sp.Rational(7, 2)) * j_integrate(sp.legendre(3, x), 1)
counterexample_error_squared = gram(high_3, high_3, 1).subs(c, 1)
counterexample_rhs_squared = sp.Rational(3, 4)
record("negative-t-counterexample:error-exact", counterexample_error_squared == sp.Rational(47, 45))
record("negative-t-counterexample:display23-fails", counterexample_error_squared > counterexample_rhs_squared)

output = {
    "status": "PASS",
    "python": sys.executable,
    "python_version": sys.version,
    "sympy_version": sp.__version__,
    "check_count": len(checks),
    "scope": "Exact finite algebra for r=1..6, selected high indices, three polynomial degree caps; not an infinite or numerical stability proof",
    "checks": checks,
    "negative_t_counterexample": {"r": 1, "c": 1, "N": 1, "t": -1, "nonzero_coefficient": "z_3=1", "error_squared": str(counterexample_error_squared), "purported_bound_squared": str(counterexample_rhs_squared)},
}
target = Path(__file__).with_suffix(".json")
target.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({key: value for key, value in output.items() if key != "checks"}, ensure_ascii=False))
