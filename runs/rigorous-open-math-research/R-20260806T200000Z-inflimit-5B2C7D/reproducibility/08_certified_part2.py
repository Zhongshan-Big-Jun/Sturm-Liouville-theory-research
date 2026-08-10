# -*- coding: utf-8 -*-
"""08_certified_part2.py
Certified (directed-rounding interval arithmetic) verification of the Part II
inequalities used in the INF-limit proof:
 (M1) mid-sliver: for R0 = 1500, u in [2/sqrt(R0), 0.1]: gap >= Dbar(u)-E(u,R0) >= 25
      with E(u,R) = 2*thetabar*delta_b/u^2,
      delta_b = Cbar*thetabar^3*(1/2-u)^3/(u^3 R (1+thetabar^2(1/2-u)^2/u^2)(1-q)),
      Cbar = 0.45, q = 0.20.  Checked: H(u) = Dbar(u) - E(u,1500) - 25 > 0.
 (M2) contraction factor q(u) <= 0.20 on [2/sqrt(R0), 0.1].
 (M3) tan certificate: (tan z - z)/z^3 <= 0.45 on [0, pi/4].
 (M4) deep sliver: B2(R0) with c = 2 >= 25.
 (M5) right sliver bound at v = 0.05, R0 >= 25.
 (M6) uniform rate: max |gap-Dbar|*R on [0.1,0.475] x {1500,1e4,1e6} <= K = 50000.
ASCII punctuation.  Run: python 08_certified_part2.py
"""
import mpmath as mp
from mpmath import iv
iv.dps = 25
mp.mp.dps = 50

Cbar = mp.mpf('0.45')
q0   = mp.mpf('0.20')
R0   = mp.mpf('1500')
PI2_LO = mp.mpf('9.86960440108935861883449099987615113')
PI2_HI = mp.mpf('9.86960440108935861883449099987615114')
PISQ4_LO = mp.mpf('2.46740110027233965470862274996903778')
PISQ4_HI = mp.mpf('2.46740110027233965470862274996903779')

def F_a_iv(a, u):
    return iv.tan(iv.mpf((a, a))) - iv.mpf((a, a))*(1 - 1/(2*iv.mpf((u, u))))

def a_root_iv(u, scan=600):
    lo = mp.mpf('1.57079632679489661923132169163975144') + mp.mpf('1e-35')
    hi = mp.mpf('3.14159265358979323846264338327950288') - mp.mpf('1e-35')
    a_lo, a_hi = lo, hi
    for k in range(1, scan):
        x = lo + (hi-lo)*k/scan
        fx = F_a_iv(x, u)
        if fx.a > 0:
            a_hi = x
            break
        a_lo = x
    assert F_a_iv(a_lo, u).b < 0 and F_a_iv(a_hi, u).a > 0
    while a_hi - a_lo > mp.mpf('1e-18'):
        m = (a_lo + a_hi)/2
        fm = F_a_iv(m, u)
        if fm.b < 0:
            a_lo = m
        else:
            a_hi = m
    return (a_lo, a_hi)

# ---- M3: tan certificate ----
zp = iv.mpf((mp.mpf('0.78539816339744830961566084581987572'),
             mp.mpf('0.78539816339744830961566084581987573')))
ratio_p4 = (iv.tan(zp) - zp)/zp**3
print("M3: (tan z-z)/z^3 at pi/4 in", ratio_p4, " (series increasing, need <= 0.45)")
assert ratio_p4.b < Cbar

# ---- M2 + M1 ----
u_lo = 2/mp.sqrt(R0)
u_hi = mp.mpf('0.1')
N = 200
qmax = mp.mpf('-inf')
grid = []
for k in range(N+1):
    u = u_lo + (u_hi - u_lo)*k/N
    grid.append(u)
    qq = (mp.mpf(1)/2 - u)/u * 2/(1 + (mp.pi**2/4)*(mp.mpf(1)/2 - u)**2/u**2)
    if qq > qmax: qmax = qq
print("M2: max q(u) = ", mp.nstr(qmax, 8), " (need <= 0.20)")
assert qmax < q0

