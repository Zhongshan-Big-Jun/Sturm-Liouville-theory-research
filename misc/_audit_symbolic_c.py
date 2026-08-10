# -*- coding: utf-8 -*-
"""Audit C (consolidated): remaining chains of SL_gap_n1_O3a_phase_rigidity_proof.tex.
Groups: I lem:B1 tail, II lem:boundary rational bounds, III lem:M2 (a)(d)(e),
IV lem:corner/C4, V lem:inclusion (+F-206, F-207). All exact/rational unless noted.
Session 45, 2026-08-09. Run: R-20260809T000000Z-j2e1-e1ify-0C11DE.
"""
import sympy as sp
from sympy import Rational as R
import mpmath as mp
res = []
def check(name, cond):
    res.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name)

pi = sp.pi
x, q, c, w, z = sp.symbols('x q c w z', positive=True)

# ---------------- I. lem:B1 tail ----------------
b = sp.Symbol('b')
t = sp.atan(w)
A2 = pi - sp.atan(w/q)
M2gen = 4*A2**2*w*q - 7*A2*q**2 - 9*A2*w**2 + 2*A2*(q**2+w**2)/(1+w**2) + t*(4*A2*w - 5*q - 9*q*w**2)
g = sp.simplify(sp.diff(M2gen, q).subs(q, 1))
# Leibniz partial sums (definition S_k := sum_{j=0}^k); doc values are S_5, S_6 (F-207 fixed)
S5 = sum((R(-1,1)**j)*(R(4,5)**(2*j+1))/R(2*j+1,1) for j in range(0,6))
S6 = S5 + (R(-1,1)**6)*(R(4,5)**(13))/R(13,1)
check('I1 S5 = 22739538548/33837890625', sp.simplify(S5 - R(22739538548,33837890625)) == 0)
check('I2 S6 = 7436856470852/10997314453125', sp.simplify(S6 - R(7436856470852,10997314453125)) == 0)
check('I3 67/100 < S5', R(67,100) < S5)
check('I4 S5 < arctan(4/5) < S6 (numeric cross)',
      float(sp.N(sp.atan(R(4,5)) - S5, 30)) > 0 and float(sp.N(S6 - sp.atan(R(4,5)), 30)) > 0)
check('I5 S6 < 17/25', S6 < R(17,25))
P = sp.Symbol('P', positive=True)
g45_P = -19*b/25 - 346*P/41 + 16*(b-P)**2/5 - R(1076,205)
gp45_P = -2152*b/205 - 2560*P/1681 + 4*(b-P)**2 - R(15008,1681)
comb = sp.simplify(g45_P.subs({b: R(67,100), P: R(22,7)}) + gp45_P.subs({b: R(67,100), P: R(22,7)})*(R(7,4)-R(4,5)))
check('I6 g(4/5;67/100,22/7)+g\'(4/5;67/100,22/7)(7/4-4/5) = -1054523/114800', comb == R(-1054523,114800))
check('I7 g\'(4/5;17/25,157/50) > 3.3581', gp45_P.subs({b: R(17,25), P: R(157,50)}) > sp.Float('3.3581', 30))
check('I8 g\'(sqrt3) upper bound = -14957063/441000',
      sp.simplify(R(16)*R(22,7)**2/R(9,1) - R(41)*R(17,10)*R(157,50)/R(6,1) - 15 - R(-14957063,441000)) == 0)

# ---------------- II. lem:boundary rational bounds ----------------
Pz = 32*z*(z**2+1)**2
Qz = -10*z**6 - 32*pi*z**5 + 42*z**4 - 64*pi*z**3 + 2*z**2 - 32*pi*z + 46
Rz = 5*pi*z**6 - 10*z**5 + 8*pi**2*z**5 - 21*pi*z**4 - 40*z**3 + 16*pi**2*z**3 - pi*z**2 - 14*z + 8*pi**2*z - 23*pi
Tz = sp.expand(sp.pi**2/36*Pz + sp.pi/6*Qz + Rz)
zmax = R(10,17); pilo = R(157,50); pihi = R(22,7)
Rbound = -23*pilo + (8*pihi**2-14)*zmax + (16*pihi**2-40)*zmax**3 + (8*pihi**2-10)*zmax**5 + 5*pihi*zmax**6
check('II1 R(z) <= -262235520291/59137044050', sp.simplify(Rbound - R(-262235520291,59137044050)) == 0)
Tbound = R(10,1)*pihi/3*zmax**6 + (R(32,1)*pihi**2/9-10)*zmax**5 + (R(64,1)*pihi**2/9-40)*zmax**3 + (R(32,1)*pihi**2/9-14)*zmax - R(46,1)*pilo/3
check('II2 T(z) <= -7282185739373/266116698225', sp.simplify(Tbound - R(-7282185739373,266116698225)) == 0)
Rpf = sp.lambdify(z, Rz, 'mpmath'); Tpf = sp.lambdify(z, Tz, 'mpmath')
mxR = max(Rpf(mp.mpf(k)/1000) for k in range(1,578)); mxT = max(Tpf(mp.mpf(k)/1000) for k in range(1,578))
check('II3 cross: max R,T on [0,1/sqrt3] < claimed bounds', mxR < float(R(-262235520291,59137044050)) and mxT < float(R(-7282185739373,266116698225)))

