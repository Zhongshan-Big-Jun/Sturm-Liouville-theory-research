import hashlib,json,sys,traceback
from pathlib import Path
import numpy as np
import mpmath as mp
sys.path.insert(0,str(Path.cwd()/'scripts'))
from _gapn2_symmetry_recon import Recon,roots_of,eigfun
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_jacobian_probe import jac_fd
root=Path.cwd().resolve(); records=[]
def req(ok,msg):
    if not bool(ok): raise RuntimeError(msg)
def case(name,fn):
    try: records.append({'name':name,'passed':True,'details':fn()})
    except Exception as e: records.append({'name':name,'passed':False,'error':repr(e),'traceback':traceback.format_exc()})
def maxabs(x): return float(np.max(np.abs(x)))
manifest=json.loads(Path('manifest.json').read_text())
expected={str(root/path):r['sha256'] for path,r in manifest['sources'].items()}

def independent_gap(x,pat,guesses):
    # Independent high-precision transfer solution; narrow secant start around
    # each supplied indexed root. Check root neighborhood as finite evidence.
    widths=[b-a for a,b in zip([mp.mpf(0)]+x,x+[mp.mpf(1)])]
    req(min(widths)>0,'directional gap has infeasible edges')
    def secular(freq):
        y,yp=mp.mpf(0),mp.mpf(1)
        for w,rho in zip(widths,pat):
            omega=freq*mp.sqrt(rho); c=mp.cos(omega*w); s=mp.sin(omega*w)
            y,yp=c*y+s*yp/omega,-omega*s*y+c*yp
        return y
    roots=[]
    for guess in guesses:
        g=mp.mpf(guess); freq=mp.findroot(secular,(g*(1-mp.mpf('1e-6')),g*(1+mp.mpf('1e-6'))),tol=mp.mpf('1e-48'))
        req(abs(freq/g-1)<mp.mpf('0.005') and abs(secular(freq))<mp.mpf('1e-45'),'independent root refinement mismatch')
        roots.append(freq)
    return roots[1]**2-roots[0]**2

