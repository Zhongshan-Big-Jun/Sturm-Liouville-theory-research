"""Bounded real backend check against per-block numerical IVP + quadrature."""
import importlib
import inspect
import json
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import solve_ivp, quad

Base = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Base/'originals'/'scripts'))
Blocks = [(0.3,1.0),(0.4,4.0),(0.3,1.0)]
Points = np.array([0.15,0.3,0.5,0.7,0.85,1.0])

def ivp_reference(Blocks, Lam, Points):
	Starts = np.r_[0.0, np.cumsum([L for L,_ in Blocks])]
	State = np.array([0.0,1.0])
	Solutions = []
	Norm = 0.0
	for I,(L,Rho) in enumerate(Blocks):
		Sol = solve_ivp(lambda X,Y: [Y[1],-Lam*Rho*Y[0]],(Starts[I],Starts[I+1]),State,method='DOP853',rtol=2e-12,atol=2e-14,dense_output=True)
		if not Sol.success: raise RuntimeError(Sol.message)
		Solutions.append(Sol.sol)
		Norm += Rho * quad(lambda X: float(Sol.sol(X)[0])**2,Starts[I],Starts[I+1],epsabs=1e-13,epsrel=1e-12)[0]
		State = Sol.y[:,-1]
	Values = np.array([Solutions[min(len(Blocks)-1,max(0,int(np.searchsorted(Starts,X,side='right')-1))) ](X)[0] for X in Points])
	return Values/np.sqrt(Norm), State[0]/np.sqrt(Norm)

def main():
	Rows = []
	for Name in ('op03_gap_precise','op03_gap_fixed'):
		Module = importlib.import_module(Name)
		Roots = Module.lams_precise(Blocks,2)
		U = Module.eigfuns_precise(Blocks,Roots,Points)
		Mass = []
		for Root in Roots:
			Xs = np.r_[0.0,np.cumsum([L for L,_ in Blocks])]
			Mass.append(sum(Rho*quad(lambda X: Module.eigfuns_precise(Blocks,np.array([Root]),np.array([X]))[0,0]**2,Xs[I],Xs[I+1],epsabs=1e-10)[0] for I,(_,Rho) in enumerate(Blocks)))
		Ref = [ivp_reference(Blocks,S*S,Points) for S in Roots]
		Error = float(np.max(np.abs(U-np.array([R[0] for R in Ref]))))
		Row = dict(backend=Name,lams_signature=str(inspect.signature(Module.lams_precise)),eigfuns_signature=str(inspect.signature(Module.eigfuns_precise)),lambda_values=(Roots**2).tolist(),weighted_mass=Mass,values=U.tolist(),ivp_values=[R[0].tolist() for R in Ref],normalized_dirichlet_endpoint=U[:,-1].tolist(),ivp_endpoint=[float(R[1]) for R in Ref],max_value_error=Error)
		Rows.append(Row)
	print(json.dumps(dict(blocks=Blocks,points=Points.tolist(),backends=Rows),indent=2))
	return int(any(R['max_value_error']>1e-7 or max(abs(M-1) for M in R['weighted_mass'])>1e-7 for R in Rows))

if __name__=='__main__':
	sys.exit(main())
