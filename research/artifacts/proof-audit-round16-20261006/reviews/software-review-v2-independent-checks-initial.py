"""Independent bounded reviewer checks; frozen inputs remain read-only."""
from pathlib import Path
from fractions import Fraction as F
import ast, hashlib, json, math, os, platform, sys, time, warnings
import numpy as np
import mpmath as mp
ROOT=Path('F:/tools/math-audit-round16-20261006/software-review-v2/root')
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'misc'))
import rigid1d as T
import _gapn2_second_variation_probe as V
import _gapn2_symmetry_recon as P
import _sl_prufer as S
import _sl_spectral_identity as I
import _gapn2_jacobian_spectral as GS
import _gapn2_jacobian_analytic as J
import _gapn2_jacobian_probe as JP
import op03_gap_fixed as OLD
ROWS=[]
def check(name,ok,**data):
    ROWS.append(dict(name=name,passed=bool(ok),**data))
def rejects(name,fn):
    try: fn()
    except (ValueError,TypeError,ArithmeticError) as e: check(name,True,error_type=type(e).__name__,error=str(e))
    else: check(name,False)

def exact_checks():
    for fn in (T.der_sign2,T.der_sign_adaptive):
        opts={'base_n':3,'max_n':3} if fn is T.der_sign2 else {'max_boxes':3}
        for a,b in ((10**400,10**400+1),(0.,math.nextafter(0.,1.)),(math.nextafter(-1.,-2.),-1.)):
            seen=[]
            def cb(z): seen.append((z.v.lo,z.v.hi));return z
            result=fn(cb,a,b,True,**opts)
            check(fn.__name__+' huge/subnormal/negative-adjacent exact coverage '+str(type(a)),result[0] and all(isinstance(x,F) for piece in seen for x in piece) and min(x[0] for x in seen)==F(a) and max(x[1] for x in seen)==F(b))
        rejects(fn.__name__+' nonboolean sign',lambda:fn(lambda z:z,0,1,1))
        rejects(fn.__name__+' noncallable function',lambda:fn(None,0,1,True))
        result=fn(lambda z:T.D2(0),0,1,True,**opts)
        check(fn.__name__+' False is explicitly unproved',result[0] is False and 'unproved' in str(result[1]))
    for value in (False,0,-1,2.5,float('nan')):
        rejects('invalid max_n '+repr(value),lambda value=value:T.der_sign2(lambda z:z,0,1,True,base_n=1,max_n=value))
    seen=[]
    def zero(z):seen.append(z);return T.D2(0)
    result=T.der_sign_adaptive(zero,0,1,True,max_boxes=5)
    check('strict five-box evaluation budget',result[0] is False and len(seen)==10,calls=len(seen),result=str(result))
    e1=ast.parse((ROOT/'misc/e1_certgen.py').read_text(encoding='utf-8-sig'))
    imports=[n for n in ast.walk(e1) if isinstance(n,ast.ImportFrom) and n.module=='rigid1d']
    names={a.name for n in imports for a in n.names}
    calls={n.func.id for n in ast.walk(e1) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
    body=next(n for n in e1.body if isinstance(n,ast.FunctionDef) and n.name=='_taylor')
    first=ast.unparse(body.body[0])
    check('E1 static exact conversion precedes arithmetic',first=='a, b, Target = (F(a), F(b), F(Target))',first_statement=first)
    check('E1 imports/calls no affected generic helpers',not {'der_sign2','der_sign_adaptive'} & (names|calls))

def physical_reference(blocks,root,dps=100):
    with mp.workdps(dps):
        wave=mp.mpf(float(root));y,v=mp.mpf(0),mp.mpf(1);start=mp.mpf(0);parts=[];mass=mp.mpf(0)
        for lf,rf in blocks:
            length,rho=mp.mpf(float(lf)),mp.mpf(float(rf));k=wave*mp.sqrt(rho);a,b=y,v/k
            mass+=rho*mp.quad(lambda x:(a*mp.cos(k*x)+b*mp.sin(k*x))**2,[0,length])
            parts.append((start,length,k,a,b));y=a*mp.cos(k*length)+b*mp.sin(k*length);v=k*(-a*mp.sin(k*length)+b*mp.cos(k*length));start+=length
        norm=mp.sqrt(mass)
    def sample(x):
        i=max(i for i,(s,*_) in enumerate(parts) if s<=x);s,length,k,a,b=parts[i]
        return (a*mp.cos(k*(x-s))+b*mp.sin(k*(x-s)))/norm
    return sample

def average_reference(probe,left,right,i,j,dps):
    with mp.workdps(dps):
        a,b=physical_reference(probe.blocks,probe.roots[i],dps),physical_reference(probe.blocks,probe.roots[j],dps)
        start,width=mp.mpf(float(left)),mp.mpf(float(right))-mp.mpf(float(left))
        return mp.quad(lambda t:a(start+width*t)*b(start+width*t),[0,1])

def nodal_checks():
    cases=[('half-width at exactly dyadic constant anchor',[(1.,1.)],.5,1),('third-mode node at non-dyadic anchor',[(1.,1.)],float(1/3),2),('direction-only node inside broad rho=4 block',[(.25,1.),(.5,4.),(.25,1.)],.5,1)]
    for name,blocks,left,idx in cases:
        probe=V.SpectralProbe(blocks,6,8);right=math.nextafter(left,1.);width=right-left
        _,cu,_,_,info=probe.pairings(V.block_direction([0.,1/width,0.],[0.,left,right,1.]),return_diagnostics=True)
        cross=average_reference(probe,left,right,0,idx,110);square=average_reference(probe,left,right,idx,idx,110)
        with mp.workdps(110):
            check(name+' 90/110-dps reference stable',abs(average_reference(probe,left,right,idx,idx,90)/square-1)<mp.mpf('1e-60'))
        with mp.workdps(110):
            rel=abs(mp.mpf(float(cu[idx,idx]))/square-1);cerr=abs(mp.mpf(float(cu[0,idx]))-cross)
            check(name+' nodal square retains physical IVP',rel<mp.mpf('2e-12'),blocks=blocks,left=left,right=right,width=width,mode=idx+1,same_binary64_frequency=float(probe.roots[idx]),actual=float(cu[idx,idx]),reference=mp.nstr(square,65),relative_error=mp.nstr(rel,35),pairing_status=info['status'])
            check(name+' nodal cross retains physical IVP',cerr<mp.mpf('3e-30'),actual=float(cu[0,idx]),reference=mp.nstr(cross,65),absolute_error=mp.nstr(cerr,35))
        check(name+' direction mass exact from endpoint binary rationals',F(float(1/width))*(F(right)-F(left))==1)
        rejects(name+' ordinary folded nodes rejected',lambda:probe.pairings(lambda x:np.where((x>=left)&(x<right),1/width,0.),(left,right)))

def pairing_checks():
    probe=V.SpectralProbe([(1.,4.)],41,8)
    result=probe.pairings(V.block_direction([-3.],[0.,1.]))
    lam,cu,cw,d=result
    check('non-unit constant rho/h analytic matrix',np.max(np.abs(cu+.75*np.eye(41)))<2e-12 and np.max(np.abs(cw+3*np.eye(41)))<2e-12)
    expected=9*41*math.pi**2/64;q=V.q_formula(lam,cu,cw,20,d)
    check('independent constant-density Q scaling',abs(q-expected)<2e-9,actual=q,expected=expected)
    rejects('ordinary callback modal underresolution budget',lambda:probe.pairings(lambda x:-3*np.ones_like(x),MaxOrder=64))
    check('ordinary modal underresolution explicit status',probe.last_pairing_diagnostics['status']=='UNRESOLVED')
    calls=[]
    def callback(x):calls.append(len(x));return -3*np.ones_like(x)
    default=probe.pairings(callback,MaxOrder=1024)
    info=default.diagnostics
    check('ordinary callback retains two-comparison estimate data',info['status']=='CONVERGED_NUMERICAL_ESTIMATE' and len(info['estimated_absolute_errors'])==4 and calls==[256,512,1024] and info['black_box_error_enclosure'] is None and not info['sign_certified'],diagnostics=info)
    for value in (True,7,8.5):rejects('callback invalid MaxOrder '+repr(value),lambda value=value:probe.pairings(lambda x:np.ones_like(x),MaxOrder=value))
    rejects('callback samples shape mismatch',lambda:probe.pairings(lambda x:np.array([1.])))
    rejects('callback nonfinite samples',lambda:probe.pairings(lambda x:np.full_like(x,float('nan'))))
    for name,blocks,left,right in [('thin density',[(.5,1.),(2.**-50,4.),(.5-2.**-50,1.)],.5,.5+2.**-50),('direction-only thin segment',[(1.,1.)],.3,.3+2.**-50)]:
        p=V.SpectralProbe(blocks,5,8);width=right-left
        _,c,_,_,info=p.pairings(V.block_direction([0.,1/width,0.],[0.,left,right,1.]),return_diagnostics=True)
        reference=average_reference(p,left,right,0,0,100)
        check(name+' independent high-precision mass pairing',abs(mp.mpf(float(c[0,0]))/reference-1)<mp.mpf('2e-12'),actual=float(c[0,0]),reference=mp.nstr(reference,40))
        check(name+' all geometric cuts retained',info['intervals']==3)
    p=V.SpectralProbe([(.25,1.),(.5,4.),(.25,1.)],4,8);left=.6;right=left+2.**-50
    _,c,_,_,info=p.pairings(V.block_direction([0.,1/(right-left),0.],[0.,left,right,1.]),Breaks=(.3,),return_diagnostics=True)
    check('union density/direction/extra cuts exact count',info['intervals']==6,intervals=info['intervals'])
    rejects('unresolvable density endpoint rejected',lambda:V.SpectralProbe([(.5,1.),(2.**-60,2.),(.5,1.)],3,8))
    z=p.pairings(V.block_direction([0.],[0.,1.]));check('zero direction preserves zero raw remainder without sign certificate',z.diagnostics['parseval_remainder_raw']==[0.]*4 and z.diagnostics['sign_certified'] is False)

def preserved_checks():
    blocks=[(.49,1.),(.001,1e6),(.509,1.)]
    prefixes=[OLD.lams_precise(blocks,n) for n in (1,4,7)]
    check('R15 high-contrast indexed prefix stable',prefixes[0][0]==prefixes[1][0]==prefixes[2][0] and np.array_equal(prefixes[1],prefixes[2][:4]))
    rejects('R15 unresolved tol cannot pass',lambda:OLD.lams_precise(blocks,4,tol=1e-20))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always');freq=OLD.lams_precise(blocks,4,smax_scale=8.)
    check('R15 nondefault legacy range warns but preserves indices',len(caught)==1 and np.array_equal(freq,prefixes[1]))
    for boundary in ('D','N'):
        table=I.IndexedSpectrum([(1.,1.)],boundary,5)
        expected=(np.arange(1,6)-(.5 if boundary=='N' else 0))*np.pi
        check(boundary+' constant indexed identity',np.max(np.abs(table.frequency_prefix(5)-expected))<2e-14)
    table=I.IndexedSpectrum([(1.,1.)],'D',5);target=table.eigenvalues[1]
    rejects('reduced wrong pole index rejected',lambda:I.spectral_denominators(table,target,5,PoleMode=1))
    rejects('reduced excluded pole outside prefix rejected',lambda:I.spectral_denominators(table,target,1,PoleMode=2))
    rejects('full target lacks spectral coverage rejected',lambda:I.spectral_denominators(table,table.eigenvalues[-1]+1,5))
    rejects('Green table geometry mismatch rejected',lambda:I.spectrum_for([(.5,1.)],'D',3,table))
    rejects('Green table boundary mismatch rejected',lambda:I.spectrum_for([(1.,1.)],'N',3,table))
    points=np.array([.8,.2,.8,0.,1.]);g=P.real_green_matrix([(1.,1.)],0.,points)
    exact=np.minimum(points[:,None],points[None,:])*(1-np.maximum(points[:,None],points[None,:]))
    check('Green coordinate order and duplicates at mu=0',np.max(np.abs(g-exact))<1e-15)
    rejects('Green positive pole rejected',lambda:P.real_green_matrix([(1.,1.)],table.eigenvalues[0],[.2,.4]))
    rejects('spectral Green wrong removed mode rejected',lambda:GS.gtilde_spectral_blocks([(1.,1.)],target,0,[.2,.4],N=4))
    raw=P.solution_states([(1.,1.)],table.eigenvalues[1],[.2,.3,.5,.8]);norm=P.eigenfunction_states([(1.,1.)],table.frequency_prefix(2)[1],[.2,.3,.5,.8])
    factor=norm[0,0]/raw[0,0]
    check('value and derivative retain one common mass',np.max(np.abs(norm-factor*raw))<3e-14)
    rc=P.Recon(1,4.,'sup');w=rc.z_to_widths(np.array([-30.,0.,0.]))
    check('pure softmax has no artificial positive width floor',0<w[0]<1e-12)
    check('solver failure cannot be stationary',not rc.stationarity_diagnostics(np.zeros(3),solver_success=False)['accepted'])
    matrix=np.diag([1.,2.,-2.,-1.]);c,d=JP.jacobian_cross_blocks(matrix,2)
    check('Jacobian CROSS determinant identity',abs(np.linalg.det(matrix)-np.linalg.det(c)*np.linalg.det(d))<1e-12)
    rejects('commuting Hessian rejected as residual CROSS Jacobian',lambda:JP.jacobian_cross_blocks(np.eye(4),2))
    data=dict(lam_n=2.,lam_np1=5.,u_n=np.array([.3,.7]),u_np1=np.array([.2,-.4]),up_n=np.zeros(2),up_np1=np.zeros(2))
    jumps=np.array([3.,-3.]);terms=J.jacobian_terms(data,jumps,np.zeros((2,2)),np.zeros((2,2)))
    numerical=np.zeros((2,2))
    with mp.workdps(70):
        for i in range(2):
            for j in range(2):
                a,b,u,v,s=map(mp.mpf,(data['lam_n'],data['lam_np1'],float(data['u_n'][j]),float(data['u_np1'][j]),float(jumps[i])))
                ui,vi=mp.mpf(float(data['u_n'][i])),mp.mpf(float(data['u_np1'][i]))
                def residual(t):
                    aa=a*mp.exp(s*ui*ui*t);bb=b*mp.exp(s*vi*vi*t);uu=u*mp.exp(s*ui*ui*t/2);vv=v*mp.exp(s*vi*vi*t/2)
                    return (aa*uu*uu-bb*vv*vv)/bb
                numerical[j,i]=float(mp.diff(residual,0))
    check('general quotient term survives away from stationarity',np.max(np.abs(numerical-terms['M1']/data['lam_np1']))<2e-16 and np.max(np.abs(terms['correction']))>1e-3)

start=time.monotonic();exceptions=[]
for fn in (exact_checks,pairing_checks,nodal_checks,preserved_checks):
    try:fn()
    except Exception as e:exceptions.append(dict(group=fn.__name__,error=repr(e)))
manifest=json.loads((ROOT.parent/'manifest.json').read_text(encoding='utf-8-sig'))
sources={r['path']:hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest() for r in manifest}
result=dict(task='/root/r16_software_review_v2',scope='finite independent reviewer checks; no interval/Lean/infinite theorem acceptance',python=sys.version,optimize=sys.flags.optimize,platform=platform.platform(),threads={k:os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS')},count=len(ROWS),pass_count=sum(r['passed'] for r in ROWS),failed=[r for r in ROWS if not r['passed']],checks=ROWS,exceptions=exceptions,elapsed_seconds=time.monotonic()-start,sources=sources)
Path(sys.argv[1]).write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
print('Independent reviewer checks',result['pass_count'],'/',result['count'],'passed; optimize=',sys.flags.optimize)
for row in result['failed']:print('FAIL',row['name'])
for error in exceptions:print('EXCEPTION',error)
sys.exit(1 if result['failed'] or exceptions else 0)

