#!/usr/bin/env python3
"""Freeze the exact mu=2 full-interface split-gap reduction.

This is proof-supporting symbolic algebra, not a numerical sign test.  It
eliminates both independent momenta at one material interface and proves
that the left and time-reversed right Schur gaps have the same residual
polynomial.  Positivity of that polynomial is discharged separately by the
exact Bernstein certificate recorded in the route derivation.
"""

from __future__ import annotations

import hashlib
import json

import sympy as sp


def cell(t: sp.Expr, z: sp.Expr) -> dict[str, sp.Expr]:
    """mu=2 endpoint data in the half-angle coordinate t=tan(theta/2)."""
    cosine = (1 - t**2) / (1 + t**2)
    sine = 2 * t / (1 + t**2)
    big_t = 2 * t / (1 - t**2)
    high_cosine = (1 - big_t**2) / (1 + big_t**2)
    high_sine = 2 * big_t / (1 + big_t**2)
    x_left = sp.factor((z - cosine) / sine)
    y_left = sp.factor((-z - high_cosine) / high_sine)
    x_right = sp.factor((cosine * z - 1) / (sine * z))
    y_right = sp.factor((1 + high_cosine * z) / (high_sine * z))
    q_value = sp.factor(sine + 2 * high_sine)
    k_value = sp.factor(2 * t**2 / (1 + t**2))
    a_value = sp.factor(-(1 + t**2) / (t * (t - 1) * (t + 1)))
    g_value = sp.factor(x_left - 2 * y_left)
    h_value = sp.factor(-x_right + 2 * y_right)
    assert sp.factor(g_value - a_value * (z - k_value)) == 0
    assert sp.factor(h_value - a_value * (1 - k_value * z) / z) == 0
    return {
        "x": x_left,
        "y": y_left,
        "xR": x_right,
        "yR": y_right,
        "Q": q_value,
        "k": k_value,
        "A": a_value,
        "g": g_value,
        "h": h_value,
    }


