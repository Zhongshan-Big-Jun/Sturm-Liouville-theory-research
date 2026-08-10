import mpmath as mp
from mpmath import iv
iv.dps = 25
mp.mp.dps = 50
uL = mp.mpf('0.051639777949432225135723538663765328144438956070554478')
uH = mp.mpf('0.0518815790596850640100449209704465015037167612902017')
a = iv.mpf((mp.mpf('1.60'), mp.mpf('1.61')))
u = iv.mpf((uL, uH))
h = iv.mpf('0.5') - u
print("h =", h)
print("u^3 =", u**3)
print("a^2 h^2/u^2 =", a**2*h**2/u**2)
denom = u**3 * iv.mpf((mp.mpf('1500'), mp.mpf('1500'))) * (1 + a**2*h**2/u**2) * (1 - iv.mpf((mp.mpf('0.20'), mp.mpf('0.20'))))
print("denom =", denom)
delta = iv.mpf((mp.mpf('0.45'), mp.mpf('0.45')))*a**3*h**3/denom
print("delta =", delta)
E = 2*a*delta/u**2
print("E =", E)
# try the full cell with real a-brackets
def F_a_iv(aa, uu):
    return iv.tan(iv.mpf((aa, aa))) - iv.mpf((aa, aa))*(1 - 1/(2*iv.mpf((uu, uu))))
def a_root_iv(uu, scan=600):
    lo = mp.mpf('1.57079632679489661923132169163975144') + mp.mpf('1e-35')
    hi = mp.mpf('3.14159265358979323846264338327950288') - mp.mpf('1e-35')
    a_lo, a_hi = lo, hi
    for k in range(1, scan):
        x = lo + (hi-lo)*k/scan
        fx = F_a_iv(x, uu)
        if fx.a > 0:
            a_hi = x; break
        a_lo = x
    while a_hi - a_lo > mp.mpf('1e-18'):
        m = (a_lo+a_hi)/2
        fm = F_a_iv(m, uu)
        if fm.b < 0: a_lo = m
        else: a_hi = m
    return (a_lo, a_hi)
aL = a_root_iv(uL); aH = a_root_iv(uH)
print("a(uL) in", aL, " a(uH) in", aH)
a2 = iv.mpf((aL[0], aH[1]))
denom2 = u**3 * iv.mpf((mp.mpf('1500'), mp.mpf('1500'))) * (1 + a2**2*h**2/u**2) * (1 - iv.mpf((mp.mpf('0.20'), mp.mpf('0.20'))))
delta2 = iv.mpf((mp.mpf('0.45'), mp.mpf('0.45')))*a2**3*h**3/denom2
E2 = 2*a2*delta2/u**2
print("E with real a-bracket =", E2)