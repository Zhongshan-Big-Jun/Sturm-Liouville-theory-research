import mpmath as mp
mp.mp.dps = 30

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

R = 100.0; m = mp.sqrt(mp.mpf(R)); tau = mp.mpf('1.22')
xmid = mp.pi/(1+tau); xmax = mp.pi/tau

xs = [xmid + (xmax-xmid)*i/4000 for i in range(1,4000)]
vals = [rtau(x,m,tau) for x in xs]
crit = []
for i in range(1,len(xs)-1):
    if (vals[i]-vals[i-1])*(vals[i+1]-vals[i]) < 0:
        crit.append(xs[i])
print("critical points:", [round(c,6) for c in crit])
for c in crit:
    print("r(%s) = %s" % (mp.nstr(c,8), mp.nstr(rtau(c,m,tau),12)))
print("r(xmid) =", mp.nstr(rtau(xmid,m,tau),12))
segs_idx = [0] + [xs.index(c) for c in crit] + [len(xs)-1]
for i in range(len(segs_idx)-1):
    a0,a1 = segs_idx[i], segs_idx[i+1]
    if a1>a0:
        seg = vals[a0:a1+1]
        print("segment [%.4f,%.4f]: min=%.8f max=%.8f" % (xs[a0], xs[a1], min(seg), max(seg)))