def main() -> int:
    # x is a positive-cell half angle, y is the adjacent negative-cell half
    # angle, r=sqrt(R), a/c are positive ratios, and b is the negative ratio.
    x, y, r = sp.symbols("x y r", positive=True)
    a, b, c = sp.symbols("a b c", nonzero=True)
    delta = r**2 - 1

    px = cell(x, a)
    ny = cell(y, b)

    # Exact simultaneous solution of x_-=xR_+/r and y_-=yR_+/r.
    denominator_a = (
        3*r*x**3*y**2 - r*x**3 - 3*r*x*y**2 + r*x
        + x**4*y + 2*x**2*y**3 - 4*x**2*y + y
    )
    numerator_b = (
        2*r*x**3*y**2 + r*x*y**4 - 4*r*x*y**2 + r*x
        + 3*x**2*y**3 - 3*x**2*y - y**3 + y
    )
    a_left = sp.factor(
        -y*(x-y)*(x+y)*(x**2+1) / denominator_a
    )
    b_left = sp.factor(
        numerator_b / (r*x*(x-y)*(x+y)*(y**2+1))
    )
    left_positive = cell(x, a_left)
    left_negative = cell(y, b_left)
    assert sp.factor(left_negative["x"] - left_positive["xR"] / r) == 0
    assert sp.factor(left_negative["y"] - left_positive["yR"] / r) == 0

    # Time reversal gives the exact simultaneous solution of
    # x_+=r*xR_- and y_+=r*yR_- at the right interface.
    c_right = sp.factor(
        -denominator_a / (y*(x-y)*(x+y)*(x**2+1))
    )
    b_right = sp.factor(
        r*x*(x-y)*(x+y)*(y**2+1) / numerator_b
    )
    right_positive = cell(x, c_right)
    right_negative = cell(y, b_right)
    assert sp.factor(right_positive["x"] - r*right_negative["xR"]) == 0
    assert sp.factor(right_positive["y"] - r*right_negative["yR"]) == 0
    assert sp.factor(a_left*c_right - 1) == 0
    assert sp.factor(b_left*b_right - 1) == 0

    # Left split gap.  Set B=-b>0, G=-g_->0 and J=-h_->0.  The cleared
    # quantity N_L has the same sign as E_L=beta_R*x_jump+gamma_2 because
    # E_L=r*G*N_L/[delta*D_1*Q_2], whose omitted factors are physical-positive.
    b_value = b_left
    B = -b_value
    G = -left_negative["g"]
    J = -left_negative["h"]
    g1, h1 = left_positive["g"], left_positive["h"]
    q1, q2 = left_positive["Q"], left_negative["Q"]
    d1 = delta*a_left*q1 + h1 + a_left**2*g1
    n_left = sp.factor(
        r**2*a_left*B*(G+J)*(delta*q1+a_left*g1)
        - delta*q2*d1
    )
    assert sp.factor(h1-r*G) == 0
    middle_w = q2/(r*B)  # normalization u_2^2=1
    x_star = sp.factor((r*J-(-r*G))/middle_w)
    beta_right = sp.factor(
        a_left*h1*(delta*q1+a_left*g1)/(delta*d1)
    )
    e_left = sp.factor(beta_right*x_star-r*G)
    assert sp.factor(e_left-r*G*n_left/(delta*d1*q2)) == 0
    left_numerator, left_denominator = map(
        sp.factor, sp.fraction(sp.cancel(n_left))
    )

    # Right split gap.  Here E_R=beta_L*x_jump-gamma_3 equals
    # r*J*N_R/[delta*D_3*B*Q_2], again with a positive physical prefactor.
    b_value = b_right
    B = -b_value
    G = -right_negative["g"]
    J = -right_negative["h"]
    g3, h3 = right_positive["g"], right_positive["h"]
    q3, q2r = right_positive["Q"], right_negative["Q"]
    d3 = delta*c_right*q3 + h3 + c_right**2*r*J
    n_right = sp.factor(
        r**2*(G+J)*(delta*c_right*q3+h3)
        - delta*q2r*B*d3
    )
    assert sp.factor(g3-r*J) == 0
    middle_wr = q2r/(r*B)  # normalization u_2^2=1
    x_starr = sp.factor((r*J-(-r*G))/middle_wr)
    beta_left = sp.factor(
        g3*(delta*c_right*q3+h3)/(delta*d3*B**2)
    )
    e_right = sp.factor(beta_left*x_starr-r*J)
    assert sp.factor(e_right-r*J*n_right/(delta*d3*B*q2r)) == 0
    right_numerator, right_denominator = map(
        sp.factor, sp.fraction(sp.cancel(n_right))
    )

    # The common primitive residual polynomial is P=Num(N_L).  The
    # reduced time-reversed right rational function has numerator -r*P and
    # a denominator with the single negative factor (x-y).  Thus its sign is
    # again the sign of P on 0<x<y.
    residual = sp.Poly(sp.expand(left_numerator), x, y, r, domain=sp.QQ)
    expected_right_numerator = sp.expand(-r*residual.as_expr())
    right_numerator_ratio = sp.factor(
        sp.cancel(right_numerator/residual.as_expr())
    )
    assert sp.factor(right_numerator_ratio+r) == 0, (
        right_numerator_ratio
    )

    expected_left_denominator = (
        x**3*(x**2+1)*(y**2+1)**2*denominator_a**3
    )
    expected_right_denominator = (
        x**2*y**2*(x-y)*(x+y)*(x**2+1)**3*(y**2+1)
        * numerator_b*denominator_a
    )
    assert sp.expand(left_denominator-expected_left_denominator) == 0
    assert sp.expand(right_denominator-expected_right_denominator) == 0

    # b_left<0 forces numerator_b>0 in the phase chamber 0<x<y; then the
    # displayed decomposition proves r*x*(3*y^2-1)-y*(1-3*x^2)<0.
    xcap = 1 - 3*x**2
    ycap = 3*y**2 - 1
    nb_decomposition = sp.expand(
        y*(1-y**2)*xcap
        - r*x*((1-y**2)*ycap + 2*y**2*(y**2-x**2))
    )
    assert sp.expand(numerator_b-nb_decomposition) == 0

    residual_text = str(residual.as_expr())

    # Natural semialgebraic coordinates.  Every monomial x^i y^j r^m in P
    # has i-m and j+m even and nonnegative.  Therefore substitution
    #   X=x^2, Y=y^2, kappa=r*x*(3Y-1)/(y*(1-3X))
    # introduces no square roots.  Multiplication by (3Y-1)^deg_r clears
    # all denominators exactly.
    X, Y, kappa = sp.symbols("X Y kappa", positive=True)
    degree_r = residual.degree(r)
    natural_expr = sp.Integer(0)
    for (power_x, power_y, power_r), coefficient in residual.terms():
        assert power_x >= power_r
        assert (power_x-power_r) % 2 == 0
        assert (power_y+power_r) % 2 == 0
        natural_expr += (
            coefficient*kappa**power_r
            * X**((power_x-power_r)//2)
            * Y**((power_y+power_r)//2)
            * (1-3*X)**power_r
            * (3*Y-1)**(degree_r-power_r)
        )
    natural_poly = sp.Poly(
        sp.expand(natural_expr), X, Y, kappa, domain=sp.QQ
    )
    natural_factor = sp.factor(natural_poly.as_expr())
    # Exact reconstruction check against direct rational substitution.
    direct_substitution = sp.cancel(
        residual.as_expr().subs(
            r, kappa*y*(1-3*x**2)/(x*(3*y**2-1))
        )*(3*y**2-1)**degree_r
    )
    natural_back = natural_poly.as_expr().subs({X: x**2, Y: y**2})
    assert sp.factor(direct_substitution-natural_back) == 0

    # Low-degree physical inequalities in (X,Y,kappa).  The common positive
    # factor y has been removed from D_a and N_b.
    d_tilde = sp.expand(
        1-4*X+X**2+2*X*Y-kappa*(1-3*X)*(1-X)
    )
    f_middle = sp.expand(Y**2+2*X*Y-4*Y+1)
    n_tilde = sp.expand((1-Y)*(3*Y-1)+kappa*f_middle)
    assert sp.factor(
        denominator_a.subs(
            r, kappa*y*(1-3*x**2)/(x*(3*y**2-1))
        )-y*d_tilde.subs({X: x**2, Y: y**2})
    ) == 0
    assert sp.factor(
        numerator_b.subs(
            r, kappa*y*(1-3*x**2)/(x*(3*y**2-1))
        )
        -y*(1-3*x**2)/(3*y**2-1)
        * n_tilde.subs({X: x**2, Y: y**2})
    ) == 0
    branch_lower = sp.expand(
        (Y-X)*(1+X)**2-2*X*d_tilde
    )
    branch_upper = sp.expand(d_tilde-2*X*(Y-X))

    report = {
        "status_label": "EXACT_SYMBOLIC_REDUCTION",
        "mu": 2,
        "interface_solutions": {
            "a_left": str(a_left),
            "b_left": str(b_left),
            "c_right": str(c_right),
            "b_right": str(b_right),
            "time_reversal_products": ["a_left*c_right=1", "b_left*b_right=1"],
        },
        "common_residual": {
            "definition": "P=primitive numerator of N_left",
            "sha256_of_expanded_sympy_string": hashlib.sha256(
                residual_text.encode("utf-8")
            ).hexdigest(),
            "term_count": len(residual.terms()),
            "degrees_x_y_r": list(residual.degree_list()),
            "content": str(sp.polys.polytools.terms_gcd(residual.as_expr(), clear=False)),
            "sympy_factorization_unchanged": bool(
                sp.factor(residual.as_expr()) == residual.as_expr()
            ),
        },
        "natural_coordinate_residual": {
            "definition": "Pnat=(3Y-1)^6 P after r=kappa*y*(1-3X)/(x*(3Y-1))",
            "sha256_of_expanded_sympy_string": hashlib.sha256(
                str(natural_poly.as_expr()).encode("utf-8")
            ).hexdigest(),
            "term_count": len(natural_poly.terms()),
            "degrees_X_Y_kappa": list(natural_poly.degree_list()),
            "factorization": str(natural_factor),
            "D_tilde_positive": str(d_tilde),
            "N_tilde_positive": str(n_tilde),
            "positive_branch_lower_positive": str(branch_lower),
            "positive_branch_upper_positive": str(branch_upper),
            "r_gt_1": "kappa^2*Y*(1-3X)^2-X*(3Y-1)^2>0",
        },
        "left_identity": {
            "N_left": "P/[x^3(1+x^2)(1+y^2)^2 D_a^3]",
            "E_left": "r G N_left/[delta D_1 Q_2]",
        },
        "right_identity": {
            "N_right": "-r P/[x^2 y^2 (x-y)(x+y)(1+x^2)^3 (1+y^2) N_b D_a]",
            "E_right": "r J N_right/[delta D_3 B Q_2]",
        },
        "admissible_signs": {
            "phase_chamber": "r>1, 0<x<1/sqrt(3)<y<1",
            "positive_ratio": "D_a>0 (equivalent to a_left>0 and c_right>0)",
            "negative_ratio": "N_b>0 (equivalent to b_left<0 and b_right<0)",
            "known_interface_factor": "r*x*(3*y^2-1)-y*(1-3*x^2)<0",
            "sign_status": "P>0 discharged by the exact Bernstein certificate in route derivation section 8",
        },
        "sympy_version": sp.__version__,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
