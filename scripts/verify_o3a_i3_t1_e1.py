# -*- coding: utf-8 -*-
"""verify_o3a_i3_t1_e1.py
T1-side analytic (E1) proof of J1_2d > 0 -- independent cross-check.
The analytic proofs live in docs/SL_gap_n1_O3a_phase_rigidity_proof.tex
(Theorem: J1_2d(x,q) >= 6499/7500 > 1733/2000 > 0 on the closure of T1,
fully elementary). This script cross-checks every ingredient (E3) and
verifies the rational alternating-series constants used in the F-analysis
and the term1 two-case bound (PART C/D).

PART A  exact-algebra identities (mpmath point checks)
PART B  E1 ingredient bounds on T1 (dense grid)
PART C  F-analysis constants via alternating series with rational arithmetic
PART D  term1 constants: case x<=pi/3 and case x>=pi/3
PART E  composed chain J1 >= 6499/7500
"""
import mpmath as mp
import random
mp.mp.dps = 60
PI = mp.pi

def c1(x, q):
    return mp.atan(1.0 / (q * mp.tan(x))) / x

def PhV(x, q):
    return mp.cos(x)**2 + q**2 * mp.sin(x)**2

def DV(x, q, c):
    return q + c * PhV(x, q)

def Gv(x, q, c):
    Ph = PhV(x, q); W = 3 + 2 * x * mp.cot(x); D = DV(x, q, c)
    return -Ph * W / D + 2 * c * x * Ph * (q**2 - 1) * mp.sin(x) * mp.cos(x) / D**2

def T1_samples(N=60, M=6000, seed=41):
    pts = []
    for i in range(N):
        for j in range(N):
            x = mp.mpf('0.841') + (mp.mpf('1.1220') - mp.mpf('0.841')) * i / (N - 1)
            q = mp.mpf('1') + j / (N - 1)
            if mp.mpf('0.4') < c1(x, q) < mp.mpf('0.5'):
                pts.append((x, q))
    rng = random.Random(seed)
    for _ in range(M):
        x = mp.mpf('0.841') + (mp.mpf('1.1220') - mp.mpf('0.841')) * rng.random()
        q = 1 + rng.random()
        if mp.mpf('0.4') < c1(x, q) < mp.mpf('0.5'):
            pts.append((x, q))
    return pts

