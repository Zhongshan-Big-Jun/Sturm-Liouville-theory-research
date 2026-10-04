"""Independent mpmath physical ODE/zero-count reference; no repo imports.
Root guesses are local seeds, not evidence of index. Indices are checked by
zeros of the piecewise trigonometric physical solution; mass uses quadrature.
Floating high precision here is not an interval certificate.
"""
import mpmath as mp

def step(y, dy, omega, rho, length):
    k = omega * mp.sqrt(rho)
    if not k:
        return y + dy*length, dy
    return (y*mp.cos(k*length) + dy*mp.sin(k*length)/k,
            -y*k*mp.sin(k*length) + dy*mp.cos(k*length))

def starts(blocks, omega):
    y,dy = mp.mpf(0),mp.mpf(1)
    states = [(y,dy)]
    for length,rho in blocks:
        y,dy=step(y,dy,omega,rho,length)
        states.append((y,dy))
    return states

def count_internal_zeros(blocks, omega, states):
    L=sum(t[0] for t in blocks); x=mp.mpf(0); zeros=[]
    tol=mp.mpf(10)**(-mp.mp.dps//2)
    for (length,rho),(y,dy) in zip(blocks,states):
        k=omega*mp.sqrt(rho); alpha=mp.atan2(y,dy/k)
        lower=int(mp.floor(alpha/mp.pi))-1
        upper=int(mp.ceil((alpha+k*length)/mp.pi))+1
        for j in range(lower,upper+1):
            t=(j*mp.pi-alpha)/k
            xx=x+t
            if -tol<t<length+tol and tol<xx<L-tol:
                if not any(abs(xx-z)<tol for z in zeros):zeros.append(xx)
        x+=length
    return sorted(zeros)

def evaluate(blocks_in, guesses, dps=65):
    with mp.workdps(dps):
        blocks=[(mp.mpf(float(l)),mp.mpf(float(r))) for l,r in blocks_in]
        out=[]
        for index,guess in guesses:
            w=mp.findroot(lambda t:starts(blocks,t)[-1][0],
                          (mp.mpf(float(guess))*.9999,mp.mpf(float(guess))*1.0001),
                          tol=mp.mpf(10)**(-(dps-10)))
            st=starts(blocks,w)
            zeros=count_internal_zeros(blocks,w,st)
            if len(zeros)!=index-1:raise RuntimeError('independent zero count disagrees with requested mode')
            mass=mp.mpf(0)
            for (length,rho),(y,dy) in zip(blocks,st):
                mass+=rho*mp.quad(lambda t:step(y,dy,w,rho,t)[0]**2,[0,length])
            vals=[v[0]/mp.sqrt(mass) for v in st[1:-1]]
            ders=[v[1]/mp.sqrt(mass) for v in st[1:-1]]
            out.append(dict(index=index,frequency=mp.nstr(w,dps),eigenvalue=mp.nstr(w*w,dps),
                    mass=mp.nstr(mass,dps),values=[mp.nstr(v,dps) for v in vals],
                    derivatives=[mp.nstr(v,dps) for v in ders],
                    internal_zero_count=len(zeros),internal_zeros=[mp.nstr(z,dps) for z in zeros],
                    right_residual=mp.nstr(st[-1][0],dps)))
        if len(out)==2:
            a,b=[mp.mpf(t['eigenvalue']) for t in out]
            u,v=[[mp.mpf(z) for z in t['values']] for t in out]
            f=[a*x*x-b*y*y for x,y in zip(u,v)]
            r=[ff/(a*x*x+b*y*y) for ff,x,y in zip(f,u,v)]
        else:f=[];r=[]
        return dict(dps=dps,method='physical transfer; explicit trigonometric zero count; block quadrature mass',
                    modes=out,raw_residual=[mp.nstr(t/b,dps) for t in f],
                    relative_defect=[mp.nstr(t,dps) for t in r])
