#!/usr/bin/env python3
"""Exact Bernstein certificate for the mu=2 full-interface Schur gap.

The script independently reconstructs the residual from oscillator endpoint
formulae, maps the admissible semialgebraic domain to the open unit cube,
converts the resulting polynomial to the full tensor Bernstein basis, and
reports the exact signs of every rational Bernstein coefficient.

No floating-point sign decision is made anywhere in this file.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math

import sympy as sp


def cell(t: sp.Expr, z: sp.Expr) -> dict[str, sp.Expr]:
    """Exact mu=2 endpoint data, t=tan(theta/2)."""
    cosine = (1-t**2)/(1+t**2)
    sine = 2*t/(1+t**2)
    big_t = 2*t/(1-t**2)
    high_cosine = (1-big_t**2)/(1+big_t**2)
    high_sine = 2*big_t/(1+big_t**2)
    x_left = sp.factor((z-cosine)/sine)
    y_left = sp.factor((-z-high_cosine)/high_sine)
    x_right = sp.factor((cosine*z-1)/(sine*z))
    y_right = sp.factor((1+high_cosine*z)/(high_sine*z))
    q_value = sp.factor(sine+2*high_sine)
    k_value = sp.factor(2*t**2/(1+t**2))
    a_value = sp.factor(-(1+t**2)/(t*(t-1)*(t+1)))
    g_value = sp.factor(x_left-2*y_left)
    h_value = sp.factor(-x_right+2*y_right)
    assert sp.factor(g_value-a_value*(z-k_value)) == 0
    assert sp.factor(h_value-a_value*(1-k_value*z)/z) == 0
    return {
        "x": x_left, "y": y_left, "xR": x_right, "yR": y_right,
        "Q": q_value, "k": k_value, "A": a_value,
        "g": g_value, "h": h_value,
    }


def reconstruct_residual() -> tuple[sp.Poly, dict[str, sp.Expr]]:
    """Reconstruct the primitive P(x,y,r) from the exact left split gap."""
    x, y, r = sp.symbols("x y r", positive=True)
    delta = r**2-1
    denominator_a = (
        3*r*x**3*y**2-r*x**3-3*r*x*y**2+r*x
        +x**4*y+2*x**2*y**3-4*x**2*y+y
    )
    numerator_b = (
        2*r*x**3*y**2+r*x*y**4-4*r*x*y**2+r*x
        +3*x**2*y**3-3*x**2*y-y**3+y
    )
    a = sp.factor(-y*(x-y)*(x+y)*(1+x**2)/denominator_a)
    b = sp.factor(numerator_b/(r*x*(x-y)*(x+y)*(1+y**2)))
    positive = cell(x, a)
    negative = cell(y, b)
    assert sp.factor(negative["x"]-positive["xR"]/r) == 0
    assert sp.factor(negative["y"]-positive["yR"]/r) == 0
    B = -b
    G = -negative["g"]
    J = -negative["h"]
    d1 = delta*a*positive["Q"]+positive["h"]+a**2*positive["g"]
    n_left = sp.cancel(
        r**2*a*B*(G+J)*(delta*positive["Q"]+a*positive["g"])
        -delta*negative["Q"]*d1
    )
    numerator, denominator = map(sp.factor, sp.fraction(n_left))
    expected_denominator = (
        x**3*(1+x**2)*(1+y**2)**2*denominator_a**3
    )
    assert sp.expand(denominator-expected_denominator) == 0
    residual = sp.Poly(sp.expand(numerator), x, y, r, domain=sp.QQ)
    assert residual.content() == 1
    return residual, {
        "x": x, "y": y, "r": r,
        "D_a": denominator_a, "N_b": numerator_b,
    }


def natural_core(
    residual: sp.Poly, variables: dict[str, sp.Expr]
) -> tuple[sp.Poly, dict[str, sp.Expr]]:
    """Remove the positive Y^2/(3Y-1)^2 factor after the kappa map."""
    x, y, r = variables["x"], variables["y"], variables["r"]
    X, Y, kappa = sp.symbols("X Y kappa", positive=True)
    degree_r = residual.degree(r)
    cleared = sp.Integer(0)
    for (power_x, power_y, power_r), coefficient in residual.terms():
        assert power_x >= power_r
        assert (power_x-power_r) % 2 == 0
        assert (power_y+power_r) % 2 == 0
        cleared += (
            coefficient*kappa**power_r
            *X**((power_x-power_r)//2)
            *Y**((power_y+power_r)//2)
            *(1-3*X)**power_r*(3*Y-1)**(degree_r-power_r)
        )
    cleared_poly = sp.Poly(sp.expand(cleared), X, Y, kappa, domain=sp.QQ)
    core_expr = sp.cancel(cleared_poly.as_expr()/(Y**2*(3*Y-1)**4))
    core = sp.Poly(core_expr, X, Y, kappa, domain=sp.QQ)
    assert sp.expand(cleared_poly.as_expr()-Y**2*(3*Y-1)**4*core.as_expr()) == 0

    # Direct rational reconstruction of
    # P = Y^2/(3Y-1)^2 * core after r=kappa*y(1-3X)/(x(3Y-1)).
    direct = sp.cancel(
        residual.as_expr().subs(
            r, kappa*y*(1-3*x**2)/(x*(3*y**2-1))
        )
    )
    expected = (
        Y**2/(3*Y-1)**2*core.as_expr()
    ).subs({X: x**2, Y: y**2})
    assert sp.factor(direct-expected) == 0
    return core, {"X": X, "Y": Y, "kappa": kappa}


def box_polynomial(
    core: sp.Poly, variables: dict[str, sp.Expr]
) -> tuple[sp.Poly, dict[str, sp.Expr]]:
    """Set kappa=w*kappa_N, X=u/3, Y=(1+2v)/3 and clear denominators."""
    X, Y, kappa = variables["X"], variables["Y"], variables["kappa"]
    u, v, w = sp.symbols("u v w", positive=True)
    C = sp.expand((3*Y-1)*(1-Y))
    E = sp.expand(C+2*Y*(Y-X))
    kappa_n = sp.cancel(C/E)
    f_middle = sp.expand(Y**2+2*X*Y-4*Y+1)
    assert sp.expand(E+f_middle) == 0
    n_tilde = sp.expand(C+kappa*f_middle)
    assert sp.factor(n_tilde.subs(kappa, w*kappa_n)-C*(1-w)) == 0

    d_zero = sp.expand(1-4*X+X**2+2*X*Y)
    d_one_coefficient = sp.expand((1-X)*(3*X-1))
    d_tilde = sp.expand(d_zero+kappa*d_one_coefficient)
    assert sp.factor(d_tilde.subs(kappa, 1)-2*X*(Y-X)) == 0

    # Clear E^degree_kappa term by term.  This is an exact polynomial-ring
    # operation and avoids asking a general rational simplifier to process a
    # thousand-term intermediate expression.
    degree_kappa = core.degree(kappa)
    cleared = sp.Integer(0)
    for (power_x, power_y, power_kappa), coefficient in core.terms():
        cleared += (
            coefficient*X**power_x*Y**power_y*w**power_kappa
            *C**power_kappa*E**(degree_kappa-power_kappa)
        )
    cleared = sp.expand(cleared)
    substituted = sp.expand(
        cleared.subs(
            {X: u/sp.Integer(3), Y: (1+2*v)/sp.Integer(3)},
            simultaneous=True,
        )
    )
    raw = sp.Poly(substituted, u, v, w, domain=sp.QQ)
    content, primitive = raw.primitive()
    midpoint = primitive.eval({u: sp.Rational(1, 2),
                               v: sp.Rational(1, 2),
                               w: sp.Rational(1, 2)})
    if midpoint < 0:
        primitive = -primitive
        content = -content
    assert midpoint != 0
    return primitive, {
        "u": u, "v": v, "w": w,
        "C": C, "E": E, "kappa_N": kappa_n,
        "D_zero": d_zero, "D_one_coefficient": d_one_coefficient,
        "D_tilde": d_tilde, "N_tilde": n_tilde,
        "cleared_content": content,
        "cleared_denominator": E**degree_kappa,
    }


def coarse_box_polynomial(
    core: sp.Poly, variables: dict[str, sp.Expr]
) -> tuple[sp.Poly, dict[str, sp.Expr]]:
    """Map the whole coarse physical container to the open unit cube."""
    X, Y, kappa = variables["X"], variables["Y"], variables["kappa"]
    u, v, w = sp.symbols("u v w", positive=True)
    substituted = sp.expand(core.as_expr().subs(
        {X: u/sp.Integer(3), Y: (1+2*v)/sp.Integer(3), kappa: w},
        simultaneous=True,
    ))
    raw = sp.Poly(substituted, u, v, w, domain=sp.QQ)
    content, primitive = raw.primitive()
    assert content > 0
    return primitive, {
        "u": u, "v": v, "w": w,
        "positive_content": content,
    }


def as_fraction(value: sp.Rational) -> Fraction:
    value = sp.Rational(value)
    return Fraction(int(value.p), int(value.q))


def tensor_bernstein_coefficients(poly: sp.Poly) -> tuple[list[Fraction], tuple[int, int, int]]:
    """Convert a trivariate power polynomial to its same-degree Bernstein basis."""
    degrees = tuple(int(value) for value in poly.degree_list())
    nu, nv, nw = degrees
    power: dict[tuple[int, int, int], Fraction] = {
        tuple(int(value) for value in powers): as_fraction(coefficient)
        for powers, coefficient in poly.terms()
    }

    # Transform one coordinate at a time.  For degree n,
    # b_i=sum_{a<=i} power_a*binom(i,a)/binom(n,a).
    stage_u: dict[tuple[int, int, int], Fraction] = {}
    for i in range(nu+1):
        for j in range(nv+1):
            for k in range(nw+1):
                value = Fraction(0)
                for alpha in range(i+1):
                    value += power.get((alpha, j, k), Fraction(0))*Fraction(
                        math.comb(i, alpha), math.comb(nu, alpha)
                    )
                stage_u[(i, j, k)] = value

    stage_v: dict[tuple[int, int, int], Fraction] = {}
    for i in range(nu+1):
        for j in range(nv+1):
            for k in range(nw+1):
                value = Fraction(0)
                for beta in range(j+1):
                    value += stage_u[(i, beta, k)]*Fraction(
                        math.comb(j, beta), math.comb(nv, beta)
                    )
                stage_v[(i, j, k)] = value

    coefficients: list[Fraction] = []
    for i in range(nu+1):
        for j in range(nv+1):
            for k in range(nw+1):
                value = Fraction(0)
                for gamma in range(k+1):
                    value += stage_v[(i, j, gamma)]*Fraction(
                        math.comb(k, gamma), math.comb(nw, gamma)
                    )
                coefficients.append(value)
    return coefficients, degrees


def tensor_power_from_bernstein(
    coefficients: list[Fraction], degrees: tuple[int, int, int]
) -> dict[tuple[int, int, int], Fraction]:
    """Exact inverse transform, used as an implementation audit."""
    nu, nv, nw = degrees
    bernstein: dict[tuple[int, int, int], Fraction] = {}
    cursor = 0
    for i in range(nu+1):
        for j in range(nv+1):
            for k in range(nw+1):
                bernstein[(i, j, k)] = coefficients[cursor]
                cursor += 1
    assert cursor == len(coefficients)

    stage_w: dict[tuple[int, int, int], Fraction] = {}
    for i in range(nu+1):
        for j in range(nv+1):
            for gamma in range(nw+1):
                value = Fraction(0)
                for k in range(gamma+1):
                    value += Fraction(
                        (-1)**(gamma-k)*math.comb(gamma, k), 1
                    )*bernstein[(i, j, k)]
                stage_w[(i, j, gamma)] = math.comb(nw, gamma)*value

    stage_v: dict[tuple[int, int, int], Fraction] = {}
    for i in range(nu+1):
        for beta in range(nv+1):
            for gamma in range(nw+1):
                value = Fraction(0)
                for j in range(beta+1):
                    value += Fraction(
                        (-1)**(beta-j)*math.comb(beta, j), 1
                    )*stage_w[(i, j, gamma)]
                stage_v[(i, beta, gamma)] = math.comb(nv, beta)*value

    power: dict[tuple[int, int, int], Fraction] = {}
    for alpha in range(nu+1):
        for beta in range(nv+1):
            for gamma in range(nw+1):
                value = Fraction(0)
                for i in range(alpha+1):
                    value += Fraction(
                        (-1)**(alpha-i)*math.comb(alpha, i), 1
                    )*stage_v[(i, beta, gamma)]
                power[(alpha, beta, gamma)] = math.comb(nu, alpha)*value
    return power


def main() -> int:
    residual, raw_variables = reconstruct_residual()
    core, natural_variables = natural_core(residual, raw_variables)
    q_box, box_data = coarse_box_polynomial(core, natural_variables)
    coefficients, degrees = tensor_bernstein_coefficients(q_box)
    coefficient_lines = [
        f"{value.numerator}/{value.denominator}" for value in coefficients
    ]
    coefficient_bytes = ("\n".join(coefficient_lines)+"\n").encode("ascii")
    negative = sum(value < 0 for value in coefficients)
    zero = sum(value == 0 for value in coefficients)
    positive = sum(value > 0 for value in coefficients)
    assert len(coefficients) == math.prod(degree+1 for degree in degrees)
    assert negative == 0
    assert positive > 0

    # Exact full round trip checks the implemented change of basis, not just
    # a sample evaluation.
    recovered_power = tensor_power_from_bernstein(coefficients, degrees)
    expected_power = {
        (i, j, k): as_fraction(q_box.coeff_monomial(
            box_data["u"]**i*box_data["v"]**j*box_data["w"]**k
        ))
        for i in range(degrees[0]+1)
        for j in range(degrees[1]+1)
        for k in range(degrees[2]+1)
    }
    assert recovered_power == expected_power

    X, Y, kappa = (
        natural_variables["X"], natural_variables["Y"],
        natural_variables["kappa"],
    )
    x, y, r = raw_variables["x"], raw_variables["y"], raw_variables["r"]
    C = sp.expand((3*Y-1)*(1-Y))
    E = sp.expand(C+2*Y*(Y-X))
    kappa_n = sp.cancel(C/E)
    d_zero = sp.expand(1-4*X+X**2+2*X*Y)
    d_slope = sp.expand((1-X)*(3*X-1))
    d_tilde = sp.expand(d_zero+kappa*d_slope)
    n_tilde = sp.expand(C-kappa*E)
    r_substitution = kappa*y*(1-3*x**2)/(x*(3*y**2-1))
    domain_checks = {
        "N_b_transform": sp.factor(
            raw_variables["N_b"].subs(r, r_substitution)
            -y*(1-3*x**2)/(3*y**2-1)
            *n_tilde.subs({X: x**2, Y: y**2})
        ),
        "D_a_transform": sp.factor(
            raw_variables["D_a"].subs(r, r_substitution)
            -y*d_tilde.subs({X: x**2, Y: y**2})
        ),
        "E_minus_C": sp.factor(E-C-2*Y*(Y-X)),
        "D_at_one": sp.factor(d_tilde.subs(kappa, 1)-2*X*(Y-X)),
        "D_slope": sp.factor(d_slope-(1-X)*(3*X-1)),
    }
    assert all(value == 0 for value in domain_checks.values())

    report = {
        "status_label": "EXACT_BERNSTEIN_CERTIFICATE",
        "scope": "mu=2, one full physical positive-negative interface",
        "residual_P": {
            "degrees_x_y_r": list(residual.degree_list()),
            "term_count": len(residual.terms()),
            "sha256_expanded": hashlib.sha256(
                str(residual.as_expr()).encode("utf-8")
            ).hexdigest(),
        },
        "natural_core": {
            "identity": "P=Y^2/(3Y-1)^2*P_core",
            "degrees_X_Y_kappa": list(core.degree_list()),
            "term_count": len(core.terms()),
            "sha256_expanded": hashlib.sha256(
                str(core.as_expr()).encode("utf-8")
            ).hexdigest(),
        },
        "domain_map": {
            "X": "u/3",
            "Y": "(1+2v)/3",
            "kappa": "w",
            "kappa_N": str(kappa_n),
            "N_b_equivalence": "N_b>0 iff 0<kappa<kappa_N",
            "kappa_N_bound": "0<kappa_N<1 because E=C+2Y(Y-X)>C>0",
            "D_slope": "(1-X)(3X-1)<0",
            "D_bound": "D(kappa)>D(1)=2X(Y-X)>0",
            "unit_cube": "0<u,v,w<1",
        },
        "Q_box": {
            "degrees_u_v_w": list(q_box.degree_list()),
            "power_term_count": len(q_box.terms()),
            "sha256_expanded": hashlib.sha256(
                str(q_box.as_expr()).encode("utf-8")
            ).hexdigest(),
            "positive_content": str(box_data["positive_content"]),
        },
        "bernstein": {
            "basis_degrees_u_v_w": list(degrees),
            "coefficient_order": "i outer, j middle, k inner; each 0..degree",
            "coefficient_serialization": "reduced numerator/denominator, one ASCII line, trailing newline",
            "coefficient_count": len(coefficients),
            "positive_count": positive,
            "zero_count": zero,
            "negative_count": negative,
            "sha256_coefficients": hashlib.sha256(coefficient_bytes).hexdigest(),
            "minimum_coefficient": str(min(coefficients)),
            "minimum_positive_coefficient": str(min(
                value for value in coefficients if value > 0
            )),
            "maximum_coefficient": str(max(coefficients)),
            "exact_full_roundtrip": True,
        },
        "logical_conclusion": (
            "Every tensor Bernstein basis function is strictly positive on "
            "the open cube; nonnegative coefficients with at least one "
            "positive coefficient imply Q_box>0 there."
        ),
        "sympy_version": sp.__version__,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
