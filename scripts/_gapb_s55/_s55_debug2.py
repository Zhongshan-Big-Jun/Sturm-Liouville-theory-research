import mpmath as mp
mp.mp.dps = 40

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

R = 100; tau = mp.mpf('1.22'); m = mp.sqrt(mp.mpf(R))
xmid = mp.pi/(1+tau); xmax = mp.pi/tau
print("xmid, xmax:", mp.nstr(xmid,8), mp.nstr(xmax,8))
n = 2000
xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
vals = [float(rtau(x,m,tau)) for x in xs]
crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
print("crit indices:", crit, "values:", [round(vals[c],8) for c in crit])

# direct check: x = 1.70, solve r(y)=r(x) in seg3
x = mp.mpf('1.70')
t = rtau(x,m,tau)
print("r(1.70) =", mp.nstr(t,10))
# find y in (2.013, 2.575) with r(y)=t
f = lambda y: rtau(y,m,tau)-t
ya, yb = mp.mpf('2.02'), mp.mpf('2.57')
print("f(2.02) =", mp.nstr(f(ya),8), " f(2.57) =", mp.nstr(f(yb),8))
if f(ya)*f(yb) < 0:
    y = mp.findroot(f, (ya,yb), solver='bisect')
    print("y =", mp.nstr(y,15), " x+y =", mp.nstr(x+y,15), " pi =", mp.nstr(mp.pi,15))
