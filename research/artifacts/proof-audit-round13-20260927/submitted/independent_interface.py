"""Independent high-precision physical transfer and implicit derivatives.
No repository spectral enumerator, normalization, or Jacobian code is imported.
"""
import mpmath as mp

def step(y, dy, k, width):
    c, s = mp.cos(k*width), mp.sin(k*width)
    return y*c + dy*s/k, -y*k*s + dy*c

def shoot(edges, omega):
    pts=[mp.mpf(0),*edges,mp.mpf(1)]
    y,dy,mass=mp.mpf(0),mp.mpf(1),mp.mpf(0)
    values=[]
    for j,rho in enumerate((1,4,1)):
        L=pts[j+1]-pts[j];k=omega*mp.sqrt(rho)
        A,B=y,dy/k
        mass+=rho*(A*A*(L/2+mp.sin(2*k*L)/(4*k))+B*B*(L/2-mp.sin(2*k*L)/(4*k))+A*B*mp.sin(k*L)**2/k)
        y,dy=step(y,dy,k,L)
        values.append(y)
    return y,mass,values

def replace(xs,i,t):
    ys=list(xs);ys[i]=t;return ys

def run(dps=65):
    with mp.workdps(dps):
        x=[mp.mpf(1)/4,mp.mpf(3)/4]
        wa=mp.findroot(lambda w:shoot(x,w)[0],(mp.mpf('1.6'),mp.mpf('1.8')))
        wb=mp.findroot(lambda w:shoot(x,w)[0],(mp.mpf('3.7'),mp.mpf('3.9')))
        # Rayleigh comparison excludes an unobserved second root below wa and
        # an unobserved third root below wb: omega_2>=pi, omega_3>=3*pi/2.
        if not (mp.pi/2<wa<mp.pi<wb<3*mp.pi/2):raise RuntimeError('mode identity bound failed')
        def res(edges,a,b,j):
            av=shoot(edges,a);bv=shoot(edges,b)
            return (a*a*av[2][j]**2/av[1]-b*b*bv[2][j]**2/bv[1])/(b*b)
        dws=[]
        for w in (wa,wb):
            denom=mp.diff(lambda t:shoot(x,t)[0],w)
            dws.append([-mp.diff(lambda t:shoot(replace(x,i,t),w)[0],x[i])/denom for i in range(2)])
        J=[]
        for j in range(2):
            J.append([mp.diff(lambda t:res(replace(x,i,t),wa,wb,j),x[i])+
              mp.diff(lambda t:res(x,t,wb,j),wa)*dws[0][i]+
              mp.diff(lambda t:res(x,wa,t,j),wb)*dws[1][i] for i in range(2)])
        return dict(dps=dps,frequencies=[mp.nstr(wa,dps),mp.nstr(wb,dps)],
             mode_identity='Rayleigh comparison: omega2>=pi>omega1; omega3>=3*pi/2>omega2',
             residual=[mp.nstr(res(x,wa,wb,j),dps) for j in range(2)],
             jacobian=[[mp.nstr(v,dps) for v in row] for row in J])
if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))

def normalized_values(edges, omega, dps=65):
    """Independent single-mode normalization and interface derivatives."""
    with mp.workdps(dps):
        xs=[mp.mpf(float(t)) for t in edges];w=mp.mpf(float(omega))
        yend,mass,_=shoot(xs,w)
        y,dy=mp.mpf(0),mp.mpf(1);vals=[];ders=[];prev=mp.mpf(0)
        for j,end in enumerate([*xs,mp.mpf(1)]):
            rho=(1,4,1)[j]
            y,dy=step(y,dy,w*mp.sqrt(rho),end-prev);prev=end
            if j<2:vals.append(y/mp.sqrt(mass));ders.append(dy/mp.sqrt(mass))
        return {'values':[mp.nstr(v,dps) for v in vals],'derivatives':[mp.nstr(v,dps) for v in ders],
          'mass_unnormalized':mp.nstr(mass,dps),'right_residual':mp.nstr(yend,dps)}
