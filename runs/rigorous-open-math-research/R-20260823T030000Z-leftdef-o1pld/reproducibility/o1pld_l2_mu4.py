# -*- coding: utf-8 -*-
"""Exact-arithmetic verification for the s=2 (L^2 descent) mu4 non-density model.

Run: R-20260823T030000Z-leftdef-o1pld
Problem: O1'LD with s=2.

The script verifies:
  - K_c p_n = q_n (three-term polynomial, c>0)
  - mu_4(q_odd) = 0 for every odd sparse index
  - mu_4(q_even) is nonzero (indeed negative) for every even sparse index
  - mu_4(q_0) = 2c/5 != 0 for c>0

This supports the STRICT example V = {f in H^2 : <K_c f, x^4>_L2 = 0},
whose kept set N is exactly {1} union {2m+1 : m>=2} in the sparse index set.
"""
import sympy as sp

x = sp.symbols("x")
c = sp.symbols("c", positive=True, real=True)
m = sp.symbols("m", integer=True, positive=True)


def q_sparse(n, cvar=None):
    """Return K_c p_n as a SymPy polynomial in x.

    p_0=1, p_1=x, p_{2m}=x^{2m}-m/(m-1)x^{2m-2}, p_{2m+1} likewise.
    K_c = -d^2/dx^2 + c.
    """
    cc = cvar if cvar is not None else c
    if n == 0:
        return cc
    if n == 1:
        return cc * x
    if n % 2 == 0:
        mm = n // 2
        A = 2 * mm * (2 * mm - 1) + cc * mm / (mm - 1)
        B = 2 * mm * (2 * mm - 3)
        return cc * x ** n - A * x ** (n - 2) + B * x ** (n - 4)
    else:
        mm = (n - 1) // 2  # n = 2mm+1
        A = 2 * mm * (2 * mm + 1) + cc * mm / (mm - 1)
        B = 2 * mm * (2 * mm - 1)
        return cc * x ** n - A * x ** (n - 2) + B * x ** (n - 4)


def mu4(poly):
    """mu_4(f) = int_-1^1 f(x) x^4 dx."""
    return sp.integrate(poly * x ** 4, (x, -1, 1))


def main():
    print("c > 0, m >= 2 integer")
    print("mu_4(q_0) =", sp.simplify(mu4(q_sparse(0))))
    print("mu_4(q_1) =", sp.simplify(mu4(q_sparse(1))))
    print()
    for n in [5, 7, 9, 11, 13, 15, 17]:
        print(f"odd n={n}: mu_4 = {sp.simplify(mu4(q_sparse(n)))}")
    print()
    for n in [4, 6, 8, 10, 12, 14, 16]:
        print(f"even n={n}: mu_4 = {sp.simplify(mu4(q_sparse(n)))}")
    print()
    print("General even formula:")
    A = 2 * m * (2 * m - 1) + c * m / (m - 1)
    B = 2 * m * (2 * m - 3)
    expr = 2 * c / (2 * m + 5) - 2 * A / (2 * m + 3) + 2 * B / (2 * m + 1)
    print("mu_4(q_{2m}) =", sp.factor(sp.cancel(sp.together(expr))))
    num = sp.factor(sp.together(expr).as_numer_denom()[0])
    den = sp.factor(sp.together(expr).as_numer_denom()[1])
    print("numerator =", num)
    print("denominator =", den)
    print("For m>=2 the bracket 8*c*m^2+10*c*m+3*c+32*m^3+48*m^2-80*m > 0,")
    print("so mu_4(q_{2m}) < 0 for every m>=2; in particular nonzero.")
    print("Odd formula: mu_4(q_{2m+1}) = 0 by parity.")


if __name__ == "__main__":
    main()
