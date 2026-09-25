import ast, json, sys, traceback
from fractions import Fraction
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path.cwd()/'scripts'))
from _gapn2_jacobian_probe import jac_fd,jacobian_cross_blocks,sym_antisym_decomp,symmetric_root
from _gapn2_symmetry_recon import Recon,roots_of,eigfun
from _gapn2_jacobian_spectral import analytic_jacobian_spectral
from _gapn2_jacobian_analytic import eigen_data
records=[]
def require(ok,message):
    if not bool(ok): raise RuntimeError(message)
def case(name,body):
    try:
        detail=body()
        records.append({'name':name,'passed':True,'details':detail})
    except Exception as exc:
        records.append({'name':name,'passed':False,'error':repr(exc),'traceback':traceback.format_exc()})
def rejected(fn):
    try: fn()
    except (ValueError,ArithmeticError) as exc: return type(exc).__name__+': '+str(exc)
    raise RuntimeError('unexpected acceptance')
def maximum(x): return float(np.max(np.abs(x)))
def basis(n):
    s=np.zeros((2*n,2*n))
    for k in range(n):
        s[k,k]=s[k,-k-1]=1; s[n+k,k]=1; s[n+k,-k-1]=-1
    return s
rng=np.random.default_rng(202609260917)
for n in (1,2,3,5):
    def blocks_case(n=n):
        s=basis(n); c=rng.integers(-6,7,(n,n)).astype(float); d=rng.integers(-6,7,(n,n)).astype(float)
        matrix=np.block([[np.zeros((n,n)),c],[d,np.zeros((n,n))]])
        j=(s.T/2)@matrix@s; original=j.copy(); p=np.eye(2*n)[::-1]
        a,b,e=jacobian_cross_blocks(j,n,rtol=0,atol=0,return_diagnostics=True)
        require(np.array_equal(a,c) and np.array_equal(b,d),'C/D ordering')
        require(np.array_equal(sym_antisym_decomp(j,n)[0],c) and np.array_equal(sym_antisym_decomp(j,n)[1],d),'compatibility')
        require(np.array_equal(j@p,-p@j),'anticommutator')
        u=rng.normal(size=n); v=rng.normal(size=n)
        odd=(s.T/2)@np.r_[np.zeros(n),u]; even=(s.T/2)@np.r_[v,np.zeros(n)]
        require(np.allclose(-p@odd,odd) and np.allclose(-p@even,-even),'physical reflection parity')
        require(np.allclose(s@j@odd,np.r_[c@u,np.zeros(n)]) and np.allclose(s@j@even,np.r_[np.zeros(n),d@v]),'input/output maps')
        signed=(-1)**n*np.linalg.det(c)*np.linalg.det(d); det=np.linalg.det(j)
        require(np.isclose(det,signed,rtol=1e-12,atol=1e-8),'odd-n determinant sign')
        a.fill(99); b.fill(-99); require(np.array_equal(j,original),'input/output alias')
        return {'n':n,'detJ':float(det),'signed_product':float(signed),'J_is_symmetric':bool(np.allclose(j,j.T)),'diagnostics':e}
    case('general cross blocks n='+str(n),blocks_case)
case('singular zero cross blocks are allowed',lambda: {'C':jacobian_cross_blocks(np.zeros((6,6)),3)[0].tolist()})
base=np.diag([1.,2.,-2.,-1.])
for name,fn in [
    ('commuting identity',lambda:jacobian_cross_blocks(np.eye(4),2)),
    ('generic incompatible nonsymmetric matrix',lambda:jacobian_cross_blocks(np.arange(16).reshape(4,4),2)),
    ('anticommutator guard below diagonal limit',lambda:jacobian_cross_blocks(base+0.75e-4*np.eye(4),2,rtol=0,atol=1e-4)),
    ('arithmetic overflow',lambda:jacobian_cross_blocks(np.full((4,4),np.finfo(float).max),2))]:
    case('reject '+name,lambda fn=fn:rejected(fn))
def tolerated():
    c,d,e=jacobian_cross_blocks(base+0.4e-4*np.eye(4),2,rtol=0,atol=1e-4,return_diagnostics=True)
    require(e['anticommutator_max']>0 and e['diagonal_block_max']>0 and not e['certified'],'approximate acceptance must disclose residuals')
    return e
