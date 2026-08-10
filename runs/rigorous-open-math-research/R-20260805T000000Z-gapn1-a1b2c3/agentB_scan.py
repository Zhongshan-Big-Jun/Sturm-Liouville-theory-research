# -*- coding: utf-8 -*-
"""agentB_scan.py: O3a numerics - fixed points, Jacobians, curves, Hessians."""
import sys, time, json
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3')
import numpy as np
from agentB_lib import *

def T(x, R):
    z = zeros_f(x[0], x[1], R)
    return None if z is None else np.array(z)

def iterate(a0, b0, R, n=30, tol=1e-10):
    x = np.array([a0, b0]); hist=[x.copy()]
    for i in range(n):
        z = T(x, R)
        if z is None: return hist, None, 'domain'
        x = z; hist.append(x.copy())
        if np.linalg.norm(hist[-1]-hist[-2]) < tol: return hist, x, 'conv'
    return hist, x, 'maxiter'

def jacobian(x, R, h=1e-5):
    J = np.zeros((2,2))
    for j in range(2):
        e = np.zeros(2); e[j]=h
        J[:,j] = (T(x+e, R) - T(x-e, R))/(2*h)
    return J

def newton_fp(R, seed, iters=8):
    x = np.array(seed, dtype=float)
    for _ in range(iters):
        J = jacobian(x, R, h=1e-6)
        z = T(x, R)
        if z is None: return None
        dx = np.linalg.solve(np.eye(2)-J, z - x)
        x = x + dx
        if np.linalg.norm(dx) < 1e-13: break
    return x

# --- D and Hessian of D via finite differences (T calls not needed) ---
def lam(a, b, R):
    return secular_roots(a, b, R, 2)**2
def D_of(a, b, R):
    l = lam(a, b, R); return l[1]-l[0]
def D_hess(a, b, R, h=1e-4):
    def Dv(aa, bb): return D_of(aa, bb, R)
    da = (Dv(a+h,b)-Dv(a-h,b))/(2*h)
    db = (Dv(a,b+h)-Dv(a,b-h))/(2*h)
    daa = (Dv(a+h,b)-2*Dv(a,b)+Dv(a-h,b))/h**2
    dbb = (Dv(a,b+h)-2*Dv(a,b)+Dv(a,b-h))/h**2
    dab = (Dv(a+h,b+h)-Dv(a+h,b-h)-Dv(a-h,b+h)+Dv(a-h,b-h))/(4*h*h)
    return da, db, np.array([[daa, dab],[dab, dbb]])

if __name__ == '__main__':
    Rs = [1.05, 1.5, 2.0, 4.0, 10.0, 100.0]
    out = {}
    for R in Rs:
        # 1) fixed point via iteration from symmetric-line guess + Newton
        seeds = [(0.1,0.9),(0.2,0.8),(0.3,0.7),(0.4,0.6),(0.44,0.56),(0.05,0.6)]
        fpts = {}
        for s in seeds:
            hist, fin, st = iterate(s[0], s[1], R, n=30)
            if fin is not None:
                key = (round(fin[0],6), round(fin[1],6))
                fpts[key] = fpts.get(key,0)+1
        print(f"R={R}: iteration endpoint clusters: {sorted(fpts.items(), key=lambda kv:-kv[1])[:6]}")
        best = None; bestc = -1
        for k,c in fpts.items():
            if c > bestc: best, bestc = k, c
        if best is None:
            print(f"  R={R}: NO convergence from seeds"); continue
        fp = newton_fp(R, best)
        J = jacobian(fp, R)
        ev = np.linalg.eigvals(J)
        l = lam(*fp, R); Dv = l[1]-l[0]
        da, db, H = D_hess(*fp, R)
        print(f"  fp=({fp[0]:.9f},{fp[1]:.9f}) lam=({l[0]:.6f},{l[1]:.6f}) D={Dv:.6f}")
        print(f"  dD/da={da:.3e} dD/db={db:.3e} (should be ~0 at critical point)")
        print(f"  J={np.round(J,5)} eig={np.round(ev,5)} rho={max(abs(ev)):.5f}")
        print(f"  H={np.round(H,4)} Hess eig={np.round(np.linalg.eigvalsh(H),4)}")
        out[str(R)] = dict(fp=[float(fp[0]),float(fp[1])], lam=list(map(float,l)), D=float(Dv),
                           J=J.tolist(), ev=list(map(float,ev)), rho=float(max(abs(ev))),
                           H=H.tolist(), dD=[float(da),float(db)])
    with open(r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260805T000000Z-gapn1-a1b2c3\agentB_fixedpoints.json','w') as f:
        json.dump(out, f, indent=1)
    print("saved agentB_fixedpoints.json")
