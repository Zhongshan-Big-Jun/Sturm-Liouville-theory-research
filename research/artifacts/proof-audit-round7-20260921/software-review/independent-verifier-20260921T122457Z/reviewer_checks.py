"""Independent local probes: augmented IVP norm oracle and asymmetric n=2 derivatives."""
from pathlib import Path
import ast,hashlib,importlib,json,os,sys,traceback
import numpy as np
import scipy
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent.parent
OWN=Path(__file__).resolve().parent
SCRIPTS=ROOT/'candidates/scripts'
os.chdir(ROOT/'candidates')
sys.path.insert(0,str(SCRIPTS))
fixed=importlib.import_module('op03_gap_fixed')
legacy=importlib.import_module('op03_gap_precise')
recon=importlib.import_module('_gapn2_symmetry_recon')
probe=importlib.import_module('_gapn2_jacobian_probe')
analytic=importlib.import_module('_gapn2_jacobian_analytic')
hesssign=importlib.import_module('_gapn2_hess_sign_and_bigR')
hessverify=importlib.import_module('_gapn2_hess_verify')
rows=[];fixtures=[];expressions=[]
def serial(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    if isinstance(v,dict):return {k:serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [serial(x) for x in v]
    return v
def record(name,passed,**detail):
    rows.append(serial(dict(name=name,passed=bool(passed),**detail)))
    print(('PASS ' if passed else 'FAIL ')+name,flush=True)
def close(name,a,b,atol=3e-5,rtol=3e-6,**detail):
    a=np.asarray(a);b=np.asarray(b)
    ok=a.shape==b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.allclose(a,b,atol=atol,rtol=rtol)
    record(name,ok,actual=a,expected=b,max_abs_error=float(np.max(np.abs(a-b))),atol=atol,rtol=rtol,**detail)
def ode(blocks,lam,points):
    # Integrate norm as a third state, separately from the supplied IVP+quad helper.
    state=np.array([0.,1.,0.]);start=0.;ends=[];solutions=[]
    for width,rho in blocks:
        end=start+width
        def rhs(t,y):return [y[1],-lam*rho*y[0],rho*y[0]**2]
        sol=solve_ivp(rhs,[start,end],state,method='DOP853',rtol=4e-12,atol=3e-14,dense_output=True)
        if not sol.success:raise RuntimeError(sol.message)
        state=sol.y[:,-1];ends.append(end);solutions.append(sol.sol);start=end
    vals=np.array([solutions[min(int(np.searchsorted(ends,t,side='left')),len(blocks)-1)](t)[0] for t in points])
    return vals/np.sqrt(state[2]),state[0],state[2]
def grad(fun,x,h=1e-5):
    return np.array([(fun(x+h*d)-fun(x-h*d))/(2*h) for d in np.eye(len(x))])
def hessian(fun,x,h):
    m=len(x);eye=np.eye(m);out=np.zeros((m,m));base=fun(x)
    for i in range(m):
        out[i,i]=(fun(x+h*eye[i])-2*base+fun(x-h*eye[i]))/(h*h)
        for j in range(i):
            ei=h*eye[i];ej=h*eye[j]
            out[i,j]=out[j,i]=(fun(x+ei+ej)-fun(x+ei-ej)-fun(x-ei+ej)+fun(x-ei-ej))/(4*h*h)
    return out
def actual_assignment(tree,name,target,bindings):
    path=ROOT/tree/'scripts'/name
    source=ast.parse(path.read_text(encoding='utf-8-sig'))
    main=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    nodes=[n.value for n in ast.walk(main) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==target for t in n.targets)]
    if len(nodes)!=1:raise RuntimeError('ambiguous source expression')
    node=nodes[0]
    expressions.append({'path':str(path.relative_to(ROOT)),'line':node.lineno,'target':target,'expression':ast.unparse(node),'ast_sha256':hashlib.sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()})
    return eval(compile(ast.Expression(node),str(path),'eval'),{'np':np,**bindings})
try:
    backend_fixtures=[('symmetric SUP',[(.3,1.),(.4,4.),(.3,1.)]),('asymmetric SUP',[(.23,1.),(.36,4.),(.41,1.)]),('asymmetric INF',[(.23,4.),(.36,1.),(.41,4.)])]
    for label,blocks in backend_fixtures:
        points=np.unique(np.r_[0.,.11,.23,.4,.59,.73,.91,1.,np.cumsum([w for w,_ in blocks])])
        roots=fixed.lams_precise(blocks,2)
        refs=[];ode_roots=[];endpoints=[]
        for s in roots:
            values,endpoint,norm=ode(blocks,s*s,points);refs.append(values);endpoints.append(endpoint/np.sqrt(norm))
            r=brentq(lambda t:ode(blocks,t*t,[])[1],s*.98,s*1.02,xtol=2e-12,rtol=1e-13)
            ode_roots.append(r)
        vals=fixed.eigfuns_precise(blocks,roots,points)
        close('fixed '+label+'/augmented IVP values',vals,refs,atol=3e-8,rtol=3e-8)
        close('fixed '+label+'/IVP shooting roots',roots,ode_roots,atol=2e-10,rtol=2e-10)
        close('fixed '+label+'/Dirichlet endpoint',endpoints,np.zeros(2),atol=3e-8)
        oldroots=legacy.lams_precise(blocks,2)
        oldvals=legacy.eigfuns_precise(blocks,oldroots,points)
        starts=np.r_[0.,np.cumsum([w for w,_ in blocks])]
        masses={}
        for mod in (fixed,legacy):
            masses[mod.__name__]=[sum(rho*quad(lambda t:mod.eigfuns_precise(blocks,np.array([s]),np.array([t]))[0,0]**2,starts[i],starts[i+1],epsabs=1e-11,epsrel=1e-11)[0] for i,(_,rho) in enumerate(blocks)) for s in roots]
        close('fixed '+label+'/actual weighted mass',masses['op03_gap_fixed'],np.ones(2),atol=3e-9,rtol=3e-9)
        close('legacy '+label+'/low roots still agree',oldroots,ode_roots,atol=2e-10,rtol=2e-10)
        record('legacy '+label+'/weighted normalization defect',np.max(np.abs(np.array(masses['op03_gap_precise'])-1))>1e-3,weighted_mass=masses['op03_gap_precise'],max_normalized_value_error=float(np.max(np.abs(oldvals-np.array(refs)))))
        close('legacy '+label+'/normalization-only diagnosis',oldvals/np.sqrt(np.asarray(masses['op03_gap_precise']))[:,None],refs,atol=3e-8,rtol=3e-8)
        fixtures.append(serial(dict(label=label,blocks=blocks,points=points,roots=roots,ivp_shooting_roots=ode_roots,weighted_mass=masses)))
    # Isolate the paired coefficient omission from the normalization defect.
    blocks=[(.3,1.),(.4,4.),(.3,1.)]
    s=fixed.lams_precise(blocks,2);lam=s*s
    vals=fixed.eigfuns_precise(blocks,s,np.array([.3]))[:,0]
    oldvals=legacy.eigfuns_precise(blocks,s,np.array([.3]))[:,0]
    truef=lam[0]*vals[0]**2-lam[1]*vals[1]**2
    oldf=lam[0]*oldvals[0]**2-lam[1]*oldvals[1]**2
    target=-6*truef
    record('op03 independent separation of two original defects',abs(-3*truef-target)>1 and abs(-6*oldf-target)>1,true_paired_derivative=target,correct_norm_but_old_half_factor=-3*truef,correct_paired_factor_but_legacy_norm=-6*oldf,actual_old_two_fault_prediction=-3*oldf)
    # Independent four-interface nonstationary checks, no table or stationary solver.
    for mode in ('sup','inf'):
        rc=recon.Recon(2,4.,mode);edges=np.array([.18,.36,.62,.83]);jumps=np.diff(rc.pat)
        def blocks_at(x):return list(zip(np.diff(np.r_[0.,x,1.]),rc.pat))
        def spectral(x):
            b=blocks_at(x);s=recon.roots_of(b,3);lam=s*s
            u=np.array([recon.eigfun(b,t,x) for t in s[1:3]])
            f=lam[1]*u[0]**2-lam[2]*u[1]**2
            return lam[2]-lam[1],f/lam[2],lam[2],u
        def gap(x):return spectral(x)[0]
        z=rc.widths_to_z(np.diff(np.r_[0.,edges,1.]));ed=analytic.eigen_data(rc,z)
        d,F,lam,u=spectral(edges)
        fj=grad(lambda x:spectral(x)[1],edges,1e-6).T
        supplied_j=probe.jac_fd(rc,z,h=1e-6)
        close('n2 '+mode+'/width-to-interface J',supplied_j,fj,atol=2e-6,rtol=1e-6)
        f=actual_assignment('candidates','_gapn2_hess_verify.py','f',{'ed':ed,'lam':lam})
        oldf=actual_assignment('originals','_gapn2_hess_verify.py','f',{'ed':ed,'lam':lam})
        independent_u=[]
        for ll in (ed['lam_n'],ed['lam_np1']):independent_u.append(ode(blocks_at(edges),ll,edges)[0])
        correctf=ed['lam_n']*independent_u[0]**2-lam*independent_u[1]**2
        close('n2 '+mode+'/lambda_n weighting with IVP eigenfunctions',f,correctf,atol=2e-7,rtol=2e-8)
        record('n2 '+mode+'/actual original lower-weight error exposed',np.max(np.abs(oldf-correctf))>1,original=oldf,ivp_expected=correctf,max_abs_error=np.max(np.abs(oldf-correctf)))
        g=-jumps*f
        close('n2 '+mode+'/unpaired gradient',g,grad(gap,edges,1e-5),atol=2e-4,rtol=3e-6)
        record('n2 '+mode+'/nonstationary premise',np.max(np.abs(F))>.01,F=F)
        glambda=lam*jumps*u[1]**2
        full=-np.diag(jumps)@(lam*fj+np.outer(F,glambda))
        simple=-lam*np.diag(jumps)@fj
        hd=hessian(gap,edges,1e-4);hd2=hessian(gap,edges,5e-5)
        close('n2 '+mode+'/independent Hessian step convergence',hd,hd2,atol=.02,rtol=8e-5)
        close('n2 '+mode+'/nonstationary full Hessian',full,hd2,atol=.02,rtol=8e-5)
        close('n2 '+mode+'/full Hessian symmetry',full,full.T,atol=2e-5,rtol=2e-7)
        record('n2 '+mode+'/stationary-only expression rejected',np.max(np.abs(simple-hd2))>1,simple_error=np.max(np.abs(simple-hd2)),rank_one_correction=full-simple)
        close('n2 '+mode+'/width-to-interface H',hesssign.hess_fd(rc,z,h=5e-5),hd2,atol=.02,rtol=8e-5)
        B=np.eye(4)[:,:2]-np.eye(4)[:,::-1][:,:2]
        close('n2 '+mode+'/paired gradient',B.T@g,grad(lambda q:gap(edges+B@q),np.zeros(2)),atol=2e-4,rtol=3e-6)
        close('n2 '+mode+'/paired Hessian',B.T@full@B,hessian(lambda q:gap(edges+B@q),np.zeros(2),5e-5),atol=.04,rtol=8e-5)
        fixtures.append(serial(dict(label='n2 nonstationary '+mode,edges=edges,pattern=rc.pat,F=F,gradient=g,full_hessian=full,fd_hessian=hd2)))
except Exception:
    record('execution exception',False,traceback=traceback.format_exc())
    traceback.print_exc()
# Full module inventory (no prefilter to the packet), for this supplemental process.
modules={name:str(Path(mod.__file__).resolve()) for name,mod in list(sys.modules.items()) if getattr(mod,'__file__',None)}
project_names=['op03_gap_fixed','op03_gap_precise','_gapn2_symmetry_recon','_gapn2_jacobian_probe','_gapn2_jacobian_analytic','_gapn2_hess_sign_and_bigR','_gapn2_hess_verify','_gapn2_hp_scan','_gapn2_jacobian_spectral']
project_bindings={name:modules.get(name) for name in project_names}
record('supplemental actual project import provenance',all(value==str(SCRIPTS/(name+'.py')) for name,value in project_bindings.items()),bindings=project_bindings)
(OWN/'supplemental-import-provenance.json').write_text(json.dumps({'modules':modules,'project_modules':project_bindings,'scope':'This supplemental process only; not retroactive instrumentation of replay.'},indent=2)+'\n')
result={'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'checks':rows,'tests':len(rows),'passed':sum(r['passed'] for r in rows),'failed':sum(not r['passed'] for r in rows),'fixtures':fixtures,'source_expressions':expressions,'oracle':'DOP853 augmented system (y, yprime, integral rho*y^2); independent brentq shooting near the supplied low-root brackets','limits':'Finite positive-width R=4 cases only. Root brackets do not establish global completeness. No historical Jacobian/spectral tail, full scans or global theorems.'}
(OWN/'reviewer-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['tests','passed','failed']}),flush=True)
sys.exit(int(result['failed']!=0))