case('subtolerance acceptance is only a diagnostic',tolerated)
for n in (0,-1,True,2.,np.bool_(False)):
    case('invalid n '+repr(n),lambda n=n:rejected(lambda:jacobian_cross_blocks(base,n)))
for j in (np.zeros((4,3)),np.full((4,4),np.nan),np.full((4,4),np.inf),base.astype(complex),base.astype(str),base.astype(bool),base.astype(object)):
    case('invalid matrix '+str(j.dtype)+' '+str(j.shape),lambda j=j:rejected(lambda:jacobian_cross_blocks(j,2)))
for key in ('rtol','atol'):
    for val in (-1.,np.nan,np.inf,True,1j):
        case('invalid '+key+' '+repr(val),lambda key=key,val=val:rejected(lambda:jacobian_cross_blocks(base,2,**{key:val})))
case('invalid block diagnostics flag',lambda:rejected(lambda:jacobian_cross_blocks(base,2,return_diagnostics='yes')))

class Transparent:
    def __init__(self,n=2): self.n=n; self.observed=[]
    def z_to_widths(self,z): return np.array(z,copy=True)
    def widths_to_z(self,w): return np.array(w,copy=True)
    def residual(self,z):
        x=np.cumsum(self.z_to_widths(z))[:-1]; self.observed.append(x.copy()); return x.copy()
def validate_geometry(e,observed):
    x=np.array(e['base_edges']); m=len(x); require(len(observed)==2*m,'exactly two residual evaluations per column')
    for k,col in enumerate(e['columns']):
        hp=col['used_step']; target=np.eye(m)[k]*hp; budget=col['geometry_error_budget']
        for sign,label,index in ((1,'plus_edges',2*k),(-1,'minus_edges',2*k+1)):
            endpoint=np.array(col[label]); require(np.array_equal(endpoint,observed[index]),'reported endpoint differs from evaluated geometry')
            require(np.min(np.diff(np.r_[0,endpoint,1]))>0,'infeasible endpoint')
            require(maximum(endpoint-x-sign*target)<=budget,'off-axis or wrong-sized motion')
            require(sign*(endpoint[k]-x[k])>0,'endpoint collapsed')
    return {'columns':m,'observed_residual_calls':len(observed),'max_backtracks':max(c['backtracks'] for c in e['columns'])}
for n in (1,2,3):
    def coupled(n=n):
        m=2*n; a=rng.normal(size=(m,m)); b=rng.normal(size=(m,m)); v=rng.normal(size=m)
        class Nonlinear(Transparent):
            def residual(self,z):
                x=np.cumsum(self.z_to_widths(z))[:-1]; self.observed.append(x.copy())
                return np.sin(b@x)+a@(x*x)+v*np.prod(x)
        rc=Nonlinear(n); w=rng.dirichlet(np.full(m+1,4.)); snapshot=w.copy(); x=np.cumsum(w)[:-1]
        exact=np.cos(b@x)[:,None]*b+2*a*x[None,:]+v[:,None]*np.prod(x)/x[None,:]
        result,e=jac_fd(rc,w,return_diagnostics=True); err=maximum(result-exact)
        require(err<1e-7,'nonlinear full Jacobian error'); require(np.array_equal(w,snapshot),'input mutation')
        geometry=validate_geometry(e,rc.observed)
        default=jac_fd(rc,w); require(isinstance(default,np.ndarray) and default.shape==(m,m),'legacy matrix API')
        return {'error':err,'geometry':geometry}
    case('coupled nonlinear full edge derivative n='+str(n),coupled)

w0=np.array([.125,.25,.25,.25,.125]); x0=np.cumsum(w0)[:-1]
class CopyMutator(Transparent):
    def z_to_widths(self,z):
        saved=z.copy(); z[:]=np.nan; return saved
    def widths_to_z(self,w):
        saved=w.copy(); w[:]=np.nan; return saved
    def residual(self,z):
        out=super().residual(z); z[:]=np.nan; return out

