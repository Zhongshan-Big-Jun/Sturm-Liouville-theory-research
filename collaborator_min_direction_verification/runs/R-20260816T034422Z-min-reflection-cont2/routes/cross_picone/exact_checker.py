"""Exact algebra checks for the cross-root Picone/Green route.

This script proves only polynomial identities and rank/sign witnesses.  It does
not search for, or certify, a global relay root.
"""

import sympy as sp


def main() -> None:
    A, B = sp.symbols("A B", real=True)
    y, yp, z, zp = sp.symbols("y yp z zp", real=True)

    # Cellwise scalar cross-energy identity.  Substitute y''=-Ay, z''=-Bz.
    m = (A + B) / 2
    energy_derivative = (-A * y) * zp + yp * (-B * z) + m * (yp * z + y * zp)
    wronskian_rhs = (A - B) * (yp * z - y * zp) / 2
    assert sp.expand(energy_derivative - wronskian_rhs) == 0

    mu = sp.symbols("mu", positive=True)
    D = sp.diag(1, mu**2)
    Cdet = sp.Matrix([[0, 1], [-1, 0]])
    u1, v1, u2, v2 = sp.symbols("u1 v1 u2 v2", real=True)
    x1 = sp.Matrix([[u1, v1]])
    x2 = sp.Matrix([u2, v2])
    root1_skew = sp.expand((x1 * D * Cdet * x2)[0])
    root2_skew = sp.expand((x1 * Cdet * D * x2)[0])
    assert root1_skew == u1 * v2 - mu**2 * v1 * u2
    assert root2_skew == mu**2 * u1 * v2 - v1 * u2

    # The two alternating event rays span R^2 after multiplication by D.
    null_ray_rows = sp.Matrix([[mu, mu**2], [-mu, mu**2]])
    assert sp.factor(null_ray_rows.det()) == 2 * mu**3
    assert null_ray_rows.rank() == 2

    # Same positive quadrant, same min-material side S2<0, opposite K1 signs.
    mu_value = sp.Integer(2)
    event = {u1: 2, v1: 1, mu: mu_value}
    witness_positive = {**event, u2: sp.Rational(1, 4), v2: 1}
    witness_negative = {**event, u2: 1, v2: 1}
    S2 = u2**2 - mu**2 * v2**2
    assert S2.subs(witness_positive) == sp.Rational(-63, 16)
    assert S2.subs(witness_negative) == -3
    assert root1_skew.subs(witness_positive) == 1
    assert root1_skew.subs(witness_negative) == -2
    # At the root-1 event, (u_1',v_1')=(0,-1) gives S_1'=8 and
    # physical signed relay energy -1.
    assert 2 * 2 * 0 - 2 * mu_value**2 * 1 * (-1) == 8
    assert 0**2 - (-1) ** 2 == -1

    # The analogous root-2-event skew also has both signs in one quadrant.
    root2_event = {u2: 2, v2: 1, mu: mu_value}
    witness2_positive = {**root2_event, u1: 1, v1: 1}
    witness2_negative = {**root2_event, u1: sp.Rational(1, 4), v1: 1}
    S1 = u1**2 - mu**2 * v1**2
    assert S1.subs(witness2_positive) == -3
    assert S1.subs(witness2_negative) == sp.Rational(-63, 16)
    assert root2_skew.subs(witness2_positive) == 2
    assert root2_skew.subs(witness2_negative) == -1

    # Reflection-sector Minty control A<0 leaves the Picone skew M with
    # either sign, even when all four local mode values are positive and the
    # mismatch direction is fixed (T<0<T_sharp).
    f, f_sharp, g, g_sharp = sp.symbols(
        "f f_sharp g g_sharp", real=True
    )
    d_u, e_u = f - f_sharp, f + f_sharp
    d_v, e_v = g - g_sharp, g + g_sharp
    T = f**2 - mu**2 * g**2
    T_sharp = f_sharp**2 - mu**2 * g_sharp**2
    minty = sp.expand(d_u * e_u - mu**2 * d_v * e_v)
    skew = sp.expand(e_u * d_v - mu**2 * e_v * d_u)
    assert sp.expand(minty - (T - T_sharp)) == 0
    sector_negative = {mu: 2, f: 8, f_sharp: 7, g: 5, g_sharp: 3}
    sector_positive = {mu: 2, f: 8, f_sharp: 7, g: 8, g_sharp: 3}
    assert (T.subs(sector_negative), T_sharp.subs(sector_negative)) == (-36, 13)
    assert (T.subs(sector_positive), T_sharp.subs(sector_positive)) == (-192, 13)
    assert (minty.subs(sector_negative), skew.subs(sector_negative)) == (-49, -2)
    assert (minty.subs(sector_positive), skew.subs(sector_positive)) == (-205, 31)

    # Generic rank of (controlled Minty polarization, free skew polarization)
    # as linear forms of (e_u,e_v).
    du, dv = sp.symbols("du dv", real=True)
    sector_matrix = sp.Matrix([[du, -mu**2 * dv], [dv, -mu**2 * du]])
    assert sp.simplify(sector_matrix.det() - mu**2 * (dv**2 - du**2)) == 0

    print("PASS: scalar identity, full-rank event obstruction, and rational sign witnesses")


if __name__ == "__main__":
    main()
