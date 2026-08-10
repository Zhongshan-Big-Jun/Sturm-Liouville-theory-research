import mpmath as mp
mp.mp.dps = 60

def M2(q, w):
    A = mp.pi - mp.atan(w/q)
    return 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + mp.atan(w)*(4*A*w - 5*q - 9*q*w**2)

def dqM2_partial_fd(t, h=mp.mpf('1e-12')):
    q = mp.cos(2*t)/(2*mp.sin(t)**2)
    w = 1/mp.tan(t)
    # partial in q holding w fixed
    qp = q + h
    return (M2(qp, w) - M2(q, w))/h

def N_tex(z):
    Pz = 32*z*(z**2+1)**2
    Qz = -10*z**6 - 32*mp.pi*z**5 + 42*z**4 - 64*mp.pi*z**3 + 2*z**2 - 32*mp.pi*z + 46
    Rz = 5*mp.pi*z**6 - 10*z**5 + 8*mp.pi**2*z**5 - 21*mp.pi*z**4 - 40*z**3 + 16*mp.pi**2*z**3 - mp.pi*z**2 - 14*z + 8*mp.pi**2*z - 23*mp.pi
    return mp.atan(z)**2*Pz + mp.atan(z)*Qz + Rz

mx = mp.mpf(0)
for i in range(21):
    t = mp.mpf('0.01') + (mp.atan(1/mp.sqrt(3)) - mp.mpf('0.01'))*mp.mpf(i)/20
    z = mp.tan(t)
    d = abs(dqM2_partial_fd(t) - N_tex(z)/(2*z**2*(z**2+1)**2))
    mx = max(mx, d)
print("partial-derivative max |fd - N_tex/den|:", mx)
print("PARTIAL IDENTITY OK:", mx < mp.mpf('1e-6'))
# conclusion: partial dqM2 < 0 over full range?
mn = mp.mpf(0)
for i in range(2001):
    t = (mp.atan(1/mp.sqrt(3)))*mp.mpf(i)/2000 + mp.mpf('1e-12')
    z = mp.tan(t)
    v = N_tex(z)/(2*z**2*(z**2+1)**2)
    mn = min(mn, v)
print("min partial dqM2 over scan:", mn)
print("NEGATIVE ON RANGE:", mn < 0)
