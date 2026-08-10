import mpmath as mp, random
mp.mp.dps = 30
def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2
def Phi_closed(A,psi,B,m):
    return (m*A*W(B,m)+m*B*W(A,m)+psi*W(A,m)*W(B,m))/(2*m**2*W(B,m))
def Phi_pieces(A,psi,B,m):
    I1 = (A - mp.sin(A)*mp.cos(A))/(2*m)
    I2 = mp.quad(lambda t: (mp.sin(A)/m*mp.cos(t)+mp.cos(A)*mp.sin(t))**2, [0,psi])
    syb = mp.cos(psi)*mp.sin(A)/m + mp.sin(psi)*mp.cos(A)
    dyb = -mp.sin(psi)*mp.sin(A)/m + mp.cos(psi)*mp.cos(A)
    lam2 = syb**2 + (dyb/m)**2
    I3 = m*(B - mp.sin(B)*mp.cos(B))/2*lam2
    return I1+I2+I3

random.seed(1)
worst = 0
for _ in range(50):
    m = mp.mpf(random.uniform(1.01, 5))
    A = mp.mpf(random.uniform(0.1, 2.5))
    psi = mp.mpf(random.uniform(0.05, 2))
    B = mp.mpf(random.uniform(0.1, 2.5))
    d = Phi_closed(A,psi,B,m)-Phi_pieces(A,psi,B,m)
    if abs(d) > worst: worst = abs(d)
print("max |closed-pieces| over random (A,psi,B):", mp.nstr(worst,8))
