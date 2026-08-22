import numpy as np, math
from scipy.optimize import least_squares

def compute_ratios(widths, R, n):
    lam = []
    # reuse simple scanning
    hi=math.sqrt(R*((n+3)**2*math.pi**2+10)); npts=20000
    om=np.linspace(1e-7,hi,npts)
    M00=np.ones(npts); M01=np.zeros(npts); M10=np.zeros(npts); M11=np.ones(npts)
    for L,c in widths:
        ww=om*math.sqrt(c); wl=ww*L
        cw=np.cos(wl); sw=np.sin(wl)/ww; sw2=-ww*np.sin(wl)
        M00,M01,M10,M11=M00*cw+M01*sw2,M00*sw+M01*cw,M10*cw+M11*sw2,M10*sw+M11*cw
    d=M01; signs=np.signbit(d[1:])!=np.signbit(d[:-1]); idx=np.nonzero(signs)[0]
    roots=[]
    for i in idx:
        lo,hi2=om[i],om[i+1]
        for _ in range(2):
            sg=np.linspace(lo,hi2,800)
            a00=np.ones(len(sg)); a01=np.zeros(len(sg)); a10=np.zeros(len(sg)); a11=np.ones(len(sg))
            for L,c in widths:
                ww=sg*math.sqrt(c); wl=ww*L
                cw=np.cos(wl); sw=np.sin(wl)/ww; sw2=-ww*np.sin(wl)
                a00,a01,a10,a11=a00*cw+a01*sw2,a00*sw+a01*cw,a10*cw+a11*sw2,a10*sw+a11*cw
            dg=a01; sg_s=np.signbit(dg[1:])!=np.signbit(dg[:-1]); jj=np.nonzero(sg_s)[0]
            if len(jj)==0: break
            lo,hi2=sg[jj[0]],sg[jj[0]+1]
        roots.append((lo+hi2)/2)
        if len(roots)>=n+2: break
    roots=np.sort(roots)
    return roots[:n+1]**2

def state_at(x, omega, widths):
    M00,M01,M10,M11=1.0,0.0,0.0,1.0
    u=0.0; up=1.0; pos=0.0
    for L,c in widths:
        if x < pos+L-1e-12:
            Lp=x-pos
            ww=omega*math.sqrt(c); wl=ww*Lp
            cw=math.cos(wl); sw=math.sin(wl)/ww; sw2=-ww*math.sin(wl)
            u,up = u*cw+up*sw, -u*ww*sw + up*cw
            return u,up
        else:
            ww=omega*math.sqrt(c); wl=ww*L
            cw=math.cos(wl); sw=math.sin(wl)/ww; sw2=-ww*math.sin(wl)
            u,up = u*cw+up*sw, -u*ww*sw + up*cw
            pos=pos+L
    raise RuntimeError('x beyond')

def G_at_switches(widths, R, n):
    lam=compute_ratios(widths,R,n)
    a,b=lam[n-1],lam[n]
    # exact normalization via Gauss-Legendre
    import numpy.polynomial.legendre as leg
    gauss_x,gauss_w=leg.leggauss(50)
    def norm_u(omega):
        xs=[0.0]
        for L,c in widths: xs.append(xs[-1]+L)
        val=0.0
        for idx,(L,c) in enumerate(widths):
            a0=xs[idx]; b0=xs[idx+1]
            for xi,wi in zip(gauss_x,gauss_w):
                x=(a0+b0)/2+(b0-a0)/2*xi
                uu=state_at(x,omega,widths)[0]
                val += c*uu*uu*(b0-a0)/2*wi
        return val
    nn=math.sqrt(norm_u(math.sqrt(a))); np_=math.sqrt(norm_u(math.sqrt(b)))
    xs=[0.0]
    for L,c in widths: xs.append(xs[-1]+L)
    G=[]
    for x in xs[1:-1]:
        un=state_at(x,math.sqrt(a),widths)[0]/nn
        up=state_at(x,math.sqrt(b),widths)[0]/np_
        G.append(un*un-up*up)
    return np.array(G), (a,b)

def residual(widths,R,n):
    try:
        G,_=G_at_switches(widths,R,n)
        return G
    except Exception:
        return np.array([1e6]*(2*n))

def widths_from_x(xs,R):
    pts=[0.0]+list(xs)+[1.0]
    widths=[]
    for i in range(len(pts)-1):
        vals=1.0 if i%2==0 else R
        widths.append((pts[i+1]-pts[i], vals))
    return widths

R=4.0; n=2
# balanced start
s=2.0; t=1.0/((n+1)*s+n); w1=s*t; w2=t
x0=np.array([w1,w1+w2,w1+w2+w1,w1+w2+w1+w2])
print('balanced x',x0)
sol=least_squares(lambda xs: residual(widths_from_x(xs,R),R,n), x0, bounds=(np.array([1e-4]*(2*n)), np.array([1-1e-4]*(2*n))), method='trf', max_nfev=300, xtol=1e-12, ftol=1e-14)
xb=sol.x; Gb,_=G_at_switches(widths_from_x(xb,R),R,n); lam=compute_ratios(widths_from_x(xb,R),R,n)
print('balanced solution x',np.round(xb,6),'res',np.linalg.norm(Gb),'ratio',lam[1]/lam[0] if False else lam[2]/lam[1])
# Try many random starts
rng=np.random.default_rng(1)
sols=[]
for trial in range(20):
    starts=[]
    # random sorted 4 points (or widths dirichlet)
    w=rng.dirichlet(np.ones(5))
    x=np.cumsum(w)[:4]+1e-3
    sol=least_squares(lambda xs: residual(widths_from_x(xs,R),R,n), x, bounds=(np.array([1e-4]*(2*n)), np.array([1-1e-4]*(2*n))), method='trf', max_nfev=200, xtol=1e-10, ftol=1e-12)
    G,lam=G_at_switches(widths_from_x(sol.x,R),R,n)
    if np.linalg.norm(G)<1e-6:
        ratio=lam[1]/lam[0] if False else lam[2]/lam[1]
        # unique key rounded
        key=tuple(np.round(sol.x,4))
        if key not in [tuple(np.round(sx[0],4)) for sx in sols]:
            sols.append((sol.x,ratio))
print('found distinct self-consistent solutions:')
for x,ratio in sols:
    print(' x',np.round(x,6),'ratio',ratio)
