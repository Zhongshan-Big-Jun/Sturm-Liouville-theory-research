import mpmath as mp
mp.mp.dps = 40
def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2
def J(x, m): return mp.sin(x)**2/W(x, m)
def rtau(x, m, tau): return J(tau*x, m)/J(x, m)

m = mp.sqrt(100); tau = mp.mpf('1.22')
x = mp.mpf('1.5')
print("x =", mp.nstr(x,8), " pi-x =", mp.nstr(mp.pi-x,8))
print("r(x)      =", mp.nstr(rtau(x,m,tau),15))
print("r(pi-x)   =", mp.nstr(rtau(mp.pi-x,m,tau),15))
print("r(pi-x) vs r(x):", ">" if rtau(mp.pi-x,m,tau)>rtau(x,m,tau) else "<")
# Lemma E at y = pi - x
y = mp.pi - x
print("y = pi-x in (pi/2, pi/tau)?", float(y) > float(mp.pi/2) and float(y) < float(mp.pi/tau))
print("r(y) =", mp.nstr(rtau(y,m,tau),15), " r(pi-y) = r(x) =", mp.nstr(rtau(x,m,tau),15))
