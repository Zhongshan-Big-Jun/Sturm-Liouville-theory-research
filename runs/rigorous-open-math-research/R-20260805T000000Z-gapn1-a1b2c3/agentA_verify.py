# -*- coding: utf-8 -*-
"""agentA_verify.py: O2 single-crossing verification (Agent A). Fast version.
Reproduces: u*(R) table, task-required sign/derivative checks, corrected zero
condition, KEY lemma margins.  Uses vectorized interpolation of the inverse
phase curves E(alpha)/alpha and O(alpha)/alpha (validated vs lams_fast)."""
import sys, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, r'F:\LaTeX\BVE research')
from scripts.gap_lib import lams_fast, y_at, norm2

class PhaseSolver:
    def __init__(self, q, N=200000):
        self.q = q
        ag1 = np.linspace(1e-12, np.pi/2-1e-12, N); self.ag1 = ag1
        self.r1 = np.arctan(1.0/(q*np.tan(ag1)))/ag1          # decreasing inf -> 0
        ag2 = np.linspace(1e-12, np.pi-1e-12, N); self.ag2 = ag2
        O = np.empty_like(ag2); m = ag2 < np.pi/2
        O[m] = np.pi - np.arctan(q*np.tan(ag2[m]))
        O[~m] = np.arctan(-q*np.tan(ag2[~m]))
        self.r2 = O/ag2
    def alpha1(self, c): return np.interp(c, self.r1[::-1], self.ag1[::-1])
    def alpha2(self, c): return np.interp(c, self.r2[::-1], self.ag2[::-1])

def Phi(a, q): return np.cos(a)**2 + q*q*np.sin(a)**2
def M(a, c, q): return q*(q*q-1.0)*a*a*np.sin(a)**2/(q + c*Phi(a,q))
def u_from_c(c, q): return q/(2.0*(c+q))
def D_of(c, q, S):
    a1 = S.alpha1(np.array([c]))[0]; a2 = S.alpha2(np.array([c]))[0]
    return 4.0*(c+q)**2*(a2*a2-a1*a1)/q**2
def G(alpha, c, q):
    Ph = Phi(alpha,q); W = 3 + 2*alpha/np.tan(alpha)
    return -Ph*W/(q+c*Ph) + 2*c*alpha*Ph*(q*q-1)*np.sin(alpha)*np.cos(alpha)/(q+c*Ph)**2

def half_s(R, u, which, N=8000):
    v = 0.5 - u; qq = np.sqrt(R)
    if which == 'even':
        f = lambda s: np.cos(s*u)*np.cos(s*qq*v) - qq*np.sin(s*u)*np.sin(s*qq*v)
        lo, hi = 1e-12, np.pi
    else:
        f = lambda s: qq*np.sin(s*u)*np.cos(s*qq*v) + np.cos(s*u)*np.sin(s*qq*v)
        lo, hi = 1e-12, 2*np.pi
    xs = np.linspace(lo, hi, N)
    vals = f(xs)
    sg = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    idx = np.nonzero(sg)[0]
    assert len(idx) >= 1, (which, R, u)
    return brentq(f, xs[idx[0]], xs[idx[0]+1])

def f_sym_full(u, R):
    blocks = [(u,1.0),(1-2*u,R),(u,1.0)]
    s = lams_fast(blocks, 2)
    vals = []
    for sk in s:
        y = y_at(blocks, np.array([sk]), np.array([u]))[0]
        vals.append(y/np.sqrt(norm2(blocks, sk)))
    U = np.array(vals)
    return s[0]**2*U[0]**2 - s[1]**2*U[1]**2

def ustar_for(R, nscan=4000):
    q = np.sqrt(R); S = PhaseSolver(q)
    cs = np.geomspace(1e-7, 1-1e-9, nscan)
    a1 = S.alpha1(cs); a2 = S.alpha2(cs)
    Fs = M(a1,cs,q) - M(a2,cs,q)
    sc = np.nonzero(np.signbit(Fs[1:])!=np.signbit(Fs[:-1]))[0]
    assert len(sc) == 1, R
    lo, hi = cs[sc[0]], cs[sc[0]+1]
    def Fsc(c):
        return M(S.alpha1(np.array([c]))[0],c,q) - M(S.alpha2(np.array([c]))[0],c,q)
    cstar = brentq(Fsc, lo, hi)
    return u_from_c(cstar,q), cstar, S

if __name__ == '__main__':
    print("u* table:")
    for R in [1.0005, 1.001, 1.01, 1.05, 1.1, 1.5, 2, 3, 4, 7, 10, 30, 100, 1e3, 1e4]:
        ust, cs, S = ustar_for(R)
        print(f"  R={R:9.1f}: u*={ust:.9f} D*={D_of(cs,np.sqrt(R),S):.9f}")
    print("task-required dD/du check (R=4):")
    for u in [0.10, 0.30, 0.45, 0.48]:
        fs = f_sym_full(u, 4.0)
        h = 1e-6
        s1l=half_s(4.0,u-h,'even'); s2l=half_s(4.0,u-h,'odd')
        s1r=half_s(4.0,u+h,'even'); s2r=half_s(4.0,u+h,'odd')
        dD = ((s2r**2-s1r**2)-(s2l**2-s1l**2))/(2*h)
        print(f"  u={u}: f={fs:+.6e} dD/du={dD:+.6e} -2(R-1)f={-6*fs:+.6e}")
    print("corrected zero condition at u*:")
    for R, ust in [(1.1,0.422035209),(2.0,0.436695944),(4.0,0.451485466),(10.0,0.466931186)]:
        blocks = [(ust,1.0),(1-2*ust,R),(ust,1.0)]
        s = lams_fast(blocks,2)
        zc = np.sqrt(norm2(blocks,s[1]))*np.sin(s[0]*ust) - np.sqrt(norm2(blocks,s[0]))*np.sin(s[1]*ust)
        print(f"  R={R:5.1f}: {zc:+.3e}")
    print("KEY lemma margins (min over c in (0,1/2) of G(a2)-G(a1)):")
    for R in [1.05, 1.1, 1.5, 2, 4, 10, 100, 1e4]:
        q = np.sqrt(R); S = PhaseSolver(q)
        cs = np.linspace(1e-4, 0.5-1e-5, 200)
        a1 = S.alpha1(cs); a2 = S.alpha2(cs)
        diff = G(a2,cs,q) - G(a1,cs,q)
        print(f"  R={R:9.1f}: min = {diff.min():.4f}")
