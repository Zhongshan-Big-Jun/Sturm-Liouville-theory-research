import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_sector_decomposition import sector_data
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n,mode in [(2,'sup'),(3,'sup'),(4,'sup'),(2,'inf'),(3,'inf')]:
 print('\n===',n,mode,'===')
 prev=None
 Rs=[1.05,1.2,2,4,10,30,100] if n==2 else [1.2,2,4,10,30] if n==3 else [1.2,2,4,10]
 for R in Rs:
  try:
   rc=Recon(n,R,mode); key=f'n{n}_{mode.upper()}'; e0=np.array(tab[key]['edges']); w0=np.diff(np.concatenate([[0],e0,[1]])); z0=rc.widths_to_z(w0); zs=symmetric_root(rc, z0 if prev is None else prev)
   if zs is None: print(' R',R,'none'); continue
   prev=zs; sd=sector_data(rc,zs,N=200)
   vals=[]
   for nm in ['Ko','Ke']:
    A=np.array(sd[nm]); D=np.diag(np.diag(A)); off=A-D
    rho=np.max(np.abs(np.linalg.eigvals(np.linalg.solve(D,off)))) if np.all(np.diag(D)!=0) else np.inf
    vals.append(rho)
   print(' R',R,'rhoKo',round(vals[0],4),'rhoKe',round(vals[1],4),'min diagKo',round(np.min(np.abs(np.diag(np.array(sd['Ko'])))),4),'min diagKe',round(np.min(np.abs(np.diag(np.array(sd['Ke'])))),4))
  except Exception as e: print(' R',R,'FAIL',type(e).__name__,str(e)[:80]); prev=None
