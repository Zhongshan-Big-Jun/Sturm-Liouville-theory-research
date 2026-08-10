import mpmath as mp
mp.mp.dps = 60

def M2(q, w):
    A = mp.pi - mp.atan(w/q)
    return 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + mp.atan(w)*(4*A*w - 5*q - 9*q*w**2)

def dqM2_fd(t, h=mp.mpf('1e-12')):
    q = mp.cos(2*t)/(2*mp.sin(t)**2)
    w = 1/mp.tan(t)
    # w_b(q) = sqrt(2q+1): check consistency
    q2 = (w**2-1)/2
    assert abs(q-q2) < mp.mpf('1e-40')
    qp = mp.cos(2*(t+h))/(2*mp.sin(t+h)**2)
    wp = 1/mp.tan(t+h)
    return (M2(qp, wp) - M2(q, w))/(qp - q)

def N_z(z):
    Pz = 32*z*(z**2+1)**2
    Qz = -10*z**6 - 32*mp.pi*z**5 + 42*z**4 - 64*mp.pi*z**3 + 2*z**2 - 32*mp.pi*z + 46
    Rz = 5*mp.pi*z**6 - 10*z**5 + 8*mp.pi**2*z**5 - 21*mp.pi*z**4 - 40*z**3 + 16*mp.pi**2*z**3 - mp.pi*z**2 - 14*z + 8*mp.pi**2*z - 23*mp.pi
    b = mp.atan(z)
    return b**2*Pz + b*Qz + Rz

for t in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5')]:
    z = mp.tan(t)
    q = mp.cos(2*t)/(2*mp.sin(t)**2)
    print("t=%.3f z=%.6f q=%.6f" % (t, z, q))
    print("  dqM2 (fd)      :", dqM2_fd(t))
    print("  N/(2z^2(z^2+1)^2):", N_z(z)/(2*z**2*(z**2+1)**2))