def saved_case(mode):
    saved=json.loads(Path(f'results/p3-{mode}.json').read_text()); n=saved['n']; geo=saved['P3_jacobian_fd']; m=2*n
    req(saved['retained_modes']==61 and saved['gauss_order_per_interval']==64 and saved['digits']==60,'nondefault execution')
    req(len(saved['P3'])==3,'incomplete P3 execution')
    for path,digest in saved['source_sha256'].items():
        req(path in expected and digest==expected[path] and hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,'saved source identity mismatch')
    blocks=np.array(saved['blocks']); x=np.cumsum(blocks[:,0])[:-1]; pat=blocks[:,1]; jumps=np.diff(pat); rc=Recon(n,saved['R'],mode)
    req(np.array_equal(x,np.array(geo['base_edges'])),'saved base geometry mismatch')
    req(maxabs(np.array(saved['edges'])[1:-1]-x)==0,'saved internal edges mismatch')
    def raw(x):
        blocks=list(zip(np.diff(np.r_[0,x,1]),pat)); roots=roots_of(blocks,n+1)
        return (roots[n-1]**2*eigfun(blocks,roots[n-1],x)**2-roots[n]**2*eigfun(blocks,roots[n],x)**2)/roots[n]**2
    rebuilt=[]; maxmotion=0.
    for k,col in enumerate(geo['columns']):
        xp=np.array(col['plus_edges']); xm=np.array(col['minus_edges']); step=col['used_step']; target=np.eye(m)[k]*step
        req(min(np.diff(np.r_[0,xp,1]))>0 and min(np.diff(np.r_[0,xm,1]))>0,'nonpositive saved endpoint width')
        movement=max(maxabs(xp-x-target),maxabs(xm-x+target)); maxmotion=max(maxmotion,movement)
        req(movement<=col['geometry_error_budget'],'saved movement budget exceeded')
        req(0<step<=geo['requested_step'] and xp[k]>x[k]>xm[k],'unresolved saved motion')
        rebuilt.append((raw(xp)-raw(xm))/(2*step))
    j=np.column_stack(rebuilt); z=rc.widths_to_z(blocks[:,0]); ed=eigen_data(rc,z); lam=ed['lam_np1']
    # Literal row weighting is equivalent to left diagonal matrix product;
    # compare against the saved quadratic values, never elementwise diag*J.
    h=-lam*jumps[:,None]*j
    p=np.eye(m)[::-1]; require_commute=maxabs(p@h-h@p)
    req(require_commute<1e-4,'stationary H does not commute numerically')
    f=raw(x); gradlam=lam*jumps*ed['u_np1']**2
    missing=-np.outer(jumps*f,gradlam)
    stationarity=maxabs(f)
    req(stationarity<1e-8,'stationary root residual failed')
    req(abs(stationarity-saved['stationary_residual_max'])<1e-12,'saved root residual not reproducible')
    row_checks=[]
    with mp.workdps(60):
        xmp=[mp.mpf(float(v)) for v in x]; guesses=[mp.sqrt(saved['lambda_n']),mp.sqrt(saved['lambda_np1'])]
        g0=independent_gap(xmp,pat,guesses)
        for row in saved['P3']:
            d=np.array(row['displacement']); quadratic=float(d@h@d/2)
            req(abs(quadratic-row['Q_interface_hessian_fd'])<1e-4,'saved P3 quadratic form does not match raw-edge J')
            req(np.sign(quadratic)==(-1 if mode=='sup' else 1),'unexpected P3 interface sign')
            fp=2*ed['lam_n']*ed['u_n']*ed['up_n']-2*lam*ed['u_np1']*ed['up_np1']
            accel=float(-np.sum(jumps*d*d*fp)/2)
            req(abs(accel-row['half_interface_acceleration'])<1e-6,'P3 acceleration sign/formula')
            recomputed_difference=quadratic-(row['Q_linear_fixed_bump']+accel)
            req(abs(recomputed_difference-row['finite_comparison_difference'])<1e-4,'P3 finite-comparison identity')
            finite=[]; dmp=[mp.mpf(float(v)) for v in d]
            for step in (mp.mpf('0.00002'),mp.mpf('0.00001')):
                plus=independent_gap([a+step*b for a,b in zip(xmp,dmp)],pat,guesses)
                minus=independent_gap([a-step*b for a,b in zip(xmp,dmp)],pat,guesses)
                q=float((plus-2*g0+minus)/(2*step**2))
                finite.append({'h':float(step),'Q_half_second':q,'error_vs_saved':q-row['Q_interface_hessian_fd']})
            req(abs(finite[-1]['error_vs_saved'])<max(1e-4,abs(quadratic)*2e-6),'independent high-precision edge path differs from saved Hessian')
            row_checks.append({'t':row['t'],'Q_saved':row['Q_interface_hessian_fd'],'Q_from_saved_geometry':quadratic,'acceleration':accel,'missing_nonstationary_quadratic':float(d@missing@d/2),'direct_gap_finite_steps':finite})
    return {'mode':mode,'saved_source_count':len(saved['source_sha256']),'root_residual':stationarity,'geometry_max_motion_error':maxmotion,'H_commutator_max':require_commute,'H_symmetry_max':maxabs(h-h.T),'nonstationary_rank_one_term_max':maxabs(missing),'P3':row_checks}
for mode in ('sup','inf'): case('saved P3 geometry, source identities, matrix product and physical edge path '+mode,lambda mode=mode:saved_case(mode))

def r1_degenerate():
    rc=Recon(2,1.,'sup'); x=np.array([.125,.375,.625,.875]); z=rc.widths_to_z(np.diff(np.r_[0,x,1])); j=jac_fd(rc,z); ed=eigen_data(rc,z); jumps=np.diff(rc.pat)
    h=-ed['lam_np1']*jumps[:,None]*j
    req(maxabs(jumps)==0 and maxabs(h)==0,'R1 Hessian not zero')
    return {'all_density_jumps':jumps.tolist(),'gap':ed['lam_np1']-ed['lam_n'],'Hessian_max':maxabs(h),'K_division_by_jumps':'undefined at R=1; not evaluated'}
case('R1 residual Jacobian can be nonzero while gap Hessian vanishes',r1_degenerate)

def identities():
    summary=[]
    for label in ('author-normal','author-optimized','jacobian-cli','o3-cli','p3-sup','p3-inf','independent'):
        execution=json.loads(Path(f'results/{label}.execution.json').read_text()); modules=json.loads(Path(f'results/{label}.modules.json').read_text())
        req(execution['returncode']==0 and execution['sources_unchanged'] and modules['all_match'],'execution provenance failed')
        for row in modules['modules']: req(row['origin'] in expected and row['sha256']==expected[row['origin']],'unexpected module origin/hash')
        summary.append({'label':label,'argv':execution['argv'],'cwd':execution['cwd'],'modules':modules['modules'],'returncode':execution['returncode']})
    return summary
case('every recorded loaded project module matches the frozen private source',identities)

result={'count':len(records),'passed':sum(r['passed'] for r in records),'failed':sum(not r['passed'] for r in records),'checks':records}
Path('results/saved-results-verification.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
for record in records:
    if not record['passed']: print(json.dumps(record,indent=2))
raise SystemExit(bool(result['failed']))
