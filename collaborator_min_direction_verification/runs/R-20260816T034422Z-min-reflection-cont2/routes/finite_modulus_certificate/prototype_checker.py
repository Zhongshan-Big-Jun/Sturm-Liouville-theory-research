"""Bounded Arb prototype for the exact C2-E compensating chart.

This checker evaluates exact h-regularized R17 ratios on a finite rational
box.  It is intentionally bounded and performs no recursive subdivision.
"""
from __future__ import annotations

import json
import argparse
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT / "tmp/r12-flint312"))
from flint import arb, ctx  # noqa: E402

ctx.prec = 256


def ball(lo: int, hi: int, bits: int) -> arb:
    return arb((lo + hi, -bits - 1), (hi - lo, -bits - 1))


def interval(lo: arb, hi: arb) -> arb:
    return lo.union(hi)


def upper(x: arb) -> arb:
    return x.upper()


def lower(x: arb) -> arb:
    return x.lower()


def evaluate(h: arb, kap: arb, beta: arb) -> dict:
    one, two, pi = arb(1), arb(2), arb.pi()
    c = pi / two
    K = kap * h
    # K is known nonnegative from the exact parameter box; raw ball
    # multiplication can acquire a tiny negative rounding tail at zero.
    k = interval(arb(0), upper(K).sqrt())
    z = c - h
    eta = h * (one + beta * h)
    theta = c + eta

    kz, kth = k * z, k * theta
    fh = h.sinc() / h.cos()                 # tan(h)/h
    fe = eta.sinc() / eta.cos()             # tan(eta)/eta
    geta = (one + beta * h) * fe
    q = z * kz.sinc() / kz.cos()            # tan(kz)/k
    sig = theta * kth.sinc() / kth.cos()    # tan(k theta)/k
    A = q * fh                              # a/h
    B = sig * geta                          # b/h

    # Exact mean-value enclosures for the two divided differences.
    xmax = interval(eta, h)
    dd_f_hi = xmax.tan() / (xmax.cos() ** 2)
    dd_f = interval(arb(0), upper(dd_f_hi))
    E = (-beta) * (fe + h * dd_f)           # [fh-geta]/h

    sec_z = one / (kz.cos() ** 2)
    sec_t = one / (kth.cos() ** 2)
    dd_q = interval(lower(sec_z), upper(sec_t))
    qdiff = (two + beta * h) * dd_q         # [sigma-q]/h

    u = A / B
    alpha = (qdiff * geta - q * E) / B      # (1-u)/h
    J = u * (
        h / (theta * kth.sinc() * kth.cos())
        + one / ((one + beta * h) * eta.sinc() * eta.cos())
    )

    Dhat = B * (one + kap * h**3 * A * B) + kap * h * (A + B) * sig**2
    Nrh = (
        q * sig * E
        - kap * h**2 * A * B**2 * (sig + q)
        - q * kap * (A + B) * sig**2
    )
    S = Nrh / (q * Dhat)                    # (rB-1)/h
    rb = one + h * S

    sd = (two * kz).sinc() - (two * z).sinc()
    xden = z.sin() * kz.cos() * (
        z.sinc() * kz.cos() - K * kz.sinc() * z.cos()
    )
    Xbar = sd / xden

    W0s = (one - kap * h**3 * A**2) * (
        q * sig * E + kap * h * A * B * (q + sig)
    ) / (q * sig * (A + B) * (one - kap * h**2 * A))
    bracket = h**2 * B**2 + h * B + sig**2 + kap * h**2 * B * sig**2
    W1s = kap * A * (one - kap * h**3 * A**2) * bracket / (
        q * (one - kap * h**2 * A) * Dhat
    )
    U0s, U1s = kap * Xbar + W0s, kap * Xbar + W1s

    ebar = (one - K) * h**2 * (B**2 - A**2) / (
        (one - kap**2 * h**4 * B**2) * (one - kap * h**3 * A**2)
    )
    g = one - K * ebar
    H0 = Xbar + ebar * h * W0s
    H1 = Xbar + ebar * h * W1s
    L0 = two * H0 + ebar * h * U0s
    L1 = two * H1 + ebar * h * U1s

    Deltas = S * (rb + one)                 # (rB^2-1)/h
    N = (
        S * U0s * L0 / two,
        (two * S * (U1s * L0 + U0s * L1) + Deltas * U0s * L0) / 6,
        (two * S * U1s * L1 + Deltas * (U1s * L0 + U0s * L1)) / 4,
        Deltas * U1s * L1,
    )                                       # Nhat_i/h^2

    a = h * A
    b = h * B
    cp2 = (a**2 + q**2) * (one + K * q**2) / q**2
    Pplus = (one - K * a**2) * (one + K * a) / (one - K * a)
    Knew = (one - kap*h**3*A**2) / ((h**2*A**2 + q**2) * (one + K * q**2)) * (
        h**2*A**2 * (one - K) / (one - kap*h**2*A) ** 2
        + q**2 * B * (one + kap*h**2*A) / (A + B)
    )
    rho = tuple(Pplus * n / (g * Knew * cp2**2) for n in N)

    R = 4 / pi - alpha - pi**2 * kap / two
    R0 = -beta - pi**2 * kap / two
    Plead = (
        R0 * (R0 + pi**2 * kap),
        two * R0 * (two * R0 + 3 * pi**2 * kap) / 3,
        R0 * (R0 + 3 * pi**2 * kap),
        4 * pi**2 * R0 * kap,
    )
    return {
        "b-a_scaled": B-A,
        "S": S,
        "J": J,
        "alpha": alpha,
        "R": R,
        "R0": R0,
        "base": g*Knew*cp2**2,
        "rho_norm": rho,
        "Plead": Plead,
        "diff": tuple(x-y for x,y in zip(rho,Plead)),
    }


