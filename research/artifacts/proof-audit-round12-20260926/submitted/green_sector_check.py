"""Independent high-precision transfer calculation; not repository code."""
from pathlib import Path
import mpmath as mp
import json
mp.mp.dps=65

def step(y,dy,w,L):
    c,s=mp.cos(w*L),mp.sin(w*L)
    return y*c+dy*s/w,-w*y*s+dy*c

def shoot(blocks,omega):
    y,dy,mass=mp.mpf(0),mp.mpf(1),mp.mpf(0)
    nodes=[]
    for L,rho in blocks:
        w=omega*mp.sqrt(rho)
        a,b=y,dy/w
        mass+=rho*(a*a*(L/2+mp.sin(2*w*L)/(4*w))+b*b*(L/2-mp.sin(2*w*L)/(4*w))+a*b*mp.sin(w*L)**2/w)
        y,dy=step(y,dy,w,L)
        nodes.append((y,dy))
    return y,dy,mass,nodes

def hblocks(x1,x2):
    return [(x1,mp.mpf(1)),(x2-x1,mp.mpf(4)),(mp.mpf('.5')-x2,mp.mpf(1))]

def equations(x1,x2,wa,wb):
    hb=hblocks(x1,x2)
    a,b=shoot(hb,wa),shoot(hb,wb)
    return (a[0],b[1],*(wa**2*a[3][i][0]**2/(2*a[2])-wb**2*b[3][i][0]**2/(2*b[2]) for i in range(2)))

def fb(edges):
    pts=[mp.mpf(0),*edges,mp.mpf(1)]
    return [(pts[i+1]-pts[i],mp.mpf(1 if i%2==0 else 4)) for i in range(5)]

def residual(edges,wa,wb):
    a,b=shoot(fb(edges),wa),shoot(fb(edges),wb)
    return mp.matrix([(wa**2*a[3][j][0]**2/a[2]-wb**2*b[3][j][0]**2/b[2])/wb**2 for j in range(4)])

def replace(x,j,t):
    z=list(x); z[j]=t; return z

def at(blocks,omega,x,left=True,bc='D'):
    if left:
        y,dy=mp.mpf(0),mp.mpf(1); z=mp.mpf(0)
        for L,rho in blocks:
            t=min(L,x-z)
            y,dy=step(y,dy,omega*mp.sqrt(rho),t)
            z+=L
            if x<=z: return y,dy
    else:
        y,dy=(mp.mpf(0),mp.mpf(-1)) if bc=='D' else (mp.mpf(1),mp.mpf(0))
        z=sum(L for L,_ in blocks)
        for L,rho in reversed(blocks):
            t=max(-L,x-z)
            y,dy=step(y,dy,omega*mp.sqrt(rho),t)
            z-=L
            if x>=z: return y,dy
    return y,dy

def green(blocks,omega,x,y,bc):
    L=sum(t for t,_ in blocks)
    pl,pr=at(blocks,omega,L/2),at(blocks,omega,L/2,False,bc)
    W=pl[1]*pr[0]-pl[0]*pr[1]
    return at(blocks,omega,min(x,y))[0]*at(blocks,omega,max(x,y),False,bc)[0]/W

def count_physical_zeros(blocks,omega):
    y,dy,start=mp.mpf(0),mp.mpf(1),mp.mpf(0)
    Ltotal=sum(t for t,_ in blocks)
    zeros=[];tol=mp.mpf('1e-40')
    for L,rho in blocks:
        w=omega*mp.sqrt(rho)
        theta=mp.atan2(w*y,dy)
        for j in range(int(mp.floor(theta/mp.pi))-1,int(mp.ceil((theta+w*L)/mp.pi))+2):
            t=(j*mp.pi-theta)/w
            loc=start+t
            if -tol<=t<=L+tol and tol<loc<Ltotal-tol:
                if not any(abs(loc-z)<tol for z in zeros): zeros.append(loc)
        y,dy=step(y,dy,w,L);start+=L
    return sorted(zeros)

def reduced_green(blocks,lam,x,y,bc):
    # Laurent finite part in mu, not in its square root.
    L=sum(t for t,_ in blocks)
    def numerator(mu):
        om=mp.sqrt(mu)
        return at(blocks,om,min(x,y))[0]*at(blocks,om,max(x,y),False,bc)[0]
    def denominator(mu):
        om=mp.sqrt(mu)
        pl,pr=at(blocks,om,L/2),at(blocks,om,L/2,False,bc)
        return pl[1]*pr[0]-pl[0]*pr[1]
    n0=numerator(lam)
    n1=mp.diff(numerator,lam)
    w1=mp.diff(denominator,lam)
    w2=mp.diff(denominator,lam,2)
    return n1/w1-n0*w2/(2*w1*w1)