# precompute a-brackets on the grid (a increasing in u)
ab = [a_root_iv(u) for u in grid]
def Dbar_lo_hi(k):
    aL, aH = ab[k]
    u = grid[k]
    return (aL*aL - PISQ4_HI)/u**2, (aH*aH - PISQ4_LO)/u**2

def E_cell(k):
    aL = ab[k][0]
    aH = ab[k+1][1]
    a = iv.mpf((aL, aH))
    u = iv.mpf((grid[k], grid[k+1]))
    h = iv.mpf('0.5') - u
    denom = u**3 * iv.mpf((R0, R0)) * (1 + a**2*h**2/u**2) * (1 - iv.mpf((q0, q0)))
    delta = iv.mpf((Cbar, Cbar)) * a**3 * h**3 / denom
    E = 2*a*delta/u**2
    return E

worst = mp.mpf('inf')
for k in range(N):
    dbar_lo_uH = Dbar_lo_hi(k+1)[0]   # Dbar(u) >= Dbar(uH) (decreasing on (0,u*))
    E = E_cell(k)
    H_lo = dbar_lo_uH - E.b - mp.mpf('25')
    if H_lo < worst:
        worst = H_lo
    assert H_lo > 0, ("FAIL cell", k, grid[k], grid[k+1], H_lo)
print("M1: min H over %d cells = " % N, mp.nstr(worst, 8), " (> 0)")

# ---- M4 ----
c = mp.mpf('2')
B2 = 3*mp.pi**2*R0/((1+4*mp.pi**2*c)*(1+mp.pi**2*c))
print("M4: B2(R0=1500), c=2 = ", mp.nstr(B2, 8), " (need >= 25)")
assert B2 > 25

# ---- M5 ----
v = mp.mpf('0.05')
bnd = 4*mp.pi**2 - mp.pi**2*R0/(R0 - 2*(R0-1)*v)
print("M5: right-sliver bound, v=0.05, R=1500 = ", mp.nstr(bnd, 8), " (need >= 25)")
assert bnd > 25

# ---- M6 ----
def a_of(u):
    f = lambda a: mp.tan(a) - a*(1 - mp.mpf(1)/(2*u))
    lo = mp.pi/2 + mp.mpf('1e-30'); hi = mp.pi - mp.mpf('1e-30')
    al, ah = lo, hi
    for k in range(1, 20000):
        x = lo + (hi-lo)*k/20000
        if f(x) > 0:
            ah = x; break
        al = x
    return mp.findroot(f, (al, ah))
def mu1bar(u): return mp.pi**2/(4*u**2)
def mu2bar(u):
    a = a_of(u); return (a/u)**2
def bisect(f, lo, hi, tol=mp.mpf('1e-26')):
    flo, fhi = f(lo), f(hi)
    assert (flo < 0 < fhi) or (fhi < 0 < flo)
    for _ in range(300):
        mid = (lo+hi)/2
        fm = f(mid)
        if fm == 0: return mid
        if (fm < 0) == (flo < 0):
            lo = mid; flo = fm
        else:
            hi = mid; fhi = fm
        if hi - lo < tol: return (lo+hi)/2
    return (lo+hi)/2
def gap_half(u, R):
    sR = mp.sqrt(R)
    m1b = mu1bar(u); m2b = mu2bar(u)
    f1 = lambda m: mp.cot(mp.sqrt(m)*u) - (1/sR)*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
    f2 = lambda m: mp.tan(mp.sqrt(m)*u) + sR*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
    m1 = bisect(f1, mp.mpf('1e-15'), m1b)
    m2 = bisect(f2, m1b*(1+mp.mpf('1e-15')), m2b)
    return m2 - m1
K = mp.mpf('50000')
Kmax = mp.mpf('-inf')
for u in [mp.mpf('0.1') + mp.mpf('0.375')*k/60 for k in range(61)]:
    for R in [R0, mp.mpf('1e4'), mp.mpf('1e6')]:
        g = gap_half(u, R)
        d = mu2bar(u) - mu1bar(u)
        val = abs(g - d)*R
        if val > Kmax: Kmax = val
print("M6: max |gap-Dbar|*R on [0.1,0.475] = ", mp.nstr(Kmax, 8), " (K=50000 ok:", Kmax < K, ")")
assert Kmax < K
print("PASS")