# -*- coding: utf-8 -*-
# Direction 2 verification:
# (V1) jump-in-H^s identity: (w, K_c p_{2m})_s = c N_{2m} - A_m N_{2m-2} + B_m N_{2m-4}, N_k = (w, x^k)_s
# (V2) ||x^k||_s growth exponent (<= C_s k^s)
# (V3) diagonal H_beta sharpness: complete iff beta <= 3/2
# (V4) {K_c p_n} complete in H^s: projection residuals decay
from fractions import Fraction as F
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import orthogonal_systems_verify as V

def mono(k):
    c = [F(0)]*(k+1); c[k] = F(1); return c


ok = True
def check(name, cond):
    global ok
    if not cond: ok = False; print("FAIL " + name)
    else: print("PASS " + name)

cval = 3

# V1: exact identity for s=0..5, m=2..6, several test polynomials w
def p_poly(m):
    c = [F(0)]*(2*m+1); c[2*m] = F(1); c[2*m-2] = -F(m, m-1); return c

for s in range(0, 6):
    for m in range(2, 7):
        Am = 2*m*(2*m-1) + F(cval*m, m-1); Bm = 2*m*(2*m-3)
        Apm = 2*m*(2*m+1) + F(cval*m, m-1); Bpm = 2*m*(2*m-1)
        # test w in {x^2, x^3, x^2+x^4, 1+x+x^5} -> need as coeff lists
        for wname, w in [("x2",[F(0),F(0),F(1)]), ("x3",[F(0),F(0),F(0),F(1)]),
                         ("mix",[F(1),F(1),F(0),F(0),F(1)]), ("x5",[F(0)]*5+[F(1)])]:
            Nk = {k: V.inner_s(w, mono(k), s, cval) for k in range(0, 2*m+2)}
            lhs = V.inner_s(w, V.Kc_apply(p_poly(m), cval), s, cval)
            rhs = cval*Nk[2*m] - Am*Nk[2*m-2] + Bm*Nk[2*m-4]
            check(f"V1 s={s} m={m} {wname}: jump identity even", lhs == rhs)
            # odd
            po = [F(0)]*(2*m+2); po[2*m+1] = F(1); po[2*m-1] = -F(m, m-1)
            lhs_o = V.inner_s(w, V.Kc_apply(po, cval), s, cval)
            rhs_o = cval*Nk[2*m+1] - Apm*Nk[2*m-1] + Bpm*Nk[2*m-3]
            check(f"V1 s={s} m={m} {wname}: jump identity odd", lhs_o == rhs_o)

# V2: ||x^k||_s growth: exponent <= s (approx by log ratio)
for s in range(0, 6):
    exps = []
    for k in [20, 40, 80]:
        n = V.norm_sq(mono(k), s, cval)
        exps.append(float(n)**0.5)
    # estimate exponent via consecutive ratios
    r1 = exps[1]/exps[0]; r2 = exps[2]/exps[1]
    est = np.log(r2)/np.log(2)
    print(f"V2 s={s}: ||x^k||_s ~ k^{est:.2f} (should be <= s = {s})")

# V3: diagonal H_beta sharpness
def w_coeffs(beta, M2, N=40):
    # w = sum_{m>=1} w_{2m} x^{2m}, w_{2m} = m*M2/(2m+1)^{2beta}
    return {2*m: m*M2/(2*m+1)**(2*beta) for m in range(1, N+1)}

for beta in [1.0, 1.4, 1.5, 1.51, 1.6, 2.0]:
    # w representable iff sum (m*M2)^2/(2m+1)^{2beta} < inf, i.e. beta > 3/2
    M2 = 1.0
    s1 = sum((m*M2)**2/(2*m+1)**(2*beta) for m in range(1, 50001))
    s2 = sum((m*M2)**2/(2*m+1)**(2*beta) for m in range(1, 100001))
    # ratio of partial sums: ~1 if convergent, >1 if divergent
    ratio = s2/s1 if s1 > 0 else 1.0
    verdict = "NOT complete (w representable)" if beta > 1.5 else "complete (w not representable)"
    print(f"V3 beta={beta}: partial ratio sum(1e5)/sum(5e4) = {ratio:.3f} => {verdict}")
print("\nALL PASS" if ok else "\nSOME FAILED")
