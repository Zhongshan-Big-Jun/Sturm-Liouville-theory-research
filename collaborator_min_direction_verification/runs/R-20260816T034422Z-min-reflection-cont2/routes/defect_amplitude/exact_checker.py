from __future__ import annotations

import sympy as sp


def main() -> None:
    z, s, c, S, C = sp.symbols("z s c S C", nonzero=True)
    energy = (z + C) ** 2 / S**2 - (z - c) ** 2 / s**2
    energy_rev = (1 / z + C) ** 2 / S**2 - (1 / z - c) ** 2 / s**2
    reciprocal_residual = sp.together(z**2 * energy_rev - energy)
    reciprocal_residual = sp.expand(reciprocal_residual * s**2 * S**2)
    reciprocal_residual = reciprocal_residual.subs(C**2, 1 - S**2)
    reciprocal_residual = reciprocal_residual.subs(c**2, 1 - s**2)
    assert sp.simplify(reciprocal_residual) == 0

    mu = sp.Integer(2)
    theta = sp.pi / 6
    st = sp.sin(theta)
    ct = sp.cos(theta)
    St = sp.sin(mu * theta)
    Ct = sp.cos(mu * theta)

    exact_rows = []
    x = sp.symbols("x", real=True)
    cos_t = (1 - x**2) / (1 + x**2)
    sin_t = 2 * x / (1 + x**2)
    cos_2t = (1 - 6 * x**2 + x**4) / (1 + x**2) ** 2
    sin_2t = 4 * x * (1 - x**2) / (1 + x**2) ** 2

    for zv in (sp.Rational(1, 2), sp.Integer(2)):
        d_left = sp.simplify((zv - ct) / st + mu * (zv + Ct) / St)
        d_right = sp.simplify(mu * (1 + Ct * zv) / St - (ct * zv - 1) / st)
        ev = sp.factor((zv + Ct) ** 2 / St**2 - (zv - ct) ** 2 / st**2,
                       extension=sp.sqrt(3))
        phi = sp.factor((zv**2 - 1) / ev, extension=sp.sqrt(3))
        assert d_left.is_positive
        assert d_right.is_positive
        assert ev.is_positive

        a = sp.simplify((zv - ct) / st)
        b = sp.simplify((-zv - Ct) / St)
        U = cos_t + a * sin_t
        B = cos_2t + b * sin_2t
        numerator = sp.factor((U**2 - B**2) * (1 + x**2) ** 4,
                              extension=sp.sqrt(3))
        exact_rows.append((zv, d_left, d_right, ev, phi, numerator))

    assert sp.simplify(exact_rows[0][4] + exact_rows[1][4]) == 0

    x_end = 2 - sp.sqrt(3)
    quadratics = (
        x**2 + x * (-3 + 4 * sp.sqrt(3) / 3) - 1 + sp.sqrt(3) / 3,
        x**2 + x * (-sp.Rational(5, 2) + sp.sqrt(3) / 2)
        - sp.Rational(3, 2) - sp.sqrt(3) / 2,
        x**2 + x * (-6 + 10 * sp.sqrt(3) / 3) - 1 - 2 * sp.sqrt(3) / 3,
        x**2 + x * (38 - 22 * sp.sqrt(3)) + 3 - 2 * sp.sqrt(3),
    )
    for quad in quadratics:
        assert sp.simplify(quad.subs(x, 0)).is_negative
        assert sp.simplify(quad.subs(x, x_end)).is_negative

    lam, rho0, p, m = sp.symbols("lam rho0 p m", nonzero=True)
    generator = sp.Matrix([[0, 1], [-lam * rho0, 0]])
    monodromy = sp.Matrix([[1 / p, 0], [m, p]])
    commutator = monodromy * generator - generator * monodromy
    assert sp.simplify(commutator[0, 1] - (1 / p - p)) == 0
    assert sp.simplify(monodromy.det() - 1) == 0

    print("PASS")
    print("reciprocal_energy_identity: z^2 E(1/z)=E(z)")
    for row in exact_rows:
        print(f"z={row[0]}")
        print(f"  D_L={row[1]}")
        print(f"  D_R={row[2]}")
        print(f"  E={row[3]}")
        print(f"  Phi={row[4]}")
        print(f"  first_crossing_numerator={row[5]}")
    print("first_crossing_quadratic_endpoint_signs: all strictly negative")
    print("translation_commutator_b=1/p-p")


if __name__ == "__main__":
    main()
