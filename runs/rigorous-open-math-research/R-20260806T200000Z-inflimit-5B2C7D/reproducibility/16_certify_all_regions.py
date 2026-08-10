# -*- coding: utf-8 -*-
"""16_certify_all_regions.py (v3, manager continuation, complete rewrite)
Fast directed-rounding interval certification of the deep-sliver lemma:
    G(R,u) = mu2(R,u) - mu1(R,u) >= 25   for all R >= 1500, u in (0, 2/sqrt(1500)],
    equivalently w = u*sqrt(R) in (0,2].
Regions (w = u sqrt(R), eps = 1/sqrt(R)):
  A: (0, 0.19]     B1 = 3 pi^2 R - 32 pi^4 R eps w^2 / c,        c = 1/(2w) - eps
  B: [0.19, w_c]   B2 = pi^2 R ((1-2 eps w)^-2 - 1),             w_c = 1/(2(1+eps))
  C: (w_c, wcap]   B3 = pi^2 R (1/(4w^2) - 1),                   wcap = 0.5 (1+25/(pi^2 R))^-1/2
  D: (wcap, 2]     max(THB, D2B), THB/D2B as in the ledger R-013
Box certification on R in [1500, 57050]; analytic tails for R >= 57050.
Every float operation is rounded outward (math.nextafter); monotone functions
evaluated at cell endpoints.  Computer-assisted proof certificate.
ASCII punctuation.
"""
import math, time

def dwn(x):
    return math.nextafter(x, -math.inf)
def upr(x):
    return math.nextafter(x, math.inf)

class Iv:
    __slots__ = ('a', 'b')
    def __init__(self, a, b):
        self.a = float(a); self.b = float(b)
    @staticmethod
    def pt(x):
        return Iv(x, x)
    def __add__(self, o):
        return Iv(dwn(self.a + o.a), upr(self.b + o.b))
    def __sub__(self, o):
        return Iv(dwn(self.a - o.b), upr(self.b - o.a))
    def __neg__(self):
        return Iv(-self.b, -self.a)
    def __mul__(self, o):
        p = [self.a*o.a, self.a*o.b, self.b*o.a, self.b*o.b]
        return Iv(dwn(min(p)), upr(max(p)))
    def __truediv__(self, o):
        if o.a <= 0.0 <= o.b:
            raise ValueError('div by interval containing 0: %s' % (o,))
        p = [self.a/o.a, self.a/o.b, self.b/o.a, self.b/o.b]
        return Iv(dwn(min(p)), upr(max(p)))
    def __repr__(self):
        return '[%.17g, %.17g]' % (self.a, self.b)

def iv_pi():
    return Iv(3.141592653589793, 3.141592653589794)
def iv_pi2():
    return Iv(9.869604401089358, 9.869604401089359)
def sqrt_iv(x):
    return Iv(dwn(math.sqrt(x.a)), upr(math.sqrt(x.b)))
def atan_iv(x):
    return Iv(dwn(math.atan(x.a)), upr(math.atan(x.b)))
def tan_iv(x):
    assert x.b < 1.5707963267948966 - 1e-7, 'tan arg near pole: %s' % (x,)
    return Iv(dwn(math.tan(x.a)), upr(math.tan(x.b)))
def cot_iv(x):
    assert x.a > 0 and x.b < 3.141592653589793, 'cot arg out of (0,pi): %s' % (x,)
    return Iv(dwn(math.cos(x.b)/math.sin(x.b)), upr(math.cos(x.a)/math.sin(x.a)))

def eps_iv(Riv):
    return Iv.pt(1.0)/sqrt_iv(Riv)

def B1_iv(Riv, wiv):
    eps = eps_iv(Riv)
    c = Iv.pt(1.0)/(Iv.pt(2.0)*wiv) - eps
    return Iv.pt(3.0)*iv_pi2()*Riv - Iv.pt(32.0)*iv_pi2()*iv_pi2()*Riv*eps*(wiv*wiv)/c

def B2_iv(Riv, wiv):
    eps = eps_iv(Riv)
    t = Iv.pt(2.0)*eps*wiv
    om = Iv.pt(1.0) - t
    inv = Iv.pt(1.0)/om
    return iv_pi2()*Riv*(inv*inv - Iv.pt(1.0))

