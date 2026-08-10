import mpmath as mp
mp.mp.dps = 40

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def structure(R, tau, n=12000):
    m = mp.sqrt(mp.mpf(R))
    xmid = mp.pi/(1+tau); xmax = mp.pi/tau
    xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
    vals = [float(rtau(x,m,tau)) for x in xs]
    crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    cvals = [xs[c] for c in crit]
    rpi2 = rtau(mp.pi/2, m, tau)
    # c1 = first critical, c2 = second
    c1, c2 = (cvals[0], cvals[1]) if len(cvals)>=2 else (None, None)
    # find y0 = solution of r(y)=r(pi/2) in (c1, c2)
    y0 = None
    if c1 is not None and c2 is not None and len(cvals)==2:
        f = lambda y: rtau(y,m,tau)-rpi2
        # bisection in (c1, c2) if sign change
        if f(c1)*f(c2) < 0:
            y0 = mp.findroot(f, (c1,c2), solver='bisect')
    # min over x-in-I pairs: S(c) -> pi/2 + y0 at c->r(pi/2)+
    return dict(m=m, xmid=xmid, xmax=xmax, crit=cvals, rpi2=rpi2, c1=c1, c2=c2, y0=y0,
                r_c1=rtau(c1,m,tau) if c1 else None, r_c2=rtau(c2,m,tau) if c2 else None)

for (R, tau) in [(100, mp.mpf('1.22')), (10000, mp.mpf('1.5')), (1000, mp.mpf('1.3')), (100, mp.mpf('1.5')), (10, mp.mpf('1.1')), (100000, mp.mpf('1.5'))]:
    S = structure(R, tau)
    print(f"R={R}, tau={tau}")
    print("  xmid=%.5f pi/2=%.5f pi/tau=%.5f" % (float(S['xmid']), float(mp.pi/2), float(S['xmax'])))
    print("  criticals:", [round(float(c),6) for c in S['crit']])
    print("  r(pi/2)=%.7f r(c1)=%.7f r(c2)=%.7f" % (float(S['rpi2']), float(S['r_c1']) if S['r_c1'] else float('nan'), float(S['r_c2']) if S['r_c2'] else float('nan')))
    if S['y0'] is not None:
        print("  y0 (r(y0)=r(pi/2) in (c1,c2)) = %.7f;  pi/2 + y0 = %.7f; margin over pi: %.7f" % (float(S['y0']), float(mp.pi/2+S['y0']), float(mp.pi/2+S['y0']-mp.pi)))
        print("  x-in-I pairs exist: levels in (r(pi/2), r(c2)), min sum -> pi/2+y0 > pi:", float(mp.pi/2+S['y0']) > float(mp.pi))
    else:
        print("  no x-in-I pairs (bump not above r(pi/2))")