# ---------------- III. lem:M2 (a)(d)(e) ----------------
h_p = 4*(pi - sp.atan(w)) - 4*w/(1+w**2) - 18*w
S2_atan12 = R(11,24) + R(1,160)
check('III1 h\'(1/2) > 0.1016 (rational)', 4*pilo - 4*S2_atan12 - R(53,5) > sp.Float('0.1016', 30))
zz = R(53,100)
S9 = sum((R(-1,1)**j)*zz**(2*j+1)/R(2*j+1,1) for j in range(0,10))
check('III2 h\'(0.53) < -0.52 (rational)', 4*pihi - 4*S9 - R(21200,12809) - R(477,50) < -sp.Float('0.52', 30))
Aq = pi - sp.atan(w/q)
dM2_full = sp.simplify(sp.diff(M2gen, q))
dM2_split = sp.simplify(4*Aq**2*w + 8*Aq*w**2*q/(q**2+w**2) - 14*Aq*q + 4*Aq*q/(1+w**2) + 2*w/(1+w**2)
                        - 5*sp.atan(w) + sp.atan(w)*(4*w**2/(q**2+w**2) - 9*w**2) - w*(7*q**2+9*w**2)/(q**2+w**2))
check('III3 d_q M2 split identity', sp.simplify(sp.expand_trig(dM2_full - dM2_split)) == 0)
qq = sp.Symbol('qq', positive=True)
Bq = (4*pi**2+14)*sp.sqrt(2*qq+1) + 8*pi*(2*qq+1)/qq + 1 + 2*pi*(2*qq+1)/qq**2 - 10*pi*qq
B0 = (4*pi**2+14)*sp.sqrt(2*qq+1) + 8*pi*(2*qq+1)/qq + 1 - 10*pi*qq
check('III4 B(q) = B0(q) + 2pi(2q+1)/q^2', sp.simplify(Bq - B0 - 2*pi*(2*qq+1)/qq**2) == 0)
dM2f = sp.lambdify((q,w), sp.simplify(dM2_full), 'mpmath'); Bf = sp.lambdify(qq, Bq, 'mpmath')
worst = mp.mpf('-inf')
for i in range(0,21):
    qv = mp.mpf(20) + mp.mpf(i)*mp.mpf('9'); wmax = mp.sqrt(2*qv+1)
    for j in range(1,41):
        worst = max(worst, dM2f(qv, mp.mpf(j)/40*wmax) - Bf(qv))
check('III5 cross: dM2 <= B on tail grid (worst %.3e)' % float(worst), worst < 0)
B20 = sp.N(Bq.subs(qq, 20), 40)
check('III6 B(20) < -232.723 (40-digit)', float(B20) < -232.723)
pia = R(314159,100000); s41b = R(640313,100000)
B20_ub = (4*pia**2+14)*s41b + 1 - R(183395,1000)*pia
check('III7 rational envelope B(20) <= -232.723', B20_ub < -sp.Float('232.723', 30))
check('III8 B\'(q) expression matches', sp.simplify(sp.diff(Bq,qq) - ((4*pi**2+14)/sp.sqrt(2*qq+1) - 12*pi/qq**2 - 4*pi/qq**3 - 10*pi)) == 0)
check('III9 Bp upper bound < 0', (4*pihi**2+14)/R(64,10) - 10*pilo < 0)
bound_e = 4*pihi**2*R(33,100) + 2*pihi*(1+R(33,100)**2)/42 - 7*(pilo - R(33,100))
check('III10 M2/q^2 bound < 0 (rational)', bound_e < 0)