def protected():
    w=w0.copy(); rc=CopyMutator(); result,e=jac_fd(rc,w,return_diagnostics=True)
    require(np.array_equal(w,w0),'callback modified caller input'); require(maximum(result-np.eye(4))<1e-9,'copy protection derivative')
    return validate_geometry(e,rc.observed)
case('callback arguments and caller input remain isolated',protected)
for h in (0.,-1.,np.inf,np.nan,True,1j,'1e-6',1e-30,64*np.finfo(float).eps):
    case('invalid or unresolvable FD h '+repr(h),lambda h=h:rejected(lambda:jac_fd(Transparent(),w0,h)))
for z in (np.zeros(4),np.r_[np.nan,w0[1:]],w0.astype(complex),w0.astype(str),w0.astype(bool)):
    case('invalid FD parameter '+str(z.dtype)+' '+str(z.shape),lambda z=z:rejected(lambda:jac_fd(Transparent(),z)))
for n in (0,-1,True,2.):
    case('invalid FD n '+repr(n),lambda n=n:rejected(lambda:jac_fd(Transparent(n),w0)))
case('invalid FD diagnostics flag',lambda:rejected(lambda:jac_fd(Transparent(),w0,return_diagnostics=1)))
for w in (np.array([.1,.2,.3,.2,.3]),np.array([.1,0.,.3,.2,.4]),np.array([.1,-.1,.3,.2,.5]),np.full(5,np.nan),np.array([.25,1e-16,.25,.25,.25-1e-16])):
    case('malformed/infeasible/unresolved base '+repr(w.tolist()),lambda w=w:rejected(lambda:jac_fd(Transparent(),w)))
for val in (np.zeros(3),np.zeros((4,1)),np.full(4,np.nan),np.full(4,np.inf),np.ones(4,dtype=complex),np.ones(4,dtype=bool),np.array(['1']*4)):
    def badres(val=val):
        rc=Transparent(); rc.residual=lambda z: val
        return rejected(lambda:jac_fd(rc,w0))
    case('malformed residual '+str(val.dtype)+' '+str(val.shape),badres)
for val in (np.zeros(4),np.full(5,np.inf),np.ones(5,dtype=complex),np.ones(5,dtype=bool),np.array(['1']*5)):
    def badconvert(val=val):
        rc=Transparent(); rc.widths_to_z=lambda w:val
        return rejected(lambda:jac_fd(rc,w0))
    case('malformed converter '+str(val.dtype)+' '+str(val.shape),badconvert)
class BadBase(Transparent):
    def widths_to_z(self,w): w[0]+=1e-4; w[-1]-=1e-4; return w
case('reject converter drift at base',lambda:rejected(lambda:jac_fd(BadBase(),w0)))
class EndpointDrift(Transparent):
    def widths_to_z(self,w):
        x=np.cumsum(w)[:-1]; x[0]+=0.5*(x[1]-x0[1]); return np.diff(np.r_[0,x,1])
case('reject off-axis drift with unchanged base',lambda:rejected(lambda:jac_fd(EndpointDrift(),w0)))
class EndpointCollapse(Transparent):
    def widths_to_z(self,w): return w0.copy()
case('reject collapsed endpoints',lambda:rejected(lambda:jac_fd(EndpointCollapse(),w0)))
class EndpointInfeasible(Transparent):
    def widths_to_z(self,w):
        if not np.array_equal(w,w0): w[0]=-1.; w[-1]+=1.125
        return w
case('reject infeasible converted endpoints',lambda:rejected(lambda:jac_fd(EndpointInfeasible(),w0)))
class OversizedResidual(Transparent):
    def residual(self,z): return np.full(4,np.finfo(float).max if z[0]>w0[0] else -np.finfo(float).max)
case('reject FD subtraction overflow',lambda:rejected(lambda:jac_fd(OversizedResidual(),w0)))
class LimitedConverter(Transparent):
    def widths_to_z(self,w):
        if maximum(np.cumsum(w)[:-1]-x0)>2**-17: raise ValueError('converter local chart too large')
        return w

