import mpmath as mp
mp.mp.dps = 40
def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2
def J(x, m): return mp.sin(x)**2/W(x, m)

m = mp.sqrt(100); tau = mp.mpf('1.22')
y = mp.pi - mp.mpf('1.5')
print("y =", mp.nstr(y,10))
ty = tau*y
print("tau y =", mp.nstr(ty,10), " in (0,pi)?", 0 < ty < mp.pi)
print("tau(pi-y) =", mp.nstr(tau*(mp.pi-y),10))
print("J(tau y) =", mp.nstr(J(ty,m),15))
print("J(tau(pi-y)) =", mp.nstr(J(tau*(mp.pi-y),m),15))
print("J(tau y - (tau-1)pi) =", mp.nstr(J(ty-(tau-1)*mp.pi,m),15))
print("J(y) =", mp.nstr(J(y,m),15))
print("J(pi-y) =", mp.nstr(J(mp.pi-y,m),15))
print("r(y) =", mp.nstr(J(ty,m)/J(y,m),15))
print("r(pi-y) =", mp.nstr(J(tau*(mp.pi-y),m)/J(mp.pi-y,m),15))