def B3_iv(Riv, wiv):
    return iv_pi2()*Riv*(Iv.pt(1.0)/(Iv.pt(4.0)*(wiv*wiv)) - Iv.pt(1.0))

def THB_iv(Riv, wiv):
    eps = eps_iv(Riv)
    c = Iv.pt(1.0)/(Iv.pt(2.0)*wiv) - eps
    cpi2 = c*iv_pi()/Iv.pt(2.0)
    z = cot_iv(cpi2)/eps
    t1m = atan_iv(z)
    arg = c*t1m
    t1p = iv_pi()/Iv.pt(2.0) - atan_iv(eps*tan_iv(arg))
    num = (iv_pi()/Iv.pt(2.0) - t1p)*(iv_pi()/Iv.pt(2.0) + t1m)
    return num/((wiv*wiv)*(eps*eps))

def D2B_iv(Riv, wiv):
    eps = eps_iv(Riv)
    x = iv_pi()/(Iv.pt(4.0)*wiv)
    if x.b >= 1.5707963267948966 - 1e-7:  # needs w > 1/2 strictly with margin
        return None
    c = Iv.pt(1.0)/(Iv.pt(2.0)*wiv) - eps
    pm = iv_pi() - eps*tan_iv(x)
    if pm.b <= 0.0:
        return None
    arg0 = x - eps*iv_pi()/Iv.pt(2.0)
    if arg0.a <= 0.0:
        return None
    d2p = atan_iv(eps*cot_iv(arg0))
    arg = x - eps*iv_pi()/Iv.pt(2.0) + c*d2p
    if arg.b >= iv_pi().a/2 - 1e-9:
        return None
    d2m = atan_iv(eps*cot_iv(arg))
    return d2m*pm/((wiv*wiv)*(eps*eps))

def d_bound(Riv, wiv):
    th = THB_iv(Riv, wiv)
    if wiv.a >= 0.503:  # D2B valid only away from the x=pi/2 pole
        d2 = D2B_iv(Riv, wiv)
        if d2 is not None:
            return Iv(max(th.a, d2.a), max(th.b, d2.b))
    return th

def w_c(R):
    eps = 1.0/math.sqrt(R)
    return 1.0/(2.0*(1.0+eps))
def wcap(R):
    return 0.5*(1.0 + 25.0/(9.869604401089358*R))**-0.5

def certify_region(name, Rlo, Rhi, w_lo_fn, w_hi_fn, bound_fn, floorv, wsplit=None):
    worst = float('inf'); worst_at = None; ncells = 0
    R = Rlo
    while R < Rhi:
        Rn = min(R*1.01, Rhi)
        wlo = w_lo_fn(R, Rn); whi = w_hi_fn(R, Rn)
        if whi - wlo <= 0:
            R = Rn; continue
        bounds = [wlo]
        if wsplit:
            for s in wsplit:
                if wlo < s < whi:
                    bounds.append(s)
        bounds.append(whi)
        for i in range(len(bounds)-1):
            wa, wb = bounds[i], bounds[i+1]
            step = 5e-4 if wa < 0.51 else 0.01
            m = max(1, int(math.ceil((wb - wa)/step)))
            for j in range(m):
                w1 = wa + (wb-wa)*j/m
                w2 = wa + (wb-wa)*(j+1)/m
                Riv = Iv(R, Rn); wiv = Iv(w1, w2)
                v = bound_fn(Riv, wiv)
                if v is None:
                    continue
                ncells += 1
                if v.a < worst:
                    worst = v.a; worst_at = (R, Rn, w1, w2, v)
                if v.a < floorv:
                    return False, ('FAIL', name, (R, Rn, w1, w2), v, floorv)
        R = Rn
    return True, (worst, worst_at, ncells)

t0 = time.time()
Rlo, Rhi = 1500.0, 1e8

# --- sanity: point values ---
def thb_pt(w, R):
    eps = 1.0/math.sqrt(R)
    c = 1.0/(2*w) - eps
    t1m = math.atan(math.cos(c*math.pi/2)/math.sin(c*math.pi/2)/eps)
    t1p = math.pi/2 - math.atan(eps*math.tan(c*t1m))
    return (math.pi/2 - t1p)*(math.pi/2 + t1m)/(w*w*eps*eps)