def adaptive():
    rc=LimitedConverter(); j,e=jac_fd(rc,w0,h=2**-12,return_diagnostics=True)
    require(maximum(j-np.eye(4))==0,'adapted identity derivative')
    require(all(c['backtracks']==5 for c in e['columns']),'expected bounded halving')
    return {'geometry':e,'observed':validate_geometry(e,rc.observed)}
case('successful converter-triggered bounded backtracking',adaptive)
def huge_step():
    rc=Transparent(); j,e=jac_fd(rc,w0,h=1e100,return_diagnostics=True)
    require(maximum(j-np.eye(4))<1e-12,'local width adaptation')
    return validate_geometry(e,rc.observed)
case('huge finite requested step adapts to local widths',huge_step)

# Independent exact R=1 calculation: normalized u_k=sqrt(2)*sin(k*pi*x).
def exact_j(x,n):
    return np.diag(2*np.pi*n**3/(n+1)**2*np.sin(2*n*np.pi*x)-2*np.pi*(n+1)*np.sin(2*(n+1)*np.pi*x))
class R1Analytic(Recon):
    def residual(self,z):
        x=np.cumsum(self.z_to_widths(z))[:-1]; n=self.n
        return 2*((n/(n+1))**2*np.sin(n*np.pi*x)**2-np.sin((n+1)*np.pi*x)**2)
oldpath=Path('before-jacobian.py'); tree=ast.parse(oldpath.read_text()); old={'np':np}
exec(compile(ast.Module(body=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ('jac_fd','sym_antisym_decomp')],type_ignores=[]),str(oldpath),'exec'),old)
def narrow():
    x=np.array([.25,.2500003,.7499997,.75]); rc=R1Analytic(2,1.,'sup'); w=np.diff(np.r_[0,x,1]); z=rc.widths_to_z(w)
    prior=old['jac_fd'](rc,z); fixed,e=jac_fd(rc,z,return_diagnostics=True); actual=jac_fd(Recon(2,1.,'sup'),z)
    expected=exact_j(x,2); olderr=maximum(prior-expected); newerr=maximum(fixed-expected); actualerr=maximum(actual-expected)
    require(olderr>6 and newerr<1e-5 and actualerr<1e-5,'narrow-block errors')
    minus=w.copy(); minus[1]-=1e-6; minus[-1]+=1e-6
    wrongedge=np.cumsum(rc.z_to_widths(rc.widths_to_z(minus)))[0]
    require(abs(wrongedge-.25/(1+9e-7))<1e-15,'old off-axis clipping mechanism')
    return {'old_error':olderr,'new_analytic_error':newerr,'new_actual_error':actualerr,'old_first_edge_after_clipping':float(wrongedge),'geometry':e}
case('independent old narrow-block reproduction and actual R1 repair',narrow)
def radical():
    prod=Fraction(40960,81)**2*Fraction(1,16)*Fraction(65,144)**3
    require(prod==Fraction(7030400000,4782969),'exact rational determinant factor')
    t=np.array([(11+2*np.sqrt(10))/36,(11-2*np.sqrt(10))/36]); left=np.arccos(np.sqrt(t))/np.pi; x=np.r_[left,1-left[::-1]]
    j=exact_j(x,2); c,d=jacobian_cross_blocks(j,2); a,b=old['sym_antisym_decomp'](j,2)
    require(max(maximum(a),maximum(b))<1e-12,'old extracted diagonal zero')
    require(abs(np.linalg.det(j)/(float(prod)*np.pi**4)-1)<1e-12,'radical determinant')
    return {'rational_factor':str(prod),'detJ':float(np.linalg.det(j)),'old_diagonal_max':max(maximum(a),maximum(b))}
case('exact algebraic n2 R1 determinant factor',radical)
for n in (1,3):
    def arbitrary_r1(n=n):
        rc=Recon(n,1.,'inf'); w=rng.dirichlet(np.full(2*n+1,5.)); z=rc.widths_to_z(w); x=np.cumsum(rc.z_to_widths(z))[:-1]
        error=maximum(jac_fd(rc,z)-exact_j(x,n)); require(error<1e-5,'R1 analytic derivative')
        return {'max_error':error,'edges':x.tolist()}
    case('actual asymmetric R1 analytic derivative n='+str(n),arbitrary_r1)

