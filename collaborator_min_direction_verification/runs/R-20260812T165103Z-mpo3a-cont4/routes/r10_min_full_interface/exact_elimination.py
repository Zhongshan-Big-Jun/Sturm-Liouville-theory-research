#!/usr/bin/env python3
"""NONPROPAGATING exact algebra for the min n=2 full-interface route.

The script does not certify the target inequality.  It checks the rational
parameterization of two completely glued adjacent cells at mu=2 and emits
the first unresolved numerator polynomial for one split response.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def trig_half(x):
    return (1 - x * x) / (1 + x * x), 2 * x / (1 + x * x)


def cell_pair(x):
    c, s = trig_half(x)
    high = 2 * x / (1 - x * x)
    C, S = trig_half(high)
    return c, s, C, S


def main() -> int:
    t, u, r = sp.symbols("t u r", positive=True)
    mu = sp.Integer(2)
    c1, s1, C1, S1 = cell_pair(t)
    c2, s2, C2, S2 = cell_pair(u)

    # State at the first interface is normalized to U=1.  In material-one
    # time, write its slopes as p=U_s and v=V_s.  Full U,V momentum matching
    # and the two opposite-label endpoint equations give the following
    # unique rational solution (away from the displayed compatibility pole).
    determinant = sp.factor(s1 * S2 - s2 * S1)
    p = sp.factor(((c1 + C1) * S2 + r * (c2 + C2) * S1) / determinant)
    v = sp.factor((s1 * r * (c2 + C2) + s2 * (c1 + C1)) / determinant)

    # Back-propagation through cell 1: its right state is (U,p,V_s)=(1,p,v).
    # The left state therefore has U=u1=c1-s1*p and V_s=-S1+C1*v.
    u1 = sp.factor(c1 - s1 * p)
    u3 = sp.factor(c2 + s2 * p / r)
    z1 = sp.factor(1 / u1)
    z2 = sp.factor(u3)

    # Reconstruct both interfaces exactly.  Cell 1 begins at label + and
    # ends at label -, while cell 2 begins at label - and ends at label +.
    p_left = sp.factor(s1 + c1 * p)
    v_left = sp.factor(-S1 + C1 * v)
    p_right = sp.factor(-r * s2 + c2 * p)
    v_right = sp.factor(r * S2 + C2 * v)
    checks = {
        "cell1_left_label": sp.factor(c1 + C1 - s1 * p + S1 * v),
        "cell1_right_label": sp.factor(c1 * u1 + s1 * p - 1),
        "cell2_left_label": sp.factor(-1 + 1),
        "cell2_right_label": sp.factor(C2 + S2 * v / r + u3),
        "U_momentum_interface": sp.factor(p - p),
        "V_momentum_interface": sp.factor(v - v),
        "cell1_propagated_U_s": sp.factor(p_left - p),
        "cell1_propagated_V_s": sp.factor(v_left - v),
        "cell2_propagated_U_s": sp.factor(p_right - p_right),
        "cell2_propagated_V_s": sp.factor(v_right - v_right),
    }
    # The left-label check above is more transparently obtained from the
    # oscillator equation used to solve p,v.  Verify the two actual endpoint
    # equations directly instead of relying on mnemonic labels.
    eq1 = sp.factor(s1 * p - S1 * v - (c1 + C1))
    eq2 = sp.factor(-s2 * p + S2 * v - r * (c2 + C2))
    assert eq1 == 0 and eq2 == 0

    delta = r * r - 1
    gamma1 = sp.factor((p_left - mu * v_left) / u1)
    gamma2 = sp.factor(-(p + mu * v))
    gamma3 = sp.factor((p_right - mu * v_right) / u3)
    Q1 = s1 + mu * S1
    Q2 = s2 + mu * S2
    a1 = sp.factor(delta * u1 * u1 / gamma1)
    a2 = sp.factor(delta / gamma2)
    K1 = sp.factor(Q1 / u1)
    K2 = sp.factor(Q2 / (r * u3))
    beta_R = sp.cancel((1 + a1 * K1) / (a1 + a2 + a1 * a2 * K1))

    # The numerically suggested split is beta_R > |K2|*(-gamma_at_event_2)
    # /(gamma_at_event_3-gamma_at_event_2).  This is sufficient but not
    # necessary for H>0.  Full two-cell gluing reduces it to this exact
    # rational function.  Its numerator is the first currently unproved
    # polynomial inequality on the admissible domain.
    split_target = sp.cancel((-K2) * gamma2 / (gamma2 + gamma3))
    split_gap = sp.cancel(beta_R - split_target)
    numerator, denominator = map(sp.factor, sp.fraction(split_gap))

    payload = {
        "status": "NONPROPAGATING_EXACT_REDUCTION",
        "specialization": {"mu": 2},
        "variables": {
            "t": "tan(theta_1/2)",
            "u": "tan(theta_2/2)",
            "r": "sqrt(R)",
        },
        "p": str(p),
        "v": str(v),
        "z1": str(z1),
        "z2": str(z2),
        "endpoint_equations": [str(eq1), str(eq2)],
        "split_gap_numerator": str(numerator),
        "split_gap_denominator": str(denominator),
        "degrees": {
            "numerator_total": int(sp.Poly(numerator, t, u, r).total_degree()),
            "numerator_t": int(sp.degree(numerator, t)),
            "numerator_u": int(sp.degree(numerator, u)),
            "numerator_r": int(sp.degree(numerator, r)),
        },
        "factor_list": [
            [str(base), int(power)]
            for base, power in sp.factor_list(numerator)[1]
        ],
        "limitation": (
            "This is a sufficient split inequality for the left block, not "
            "the full H inequality; no sign certificate is claimed."
        ),
    }
    output = HERE / "exact_elimination.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(json.dumps({"output": str(output), "sha256": digest, **payload["degrees"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
