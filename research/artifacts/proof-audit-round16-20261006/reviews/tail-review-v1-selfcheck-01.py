"""Independent exact Fourier checks plus isolated q_formula comparison.

This reads only the frozen variation.py q_formula AST for execution.  It does
not import the project, the frozen module, its dependencies, or a full CLI.
All proof-side calculations below use rational coefficients of pi**2.
"""
import ast
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(r"F:/tools/math-audit-round16-20261006/tail-review-v1")
OUT = Path(r"F:/tools/math-audit-round16-20261006/tail-review-v1-selfcheck-01.json")
raw = (ROOT / "variation.py").read_bytes()
source = raw.decode("utf-8")
tree = ast.parse(source)
q_node = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
              and node.name == "q_formula")
q_source = ast.get_source_segment(source, q_node)


def finite_vector(value, name):
    result = np.asarray(value, dtype=float)
    if result.ndim != 1 or not np.all(np.isfinite(result)):
        raise ValueError(name)
    return result


def positive_integer(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value <= 0:
        raise ValueError(name)
    return int(value)


scope = {"np": np, "math": math, "finite_vector": finite_vector,
         "positive_integer": positive_integer}
exec(compile(ast.Module(body=[q_node], type_ignores=[]),
             "frozen-variation-q_formula-only", "exec"), scope)
q_formula = scope["q_formula"]
records = []


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def alpha(k):
    return F(k * k, 2)  # lambda_k = pi**2 * alpha(k) for rho == 2.


def coeff(k, l, directions):
    # h = 2 sum_j d_j cos(j*pi*x), u_k = sin(k*pi*x).
    value = F(0)
    for j, d in directions.items():
        if j == 0:
            value += d * int(l == k)
            continue
        value += d / 2 * int(l == k + j)
        delta = k - j
        if delta:
            value += d / 2 * (1 if delta > 0 else -1) * int(l == abs(delta))
    return value


def energy(k, directions):
    # Direct cos-product integral of (h**2/rho) * sin(k*pi*x)**2.
    # Here j=0 is handled separately; mixed constant/cos integrals contribute
    # only the cos(2*k*pi*x) Fourier coefficient of sin**2.
    total = F(0)
    for p, dp in directions.items():
        for q, dq in directions.items():
            if p == 0 and q == 0:
                factor = F(1)
            elif p == 0 or q == 0:
                factor = -F(int(p + q == 2 * k), 2)
            else:
                factor = F(int(p == q), 2) - F(
                    int(p + q == 2 * k) + int(abs(p - q) == 2 * k), 4)
            total += dp * dq * factor
    return total


def q_coefficient(n, cutoff, directions):
    a, b = alpha(n), alpha(n + 1)
    ca, cb = coeff(n, n, directions), coeff(n + 1, n + 1, directions)
    sa = sum((coeff(n, l, directions) ** 2 / (alpha(l) - a)
              for l in range(1, cutoff + 1) if l != n), F(0))
    sb = sum((coeff(n + 1, l, directions) ** 2 / (alpha(l) - b)
              for l in range(1, cutoff + 1) if l != n + 1), F(0))
    return b * cb ** 2 - a * ca ** 2 + a ** 2 * sa - b ** 2 * sb


def run_case(label, n, cutoff, directions, sharp=False):
    support = n + 1 + max(directions)
    j_a, j_b = energy(n, directions), energy(n + 1, directions)
    full_a = sum((coeff(n, l, directions) ** 2 for l in range(1, support + 1)), F(0))
    full_b = sum((coeff(n + 1, l, directions) ** 2 for l in range(1, support + 1)), F(0))
    check(j_a == full_a and j_b == full_b, "Parseval direct integral mismatch")
    e_a = j_a - sum((coeff(n, l, directions) ** 2 for l in range(1, cutoff + 1)), F(0))
    e_b = j_b - sum((coeff(n + 1, l, directions) ** 2 for l in range(1, cutoff + 1)), F(0))
    check(e_a >= 0 and e_b >= 0, "negative exact residual")
    q_full = q_coefficient(n, max(support, cutoff), directions)
    q_n = q_coefficient(n, cutoff, directions)
    error = q_full - q_n
    lower = -alpha(n + 1) ** 2 * e_b / (alpha(cutoff + 1) - alpha(n + 1))
    upper = alpha(n) ** 2 * e_a / (alpha(cutoff + 1) - alpha(n))
    check(lower <= error <= upper, "two-sided bound mismatch")
    coarse_energy = sum((abs(d) for d in directions.values()), F(0)) ** 2
    check(j_a <= coarse_energy and j_b <= coarse_energy, "L-infinity energy mismatch")
    if sharp:
        expected = -F((n + 1) ** 4, 8 * (2 * n + 3))
        check(e_a == 0 and e_b == F(1, 4), "sharp residual mismatch")
        check(error == lower == expected, "left endpoint not sharp")
    if label == "constant_scaling":
        check(q_full == alpha(n + 1) - alpha(n), "scaling second derivative mismatch")
        check(error == 0 and e_a == 0 and e_b == 0, "scaling has a spurious tail")

    lam = np.array([float(alpha(l)) * math.pi ** 2 for l in range(1, cutoff + 1)])
    pairings = np.array([[float(coeff(k, l, directions)) for l in range(1, cutoff + 1)]
                         for k in range(1, cutoff + 1)])
    numeric_q = q_formula(lam, pairings, np.zeros_like(pairings), n, np.diag(pairings))
    reference = float(q_n) * math.pi ** 2
    check(math.isclose(numeric_q, reference, rel_tol=3e-13, abs_tol=3e-12),
          "isolated production q_formula mismatch")
    coarse = []
    for density_upper in (F(2), F(4), F(100)):
        b_compare = F((cutoff + 1) ** 2, 1) / density_upper
        if b_compare > alpha(n + 1):
            lo = -alpha(n + 1) ** 2 * e_b / (b_compare - alpha(n + 1))
            hi = alpha(n) ** 2 * e_a / (b_compare - alpha(n))
            check(lo <= error <= hi, "valid Sturm comparison substitution failed")
            coarse.append({"M": str(density_upper), "usable": True,
                           "lower_pi2": str(lo), "upper_pi2": str(hi)})
        else:
            coarse.append({"M": str(density_upper), "usable": False,
                           "reason": "comparison lower bound does not exceed b"})
    records.append({"label": label, "n": n, "N": cutoff,
                    "E_n": str(e_a), "E_np1": str(e_b), "J_n": str(j_a),
                    "J_np1": str(j_b), "Q_pi2": str(q_full), "Q_N_pi2": str(q_n),
                    "error_pi2": str(error), "lower_pi2": str(lower),
                    "upper_pi2": str(upper), "isolated_q_float": numeric_q,
                    "reference_q_float": reference, "coarse": coarse})


for n in range(2, 13):
    run_case("sharp_cosine", n, n + 1, {1: F(1)}, sharp=True)
for n in range(1, 13):
    for extra in (1, 3):
        run_case("constant_scaling", n, n + extra, {0: F(1)})
for n in (2, 5, 8):
    for extra in (1, 5):
        run_case("multi_cosine", n, n + extra, {1: F(1), 4: -F(2, 3), 7: F(1, 5)})

result = {"status": "PASS", "cases": len(records),
          "scope": "exact finite-support Fourier identities; isolated q_formula float comparison only",
          "interpreter": sys.executable, "python": sys.version,
          "numpy": np.__version__,
          "variation_sha256": hashlib.sha256(raw).hexdigest(),
          "q_formula_source_sha256": hashlib.sha256(q_source.encode("utf-8")).hexdigest(),
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "records": records}
with OUT.open("x", encoding="utf-8", newline="\n") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)
    handle.write("\n")
print(json.dumps({"status": result["status"], "cases": result["cases"],
                  "output": str(OUT), "q_formula_source_sha256": result["q_formula_source_sha256"],
                  "script_sha256": result["script_sha256"]}, ensure_ascii=False))