def raw_residual(rc,x):
    blocks=list(zip(np.diff(np.r_[0.,x,1.]),rc.pat)); roots=roots_of(blocks,rc.n+1)
    low=roots[rc.n-1]**2; high=roots[rc.n]**2
    return low/high*eigfun(blocks,roots[rc.n-1],x)**2-eigfun(blocks,roots[rc.n],x)**2
for n in (1,2,3):
    def rawfull(n=n):
        rc=Recon(n,4.,'sup'); w=rng.dirichlet(np.full(2*n+1,5.)); z=rc.widths_to_z(w); x=np.cumsum(rc.z_to_widths(z))[:-1]
        j=jac_fd(rc,z); step=5e-7; independent=np.column_stack([(raw_residual(rc,x+step*v)-raw_residual(rc,x-step*v))/(2*step) for v in np.eye(2*n)])
        error=maximum(j-independent); require(error<5e-5,'full raw-edge derivative disagreement')
        reflection=maximum(raw_residual(rc,1-x[::-1])-raw_residual(rc,x)[::-1]); require(reflection<1e-10,'physical equivariance')
        return {'max_jacobian_error':error,'reflection_residual':reflection,'nonzero_residual':maximum(rc.residual(z)),'edges':x.tolist()}
    case('arbitrary off-root R4 raw full Jacobian n='+str(n),rawfull)
def symmetric_noncritical():
    rc=Recon(2,4.,'sup'); w=w0.copy(); z=rc.widths_to_z(w); j=jac_fd(rc,z); c,d,e=jacobian_cross_blocks(j,2,return_diagnostics=True)
    residual=maximum(rc.residual(z)); require(residual>1e-3,'noncritical witness')
    return {'residual':residual,'sector_diagnostics':e}
case('anticommutation does not require stationarity',symmetric_noncritical)

# Compare finite retained-mode Jacobians at numerical stationary points.
table=json.loads(Path('scripts/op03_gap_table.json').read_text())
for n in (2,3):
    for mode in ('sup','inf'):
        def compare(n=n,mode=mode):
            rc=Recon(n,4.,mode); seed=rc.widths_to_z(np.diff(np.r_[0,table[f'n{n}_{mode.upper()}']['edges'],1])); z=symmetric_root(rc,seed)
            require(z is not None,'root unavailable'); residual=maximum(rc.residual(z)); jd,geo=jac_fd(rc,z,return_diagnostics=True)
            ed=eigen_data(rc,z); s=np.diff(rc.pat); lp=ed['lam_np1']; vals=[]
            for cutoff in (80,160,320):
                js=analytic_jacobian_spectral(rc,z,N=cutoff); c,d,sec=jacobian_cross_blocks(js,n,return_diagnostics=True)
                k=lp*np.diag(1/s)@js; h=(-lp*np.diag(s))@js
                require(maximum(h+(4-1)**2*k)<1e-9,'K/H scaling'); require(maximum(k-k.T)<1e-9,'stationary K symmetry')
                vals.append({'N':cutoff,'retained_modes':cutoff+1,'error_vs_fd':maximum(js-jd),'detJ':float(np.linalg.det(js)),'detC':float(np.linalg.det(c)),'detD':float(np.linalg.det(d)),'signed_product':float((-1)**n*np.linalg.det(c)*np.linalg.det(d)),'Ksym':maximum(k-k.T),'Hsym':maximum(h-h.T),'sector':sec})
            require(vals[-1]['error_vs_fd']<vals[0]['error_vs_fd'],'sampled spectral refinement does not reduce error')
            return {'n':n,'mode':mode,'root_residual':residual,'fd_detJ':float(np.linalg.det(jd)),'fd_geometry':geo,'cutoffs':vals,'limitation':'finite cutoff comparisons; no tail bound or exact stationarity'}
        case(f'finite spectral comparison n={n}/{mode}',compare)
result={'count':len(records),'passed':sum(r['passed'] for r in records),'failed':sum(not r['passed'] for r in records),'checks':records}
Path('results/independent-checks.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
for r in records:
    if not r['passed']: print(json.dumps(r,indent=2))
raise SystemExit(bool(result['failed']))
