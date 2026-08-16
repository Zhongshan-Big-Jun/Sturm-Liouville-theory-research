"""Exact replay of the MIN-REFL-C2-K explicit-modulus frontier.

The script proves the exact inverse Jacobian and coarse leading-polynomial
majorants.  It also checks that boundary limits alone cannot determine a
positive collar cutoff.  No floating sign test is used.
"""
from __future__ import annotations

import json
import sympy as sp


def main() -> dict:
    h, kappa, beta = sp.symbols("h kappa beta", positive=True)
    c = sp.pi / 2
    k = sp.sqrt(kappa * h)
    z = c - h
    eta = h + beta * h**2
    theta = c + eta
    u = sp.tan(k*z) * sp.tan(h) / (sp.tan(k*theta) * sp.tan(eta))
    alpha = (1-u)/h

    # Exact inverse Jacobian for beta -> alpha in the C2-E chart.
    J = h*u*(
        k/(sp.sin(k*theta)*sp.cos(k*theta))
        + 1/(sp.sin(eta)*sp.cos(eta))
    )
    assert sp.simplify(sp.diff(alpha, beta) - J) == 0
    assert sp.limit(J, h, 0, dir="+") == 1

    # C2-C implicit negative-phase derivatives.  Boundary nondegeneracy is
    # exact, but the frozen artifacts contain no finite-box lower bounds.
    kk, eps, sigma = sp.symbols("kk eps sigma", positive=True)
    F0 = sp.atan(kk*sigma)/kk + sp.atan(kk*sigma/(1-eps)) - sp.pi
    J0 = sp.factor(sp.diff(F0, sigma))
    assert sp.limit(J0, kk, 0, dir="+") == 1

    d, v, tau = sp.symbols("d v tau", positive=True)
    F1 = (
        sp.atan(d/((1-d)*tau))
        + (1-d)*sp.atan(d*(1-d*v)/((1-d)*tau))
    )/d - sp.pi/2
    J1_boundary = sp.limit(sp.diff(F1, tau), d, 0, dir="+").subs(tau, 4/sp.pi)
    assert sp.simplify(J1_boundary + sp.pi**2/8) == 0

    # Coarse exact majorant for all four C2-E leading polynomials.
    # Put x=2*c^2*kappa.  The retained triangle is R>=0,x>=0,R+x<=A.
    R, x, A = sp.symbols("R x A", nonnegative=True)
    Aexpr = 2/c
    PE = [
        R*(R+2*x),
        sp.Rational(4,3)*R*(R+3*x),
        R*(R+6*x),
        8*R*x,
    ]
    edge = [sp.expand(P.subs(x, A-R)) for P in PE]
    maxima = [A**2, sp.Rational(3,2)*A**2, sp.Rational(9,5)*A**2, 2*A**2]
    critical = [A, sp.Rational(3,4)*A, sp.Rational(3,5)*A, A/2]
    for poly, m, r0 in zip(edge, maxima, critical):
        assert sp.simplify(poly.subs(R, r0)-m) == 0
        assert sp.diff(poly, R, 2) < 0
    assert sp.simplify((2*A**2).subs(A, Aexpr) - 32/sp.pi**2) == 0
    assert sp.pi**2 > 8  # hence every C2-E leading polynomial is <4

    # Boundary-limit data do not determine a collar modulus: arbitrary M
    # preserves the replayed limit while making the first safe radius O(1/M).
    radial, M, P0, lam = sp.symbols("radial M P0 lam", positive=True)
    perturbed_E = h**2*(P0+M*h)
    perturbed_C = lam*(P0+M*radial)
    assert sp.limit(perturbed_E/h**2, h, 0, dir="+") == P0
    assert sp.limit(perturbed_C/lam, radial, 0, dir="+") == P0

    return {
        "status": "RIGOROUS_PARTIAL_RESULT",
        "result": "PASS",
        "proved": {
            "C2_E_exact_inverse_jacobian": str(sp.factor(J)),
            "C2_E_jacobian_boundary_limit": "1",
            "C2_C_low_implicit_derivative": str(J0),
            "C2_C_low_derivative_boundary_limit": "1",
            "C2_C_high_derivative_boundary_limit": "-pi**2/8",
            "C2_E_leading_common_upper_bound": "32/pi**2 < 4"
        },
        "unsigned_effective_data": [
            "finite-chart lower bound for C2_E inverse Jacobian J_E",
            "finite-chart lower bound for g*Knew*cp^4",
            "finite-chart suprema of C2_C Psi_0 and Psi_1",
            "finite-chart O(h) bound for C2_E rho_i/h^2-P_i",
            "effective Lebesgue number for complementary t=0 strata"
        ],
        "underdetermination_check": "PASS: arbitrary analytic M preserves all frozen leading limits",
        "floating_sign_tests": 0
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
