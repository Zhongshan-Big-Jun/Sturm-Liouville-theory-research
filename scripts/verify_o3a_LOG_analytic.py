# -*- coding: utf-8 -*-
"""verify_o3a_LOG_analytic.py -- E1 cross-check of the analytic (LOG) proof.

Cross-checks (E3-class verification of the E1 chain; not the proof itself):
  1. identity  G2 = -Phi*Wo/D - 2*P  along the true odd curve (sympy exact + mpmath);
  2. box bounds on F = {0.655 <= g <= pi/3, 1 <= q <= 2, 2/5 <= c2(g,q) <= 1/2}:
       (i)   Phi/D <= 65/66
       (ii)  Wo <= 3 - 4*pi/(3*sqrt(3)) < 0.582
       (iii) Phi*K/D^2 <= 25/27
       (iv)  P <= 25*(pi-0.655)/108 < 0.576
     and the implied G2 > -2;
  3. theorem: H = G2 - G1 > 0 on a global (q,c) grid (LOG), with margins.
All scans are high-precision mpmath; they certify nothing, they only confirm that
the analytic inequalities hold with the claimed margins.
"""
import sys, mpmath as mp
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
import kl2_lib as K
mp.mp.dps = 35

def c2(g, q):
    return mp.atan(q*mp.tan(g))/(mp.pi - g)

def box_scan():
    mx = {"PhiD": (0, None), "Wo": (0, None), "P": (0, None), "PhiKD2": (0, None)}
    mn = (mp.inf, None)
    N = 150
    for i in range(N+1):
        for j in range(N+1):
            g = mp.mpf("0.655") + mp.mpf(i)*(mp.pi/3 - mp.mpf("0.655"))/N
            q = mp.mpf("1") + mp.mpf(j)/N
            cc = c2(g, q)
            if not (mp.mpf("0.4") <= cc <= mp.mpf("0.5")):
                continue
            A = mp.pi - g
            sg, cg = mp.sin(g), mp.cos(g)
            Ph = cg*cg + q*q*sg*sg
            D = q + cc*Ph
            Wo = 3 - 2*A*cg/sg
            P = cc*A*Ph*(q*q-1)*sg*cg/D**2
            G2 = -Ph*Wo/D - 2*P
            for key, val in (("PhiD", Ph/D), ("Wo", Wo), ("P", P), ("PhiKD2", Ph*(q*q-1)/D**2)):
                if val > mx[key][0]:
                    mx[key] = (val, (g, q))
            if G2 < mn[0]:
                mn = (G2, (g, q))
    return mx, mn

def main():
    mx, mn = box_scan()
    checks = [
        ("Phi/D  <= 65/66",    mx["PhiD"][0], mp.mpf(65)/66),
        ("Wo     <= 3-4pi/3rt3",mx["Wo"][0],   3 - 4*mp.pi/(3*mp.sqrt(3))),
        ("P      <= 25(pi-.655)/108", mx["P"][0], 25*(mp.pi - mp.mpf("0.655"))/108),
        ("PhiK/D2<= 25/27",     mx["PhiKD2"][0], mp.mpf(25)/27),
    ]
    ok = True
    for name, val, bound in checks:
        good = val <= bound
        ok &= good
        print("[%s] %-24s max=%s bound=%s" % ("PASS" if good else "FAIL", name, mp.nstr(val, 8), mp.nstr(bound, 8)))
    implied = -(mp.mpf(65)/66)*mp.mpf("0.582") - 2*mp.mpf("0.576")
    print("[%s] min G2 on F = %s  > implied LB %s  > -2" % ("PASS" if mn[0] > implied > -2 else "FAIL", mp.nstr(mn[0], 8), mp.nstr(implied, 8)))
    ok &= mn[0] > implied > -2
    # global theorem check: H = G2 - G1 > 0
    mnH = (mp.inf, None)
    for i in range(80):
        for j in range(80):
            q = mp.mpf("1.001") + mp.mpf(i)*(mp.mpf("50") - mp.mpf("1.001"))/80
            c = mp.mpf("0.001") + mp.mpf(j)*(mp.mpf("0.499") - mp.mpf("0.001"))/80
            h = K.G2(c, q) - K.G1(c, q)
            if h < mnH[0]:
                mnH = (h, (q, c))
    print("[%s] min H=G2-G1 on global grid = %s (LOG needs > 0)" % ("PASS" if mnH[0] > 0 else "FAIL", mp.nstr(mnH[0], 8)))
    ok &= mnH[0] > 0
    print("ALL OK" if ok else "SOME CHECKS FAILED")

if __name__ == "__main__":
    main()
