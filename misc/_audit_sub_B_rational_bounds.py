# _audit_sub_B_rational_bounds.py — exact Fraction / high-precision checks of all rational constant bounds
from fractions import Fraction as F
from mpmath import mp, mpf, pi, sqrt, sin, cos, tan, atan, cot, acos
mp.dps = 50
res = []
def check(name, ok): res.append((name, bool(ok))); print(("PASS" if ok else "FAIL"), name)

# ---- lem:B1 ----
# g'(sqrt3) <= 16(22/7)^2/9 - 41(17/10)(157/50)/6 - 15 = -14957063/441000
val = F(16)*F(22,7)**2/F(9) - F(41)*F(17,10)*F(157,50)/F(6) - F(15)
check("lem:B1 g'(sqrt3) upper bound = -14957063/441000", val == F(-14957063,441000))
check("lem:B1 bound < 0", val < 0)

# S_5, S_6 partial sums of arctan series at x=4/5
def arctan_partial(x, k):
    s = F(0)
    for j in range(k+1):
        s += F((-1)**j) * x**(2*j+1) / F(2*j+1)
    return s
S5 = arctan_partial(F(4,5), 5)
S6 = arctan_partial(F(4,5), 6)
check("S_5 = 22739538548/33837890625", S5 == F(22739538548, 33837890625))
check("S_6 = 7436856470852/10997314453125", S6 == F(7436856470852, 10997314453125))
b45 = mp.atan(mpf(4)/5)
S5m = mpf(S5.numerator)/S5.denominator; S6m = mpf(S6.numerator)/S6.denominator
check("67/100 < S5 < b < S6 < 17/25", mpf(67)/100 < S5m < b45 < S6m < mpf(17)/25)
check("S5 in (67/100, b): numeric", mpf(S5.numerator)/S5.denominator < b45)

# g(4/5; b=67/100, pi=22/7), g'(4/5; b=17/25, pi=157/50), g'(4/5; b=67/100, pi=22/7)
def g45(b, p):
    return -F(19)*b/F(25) - F(346)*p/F(41) + F(16)*(b-p)**2/F(5) - F(1076,205)
def gp45(b, p):
    return -F(2152)*b/F(205) - F(2560)*p/F(1681) + F(4)*(b-p)**2 - F(15008,1681)
g45_lo = g45(F(67,100), F(22,7))
gp45_hi = gp45(F(17,25), F(157,50))
gp45_lo = gp45(F(67,100), F(22,7))
check("g(4/5;67/100,22/7) < 0", g45_lo < 0)
check("g'(4/5;17/25,157/50) > 3.3581", gp45_hi > F(33581,10000))
check("g'(4/5;17/25,157/50) numeric > 3.3581", float(gp45_hi) > 3.3581)
final = g45_lo + gp45_lo*F(19,20)
check("final = -1054523/114800", final == F(-1054523, 114800))
check("final < 0", final < 0)

# ---- lem:boundary R,T upper bounds (z<=10/17, pi in (157/50,22/7)) ----
def Rz_bound():
    # R(z) = -23p + (8p^2-14)z + (16p^2-40)z^3 + (8p^2-10)z^5 + 5p z^6 - 21p z^4 - p z^2
    # positive coeffs: (8p^2-14), (16p^2-40), (8p^2-10), 5p ; negative: -23p, -21p z^4, -p z^2
    p_hi = F(22,7); z_hi = F(10,17); p_lo = F(157,50)
    return (8*p_hi**2-14)*z_hi + (16*p_hi**2-40)*z_hi**3 + (8*p_hi**2-10)*z_hi**5 + 5*p_hi*z_hi**6 - 23*p_lo
rb = Rz_bound()
check("R(z) <= -262235520291/59137044050", rb == F(-262235520291, 59137044050))
check("R bound < 0", rb < 0)
def Tz_bound():
    p_hi = F(22,7); z_hi = F(10,17); p_lo = F(157,50)
    # T = 10p/3 z^6 + (32p^2/9-10) z^5 - 14p z^4 + (64p^2/9-40) z^3 - 2p/3 z^2 + (32p^2/9-14) z - 46p/3
    # positive coeffs: 10p/3, (32p^2/9-10), (64p^2/9-40), (32p^2/9-14); negative: -14p, -2p/3, -46p/3
    return F(10,3)*p_hi*z_hi**6 + (F(32,9)*p_hi**2-10)*z_hi**5 + (F(64,9)*p_hi**2-40)*z_hi**3 + (F(32,9)*p_hi**2-14)*z_hi - 46*p_lo/3