ok = True
def report(name, cond, detail=""):
    global ok
    print("  [%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))
    ok = ok and cond

# ---------------- PART A ----------------
print("== PART A: identities ==")
h = mp.mpf('1e-7'); fails = [0] * 9; cnt = 0
for (x, q) in T1_samples()[::5]:
    c = c1(x, q); th = c * x
    sx, cx, st, ct = mp.sin(x), mp.cos(x), mp.sin(th), mp.cos(th)
    Ph = PhV(x, q); D = DV(x, q, c)
    W0 = x * st * ct + th * sx * cx; R = cx**2 - st**2
    u = x * Ph / D; A = 3 / x + 2 * cx / sx
    H = 2 * c * (q**2 - 1) * sx * cx / D
    G = Gv(x, q, c)
    t1 = Ph**2 * (3 + 2 * x * cx / sx) / D**2
    t2 = 2 * x * Ph * (q**2 - 1) * sx * cx * (q - c * Ph) / D**3
    Gc = (Gv(x, q, c + h) - Gv(x, q, c - h)) / (2 * h)
    Gx = (Gv(x + h, q, c) - Gv(x - h, q, c)) / (2 * h)
    if abs(G - u * (H - A)) > mp.mpf('1e-15'): fails[0] += 1
    if abs(u - x**2 * sx * cx / W0) > mp.mpf('1e-15'): fails[1] += 1
    if abs(H - 2 * th * R / W0) > mp.mpf('1e-15'): fails[2] += 1
    if abs(Ph / D - x * sx * cx / W0) > mp.mpf('1e-15'): fails[3] += 1
    if abs(Gc - (t1 + t2)) > mp.mpf('1e-12'): fails[4] += 1
    if abs(q / Ph + c - W0 / (x * sx * cx)) > mp.mpf('1e-15'): fails[5] += 1
    ux = (Ph * D + 2 * x * q * (q**2 - 1) * sx * cx) / D**2
    def uv(xv):
        Phv = mp.cos(xv)**2 + q**2 * mp.sin(xv)**2
        return xv * Phv / (q + c * Phv)
    if abs((uv(x + h) - uv(x - h)) / (2 * h) - ux) > mp.mpf('1e-6'): fails[6] += 1
    Hx = 2 * c * (q**2 - 1) * (mp.cos(2 * x) * D - 2 * c * (q**2 - 1) * sx**2 * cx**2) / D**2
    def Hv2(xv):
        Phv = mp.cos(xv)**2 + q**2 * mp.sin(xv)**2
        return 2 * c * (q**2 - 1) * mp.sin(xv) * mp.cos(xv) / (q + c * Phv)
    if abs((Hv2(x + h) - Hv2(x - h)) / (2 * h) - Hx) > mp.mpf('1e-6'): fails[7] += 1
    Ax = -3 / x**2 - 2 / sx**2
    if abs(Gx - (ux * (H - A) + u * (Hx - Ax))) > mp.mpf('1e-5'): fails[8] += 1
    cnt += 1
report("9 identities at %d points" % cnt, all(f == 0 for f in fails), str(fails))

# ---------------- PART B ----------------
print("== PART B: E1 ingredient bounds on T1 (dense grid) ==")
pts = T1_samples()
mn, mx = {}, {}
def acc(nm, v):
    mn[nm] = min(mn.get(nm, v), v); mx[nm] = max(mx.get(nm, v), v)
worst_uc04 = mp.inf
for (x, q) in pts:
    c = c1(x, q); th = c * x
    sx, cx, st, ct = mp.sin(x), mp.cos(x), mp.sin(th), mp.cos(th)
    Ph = PhV(x, q); D = DV(x, q, c)
    W0 = x * st * ct + th * sx * cx
    u = x * Ph / D
    t1 = Ph**2 * (3 + 2 * x * cx / sx) / D**2
    t2 = 2 * x * Ph * (q**2 - 1) * sx * cx * (q - c * Ph) / D**3
    H = 2 * th * (cx**2 - st**2) / W0; A = 3 / x + 2 * cx / sx
    ux = (Ph * D + 2 * x * q * (q**2 - 1) * sx * cx) / D**2
    Hx = 2 * c * (q**2 - 1) * (mp.cos(2 * x) * D - 2 * c * (q**2 - 1) * sx**2 * cx**2) / D**2
    Gc = t1 + t2
    Gx = (Gv(x + h, q, c) - Gv(x - h, q, c)) / (2 * h)
    G = Gv(x, q, c)
    J1 = G**2 + Gc - u * Gx
    u_c04 = x * mp.sin(2 * x) / (mp.sin(mp.mpf('0.8') * x) + mp.mpf('0.4') * mp.sin(2 * x))
    C = 3 / x**2 + 2 / sx**2
    worst_uc04 = min(worst_uc04, u_c04 - u)
    acc('PhiD', Ph / D); acc('Hm2cot', H - 2 * cx / sx); acc('uxmPhiD', ux - Ph / D)
    acc('Hx', Hx); acc('C', C); acc('u', u); acc('t1', t1); acc('t2', t2)
    acc('G', G); acc('J1', J1)
    acc('u_minus_2x3', u - 2 * x / 3); acc('ux_minus_23', ux - mp.mpf(2) / 3)
    acc('uu_x_minus_4x9', u * ux - 4 * x / 9)
for k in ["PhiD", "Hm2cot", "uxmPhiD", "Hx", "C", "u", "t1", "t2", "G", "J1"]:
    print("  %-9s [%s, %s]" % (k, mp.nstr(mn[k], 8), mp.nstr(mx[k], 8)))
report("Phi/D >= 2/3", mn['PhiD'] >= mp.mpf(2) / 3)
report("H - 2cot x <= 0", mx['Hm2cot'] <= 0)
report("u_x - Phi/D >= 0", mn['uxmPhiD'] >= -mp.mpf('1e-20'))
report("H_x <= 0", mx['Hx'] <= 0)
report("C = 3/x^2+2csc^2x <= 8", mx['C'] <= 8)
report("u <= 0.89", mx['u'] <= mp.mpf('0.89'))
report("u <= u_c04 pointwise", worst_uc04 >= 0)
report("term1 >= 1.87 - 1e-3 (grid)", mn['t1'] >= mp.mpf('1.87') - mp.mpf('1e-3'))
report("term2 >= 0", mn['t2'] >= 0)
report("G <= -2", mx['G'] <= -2)
report("u >= 2x/3", mn['u_minus_2x3'] >= 0)
report("u_x >= 2/3", mn['ux_minus_23'] >= 0)
report("u*u_x >= 4x/9", mn['uu_x_minus_4x9'] >= 0)
report("J1 >= 0.8665 (grid)", mn['J1'] >= mp.mpf('0.8665'))

# ---------------- PART C: F-analysis with corrected rational bounds ----------------
print("== PART C: F-analysis (u <= 89/100), corrected rational bounds ==")
# F(x) = (89/100) sin(4x/5) - (x - 89/250) sin(2x);  F >= 0 on [841/1000, 1122/1000]
# F'' = -(356/625) sin(4x/5) - 4 cos(2x) + 4(x-89/250) sin(2x)
# Claim: F'' >= 3/2.  Proof via y = 2x, g(y) = (y/2-89/250) sin y - cos y:
#   F'' = -(356/625) sin(4x/5) + 4 g(2x),  g' > 0 on y in [1.682, 2.244].
def sin_lb(t, n=10):
    s = mp.mpf(0); term = t; k = 0
    while k <= n:
        s += term; k += 1
        term = -term * t * t / ((2 * k) * (2 * k + 1))
    return s
def sin_ub(t, n=10):
    s = mp.mpf(0); term = t; k = 0
    while k <= n:
        s += term; k += 1
        term = -term * t * t / ((2 * k) * (2 * k + 1))
    return s + term
def cos_lb(t, n=10):
    s = mp.mpf(1); term = mp.mpf(1); k = 0
    while k <= n:
        k += 1
        term = -term * t * t / ((2 * k - 1) * (2 * k))
        s += term
    return s
def cos_ub(t, n=10):
    s = mp.mpf(1); term = mp.mpf(1); k = 0
    while k <= n:
        k += 1
        term = -term * t * t / ((2 * k - 1) * (2 * k))
        s += term
    return s + term

# g'(y) = (3/2) sin y + (y/2-89/250) cos y >= (3/2) sin(2.244) - 0.766 |cos(2.244)|
# sin(2.244) = sin(pi-2.244) >= sin(0.8975)  (pi >= 3.1415)
# |cos(2.244)| = cos(pi-2.244) <= cos(0.8975)  (pi <= 3.1416)
gp_lb = mp.mpf(3) / 2 * sin_lb(mp.mpf('0.8975')) - mp.mpf('0.766') * cos_ub(mp.mpf('0.8975'))
report("g'(y) > 0 on [1.682,2.244]", gp_lb > 0, "g' >= %s" % mp.nstr(gp_lb, 7))
# g(1.682) = 0.485 sin(1.682) - cos(1.682) >= 0.485 cos_lb(0.13) + cos_lb(1.4596)
#   sin(1.682) >= sin(1.7) = cos(1.7-pi/2) >= cos(0.13)  (pi/2 >= 1.57, cos decreasing)
#   -cos(1.682) = cos(pi-1.682) >= cos(1.4596)          (pi <= 3.1416, cos decreasing)
g_lb = mp.mpf('0.485') * cos_lb(mp.mpf('0.13')) + cos_lb(mp.mpf('1.4596'))
# -(356/625) sin(4x/5) >= -(356/625) sin(0.8976) >= -(356/625) sin_ub(0.8976)
Fpp_lb = 4 * g_lb - mp.mpf('356') / 625 * sin_ub(mp.mpf('0.8976'))
report("F'' >= 3/2 on [0.841,1.122] (rational bound)", Fpp_lb >= mp.mpf(3) / 2,
       "F'' >= %s" % mp.nstr(Fpp_lb, 7))

# F'(24/25) = (89/125)cos(96/125) - sin(48/25) - (151/125)cos(48/25)
c768_ub = cos_ub(mp.mpf('96') / 125)
s192_lb = sin_lb(mp.mpf('48') / 25)
c192_lb = cos_lb(mp.mpf('48') / 25)
Fp96_ub = mp.mpf('89') / 125 * c768_ub - s192_lb - mp.mpf('151') / 125 * c192_lb
c768_lb = cos_lb(mp.mpf('96') / 125)
s192_ub = sin_ub(mp.mpf('48') / 25)
c192_ub = cos_ub(mp.mpf('48') / 25)
Fp96_lb = mp.mpf('89') / 125 * c768_lb - s192_ub - mp.mpf('151') / 125 * c192_ub
report("-1/20 < F'(24/25) < 0", Fp96_lb > -mp.mpf('1') / 20 and Fp96_ub < 0,
       "F'(24/25) in [%s, %s]" % (mp.nstr(Fp96_lb, 7), mp.nstr(Fp96_ub, 7)))

# F'(97/100) = (89/125)cos(97/125) - sin(97/50) - (307/250)cos(97/50)
c776_lb = cos_lb(mp.mpf('97') / 125)
s194_ub = sin_ub(mp.mpf('97') / 50)
c194_ub = cos_ub(mp.mpf('97') / 50)
Fp97_lb = mp.mpf('89') / 125 * c776_lb - s194_ub - mp.mpf('307') / 250 * c194_ub
report("F'(97/100) > 0", Fp97_lb > 0, "F'(97/100) >= %s" % mp.nstr(Fp97_lb, 7))

# F(24/25) = (89/100)sin(96/125) - (151/250)sin(48/25)
s768_lb = sin_lb(mp.mpf('96') / 125)
s192_ub = sin_ub(mp.mpf('48') / 25)
F96_lb = mp.mpf('89') / 100 * s768_lb - mp.mpf('151') / 250 * s192_ub
report("F(24/25) >= 49/1000", F96_lb >= mp.mpf('49') / 1000, "F(24/25) >= %s" % mp.nstr(F96_lb, 7))

# F(97/100) = (89/100)sin(97/125) - (307/500)sin(97/50)
s776_lb = sin_lb(mp.mpf('97') / 125)
s194_ub = sin_ub(mp.mpf('97') / 50)
F97_lb = mp.mpf('89') / 100 * s776_lb - mp.mpf('307') / 500 * s194_ub
report("F(97/100) >= 49/1000", F97_lb >= mp.mpf('49') / 1000, "F(97/100) >= %s" % mp.nstr(F97_lb, 7))

# conclusion F >= 49/1000 (high-precision grid, E3)
def F(x):
    return mp.mpf('89') / 100 * mp.sin(mp.mpf('4') / 5 * x) - (x - mp.mpf('89') / 250) * mp.sin(2 * x)
mnF = mp.inf
for i in range(40001):
    x = mp.mpf('0.841') + (mp.mpf('1.1220') - mp.mpf('0.841')) * i / 40000
    mnF = min(mnF, F(x))
report("F >= 0.04 (grid)", mnF >= mp.mpf('0.04'), "min F = %s" % mp.nstr(mnF, 9))
mxu = -mp.inf
for i in range(40001):
    x = mp.mpf('0.841') + (mp.mpf('1.1220') - mp.mpf('0.841')) * i / 40000
    mxu = max(mxu, x * mp.sin(2 * x) / (mp.sin(mp.mpf('0.8') * x) + mp.mpf('0.4') * mp.sin(2 * x)))
report("u_c04 <= 89/100 (grid)", mxu <= mp.mpf('89') / 100, "max u_c04 = %s" % mp.nstr(mxu, 9))

# ---------------- PART D: term1 constants ----------------
print("== PART D: term1 two-case bound ==")
# Case x <= pi/3: term1 >= (4/9)(3 + 2pi/(3 sqrt3)) = 4/3 + 8pi/(27 sqrt3) > 187/100
pi_lo = mp.mpf('31415') / 10000
s3_hi = mp.mpf('17321') / 10000
lhs = 8 * pi_lo / (27 * s3_hi)
report("4/3 + 8*pi/(27 sqrt3) > 187/100", mp.mpf(4) / 3 + lhs > mp.mpf('187') / 100,
       "4/3+8pi/(27 sqrt3) >= %s" % mp.nstr(mp.mpf(4) / 3 + lhs, 9))
# Case x >= pi/3: term1(x,q) >= term1(x,1) = (2x/pi)^2(3+2x cotx) =: f(x), f increasing:
# f'(x) = (8x/pi^2) b(x), b(x) = 3 + 3x cotx - x^2 csc^2x
# b(x) >= 3 + 3(5pi/14) tan(pi/7) - (4/3)(5pi/14)^2 > 0
#   x cotx >= (5pi/14) cot(5pi/14) = (5pi/14) tan(pi/7),  x^2 csc^2x <= (5pi/14)^2 / sin^2(pi/3)
pi_hi = mp.mpf('31416') / 10000
t7 = mp.mpf('3.1415') / 7
tan_lb = t7 + t7**3 / 3 + 2 * t7**5 / 15          # tan t >= t + t^3/3 + 2t^5/15, t <= pi/2
b_lb = 3 + 3 * (5 * pi_lo / 14) * tan_lb - mp.mpf(4) / 3 * (5 * pi_hi / 14)**2
report("b(x) = 3+3xcotx-x^2 csc^2x > 0 on [pi/3,5pi/14]", b_lb > 0, "b >= %s" % mp.nstr(b_lb, 7))
# d/dq (Phi/D) = (q^2 sin^2x - cos^2x)/D^2 > 0 for x >= pi/3 > pi/4  (grid check)
mn_dq = mp.inf
for i in range(2001):
    x = PI / 3 + (5 * PI / 14 - PI / 3) * i / 2000
    q = mp.mpf('1') + i / 2000
    if mp.mpf('0.4') < c1(x, q) < mp.mpf('0.5'):
        mn_dq = min(mn_dq, q**2 * mp.sin(x)**2 - mp.cos(x)**2)
report("d/dq(Phi/D) >= 0 for x >= pi/3 (grid)", mn_dq >= 0, "min = %s" % mp.nstr(mn_dq, 7))
# term1(x,q) >= term1(x,1) on x >= pi/3 (grid) and f increasing (grid)
mn_t1q1 = mp.inf; mn_f = mp.inf
for i in range(2001):
    x = PI / 3 + (5 * PI / 14 - PI / 3) * i / 2000
    c1v = c1(x, 1)
    t1q1 = PhV(x, 1)**2 * (3 + 2 * x * mp.cot(x)) / DV(x, 1, c1v)**2
    mn_t1q1 = min(mn_t1q1, t1q1)
    mn_f = min(mn_f, (2 * x / PI)**2 * (3 + 2 * x * mp.cot(x)))
report("term1(x,1) >= 187/100 on [pi/3,5pi/14] (grid)", mn_t1q1 >= mp.mpf('187') / 100,
       "min term1(x,1) = %s" % mp.nstr(mn_t1q1, 8))
report("f(x) >= f(pi/3) (grid)", mn_f >= mp.mpf(4) / 3 + 8 * pi_lo / (27 * s3_hi),
       "min f = %s" % mp.nstr(mn_f, 8))

# ---------------- PART E: composed chain ----------------
print("== PART E: composed chain ==")
# J1 >= G^2 + Gc - u*Gx
#    >= 4 + 187/100 - (u^2 C - 3 u u_x / x)      [G <= -2, Gc >= 187/100, u Gx <= u^2 C - 3 u u_x/x]
#    >= 4 + 187/100 - ((89/100)^2 * 8 - 4/3)     [u <= 89/100, C <= 8, u u_x >= 4x/9]
num = 4 + mp.mpf('187') / 100 - (mp.mpf('89')**2 * 8 / 100**2 - mp.mpf(4) / 3)
report("composed bound = 6499/7500", num == mp.mpf('6499') / 7500, "= %s" % mp.nstr(num, 12))
report("6499/7500 > 1733/2000", mp.mpf('6499') / 7500 > mp.mpf('1733') / 2000,
       "margin = %s" % mp.nstr(mp.mpf('6499') / 7500 - mp.mpf('1733') / 2000, 8))

print()
print("RESULT:", "ALL PASS" if ok else "SOME FAIL")