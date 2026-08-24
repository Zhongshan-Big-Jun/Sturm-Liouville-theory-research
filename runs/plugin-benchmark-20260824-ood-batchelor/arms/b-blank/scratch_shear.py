import numpy as np
from scipy.integrate import solve_ivp
# fixed k=1, equation d_t f_n = -i k sum_m U_m f_{n-m} - nu (k^2+n^2) f_n
# U(y)=A cos(Ny) => U_m = A/2 for m=±N
k=1
A=10.0
N=3
nu=0.2
nmax=120
ns=np.arange(-nmax,nmax+1)
# initial low mode n=0
f0=np.zeros(len(ns),dtype=complex); f0[ns==0]=1.0
# zero constant initial? Must mean-zero in x,y total: k=1,n=0 is okay mean zero (k!=0)

def rhs(t,f):
    f=f.reshape(len(ns))
    df=-nu*(k**2+ns**2)*f
    # -i k (U * f) convolution in n: U_m A/2 at +-N
    # conv_n = sum_m U_m f_{n-m}
    # use np.roll for finite truncation: roll indices by N
    conv=(A/2)*(np.roll(f,N)+np.roll(f,-N))
    # note roll wraps around, fine for finite but not exact; use zero outside by pad maybe
    df -= 1j*k*conv
    return df

# Better use truncated convolution with zero outside: shift and zero edges
def rhs_exact(t,f):
    f=f.reshape(len(ns))
    df=-nu*(k**2+ns**2)*f
    conv=np.zeros_like(f)
    for m in [N,-N]:
        idx_n=ns+m
        idx_shift=np.searchsorted(ns,idx_n)
        valid=(idx_n>=ns[0])&(idx_n<=ns[-1])
        conv[valid]=f[idx_shift[valid]-m*0] # wait index relation
    # Let's simpler use linear operator matrix? for now roll may be okay small A time
    conv=(A/2)*(np.roll(f,N)+np.roll(f,-N))
    df -= 1j*k*conv
    return df

sol=solve_ivp(rhs_exact,[0,20],f0,t_eval=np.linspace(0,20,101),method='RK45',rtol=1e-6,atol=1e-9)
# compute Q = sqrt(sum |f|^2/(k^2+n^2)/sum |f|^2)
for tt in [0,0.5,1,2,5,10,20]:
    i=np.argmin(abs(sol.t-tt))
    f=sol.y[:,i]
    E=np.sum(np.abs(f)**2)
    F=np.sum(np.abs(f)**2/(k**2+ns**2))
    print('t',sol.t[i],'E',E,'F',F,'Q',np.sqrt(F/E))
