import hashlib
"""Round14 scoped checks. A confirmed defect is a PASS of a counterexample test,
not a PASS of upstream correctness. New infinite-dimensional results are proved
in the accompanying notes, not by these finite tests. No remote writes.
"""
from pathlib import Path
import sys,json,hashlib,warnings,argparse,time
from fractions import Fraction as Q
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[3]
if '--root' in sys.argv:
    ROOT=Path(sys.argv[sys.argv.index('--root')+1]).resolve()
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(ROOT/'scripts'))
from _gapn2_symmetry_recon import Recon,roots_of,eigenfunction_states,real_green_matrix
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data,term_breakdown
from _gapn2_jacobian_spectral import gtilde_spectral
from _gapn2_sector_decomposition import sector_data
from _gapn2_half_problem_probe import half_spectrum,_spectral_green,_spectral_full_green
from independent_physical import evaluate
from independent_threeblock import run as threeblock_reference

records=[]
def check(name, condition, details=None, kind='property'):
    passed=bool(condition)
    records.append(dict(name=name,passed=passed,kind=kind,details=details))
    if not passed:raise RuntimeError('check failed: '+name)
def maxerr(a,b):return float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
def rejects(fn):
    try:fn()
    except (ValueError,ArithmeticError):return True
    return False

def execute():
    data=(ROOT/'scripts/_sl_prufer.py').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    check('current_phase_full_blob_identity',blob=='a69d89e28cb54562cbea605c92a822b807d75529',blob,'provenance')
    for bc in ('D','N'):
        table=half_spectrum([(.5,100.)],bc,N=160,return_table=True)
        shift=0 if bc=='D' else .5
        expected=((np.arange(1,161)-shift)*np.pi/5)**2
        relative=maxerr(table.prefix(160)/expected,np.ones(160))
        check('constant_half_'+bc+'_indexed_spectrum',relative<2e-13,relative)
        check('constant_half_'+bc+'_prefix_invariance',
              np.array_equal(table.prefix(4),half_spectrum([(.5,100.)],bc,N=4)) and
              np.array_equal(table.prefix(80),half_spectrum([(.5,100.)],bc,N=80)))
        val=_spectral_green([(.5,100.)],table.eigenvalues[1],1,bc,.1,.2,N=80,spectrum=table)
        check('half_'+bc+'_correct_pole_is_finite',np.isfinite(val),val)
        check('half_'+bc+'_mismatched_pole_is_rejected',rejects(lambda:_spectral_green([(.5,100.)],table.eigenvalues[1],0,bc,.1,.2,N=80,spectrum=table)))
    pts=np.array([.4,0.,.1,.5,.1])
    for bc in ('D','N'):
        for mu in (0.,-1.):
            G=real_green_matrix([(.5,1.)],mu,pts,RightBoundary=bc)
            X=np.minimum(pts[:,None],pts[None,:]);Y=np.maximum(pts[:,None],pts[None,:])
            if mu==0:expected=X*(.5-Y)/.5 if bc=='D' else X
            else:expected=np.sinh(X)*(np.sinh(.5-Y)/np.sinh(.5) if bc=='D' else np.cosh(.5-Y)/np.cosh(.5))
            err=maxerr(G,expected)
            check(f'real_green_{bc}_mu_{mu}_permutation_endpoints_duplicates',err<2e-14,err)
    check('real_green_outside_point_rejected',rejects(lambda:real_green_matrix([(.5,1.)],0.,[-1e-5,.1])))
    points=[0.,.25,.5,.75,1.]
    U=eigenfunction_states([(1.,1.)],2*np.pi,points)
    ref=np.column_stack((np.sqrt(2)*np.sin(2*np.pi*np.array(points)),2*np.pi*np.sqrt(2)*np.cos(2*np.pi*np.array(points))))
    check('node_sampler_common_mass_constant_density',maxerr(U,ref)<2e-13,maxerr(U,ref))
    # R13 ordinary R4 node example: independent quadrature and physical zero count.
    node_rc=Recon(1,4.,'sup'); edges=np.array([.55,.6746455700142735]); z=node_rc.widths_to_z(np.diff(np.r_[0,edges,1]))
    ed=eigen_data(node_rc,z)
    hp_node=evaluate(node_rc.blocks_from_z(z),[(2,np.sqrt(ed['lam_np1']))])
    vals=np.array(hp_node['modes'][0]['values'],float);ders=np.array(hp_node['modes'][0]['derivatives'],float)
    err=max(maxerr(vals,ed['u_np1']),maxerr(ders,ed['up_np1']))
    check('R13_R4_node_normalization_fixed',err<2e-10,dict(error=err,reference=hp_node))
    # Deliberately invalid full-interval pole tuple must not be confused with valid data.
    rc=Recon(1,1.,'sup');z=rc.widths_to_z([.25,.5,.25]); ss=roots_of(rc.blocks_from_z(z),10)
    check('R14_02_wrong_full_pole_pair_rejected',rejects(lambda:gtilde_spectral(rc,z,ss[0]**2,1,[.25,.75],N=9)))
    rc=Recon(2,4.,'sup');delta=1e-6;z0=rc.widths_to_z([delta,delta,1-4*delta,delta,delta])
    candidate,diagnostic=symmetric_root(rc,z0,return_diagnostics=True)
    check('R14_01_false_stationary_rejected',candidate is None and diagnostic['status']=='rejected',diagnostic)
    ed=eigen_data(rc,z0);a,b=ed['lam_n'],ed['lam_np1'];u,v=ed['u_n'],ed['u_np1']
    r=(a*u*u-b*v*v)/(a*u*u+b*v*v)
    hp=evaluate(rc.blocks_from_z(z0),[(2,np.sqrt(a)),(3,np.sqrt(b))])
    check('R14_01_independent_negative_control',min(abs(np.array(hp['relative_defect'],float)))>.66 and maxerr(r,np.array(hp['relative_defect'],float))<1e-7,hp,kind='independent-check')
    check('R14_01_stationary_sector_rejects_nonroot',rejects(lambda:sector_data(rc,z0,N=20)))
    from _gapn2_symmetry_recon import one_solve
    check('R14_01_one_solve_rejects_nonroot',one_solve((2,4.,'sup',z0,'negative-control')) is None)
    check('R14_01_optimizer_success_is_not_stationarity',not rc.solve(z0).stationary)
    tiny=rc.widths_to_z([1e-12,1e-12,1-4e-12,1e-12,1e-12])
    tiny_diagnostic=rc.stationarity_diagnostics(tiny)
    check('R14_01_unresolved_denominator_is_not_accepted',not tiny_diagnostic['accepted'] and tiny_diagnostic['status']=='unresolved',tiny_diagnostic)
    narrow=np.array([1e-8,1e-8,1-4e-8,1e-8,1e-8])
    check('R14_01_no_artificial_minimum_width',maxerr(rc.z_to_widths(rc.widths_to_z(narrow)),narrow)<1e-15)
    check('R14_01_nonconvergence_is_not_accepted',rc.stationarity_diagnostics(z0,solver_success=False)['status']=='not_converged')
    from _gapn2_k_global_rank2 import build_kprime
    from _gapn2_kp_collapsed_probe import build
    check('R14_01_stationary_K_formulas_reject_nonroot',rejects(lambda:build_kprime(rc,z0,N=10)) and rejects(lambda:build(rc,z0,N=10)))
    from _gapn2_reduced_endpoint_hunt import Reduced
    for end in ('first','last','both'):
        reduced=Reduced(2,4.,'sup',end)
        widths=np.full(reduced.nb,1e-6);widths[reduced.nb//2]=1-(reduced.nb-1)*1e-6
        rz=reduced.widths_to_z(widths)
        check('R14_01_reduced_'+end+'_rejects_false_balance',not reduced.stationarity_diagnostics(rz)['accepted'])
        exhausted=reduced.solve(rz,max_nfev=1)
        check('R14_01_reduced_'+end+'_rejects_unconverged',not exhausted.stationary)
        check('R14_01_reduced_'+end+'_no_width_floor',maxerr(reduced.z_to_widths(rz),widths)<1e-15)
    from _gapn2_jacobian_analytic import analytic_jacobian
    check('R14_01_general_J_available_but_stationary_identity_absent',analytic_jacobian(rc,z0)[2] is None)
    # Controls: source finds ordinary interior roots; relative acceptance does not exclude them.
    # Current table seeds, then solve and check independently; the table is not an oracle.
    table_seeds={'sup':[.29343444668879154,.36546070235557726,.6345392976444227,.7065655533112085],
                 'inf':[.2028824169434251,.4040382298316725,.5959617701683275,.7971175830565749]}
    for mode in ('sup','inf'):
        initial=np.array(table_seeds[mode])
        rc=Recon(2,4.,mode);z=symmetric_root(rc,rc.widths_to_z(np.diff(np.r_[0.,initial,1.])))
        if z is None:raise RuntimeError('positive-control root missing')
        ed=eigen_data(rc,z);a,b=ed['lam_n'],ed['lam_np1'];u,v=ed['u_n'],ed['u_np1']
        ratio=(a*u*u-b*v*v)/(a*u*u+b*v*v)
        check('R4_'+mode+'_interior_root_relative_positive_control',max(abs(ratio))<1e-7,
              dict(edges=ed['edges'].tolist(),relative=ratio.tolist(),raw=rc.residual(z).tolist()))
        positive_hp=evaluate(rc.blocks_from_z(z),[(2,np.sqrt(a)),(3,np.sqrt(b))])
        check('R4_'+mode+'_independent_positive_control',max(abs(np.array(positive_hp['relative_defect'],float)))<1e-7,positive_hp,kind='independent-check')
        from _gapn2_ktilde_positivity import run as positivity_run
        check('R14_02_'+mode+'_positivity_target_coverage_rejected',rejects(lambda:positivity_run(2,mode,4.,z,N=1)))
        positivity=positivity_run(2,mode,4.,z,N=40)
        raw_sector=sector_data(rc,z,N=40)
        check('R14_02_'+mode+'_positivity_assembly_positive_control',np.isfinite(positivity['detK']))
        check('R14_02_'+mode+'_positivity_raw_K_sector_identity',maxerr(positivity['evKe'],raw_sector['Ke_ev'])<1e-8 and maxerr(positivity['evKo'],raw_sector['Ko_ev'])<1e-8)
        check('R14_02_'+mode+'_positivity_explicit_Kp_sector_identity',maxerr(positivity['evKpEven'],raw_sector['Ko_ev'])<1e-8 and maxerr(positivity['evKpOdd'],raw_sector['Ke_ev'])<1e-8)
        check('R4_'+mode+'_accepted_full_report',rc.full_report(z)['stationary'])
        check('R4_'+mode+'_stationary_sector_positive_control',all(np.isfinite(sector_data(rc,z,N=40)['Ke_ev'])))
        exhausted=symmetric_root(rc,z+np.array([.002,0,0,0,0]),max_nfev=1,return_diagnostics=True)
        check('R4_'+mode+'_exhausted_optimizer_rejected',exhausted[0] is None and exhausted[1]['status']=='not_converged',exhausted[1])
    # Preserve the corrected GENERAL Jacobian, using an independent implicit derivative.
    hpJ=threeblock_reference();Jref=np.array(hpJ['jacobian'],float)
    rc=Recon(1,4.,'sup');z=rc.widths_to_z([.25,.5,.25]);errors=[]
    for N in (160,640):
        ts=term_breakdown(rc,z,N=N);J=(np.diag(ts['fprime'])+ts['M1']+ts['M2']+ts['M3'])/ts['eigen_data']['lam_np1']
        errors.append(maxerr(J,Jref))
    check('R13_general_Jacobian_fix_preserved',errors[1]<.010 and errors[0]<.037 and errors[1]<errors[0]/3,
          dict(errors=errors,reference=hpJ),kind='independent-check')
    # Exact finite algebra checks supporting, but NOT proving, the analytic supplements.
    m,c=sp.symbols('m c',positive=True);z=sp.symbols('z')
    Ae=2*m*(2*m-1)+c*m/(m-1);Be=2*m*(2*m-3)
    Ao=2*m*(2*m+1)+c*m/(m-1);Bo=2*m*(2*m-1)
    target_e=[c*(z+2),-(z+4)*((z+2)*(z+3)+c),(z+2)*(z+4)*(z+1)]
    target_o=[c*(z+2),-(z+4)*((z+2)*(z+5)+c),(z+2)*(z+4)*(z+3)]
    for name,vec,target in [('even',[c,-Ae,Be],target_e),('odd',[c,-Ao,Bo],target_o)]:
        differences=[sp.factor(((2*m-2)*v).subs(m,(z+4)/2)-t) for v,t in zip(vec,target)]
        check('Mellin_polynomial_identity_'+name,all(v==0 for v in differences),[str(v) for v in differences],kind='exact-algebra')
    for exps in ([0,2,4],[1,3,7],[0,4,12,28]):
        q=sp.Rational(1,2);G=sp.Matrix([[sp.Rational(1,x+y+1) for y in exps] for x in exps]);h=sp.Matrix([1/(q+x+1) for x in exps])
        distance=1/(2*q+1)-(h.T*G.inv()*h)[0]
        product=1/(2*q+1)*sp.prod(((q-x)/(q+x+1))**2 for x in exps)
        check('Cauchy_Gram_distance_'+str(exps),sp.cancel(distance-product)==0,dict(distance=str(distance)),kind='exact-algebra')
    aa,bb,alpha=sp.symbols('a b alpha');beta2=alpha**2+2*(bb-aa)
    check('G2_endpoint_energy_identity',sp.expand(aa*alpha**2-bb*beta2+(bb-aa)*(alpha**2+2*bb))==0,kind='exact-algebra')
    check('constant_n2_endpoint_relative_defect',Q(2**4-3**4,2**4+3**4)==Q(-65,97),str(Q(-65,97)),kind='exact-algebra')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();started=time.time()
    failure=None
    try:execute()
    except Exception as e:failure=dict(type=type(e).__name__,message=str(e))
    source_names=['_gapn2_symmetry_recon.py','_gapn2_jacobian_probe.py','_gapn2_jacobian_analytic.py','_gapn2_jacobian_spectral.py','_gapn2_sector_decomposition.py','_gapn2_half_problem_probe.py','_sl_prufer.py','_sl_spectral_identity.py']
    result=dict(source_sha256={name:hashlib.sha256((ROOT/'scripts'/name).read_bytes()).hexdigest() for name in source_names},test_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),status='PASS' if failure is None else 'FAIL',checks=len(records),passed=sum(r['passed'] for r in records),
        python=sys.version,optimized=not __debug__,elapsed_seconds=time.time()-started,records=records,failure=failure,
        limitation='Actual current workspace modules plus independent high-precision physical and implicit derivative references; finite diagnostics, not interval proofs, global scans, Lean or infinite-dimensional theorem verification.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=False,indent=2))
    if failure:raise SystemExit(1)
