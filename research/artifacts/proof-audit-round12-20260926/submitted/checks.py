"""Round 12 independent checks. A successful check can confirm a BUG.

No assert statements are used; python -O must not disable a check.
Infinite-dimensional theorems are reviewed analytically, not certified here.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,sys,json,math,platform,warnings,contextlib,io
import numpy as np
import sympy as sp
import mpmath as mp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source_excerpts'))
from half_spectrum_excerpt import half_spectrum,_spectral_green,_secular_all
from jacobian_excerpt import jac_fd,jacobian_cross_blocks
import primitive_check as primitives
import green_sector_check as gcheck
RESULTS=[]
def check(name,condition,kind,details=None):
    if not bool(condition):raise RuntimeError('CHECK FAILED: '+name)
    row={'name':name,'confirmed':True,'kind':kind,'details':details}
    RESULTS.append(row);print(name,'CONFIRMED',flush=True)

def atan_bounds(x,n=32):
    s=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(n)),F(0))
    sn=s+(-1)**n*x**(2*n+1)/F(2*n+1)
    return min(s,sn),max(s,sn)
a,b=atan_bounds(F(1,5));c,d=atan_bounds(F(1,239))
piL,piU=16*a-4*d,16*b-4*c
check('pi_rational_enclosure',F(314159,100000)<piL<piU<F(314160,100000),'exact rational')

class AnalyticRC:
    n=2
    def z_to_widths(self,z):
        z=np.asarray(z,dtype=float);t=np.exp(z-np.max(z));return (1-5e-7)*t/np.sum(t)+1e-7
    def widths_to_z(self,widths):
        w=np.asarray(widths,dtype=float);w=np.clip(w,2e-7,1-2e-7);w=w/np.sum(w);return np.log(w-1e-7)
    def residual(self,z):
        x=np.cumsum(self.z_to_widths(z))[:-1]
        return 2*((4/9)*np.sin(2*np.pi*x)**2-np.sin(3*np.pi*x)**2)
rc=AnalyticRC()
tp=(11+2*np.sqrt(10))/36;tm=(11-2*np.sqrt(10))/36
x=np.array([np.arccos(np.sqrt(tp))/np.pi,np.arccos(np.sqrt(tm))/np.pi])
x=np.r_[x,1-x[::-1]]
di=(16*np.pi/9)*np.sin(4*np.pi*x)-6*np.pi*np.sin(6*np.pi*x)
# Exact reflection of the first two entries avoids attributing trig roundoff to the algebra.
J0=np.diag([di[0],di[1],-di[1],-di[0]])
C,D,e=jacobian_cross_blocks(J0,2,return_diagnostics=True)
check('repaired_cross_blocks_nonzero',abs(np.linalg.det(C))>1 and abs(np.linalg.det(D))>1,'source function numeric')
check('repaired_cross_determinant',abs(np.linalg.det(J0)-np.linalg.det(C)*np.linalg.det(D))<1e-8,'source function numeric')
expected=7030400000*np.pi**4/4782969
check('constant_R1_Jacobian_determinant',abs(np.linalg.det(J0)-expected)<1e-7,'finite closed-form numeric')
try:jacobian_cross_blocks(np.eye(4),2)
except ValueError: rejected=True
else: rejected=False
check('commuting_Hessian_not_accepted_as_J',rejected,'expected rejection')
widths=np.array([.25,3e-7,.4999994,3e-7,.25]);z=rc.widths_to_z(widths)
Jn,ev=jac_fd(rc,z,return_diagnostics=True);xx=np.cumsum(rc.z_to_widths(z))[:-1]
truth=np.diag((16*np.pi/9)*np.sin(4*np.pi*xx)-6*np.pi*np.sin(6*np.pi*xx))
err=float(abs(Jn-truth).max())
check('repaired_narrow_J_accuracy',err<1e-6,'source function numeric',{'max_error':err})
check('repaired_narrow_J_actual_endpoint_check',all(r['max_motion_error']<=r['geometry_error_budget'] and r['minimum_endpoint_width']>0 for r in ev['columns']),'source function numeric',ev)

# Symbolic checks accompanying, but not proving, the newly integrated closure theorem.
L=sp.symbols('L',integer=True,positive=True)
Me=sp.Matrix([[L,L+2],[L*(L-1)*(L-2),L*(L+1)*(L+2)]])
Mo=sp.Matrix([[L,L+2],[L*(L+1)*(L-2),L*(L+2)*(L+3)]])
check('cofinite_even_right_inverse_determinant',sp.expand(Me.det()-2*L*(L+2)*(2*L-1))==0,'symbolic identity')
check('cofinite_odd_right_inverse_determinant',sp.expand(Mo.det()-2*L*(L+2)*(2*L+1))==0,'symbolic identity')
xv=sp.symbols('x')
low=[sp.Integer(1),xv,xv**4-2*xv**2,xv**5-2*xv**3]
check('cofinite_low_trace_matrix',sp.Matrix([[sp.diff(q,xv,r).subs(xv,0) for q in low] for r in range(4)])==sp.diag(1,1,-4,-12),'symbolic identity')
w,t,bv,zv=sp.symbols('w t b z',real=True)
quad=(zv-bv)**2+t*t*w*bv*bv
bmin=zv/(1+t*t*w)
check('cofinite_K_functional_coordinate_minimum',sp.factor(quad.subs(bv,bmin)-t*t*w*zv*zv/(1+t*t*w))==0,'symbolic identity; not interpolation theorem')

# The nine claimed trigonometric primitives remain correct.
for key,expr in primitives.o.items():
    u,v=key.split(',')
    dd=sp.trigsimp(sp.expand_trig(sp.diff(expr,primitives.l)-primitives.f[u]*primitives.g[v]))
    check('Green_primitive_'+key,dd==0 and sp.simplify(expr.subs(primitives.l,0))==0,'symbolic antiderivative')

# Run the independent half-spectrum enumerator retained in the repository.
hb=[(.5,100.)]
cases={}
for bc,N in [('D',4),('D',80),('D',160),('N',4),('N',80),('N',160)]:
    cases[bc,N]=half_spectrum(hb,bc,N)
D4,D80,D160=cases['D',4],cases['D',80],cases['D',160]
N4,N80,N160=cases['N',4],cases['N',80],cases['N',160]
check('half_D_small_N_matches_exact',np.allclose(D4,np.arange(1,5)**2*np.pi**2/25,rtol=1e-13,atol=0),'source function numeric')
check('half_D_N80_loses_first_two',abs(D80[0]-9*np.pi**2/25)<1e-13,'confirmed enumeration bug',{'roots':D80[:5].tolist()})
check('half_D_non_nested_N160',abs(D160[1]-36*np.pi**2/25)<1e-13 and abs(D80[1]-16*np.pi**2/25)<1e-13,'confirmed enumeration bug',{'N80':D80[:5].tolist(),'N160':D160[:5].tolist()})
muMax=max(4*np.pi**2*(80+2)**2/.5**2,100.)
pts=max(4000,int(np.ceil(400*np.sqrt(muMax))))
endpoint=np.linspace(1e-8,muMax,pts)[:2]
left,right=map(F.from_float,map(float,endpoint))
# Exact arithmetic comparison certifies exactly two analytic D eigenvalues in the first cell.
check('half_D_first_cell_contains_exactly_two_roots',0<left<piL*piL/25 and 4*piU*piU/25<right<9*piL*piL/25,'exact rational grid-count counterexample',{'grid_endpoints':endpoint.tolist(),'grid_points':pts})
check('half_N_small_N_matches_exact',np.allclose(N4,(np.arange(1,5)-.5)**2*np.pi**2/25,rtol=1e-13,atol=0),'source function numeric')
check('half_N_N80_N160_change_low_index',abs(N80[0]-25*np.pi**2/100)<1e-13 and abs(N160[0]-81*np.pi**2/100)<1e-13,'confirmed enumeration bug',{'N80':N80[:5].tolist(),'N160':N160[:5].tolist()})
mu=N160[1]
check('wrong_pole_identity_in_nested_calls',np.where(N80==mu)[0].tolist()==[3],'confirmed wrong exclusion index',{'mu':float(mu),'claimed_pole_index':1,'actual_index':3})
with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter('always')
    val=_spectral_green(hb,mu,1,'N',.1,.1,N=80)
check('wrong_pole_produces_infinity',np.isposinf(val),'source function counterexample',{'value':str(val),'warnings':[str(r.message) for r in ws]})

# Pure linear algebra: conjugation changes which parity block is being tested.
a,b,c,d,e,f=sp.symbols('a b c d e f',real=True)
K=sp.Matrix([[a,b,c,d],[b,e,f,c],[c,f,e,b],[d,c,b,a]])
Be=sp.Matrix([[1,0],[0,1],[0,1],[1,0]])/sp.sqrt(2)
Bo=sp.Matrix([[1,0],[0,1],[0,-1],[-1,0]])/sp.sqrt(2)
S=sp.diag(1,-1,1,-1);E=sp.diag(1,-1)
check('Kprime_odd_equals_conjugated_K_even',sp.simplify(Bo.T*S*K*S*Bo-E*Be.T*K*Be*E)==sp.zeros(2),'symbolic all-matrix identity')
check('Kprime_odd_is_not_raw_K_odd_identity',sp.simplify(Bo.T*S*K*S*Bo-Bo.T*K*Bo)!=sp.zeros(2),'symbolic inequivalent objects; arbitrary matrix not SL counterexample')

# Independently solve the real R4 SUP stationary configuration and differentiate the exact transfers.
with contextlib.redirect_stdout(io.StringIO()): gout=gcheck.main()
check('R4_mode_identity_from_physical_zero_count',len(gout['physical_zeros_2'])==1 and len(gout['physical_zeros_3'])==2,'independent finite nodal count',{'mode2':gout['physical_zeros_2'],'mode3':gout['physical_zeros_3']})
check('R4_stationary_transfer_and_K_symmetry',mp.mpf(gout['residual'])<mp.mpf('1e-50') and mp.mpf(gout['K_symmetry_error'])<mp.mpf('1e-50'),'65-digit independent numerical')
check('R4_Green_formula_targets_Kprime_odd',mp.mpf(gout['raw_Ko_discrepancy'])>5 and mp.mpf(gout['Kp_odd_discrepancy'])<mp.mpf('1e-50'),'65-digit countercheck; not interval certification',gout)
check('R4_corrected_raw_odd_Green_formula',mp.mpf(gout['corrected_Ko_discrepancy'])<mp.mpf('1e-50'),'65-digit independent numerical')

out={'commit':'be7c0912849a50a46869773eab4b3a2ec655ce88','optimized':not __debug__,'count':len(RESULTS),'checks':RESULTS,'environment':{'python':sys.version,'numpy':np.__version__,'sympy':sp.__version__,'mpmath':mp.__version__,'platform':platform.platform()},'scope':'Source function excerpts, symbolic identities and finite numerical diagnostics. Not a full repository test run, general interval proof, or Lean verification.'}
filename=ROOT/'evidence'/('checks_optimized.json' if not __debug__ else 'checks_normal.json')
filename.write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('TOTAL',len(RESULTS),'CONFIRMED',flush=True)