def main() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hbits", type=int, default=16)
    args = parser.parse_args()
    # One deliberately finite tensor grid; h includes the exact boundary.
    h = ball(0, 1, args.hbits)
    KBITS, BBITS = 6, 6
    # 0 <= kappa <= 3/8, -3/2 <= beta <= 0.
    min_j = 10**9
    max_rho = [None]*4
    max_diff = [None]*4
    retained_boxes = discarded = failures = 0
    for ik in range(24):
        kap = ball(ik, ik+1, KBITS)       # 24/64=3/8
        for ib in range(-96, 0):
            beta = ball(ib, ib+1, BBITS)
            try:
                out = evaluate(h, kap, beta)
                if upper(out["b-a_scaled"]) <= 0 or upper(out["S"]) <= 0:
                    discarded += 1
                    continue
                retained_boxes += 1
                assert out["J"] > arb(999)/1000
                jl = float(lower(out["J"]))
                min_j = min(min_j, jl)
                for i,x in enumerate(out["rho_norm"]):
                    assert x < 5
                    xu = float(upper(x))
                    max_rho[i] = xu if max_rho[i] is None else max(max_rho[i],xu)
                for i,x in enumerate(out["diff"]):
                    au = max(abs(float(lower(x))),abs(float(upper(x))))
                    max_diff[i] = au if max_diff[i] is None else max(max_diff[i],au)
            except Exception:
                failures += 1
    return {
        "status": "FINITE_COMPUTATIONAL_RESULT",
        "scope": {"h":f"[0,2^-{args.hbits}]","kappa":"[0,3/8]","beta":"[-3/2,0]"},
        "grid": {"kappa_cells":24,"beta_cells":96,"total":2304},
        "retained_or_unresolved_boxes":retained_boxes,
        "discarded_boxes":discarded,
        "failures":failures,
        "min_J_lower":min_j,
        "max_rho_norm_upper":max_rho,
        "max_abs_diff_upper":max_diff,
        "certified_rational_bounds": {"J_lower":"999/1000","rho_i_over_h2_upper":"5"},
    }


if __name__ == "__main__":
    print(json.dumps(main(),indent=2))
