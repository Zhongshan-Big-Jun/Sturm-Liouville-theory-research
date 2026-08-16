"""Exact SymPy checks for the R9 n=2 dual-Schur reduction.

This script performs identities over rational-function fields.  Its final
example refutes only a deliberately relaxed proof mechanism; it is not a
physical relay counterexample because the full momentum interface equations
are displayed as nonzero.
"""

from __future__ import annotations

import sympy as sp


def cell_data(mu, t, z):
    """Half-angle cell data, with T=tan(mu*theta/2) supplied algebraically."""
    if mu != 2:
        raise ValueError("the exact rational specialization uses mu=2")
    big_t = 2 * t / (1 - t * t)
    cosine = (1 - t * t) / (1 + t * t)
    sine = 2 * t / (1 + t * t)
    high_cosine = (1 - big_t * big_t) / (1 + big_t * big_t)
    high_sine = 2 * big_t / (1 + big_t * big_t)
    denominator = mu * big_t**2 * t + big_t * t**2 + big_t + mu * t
    threshold = sp.factor(
        (mu * big_t**2 * t - big_t * t**2 + big_t - mu * t) / denominator
    )
    prefactor = sp.factor(denominator / (2 * big_t * t))
    q_value = sp.factor(sine + mu * high_sine)
    x_left = sp.factor((z - cosine) / sine)
    y_left = sp.factor((-z - high_cosine) / high_sine)
    x_right = sp.factor((cosine * z - 1) / (sine * z))
    y_right = sp.factor((1 + high_cosine * z) / (high_sine * z))
    g_value = sp.factor(x_left - mu * y_left)
    h_value = sp.factor(-x_right + mu * y_right)
    assert sp.factor(g_value - prefactor * (z - threshold)) == 0
    assert sp.factor(h_value - prefactor * (1 - threshold * z) / z) == 0
    return {
        "A": prefactor, "k": threshold, "Q": q_value,
        "g": g_value, "h": h_value,
        "x": x_left, "y": y_left, "xR": x_right, "yR": y_right,
    }


def normalized_positive_block(delta, z, data):
    """Return u^2 times the entries of the positive-cell P-block inverse."""
    g_value, h_value, q_value = data["g"], data["h"], data["Q"]
    common = delta * z * q_value + h_value + z * z * g_value
    left = sp.factor(g_value * (delta * z * q_value + h_value) / (delta * common))
    right = sp.factor(
        h_value * (delta * q_value + z * g_value) / (delta * z * common)
    )
    off = sp.factor(g_value * h_value / (delta * common))

    a_left = delta / g_value
    a_right = delta * z * z / h_value
    compliance = z / q_value
    determinant = a_left * a_right + compliance * (a_left + a_right)
    assert sp.factor(left - (a_right + compliance) / determinant) == 0
    assert sp.factor(right - (a_left + compliance) / determinant) == 0
    assert sp.factor(off - compliance / determinant) == 0
    return left, right, off


def exact_relaxed_counterexample():
    mu = sp.Integer(2)
    t1, t2, t3 = sp.Rational(1, 5), sp.Rational(49, 50), sp.Rational(1, 50)
    middle_abs_ratio = sp.Rational(1, 100)
    root_r = sp.Rational(6, 5)
    delta = root_r**2 - 1

    # First obtain A,k,Q without fixing the positive-cell amplitude ratios.
    dummy = sp.Integer(1)
    raw1, raw2, raw3 = (cell_data(mu, t, dummy) for t in (t1, t2, t3))
    a1, k1 = raw1["A"], raw1["k"]
    a2, k2 = raw2["A"], raw2["k"]
    a3, k3 = raw3["A"], raw3["k"]

    # The middle ratio is z_2=-b.  Match only the physical switch derivative
    # gamma=x-mu*y at both material interfaces.
    middle_left = a2 * (middle_abs_ratio + k2)
    middle_right = a2 * (1 + k2 * middle_abs_ratio) / middle_abs_ratio
    z1 = sp.factor(1 / (k1 + root_r * middle_left / a1))
    z3 = sp.factor(k3 + root_r * middle_right / a3)

    data1 = cell_data(mu, t1, z1)
    data2 = cell_data(mu, t2, -middle_abs_ratio)
    data3 = cell_data(mu, t3, z3)
    left1, right1, off1 = normalized_positive_block(delta, z1, data1)
    left3, right3, off3 = normalized_positive_block(delta, z3, data3)
    del left1, off1, right3, off3

    margin = sp.factor(
        z1**2 * right1
        + left3 / middle_abs_ratio**2
        - data2["Q"] / (root_r * middle_abs_ratio)
    )
    expected_margin = -sp.Rational(
        28631724371526853374269606961558602772691167786748224037432491186500,
        392256468455448162251149432130501665881941586956928806198562754029,
    )
    assert margin == expected_margin
    assert all(value > 0 for value in (
        z1 - k1, 1 / k1 - z1, z3 - k3, 1 / k3 - z3,
    ))

    # The retained gamma combination matches exactly, while the independent
    # low/high momentum conditions do not.  This certifies the scope defect.
    defect12_x = sp.factor(data2["x"] - data1["xR"] / root_r)
    defect12_y = sp.factor(data2["y"] - data1["yR"] / root_r)
    defect23_x = sp.factor(data3["x"] - root_r * data2["xR"])
    defect23_y = sp.factor(data3["y"] - root_r * data2["yR"])
    assert sp.factor(defect12_x - mu * defect12_y) == 0
    assert sp.factor(defect23_x - mu * defect23_y) == 0
    assert defect12_x == sp.Rational(119315789, 5390000)
    assert defect23_x == sp.Rational(785424183, 269500)
    return {
        "mu": mu, "sqrt_R": root_r,
        "half_angles": (t1, t2, t3),
        "amplitude_ratios": (z1, -middle_abs_ratio, z3),
        "dual_scalar": margin,
        "interface_defects_x": (defect12_x, defect23_x),
    }


if __name__ == "__main__":
    print(exact_relaxed_counterexample())
