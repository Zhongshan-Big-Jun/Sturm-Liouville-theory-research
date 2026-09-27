"""Reproduce Round 13 findings; PASS means the specified observation is confirmed.
No remote repository is modified. Infinite-dimensional assertions are proved in
analytic_notes.md, not by these finite checks. Run: python checks.py; python -O checks.py.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext, getcontext
import ast, hashlib, json, math, platform, sys, warnings
import numpy as np
import mpmath as mp
import sympy as sp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source_excerpts'))
import rigid_dec as dec
import rational_excerpt as rat
import spectral_core as spec
import half_core as half
from independent_interface import run as interface_run
MODE='optimized' if not __debug__ else 'normal'
ROWS=[]; DATA={}

def check(name, condition, detail=None):
    if not bool(condition): raise RuntimeError('CHECK FAILED: '+name+' '+str(detail))
    ROWS.append(dict(name=name,confirmed=True,detail=detail))
    print('CONFIRMED',name,flush=True)

def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def interval_strings(v):return [str(v.lo),str(v.hi)]
def safe(v):
    if isinstance(v,(np.floating,np.integer)):return v.item()
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,(F,Decimal,Path)):return str(v)
    raise TypeError(type(v).__name__)

def exact_atan_bounds(x,N=70):
    if not (0<x<1):raise ValueError('atan proof range')
    s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(N)),F(0))
    t=(-1)**N*x**(2*N+1)/F(2*N+1)
    return min(s,s+t),max(s,s+t)
def exact_trig_bounds(x,which,N=40):
    if not 0<x<1:raise ValueError('trig proof range')
    base=1 if which=='sin' else 0
    s=sum((F((-1)**k)*x**(2*k+base)/math.factorial(2*k+base) for k in range(N)),F(0))
    t=F((-1)**N)*x**(2*N+base)/math.factorial(2*N+base)
    return min(s,s+t),max(s,s+t)
def dec_out(q,places=32,up=False):
    scale=10**places;z=q*scale
    n=-((-z.numerator)//z.denominator) if up else z.numerator//z.denominator
    sign='-' if n<0 else '';n=abs(n)
    return f'{sign}{n//scale}.{n%scale:0{places}d}'

# Whole-file identity, not inferred from filenames.
for name,expected in [('rigid_dec.py','92fa400d858e859e6c39d5ca77b4753e0d0a9d8e'),
 ('_sl_prufer.py','a69d89e28cb54562cbea605c92a822b807d75529'),
 ('zz_verify_e1_dec.py','dd8a5207210cb0a29c509d3bd4b4121d7d224132')]:
    check('SOURCE '+name,blob((ROOT/'source_excerpts'/name).read_bytes())==expected)

# 01: current certificate's displayed positive lower endpoint is rounded upward.
x=F(17,20);a5=exact_atan_bounds(F(1,5));a239=exact_atan_bounds(F(1,239))
pL,pU=16*a5[0]-4*a239[1],16*a5[1]-4*a239[0]
sL,sU=exact_trig_bounds(x,'sin');cL,cU=exact_trig_bounds(x,'cos')
bL,bU=(pL-x)*cL-2*sU,(pU-x)*cU-2*sL
claimed=F('0.009851718323')
check('01 actual B1 certificate point excludes the exact value',bU<claimed)
check('01 the original weaker B1 >= 1/200 remains true',bL>F(1,200))
check('01 ds(1/3) is not a lower endpoint',F(rat.ds(F(1,3)))>F(1,3))
DATA['certificate_display']={'printed_interval':[str(claimed)]*2,
 'independent_true_bounds':[dec_out(bL),dec_out(bU,up=True)],
 'true_bounds_exact':[str(bL),str(bU)],'ds_one_third':rat.ds(F(1,3))}

# 02: the two callers test positivity, not their advertised nonzero thresholds.
for label,a,b,target in [('TA_B2',F(723,1000),F(724,1000),F(27,10)),('TC',F(82,100),F(83,100),F(19,10))]:
    ok,pieces=rat.taylor_value(lambda _:rat.D2(rat.I(1)),a,b,True,4)
    check('02 '+label+' call pattern accepts 1 below its labelled threshold',ok and F(1)<target)
    DATA['threshold_'+label]={'test_callback':'constant 1, not an assertion about the actual TA/TC functions',
          'labelled_threshold':str(target),'accepted':ok,'pieces':pieces}

# 03: range of cosine, not cosine evaluated at the interval radius.
v=rat.I_cos(rat.I(F(-1,10),F(1,10)))
check('03 rational cos interval misses cos(0)=1',v.hi<1)
check('03 exact rational cosine can falsely prove 0.997-cos positive', (rat.I(F(997,1000))-v).lo>0)
s=dec.I_sin(dec.I(-2,2)); c=dec.I_cos(dec.I(-4,4))
check('03 Decimal sin misses interior maximum',F(s.hi)<1)
check('03 Decimal cos misses interior minimum',F(c.lo)>-1)
ok,boxes=dec.range_pos(lambda z:Decimal('0.95')-dec.d1_sin(z),-2,2)
check('03 Decimal range_pos falsely accepts 0.95-sin on [-2,2]',ok and boxes==1)
DATA['trig']={'rational_cos_interval_exact':interval_strings(v),'rational_cos_interval_float':[float(v.lo),float(v.hi)],
 'decimal_sin':interval_strings(s),'decimal_cos':interval_strings(c),'false_range_result':[ok,boxes]}

# 04: atanh is not involved; this is ordinary atan, continuous across x=1.
try:
    rat.I_atan(rat.I(F(9,10),F(11,10)))
    caught=False; err='no exception'
except RecursionError as e:caught=True;err=str(e)
check('04 rational atan crossing 1 recurses without progress',caught)
DATA['atan_recursion']={'input':['9/10','11/10'],'exception':'RecursionError','message':err}

# 05: old Decimal engine's two elementary endpoint operations.
getcontext().prec=70
v=dec.I(2).sqrt();q=v.lo
check('05 Decimal sqrt returns a non-enclosing singleton',v.lo==v.hi and F(q)**2<2)
with localcontext() as ctx:
    ctx.prec=100;t=q+Decimal('1e-70')
ok,boxes=dec.range_pos(lambda z:t-z.sqrt(),2,2)
check('05 Decimal sqrt induces a false strict sign proof',ok and F(t)**2<2 and t>q)
a=Decimal('1.'+'0'*69+'1');neg=-dec.I(a)
check('05 unary minus rounds away an exact negative input',not(F(neg.lo)<=-F(a)<=F(neg.hi)))
DATA['decimal_endpoints']={'sqrt2_interval':interval_strings(v),'false_positive_threshold':str(t),
   'threshold_square_lt_2':F(t)**2<2,'range_result':[ok,boxes],
   'neg_input':str(a),'neg_interval':interval_strings(neg),'exact_negated_input':str(-F(a))}

# 06: actual restored driver process, with one intentionally false obligation.
e1=ROOT/'evidence'/f'e1_{MODE}_runs.json'
if not e1.exists():
    import subprocess
    subprocess.run([sys.executable]+(['-O'] if not __debug__ else [])+[str(ROOT/'run_e1.py')],check=True)
runs=json.loads(e1.read_text())
check('06 full legacy E1 driver replays 55 original facts',runs[0]['facts']==55 and runs[0]['exit_code']==0 and runs[0]['failed']==[])
check('06 a FAIL still yields successful process exit and a ledger',runs[1]['exit_code']==0 and len(runs[1]['failed'])==1)
DATA['driver_runs']=runs

# 07: the normalization ratio is evaluated at a modal node.
rc=spec.Recon(2,1.,'sup');z=rc.widths_to_z(np.diff([0.,.1,.5,.6,.8,1.]))
ed=spec.eigen_data(rc,z);x=ed['edges'];blocks=rc.blocks_from_z(z);roots=spec.roots_of(blocks,3)
ue=np.sqrt(2)*np.sin(2*np.pi*x);de=2*np.pi*np.sqrt(2)*np.cos(2*np.pi*x)
direct=spec.eigfun(blocks,roots[1],x)
error=float(np.max(np.abs(ed['up_n']-de)));scale=float(ed['up_n'][0]/de[0])
check('07 modal frequencies are correct in the normalization counterexample',np.max(abs(roots-np.arange(1,4)*np.pi))<1e-12)
check('07 direct eigfun still has correct normalization',np.max(abs(direct-ue))<1e-12)
check('07 eigen_data node division corrupts the derivative amplitude',error>1)
DATA['normalization']={'actual_edges':x.tolist(),'actual_edges_hex':[float(t).hex() for t in x],
  'frequencies':roots.tolist(),'returned_u':ed['u_n'].tolist(),'direct_normalized_u':direct.tolist(),
  'returned_derivative':ed['up_n'].tolist(),'exact_derivative':de.tolist(),'max_derivative_error':error,
  'amplitude_factor':scale,'implied_normalized_mass':scale**2}

# A second normalization example has R=4 and non-small blocks.
from independent_interface import normalized_values
rc4=spec.Recon(1,4.,'sup')
z4=rc4.widths_to_z(np.diff([0.,.55,.674645570014273463160410442496,1.]))
e4=spec.eigen_data(rc4,z4);roots4=spec.roots_of(rc4.blocks_from_z(z4),2)
ind4=normalized_values(e4['edges'],roots4[1]);true4=np.array(ind4['values'],dtype=float);dtrue4=np.array(ind4['derivatives'],dtype=float)
factor4=float(e4['u_np1'][1]/true4[1])
check('07 nondegenerate R=4 nodal normalization also fails',abs(factor4-1)>.5)
check('07 R=4 direct eigfun agrees with independent physical normalization',np.max(abs(spec.eigfun(rc4.blocks_from_z(z4),roots4[1],e4['edges'])-true4))<1e-12)
DATA['normalization_R4']={'actual_edges':e4['edges'].tolist(),'actual_edges_hex':[float(t).hex() for t in e4['edges']],
  'frequencies':roots4.tolist(),'returned_u2':e4['u_np1'].tolist(),'returned_derivative2':e4['up_np1'].tolist(),
  'independent':ind4,'amplitude_factor':factor4,'implied_mass':factor4**2,
  'max_derivative_error':float(np.max(abs(e4['up_np1']-dtrue4)))}

# 08: a point permutation must induce only a simultaneous row/column permutation.
p=np.array([.25,.75]);G=spec.green_kernel([(1.,1.)],1,p)
Gr=spec.green_kernel([(1.,1.)],1,p[::-1]);GT=G[::-1,::-1]
check('08 Green uses list order instead of coordinate order',np.max(abs(Gr-GT))>.47)
check('08 Green error equals sin(1/2)',abs((Gr[0,1]-GT[0,1])-math.sin(.5))<1e-14)
check('08 unordered positive resolvent yields a spurious negative eigenvalue',np.min(np.linalg.eigvalsh(Gr))<0 and np.min(np.linalg.eigvalsh(GT))>0)
try:spec.green_kernel([(1.,1.)],1,[0.,.25]);endpoint_error=False
except ValueError as e:endpoint_error=True;endmsg=str(e)
check('08 valid left endpoint is not handled by uv_at',endpoint_error)
DATA['point_order']={'points':p[::-1].tolist(),'returned':Gr.tolist(),'correct_permutation':GT.tolist(),
 'max_error':float(np.max(abs(Gr-GT))),'wrong_eigenvalues':np.linalg.eigvalsh(Gr).tolist(),
 'correct_eigenvalues':np.linalg.eigvalsh(GT).tolist(),'endpoint_error':endmsg}

# 09: zero and negative mu are in the resolvent of both positive half problems.
zrows=[]
for bc in 'DN':
    for mu in (0.,-1.):
        with np.errstate(all='ignore'):closed=half.green_regular([(.5,1.)],mu,.1,.2,bc)
        exact=(.06 if bc=='D' else .1) if mu==0 else (math.sinh(.1)*math.sinh(.3)/math.sinh(.5) if bc=='D' else math.sinh(.1)*math.cosh(.3)/math.cosh(.5))
        finite=half._spectral_full_green([(.5,1.)],mu,bc,.1,.2,1000)
        check('09 closed Green mishandles valid '+bc+' mu='+str(mu),not np.isfinite(closed) and abs(finite-exact)<1e-8)
        zrows.append({'bc':bc,'mu':mu,'closed':'nan' if np.isnan(closed) else str(closed),'exact':exact,'finite_1000':finite})
DATA['nonpositive_green']=zrows

# Round 12 positive controls: use the repaired modes/pole binding, not old scans.
r12=[]
for bc in 'DN':
    tab=half.half_spectrum([(.5,100.)],bc,160,return_table=True)
    p4=half.half_spectrum([(.5,100.)],bc,4);p80=half.half_spectrum([(.5,100.)],bc,80)
    j=np.arange(1,161)-(0 if bc=='D' else .5)
    exact=j*j*np.pi**2/25
    check('R12 '+bc+' exact constant-density spectrum and prefix consistency',np.array_equal(p4,tab.prefix(4)) and np.array_equal(p80,tab.prefix(80)) and np.max(abs(tab.prefix(160)/exact-1))<1e-13)
    val=half._spectral_green([(.5,100.)],tab.eigenvalues[1],1,bc,.1,.1,80,spectrum=tab)
    check('R12 '+bc+' matching pole is finite',np.isfinite(val))
    try:half._spectral_green([(.5,100.)],tab.eigenvalues[5],1,bc,.1,.1,80,spectrum=tab);rejected=False
    except ValueError:rejected=True
    check('R12 '+bc+' incorrect pole identity is explicitly rejected',rejected)
    r12.append({'bc':bc,'first_four':p4.tolist(),'reduced_value':val,'mismatched_pole_rejected':rejected})
DATA['round12_controls']=r12

# 10: off-root residual differentiation has terms absent from the root-only formula.
a,b,Ui,Uj,Vi,Vj,si,F_i,F_j=sp.symbols('a b Ui Uj Vi Vj si Fi Fj')
true=si/b*(2*a*Ui*Uj-2*b*Vi*Vj-(a*Uj-b*Vj)*Vi)
old=si/b*(2*a*Ui*Uj*(b-a)/b)
expected=si/b**2*(a*Ui*F_j+2*a*Uj*F_i-F_i*F_j)
check('10 general residual-Jacobian correction is a symbolic identity',sp.factor((true-old-expected).subs({F_i:a*Ui-b*Vi,F_j:a*Uj-b*Vj}))==0)
ind=interface_run();Jtrue=np.array(ind['jacobian'],dtype=float)
rc=spec.Recon(1,4.,'sup');z=rc.widths_to_z(np.diff([0.,.25,.75,1.]));ed=spec.eigen_data(rc,z)
a,b=ed['lam_n'],ed['lam_np1'];u,v=ed['u_n'],ed['u_np1'];f=a*u*u-b*v*v;s=np.diff(rc.pat)
corr=np.array([[s[i]/b**2*(a*u[i]**2*f[j]+2*a*u[j]**2*f[i]-f[i]*f[j]) for i in range(2)]for j in range(2)])
js=[]
for N in (160,640,2560):
    J=spec.analytic_jacobian_spectral(rc,z,N)
    js.append({'N':N,'uncorrected_error':float(np.max(abs(J-Jtrue))),'corrected_error':float(np.max(abs(J+corr-Jtrue)))})
check('10 the off-root error does not disappear with spectral truncation',all(r['uncorrected_error']>1.4 for r in js))
check('10 adding the derived correction removes the finite bias',js[-1]['corrected_error']<.003 and js[-1]['corrected_error']<js[0]['corrected_error']/10)
DATA['offroot_jacobian']={'independent':ind,'source_residual':(f/b).tolist(),'correction':corr.tolist(),'truncations':js}

# 11: exact trial-function estimate for the Helly nonattainment example.
k,R=sp.symbols('k R',positive=True);t=sp.symbols('t',nonnegative=True)
q=sp.integrate((1-k*t)*sp.pi**2*t**2,(t,0,1/k))
check('11 exact mass-defect bound for continuous monotone densities',sp.simplify(q-sp.pi**2/(12*k**3))==0)
DATA['helly_counterexample']={'class':'continuous nondecreasing 1<=rho<=R, rho(0)=1, rho(1)=R',
 'sequence':'rho_k=1+(R-1)*min(k*x,1)',
 'infimum':'pi^2/R, not attained; proof in analytic_notes.md',
 'trial_mass_defect_upper_bound':'(R-1)*pi^2/(12*k^3)'}

DATA['environment']={'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,'mpmath':mp.__version__,'sympy':sp.__version__,'decimal_precision':getcontext().prec,'mode':MODE}
OUT=ROOT/'evidence'/f'checks_{MODE}.json'
OUT.write_text(json.dumps({'meaning':'CONFIRMED includes reproduced source failures, not kernel verification of repository theorems','checks':ROWS,'count':len(ROWS),'data':DATA},ensure_ascii=False,indent=2,default=safe))
print('Confirmed groups:',len(ROWS),'written',OUT)