def main():
    x1,x2,wa,wb=mp.findroot(equations,(mp.mpf('.29343444668879'),mp.mpf('.36546070235558'),mp.sqrt(mp.mpf('22.50044205115')),mp.sqrt(mp.mpf('85.5936408854'))),tol=mp.mpf('1e-60'))
    edges=[x1,x2,1-x2,1-x1]
    la,lb=wa**2,wb**2
    dw=[]
    for w in (wa,wb):
        ds=mp.diff(lambda t:shoot(fb(edges),t)[0],w)
        dw.append([-mp.diff(lambda t:shoot(fb(replace(edges,j,t)),w)[0],edges[j])/ds for j in range(4)])
    Fw=[mp.diff(lambda t: residual(edges,t,wb),wa),mp.diff(lambda t:residual(edges,wa,t),wb)]
    J=mp.matrix(4)
    for j in range(4):
        col=mp.diff(lambda t:residual(replace(edges,j,t),wa,wb),edges[j])+Fw[0]*dw[0][j]+Fw[1]*dw[1][j]
        for i in range(4):J[i,j]=col[i]
    jumps=[mp.mpf(3),mp.mpf(-3),mp.mpf(3),mp.mpf(-3)]
    K=mp.diag([1/t for t in jumps])*J
    be=mp.matrix([[1,0],[0,1],[0,1],[1,0]])/mp.sqrt(2)
    bo=mp.matrix([[1,0],[0,1],[0,-1],[-1,0]])/mp.sqrt(2)
    Ke,Ko=be.T*K*be,bo.T*K*bo
    eps=mp.diag([1,-1,1,-1]); E=mp.diag([1,-1]);Kp=eps*K*eps
    a,b=shoot(fb(edges),wa),shoot(fb(edges),wb)
    u=[a[3][i][0]/mp.sqrt(a[2]) for i in range(2)]
    up=[a[3][i][1]/mp.sqrt(a[2]) for i in range(2)]
    v=[b[3][i][0]/mp.sqrt(b[2]) for i in range(2)]
    vp=[b[3][i][1]/mp.sqrt(b[2]) for i in range(2)]
    d=[(2*la*u[i]*up[i]-2*lb*v[i]*vp[i])/(lb*jumps[i]) for i in range(2)]
    hb=hblocks(x1,x2);xs=[x1,x2]
    GD=mp.matrix([[green(hb,wb,x,y,'D') for y in xs] for x in xs])
    GN=mp.matrix([[green(hb,wa,x,y,'N') for y in xs] for x in xs])
    candidate=mp.diag(d)+2*la*mp.diag(u)*(E*GD*E-la/lb*GN)*mp.diag(u)
    redGD=mp.matrix([[reduced_green(hb,la,x,y,'D') for y in xs] for x in xs])
    redGN=mp.matrix([[reduced_green(hb,lb,x,y,'N') for y in xs] for x in xs])
    ru=E*mp.matrix([t*t for t in u])
    corrected_odd=mp.diag(d)+4*la*(lb-la)/lb**2*(ru*ru.T)+2*la*mp.diag(u)*(redGN-la/lb*E*redGD*E)*mp.diag(u)

    mx=lambda A:max(abs(t) for t in A)
    mat=lambda M:[[mp.nstr(M[i,j],45) for j in range(M.cols)] for i in range(M.rows)]
    out=dict(physical_zeros_2=[mp.nstr(z,40) for z in count_physical_zeros(fb(edges),wa)],physical_zeros_3=[mp.nstr(z,40) for z in count_physical_zeros(fb(edges),wb)],dps=mp.mp.dps,edges=[mp.nstr(x,45) for x in edges],lambda2=mp.nstr(la,45),lambda3=mp.nstr(lb,45),residual=mp.nstr(mx(residual(edges,wa,wb)),10),K_symmetry_error=mp.nstr(mx(K-K.T),10),Ke=mat(Ke),Ko=mat(Ko),cross_Green_candidate=mat(candidate),corrected_Ko_discrepancy=mp.nstr(mx(corrected_odd-Ko),10),corrected_Ko=mat(corrected_odd),raw_Ko_discrepancy=mp.nstr(mx(candidate-Ko),45),conjugated_Ke_discrepancy=mp.nstr(mx(candidate-E*Ke*E),10),Kp_odd_discrepancy=mp.nstr(mx(candidate-bo.T*Kp*bo),10),GN=mat(GN),GD=mat(GD))
    print(json.dumps(out,indent=2));Path(__file__).resolve().joinpath('../evidence/green_sector.json').resolve().write_text(json.dumps(out,indent=2));return out
if __name__=='__main__': main()
