"""Independent, packet-only R13 review. No writes outside this reviewer directory.

Run python3 [-O] -I -B verify_351b4411.py. The missing reflection_seeds import
is replaced only by fail-closed sentinels: no seed routine may be executed.
No author's tests, oracle, table, logs, or working-tree modules are executed.
"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/huangzy/.local/lib/python3.14/site-packages')
import ast
import hashlib
import importlib.abc
import importlib.util
import json
import math
import time
import traceback
import types
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import least_squares, brentq
import mpmath as mp

BASE = Path('/mnt/f/LaTeX/BVE research/research/library/reviews/packets/351b4411775cb431fa4f75d0c2e7b37718820cfcd9737cba2820ca43738ff3c6')
OUT = Path('/mnt/f/tools/math-audit-round13-20260927/spectral-reviewer')
PACKET = json.loads((BASE/'packet.json').read_text())
START = time.monotonic()
RESULTS, FAILURES, METRICS = [], [], {}

def check(name, condition, detail=None):
    row = {'name':name, 'passed':bool(condition), 'detail':detail}
    RESULTS.append(row)
    if not row['passed']:
        FAILURES.append(row)
        print('FAIL', name, detail, flush=True)
    return row['passed']

def near(name, actual, expected, atol=1e-12, rtol=0):
    a,b = np.asarray(actual, float), np.asarray(expected, float)
    error = float(np.max(np.abs(a-b))) if a.size else 0.
    limit = atol + rtol*(float(np.max(np.abs(b))) if b.size else 0.)
    check(name, np.all(np.isfinite(a)) and error <= limit,
          {'max_error':error, 'limit':limit})
    return error

def rejects(name, fn):
    try:
        fn()
    except (ValueError, ArithmeticError) as exc:
        check(name, True, {'type':type(exc).__name__, 'message':str(exc)})
    except Exception as exc:
        check(name, False, {'unexpected_exception':repr(exc)})
    else:
        check(name, False, 'accepted invalid/unresolved input')

for rel, info in PACKET['inputs'].items():
    check('snapshot-hash:'+rel,
          hashlib.sha256((BASE/info['snapshot']).read_bytes()).hexdigest()==info['sha256'])

ALLOWED = {Path(rel).stem:BASE/info['snapshot'] for rel,info in PACKET['inputs'].items()
           if rel.startswith('scripts/') and rel.endswith('.py')}

class FrozenSourceLoader(importlib.abc.Loader):
    def create_module(self, spec):
        return None
    def exec_module(self, module):
        path=ALLOWED[module.__name__]
        module.__file__=str(path)
        # Compile listed source bytes directly; never consult a pyc cache.
        exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)

class FrozenImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in ALLOWED:
            return importlib.util.spec_from_file_location(fullname, ALLOWED[fullname],loader=FrozenSourceLoader())
        if fullname.startswith('_gapn') or fullname in ('_sl_prufer','reflection_seeds'):
            raise ImportError('unlisted project dependency forbidden: '+fullname)

sys.meta_path.insert(0, FrozenImports())
SEED_CALLS = []
stub = types.ModuleType('reflection_seeds')
class MissingSeedDependency(RuntimeError):
    pass
def forbidden_seed(*args, **kwargs):
    SEED_CALLS.append(True)
    raise MissingSeedDependency('reflection_seeds.py was not supplied; execution forbidden')
stub.SeedGenerationError = MissingSeedDependency
stub.generate_sector_seed = forbidden_seed
sys.modules['reflection_seeds'] = stub

import _gapn2_symmetry_recon as S
import _gapn2_jacobian_analytic as A
import _gapn2_jacobian_spectral as J
import _gapn2_half_problem_probe as H
import _gapn2_jacobian_probe as P
import _gapn2_sector_decomposition as D
import _sl_prufer as Q

mp.mp.dps = 65
QUAD = {}
def quadrature(order=40):
    if order not in QUAD:
        nodes, weights = mp.gauss_quadrature(order, 'legendre')
        QUAD[order] = list(zip(nodes,weights))
    return QUAD[order]

def matrix(mu, ell, rho):
    if mu == 0:
        return mp.matrix([[1,ell],[0,1]])
    k = mp.sqrt(mu*rho)
    c, s = mp.cos(k*ell), mp.sin(k*ell)
    return mp.matrix([[c,s/k],[-k*s,c]])

def blocks_from_edges(edges, densities):
    ends = [mp.mpf(0),*edges,mp.mpf(1)]
    return [(ends[i+1]-ends[i],mp.mpf(r)) for i,r in enumerate(densities)]

def starts(mu, blocks, initial=(0,1)):
    values = [mp.matrix(initial)]
    for ell,rho in blocks:
        values.append(matrix(mu,ell,rho)*values[-1])
    return values

def sample(mu, blocks, x, initial=(0,1)):
    value = mp.matrix(initial)
    left = mp.mpf(0)
    for ell,rho in blocks:
        if x <= left+ell:
            return matrix(mu,x-left,rho)*value
        value = matrix(mu,ell,rho)*value
        left += ell
    return value

def mass(mu, blocks, data=None, order=40):
    data = starts(mu,blocks) if data is None else data
    total = mp.mpf(0)
    for (ell,rho),v in zip(blocks,data):
        total += rho*ell/2*sum(w*(matrix(mu,ell*(1+t)/2,rho)*v)[0]**2
                              for t,w in quadrature(order))
    return total

def zero_count(freq, blocks):
    state = mp.matrix([0,1]); left = mp.mpf(0)
    length = sum(ell for ell,rho in blocks)
    found=[]
    tol=mp.mpf('1e-42')*max(1,length)
    for ell,rho in blocks:
        wave=freq*mp.sqrt(rho)
        phase=mp.atan2(mp.re(state[0])*wave,mp.re(state[1]))
        lo=int(mp.floor(phase/mp.pi))-1
        hi=int(mp.ceil((phase+wave*ell)/mp.pi))+1
        for k in range(lo,hi+1):
            t=(k*mp.pi-phase)/wave
            x=left+t
            if -tol<=t<=ell+tol and tol<x<length-tol:
                if all(abs(x-v)>tol for v in found): found.append(x)
        state=matrix(freq**2,ell,rho)*state
        left+=ell
    return len(found)

def roots(blocks, count, bc='D'):
    # Independent secular sign scan plus explicit physical zero counts. No
    # source phase, source eigenvalues, or source scan tables initialize it.
    component = 0 if bc=='D' else 1
    step=mp.pi/(16*sum(l for l,r in blocks)*mp.sqrt(max(r for l,r in blocks)))
    sec=lambda f: starts(f*f,blocks)[-1][component]
    left=step/37; prev=sec(left); answer=[]
    for iteration in range(20000):
        right=left+step; value=sec(right)
        if mp.re(prev)*mp.re(value)<0:
            f=mp.findroot(sec,(left,right),tol=mp.mpf('1e-58'))
            if not left < f < right or abs(sec(f))>mp.mpf('1e-48'):
                raise RuntimeError('independent secular refinement failed')
            if zero_count(f,blocks)!=len(answer):
                raise RuntimeError('independent root scan skipped a physical mode')
            answer.append(f*f)
            if len(answer)==count: return answer
        left,prev=right,value
    raise RuntimeError('independent scan exhausted')

def residual_pair(pair, edges, densities, order=40):
    blocks=blocks_from_edges(edges,densities)
    terms=[]
    for mu in pair:
        data=starts(mu,blocks)
        norm=mass(mu,blocks,data,order)
        terms.append([v[0]**2/norm for v in data[1:-1]])
    return mp.matrix([pair[0]/pair[1]*u-v for u,v in zip(*terms)])

def implicit_oracle(edges, densities, n, h=mp.mpf('1e-25'), order=40):
    edges=list(map(mp.mpf,edges)); blocks=blocks_from_edges(edges,densities)
    pair=roots(blocks,n+1)[-2:]
    f=residual_pair(pair,edges,densities,order)
    result=mp.matrix(len(edges)); dl=mp.matrix(2,len(edges))
    for i in range(len(edges)):
        moved=edges.copy(); moved[i]+=mp.j*h
        shifted=blocks_from_edges(moved,densities)
        slopes=[]
        for k,mu in enumerate(pair):
            dx=mp.im(starts(mu,shifted)[-1][0])/h
            dm=mp.im(starts(mu+mp.j*h,blocks)[-1][0])/h
            slopes.append(-dx/dm); dl[k,i]=slopes[-1]
        varied=[mu+mp.j*h*slope for mu,slope in zip(pair,slopes)]
        rf=residual_pair(varied,moved,densities,order)
        for j in range(len(edges)): result[j,i]=mp.im(rf[j])/h
    return pair,np.array(f.tolist(),float).ravel(),np.array(result.tolist(),float),np.array(dl.tolist(),float)

def green_bvp(mu, blocks, points, bc):
    # Solve the two coefficient matching equations at each delta source.
    # Right data use reversed geometry. No Wronskian or source Green formula.
    length=sum(ell for ell,rho in blocks); rev=list(reversed(blocks))
    def right(x):
        q=sample(mu,rev,length-x,(0,1) if bc=='D' else (1,0))
        return mp.matrix([q[0],-q[1]])
    output=np.empty((len(points),len(points)))
    for j,y in enumerate(points):
        ly,ry=sample(mu,blocks,y),right(y)
        coeff=mp.lu_solve(mp.matrix([[ly[0],-ry[0]],[-ly[1],ry[1]]]),mp.matrix([0,-1]))
        for i,x in enumerate(points):
            value=coeff[0]*sample(mu,blocks,x)[0] if x<=y else coeff[1]*right(x)[0]
            output[i,j]=float(mp.re(value))
    return output

def config(n,r,edges,mode='sup'):
    rc=S.Recon(n,r,mode)
    z=rc.widths_to_z(np.diff([0.,*edges,1.]))
    return rc,z,np.cumsum(rc.z_to_widths(z))[:-1]

def normalized_checks():
    cases=[(2,1,[.1,.5,.6,.8],'sup'),(1,4,[.55,.6746455700142735],'sup'),
           (2,4,[.071,.249,.608,.911],'inf'),(1,100,[.48,.53],'sup')]
    for c,(n,r,x,mode) in enumerate(cases):
        rc,z,x=config(n,r,x,mode); data=A.eigen_data(rc,z)
        blocks=blocks_from_edges(list(map(mp.mpf,x)),rc.pat)
        exact=roots(blocks,n+1)
        for index,tag in ((n-1,'n'),(n,'np1')):
            mu=exact[index]; norm=mp.sqrt(mass(mu,blocks))
            states=[[float(mp.re(t/norm)) for t in sample(mu,blocks,mp.mpf(xi))] for xi in x]
            err=near(f'normalized-nodes-{c}-{tag}',np.c_[data['u_'+tag],data['up_'+tag]],states,atol=2e-10)
            if c<2: METRICS[f'nodal-error-{c}-{tag}']=err
            vals,weights=np.polynomial.legendre.leggauss(96)
            pts=[]; wt=[]; start=0.
            for ell,rho in rc.blocks_from_z(z):
                pts.extend(start+ell*(vals+1)/2); wt.extend(rho*ell*weights/2); start+=ell
            u=S.eigenfunction_states(rc.blocks_from_z(z),np.sqrt(data['lam_'+tag]),pts)[:,0]
            near(f'unit-mass-{c}-{tag}',np.dot(wt,u*u),1,4e-12)
    for freq in (0.,1e-14,1e-5,.0099,.0101,2.5):
        raw=[(.2,1),(.3,7),(.5,2)]; blocks=[(mp.mpf(l),mp.mpf(r)) for l,r in raw]
        pts=[0.,.2,.77,1.,.2]
        norm=mp.sqrt(mass(mp.mpf(freq)**2,blocks))
        expected=[[float(mp.re(t/norm)) for t in sample(mp.mpf(freq)**2,blocks,mp.mpf(x))] for x in pts]
        near('small-wave:'+str(freq),S.eigenfunction_states(raw,freq,pts),expected,5e-12)
    raw=[(.1,1),(.2,4),(.3,1),(.3999999999999998,4)]
    end=float(np.cumsum(np.array(raw)[:,0])[-1])
    near('normalized-roundoff-snap',S.eigenfunction_states(raw,3,[1]),S.eigenfunction_states(raw,3,[end]),0)
    rejects('strict-green-no-snap',lambda:S.real_green_matrix(raw,0,[1]))
    rejects('strict-state-no-snap',lambda:S.solution_states(raw,0,[1]))
    for x in (-1e-8,1+1e-8,np.inf,np.nan):
        rejects('normalized-domain:'+str(x),lambda x=x:S.eigenfunction_states([(1,1)],1,[x]))

def green_checks():
    rng=np.random.default_rng(391527)
    for c,raw in enumerate([[(1.,1.)],[(.18,1),(.31,7),(.51,2)],[(.1,1),(.17,30),(.23,3)]]):
        end=float(np.cumsum(np.array(raw)[:,0])[-1]); pts=np.array([end*.76,0,end*.13,end,end*.13,end*.45])
        blocks=[(mp.mpf(l),mp.mpf(r)) for l,r in raw]
        for mu in (-100.,-1.,-1e-20,0.,1e-20,.7,7.):
            for bc in ('D','N'):
                g=S.real_green_matrix(raw,mu,pts,RightBoundary=bc)
                truth=green_bvp(mp.mpf(mu),blocks,list(map(mp.mpf,pts)),bc)
                near(f'green-independent:{c}:{mu}:{bc}',g,truth,5e-12)
                perm=rng.permutation(len(pts))
                near(f'green-permutation:{c}:{mu}:{bc}',S.real_green_matrix(raw,mu,pts[perm],RightBoundary=bc),g[np.ix_(perm,perm)],0)
                near(f'green-symmetry:{c}:{mu}:{bc}',g,g.T,0)
                near(f'green-duplicates:{c}:{mu}:{bc}',g[2],g[4],0)
                near(f'green-left-end:{c}:{mu}:{bc}',g[1],0,0)
                if bc=='D': near(f'green-right-end:{c}:{mu}',g[3],0,2e-14)
                near(f'half-route:{c}:{mu}:{bc}',H.green_regular(raw,mu,pts[0],pts[2],bc),g[0,2],0)
                if bc=='D': near(f'full-route:{c}:{mu}',A.green_kernel(raw,mu,pts),g,0)
                if mu<=0:
                    check(f'green-positive:{c}:{mu}:{bc}',np.linalg.eigvalsh(g[np.ix_([0,2,5],[0,2,5])]).min()>0)
    near('zero-DD',H.green_regular([(.5,9)],0,.1,.2,'D'),.06,2e-16)
    near('zero-DN',H.green_regular([(.5,9)],0,.1,.2,'N'),.1,2e-16)
    check('green-empty',S.real_green_matrix([(1,1)],0,[]).shape==(0,0))
    raw=[(.3,1),(.4,4),(.3,2)]; h=1e-6
    for y in (.3,.51):
        for mu in (-2.,0.,7.):
            for bc in ('D','N'):
                g=lambda x:H.green_regular(raw,mu,x,y,bc)
                right=(-3*g(y)+4*g(y+h)-g(y+2*h))/(2*h)
                left=(3*g(y)-4*g(y-h)+g(y-2*h))/(2*h)
                near(f'green-source-jump:{y}:{mu}:{bc}',right-left,-1,2e-8)
    for mu in (-2.,0.,7.):
        g=lambda x:H.green_regular(raw,mu,x,.51,'N')
        near('DN-right-derivative:'+str(mu),(3*g(1)-4*g(1-h)+g(1-2*h))/(2*h),0,2e-8)
    for mu in (np.nan,np.inf,-np.inf,1j,False,'1'):
        rejects('invalid-mu:'+str(mu),lambda mu=mu:S.real_green_matrix([(1,1)],mu,[.2]))
    for pts in ([-np.finfo(float).eps],[1+np.finfo(float).eps],[np.inf],[np.nan],[1j],[[.2]]):
        rejects('invalid-points:'+repr(pts),lambda pts=pts:S.real_green_matrix([(1,1)],0,pts))
    for blocks in ([],[(0,1)],[(1,0)],[(1,-1)],[(1,np.nan)],[(np.inf,1)],[(1,1),(1e-20,1)]):
        rejects('invalid-blocks:'+repr(blocks),lambda blocks=blocks:S.real_green_matrix(blocks,0,[]))
    for bc in ('X',None,False):
        rejects('invalid-boundary:'+str(bc),lambda bc=bc:H.green_regular([(1,1)],0,.1,.2,bc))
    for bc,mu in [('D',np.pi**2),('N',(np.pi/2)**2)]:
        rejects('closed-pole:'+bc,lambda bc=bc,mu=mu:S.real_green_matrix([(1,1)],mu,[.2],RightBoundary=bc))
        rejects('overflow:'+bc,lambda bc=bc:S.real_green_matrix([(1,1)],-1e12,[.1,.2],RightBoundary=bc))
        for mu in (0.,-1.):
            rejects('reduced-nonpositive:'+bc+str(mu),lambda bc=bc,mu=mu:H.green_regularized([(.5,1)],mu,.1,.2,bc))

def jacobian_checks():
    cases=[(1,4,[.25,.75],'sup'),(1,4,[.55,.6746455700142735],'sup'),
           (1,3,[.17,.62],'inf'),(2,4,[.071,.249,.608,.911],'sup'),(2,1,[.1,.5,.6,.8],'sup')]
    for c,(n,r,x,mode) in enumerate(cases):
        rc,z,x=config(n,r,x,mode)
        pair,f,truth,slopes=implicit_oracle(x,rc.pat,n)
        data=A.eigen_data(rc,z)
        near('independent-residual:'+str(c),rc.residual(z),f,2e-12)
        near('independent-lambda-shapes:'+str(c),[data['lam_n']*np.diff(rc.pat)*data['u_n']**2,
             data['lam_np1']*np.diff(rc.pat)*data['u_np1']**2],slopes,2e-9)
        counts=[160,640,2560] if c==0 else [160,640]
        errors=[]
        for count in counts:
            result=J.analytic_jacobian_spectral(rc,z,N=count)
            errors.append(float(np.max(abs(result-truth))))
        METRICS['nonstationary:'+str(c)]={'counts':counts,'errors':errors,'oracle':truth.tolist()}
        check('jacobian-convergence:'+str(c), errors[-1]<.1 and (r==1 or errors[-1]<.36*errors[0]),errors)
        if r==1: near('R1-jacobian-closed',result,truth,2e-11)
        fd,diag=P.jac_fd(rc,z,h=1e-6,return_diagnostics=True)
        near('physical-FD-oracle:'+str(c),fd,truth,4e-6)
        for row in diag['columns']:
            target=np.zeros(2*n); target[row['edge_index']]=row['used_step']
            near('plus-physical-direction:'+str((c,row['edge_index'])),np.array(row['plus_edges'])-x,target,row['geometry_error_budget'])
            near('minus-physical-direction:'+str((c,row['edge_index'])),x-np.array(row['minus_edges']),target,row['geometry_error_budget'])
        terms=A.term_breakdown(rc,z,N=160); b=terms['eigen_data']['lam_np1']
        direct=A.analytic_jacobian(rc,z,N=160)[0]
        near('entrypoint-agreement:'+str(c),direct,J.analytic_jacobian_spectral(rc,z,N=160),0)
        near('breakdown-agreement:'+str(c),direct,(np.diag(terms['fprime'])+terms['M1']+terms['M2']+terms['M3'])/b,0)
        a=data['lam_n']; u=data['u_n']; ff=a*u*u-b*data['u_np1']**2
        correction=(a*np.outer(ff,u*u)+2*a*np.outer(u*u,ff)-np.outer(ff,ff))*np.diff(rc.pat)[None,:]/b**2
        near('correction-algebra:'+str(c),terms['correction']/b,correction,2e-12)
        if c==0:
            _,_,again,_=implicit_oracle(x,rc.pat,n,h=mp.mpf('1e-29'),order=52)
            near('oracle-step-quadrature-refinement',truth,again,1e-25)
            C,E=P.jacobian_cross_blocks(direct,n)
            near('symmetric-nonstationary-cross-det',np.linalg.det(direct),(-1)**n*np.linalg.det(C)*np.linalg.det(E),1e-10)
    for h in (False,0,-1,np.inf,np.nan):
        rejects('FD-invalid-h:'+str(h),lambda h=h:P.jac_fd(rc,z,h=h))
    rejects('cross-block-reject-commuting-Hessian',lambda:P.jacobian_cross_blocks(np.eye(4),2))
    rejects('FD-unrepresentable-base',lambda:P.jac_fd(S.Recon(1,4,'sup'),np.array([-100.,0.,0.])))

def stationary_point(n,mode):
    # Start at the exact constant-density switching equation, then continue
    # the density contrast. This uses no supplied or unsupplied branch table.
    f=lambda x:n*n*np.sin(n*np.pi*x)**2-(n+1)**2*np.sin((n+1)*np.pi*x)**2
    grid=np.linspace(1e-7,1-1e-7,2049)
    edges=[brentq(f,left,right,xtol=1e-14) for left,right in zip(grid,grid[1:]) if f(left)*f(right)<0]
    if len(edges)!=2*n: raise RuntimeError('constant-density seed has wrong switching count')
    rc=S.Recon(n,1.,mode); z=rc.widths_to_z(np.diff([0,*edges,1]))
    for contrast in (1.05,1.2,1.5,2.,2.5,3.,3.5,4.):
        rc=S.Recon(n,contrast,mode)
        z=P.symmetric_root(rc,z,max_nfev=250)
        if z is None: break
    if z is not None and min(rc.z_to_widths(z))>.005 and rc.full_report(z)['band_ok']:
        return rc,z
    rc=S.Recon(n,4.,mode)
    rng=np.random.default_rng(n*91+(0 if mode=='sup' else 1))
    for attempt in range(12):
        ws=np.ones(2*n+1) if attempt==0 else rng.uniform(.2,1.5,2*n+1)
        ws=(ws+ws[::-1])/2; ws/=sum(ws)
        z=P.symmetric_root(rc,rc.widths_to_z(ws),max_nfev=250)
        if z is not None:
            widths=rc.z_to_widths(z)
            if min(widths)>.005 and np.max(abs(rc.residual(z)))<1e-10 and rc.full_report(z)['band_ok']:
                return rc,z
    raise RuntimeError('no interior stationary band point found from independent seeds')

def stationary_checks():
    for n in (1,2,3):
        for mode in ('sup','inf'):
            print('STATIONARY',n,mode,flush=True)
            rc,z=stationary_point(n,mode); x=np.cumsum(rc.z_to_widths(z))[:-1]
            pair,residual,truth,slopes=implicit_oracle(x,rc.pat,n)
            key=str(n)+':'+mode
            near('true-stationary-residual:'+key,residual,0,2e-10)
            counts=[160,640]; errors=[]
            for count in counts:
                result=J.analytic_jacobian_spectral(rc,z,N=count)
                errors.append(float(np.max(abs(result-truth))))
            check('stationary-J-convergence:'+key,errors[1]<.35*errors[0] and errors[1]<.2,errors)
            fd,diag=P.jac_fd(rc,z,return_diagnostics=True)
            near('stationary-FD-independent:'+key,fd,truth,7e-6)
            terms=A.term_breakdown(rc,z,N=160); data=terms['eigen_data']; b=data['lam_np1']; a=data['lam_n']
            near('stationary-correction-zero:'+key,terms['correction']/b,0,3e-9)
            direct,fp,fpid,_,_=A.analytic_jacobian(rc,z,N=160)
            near('stationary-Wronskian:'+key,fp,fpid,3e-6)
            C,E=P.jacobian_cross_blocks(truth,n)
            near('stationary-cross-det:'+key,np.linalg.det(truth),(-1)**n*np.linalg.det(C)*np.linalg.det(E),1e-7,1e-12)
            near('independent-J-anticommutation:'+key,truth[:,::-1]+truth[::-1,:],0,5e-8)
            jumps=np.diff(rc.pat); K=np.diag(1/jumps)@truth
            near('independent-raw-K-symmetry:'+key,K,K.T,3e-8)
            I=np.eye(2*n); be=(I[:,:n]+I[:,::-1][:,:n])/np.sqrt(2); bo=(I[:,:n]-I[:,::-1][:,:n])/np.sqrt(2)
            sd=D.sector_data(rc,z,N=640)
            ss=np.diag(data['eps']); ee=np.diag(data['eps'][:n]); raw=np.diag(1/jumps)@result
            for name,expected in [('Ke',be.T@raw@be),('Ko',bo.T@raw@bo),('KpEven',be.T@ss@raw@ss@be),('KpOdd',bo.T@ss@raw@ss@bo)]:
                near('sector-truncation-identity:'+key+':'+name,sd[name],expected,8e-8)
            near('sector-swap-Ke:'+key,sd['KpOdd'],ee@np.asarray(sd['Ke'])@ee,1e-12)
            near('sector-swap-Ko:'+key,sd['KpEven'],ee@np.asarray(sd['Ko'])@ee,1e-12)
            for suffix in ('e','o'):
                near('sector-pieces:'+key+':'+suffix,sd['K'+suffix],np.diag(sd['d'])+np.asarray(sd['H'+suffix])+np.asarray(sd['E'+suffix]),2e-12)
            METRICS['stationary:'+key]={'edges':x.tolist(),'independent_F_max':float(max(abs(residual))),'errors':errors,
                'FD_error':float(np.max(abs(fd-truth)))}
            if n==2:
                hb=H.half_blocks(rc,rc.z_to_widths(z)); xx=x[:n]; u=data['u_n'][:n]; eps=ee
                # Direct half-kernel assembly against an independent implicit J.
                gtD=np.array([[H.green_regularized(hb,a,xi,yj,'D') for yj in xx] for xi in xx])
                gtN=np.array([[H.green_regularized(hb,b,xi,yj,'N') for yj in xx] for xi in xx])
                gd=np.array([[H.green_regular(hb,b,xi,yj,'D') for yj in xx] for xi in xx])
                gn=np.array([[H.green_regular(hb,a,xi,yj,'N') for yj in xx] for xi in xx])
                rank=eps@(u*u)
                ko=np.diag(sd['d'])+4*a*(b-a)/b**2*np.outer(rank,rank)+2*a*np.diag(u)@(gtN-a/b*eps@gtD@eps)@np.diag(u)
                kpodd=np.diag(sd['d'])+2*a*np.diag(u)@(eps@gd@eps-a/b*gn)@np.diag(u)
                near('closed-half-raw-Ko-independent:'+key,ko,bo.T@K@bo,2e-8)
                near('closed-half-KpOdd-independent:'+key,kpodd,ee@(be.T@K@be)@ee,2e-8)
                METRICS['half-closed:'+key]={'Ko_error':float(np.max(abs(ko-bo.T@K@bo))),
                    'KpOdd_error':float(np.max(abs(kpodd-ee@(be.T@K@be)@ee)))}

def r12_checks():
    for rho in (1e-6,1.,100.):
        for bc in ('D','N'):
            blocks=[(.5,rho)]; table=H.HalfSpectrum(blocks,bc,160)
            for count in (4,80,160):
                exact=((np.arange(1,count+1)-(0.5 if bc=='N' else 0))*np.pi/(.5*np.sqrt(rho)))**2
                actual=H.half_spectrum(blocks,bc,count)
                near(f'constant-spectrum:{rho}:{bc}:{count}',actual/exact,1,3e-14)
                check(f'prefix:{rho}:{bc}:{count}',np.array_equal(actual,table.prefix(count)))
    for c,raw in enumerate([[ (.1,1),(.05,100),(.35,2) ],[(.499,1),(.001,1e4)]]):
        blocks=[(mp.mpf(l),mp.mpf(r)) for l,r in raw]
        for bc in ('D','N'):
            lam=H.half_spectrum(raw,bc,20)
            check(f'piecewise-prefix:{c}:{bc}',np.array_equal(lam[:4],H.half_spectrum(raw,bc,4)))
            index=0 if bc=='D' else 1
            for mode in (1,2,5,15):
                guess=mp.sqrt(mp.mpf(float(lam[mode-1])))
                secular=lambda freq: starts(freq**2,blocks)[-1][index]
                f=mp.findroot(secular,(guess*(1-mp.mpf('1e-8')),guess*(1+mp.mpf('1e-8'))),tol=mp.mpf('1e-57'))
                check(f'physical-node-index:{c}:{bc}:{mode}',zero_count(f,blocks)==mode-1)
                near(f'physical-transfer-root:{c}:{bc}:{mode}',float(f*f)/lam[mode-1],1,3e-12)
    raw=[(.5,100.)]; table=H.HalfSpectrum(raw,'N',160); mu=table.eigenvalues[1]
    for count in (4,80,160):
        actual=H._spectral_green(raw,mu,1,'N',.1,.2,count,spectrum=table)
        k=np.arange(1,count+1); k=k[k!=2]
        freq=(k-.5)*np.pi/.5; lam=freq**2/100
        oracle=np.sum((2/(100*.5))*np.sin(freq*.1)*np.sin(freq*.2)/(lam-mu))
        near('pole-removed-constant-series:'+str(count),actual,oracle,2e-14)
    for name,fn in [
        ('wrong-pole-target',lambda:H._spectral_green(raw,(5.5*np.pi/5)**2,1,'N',.1,.1,80,spectrum=table)),
        ('wrong-pole-mode',lambda:H._spectral_green(raw,mu,0,'N',.1,.1,80,spectrum=table)),
        ('wrong-geometry',lambda:H._spectral_green([(.5,101)],mu,1,'N',.1,.1,80,spectrum=table)),
        ('wrong-BC',lambda:H._spectral_green(raw,mu,1,'D',.1,.1,80,spectrum=table)),
        ('outside-prefix',lambda:H._spectral_green(raw,mu,1,'N',.1,.1,1,spectrum=table)),
        ('short-table',lambda:H._spectral_green(raw,mu,1,'N',.1,.1,161,spectrum=table)),
        ('full-pole',lambda:H._spectral_full_green(raw,mu,'N',.1,.1,80,spectrum=table)),
        ('full-near-pole',lambda:H._spectral_full_green(raw,np.nextafter(mu,np.inf),'N',.1,.1,80,spectrum=table)),
        ('uncovered-target',lambda:H._spectral_full_green(raw,2*table.eigenvalues[-1],'N',.1,.1,80,spectrum=table)),
        ('bad-mumax',lambda:H.half_spectrum(raw,'D',4,mumax=.1)),
        ('bad-refinement',lambda:Q.indexed_roots(raw,4,Refine=1,RightBoundary='N'))]:
        rejects('bound-pole:'+name,fn)
    for count in (False,0,-1,2.5):
        rejects('bad-spectrum-count:'+repr(count),lambda count=count:H.HalfSpectrum(raw,'D',count))
    extreme=H.HalfSpectrum([(1,1e-306)],'D',4)
    rejects('spectral-overflow',lambda:H._spectral_full_green([(1,1e-306)],-np.finfo(float).max,'D',.25,.25,4,spectrum=extreme))
    for bc in ('D','N'):
        table=H.HalfSpectrum([(.5,1)],bc,640)
        for mu in (0.,-1.,-100.):
            truth=green_bvp(mp.mpf(mu),[(mp.mpf('.5'),mp.mpf(1))],[mp.mpf('.1'),mp.mpf('.2')],bc)[0,1]
            errs=[]
            for count in (160,640):
                val=H._spectral_full_green([(.5,1)],mu,bc,.1,.2,count,spectrum=table)
                errs.append(abs(val-truth))
            check('nonpositive-spectrum:'+bc+str(mu),errs[1]<2e-7 and errs[1]<errs[0],errs)

for name,fn in [('normalization',normalized_checks),('Green',green_checks),('Jacobian',jacobian_checks),
                ('stationarity-and-sectors',stationary_checks),('R12-index-and-poles',r12_checks)]:
    print('START',name,flush=True)
    try: fn()
    except Exception:
        check('group-execution:'+name,False,traceback.format_exc())
    print('END',name,'checks',len(RESULTS),'failures',len(FAILURES),flush=True)

check('missing-seed-dependency-never-called',not SEED_CALLS)
loaded={name:str(Path(mod.__file__).resolve()) for name,mod in sys.modules.items()
        if name in ALLOWED and getattr(mod,'__file__',None)}
check('all-project-imports-from-snapshots',all(Path(path)==ALLOWED[name] for name,path in loaded.items()))
for rel, info in PACKET['inputs'].items():
    check('unchanged-after-execution:'+rel,hashlib.sha256((BASE/info['snapshot']).read_bytes()).hexdigest()==info['sha256'])
report={'status':'PASS' if not FAILURES else 'FAIL','optimized':not __debug__,
        'packet_sha256':hashlib.sha256((BASE/'packet.json').read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mp.__version__},
        'elapsed_seconds':time.monotonic()-START,'count':len(RESULTS),'failures':FAILURES,
        'metrics':METRICS,'checks':RESULTS,'loaded_project_modules':loaded,
        'adaptation':'Only missing reflection_seeds import uses fail-closed sentinels; target functions are unmodified snapshots.',
        'limitations':['Finite numerical tests; no interval or uniform tail bound.',
            'Missing reflection_seeds.py and op03_gap_table.json prevent unadapted imports/table-driven CLIs.',
            'Author test scripts/logs and unsupplied caller modules were not executed.']}
dest=OUT/('result-351b4411-optimized.json' if not __debug__ else 'result-351b4411-normal.json')
dest.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:report[k] for k in ('status','optimized','count','elapsed_seconds','failures','metrics')},indent=2),flush=True)
sys.exit(0 if not FAILURES else 1)
