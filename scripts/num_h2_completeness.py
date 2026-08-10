# -*- coding: utf-8 -*-
"""Numerical verification for the H^2[-1,1] analytic completeness claim."""
import numpy as np
import math

def poly_solve(qcoeff, c):
    n = len(qcoeff) - 1
    a = [0.0]*(n+1)
    for j in range(n, -1, -1):
        if j+2 <= n:
            a[j] = (qcoeff[j] + (j+1)*(j+2)*a[j+2])/c
        else:
            a[j] = qcoeff[j]/c
    return a

def ell1(pcoeff):
    return sum(k*a for k,a in enumerate(pcoeff) if k % 2 == 0)

def ell2(pcoeff):
    return sum((k-1)*a for k,a in enumerate(pcoeff) if k % 2 == 1)

def norm2_poly(pcoeff):
    n = len(pcoeff)-1
    s = 0.0
    for j in range(n+1):
        for k in range(n+1):
            if (j+k) % 2 == 0:
                s += pcoeff[j]*pcoeff[k]*2.0/(j+k+1)
    return s

def p_basis(N):
    out = []
    for k in range(N+1):
        if k in (2,3):
            continue
        c_ = np.zeros(k+1); c_[k] = 1.0
        n = k//2
        if n != 1 and k >= 4:
            c_[k-2] = -n/(n-1)
        assert abs(ell1(c_)) < 1e-12 and abs(ell2(c_)) < 1e-12
        out.append((k, c_))
    return out

def kc_apply(pcoeff, c):
    n = len(pcoeff)-1
    out = [0.0]*(n+1)
    for j in range(n+1):
        out[j] += c*pcoeff[j]
        if j+2 <= n:
            out[j] -= (j+1)*(j+2)*pcoeff[j+2]
    return out

def l2_pair(pcoeff, qcoeff):
    n = max(len(pcoeff), len(qcoeff))-1
    p = np.zeros(n+1); q = np.zeros(n+1)
    p[:len(pcoeff)] = pcoeff; q[:len(qcoeff)] = qcoeff
    s = 0.0
    for j in range(n+1):
        for k in range(n+1):
            if (j+k) % 2 == 0:
                s += p[j]*q[k]*2.0/(j+k+1)
    return s

c = 1.0
N = 30
basis = p_basis(N)
print("(A) basis size (deg<=%d excl 2,3): %d" % (N, len(basis)))
for k in (2,3):
    cc = np.zeros(k+1); cc[k]=1.0
    print("   x^%d: ell1=%.3e ell2=%.3e (nonzero => not in P_bc)" % (k, ell1(cc), ell2(cc)))

# dimension check: truncated P_bc has dim N-1 for N>=2
dims = [sum(1 for deg,_ in basis if deg <= M) for M in (5, 10, 20, 30)]
print("   dims of span{p_n: deg<=M} for M=5,10,20,30:", dims, " (expected M-1)")

G = np.zeros((len(basis), len(basis)))
kc_basis = []
for i,(deg_i, pi_) in enumerate(basis):
    kpi = kc_apply(pi_, c)
    kc_basis.append(kpi)
    for j in range(i+1):
        G[i,j] = G[j,i] = l2_pair(kpi, kc_basis[j])

ev = np.linalg.eigvalsh(G)
print("(B) Gram of {K_c p_n}: smallest evs:", np.round(ev[:4], 10), " largest:", round(ev[-1],3))

def cos_coeff(m, Nc=60):
    out = np.zeros(Nc+1)
    for k in range(Nc//2+1):
        out[2*k] = (-1)**k * (m*math.pi)**(2*k)/math.factorial(2*k)
    return out

# project cos(m pi x) onto span{basis} in H^2 for increasing N
for m in (1,2):
    f = cos_coeff(m, 2*N)
    fk = kc_apply(f, c)
    f2 = l2_pair(fk, fk)
    for NN in (6, 10, 16, 24, 30):
        idx = [i for i,(deg,_) in enumerate(basis) if deg <= NN]
        Gs = G[np.ix_(idx,idx)]
        rhs = np.array([l2_pair(fk, kc_basis[i]) for i in idx])
        x = np.linalg.solve(Gs, rhs)
        resid = max(f2 - x @ Gs @ x, 0.0)
        print("   cos(%d pi x), N=%d: residual^2 = %.3e" % (m, NN, resid))

print("(C) functional growth (should diverge):")
print("    n   |ell1(Kc^{-1}x^{2n})|/||x^{2n}||  |ell2(Kc^{-1}x^{2n+1})|/||..||")
for n in (2,4,6,8,10,12,16,20):
    qe = np.zeros(2*n+1); qe[2*n]=1.0
    L1 = ell1(poly_solve(qe, c))
    qo = np.zeros(2*n+2); qo[2*n+1]=1.0
    L2 = ell2(poly_solve(qo, c))
    print("   %2d   %16.6e   %16.6e" % (n, abs(L1)/math.sqrt(norm2_poly(qe)), abs(L2)/math.sqrt(norm2_poly(qo))))

# (D) verify (h,p)_{2,c} = (K_c h, K_c p) numerically for h=cos(pi x), p=p_4
def ip2(hc, pc, c):
    # formula (26): -c(h(1)-h(-1))(p(1)-p(-1)) + int(h''p''+2c h'p'+c^2 h p)
    def ev(cf, x):
        s = 0.0
        for j,a in enumerate(cf):
            s += a*x**j
        return s
    def deriv(cf):
        return [ (j+1)*cf[j+1] for j in range(len(cf)-1) ]
    h = ev(hc,1.0)-ev(hc,-1.0); p = ev(pc,1.0)-ev(pc,-1.0)
    d2h = deriv(deriv(hc)); d2p = deriv(deriv(pc)); dh = deriv(hc); dp = deriv(pc)
    def intp(a,b):
        return l2_pair(a,b)
    return -c*h*p + intp(d2h,d2p) + 2*c*intp(dh,dp) + c*c*intp(hc,pc)

f = cos_coeff(1, 60)
p4 = np.zeros(5); p4[4]=1.0; p4[2]=-2.0
a1 = ip2(f, p4, c)
a2 = l2_pair(kc_apply(f,c), kc_apply(p4,c))
print("(D) (f,p4)_{2,c} = %.10f  vs (K_c f, K_c p4) = %.10f  diff %.2e" % (a1,a2,abs(a1-a2)))
