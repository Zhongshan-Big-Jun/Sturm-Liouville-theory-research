#!/usr/bin/env python3
"""Independent direct-formula check of the first blow-up endpoint.

Unlike finite_r_replay.py, this file does not use the bound series builder.
It re-encodes the exact formulas in scripts/_gapn2_largeR_closed.py and uses
staged Taylor arithmetic on those formulas, independently of the repository's
series builder.  Agreement is an implementation-level cross-check, while the
mathematical proof uses analyticity and the displayed exact coefficients.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import mpmath as mp
import sympy as sp


ROOT = Path(__file__).resolve().parents[6]
CLOSED = ROOT / "scripts/_gapn2_largeR_closed.py"
EXPECTED = "e357d8e447ce998020c8dadc94eb27db884dd85932d592a9b4331366f8ac13a4"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    observed = digest(CLOSED)
    if observed != EXPECTED:
        raise RuntimeError(f"closed source hash mismatch: {observed}")

    u = sp.symbols("u", positive=True)
    K = sp.symbols("K", positive=True)
    D, B, C = sp.symbols("D B C", real=True)
    eps = u**3
    A = (2 + u**2 * D) / K
    k2 = K * u
    k3 = K * u + C * u**5
    p1 = sp.pi / 2 + A * u**2
    p3 = sp.pi / 4 + B * u**2
    fac = 1 + C * u**4 / K
    p1t = p1 * fac
    p3t = p3 * fac
    p2 = k2 / 2 - eps * (p1 + p3)
    p2t = k3 / 2 - eps * fac * (p1 + p3)

    def T(expression, order=11):
        return sp.expand(sp.series(expression, u, 0, order).removeO())

    # Expand atomic analytic factors once.  All later operations are exact
    # Laurent-polynomial arithmetic, avoiding a monolithic expression tree.
    sp1, cp1 = T(sp.sin(p1)), T(sp.cos(p1))
    sp3, cp3 = T(sp.sin(p3)), T(sp.cos(p3))
    sp1t, cp1t = T(sp.sin(p1t)), T(sp.cos(p1t))
    sp3t, cp3t = T(sp.sin(p3t)), T(sp.cos(p3t))
    sp2, cp2 = T(sp.sin(p2)), T(sp.cos(p2))
    sp2t, cp2t = T(sp.sin(p2t)), T(sp.cos(p2t))
    sin_p1p3 = T(sp.sin(p1 + p3))

    E1 = T(cp2 * sin_p1p3 + sp2 * cp3 * cp1 / eps
           - eps * sp3 * sp2 * sp1, 5)
    E2 = T(cp2t * cp1t * cp3t - sp3t * sp2t * cp1t / eps
           - sp3t * cp2t * sp1t - eps * cp3t * sp2t * sp1t, 5)

    inv_sp3 = T(1 / sp3)
    inv_cp3t = T(1 / cp3t)
    qD = T(eps * cp2 * sp1 / k2 + sp2 * cp1 / k2)
    qN = T(eps * cp2t * sp1t / k3 + sp2t * cp1t / k3)
    bcD = T(-qD * inv_sp3)
    bcN = T(qN * inv_cp3t)
    m1D = T((p1 - T(sp.sin(2 * p1)) / 2) * eps / (2 * k2**3), 7)
    m1N = T((p1t - T(sp.sin(2 * p1t)) / 2) * eps / (2 * k3**3), 7)
    m3D = T(bcD**2 * (p3 - T(sp.sin(2 * p3)) / 2) / (2 * k2 * eps), 7)
    m3N = T(bcN**2 * (p3t + T(sp.sin(2 * p3t)) / 2) / (2 * k3 * eps), 7)
    aaD, bbD = T(eps * sp1 / k2), T(cp1 / k2)
    aaN, bbN = T(eps * sp1t / k3), T(cp1t / k3)
    mLD = T((aaD**2 + bbD**2) * p2 / (2 * k2)
            + (aaD**2 - bbD**2) * T(sp.sin(2 * p2)) / (4 * k2)
            + aaD * bbD * (1 - T(sp.cos(2 * p2))) / (2 * k2), 7)
    mLN = T((aaN**2 + bbN**2) * p2t / (2 * k3)
            + (aaN**2 - bbN**2) * T(sp.sin(2 * p2t)) / (4 * k3)
            + aaN * bbN * (1 - T(sp.cos(2 * p2t))) / (2 * k3), 7)
    ID, IN = T(m1D + m3D + mLD, 7), T(m1N + m3N + mLN, 7)
    E5 = T(ID * sp1t**2 - IN * sp1**2, 7)
    E6 = T(sp1 * (eps * cp2t + sp2t * cp1t * T(1 / sp1t))
           + eps * cp2 * sp1 + sp2 * cp1, 8)

    values = {
        "E1/u2": sp.factor(E1.coeff(u, 2)),
        "E2/u2": sp.factor(E2.coeff(u, 2)),
        "E5/u4": sp.factor(E5.coeff(u, 4)),
        "E6/u5": sp.factor(E6.coeff(u, 5)),
    }
    for name, coefficient in values.items():
        print(name, "=", sp.sstr(coefficient))

    seed = {
        C: 16 / (sp.pi * K),
        D: -(K**3 - 18 * sp.pi + 24) / (6 * K),
    }
    print("AFTER_E1_E2_RELATIONS")
    for name, value in values.items():
        print(name, "=", sp.sstr(sp.factor(value.subs(seed))))
    e5_u5 = sp.factor(E5.coeff(u, 5))
    print("E5_U5_FIXED_D_C =", sp.sstr(e5_u5))
    print("E5_U5_AFTER_SEED_RELATIONS =", sp.sstr(sp.factor(e5_u5.subs(seed))))

    d, c = sp.symbols("d c", real=True)
    next_endpoint = {
        "E1/u3": sp.factor(values["E1/u2"].diff(D) * d
                            + values["E1/u2"].diff(C) * c),
        "E2/u3": sp.factor(values["E2/u2"].diff(D) * d
                            + values["E2/u2"].diff(C) * c),
        "E5/u5": sp.factor(values["E5/u4"].diff(D) * d
                            + values["E5/u4"].diff(C) * c + e5_u5),
        "E6/u6": sp.factor(values["E6/u5"].diff(D) * d
                            + values["E6/u5"].diff(C) * c),
    }
    print("SECOND_BLOWUP_D_EQ_D0_PLUS_Ud_C_EQ_C0_PLUS_Uc")
    for name, value in next_endpoint.items():
        print(name, "=", sp.sstr(sp.factor(value.subs(seed))))

    e1_u4 = sp.factor(E1.coeff(u, 4))
    e2_u4 = sp.factor(E2.coeff(u, 4))
    e5_u6 = sp.factor(E5.coeff(u, 6))
    e6_u7 = sp.factor(E6.coeff(u, 7))
    d2, c2 = sp.symbols("d2 c2", real=True)
    third_endpoint = {
        "E1/u4": sp.factor((values["E1/u2"].diff(D) * d2
                             + values["E1/u2"].diff(C) * c2 + e1_u4).subs(seed)),
        "E2/u4": sp.factor((values["E2/u2"].diff(D) * d2
                             + values["E2/u2"].diff(C) * c2 + e2_u4).subs(seed)),
        "E5/u6": sp.factor((values["E5/u4"].diff(D) * d2
                             + values["E5/u4"].diff(C) * c2 + e5_u6).subs(seed)),
        "E6/u7": sp.factor((values["E6/u5"].diff(D) * d2
                             + values["E6/u5"].diff(C) * c2 + e6_u7).subs(seed)),
    }
    print("THIRD_BLOWUP_D_EQ_D0_PLUS_U2d2_C_EQ_C0_PLUS_U2c2")
    for name, value in third_endpoint.items():
        print(name, "=", sp.sstr(value))
    linear_solution = sp.solve(
        [third_endpoint["E1/u4"], third_endpoint["E2/u4"]],
        [d2, c2], dict=True, simplify=True,
    )
    print("THIRD_BLOWUP_LINEAR_SOLUTION")
    print(sp.sstr(linear_solution))
    if len(linear_solution) == 1:
        reduced5 = sp.factor(third_endpoint["E5/u6"].subs(linear_solution[0]))
        reduced6 = sp.factor(third_endpoint["E6/u7"].subs(linear_solution[0]))
        print("THIRD_BLOWUP_REDUCED_E5 =", sp.sstr(reduced5))
        print("THIRD_BLOWUP_REDUCED_E6 =", sp.sstr(reduced6))
        n5, _ = sp.cancel(reduced5).as_numer_denom()
        n6, _ = sp.cancel(reduced6).as_numer_denom()
        resultant = sp.factor(sp.resultant(n5, n6, B))
        print("THIRD_BLOWUP_RESULTANT_IN_K =", sp.sstr(resultant))
        kpoly = sp.pi * K**3 - 18 * sp.pi**2 + 48
        bseed = 1 / K
        d2seed = sp.factor(linear_solution[0][d2].subs(B, bseed))
        c2seed = sp.factor(linear_solution[0][c2])
        seed3 = {B: bseed, d2: d2seed, c2: c2seed}
        print("THIRD_BLOWUP_EXACT_SEED")
        print("K_positive_root_of =", sp.sstr(kpoly))
        print("B =", sp.sstr(bseed))
        print("d2 =", sp.sstr(d2seed))
        print("c2 =", sp.sstr(c2seed))
        jac3 = sp.Matrix(list(third_endpoint.values())).jacobian([K, B, d2, c2])
        det3 = sp.factor(jac3.det())
        det3_seed = sp.factor(det3.subs(seed3))
        det_num, det_den = sp.cancel(det3_seed).as_numer_denom()
        det_num_reduced = sp.factor(sp.rem(sp.Poly(det_num, K), sp.Poly(kpoly, K)).as_expr())
        print("THIRD_BLOWUP_JACOBIAN_DET =", sp.sstr(det3))
        print("THIRD_BLOWUP_JACOBIAN_DET_AT_SEED =", sp.sstr(det3_seed))
        print("THIRD_BLOWUP_JACOBIAN_NUM_REDUCED_MOD_KPOLY =", sp.sstr(det_num_reduced))
        kvalue = sp.real_root(18 * sp.pi - 48 / sp.pi, 3)
        print("THIRD_BLOWUP_SEED_APPROX")
        print("K =", sp.N(kvalue, 30))
        print("B =", sp.N(bseed.subs(K, kvalue), 30))
        print("D0 =", sp.N(seed[D].subs(K, kvalue), 30))
        print("C0 =", sp.N(seed[C].subs(K, kvalue), 30))
        print("d2 =", sp.N(d2seed.subs(K, kvalue), 30))
        print("c2 =", sp.N(c2seed.subs(K, kvalue), 30))
        print("detJ =", sp.N(det3_seed.subs(K, kvalue), 30))

        # Half-interval nodal correspondence.  qD and qN are the values at
        # the inner/central interface of the low-block solutions that start
        # positive at the outer/low interface.  Their leading signs decide
        # whether the low block contains zero or one crossing.
        coordinate3 = {
            D: seed[D] + u**2 * d2,
            C: seed[C] + u**2 * c2,
        }
        qD_seed = T(qD.subs(coordinate3).subs(seed3), 10)
        qN_seed = T(qN.subs(coordinate3).subs(seed3), 10)

        def reduced_coefficient(expression, degree):
            value = sp.factor(expression.coeff(u, degree))
            num, den = sp.cancel(value).as_numer_denom()
            reduced_num = sp.factor(sp.rem(sp.Poly(num, K), sp.Poly(kpoly, K)).as_expr())
            return sp.factor(reduced_num / den)

        print("HALF_INTERVAL_ENDPOINT_VALUE_COEFFICIENTS_MOD_KPOLY")
        for label, expression in (("qD", qD_seed), ("qN", qN_seed)):
            printed = 0
            for degree in range(10):
                coefficient = reduced_coefficient(expression, degree)
                if coefficient != 0:
                    print(label, "leading_degree", degree, "coefficient", sp.sstr(coefficient))
                    printed = 1
                    break
            if not printed:
                print(label, "no_nonzero_coefficient_below_10")

    # High-precision check against the unexpanded exact mass formulas.  This
    # is not used as proof; it detects truncation mistakes in either symbolic
    # implementation.  If the endpoint coefficient is zero, E5/u^4 must tend
    # to zero rather than to a nonzero constant.
    mp.mp.dps = 100

    def numeric_mass(k, q1, q2, q3, e, mode):
        if mode == "D":
            bc = -(e * mp.cos(q2) * mp.sin(q1) / k
                   + mp.sin(q2) * mp.cos(q1) / k) / mp.sin(q3)
            m3 = bc**2 * (q3 - mp.sin(2 * q3) / 2) / (2 * k * e)
        else:
            bc = (e * mp.cos(q2) * mp.sin(q1) / k
                  + mp.sin(q2) * mp.cos(q1) / k) / mp.cos(q3)
            m3 = bc**2 * (q3 + mp.sin(2 * q3) / 2) / (2 * k * e)
        m1 = (q1 - mp.sin(2 * q1) / 2) * e / (2 * k**3)
        aaa, bbb = e * mp.sin(q1) / k, mp.cos(q1) / k
        ml = ((aaa**2 + bbb**2) * q2 / (2 * k)
              + (aaa**2 - bbb**2) * mp.sin(2 * q2) / (4 * k)
              + aaa * bbb * (1 - mp.cos(2 * q2)) / (2 * k))
        return m1 + m3 + ml

    kval = mp.mpf(3)
    bval = mp.mpf(1) / 5
    cval = 16 / (mp.pi * kval)
    dval = -(kval**3 - 18 * mp.pi + 24) / (6 * kval)
    print("DIRECT_NUMERIC_E5_OVER_U4_K3_B1OVER5")
    for uval in (mp.mpf(1) / 20, mp.mpf(1) / 40, mp.mpf(1) / 80,
                 mp.mpf(1) / 160):
        eval_ = uval**3
        aval = (2 + uval**2 * dval) / kval
        k2v = kval * uval
        k3v = kval * uval + cval * uval**5
        p1v = mp.pi / 2 + aval * uval**2
        p3v = mp.pi / 4 + bval * uval**2
        facv = 1 + cval * uval**4 / kval
        p1tv, p3tv = p1v * facv, p3v * facv
        p2v = k2v / 2 - eval_ * (p1v + p3v)
        p2tv = k3v / 2 - eval_ * facv * (p1v + p3v)
        idv = numeric_mass(k2v, p1v, p2v, p3v, eval_, "D")
        inv = numeric_mass(k3v, p1tv, p2tv, p3tv, eval_, "N")
        e5v = idv * mp.sin(p1tv)**2 - inv * mp.sin(p1v)**2
        print(mp.nstr(uval, 8), mp.nstr(e5v / uval**4, 40))


if __name__ == "__main__":
    main()
