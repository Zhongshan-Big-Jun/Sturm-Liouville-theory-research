"""Exact symbolic replay for MIN-REFL-C2-E.

This is a conditional R14/R17 calculation.  It uses exact SymPy algebra
over QQ(pi) and never performs a floating sign decision.
"""
from __future__ import annotations

import json
import sympy as sp


def main() -> dict:
    # Exact tangent elimination of a,q,b,sigma from rB.
    p, s, X, T, k = sp.symbols("p s X T k", positive=True)
    q = p / k
    a = p / (k * X)
    sigma = s / k
    b = s / (k * T)
    D = b * (1 + k**2 * a * b) + k**2 * (a + b) * sigma**2
    rb = sp.factor(a * sigma * (1 - k**2 * b**2) / (q * D))
    rb_stable = (T**2 - s**2) / (
        X * T * (1 + s**2) + p * s * (1 + T**2)
    )
    assert sp.simplify(rb - rb_stable) == 0

    # The retained ratio u=a/b and the regular plus ratio v=p/X.
    u, v = sp.symbols("u v", positive=True)
    rb_uv = (s / p) * (u**2 - v**2) / (
        u * (1 + s**2) + u**2 * s**2 + v**2
    )
    assert sp.simplify(
        rb_stable.subs(T, u * s * X / p).subs(X, p / v) - rb_uv
    ) == 0

    # Low-frequency t=1 compensating chart.  h=pi/2-z,
    # k^2=kappa*h and u=1-alpha*h.  The negative angle is solved to the
    # order required by u through eta=h+(alpha-2/c)h^2+O(h^3).
    h, alpha, kappa = sp.symbols("h alpha kappa", positive=True)
    c = sp.pi / 2
    K = kappa * h
    z = c - h
    eta = h + (alpha - 2 / c) * h**2
    theta = c + eta

    # tan(sqrt(K)*x)/sqrt(K), truncated with a rigorously sufficient
    # formal order for all displayed leading coefficients.
    def tan_over_k(x):
        return x + K * x**3 / 3 + 2 * K**2 * x**5 / 15

    qh = tan_over_k(z)
    sh = tan_over_k(theta)
    ah = sp.series(qh * (h + h**3 / 3), h, 0, 4).removeO()
    bh = sp.series(sh * (eta + eta**3 / 3), h, 0, 4).removeO()
    uh = sp.series(ah / bh, h, 0, 2)
    assert sp.simplify(uh.removeO() - (1 - alpha * h)) == 0

    Dh = bh * (1 + K * ah * bh) + K * (ah + bh) * sh**2
    rbh = ah * sh * (1 - K * bh**2) / (qh * Dh)
    rb_series = sp.series(rbh, h, 0, 2).removeO()
    R = 2 / c - alpha - 2 * c**2 * kappa
    assert sp.simplify(rb_series - (1 + h * R)) == 0

    W0 = (1 - K * ah**2) * (
        ah * sh - bh * qh + K * ah * bh * (qh + sh)
    ) / (qh * sh * (ah + bh) * (1 - K * ah))
    W1 = K * ah * (1 - K * ah**2) * (
        bh**2 + bh + sh**2 + K * bh * sh**2
    ) / (qh * (1 - K * ah) * Dh)
    W0lim = sp.factor(sp.limit(W0 / h, h, 0))
    W1lim = sp.factor(sp.limit(W1 / h, h, 0))
    assert sp.simplify(W0lim - (2 - c * alpha) / (2 * c**2)) == 0
    assert sp.simplify(W1lim - kappa * c) == 0

    Knew = (1 - K * ah**2) / ((ah**2 + qh**2) * (1 + K * qh**2)) * (
        ah**2 * (1 - K) / (1 - K * ah) ** 2
        + qh**2 * bh * (1 + K * ah) / (ah + bh)
    )
    cp2 = (ah**2 + qh**2) * (1 + K * qh**2) / qh**2
    Pplus = (1 - K * ah**2) * (1 + K * ah) / (1 - K * ah)
    ebar = (1 - K) * (bh**2 - ah**2) / (
        (1 - K**2 * bh**2) * (1 - K * ah**2)
    )
    assert sp.limit(Knew, h, 0) == sp.Rational(1, 2)
    assert sp.limit(cp2, h, 0) == 1
    assert sp.limit(Pplus, h, 0) == 1
    assert sp.simplify(sp.limit(ebar / h**3, h, 0) - 2 * c**2 * alpha) == 0

    A0 = sp.simplify(kappa * c + W0lim)
    A1 = 2 * kappa * c
    nlims = [
        c * R * A0,
        2 * c * R * (2 * A0 + A1) / 3,
        c * R * (A0 + 2 * A1),
        4 * c * R * A1,
    ]
    rho_lims = [sp.factor(2 * x) for x in nlims]

    # Substitute the retained boundary margin R>0.  All coefficients in
    # (kappa,R) must be nonnegative; this is the exact sign certificate.
    Rsym = sp.symbols("R", positive=True)
    alpha_from_R = 2 / c - 2 * c**2 * kappa - Rsym
    certified = [
        sp.factor(expr.subs(alpha, alpha_from_R).subs(R, Rsym))
        for expr in rho_lims
    ]
    expected = [
        4 * c**2 * kappa * Rsym + Rsym**2,
        8 * c**2 * kappa * Rsym + sp.Rational(4, 3) * Rsym**2,
        12 * c**2 * kappa * Rsym + Rsym**2,
        16 * c**2 * kappa * Rsym,
    ]
    assert all(sp.simplify(x - y) == 0 for x, y in zip(certified, expected))
    assert all(
        all(coef >= 0 for coef in sp.Poly(expr, kappa, Rsym).coeffs())
        for expr in certified
    )

    return {
        "status": "RIGOROUS_PARTIAL_RESULT",
        "result": "PASS",
        "exact_rb_formula": str(rb_stable),
        "retained_chart_margin_R": str(R),
        "limits_rho_over_h2": [str(x) for x in certified],
        "base_limit_g_Knew_cp4": "1/2",
        "checks": {
            "tangent_elimination": True,
            "u_v_compactification": True,
            "low_corner_series": True,
            "four_nonnegative_leading_polynomials": True,
            "floating_sign_tests": 0,
        },
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
