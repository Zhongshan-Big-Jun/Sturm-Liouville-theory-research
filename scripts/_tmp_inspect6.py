import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_sector_decomposition import sector_data
from _gapn2_green_inertia_probe import reduced_resolvent
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n,R,mode in [(2,4,'sup'),(3,4,'sup'),(2,4,'inf'),(3,4,'inf')]:
 rc=Recon(n,R,mode); key=f'n{n}_{mode.upper()}'; e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc,z0); blocks=rc.blocks_from_z(zs); ed=eigen_data(rc,zs); lam_n=ed['lam_n']; lam_np1=ed['lam_np1']; x=ed['edges'][:n]; u=ed['u_n'][:n]; eps=ed['eps'][:n]; E=np.diag(eps)
 if n%2==0: Rlo=reduced_resolvent(blocks,lam_n,x,'even'); Rhi=reduced_resolvent(blocks,lam_np1,x,'odd')
 else: Rlo=reduced_resolvent(blocks,lam_n,x,'odd'); Rhi=reduced_resolvent(blocks,lam_np1,x,'even')
 M=lam_np1*(E@Rhi@E)-lam_n*Rlo; sd=sector_data(rc,zs,N=200); d=np.array(sd['d']); fac=4*lam_n/lam_np1
 A=np.diag(d/u**2)+fac*M
 print('\n===',n,mode,'=== A')
 print(np.round(A,5))
 print('diag',np.round(np.diag(A),5))
 print('A eig',np.round(np.linalg.eigvalsh(A),5))
