import sys, json, numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
tab=json.load(open(r'scripts/op03_gap_table.json',encoding='utf-8'))
for n,R,mode in [(2,4,'sup'),(2,4,'inf'),(3,4,'sup'),(3,4,'inf')]:
    rc=Recon(n,R,mode); key=f'n{n}_{mode.upper()}'; edges=np.array(tab[key]['edges']); w=np.diff(np.concatenate([[0],edges,[1]])); z0=rc.widths_to_z(w); zs=symmetric_root(rc,z0); J=jac_fd(rc,zs)
    print('\n===',n,mode,'=== J')
    print(np.round(J,4))
    print('diag',np.round(np.diag(J),4))
    print('row dominance min', min(np.abs(J[i,i])-np.sum(np.abs(J[i,:]))+np.abs(J[i,i]) for i in range(2*n)))
