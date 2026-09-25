"""Semantic reproduction of roots_of/D_scalar from the reviewed repository.
Source: scripts/_gapn2_symmetry_recon.py
Commit: 5bb6b2605122d2daf472863b4bec0f35a9c192e1
This is not a byte-identical source copy or an independently corrected solver.
It intentionally preserves the sign-scan defect being audited.
"""
import numpy as np

def D_scalar(blocks,s):
    M00=1.; M01=0.; M10=0.; M11=1.
    for L,c in blocks:
        w=s*np.sqrt(c); wL=w*L
        cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
        M00,M01,M10,M11=cw*M00+sw*M10,cw*M01+sw*M11,sw2*M00+cw*M10,sw2*M01+cw*M11
    return M01

def roots_of(blocks,k,npts=20000,refine=60):
    smax=np.pi*np.sqrt(max(c for _,c in blocks))*(k+2)+20.
    s=np.linspace(1e-9,smax,npts)
    npts=max(npts,int(np.ceil(smax/.02)))
    s=np.linspace(1e-9,smax,npts)
    M00=np.ones(npts); M01=np.zeros(npts); M10=np.zeros(npts); M11=np.ones(npts)
    for L,c in blocks:
        w=s*np.sqrt(c); wL=w*L
        cw=np.cos(wL); sw=np.sin(wL)/w; sw2=-w*np.sin(wL)
        M00,M01,M10,M11=cw*M00+sw*M10,cw*M01+sw*M11,sw2*M00+cw*M10,sw2*M01+cw*M11
    idx=np.nonzero(np.signbit(M01[1:])!=np.signbit(M01[:-1]))[0]
    out=[]
    for i in idx[:k]:
        lo,hi=s[i],s[i+1]
        for _ in range(refine):
            mid=(lo+hi)/2
            if D_scalar(blocks,lo)*D_scalar(blocks,mid)<=0:hi=mid
            else:lo=mid
        out.append((lo+hi)/2)
    return np.array(out)

if __name__ == "__main__":
    blocks = [(.02, 10000.), (.96, 1.), (.02, 10000.)]
    for count in (2, 3, 61):
        roots = roots_of(blocks, count)
        print("requested", count, "first returned", roots[:min(count, 5)])