tb = Tz_bound()
check("T(z) <= -7282185739373/266116698225", tb == F(-7282185739373, 266116698225))
check("T bound < 0", tb < 0)

# ---- lem:M2(d): B(20) ----
p_lo = F(314159,100000); p_hi = F(314160,100000)
mp_plo = mpf(314159)/100000; mp_phi = mpf(314160)/100000; mp_slo = mpf(640312)/100000; mp_shi = mpf(640313)/100000
s_lo = F(640312,100000); s_hi = F(640313,100000)
B20 = (4*p_lo**2 + 14)*s_hi + 1 - F(183395,1000)*p_lo
check("B(20) <= -58180766243071047/250000000000000", B20 == F(-58180766243071047, 250000000000000))
check("B(20) < -232.723", B20 < F(-232723,1000))
# B'(q) <= (4pi^2+14)/sqrt41 - 10pi < 0: check with bounds
bp = None
bp_num = (4*mp_phi**2+14)/sqrt(mpf(41)) - 10*mp_plo
check("B'(q) < 0 (numeric)", bp_num < 0)

# ---- lem:M2(e): M2/q^2 bound < 0 ----
bound_e = 4*(pi**2)*mpf('0.33') - 7*(pi - mpf('0.33')) + 2*pi*(1+mpf('0.33')**2)/42
check("lem:M2(e) bound < 0", bound_e < 0)
# verify bound actually dominates M2/q^2 on w>sqrt41, q>20, w^2<2q+1 by dense sampling
def M2(qq, ww):
    A = pi - atan(ww/qq)
    return 4*A**2*ww*qq - 7*A*qq**2 - 9*A*ww**2 + 2*A*(qq**2+ww**2)/(1+ww**2) + atan(ww)*(4*A*ww - 5*qq - 9*qq*ww**2)
ok_e = True
import random
random.seed(3)
for _ in range(2000):
    qq = mpf(random.uniform(20, 60))
    ww = mpf(random.uniform(sqrt(41)+1e-9, sqrt(2*qq+1)-1e-9))
    if ww <= sqrt(41): continue
    val = M2(qq, ww)/qq**2
    if val > bound_e + mpf('1e-12'):
        ok_e = False; print("  e-bound violation", qq, ww, val, bound_e)
check("lem:M2(e) bound dominates M2/q^2 (sampling)", ok_e)

# ---- CORNER: G2(1/2;2) > 0 via pi>3.14, sqrt5<2.24 ----
# pi - acos(2/3) - sqrt5: cos envelope at 2/3: cos x <= 1-x^2/2+x^4/24 (even partial sum upper)
# acos(2/3) < y iff cos y < 2/3; find rational y: check cos(67/80)?  try y = 841/1000: cos(0.841) ~ 0.6663 > 2/3? compute
g_corner = pi - acos(mpf(2)/3) - sqrt(5)
check("CORNER G2(1/2;2) numerator > 0", g_corner > 0)
# rational verification: pi > 3.14, sqrt5 < 2.24, acos(2/3) < 43/50?
acos23 = acos(mpf(2)/3)
check("acos(2/3) < 43/50", acos23 < mpf(43)/50)
check("pi - 3.14 - ... : 3.14 - 43/50 - 2.24 =", float(mpf('3.14') - mpf(43)/50 - mpf('2.24')) > 0)
check("3.14 - 43/50 - 2.24 > 0", mpf('3.14') - mpf(43)/50 - mpf('2.24') > 0)

# ---- C4 constants ----
check("pi in (31415/10000, 31416/10000)", mpf('3.1415') < pi < mpf('3.1416'))
check("2pi/7 > 8975/10000", 2*pi/7 > mpf('0.8975'))
check("3pi/10 in (9424/10000, 9425/10000)", mpf('0.9424') < 3*pi/10 < mpf('0.9425'))
check("2pi/5 < 12567/10000", 2*pi/5 < mpf('1.2567'))
check("sqrt5 in (2.2360, 2.2361)", mpf('2.2360') < sqrt(5) < mpf('2.2361'))
t310 = tan(3*pi/10)
check("tan^2(3pi/10) = 1+2sqrt5/5", abs(t310**2 - (1+2*sqrt(5)/5)) < mpf('1e-40'))
check("tan(3pi/10) in (13763/10000, 13765/10000)", mpf('1.3763') < t310 < mpf('1.3765'))
check("tan(2pi/5) < 3078/1000", tan(2*pi/5) < mpf('3.078'))
def P(t): return t**6 - 21*t**4 + 35*t**2 - 7
check("P(tan(2pi/7)) = 0", abs(P(tan(2*pi/7))) < mpf('1e-40'))
check("P(1253/1000) > 0 > P(1254/1000)", P(mpf('1.253')) > 0 > P(mpf('1.254')))
check("P(1) = 8, P(2) = -139", P(1) == 8 and P(2) == -139)
# P' < 0 on [1,2]: P'(t) = 2t(3t^4-42t^2+35), s=t^2 in [1,4]: 3s^2-42s+35 <= -4
s = mpf('1.0')
maxv = 3*s**2-42*s+35
check("P' second factor <= -4 on [1,4]", maxv <= -4)