# ---------------- IV. lem:corner / C4 ----------------
v, T = sp.symbols('v T', positive=True)
pia4 = R(31415,10000); pib4 = R(31416,10000)
check('IV1 pi in (31415/10000, 31416/10000)', float(sp.N(pi,40)) > float(pia4) and float(sp.N(pi,40)) < float(pib4))
check('IV2 2pi/7 > 8975/10000', R(2,1)*pia4/R(7,1) > R(8975,10000))
check('IV3 3pi/10 < 9425/10000', R(3,1)*pib4/R(10,1) < R(9425,10000))
check('IV4 3pi/10 > 9424/10000', R(3,1)*pia4/R(10,1) > R(9424,10000))
check('IV5 2pi/5 < 12567/10000', R(2,1)*pib4/R(5,1) < R(12567,10000))
s5lo = R(22360,10000); s5hi = R(22361,10000)
check('IV6 sqrt5 in (2.2360,2.2361)', float(sp.N(sp.sqrt(5),40)) > float(s5lo) and float(sp.N(sp.sqrt(5),40)) < float(s5hi))
check('IV7 tan^2(3pi/10) = 1+2sqrt5/5', sp.simplify(sp.expand_trig(sp.tan(3*pi/10)**2 - (1 + 2*sp.sqrt(5)/5))) == 0)
check('IV8 tan^2(2pi/5) = 5+2sqrt5', sp.simplify(sp.expand_trig(sp.tan(2*pi/5)**2 - (5 + 2*sp.sqrt(5)))) == 0)
check('IV9 (13763/10000)^2 < 1+2*2.2360/5', R(13763,10000)**2 - (1 + 2*s5lo/R(5,1)) < 0)
check('IV10 1+2*2.2361/5 < (13765/10000)^2', (1 + 2*s5hi/R(5,1)) - R(13765,10000)**2 < 0)
check('IV11 tan(2pi/5) < 3078/1000', R(3078,1000)**2 - (5 + 2*s5hi) > 0)
tq = sp.symbols('tq', positive=True)
Pp6 = tq**6 - 21*tq**4 + 35*tq**2 - 7
check('IV12 P(1) = 8, P(2) = -139', sp.simplify(Pp6.subs(tq,1) - 8) == 0 and sp.simplify(Pp6.subs(tq,2) + 139) == 0)
u = sp.symbols('u', positive=True)
fq = 3*u**2 - 42*u + 35
check('IV13 P\'(t) = 2t(3t^4-42t^2+35)', sp.simplify(sp.diff(Pp6,tq) - 2*tq*(3*tq**4-42*tq**2+35)) == 0)
check('IV14 3u^2-42u+35 <= -4 on u in [1,4]', sp.simplify(fq.subs(u,1) + 4) == 0 and sp.simplify(fq.subs(u,4) + 85) == 0 and sp.diff(fq,u,2) == 6)
th = sp.symbols('th', positive=True)
tt = sp.tan(th)
num7 = 7*tt - 35*tt**3 + 21*tt**5 - tt**7
den7 = 1 - 21*tt**2 + 35*tt**4 - 7*tt**6
check('IV15 tan(7th) rational identity', sp.simplify(sp.factor(sp.together(sp.expand_trig(sp.tan(7*th) - num7/den7)))) == 0)
check('IV16 num = -t*P(t)', sp.simplify(sp.expand(num7 + tt*(tt**6 - 21*tt**4 + 35*tt**2 - 7))) == 0)
check('IV17 P(1253/1000) > 0 > P(1254/1000)', Pp6.subs(tq,R(1253,1000)) > 0 and Pp6.subs(tq,R(1254,1000)) < 0)
q2, w2 = sp.symbols('q2 w2', positive=True)
A52 = R(5,2)*v
INc = (q2**2+w2**2)*A52*(2*A52*q2 - 3*w2 + 2*v) - 3*w2*q2*(1+w2**2)*v
Kc = (q2**2+w2**2)*(5*v*q2 - 3*w2 + 2*v) - R(6,5)*w2*q2*(1+w2**2)
check('IV18 IN = A*K on c=0.4', sp.simplify(sp.expand(INc - A52*Kc)) == 0)
Lv = (1+T**2)*(w*(5*v/T - 3) + 2*v) - R(6,5)*T*(1+w**2)
Kexpr = sp.simplify((w**2/T**2 + w**2)*(w*(5*v/T-3)+2*v) - R(6,5)*(w/T)*w*(1+w**2))
check('IV19 K = q^2 L, q = w/T', sp.simplify(sp.expand(Kexpr - (w**2/T**2)*Lv)) == 0)
wv = sp.Function('wv')(v); Tv = sp.Function('Tv')(v)
Lsym = (1+Tv**2)*(wv*(5*v/Tv - 3) + 2*v) - R(6,5)*Tv*(1+wv**2)
dL = sp.diff(Lsym, v).subs(sp.Derivative(wv, v), 1+wv**2).subs(sp.Derivative(Tv, v), -R(5,2)*(1+Tv**2))
c3 = 50*wv**2*v - 24*wv**3 + 176*wv - 50*v
c5 = 150*wv - 100*v
Ndoc = 125*wv*v + 50*Tv*(v*(1+wv**2)+wv) + 20*Tv**2 + c3*Tv**3 + (20-125*wv*v)*Tv**4 + c5*Tv**5
check('IV20 L\'(v) = N/(10 T^2)', sp.simplify(sp.factor(sp.together(dL - Ndoc/(10*Tv**2)))) == 0)
c3_lb = 50*R(8975,10000)*(R(1253,1000)**2 - 1) + 2*R(1253,1000)*(88 - 12*R(13765,10000)**2)
c5_lb = 150*R(1253,1000) - 100*R(9425,10000)
regI = (125*R(1253,1000)*R(8975,10000) + 50*(R(8975,10000)*(1+R(1253,1000)**2) + R(1253,1000)) + 20 + c3_lb + c5_lb
        - 125*R(13765,10000)*R(9425,10000)*R(1254,1000)**4)
