# verify_hs_weyl_independent.py - independent O1a checks (evidence only)
#  H1: HS bound ||S_rho - S_sigma||_HS <= (R/4)||rho - sigma||_1^{1/2}
#  H2: Weyl |1/lambda_k(rho) - 1/lambda_k(sigma)| <= ||S_rho - S_sigma||_HS
#  H3: comparison bounds k^2 pi^2 / R <= lambda_k <= k^2 pi^2
#  H4: F-001 chain arithmetic: I1 <= ||A||_2^2/16, I2 <= ||A||_1^2/16,
#      (R/32)(||A||_2^2 + ||A||_1^2) <= (R^2/16)||A||_1,
#      ||A||_2^2 <= (R-1)||A||_1, ||A||_1^2 <= (R-1)||A||_1
# Written from scratch (independent of the audited run's battery).
# Seeds: 20260806.

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from fd_lib import fd_eigs, grid_rho_from_steps, l1_exact, hs_norm2, fh_cross_integrals

rng = np.random.default_rng(20260806)
R = 4.0
N = 3000
out = {}

def random_rho(nblocks, rng, R):
    xs = np.sort(rng.uniform(0.05, 0.95, nblocks - 1))
    breaks = np.concatenate([[0.0], xs, [1.0]])
    values = rng.uniform(1.0, R, nblocks)
    return (breaks.tolist(), values.tolist())

pairs = []
for t in range(8):
    pairs.append((random_rho(6, rng, R), random_rho(6, rng, R), "random" + str(t)))
pairs.append((([0.0, 0.4, 0.7, 1.0], [1.0, R, 1.0]), ([0.0, 0.4, 0.7, 1.0], [R, 1.0, R]), "bar_vs_well"))
pairs.append((([0.0, 0.5, 1.0], [1.0, R]), ([0.0, 0.5, 1.0], [R, 1.0]), "single_jump_flip"))
pairs.append((([0.0, 0.25, 0.5, 0.75, 1.0], [1.0, R, 1.0, R, 1.0]), ([0.0, 1.0], [2.0]), "alternating_vs_const"))

H1, H2, H3, H4 = [], [], [], []
for rho, sigma, tag in pairs:
    d1 = l1_exact(rho, sigma)
    hs = np.sqrt(hs_norm2(rho, sigma))
    bound = (R / 4.0) * np.sqrt(d1)
    H1.append({"tag": tag, "hs": hs, "bound": bound, "ratio": hs / bound,
               "ok": hs <= bound * (1 + 1e-9) + 1e-12})
    lr = fd_eigs(grid_rho_from_steps(*rho, N), N, k_max=2)[0]
    ls = fd_eigs(grid_rho_from_steps(*sigma, N), N, k_max=2)[0]
    for k in (0, 1):
        weyl = abs(1.0 / lr[k] - 1.0 / ls[k])
        ok = weyl <= hs + 1e-9
        H2.append({"tag": tag, "k": k + 1, "weyl_diff": weyl, "hs": hs, "ok": ok})
        ub = (k + 1) ** 2 * np.pi ** 2
        lb = ub / R
        okb = (lb - 1e-6 <= lr[k] <= ub + 1e-6) and (lb - 1e-6 <= ls[k] <= ub + 1e-6)
        H3.append({"tag": tag, "k": k + 1, "lam": lr[k], "lb": lb, "ub": ub, "ok": okb})
    ci = fh_cross_integrals(rho, sigma)
    A1, A2 = ci["A1"], ci["A2"]
    I1, I2 = ci["I1"], ci["I2"]
    ok_chain = (
        I1 <= A2 / 16.0 * (1 + 1e-9) + 1e-12
        and I2 <= A1 ** 2 / 16.0 * (1 + 1e-9) + 1e-12
        and A2 <= (R - 1.0) * A1 * (1 + 1e-9) + 1e-12
        and A1 ** 2 <= (R - 1.0) * A1 * (1 + 1e-9) + 1e-12
        and (R / 32.0) * (A2 + A1 ** 2) <= (R ** 2 / 16.0) * A1 * (1 + 1e-9) + 1e-12
    )
    H4.append({"tag": tag, "I1": I1, "A2/16": A2 / 16.0, "I2": I2, "A1^2/16": A1 ** 2 / 16.0,
               "rhs_final": (R ** 2 / 16.0) * A1, "lhs_final": (R / 32.0) * (A2 + A1 ** 2),
               "ok_chain": bool(ok_chain)})

out["H1_HS_bound"] = H1
out["H2_Weyl"] = H2
out["H3_comparison_bounds"] = H3
out["H4_F001_chain"] = H4

def _conv(o):
    if isinstance(o, (np.bool_, np.integer)):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_hs_weyl_independent_out.json"), "w") as fp:
    json.dump(out, fp, indent=1, default=_conv)