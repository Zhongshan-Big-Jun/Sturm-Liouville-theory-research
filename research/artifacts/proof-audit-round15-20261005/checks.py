"""Round 15 current-workspace properties and unchanged finite algebra controls.
Baseline defect expectations remain only in the immutable input package.
Analytic infinite-dimensional claims live in proofs/, not in the test count.
"""
from pathlib import Path
import sys, json, hashlib, argparse, platform, time, math
from fractions import Fraction as Q
import numpy as np
import sympy as sp
WORK=Path(__file__).resolve().parent
ROOT=Path(__file__).resolve().parents[3]
if '--root' in sys.argv:
    ROOT=Path(sys.argv[sys.argv.index('--root')+1]).resolve()
sys.path.insert(0,str(ROOT/'scripts'))
from _gapn2_symmetry_recon import Recon, roots_of, eigenfunction_states, real_green_matrix
from _gapn2_jacobian_probe import symmetric_root
from op03_gap_fixed import lams_precise, eigfuns_precise
from _sl_spectral_identity import IndexedSpectrum, spectrum_for, spectral_denominators, reduced_pole_table
from _gapn2_jacobian_spectral import gtilde_spectral_blocks
from independent_physical import evaluate
import warnings, ast

CHECKS=[]; DATA={}
def require(name,condition,detail=None):
    ok=bool(condition)
    CHECKS.append(dict(name=name,ok=ok,detail=detail))
    print(('PASS' if ok else 'FAIL')+' '+name,flush=True)
    if not ok:raise RuntimeError(name)
def reject(name,fn):
    try:fn()
    except (ValueError,ArithmeticError) as e:
        require(name,True,dict(type=type(e).__name__,message=str(e)));return
    require(name,False,'invalid input was accepted')
def git_blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def mul(a,b):
    p=[x*y for x in a for y in b];return(min(p),max(p))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[1],a[1]-b[0])
def scale(a,c):return mul(a,(c,c))
def sincos(x,terms=32):
    # Lagrange bounds; no floating point and no assumption of alternating decay.
    ss=sum(((-1)**j*x**(2*j+1)/math.factorial(2*j+1) for j in range(terms)),Q(0))
    cc=sum(((-1)**j*x**(2*j)/math.factorial(2*j) for j in range(terms)),Q(0))
    rs=abs(x)**(2*terms+1)/math.factorial(2*terms+1)
    rc=abs(x)**(2*terms)/math.factorial(2*terms)
    return (ss-rs,ss+rs),(cc-rc,cc+rc)
def characteristic(w,L,C):
    sa,ca=sincos(100*L*w);sb,cb=sincos(C*w)
    even=sub(mul(ca,cb),scale(mul(sa,sb),Q(1,100)))
    odd=add(scale(mul(sa,cb),Q(1,100)),mul(ca,sb))
    return even,odd

