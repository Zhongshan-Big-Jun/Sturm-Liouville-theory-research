# -*- coding: utf-8 -*-
"""17_certify_medium_region.py (v4, manager continuation, delta-bracketing)
Independent computer-assisted certification of the medium-sliver region:
    G(R,u) = mu2(R,u) - mu1(R,u) >= 25  for R in [1500,1e8], u in [0.02,0.2], w = u*sqrt(R) >= 2.
Cells with w < 2 are covered by the deep-sliver certification (script 16) and
cells with w >= 2 are covered analytically by Lemma A'' (G >= Dbar >= 29.2).
This script certifies the w >= 2 part by a monotone-corner scheme as an
independent check.
For w >= 2: theta1 = pi/2 - delta1 with delta1 in (0, pi/4) solving
    tan delta1 = eps*tan(z1),  z1 = (pi/2 - delta1)*ell*eps/u,  ell = 1/2 - u;
theta2 = pi/2 + delta2 with delta2 in (0, delta2+) solving
    tan delta2 = eps*cot(z2),  z2 = (pi/2 + delta2)*ell*eps/u.
Proven brackets (no tan-pole issues):
    delta1 in [delta1m, delta1p], delta1m = (pi/2)*ell*eps^2/(u+ell*eps^2),
    delta1p = arctan(eps*tan((pi/2)*ell*eps/u));
    delta2 in [0, delta2p], delta2p = arctan(2u/(pi*ell)).
mu1 = ((pi/2-delta1)/u)^2 is decreasing in delta1, mu2 = ((pi/2+delta2)/u)^2
increasing in delta2; the corner bound uses mu1 upper and mu2 lower.
FH monotonicity (d mu_k/du < 0, d mu_k/dR > 0, both proven) gives on each cell
    G(R,u) >= mu2(R1,u2) - mu1(R2,u1).
Computer-assisted proof certificate.  ASCII punctuation.
"""
import math, time

def dwn(x): return math.nextafter(x, -math.inf)
def upr(x): return math.nextafter(x, math.inf)

class Iv:
    __slots__ = ('a','b')
    def __init__(self, a, b): self.a = float(a); self.b = float(b)
    @staticmethod
    def pt(x): return Iv(x, x)
    def __add__(self, o): return Iv(dwn(self.a+o.a), upr(self.b+o.b))
    def __sub__(self, o): return Iv(dwn(self.a-o.b), upr(self.b-o.a))
    def __neg__(self): return Iv(-self.b, -self.a)
    def __mul__(self, o):
        p = [self.a*o.a, self.a*o.b, self.b*o.a, self.b*o.b]
        return Iv(dwn(min(p)), upr(max(p)))
    def __truediv__(self, o):
        if o.a <= 0.0 <= o.b: raise ValueError('div by 0-containing interval')
        p = [self.a/o.a, self.a/o.b, self.b/o.a, self.b/o.b]
        return Iv(dwn(min(p)), upr(max(p)))
    def __repr__(self): return '[%.12g, %.12g]' % (self.a, self.b)

HALFPI = 1.5707963267948966
def sqrt_iv(x): return Iv(dwn(math.sqrt(x.a)), upr(math.sqrt(x.b)))
def atan_iv(x): return Iv(dwn(math.atan(x.a)), upr(math.atan(x.b)))
def tan_iv(x):
    assert x.b < HALFPI - 1e-9, x
    return Iv(dwn(math.tan(x.a)), upr(math.tan(x.b)))
def cot_iv(x):
    assert 0 < x.a and x.b < HALFPI, x
    return Iv(dwn(math.cos(x.b)/math.sin(x.b)), upr(math.cos(x.a)/math.sin(x.a)))

def g1_iv(delta, R, u):
    eps = Iv.pt(1.0)/sqrt_iv(Iv.pt(R))
    ell = Iv.pt(0.5) - Iv.pt(u)
    z = (Iv.pt(HALFPI) - delta)*ell*eps/Iv.pt(u)
    return tan_iv(delta) - eps*tan_iv(z)
def g2_iv(delta, R, u):
    eps = Iv.pt(1.0)/sqrt_iv(Iv.pt(R))
    ell = Iv.pt(0.5) - Iv.pt(u)
    z = (Iv.pt(HALFPI) + delta)*ell*eps/Iv.pt(u)
    return tan_iv(delta) - eps*cot_iv(z)

def bisect(F, lo, hi, tol=1e-13):
    for _ in range(200):
        if hi - lo <= tol:
            break
        mid = (lo+hi)/2
        fm = F(Iv.pt(mid))
        if fm.b < 0:
            lo = mid
        elif fm.a > 0:
            hi = mid
        else:
            break
    return lo, hi

