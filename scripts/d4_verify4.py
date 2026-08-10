# -*- coding: utf-8 -*-
"""Direction 4 final: correct sum-form + fundamental system + Casoratian."""
from mpmath import mp, mpf, log
mp.dps = 120

def minimal_mp(parity, cval, N):
    cf = mpf(cval); lam = mpf(4)/cf
    def a1(j):
        jj = mpf(j)
        if parity=='e': P = 8*cf*jj*jj - 4*cf*jj + cf*cf*jj/(jj-1)
        else:           P = 8*cf*jj*jj + 4*cf*jj + cf*cf*jj/(jj-1)
        return P/(cf*cf*jj*jj*lam)
    def a2(j):
        jj = mpf(j)
        if parity=='e': Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj-3) + 4*cf*jj*(2*jj-3)
        else:           Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj+1) + 4*cf*jj*(2*jj-1)
        return -Q/(cf*cf*jj*jj*(jj-1)*(jj-1)*lam*lam)
    def a3(j):
        jj = mpf(j)
        if parity=='e': R = 4*jj*(jj-2)*(2*jj-3)*(2*jj-5)
        else:           R = 4*jj*(jj-2)*(2*jj-1)*(2*jj-3)
        return R/(cf*cf*jj*jj*(jj-1)*(jj-1)*(jj-2)*(jj-2)*lam**3)
    z = [mpf(0)]*(N+3)
    z[N] = mpf(1)
    for j in range(N-1, -1, -1):
        z[j] = (z[j+3] - a1(j+3)*z[j+2] - a2(j+3)*z[j+1])/a3(j+3)
    return [z[j]/z[0] for j in range(N+1)]

def build_third(parity, cval, N, w2=1):
    cf = mpf(cval); lam = mpf(4)/cf
    def a2(j):
        jj = mpf(j)
        if parity=='e': Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj-3) + 4*cf*jj*(2*jj-3)
        else:           Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj+1) + 4*cf*jj*(2*jj-1)
        return -Q/(cf*cf*jj*jj*(jj-1)*(jj-1)*lam*lam)
    def a3(j):
        jj = mpf(j)
        if parity=='e': R = 4*jj*(jj-2)*(2*jj-3)*(2*jj-5)
        else:           R = 4*jj*(jj-2)*(2*jj-1)*(2*jj-3)
        return R/(cf*cf*jj*jj*(jj-1)*(jj-1)*(jj-2)*(jj-2)*lam**3)
    E = [mpf(1)]*(N+1)
    beta = 1 if parity=='e' else 3
    for j in range(1,N+1): E[j] = E[j-1]*(1+mpf(beta)/(2*j))
    if parity=='e':
        sm = [None] + [mpf(1)/(2*j+1) - mpf(1)/(2*j-1) for j in range(1,N+1)]
    else:
        sm = [None] + [mpf(3)/(2*j+3) - mpf(3)/(2*j+1) for j in range(1,N+1)]
    w = [mpf(0)]*(N+1); w[2] = mpf(w2)
    for j in range(3,N+1):
        Bj = -a3(j)*E[j-3]/E[j]
        w[j] = -Bj*(sm[j-2]/sm[j])*w[j-1]
    sind = [mpf(0)]*(N+1)
    acc = mpf(0)
    for j in range(2,N+1):
        acc += w[j]
        sind[j] = sm[j]*acc
    return sind, E, a2, a3

for par in ('e','o'):
    N = 400
    sind, E, a2, a3 = build_third(par, 3, N)
    # 1) sind satisfies the s-recurrence
    ok = True
    for j in range(3,N+1):
        Aj = -(a2(j)*E[j-2]+a3(j)*E[j-3])/E[j]
        Bj = -a3(j)*E[j-3]/E[j]
        if abs(sind[j]-Aj*sind[j-1]-Bj*sind[j-2]) > mpf(10)**(-110):
            ok = False; print("  fail s-rec", par, j); break
    # 2) zind_j = E_j * sum_{k<=j} sind_k solves the z-recurrence (j>=3)
    rind = [mpf(0)]*(N+1)
    for j in range(2,N+1): rind[j] = rind[j-1] + sind[j]
    zind = [E[j]*rind[j] for j in range(N+1)]
    lam = mpf(4)/3
    def a1(j):
        jj = mpf(j)
        if par=='e': P = 8*3*jj*jj - 4*3*jj + 9*jj/(jj-1)
        else:        P = 8*3*jj*jj + 4*3*jj + 9*jj/(jj-1)
        return P/(9*jj*jj*lam)
    ok2 = True
    for j in range(3,N+1):
        if abs(zind[j] - a1(j)*zind[j-1] - a2(j)*zind[j-2] - a3(j)*zind[j-3]) > mpf(10)**(-105):
            ok2 = False; break
    # 3) E^+, E^- product solutions + Casoratian nonzero
    Ep = [mpf(1)]*(N+1); Em = [mpf(1)]*(N+1)
    bp, bm = (1,-1) if par=='e' else (3,1)
    for j in range(1,N+1):
        Ep[j] = Ep[j-1]*(1+mpf(bp)/(2*j))
        Em[j] = Em[j-1]*(1+mpf(bm)/(2*j))
    # Casoratian det at j=3 (using zind and Ep, Em)
    C = (Ep[3]*Em[2]*zind[1] + Em[3]*zind[2]*Ep[1] + zind[3]*Ep[2]*Em[1]
         - Ep[3]*zind[2]*Em[1] - Em[3]*Ep[2]*zind[1] - zind[3]*Em[2]*Ep[1])
    # compare zind vs minimal h*: fit the linear combination: h* = a*Ep + b*Em + c*zind
    h = minimal_mp(par, 3, 200)
    # use j=0,1,2 to solve for a,b,c
    from mpmath import lu_solve, matrix
    M = matrix([[Ep[0],Em[0],zind[0]],[Ep[1],Em[1],zind[1]],[Ep[2],Em[2],zind[2]]])
    v = matrix([h[0],h[1],h[2]])
    sol = lu_solve(M, v)
    err = max(abs(sol[0]*Ep[j]+sol[1]*Em[j]+sol[2]*zind[j]-h[j]) for j in range(3,60))
    print(f"  par={par}: s-rec ok={ok}, zind solves z-rec ok={ok2}, Casoratian(j=3)={mp.nstr(C,6)}, h* = aE+ + bE- + c*zind (max err j<=60)={mp.nstr(err,6)}")

print()
print("=== K (asymptotic constant) estimate ===")
from math import lgamma
for par in ('e','o'):
    h = minimal_mp(par, 3, 1500)
    logQ = [log(h[j]) + 2*lgamma(j+1) + j*log(mpf(4)/3) for j in (600, 900, 1200, 1400)]
    # log Q ~ log K - 3 log j : extrapolate logK = logQ + 3 log j
    logK = [logQ[i] + 3*log(mpf(jj)) for i, jj in enumerate((600,900,1200,1400))]
    print(f"  par={par}: log K estimates: {[mp.nstr(x,10) for x in logK]}")
