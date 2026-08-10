# _audit_sub_A_debug.py — high precision numerical checks of the failing identities
from mpmath import mp, mpf, sin, cos, tan, atan, cot, sqrt, pi, asin, acos
mp.dps = 60

def Phi(qq, xx): return cos(xx)**2 + qq**2*sin(xx)**2
def G_mp(xx, qq, cc):
    P = Phi(qq, xx); D = qq + cc*P
    return -P*(3+2*xx*cot(xx))/D + 2*cc*xx*P*(qq**2-1)*sin(xx)*cos(xx)/D**2

# 1. lem:boundary M2 closed form: parametrize theta
def M2(qq, ww):
    A = pi - atan(ww/qq)
    return 4*A**2*ww*qq - 7*A*qq**2 - 9*A*ww**2 + 2*A*(qq**2+ww**2)/(1+ww**2) + atan(ww)*(4*A*ww - 5*qq - 9*qq*ww**2)
ok1 = True
for th in [mpf('0.05'), mpf('0.2'), mpf('0.5')]:
    qq = cos(2*th)/(2*sin(th)**2); ww = cot(th)
    lhs = M2(qq, ww)
    rhs = 2*(2*th-pi)*cot(th)**2*((2*th-pi)*cot(th) + 2/sin(th)**2)
    if abs(lhs-rhs) > mpf('1e-40'): ok1 = False; print("M2 boundary mismatch", th, lhs, rhs)
print("M2 boundary closed form:", ok1)

# 2. dqM2 at boundary = N/(2z^2(z^2+1)^2)
def dM2dq(qq, ww):
    A = pi - atan(ww/qq)
    # partial derivative wrt q: symbolic then evaluate
    h = mpf('1e-25')
    return (M2(qq+h, ww) - M2(qq-h, ww))/(2*h)
ok2 = True
for zz in [mpf('0.1'), mpf('0.4'), mpf('0.577')]:
    th = atan(zz)
    qq = cos(2*th)/(2*sin(th)**2); ww = cot(th)
    lhs = dM2dq(qq, ww)
    beta = atan(zz)
    Pz = 32*zz*(zz**2+1)**2
    Qz = -10*zz**6 - 32*pi*zz**5 + 42*zz**4 - 64*pi*zz**3 + 2*zz**2 - 32*pi*zz + 46
    Rz = 5*pi*zz**6 - 10*zz**5 + 8*pi**2*zz**5 - 21*pi*zz**4 - 40*zz**3 + 16*pi**2*zz**3 - pi*zz**2 - 14*zz + 8*pi**2*zz - 23*pi
    Nz = beta**2*Pz + beta*Qz + Rz
    rhs = Nz/(2*zz**2*(zz**2+1)**2)
    if abs(lhs-rhs) > mpf('1e-12'): ok2 = False; print("dqM2 boundary mismatch", zz, lhs, rhs)
print("dqM2 boundary:", ok2)

# 3. CORNER: G2(1/2;q) closed form
ok3 = True
for qq in [mpf('1.1'), mpf('2'), mpf('5')]:
    xq = acos(qq/(qq+1))
    lhs = G_mp(pi-xq, qq, mpf('0.5'))
    rhs = 2*qq*(qq+1)*(pi-xq-3*sin(xq))/(2*qq+1)**mpf('1.5')
    if abs(lhs-rhs) > mpf('1e-40'): ok3 = False; print("CORNER mismatch", qq, lhs, rhs)
print("CORNER closed form:", ok3)
print("G2(1/2;2) =", 12*(pi-acos(mpf(2)/3)-sqrt(5))/(5*sqrt(5)), "> 0")

# 4. C4: IN = A*K(v) on c=0.4
def IN(qq, ww):
    A = pi - atan(ww/qq)
    return (qq**2+ww**2)*A*(2*A*qq - 3*ww + 2*atan(ww)) - 3*ww*qq*(1+ww**2)*atan(ww)
ok4 = True
for vv in [2*pi/7, mpf('0.95'), mpf('1.2')]:
    vv = mpf(vv)
    qq = tan(vv)/tan(pi - mpf(5)/2*vv)
    ww = tan(vv)
    Av = mpf(5)/2*vv
    Kv = (qq**2+ww**2)*(5*vv*qq - 3*ww + 2*vv) - mpf(6)/5*ww*qq*(1+ww**2)
    lhs = IN(qq, ww)
    rhs = Av*Kv
    if abs(lhs-rhs) > mpf('1e-35')*max(1,abs(lhs)): ok4 = False; print("C4 IN mismatch", vv, lhs, rhs, lhs-rhs)
print("C4 IN = A K:", ok4)

# 5. F_e'(q,1/2) closed form
def Mf_mp(xx, qq, cc):
    return xx**2*sin(xx)**2/(qq+cc*Phi(qq,xx))
def alpha1_mp(qq, cc):
    lo, hi = mpf('1e-12'), pi/2 - mpf('1e-12')
    for _ in range(200):
        mid = (lo+hi)/2
        if cc*mid > atan(1/(qq*tan(mid))):
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2
def Fe_mp(qq, cc):
    a1 = alpha1_mp(qq, cc)
    return Mf_mp(a1, qq, cc) - Mf_mp(pi-a1, qq, cc)
ok5 = True
for qq in [mpf('1.1'), mpf('1.5'), mpf('2')]:
    h = mpf('1e-9')
    num = (Fe_mp(qq, mpf('0.5')+h) - Fe_mp(qq, mpf('0.5')-h))/(2*h)
    xq = 2*asin(1/sqrt(2*(qq+1)))
    Pq = 3*xq**2 + 6*xq*sin(xq) - 3*pi*xq - 3*pi*sin(xq) + pi**2
    cf = 2*pi*(cos(xq)-1)**3/sin(xq)**3*Pq
    print("q=", qq, "num=", num, "closed=", cf, "rel err", abs(num-cf)/abs(cf))
    if abs(num-cf) > mpf('1e-8'): ok5 = False
print("Fep12 closed form:", ok5)
