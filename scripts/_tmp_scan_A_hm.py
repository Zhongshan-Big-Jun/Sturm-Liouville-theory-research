import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_sector_decomposition import sector_data
from _gapn2_green_inertia_probe import reduced_resolvent
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n in [2,3,4]:
 print('\nSUP n',n)
 prev=None
 for R in ([1.2,2,4,10,30,100] if n==2 else [1.2,2,4,10,30] if n==3 else [1.2,2,4,10]):
  try:
   rc=Recon(n,R,'sup'); key=f'n{n}_SUP'; e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc, z0 if prev is None else prev)
   if zs is None: print('R',R,'none'); continue
   prev=zs; ed=eigen_data(rc,zs); blocks=rc.blocks_from_z(zs); x=ed['edges'][:n]; u=ed['u_n'][:n]; eps=ed['eps'][:n]; E=np.diag(eps); lam_n=ed['lam_n']; lam_np1=ed['lam_np1']; fac=4*lam_n/lam_np1
   if n%2==0: Rlo=reduced_resolvent(blocks,lam_n,x,'even'); Rhi=reduced_resolvent(blocks,lam_np1,x,'odd')
   else: Rlo=reduced_resolvent(blocks,lam_n,x,'odd'); Rhi=reduced_resolvent(blocks,lam_np1,x,'even')
   M=lam_np1*(E@Rhi@E)-lam_n*Rlo; sd=sector_data(rc,zs,N=200); d=np.array(sd['d']); A=np.diag(d/u**2)+fac*M; D=np.diag(np.diag(A)); off=A-D; rho=np.max(np.abs(np.linalg.eigvals(np.linalg.solve(D,off))))
   print('R',R,'rhoA',round(rho,4),'minA',np.min(np.linalg.eigvalsh(A)))
  except Exception as e: print('R',R,'fail',e); prev=None