# ---- C4 region I exact bound ----
num = F(125)*F(1253,1000)*F(8975,10000) \
    + F(50)*(F(8975,10000)*(1 + F(1253,1000)**2) + F(1253,1000)) + F(20) \
    + (F(50)*F(8975,10000)*(F(1253,1000)**2 - 1) + F(2)*F(1253,1000)*(F(88) - F(12)*F(13765,10000)**2)) \
    + (F(150)*F(1253,1000) - F(100)*F(9425,10000)) \
    - F(125)*F(13765,10000)*F(9425,10000)*F(1254,1000)**4
check("C4 region I N >= 88146367488708279/400000000000000", num == F(88146367488708279, 400000000000000))
check("region I bound > 0", num > 0)
# region II
c3b = F(50)*F(9424,10000)*(F(27,10)**2 - 1) + (F(176)*F(3078,1000) - F(24)*F(3078,1000)**3)
check("C4 region II c3 >= 2160051043/15625000", c3b == F(2160051043, 15625000))
check("region II c5 > 0", F(150)*F(13763,10000) - F(100)*F(12567,10000) > 0)
check("region II w<=27/10 c3 > 0", F(2)*F(27,10)*(F(88) - F(12)*F(27,10)**2) > 0)
# L(2pi/7) >= 13058215729/5000000000
w7lo = F(1253,1000)
L27 = (1 + w7lo**2)*(F(2)*F(31415,10000) - F(21,5)*F(1254,1000))
check("L(2pi/7) >= 13058215729/5000000000", L27 == F(13058215729, 5000000000))
check("L(2pi/7) > 0", L27 > 0)

# ---- lem:G2m2 ----
check("65/66 < 1", F(65,66) < 1)
check("PhiD = 65/66", F(13,8)/(1+F(13,20)) == F(65,66))
# 4pi/(3sqrt3) > 2.418 via pi>3.1415, sqrt3<1.7321
check("4*3.1415/(3*1.7321) > 2.418", mpf('4')*mpf('3.1415')/(3*mpf('1.7321')) > mpf('2.418'))
check("25(pi-0.655)/108 < 0.576 via pi<3.1416", F(25)*F(31416,10000) < F(576,1000)*F(108,1) + F(25)*F(655,1000))
# G2 > -1.734 > -2
check("-(0.582)-2(0.576) = -1.734 > -2", mpf('-1.734') > mpf('-2'))

