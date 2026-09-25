"""Author finite diagnostics for actual repaired modules; not independent review."""
from pathlib import Path
import ast, hashlib, json, sys
import numpy as np

R=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/mnt/f/LaTeX/BVE research')
O=Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).resolve().parent
O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'scripts'))
from _gapn2_jacobian_probe import jac_fd,jacobian_cross_blocks,sym_antisym_decomp,symmetric_root
from _gapn2_symmetry_recon import Recon
Records=[]
def require(Condition,Name,**Detail):
	if not bool(Condition): raise RuntimeError('FAILED: '+Name)
	Records.append(dict(name=Name,passed=True,details=Detail))
def rejects(Action,Name):
	try: Action()
	except (ValueError,ArithmeticError) as E: require(True,Name,error=str(E)); return
	raise RuntimeError('FAILED TO REJECT: '+Name)
class AnalyticRecon(Recon):
	def residual(self,Z):
		X=np.cumsum(self.z_to_widths(Z))[:-1];N=self.n
		return 2*((N/(N+1))**2*np.sin(N*np.pi*X)**2-np.sin((N+1)*np.pi*X)**2)
Rc=AnalyticRecon(2,1.,'sup')
X=np.array([.25,.2500003,.7499997,.75]);Z=Rc.widths_to_z(np.diff(np.r_[0.,X,1.]))
J,E=jac_fd(Rc,Z,return_diagnostics=True)
# Derivative of 2*(n/(n+1))^2*sin(n*pi*x)^2 is 2*n^3*pi/(n+1)^2*sin(2*n*pi*x).
def exact_jac(X,N):
	return np.diag(2*np.pi*N**3/(N+1)**2*np.sin(2*N*np.pi*X)-2*np.pi*(N+1)*np.sin(2*(N+1)*np.pi*X))
require(np.max(np.abs(J-exact_jac(X,2)))<1e-5,'reported narrow R1 example repaired',max_error=float(np.max(np.abs(J-exact_jac(X,2)))),geometry=E)
OldPath=Path(sys.argv[3]) if len(sys.argv)>3 else R/'research/artifacts/proof-audit-round11-20260926/before/scripts/_gapn2_jacobian_probe.py'
Tree=ast.parse(OldPath.read_text()); Namespace={'np':np}
exec(compile(ast.Module(body=[N for N in Tree.body if isinstance(N,ast.FunctionDef) and N.name in {'jac_fd','sym_antisym_decomp'}],type_ignores=[]),str(OldPath),'exec'),Namespace)
Old=Namespace['jac_fd'](Rc,Z)
require(np.max(np.abs(Old-exact_jac(X,2)))>6.,'exact old function reproduces clipping failure',max_error=float(np.max(np.abs(Old-exact_jac(X,2)))))
for H in [1e-6,1e-7,1e-8]:
	Matrix,Geometry=jac_fd(Rc,Z,H,return_diagnostics=True)
	require(np.max(np.abs(Matrix-exact_jac(X,2)))<1e-5,f'narrow requested step {H:g}',error=float(np.max(np.abs(Matrix-exact_jac(X,2)))))
	for K,Column in enumerate(Geometry['columns']):
		Expected=np.zeros(4);Expected[K]=Column['used_step']
		Plus=np.array(Column['plus_edges']);Minus=np.array(Column['minus_edges']);Base=np.array(Geometry['base_edges'])
		require(max(np.max(np.abs(Plus-Base-Expected)),np.max(np.abs(Minus-Base+Expected)))<=Column['geometry_error_budget'],f'actual endpoint direction {H:g}/{K}')
		require(min(np.diff(np.r_[0.,Plus,1.]).min(),np.diff(np.r_[0.,Minus,1.]).min())>2e-7,f'no endpoint clipping {H:g}/{K}')
for N in [1,2,3,5]:
	Local=AnalyticRecon(N,1.,'sup'); Edges=np.linspace(.1,.9,2*N); Seed=Local.widths_to_z(np.diff(np.r_[0.,Edges,1.]))
	Matrix=jac_fd(Local,Seed)
	require(np.max(np.abs(Matrix-exact_jac(Edges,N)))<3e-6,f'analytic R1 n={N}',max_error=float(np.max(np.abs(Matrix-exact_jac(Edges,N)))))
	Actual=Recon(N,1.,'sup');ActualMatrix=jac_fd(Actual,Seed)
	require(np.max(np.abs(ActualMatrix-exact_jac(Edges,N)))<3e-5,f'actual full Recon R1 n={N}',max_error=float(np.max(np.abs(ActualMatrix-exact_jac(Edges,N)))))
	Left=np.arange(1,N+1,dtype=float)+.25;Diagonal=np.r_[Left,-Left[::-1]];Reference=np.diag(Diagonal)
	C,D,Geometry=jacobian_cross_blocks(Reference,N,return_diagnostics=True)
	require(np.array_equal(C,np.diag(Left)) and np.array_equal(D,np.diag(Left)),f'physical opposite-pair cross blocks n={N}')
	Signed=(-1)**N*np.linalg.det(C)*np.linalg.det(D)
	require(np.isclose(Signed,np.linalg.det(Reference),rtol=1e-12),f'odd-even determinant sign n={N}',signed_product=float(Signed),det_j=float(np.linalg.det(Reference)))
	rejects(lambda:jacobian_cross_blocks(np.eye(2*N),N),f'commuting identity/Hessian is not an anti Jacobian n={N}')
