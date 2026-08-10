# -*- coding: utf-8 -*-
"""15_certify_region_d.py (v3, custom interval arctan via alternating series)
Rigorous interval-arithmetic certification of the deep-sliver elementary bounds.
arctan over [a,b] (0<=a<=b): arctan increasing, and for z in [0,1] the series
arctan(z)=sum (-1)^k z^(2k+1)/(2k+1) is alternating with decreasing terms, so
S_(2m+1)(z) <= arctan(z) <= S_(2m)(z); endpoint evaluation with directed rounding
gives a valid enclosure.  For b>1 use arctan(z)=pi/2-arctan(1/z).
  Region A: B1 >= 42744 (corner (1500,0.19), monotone)
  Region B: B2 >= 294.7 (corner (1500,0.19), monotone)
  Region C: B3 >= 25 at wcap exactly (monotone; iv check)
  Region D: G >= max(THB,D2B) >= 25 via 2D interval cells [1500,57050]x(0.5,2]
            plus analytic tail THB >= 0.10468 sqrt(R) for R >= 57050.
ASCII punctuation.
"""
import mpmath as mp
from mpmath import iv
iv.dps = 40
mp.mp.dps = 50

PI_LO = mp.mpf('3.14159265358979323846264338327950288419716939937510582097494')
PI_HI = mp.mpf('3.14159265358979323846264338327950288419716939937510582097495')
PI2_LO = mp.mpf('9.869604401089358618834490999876151135313699407240790626413349')
PI2_HI = mp.mpf('9.869604401089358618834490999876151135313699407240790626413350')
def iv_pi(): return iv.mpf([PI_LO, PI_HI])
def iv_pi2(): return iv.mpf([PI2_LO, PI2_HI])

M = 220  # alternating-series terms: tail <= 1/(4M+5) < 0.0012

def arctan_series_pt(x, m):
    """Interval enclosure of the partial sum S_m(x) = sum_{k=0}^m (-1)^k x^(2k+1)/(2k+1)."""
    xp = iv.mpf([x, x])
    s = iv.mpf([0, 0])
    term = xp
    for k in range(0, m+1):
        s = s + term/iv.mpf([2*k+1, 2*k+1])
        term = -term*xp*xp
    return s

def my_atan_iv(xint):
    """Valid interval enclosure of arctan over the interval xint (>= 0)."""
    a, b = xint.a, xint.b
    if a < 0:
        raise ValueError("my_atan_iv expects nonnegative interval")
    if b <= 1:
        lo = arctan_series_pt(a, 2*M+1).a   # S_odd(a) <= arctan(a)
        hi = arctan_series_pt(b, 2*M).b     # S_even(b) >= arctan(b)
        return iv.mpf([lo, hi])
    if a >= 1:
        inner = my_atan_iv(iv.mpf([1/b, 1/a]))
        return iv.mpf([iv_pi()/2 - inner.b, iv_pi()/2 - inner.a])
    # straddles 1
    lo1 = arctan_series_pt(a, 2*M+1).a
    hi1 = arctan_series_pt(1, 2*M).b
    inner = my_atan_iv(iv.mpf([1/b, 1]))
    lo2 = iv_pi()/2 - inner.b
    hi2 = iv_pi()/2 - inner.a
    return iv.mpf([min(lo1, lo2), max(hi1, hi2)])

def THB_iv(Riv, wiv):
    eps = 1/iv.sqrt(Riv)
    c = 1/(2*wiv) - eps
    z1 = iv.cot(c*iv_pi()/2)/eps
    t1m = my_atan_iv(z1)
    z2 = eps*iv.tan(c*t1m)
    t1p = iv_pi()/2 - my_atan_iv(z2)
    return (iv_pi()/2 - t1p)*(iv_pi()/2 + t1m)/(wiv*wiv*eps*eps)

