import json
import sys
import warnings
from pathlib import Path
import numpy as np
import reference as Ref
sys.path.insert(0,'/mnt/f/LaTeX/BVE research/scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_analytic import eigen_data,green_kernel
from _gapn2_jacobian_spectral import analytic_jacobian_spectral
from _gapn2_half_problem_probe import green_regular

Results = {}
for N,R,Points in [(2,1,[.1,.5,.6,.8]),(1,4,[.55,.6746455700142735])]:
	Rc=Recon(N,R,'sup')
	Z=Rc.widths_to_z(np.diff([0,*Points,1]))
	Data=eigen_data(Rc,Z)
	Blocks=Ref.blocks_from_edges(Data['edges'],Rc.pat)
	Lambdas=Ref.roots(Blocks,N+1)
	Truth=np.array(Ref.normalized(Lambdas[N-1 if R==1 else N],Blocks,Data['edges']),float)
	Suffix='n' if R==1 else 'np1'
	Actual=np.column_stack([Data['u_'+Suffix],Data['up_'+Suffix]])
	Results['R'+str(R)]=dict(edges=Data['edges'].tolist(),expected=Truth.tolist(),actual=Actual.tolist(),max_error=float(np.max(abs(Actual-Truth))))
Results['reversed_green']=(green_kernel([(1,1)],1,[.75,.25])-np.array([[float(Ref.green(1,[(Ref.mp.mpf(1),Ref.mp.mpf(1))],X,Y)) for Y in [.75,.25]] for X in [.75,.25]])).tolist()
try:
	green_kernel([(1,1)],1,[0,.2,1])
except Exception as Error:
	Results['legal_endpoint_error']=repr(Error)
with warnings.catch_warnings(record=True) as Seen:
	warnings.simplefilter('always')
	for Mu in [0,-1]:
		for Boundary in ['D','N']:
			Results[f'half_{Mu}_{Boundary}']=repr(green_regular([(.5,1)],Mu,.1,.2,Boundary))
	Results['warnings']=[str(Row.message) for Row in Seen]
Rc=Recon(1,4,'sup'); Z=Rc.widths_to_z([.25,.5,.25])
Lambdas,F,J=Ref.implicit_jacobian([.25,.75],Rc.pat,1)
Truth=np.array(J.tolist(),float)
Results['nonstationary']=dict(expected=Truth.tolist(),actual=analytic_jacobian_spectral(Rc,Z,N=160).tolist())
print(json.dumps(Results,indent=2))