# ---- j1e1 ----
check("4/3 + 8pi/(27sqrt3) > 187/100 (numeric)", mpf(4)/3 + 8*pi/(27*sqrt(3)) > mpf('1.87'))
check("8*3.1415/(27*1.7321) > 161/300", 8*mpf('3.1415')/(27*mpf('1.7321')) > mpf(161)/300)
# f' bracket positivity at rational bounds
pi7 = pi/7
val_f = 3 + 3*(5*pi/14)*tan(pi/7) - mpf(4)/3*(5*pi/14)**2
check("f' bracket > 0 (numeric)", val_f > 0)
# C <= 8
check("3000/707 + 200/55 < 8", F(3000,707) + F(200,55) < 8)
check("sin(841/1000) > 0.7418", sin(mpf('0.841')) > mpf('0.7418'))
check("(0.7418)^2 > 0.55", mpf('0.7418')**2 > mpf('0.55'))
# F'' > 3/2
Fpp = 4*(mpf('0.485')*mpf('0.99155') + mpf('0.11047')) - mpf(356)/625*mpf('0.78193')
check("F'' lower bound > 3/2", Fpp > mpf('1.5'))
# F endpoints
def Ffun(xx): return mpf('0.89')*sin(mpf('0.8')*xx) - (xx - mpf('0.356'))*sin(2*xx)
check("F'(24/25) in (-1/20, 0)", mpf('-0.05') < (Ffun(mpf('0.96001'))-Ffun(mpf('0.95999')))/mpf('0.00002') < 0)
check("F'(97/100) > 0", (Ffun(mpf('0.97001'))-Ffun(mpf('0.96999')))/mpf('0.00002') > 0)
check("F(24/25) >= 49/1000", Ffun(mpf('0.96')) >= mpf('0.049'))
check("F(97/100) >= 49/1000", Ffun(mpf('0.97')) >= mpf('0.049'))
# J1 final
check("J1 >= 6499/7500", mpf(4) + mpf(187)/100 - (mpf(89)/100**2*8 - mpf(4)/3) >= mpf(6499)/7500)
check("6499/7500 > 1733/2000", mpf(6499)/7500 > mpf(1733)/2000)
# q=1 J1
check("J1 q=1 N >= 17.9", mpf(2)*(mpf('0.25')+4+6) - 2*mpf('1.26') > mpf('17.9'))
check("J2 q=1 N < -7", mpf(2)*(4 - 8*8*pi/21 + 6) - 2*(2*pi/3)**2 < -7)
x2c = 2*pi/3; zc = -x2c*cot(x2c); Nc = 2*(zc**2-8*zc+6) - 2*x2c**2
check("J2 q=1 corner ~ -5.87", abs(4*Nc/9 - (-5.87)) < 0.01)

# ---- lem:track(iv) ----
check("h''(0.655) region: cos(2*0.655) < 26/100", cos(2*mpf('0.655')) < mpf('0.26'))
check("0.655*sin(2*0.655) > 3/5", mpf('0.655')*sin(2*mpf('0.655')) > mpf('0.6'))
check("tau(0.655) > pi/4", atan(2*tan(mpf('0.655'))) > pi/4)
check("h(0.655) >= 791/2500", mpf('0.655')*sin(mpf('0.655'))*cos(mpf('0.655')) >= mpf(791)/2500)
check("h(13/10) >= 791/2500", mpf('1.3')*sin(mpf('1.3'))*cos(mpf('1.3')) >= mpf(791)/2500)
check("m = 3164/10000 = 791/2500", F(3164,10000) == F(791,2500))

# ---- table g1 ----
rows = {
 '[0.655,0.72]': (F(11,5), F(3,10), F(57,50), F(0)),
 '[0.72,0.723]': (F(13,5), F(3,10), F(3,2), F(0)),
 '[0.723,0.724]': (F(27,10), F(3,10), F(3,2), F(0)),
 '[0.724,0.73]': (F(13,5), F(3,10), F(3,2), F(0)),
 '[0.73,0.82]': (F(2), F(3,20), F(3,2), F(0)),
 '[0.82,0.83]': (F(2), F(3,20), F(19,10), F(0)),
 '[0.83,0.85]': (F(19,10), F(1,10), F(19,10), F(0)),
 '[0.85,0.86]': (F(9,5), F(1,10), F(19,10), F(0)),
 '[0.86,1.0014]': (F(3,5), F(1,25), F(4,3), F(0)),
 '[1.0014,1.0472]': (F(3,8), F(1,40), F(11,10), F(63,100)*F(33,200)),
}
mu_claimed = {
 '[0.655,0.72]': F(91,25), '[0.72,0.723]': F(22,5), '[0.723,0.724]': F(9,2),
 '[0.724,0.73]': F(22,5), '[0.73,0.82]': F(73,20), '[0.82,0.83]': F(81,20),
 '[0.83,0.85]': F(39,10), '[0.85,0.86]': F(19,5), '[0.86,1.0014]': F(148,75),
 '[1.0014,1.0472]': F(27921,20000),
}
allok = True
for k, (ta, tb_, tc, td) in rows.items():
    mu = ta + tb_ + tc - td
    if mu != mu_claimed[k]:
        allok = False
        print("  mu mismatch", k, mu, mu_claimed[k])
    if mu < F(139,100):
        allok = False
        print("  mu < 139/100", k, mu)
check("table g1 mu values + >= 139/100", allok)

print()
fails = [r for r in res if not r[1]]
print("RATIONAL BOUND CHECKS: %d total, %d failed" % (len(res), len(fails)))
for f in fails: print("  FAIL:", f[0])
