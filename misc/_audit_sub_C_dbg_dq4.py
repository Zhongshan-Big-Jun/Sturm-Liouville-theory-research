import mpmath as mp
mp.mp.dps = 60

def M2(q, w):
    A = mp.pi - mp.atan(w/q)
    return 4*A**2*w*q - 7*A*q**2 - 9*A*w**2 + 2*A*(q**2+w**2)/(1+w**2) + mp.atan(w)*(4*A*w - 5*q - 9*q*w**2)

def dqM2_fd(t, h=mp.mpf('1e-14')):
    q = mp.cos(2*t)/(2*mp.sin(t)**2)
    w = 1/mp.tan(t)
    qp = mp.cos(2*(t+h))/(2*mp.sin(t+h)**2)
    wp = 1/mp.tan(t+h)
    return (M2(qp, wp) - M2(q, w))/(qp - q)

def N_true(z):
    b = mp.atan(z)
    N = (32*z**6*b - 16*mp.pi*z**6 + 48*z**5*b**2 - 48*mp.pi*z**5*b - 16*z**5 + 12*mp.pi**2*z**5
         + 96*z**4*b - 48*mp.pi*z**4 + 96*z**3*b**2 - 96*mp.pi*z**3*b - 32*z**3 + 24*mp.pi**2*z**3
         + 128*z**2*b - 64*mp.pi*z**2 + 48*z*b**2 - 48*mp.pi*z*b - 16*z + 12*mp.pi**2*z + 64*b - 32*mp.pi)
    return N

def N_tex(z):
    Pz = 32*z*(z**2+1)**2
    Qz = -10*z**6 - 32*mp.pi*z**5 + 42*z**4 - 64*mp.pi*z**3 + 2*z**2 - 32*mp.pi*z + 46
    Rz = 5*mp.pi*z**6 - 10*z**5 + 8*mp.pi**2*z**5 - 21*mp.pi*z**4 - 40*z**3 + 16*mp.pi**2*z**3 - mp.pi*z**2 - 14*z + 8*mp.pi**2*z - 23*mp.pi
    b = mp.atan(z)
    return b**2*Pz + b*Qz + Rz

for t in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('0.52359877559829887308')]:
    z = mp.tan(t)
    fd = dqM2_fd(t)
    ntrue = N_true(z)/(2*z**2*(z**2+1)**2)
    ntex = N_tex(z)/(2*z**2*(z**2+1)**2)
    print("t=%.6f  fd=%.12f  N_true/den=%.12f  N_tex/den=%.12f" % (t, fd, ntrue, ntex))
