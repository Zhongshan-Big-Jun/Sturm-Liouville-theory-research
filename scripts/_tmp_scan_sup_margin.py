import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_sector_decomposition import sector_data
from _gapn2_green_inertia_probe import reduced_resolvent
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n in [2,3,4]:
    print('\n=== SUP n',n,'===')
    prev=None
    for R in ([1.05,1.2,2,4,10,30,100] if n==2 else [1.2,2,4,10,30] if n==3 else [1.2,2,4,10]):
        try:
            rc=Recon(n,R,'sup'); key=f'n{n}_SUP'; e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0)
            zs=symmetric_root(rc, z0 if prev is None else prev)
            if zs is None: print('R',R,'no root'); prev=None; continue
            prev=zs
            blocks=rc.blocks_from_z(zs); ed=eigen_data(rc,zs); lam_n=ed['lam_n']; lam_np1=ed['lam_np1']; x=ed['edges'][:n]; u=ed['u_n'][:n]; eps=ed['eps'][:n]; E=np.diag(eps)
            if n%2==0: Rlo=reduced_resolvent(blocks,lam_n,x,'even'); Rhi=reduced_resolvent(blocks,lam_np1,x,'odd')
            else: Rlo=reduced_resolvent(blocks,lam_n,x,'odd'); Rhi=reduced_resolvent(blocks,lam_np1,x,'even')
            M=lam_np1*(E@Rhi@E)-lam_n*Rlo
            sd=sector_data(rc,zs,N=400); d=np.array(sd['d']); fac=4*lam_n/lam_np1
            mev=np.linalg.eigvalsh(M); mneg=max(0,-mev.min()); dmin=np.min(d/u**2); margin=dmin-fac*mneg
            A=np.diag(d/u**2)+fac*M; amin=np.linalg.eigvalsh(A)[0]
            print('R=%-7g dmin=%.5f fac*mneg=%.5f margin=%.5f A_min=%.5f'%(R,dmin,fac*mneg,margin,amin))
        except Exception as e:
            print('R',R,'FAIL',type(e).__name__,e); prev=None