Tp=(11+2*np.sqrt(10))/36; Tm=(11-2*np.sqrt(10))/36
Left=np.arccos(np.sqrt([Tp,Tm]))/np.pi; Star=np.r_[Left,1-Left[::-1]]; Js=exact_jac(Star,2)
C,D=jacobian_cross_blocks(Js,2)
Expected=7030400000*np.pi**4/4782969
require(abs(np.linalg.det(Js)/Expected-1)<1e-12,'actual SL radical determinant',det=float(np.linalg.det(Js)),expected=float(Expected))
require(np.array_equal(C,sym_antisym_decomp(Js,2)[0]) and np.array_equal(D,sym_antisym_decomp(Js,2)[1]),'legacy import name returns corrected cross blocks')
OldA,OldB=Namespace['sym_antisym_decomp'](Js,2)
require(max(np.max(np.abs(OldA)),np.max(np.abs(OldB)))<1e-12,'old diagonal extraction is numerical zero on nondegenerate SL witness')
class LinearRecon(Recon):
	def residual(self,Z): return np.array([[1.,2.,3.,4.],[-2.,0.,1.,2.],[3.,4.,0.,-2.],[9.,7.,6.,5.]])@np.cumsum(self.z_to_widths(Z))[:-1]
Linear=LinearRecon(2,1,'sup');Seed=Linear.widths_to_z(np.array([.1,.2,.3,.25,.15]))
ExpectedLinear=np.array([[1.,2.,3.,4.],[-2.,0.,1.,2.],[3.,4.,0.,-2.],[9.,7.,6.,5.]])
require(np.max(np.abs(jac_fd(Linear,Seed)-ExpectedLinear))<1e-7,'coupled linear residual has correct full edge Jacobian')
for H in [0,-1,float('nan'),float('inf'),True,1e-30]: rejects(lambda H=H:jac_fd(Rc,Z,H),'reject invalid/unresolvable step '+str(H))
rejects(lambda:jac_fd(Rc,np.zeros(4)),'reject wrong parameter dimension')
rejects(lambda:jac_fd(Rc,np.r_[np.nan,np.zeros(4)]),'reject nonfinite parameters')
class MalformedResidual(AnalyticRecon):
	def residual(self,Z): return np.full(4,np.nan)
rejects(lambda:jac_fd(MalformedResidual(2,1,'sup'),Z),'reject nonfinite residual')
class ChangedConverter(AnalyticRecon):
	def widths_to_z(self,W):
		W=W.copy();W[0]+=1e-4;W[-1]-=1e-4
		return super().widths_to_z(W)
rejects(lambda:jac_fd(ChangedConverter(2,1,'sup'),Z),'reject converter changing the base')
Tiny=np.array([.2,1.5e-7,.3,.2,.3-1.5e-7]);TinyZ=np.log(Tiny-1e-7)
rejects(lambda:jac_fd(Rc,TinyZ),'reject feasible softmax base clipped by inverse callback')
Barely=np.array([.2,2e-7,.3,.2,.3-2e-7]);BarelyZ=Rc.widths_to_z(Barely)
rejects(lambda:jac_fd(Rc,BarelyZ),'reject no resolvable symmetric pair at inverse clipping threshold')
for Matrix,N in [(np.zeros((2,3)),1),(np.eye(4),0),(np.eye(4),True),(np.full((4,4),np.nan),2),(np.eye(4)*1j,2)]:
	rejects(lambda Matrix=Matrix,N=N:jacobian_cross_blocks(Matrix,N),'reject invalid block input '+str((Matrix.shape,N,Matrix.dtype)))
Table=json.loads((R/'scripts/op03_gap_table.json').read_text())
for N,Mode in [(1,'sup'),(2,'sup'),(2,'inf'),(3,'sup')]:
	Local=Recon(N,4.,Mode); Edges=np.array(Table[f'n{N}_{Mode.upper()}']['edges']);Seed=Local.widths_to_z(np.diff(np.r_[0.,Edges,1.]))
	Root=symmetric_root(Local,Seed)
	require(Root is not None,f'actual R4 symmetric root n={N}/{Mode}')
	Matrix,Geometry=jac_fd(Local,Root,return_diagnostics=True)
	Half=jac_fd(Local,Root,h=5e-7);Old=Namespace['jac_fd'](Local,Root)
	C,D,Block=jacobian_cross_blocks(Matrix,N,return_diagnostics=True)
	require(np.max(np.abs(Matrix-Half))<5e-5,f'two feasible steps R4 n={N}/{Mode}',absolute_difference=float(np.max(np.abs(Matrix-Half))),geometry=Geometry)
	require(np.max(np.abs(Matrix-Old))<5e-5,f'well-separated old-new R4 comparison n={N}/{Mode}',absolute_difference=float(np.max(np.abs(Matrix-Old))))
	require(np.isclose(np.linalg.det(Matrix),(-1)**N*np.linalg.det(C)*np.linalg.det(D),rtol=1e-6,atol=1e-6),f'cross blocks of actual R4 n={N}/{Mode}',diagnostics=Block)
Sources=['_gapn2_jacobian_probe.py','_gapn2_symmetry_recon.py','_sl_prufer.py','reflection_seeds.py','_gapn2_second_variation_probe.py','_gapn2_o3_scan.py','op03_gap_table.json']
Out=O/('checks-optimized.json' if not __debug__ else 'checks-normal.json')
Out.write_text(json.dumps(dict(status='PASS',scope='author finite checks, no interval certification or independent verdict',optimized=not __debug__,count=len(Records),checks=Records,source_sha256={N:hashlib.sha256((R/'scripts'/N).read_bytes()).hexdigest() for N in Sources}),indent=2)+'\n')
print(json.dumps(dict(status='PASS',count=len(Records),output=str(Out)),indent=2),flush=True)