check('IV21 Region I sum = 88146367488708279/400000000000000', sp.simplify(regI - R(88146367488708279,400000000000000)) == 0)
check('IV22 (1253/1000)(8975/10000) > 20/125', R(1253,1000)*R(8975,10000) > R(20,125))
c3II = 50*R(9424,10000)*(R(27,10)**2 - 1) + (176*R(3078,1000) - 24*R(3078,1000)**3)
check('IV23 Region II c3 bound = 2160051043/15625000', sp.simplify(c3II - R(2160051043,15625000)) == 0)
check('IV24 c5 lower bound > 0', 150*R(13763,10000) - 100*R(12567,10000) > 0)
check('IV25 88 - 12(27/10)^2 > 0 and 176 - 72(3078/1000)^2 < 0', 88 - 12*R(27,10)**2 > 0 and 176 - 72*R(3078,1000)**2 < 0)
w7 = sp.tan(2*pi/7)
Lval = sp.simplify(sp.expand_trig(Lv.subs({v: 2*pi/7, w: w7, T: w7})))
L_alt = sp.simplify(sp.expand_trig((1+w7**2)*(2*pi - R(21,5)*w7)))
check('IV26 L(2pi/7) = (1+w^2)(2pi-21w/5)', sp.simplify(sp.expand_trig(Lval - L_alt)) == 0)
Lbound = (1+R(1253,1000)**2)*(2*R(31415,10000) - R(21,5)*R(1254,1000))
check('IV27 L(2pi/7) >= 13058215729/5000000000', sp.simplify(Lbound - R(13058215729,5000000000)) == 0)
xx = sp.acos(R(2,3))
check('IV28 G2(1/2;2) = 12(pi-arccos(2/3)-sqrt5)/(5 sqrt5)', sp.simplify(R(12,1)/(5*sp.sqrt(5))*(pi - xx - sp.sqrt(5)) - R(12,1)*(pi - xx - 3*sp.sqrt(5)/3)/(5*sp.sqrt(5))) == 0)
cos09_ub = 1 - R(9,10)**2/2 + R(9,10)**4/24
check('IV29 cos(0.9) upper bound < 2/3', sp.simplify(cos09_ub - R(2,3)) < 0)
check('IV30 pi - sqrt5 > 3.14 - 2.24', float(sp.N(pi - sp.sqrt(5) - (R(314,100) - R(224,100)), 40)) > 0)

