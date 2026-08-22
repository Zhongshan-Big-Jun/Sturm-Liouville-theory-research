import numpy as np, math
from scipy.optimize import least_squares

def compute_ratios(widths, R, n, npts=30000, refine=3):
    """Return lambda_n, lambda_{n+1} and normalized eigenfunctions on a mesh? We'll do shoot."""
    # widths list of (L,c)
    hi=math.sqrt(R*((n+3)**2*math.pi**2+10))
    om=np.linspace(1e-7,hi,npts)
    M00=np.ones(npts); M01=np.zeros(npts); M10=np.zeros(npts); M11=np.ones(npts)
    for L,c in widths:
        ww=om*math.sqrt(c); wl=ww*L
        cw=np.cos(wl); sw=np.sin(wl)/ww; sw2=-ww*np.sin(wl)
        M00,M01,M10,M11=M00*cw+M01*sw2,M00*sw+M01*cw,M10*cw+M11*sw2,M10*sw+M11*cw
    d=M01
    signs=np.signbit(d[1:])!=np.signbit(d[:-1]); idx=np.nonzero(signs)[0]
    roots=[]
    for i in idx:
        lo,hi2=om[i],om[i+1]
        for _ in range(refine):
            sg=np.linspace(lo,hi2,1200)
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

def state_at(x, omega, widths, R):
    """Propagate from 0 with u(0)=0,u'(0)=1; return u(x),u'(x) before normalization."""
    M00,M01,M10,M11=1.0,0.0,0.0,1.0
    u=0.0; up=1.0
    pos=0.0
    for L,c in widths:
        if x < pos+L-1e-12:
            # propagate only part
            Lp=x-pos
            ww=omega*math.sqrt(c); wl=ww*Lp
            cw=math.cos(wl); sw=math.sin(wl)/ww; sw2=-ww*math.sin(wl)
            # multiply vector by block matrix from current (u,up)
            u,up = u*cw+up*sw, -u*ww*sw + up*cw
            return u,up
        else:
            L2=pos+L
            ww=omega*math.sqrt(c); wl=ww*L
            cw=math.cos(wl); sw=math.sin(wl)/ww; sw2=-ww*math.sin(wl)
            u,up = u*cw+up*sw, -u*ww*sw + up*cw
            pos=L2
    # x at endpoint
    raise RuntimeError('x beyond')

def normalized_eig(widths, R, lambda_k, N=2000):
    """Compute normalized u on mesh by shooting and scale."""
    omega=math.sqrt(lambda_k)
    # integrate norm using shooting on blocks
    # we can compute normalized values at switch positions via shooting and norm numerical quadrature
    # Use high-order Simpson on each block using exact u(phase)
    # Prepare block boundaries
    xs=[0.0]
    for L,c in widths: xs.append(xs[-1]+L)
    # ODE integrate state (u,up) with exact transfer, collect values at points including switches
    pts=[]
    for L in xs: pts.append(L)
    # also midpoints maybe
    # sample each block at 20 points for quadrature
    samples=[]
    for idx,(L,c) in enumerate(widths):
        a=xs[idx]; b=xs[idx+1]
        for m in range(20):
            t=a+(b-a)*(m+0.5)/20
            samples.append((t,c,L, (m+0.5)/20-0.5))
    # but easier use fine global points
    # compute u on many points by shooting start-to-point
    def u_at(x):
        return state_at(x, omega, widths, R)[0]
    grid=[]
    for i in range(N+1):
        x=i/N
        grid.append(u_at(x))
    grid=np.array(grid)
    norm2=np.dot(grid, grid)*(1.0/N)*2  # Simpson-ish approximate trapezoid, okay
    # more accurate: use scipy quad? skip.
    # Use normalization to rho weighted: ∫ rho u^2; approximate using node points per block with Simpson
    norm=0.0
    for idx,(L,c) in enumerate(widths):
        a=xs[idx]; b=xs[idx+1]
        # use 20-point Gauss-Legendre on each block
        for k in range(10):
            xk = a + (b-a)*( (2*k+1)/(20) )  # crude midpoint
            uk=u_at(xk)
            norm += c*uk*uk*(b-a)
    scale=1/math.sqrt(norm)
    # values at switch positions
    vals=[]
    for x in xs[1:-1]:
        u=u_at(x)
        vals.append(u*scale)
    return omega, grid, scale, vals

def G_at_switches(widths, R, n):
    # widths list; n is index (lambda_n, lambda_{n+1})
    lam=compute_ratios(widths,R,n,npts=20000,refine=2)
    a,b=lam[n-1],lam[n]
    # get omega and function values at switches normalized
    omega_n=math.sqrt(a); omega_p=math.sqrt(b)
    # compute u at switch positions for both modes and normalize ∫ρu^2=1
    # We'll implement shoot + quadrature using scipy.integrate.quad? simpler Gauss with many points.
    # Use 40-point Gauss-Legendre per block.
    import numpy.polynomial.legendre as leg
    gauss_x,gauss_w=leg.leggauss(40)
    def norm_u(omega):
        # define u at x by state_at from 0
        def u(x): return state_at(x, omega, widths, R)[0]
        xs=[0.0]
        for L,c in widths: xs.append(xs[-1]+L)
        val=0.0
        for idx,(L,c) in enumerate(widths):
            a=xs[idx]; b=xs[idx+1]
            for xi,wi in zip(gauss_x,gauss_w):
                x=(a+b)/2 + (b-a)/2*xi
                uu=u(x)
                val += c*uu*uu*(b-a)/2*wi
        return val
    normn=math.sqrt(norm_u(omega_n)); normp=math.sqrt(norm_u(omega_p))
    xs=[0.0]
    for L,c in widths: xs.append(xs[-1]+L)
    G=[]
    for x in xs[1:-1]:
        un=state_at(x,omega_n,widths,R)[0]/normn
        up=state_at(x,omega_p,widths,R)[0]/normp
        G.append(un*un-up*up)
    return np.array(G), (a,b)

def residual(widths, R, n):
    try:
        G,_=G_at_switches(widths,R,n)
        return G
    except Exception:
        return np.array([1e6]* (2*n))

# define widths from switch positions: pattern [1,R,1,...]; x1..x_{2n}
def widths_from_x(xs, R):
    pts=[0.0]+list(xs)+[1.0]
    widths=[]
    for i in range(len(pts)-1):
        vals=1.0 if i%2==0 else R
        widths.append((pts[i+1]-pts[i], vals))
    return widths

for R in (4.0,):
    n=2
    # start from evenly spaced for R=1
    x0=np.linspace(0,1,2*n+1)[1:-1]
    # for R>1 start balanced width maybe known
    if R>1:
        s=math.sqrt(R); t=1.0/((n+1)*s+n); w1=s*t; w2=t
        x0=np.cumsum([w1,w2,w1,w2])[:2*n]
    # refine residual
    for trial in range(3):
        sol=least_squares(lambda xs: residual(widths_from_x(xs,R),R,n), x0, bounds=(np.array([1e-4]*(2*n)), np.array([1-1e-4]*(2*n))), method='trf', max_nfev=200, xtol=1e-10, ftol=1e-12)
        x0=sol.x
    print('R',R,'x',np.round(sol.x,6),'res',np.linalg.norm(sol.fun))
