import sys, json, numpy as np
sys.path.insert(0,'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_green_inertia_probe import reduced_resolvent
for n,mode in [(2,'sup'),(2,'inf'),(3,'sup')]:
 rc=Recon(n,4,mode)
 tab=json.load(open('scripts/op03_gap_table.json'))
 key='n%d_%s'%(n,mode.upper()); e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc,z0)
 blocks=rc.blocks_from_z(zs); ed=eigen_data(rc,zs)
 lam_n,lam_np1=ed['lam_n'],ed['lam_np1']; x=ed['edges'][:n]; u=ed['u_n'][:n]; eps=ed['eps'][:n]
 if n%2==0: Rlo=reduced_resolvent(blocks,lam_n,x,'even'); Rhi=reduced_resolvent(blocks,lam_np1,x,'odd')
 else: Rlo=reduced_resolvent(blocks,lam_n,x,'odd'); Rhi=reduced_resolvent(blocks,lam_np1,x,'even')
 E=np.diag(eps); M=lam_np1*(E@Rhi@E)-lam_n*Rlo
 p=4*lam_n/lam_np1
 A=np.diag((4*lam_n/lam_np1)*np.ones(n)? )
