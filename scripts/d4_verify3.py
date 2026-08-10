# -*- coding: utf-8 -*-
"""Direction 4: (i) precise minimal-solution asymptotics; (ii) sum-form (variation of constants)."""
from mpmath import mp, mpf, log, exp
mp.dps = 200

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

print("=== (i) asymptotics fit ===")
for par in ('e','o'):
    h = minimal_mp(par, 3, 1500)
    # Q_j = h_j (j!)^2 (4/c)^j ; fit log Q_j = log K - alpha log j over j in [600, 1400]
    jj = [600, 800, 1000, 1200, 1400]
    from math import lgamma
    Qs = []
    for j in jj:
        logfact2 = 2*lgamma(j+1)
        Q = log(h[j]) + logfact2 + j*log(mpf(4)/3)
        Qs.append(Q)
    # alpha from adjacent pairs
    alphas = []
    for a,b in zip(jj, jj[1:]):
        ia, ib = jj.index(a), jj.index(b)
        alphas.append((Qs[ib]-Qs[ia])/(log(mpf(b))-log(mpf(a))))
    print(f"  par={par}: local exponents alpha between {jj[0]}..{jj[-1]}: {[mp.nstr(x,8) for x in alphas]}")
    print(f"    log Q at j=1000: {mp.nstr(Qs[3],10)}")
    # ratio*j^2
    print(f"    j^2*ratio at j=1000,1400: {mp.nstr(1e6*h[1001]/h[1000],10)}, {mp.nstr(1.96e6*h[1401]/h[1400],10)}")

print()
print("=== (ii) variation-of-constants sum form for the third solution ===")
# Work in z-scale with E^+ product solution. s_j = r_j - r_{j-1}, r_j = z_j/E_j.
# s-recurrence: s_j = A_j s_{j-1} + B_j s_{j-2}, A_j = -(a2 E_{j-2}+a3 E_{j-3})/E_j, B_j = -a3 E_{j-3}/E_j.
# Known solution: s^-_j = 3/(2j+3) - 3/(2j+1). Independent: s^ind via w_j = -B_j (s^-_{j-2}/s^-_j) w_{j-1}.
def third_solution(parity, cval, N, w2=1):
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
    sm = [None]*(N+1)   # s^-_j
    for j in range(1,N+1): sm[j] = mpf(3)/(2*j+3) - mpf(3)/(2*j+1)
    # w_j = -B_j (s^-_{j-2}/s^-_j) w_{j-1}, j>=3; w_2 = w2
    w = [mpf(0)]*(N+1); w[2] = mpf(w2)
    for j in range(3,N+1):
        Bj = -a3(j)*E[j-3]/E[j]
        w[j] = -Bj*(sm[j-2]/sm[j])*w[j-1]
    # s^ind_j = s^-_j * (sum_{k=2}^{j} w_k)
    sind = [mpf(0)]*(N+1)
    acc = mpf(0)
    for j in range(2,N+1):
        acc += w[j]
        sind[j] = sm[j]*acc
    return sind, sm, w

for par in ('e','o'):
    sind, sm, w = third_solution(par, 3, 300)
    # consistency: sind must satisfy the s-recurrence (exact by construction, verify numerically)
    cf = mpf(3); lam = mpf(4)/3
    def a2(j):
        jj = mpf(j)
        if par=='e': Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj-3) + 4*cf*jj*(2*jj-3)
        else:        Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj+1) + 4*cf*jj*(2*jj-1)
        return -Q/(cf*cf*jj*jj*(jj-1)*(jj-1)*lam*lam)
    def a3(j):
        jj = mpf(j)
        if par=='e': R = 4*jj*(jj-2)*(2*jj-3)*(2*jj-5)
        else:        R = 4*jj*(jj-2)*(2*jj-1)*(2*jj-3)
        return R/(cf*cf*jj*jj*(jj-1)*(jj-1)*(jj-2)*(jj-2)*lam**3)
    E=[mpf(1)]*(301)
    beta = 1 if par=='e' else 3
    for j in range(1,301): E[j]=E[j-1]*(1+mpf(beta)/(2*j))
    ok=True
    for j in range(3,301):
        Aj=-(a2(j)*E[j-2]+a3(j)*E[j-3])/E[j]
        Bj=-a3(j)*E[j-3]/E[j]
        if abs(sind[j]-Aj*sind[j-1]-Bj*sind[j-2]) > mpf(10)**(-190):
            ok=False; break
    print(f"  par={par}: sind satisfies s-recurrence = {ok}")
    # the third solution z^ind_j = E_j * r^ind_j with r^ind from sind (choose r_1, s_2 accordingly)
    # minimal solution in z-scale should be a linear combination; compare ratios
    h = minimal_mp(par, 3, 300)
    # compute z^ind with initial r_1 = 0, s_2 = 1 -> r_j = sum_{k<=j} s_k
    rind = [mpf(0)]*(301)
    for j in range(2,301): rind[j] = rind[j-1] + sind[j]
    zind = [E[j]*rind[j] for j in range(301)]
    # compare ratio zind_{j+1}/zind_j with h_{j+1}/h_j at j=100,200 (should match if proportional)
    print(f"    par={par}: ratio zind/h at j=100: {mp.nstr((zind[101]/zind[100])/(h[101]/h[100]),10)}; at j=200: {mp.nstr((zind[201]/zind[200])/(h[201]/h[200]),10)}")
