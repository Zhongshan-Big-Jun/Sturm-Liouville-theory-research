# -*- coding: utf-8 -*-
"""Completeness tests in H^2, H^3, H^4: project cos(pi x) onto span of polynomial bases.
Gauss-Legendre over [-1,1] with weights summing to 2."""
from fractions import Fraction as F
import numpy as np

def ev(p, x): return sum(a*x**k for k, a in enumerate(p))
def deriv(p): return [F(k)*p[k] for k in range(1, len(p))]
def bc1_res(p):
    d = deriv(p); v = (ev(p, F(1)) - ev(p, F(-1)))/2
    return (ev(d, F(1)) - v, ev(d, F(-1)) - v)
def kc(p, c):
    n = len(p)-1; out = [F(0)]*(n+1)
    for j in range(n+1):
        out[j] += c*p[j]
        if j+2 <= n: out[j] -= F((j+1)*(j+2))*p[j+2]
    return out
def l2(p, q):
    n = max(len(p), len(q)); P = list(p)+[F(0)]*(n-len(p)); Q = list(q)+[F(0)]*(n-len(q))
    s = F(0)
    for j in range(n):
        for k in range(n):
            if (j+k)%2 == 0: s += P[j]*Q[k]*F(2, j+k+1)
    return s

xgl, wgl = np.polynomial.legendre.leggauss(1600)
def I_cos(k): return np.sum(np.cos(np.pi*xgl)*xgl**k*wgl)
def I_sin(k): return np.sum(np.sin(np.pi*xgl)*xgl**k*wgl)

def p_basis_H2(N, c):
    out = {}
    for k in range(N+1):
        if k in (2,3): continue
        cc = [F(0)]*(k+1); cc[k] = F(1)
        n = k//2
        if n != 1 and k >= 4: cc[k-2] = -F(n, n-1)
        out[k] = cc
    return out

def solve_particular(rows, rhs, n):
    """solve A x = rhs (underdetermined OK, free vars -> 0); rows: list of lists len n"""
    M = [r[:]+[b] for r, b in zip(rows, rhs)]
    nrows = len(M); rr = 0; piv = 0
    while rr < nrows and piv < n+1:
        pv = next((i for i in range(rr, nrows) if M[i][piv] != 0), None)
        if pv is None: piv += 1; continue
        M[rr], M[pv] = M[pv], M[rr]
        fac = M[rr][piv]; M[rr] = [z/fac for z in M[rr]]
        for i in range(nrows):
            if i != rr and M[i][piv] != 0:
                f = M[i][piv]; M[i] = [z - f*y for z, y in zip(M[i], M[rr])]
        piv += 1; rr += 1
    sol = [F(0)]*n
    for row in M:
        pc = next((i for i, z in enumerate(row[:-1]) if z != 0), None)
        if pc is None: continue
        sol[pc] = row[-1] - sum(row[i]*sol[i] for i in range(n) if i != pc)
    return sol

def p_basis_H4(N, c):
    out = {0: [F(1)], 1: [F(0), F(1)]}
    for d in range(6, N+1):
        rows = []
        for j in (0, 1):
            for e in (0, 1):
                row = [F(0)]*d
                for t in range(d):
                    p = [F(0)]*(d+1); p[t] = F(1)
                    kcj = kc(p, c) if j == 1 else p
                    row[t] = bc1_res(kcj)[e]
                lead = [F(0)]*(d+1); lead[d] = F(1)
                kclead = kc(lead, c) if j == 1 else lead
                rhs = -bc1_res(kclead)[e]
                rows.append(row); rows.append([rhs])  # placeholder, fix below
        # rebuild properly: rows as (row, rhs)
        rows = []
        for j in (0, 1):
            for e in (0, 1):
                row = [F(0)]*d
                for t in range(d):
                    p = [F(0)]*(d+1); p[t] = F(1)
                    kcj = kc(p, c) if j == 1 else p
                    row[t] = bc1_res(kcj)[e]
                lead = [F(0)]*(d+1); lead[d] = F(1)
                kclead = kc(lead, c) if j == 1 else lead
                rhs = -bc1_res(kclead)[e]
                rows.append((row, rhs))
        sol = solve_particular([r for r, _ in rows], [b for _, b in rows], d)
        cc = [F(0)]*(d+1)
        for t in range(d): cc[t] = sol[t]
        cc[d] = F(1)
        assert all(z == 0 for z in bc1_res(cc) + bc1_res(kc(cc, c))), f"BC fail d={d}"
        out[d] = cc
    return out

def h2_inner(p, q, c): return l2(kc(p, c), kc(q, c))
def h3_inner(p, q, c):
    kp = kc(p, c); kq = kc(q, c)
    term = -F(1,2)*(ev(kp,F(1))-ev(kp,F(-1)))*(ev(kq,F(1))-ev(kq,F(-1)))
    return term + l2(deriv(kp), deriv(kq)) + c*l2(kp, kq)
def h4_inner(p, q, c):
    return l2(kc(kc(p, c), c), kc(kc(q, c), c))

def project(f_self, b, G):
    n = len(b)
    try:
        coef = np.linalg.solve(G, b)
    except np.linalg.LinAlgError:
        coef = np.linalg.lstsq(G, b, rcond=None)[0]
    return max(f_self - coef @ G @ coef, 0.0), coef

c = F(3); cfl = 3.0; lam = np.pi**2 + cfl
for mode, inner in [("H2", h2_inner), ("H3", h3_inner), ("H4", h4_inner)]:
    start = 4 if mode != "H4" else 6
    print(f"== cos(pi x) projection residual in {mode} ==")
    for N in (start+2, start+6, start+12, start+20, start+30):
        basis = (p_basis_H2 if mode != "H4" else p_basis_H4)(N, c)
        degs = sorted(basis); blist = [basis[d] for d in degs]
        G = np.array([[float(inner(p, q, c)) for q in blist] for p in blist])
        b = []
        for q in blist:
            if mode == "H2":
                kq = kc(q, c)
                b.append(lam*sum(float(a)*I_cos(k) for k, a in enumerate(kq)))
            elif mode == "H3":
                kq = kc(q, c); dkq = deriv(kq)
                s = -0.5*(float(ev(kq,F(1))-ev(kq,F(-1))))*(lam*(np.cos(np.pi)-np.cos(-np.pi)))
                s += sum(float(a)*(-lam*np.pi)*I_sin(k) for k, a in enumerate(dkq))
                s += cfl*lam*sum(float(a)*I_cos(k) for k, a in enumerate(kq))
                b.append(s)
            else:
                k2q = kc(kc(q, c), c)
                b.append(lam**2*sum(float(a)*I_cos(k) for k, a in enumerate(k2q)))
        if mode == "H2": f_self = lam**2*np.sum(np.cos(np.pi*xgl)**2*wgl)
        elif mode == "H3":
            f_self = -0.5*(lam*(np.cos(np.pi)-np.cos(-np.pi)))**2 + (-lam*np.pi)**2*np.sum(np.sin(np.pi*xgl)**2*wgl) + cfl*lam**2*np.sum(np.cos(np.pi*xgl)**2*wgl)
        else: f_self = lam**4*np.sum(np.cos(np.pi*xgl)**2*wgl)
        res, coef = project(f_self, np.array(b), G)
        print(f"   N={N}: residual = {res:.3e}")
