import mpmath as mp
mp.mp.dps = 60

# ---- CORNER: G2(1/2;q) = G(alpha2; 1/2), alpha2 = pi - x, cos x = q/(q+1) ----
def G(x, c, q):
    Phi = mp.cos(x)**2 + q**2*mp.sin(x)**2
    D = q + c*Phi
    return -Phi*(3+2*x/mp.tan(x))/D + 2*c*x*Phi*(q**2-1)*mp.sin(x)*mp.cos(x)/D**2
def corner(q):
    x = mp.acos(q/(q+1))
    return G(mp.pi - x, mp.mpf(1)/2, q)
def corner_claim(q):
    x = mp.acos(q/(q+1))
    return 2*q*(q+1)*(mp.pi - x - 3*mp.sin(x))/(2*q+1)**mp.mpf(1.5)
mx = mp.mpf(0)
for qv in [mp.mpf(2), mp.mpf('2.5'), mp.mpf(3), mp.mpf(5), mp.mpf(10), mp.mpf('1.001')]:
    d = abs(corner(qv) - corner_claim(qv))
    mx = max(mx, d)
print("CORNER max |G2 - claim|:", mx)
print("G2(1/2;2) =", corner(mp.mpf(2)), " claim:", corner_claim(mp.mpf(2)))
print("CORNER OK:", mx < mp.mpf('1e-50'))

# ---- dqM2 at w_b: q = cos2t/(2 sin^2 t), w = cot t ----
def M2(q, w):
    A = mp.pi - mp.atan(w/q)
    return 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + mp.atan(w)*(4*A*w - 5*q - 9*q*w**2)
def dqM2_num(t):
    q = mp.cos(2*t)/(2*mp.sin(t)**2)
    w = 1/mp.tan(t)
    # numeric derivative d/dq: (dM2/dt)/(dq/dt)
    h = mp.mpf('1e-30')
    dM = (M2(q, w + mp.mpf(0)) - M2(q, w + mp.mpf(0)))*0  # placeholder
    # use derivative along the curve: dM2/dq = (dM2/dt)/(dq/dt)
    def M2_of_t(tt):
        qq = mp.cos(2*tt)/(2*mp.sin(tt)**2)
        ww = 1/mp.tan(tt)
        A = mp.pi - mp.atan(ww/qq)
        return 4*A**2*ww*qq - 7*A*qq**2 - 9*A*ww**2 + 2*A*(qq**2+ww**2)/(1+ww**2) + mp.atan(ww)*(4*A*ww - 5*qq - 9*qq*ww**2)
    dMdt = mp.diff(M2_of_t, t)
    dqdt = mp.diff(lambda tt: mp.cos(2*tt)/(2*mp.sin(tt)**2), t)
    return dMdt/dqdt
def N_z(z):
    Pz = 32*z*(z**2+1)**2
    Qz = -10*z**6 - 32*mp.pi*z**5 + 42*z**4 - 64*mp.pi*z**3 + 2*z**2 - 32*mp.pi*z + 46
    Rz = 5*mp.pi*z**6 - 10*z**5 + 8*mp.pi**2*z**5 - 21*mp.pi*z**4 - 40*z**3 + 16*mp.pi**2*z**3 - mp.pi*z**2 - 14*z + 8*mp.pi**2*z - 23*mp.pi
    b = mp.atan(z)
    return b**2*Pz + b*Qz + Rz
mx2 = mp.mpf(0)
for i in range(21):
    t = mp.mpf('0.01') + (mp.atan(1/mp.sqrt(3)) - mp.mpf('0.01'))*mp.mpf(i)/20
    z = mp.tan(t)
    lhs = dqM2_num(t)
    rhs = N_z(z)/(2*z**2*(z**2+1)**2)
    mx2 = max(mx2, abs(lhs-rhs))
print("dqM2 max |lhs-rhs|:", mx2)
print("dqM2 OK:", mx2 < mp.mpf('1e-40'))