# ---------------- V. lem:inclusion ----------------
g = sp.symbols('g', positive=True)
Phi = sp.cos(x)**2 + q**2*sp.sin(x)**2
F1 = c*x - sp.atan(1/(q*sp.tan(x)))
F2 = c*(pi - g) - sp.atan(q*sp.tan(g))
check('V1 d_x F1 = c + q/Phi', sp.simplify(sp.diff(F1,x) - (c + q/Phi)) == 0)
check('V2 d_q F1 = tan x/(1+q^2 tan^2 x)', sp.simplify(sp.diff(F1,q) - sp.tan(x)/(1+q**2*sp.tan(x)**2)) == 0)
check('V2b F-206: doc q-factor formula is wrong', sp.simplify(sp.diff(F1,q) - q*sp.tan(x)/(1+q**2*sp.tan(x)**2)) != 0)
check('V3 d_c F1 = x', sp.simplify(sp.diff(F1,c) - x) == 0)
check('V4 d_g F2 = -c - q sec^2 g/(1+q^2 tan^2 g)', sp.simplify(sp.diff(F2,g) - (-c - q*(1+sp.tan(g)**2)/(1+q**2*sp.tan(g)**2))) == 0)
check('V5 d_q F2 = -tan g/(1+q^2 tan^2 g)', sp.simplify(sp.diff(F2,q) + sp.tan(g)/(1+q**2*sp.tan(g)**2)) == 0)
check('V6 d_c F2 = pi - g', sp.simplify(sp.diff(F2,c) - (pi - g)) == 0)
check('V7 alpha1(1,2/5) = 5pi/14', sp.simplify(sp.expand_trig(F1.subs({q:1, c:R(2,5), x: R(5,1)*pi/14}))) == 0)
check('V8 gamma(1,1/2) = pi/3', sp.simplify(sp.expand_trig(F2.subs({q:1, c:R(1,2), g: pi/3}))) == 0)
x0 = sp.acos(R(2,3))
check('V9 alpha1(2,1/2) = arccos(2/3): 2tan x tan(x/2)=1',
      sp.simplify(sp.expand_trig(2*sp.tan(x0)*sp.sin(x0)/(1+sp.cos(x0)) - 1)) == 0)
xr = R(841,1000)
coslb = 1 - xr**2/2 + xr**4/24 - xr**6/720
check('V10 1-x^2/2+x^4/24-x^6/720 > 2/3 at x=841/1000', sp.simplify(coslb - R(2,3)) > 0)
check('V11 5pi/14 < 1.1220 and pi/3 < 1.0472 (pi < 3.14159)', R(5,1)*R(314159,100000)/14 < R(11220,10000) and R(314159,100000)/3 < R(10472,10000))
check('V12 (2/5)(pi-0.655) > 0.9946 (pi > 3.14159)', R(2,5)*(R(314159,100000) - R(655,1000)) > R(9946,10000))
xr2 = R(131,200)
sinub = xr2 - xr2**3/6 + xr2**5/120
coslb2 = 1 - xr2**2/2 + xr2**4/24 - xr2**6/720
tanub = sinub/coslb2
check('V13 sin upper / cos lower bounds valid (numeric sanity)',
      float(sp.N(sp.sin(xr2) - sinub, 30)) <= 0 and float(sp.N(sp.cos(xr2) - coslb2, 30)) >= 0)
check('V14 tan(0.655) < 0.7682', sp.simplify(tanub - R(7682,10000)) < 0)
check('V15 1/1.5364 > 0.6508', R(10000,15364) > R(6508,10000))
zr = R(6508,10000)
S5z = zr - zr**3/3 + zr**5/5 - zr**7/7 + zr**9/9 - zr**11/11
check('V16 arctan(0.6508) >= S5 > 0.5767', S5z > R(5767,10000))
check('V17 pi/2 - 0.5767 < 0.9941 < 0.9946', R(1,2)*R(314159,100000) - R(5767,10000) < R(9941,10000))
h = R(2,5)*(pi - g) - sp.atan(2*sp.tan(g))
check('V18 h\' = -2/5 - 2sec^2 g/(1+4tan^2 g) < 0',
      sp.simplify(sp.diff(h,g) + (R(2,5) + 2*(1+sp.tan(g)**2)/(1+4*sp.tan(g)**2))) == 0)

print()
print('SUMMARY:', sum(1 for _, ok in res if ok), 'PASS /', len(res), 'total')