def D2B_iv(Riv, wiv):
    eps = 1/iv.sqrt(Riv)
    x = iv_pi()/(4*wiv)
    c = 1/(2*wiv) - eps
    pm = iv_pi() - eps*iv.tan(x)
    if pm.b <= 0:
        return None
    z3 = iv.tan(x - eps*iv_pi()/2)/eps
    d2p = my_atan_iv(1/z3) if z3.a > 0 else None
    if d2p is None:
        return None
    arg = x - eps*iv_pi()/2 + c*d2p
    if arg.b >= iv_pi()/2:
        return None
    z4 = iv.tan(arg)/eps
    d2m = my_atan_iv(1/z4)
    return d2m*pm/(wiv*wiv*eps*eps)

# sanity: my_atan_iv vs known values
t = my_atan_iv(iv.mpf(['1.0','1.0']))
print("atan(1) enclosure:", t, " (pi/4 =", mp.nstr(mp.pi/4, 10), ")")
assert t.a < mp.pi/4 < t.b
t2 = my_atan_iv(iv.mpf(['0.5','0.55']))
print("atan([0.5,0.55]) in", t2)
assert t2.b < mp.pi/4

# --- Region D cells ---
RLO = mp.mpf('1500'); RHI = mp.mpf('57050')
NW = 100
wlo, whi = mp.mpf('0.5'), mp.mpf('2.0')
ratio = mp.mpf('1.01')
Rs = [RLO]
while Rs[-1] < RHI:
    Rs.append(min(Rs[-1]*ratio, RHI))
worst = mp.inf; worst_at = None
ncells = 0
for i in range(len(Rs)-1):
    Riv = iv.mpf([Rs[i], Rs[i+1]])
    for j in range(NW):
        wa = wlo + (whi-wlo)*j/NW
        wb = wlo + (whi-wlo)*(j+1)/NW
        wiv = iv.mpf([wa, wb])
        th = THB_iv(Riv, wiv)
        d2 = D2B_iv(Riv, wiv)
        v = th.a if d2 is None else max(th.a, d2.a)
        ncells += 1
        if v < worst:
            worst = v; worst_at = (Rs[i], Rs[i+1], wa, wb)
        assert v > 25, ("region-D cell fail", i, j, Rs[i], Rs[i+1], wa, wb, th, d2)
print("Region D cells: %d cells; min lower bound = %s at %s (need > 25)" % (
    ncells, mp.nstr(worst, 8), worst_at))

eps0 = 1/mp.sqrt(RLO)
C = mp.tan(mp.pi/16 - eps0*mp.pi/4)*mp.mpf('0.75')*mp.pi*(1 - eps0*eps0/3)/4
print("tail C =", mp.nstr(C, 10), "; C*sqrt(57050) =", mp.nstr(C*mp.sqrt(RHI), 8))
assert C*mp.sqrt(RHI) > 25

def B1_iv(Riv, wiv):
    eps = 1/iv.sqrt(Riv)
    c = 1/(2*wiv) - eps
    return 3*iv_pi2()*Riv - 32*iv_pi()**4*Riv*eps*wiv*wiv/c
def B2_iv(Riv, wiv):
    eps = 1/iv.sqrt(Riv)
    return iv_pi2()*Riv*((1-2*eps*wiv)**-2 - 1)
def B3_iv(Riv, wiv):
    eps = 1/iv.sqrt(Riv)
    return iv_pi2()*Riv*(1/(4*wiv*wiv) - 1)

b1 = B1_iv(iv.mpf(['1500','1500']), iv.mpf(['0.19','0.19']))
print("B1(1500,0.19) in", b1)
assert b1.a > 25
b2 = B2_iv(iv.mpf(['1500','1500']), iv.mpf(['0.19','0.19']))
print("B2(1500,0.19) in", b2)
assert b2.a > 25
wcap = mp.mpf('0.5')*(1 + 25/PI2_LO)**-mp.mpf('0.5')
b3 = B3_iv(iv.mpf(['1500','1500']), iv.mpf([wcap, wcap]))
print("B3(1500, wcap) in", b3, " wcap =", mp.nstr(wcap, 10))
assert b3.a >= 25
print("PASS")

