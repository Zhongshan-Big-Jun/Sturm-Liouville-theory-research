import numpy as np
from scipy.linalg import eig

def make_matrix(k,A,N,nu,nmax):
    ns=np.arange(-nmax,nmax+1)
    n=len(ns)
    M=np.zeros((n,n),dtype=complex)
    for i,n in enumerate(ns):
        M[i,i]=-nu*(k*k+n*n)
        # U_y multiplication in Fourier: (U*f)_n = A/2 (f_{n-N}+f_{n+N})
        for m in [N,-N]:
            j=np.where(ns==n-m)[0]
            if len(j):
                # convolution (U*f)_n = sum_m U_m f_{n-m}; U_m=A/2 for m=±N
                M[i,j[0]] += -1j*k*(A/2)
    return M, ns

for A in [1,3,10,30]:
    M,ns=make_matrix(1,A,3,0.2,80)
    w,v=np.linalg.eig(M)
    idx=np.argsort(-w.real)
    print('A',A)
    for q in range(3):
        e=w[idx[q]]
        f=v[:,idx[q]]
        # normalize
        f=f/np.linalg.norm(f)
        E=1
        F=np.sum(np.abs(f)**2/(1+ns**2))
        nmean=np.sum(np.abs(f)**2*ns**2)
        print('  eig real',e.real,'imag',e.imag,'Q',np.sqrt(F/E),'n2mean',nmean,'top n',ns[np.argmax(np.abs(f))], 'f norm',np.linalg.norm(f))