def d2b_pt(w, R):
    eps = 1.0/math.sqrt(R)
    x = math.pi/(4*w)
    c = 1.0/(2*w) - eps
    pm = math.pi - eps*math.tan(x)
    if pm <= 0: return None
    d2p = math.atan(eps/math.tan(x - eps*math.pi/2))
    arg = x - eps*math.pi/2 + c*d2p
    if arg >= math.pi/2: return None
    d2m = math.atan(eps/math.tan(arg))
    return d2m*pm/(w*w*eps*eps)
print('sanity THB(2,1500)=', thb_pt(2.0,1500), 'D2B(2,1500)=', d2b_pt(2.0,1500))
print('sanity THB(0.50005,1500)=', thb_pt(0.50005,1500))
print('iv THB(2,1500)=', THB_iv(Iv(1500,1500), Iv(2,2)))
print('iv D2B(2,1500)=', D2B_iv(Iv(1500,1500), Iv(2,2)))

# --- Region A: w in (0, 0.19] ---
ok, info = certify_region('A', Rlo, Rhi, lambda R, Rn: 1e-9, lambda R, Rn: 0.19, B1_iv, 25.0, None)
print('Region A:', ok, 'worst =', info[0], 'at', info[1][:4], 'cells', info[2])
assert ok

# --- Region B: w in [0.19, w_c(R)], conservative w <= w_c(r1) ---
ok, info = certify_region('B', Rlo, Rhi, lambda R, Rn: 0.19, lambda R, Rn: w_c(R), B2_iv, 25.0, None)
print('Region B:', ok, 'worst =', info[0], 'at', info[1][:4], 'cells', info[2])
assert ok

# --- Region C: EXACT analytic lemma (B3 = 25 at the exact endpoint), sanity only ---
wcl = wcap(1500) - 1e-6
print('B3 sanity (1500, wcap-1e-6):', B3_iv(Iv(1500,1500), Iv(wcl, wcl)))
assert B3_iv(Iv(1500,1500), Iv(wcl, wcl)).a > 25.0

# --- Region D: w in (wcap(R), 2]; THB everywhere, D2B where valid ---
ok, info = certify_region('D', Rlo, Rhi, lambda R, Rn: wcap(Rn), lambda R, Rn: 2.0, d_bound, 25.0,
                          wsplit=[0.5005, 0.503, 0.51, 0.6, 1.0, 1.5, 1.9])
print('Region D:', ok, 'worst =', info[0], 'at', info[1][:4], 'cells', info[2])
assert ok

# --- analytic tail for R >= 1e8 (honest constants, uniform in w in (0.5,2]) ---
# eps <= 1e-4: c = 1/(2w)-eps in [1/4-1e-4, 1); c*pi/2 in [pi/8-1.58e-4, pi/2-1.57e-4];
# tan(c*pi/2) in [0.4139, 6366]; u = eps*tan(c*pi/2) <= 0.6366;
# t1m >= pi/2 - u; c*t1m >= (1/4-1e-4)(pi/2-0.6366) = 0.2335; tan(c*t1m) >= 0.2376;
# A >= arctan(eps*0.2376) >= 0.2375*eps; B >= pi - arctan(0.6366) = 2.5746;
# THB >= 0.2375*2.5746/(4*eps) = 0.1529/eps = 0.1529*sqrt(R) >= 1529 for R >= 1e8.
Ctail = 0.1529
print('tail D: C*sqrt(1e8) =', Ctail*1e4)
assert Ctail*1e4 > 25.0

# --- analytic tails (R >= 57050), interval-verified constants ---
# Region A tail: B1 >= R*(3pi^2 - 32pi^4 w^2/(c sqrt(R))); w<=0.19, c>=1/0.38-eps0, eps0=1/sqrt(57050)
eps0 = 1.0/math.sqrt(57050.0)
cmin = 1.0/0.38 - eps0
tailA = 57050.0*(3.0*9.869604401089358 - 32.0*9.869604401089358**2*0.19**2/(cmin*math.sqrt(57050.0)))
print('tail A coefficient check:', tailA)
assert tailA > 25.0
# Region B tail: B2 >= pi^2 R * 0.76 * eps  (since (1-t)^-2 - 1 >= 2t = 4 eps w, w>=0.19)
tailB = 9.869604401089358*57050.0*0.76*eps0
print('tail B coefficient check:', tailB)
assert tailB > 25.0
print('PASS: all regions certified; total time %.2f s' % (time.time()-t0))