def main():
    for f,expected in [('_sl_prufer.py','a69d89e28cb54562cbea605c92a822b807d75529'),
                       ('_sl_spectral_identity.py','53a8069ec5e064765b034dabc8f06729c7946d10')]:
        actual=git_blob((ROOT/'scripts'/f).read_bytes())
        require('full_source_blob_'+f,actual==expected,actual)
    rc=Recon(2,4,'sup');d=1e-6
    z=rc.widths_to_z([d,d,1-4*d,d,d])
    ans,ev=symmetric_root(rc,z,return_diagnostics=True)
    DATA['thin_false_root']=ev
    require('R14_endpoint_pseudoroot_rejected',ans is None and not ev['accepted'] and ev['relative_max']>.6)
    zfar=rc.widths_to_z(np.ones(5)/5)
    ans,ev=symmetric_root(rc,zfar,max_nfev=1,return_diagnostics=True)
    require('R14_unconverged_rejected',ans is None and ev['status']=='not_converged',ev)
    seeds={'sup':[.29343444668879154,.36546070235557726,.6345392976444227,.7065655533112085],
           'inf':[.2028824169434251,.4040382298316725,.5959617701683275,.7971175830565749]}
    DATA['true_roots']={}
    for mode,edges in seeds.items():
        r=Recon(2,4,mode);w=np.diff(np.r_[0,edges,1]);z0=r.widths_to_z(w)
        zr,ev=symmetric_root(r,z0,return_diagnostics=True)
        require('R14_true_R4_'+mode,zr is not None and ev['accepted'],ev)
        b=r.blocks_from_z(zr);ww=roots_of(b,3)
        ref=evaluate(b,[(2,ww[1]),(3,ww[2])],dps=65)
        require('independent_R4_modes_mass_balance_'+mode,max(abs(float(x)) for x in ref['relative_defect'])<1e-9)
        DATA['true_roots'][mode]=dict(diagnostics=ev,reference=ref)
    # Pole-table rejection is tested on exact current file bytes.
    blocks=[(1.,1.)];table=IndexedSpectrum(blocks,'D',21);lam=table.eigenvalues[0]
    reject('R14_wrong_full_pole_rejected',lambda:gtilde_spectral_blocks(blocks,lam,1,[.2,.7],N=20,spectrum=table))
    reject('R14_wrong_BC_rejected',lambda:reduced_pole_table(blocks,lam,'N',Mode=1))
    reject('R14_positive_non_eigenvalue_rejected',lambda:reduced_pole_table(blocks,1.,'D',Mode=1))
    reject('R14_wrong_geometry_rejected',lambda:spectrum_for([(1.,2.)],'D',3,table))
    reject('R14_insufficient_table_rejected',lambda:spectrum_for(blocks,'D',30,table))
    G=gtilde_spectral_blocks(blocks,lam,0,[.2,.7],N=20,spectrum=table)
    require('R14_valid_reduced_Green_finite_symmetric',np.all(np.isfinite(G)) and np.max(abs(G-G.T))<1e-14)
    for bc in ['D','N']:
        ts=[IndexedSpectrum([(.5,100.)],bc,n) for n in [4,80,160]]
        require('R14_half_prefix_'+bc,all(np.array_equal(ts[0].prefix(4),t.prefix(4)) for t in ts[1:]))
        ids=np.arange(1,5)-(0.5 if bc=='N' else 0.)
        expected=(ids*np.pi/5)**2
        require('R14_half_analytic_'+bc,np.max(abs(ts[0].prefix(4)-expected))<1e-12)
    x=np.array([.7,0.,.2,1.]);G0=real_green_matrix(blocks,0,x)
    expected=np.minimum.outer(x,x)*(1-np.maximum.outer(x,x))
    require('R13_green_zero_endpoints_permutation',np.max(abs(G0-expected))<1e-15)
    Gn=real_green_matrix(blocks,-1,x)
    expected=np.sinh(np.minimum.outer(x,x))*np.sinh(1-np.maximum.outer(x,x))/np.sinh(1)
    require('R13_green_negative',np.max(abs(Gn-expected))<1e-15)
    vz=eigenfunction_states(blocks,0,[0.,.2,.7,1.])
    require('R13_common_mass_linear_limit',np.max(abs(vz[:,0]-np.sqrt(3)*np.array([0.,.2,.7,1.])))<1e-14 and np.max(abs(vz[:,1]-np.sqrt(3)))<1e-14)
    # Current full module, not the baseline excerpt: first modes and prefix identity.
    b=[(.021,10000.),(.958,1.),(.021,10000.)]
    fresh=lams_precise(b,6)
    DATA['repaired_scan']=dict(blocks=b,frequencies=fresh.tolist())
    for k in [1,3,6,12]:
        w=lams_precise(b,k)
        require('R15_exact_count_increasing_'+str(k),len(w)==k and np.all(np.isfinite(w)) and np.all(np.diff(w)>0))
        require('R15_prefix_'+str(k),np.array_equal(w[:min(k,6)],fresh[:min(k,6)]))
    ref=evaluate(b,list(enumerate(fresh,1)),dps=65)
    DATA['repaired_scan']['independent']=ref
    require('R15_physical_zero_counts_1_to_6',all(t['internal_zero_count']==i-1 for i,t in enumerate(ref['modes'],1)))
    require('R15_physical_frequencies_1_to_6',max(abs(fresh[i]-float(t['frequency'])) for i,t in enumerate(ref['modes']))<1e-12)
    require('R15_frequency_not_eigenvalue',fresh[0]<1 and abs(fresh[0]-float(ref['modes'][0]['frequency']))<1e-12 and abs(fresh[0]-float(ref['modes'][0]['eigenvalue']))>.1)
    ctr=[(.30,1.),(.4,4.),(.3,1.)]
    a=lams_precise(ctr,3);bb=roots_of(ctr,3)
    require('R15_R4_positive_control',max(abs(a-bb))<1e-12,dict(frequencies=a.tolist(),indexed=bb.tolist()))
    r4ref=evaluate(ctr,list(enumerate(a,1)),dps=65)
    require('R15_R4_physical_indices',all(t['internal_zero_count']==i-1 for i,t in enumerate(r4ref['modes'],1)))
    vals=eigfuns_precise(ctr,a,np.array([.3,.7]))
    require('R15_R4_common_mass',max(abs(vals[i,j]-float(r4ref['modes'][i]['values'][j])) for i in range(3) for j in range(2))<1e-12)
    DATA['repaired_scan']['R4_reference']=r4ref
    for k in [0,-1,1.5,True,'3',complex(3)]:
        reject('R15_invalid_count_'+repr(k),lambda k=k:lams_precise(ctr,k))
    for ib,bad in enumerate([[],[(0.,1.)],[(-1.,1.)],[(1.,0.)],[(1.,-1.)],[(math.nan,1.)],[(1.,math.inf)],[(1.,1.),(1e-20,1.)],[(1.,1.,1.)]]):
        reject('R15_invalid_geometry_'+str(ib),lambda bad=bad:lams_precise(bad,3))
    for param in ['tol','smax_scale']:
        for bad in [0.,-1.,math.nan,math.inf,True,'1e-15',complex(1)]:
            reject('R15_invalid_'+param+'_'+repr(bad),lambda param=param,bad=bad:lams_precise(ctr,3,**{param:bad}))
    for tol in [1e-8,1e-15]:
        require('R15_tol_positive_'+str(tol),max(abs(lams_precise(ctr,3,tol=tol)-a))<1e-12)
    reject('R15_tol_unresolved_rejected',lambda:lams_precise([(1.,1.)],3,tol=1e-30))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        alternate=lams_precise(b,6,smax_scale=.1)
    require('R15_deprecated_scale_warns_and_preserves_modes',np.array_equal(alternate,fresh) and len(caught)==1 and issubclass(caught[0].category,DeprecationWarning))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always');lams_precise(ctr,3)
    require('R15_default_scale_no_warning',not caught)
    # Actual FH caller at four original R4 points, with the same epsilon.
    import op03_gap_fh as FH
    for u in [.40,.43,.45,.458]:
        gap,f=FH.Df_at(u);eps=1e-5
        num=(FH.Df_at(u+eps)[0]-FH.Df_at(u-eps)[0])/(2*eps);pred=2*(1-4)*f
        require('R15_R4_FH_'+str(u),abs(num-pred)<2e-6,dict(numerical=num,prediction=pred,error=abs(num-pred)))
    # Four exact rational brackets; also repeat for the exact binary64 input lengths.
    rootboxes=[('0.746219772791','0.746219772792',0),('0.760484385275','0.760484385276',1),
               ('2.235281119475','2.235281119476',0),('2.246563445569','2.246563445570',1)]
    exact=[]
    for label,L,C in [('rational_model',Q(21,1000),Q(479,1000)),
                      ('binary_inputs',Q.from_float(.021),Q.from_float(.958)/2)]:
        for i,(lo,hi,branch) in enumerate(rootboxes):
            fl=characteristic(Q(lo),L,C)[branch];fh=characteristic(Q(hi),L,C)[branch]
            passed=(fl[0]>0 and fh[1]<0) or (fl[1]<0 and fh[0]>0)
            require('exact_root_bracket_'+label+'_'+str(i+1),passed)
            exact.append(dict(model=label,interval=[lo,hi],branch='E' if branch==0 else 'O',
                value_left=list(map(str,fl)),value_right=list(map(str,fh))))
    DATA['exact_root_brackets']=exact
    smax=np.pi*100*5+20;grid=np.linspace(1e-7,smax,30000)
    ia=np.searchsorted(grid,fresh[0])-1;ib=np.searchsorted(grid,fresh[1])-1
    ja=np.searchsorted(grid,fresh[2])-1;jb=np.searchsorted(grid,fresh[3])-1
    cells = [[Q.from_float(float(grid[ia])), Q.from_float(float(grid[ia+1]))],
             [Q.from_float(float(grid[ja])), Q.from_float(float(grid[ja+1]))]]
    exact_containment = (cells[0][0] < Q(rootboxes[0][0]) < Q(rootboxes[1][1]) < cells[0][1]
                         and cells[1][0] < Q(rootboxes[2][0]) < Q(rootboxes[3][1]) < cells[1][1])
    require('legacy_grid_two_pairs_inside_single_cells',ia==ib and ja==jb and exact_containment,
            dict(cells=[[float(v) for v in cell] for cell in cells],
                 exact_binary_cells=[[str(v) for v in cell] for cell in cells],
                 rational_root_boxes_strictly_inside=True))
    # Finite algebra supporting the new analytic proof, never replacing it.
    t,zs=sp.symbols('t z',positive=True)
    p4=t**4-2*t**2;p5=t**5-2*t**3
    def B(p):return sp.Matrix([sp.diff(p,t).subs(t,1)-(p.subs(t,1)-p.subs(t,-1))/2,
                              sp.diff(p,t).subs(t,-1)-(p.subs(t,1)-p.subs(t,-1))/2])
    T=sp.Matrix.hstack(B(sp.diff(p4,t,2)),B(sp.diff(p5,t,2)))
    require('boundary_lifts_exact',T==sp.Matrix([[24,40],[-24,40]]),str(T))
    require('boundary_lift_inverse_exact',T.inv()==sp.Matrix([[sp.Rational(1,48),-sp.Rational(1,48)],
                                                           [sp.Rational(1,80),sp.Rational(1,80)]]))
    phi=t**(zs+6)-(zs+6)/(zs+4)*t**(zs+4)
    require('holomorphic_family_endpoint_condition',sp.simplify(sp.diff(phi,t).subs(t,1))==0)
    for m in [3,4,10]:
        pp=t**(2*m)-sp.Rational(m,m-1)*t**(2*m-2)
        require('holomorphic_family_integer_'+str(m),sp.simplify(phi.subs(zs,2*m-6)-pp)==0)
    for exps in [[0,2,6],[1,3,9],[0,8,32,128]]:
        q=sp.Rational(1,2);Gram=sp.Matrix([[sp.Rational(1,a+b+1) for b in exps] for a in exps])
        v=sp.Matrix([1/(q+a+1) for a in exps]);distance=1/(2*q+1)-(v.T*Gram.inv()*v)[0]
        product=1/(2*q+1)*sp.prod(((q-a)/(q+a+1))**2 for a in exps)
        require('Cauchy_Gram_distance_'+str(exps),sp.simplify(distance-product)==0 and distance>0)
    require('trace_coordinate_matrix',sp.Matrix([[1,0,0],[0,1,0],[0,0,-4]]).det()==-4)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);a=p.parse_args();started=time.time()
    error=None
    try:main()
    except Exception as e:error=dict(type=type(e).__name__,message=str(e))
    result=dict(baseline_commit='ec45bf99ae746b0a3699557e06700a3c00c5a831',test_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),source_sha256={name:hashlib.sha256((ROOT/'scripts'/name).read_bytes()).hexdigest() for name in ['op03_gap_fixed.py','op03_gap_fh.py','_sl_prufer.py','_sl_spectral_identity.py','_gapn2_symmetry_recon.py','_gapn2_jacobian_probe.py','_gapn2_jacobian_spectral.py']},python=sys.version,
                optimized=not __debug__,platform=platform.platform(),seconds=time.time()-started,
                count=len(CHECKS),passed=sum(x['ok'] for x in CHECKS),checks=CHECKS,data=DATA,error=error,
                scope='Finite numerical regressions, exact rational brackets and symbolic algebra; not a machine proof of infinite-dimensional theorems.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False))
    if error:print(error,file=sys.stderr);raise SystemExit(1)
    print('CONFIRMED',len(CHECKS),flush=True)
