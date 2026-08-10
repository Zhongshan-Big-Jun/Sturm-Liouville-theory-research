import mpmath as mp
mp.mp.dps = 50
u = mp.mpf('0.1'); R = mp.mpf('1000')
sR = mp.sqrt(R)
def mu1bar(u): return mp.pi**2/(4*u**2)
# a root
f = lambda a: mp.tan(a) - a*(1 - mp.mpf(1)/(2*u))
lo, hi = mp.pi/2 + mp.mpf('1e-25'), mp.pi - mp.mpf('1e-25')
al, ah = lo, hi
for k in range(1, 100000):
    x = lo + (hi-lo)*k/100000
    if f(x) > 0:
        ah = x; break
    al = x
a = mp.findroot(f, (al, ah))
mu2bar = (a/u)**2
print("mu1bar =", mp.nstr(mu1bar(u), 20))
print("mu2bar =", mp.nstr(mu2bar, 20))
O = lambda m: mp.tan(mp.sqrt(m)*u) + sR*mp.tan(mp.sqrt(m/R)*(mp.mpf(1)/2 - u))
for m in [mu1bar(u)*(1+mp.mpf('1e-9')), (mu1bar(u)+mu2bar)/2, mu2bar*(1-mp.mpf('1e-12')), mu2bar]:
    print("O(", mp.nstr(m,5), ") =", mp.nstr(O(m),6))