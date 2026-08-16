import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n in [2,3,4]:
 print('\nSUP n',n)
 prev=None
 for R in ([1.2,2,4,10,30,100] if n==2 else [1.2,2,4,10] if n==3 else [1.2,2,4,10]):
  try:
   rc=Recon(n,R,'sup'); key=f'n{n}_SUP'; e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc, z0 if prev is None else prev)
   if zs is None: print('R',R,'none'); continue
   prev=zs; J=jac_fd(rc,zs); D=np.diag(np.diag(J)); off=J-D; rho=np.max(np.abs(np.linalg.eigvals(np.linalg.solve(D,off)))); print('R',R,'rho',rho,'det',np.linalg.det(J),'sgn',np.sign(np.linalg.det(J)))
  except Exception as e: print('R',R,'fail',e); prev=None