def enclose_mu1(R, u):
    eps = 1.0/math.sqrt(R); ell = 0.5-u
    dm = (HALFPI)*ell*eps*eps/(u + ell*eps*eps)
    dp = math.atan(eps*math.tan(HALFPI*ell*eps/u))
    # verify brackets are sign-separated
    glm = g1_iv(Iv.pt(dm), R, u); gup = g1_iv(Iv.pt(dp), R, u)
    assert glm.b < 0 < gup.a, (R, u, 'g1 brackets', glm, gup)
    dlo, dhi = bisect(lambda d: g1_iv(d, R, u), dm, dp)
    # mu1 decreasing in delta1: upper bound uses dlo
    mu_hi = ((HALFPI-dlo)/u)**2
    mu_lo = ((HALFPI-dhi)/u)**2
    return mu_lo, mu_hi

def enclose_mu2(R, u):
    ell = 0.5-u
    dp = math.atan(2*u/(HALFPI*ell))
    glm = g2_iv(Iv.pt(0.0), R, u); gup = g2_iv(Iv.pt(dp), R, u)
    assert glm.b < 0 < gup.a, (R, u, 'g2 brackets', glm, gup)
    dlo, dhi = bisect(lambda d: g2_iv(d, R, u), 0.0, dp)
    # mu2 increasing in delta2: lower bound uses dlo
    mu_lo = ((HALFPI+dlo)/u)**2
    mu_hi = ((HALFPI+dhi)/u)**2
    return mu_lo, mu_hi

m1lo, m1hi = enclose_mu1(1500.0, 0.1)
m2lo, m2hi = enclose_mu2(1500.0, 0.1)
print('mu1(1500,0.1) in [%.8f, %.8f]' % (m1lo, m1hi))
print('mu2(1500,0.1) in [%.8f, %.8f]' % (m2lo, m2hi))
assert abs(m1lo-245.41790401) < 1e-4 and abs(m2lo-293.82303039) < 1e-4

# large-R sanity: mu1 must approach pi^2/(4u^2) from below
m1lo, m1hi = enclose_mu1(1e8, 0.2)
print('mu1(1e8,0.2) in [%.8f, %.8f], mu1bar=%.8f' % (m1lo, m1hi, 9.869604401089358/(4*0.04)))
assert m1hi < 9.869604401089358/(4*0.04) + 1e-3 and m1lo > 9.869604401089358/(4*0.04) - 1e-2

t0 = time.time()
R0, R1 = 1500.0, 1e8
ratio1 = 1.01; ratio2 = 1.02
Rs = [R0]
while Rs[-1] < 1e4:
    Rs.append(min(Rs[-1]*ratio1, 1e4))
while Rs[-1] < R1:
    Rs.append(min(Rs[-1]*ratio2, R1))
Us = []
u = 0.02
while u < 0.03 - 1e-12:
    Us.append(u); u += 0.0002
while u < 0.05 - 1e-12:
    Us.append(u); u += 0.0005
while u < 0.10 - 1e-12:
    Us.append(u); u += 0.001
while u <= 0.20 + 1e-12:
    Us.append(u); u += 0.002
print('grid: %d R-cells, %d u-points' % (len(Rs)-1, len(Us)))

cache1 = {}; cache2 = {}
def mu1_at(i, j):
    key = (i, j)
    if key not in cache1:
        cache1[key] = enclose_mu1(Rs[i], Us[j])
    return cache1[key]
def mu2_at(i, j):
    key = (i, j)
    if key not in cache2:
        cache2[key] = enclose_mu2(Rs[i], Us[j])
    return cache2[key]

worst = float('inf'); worst_at = None; ncells = 0; skipped = 0
for i in range(len(Rs)-1):
    for j in range(len(Us)-1):
        if Us[j]*math.sqrt(Rs[i]) < 2.0:
            skipped += 1
            continue
        m2lo, _ = mu2_at(i, j+1)
        _, m1hi = mu1_at(i+1, j)
        v = m2lo - m1hi
        ncells += 1
        if v < worst:
            worst = v; worst_at = (Rs[i], Rs[i+1], Us[j], Us[j+1])
        if v < 25.0:
            print('FAIL cell', (Rs[i], Rs[i+1], Us[j], Us[j+1]), 'bound', v)
            raise SystemExit(1)
print('medium region w>=2: PASS; cells=%d skipped(w<2)=%d worst corner bound = %.6f at %s' % (
    ncells, skipped, worst, worst_at))
print('time %.1f s' % (time.time()-t0))
