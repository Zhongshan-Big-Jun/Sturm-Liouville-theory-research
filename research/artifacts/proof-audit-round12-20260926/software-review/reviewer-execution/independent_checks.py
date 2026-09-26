import dataclasses,importlib,json,math,sys,warnings
from pathlib import Path
import numpy as np
import mpmath as mp
sys.path.insert(0,str(Path.cwd()/'scripts'))
import _sl_prufer as P
import _gapn2_half_problem_probe as H
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_jacobian_spectral import analytic_jacobian_spectral
from _gapn2_sector_decomposition import sector_data
mp.mp.dps=85
checks=[]
def check(name,ok,detail=None):
    checks.append(dict(name=name,status='PASS' if bool(ok) else 'FAIL',detail=detail))
def reject(name,fn):
    try: value=fn()
    except (ValueError,ArithmeticError,TypeError,dataclasses.FrozenInstanceError) as e:
        check(name,True,type(e).__name__+': '+str(e))
    except Exception as e: check(name,False,'unexpected '+type(e).__name__+': '+str(e))
    else: check(name,False,'accepted '+repr(value))
def endpoint(blocks,w,bc):
    y,v=mp.mpf(0),mp.mpf(1)
    for l,rho in blocks:
        q=w*mp.sqrt(mp.mpf(rho)); a=q*mp.mpf(l); c,s=mp.cos(a),mp.sin(a)
        y,v=c*y+s*v/q,-q*s*y+c*v
    return y if bc=='D' else v

def nodal_count(blocks,w):
    y,v=mp.mpf(0),mp.mpf(1); start=mp.mpf(0); found=[]; length=sum(mp.mpf(b[0]) for b in blocks)
    for l,rho in blocks:
        l=mp.mpf(l); q=w*mp.sqrt(mp.mpf(rho)); phase=mp.atan2(q*y,v)
        first=int(mp.ceil(phase/mp.pi)); last=int(mp.floor((phase+q*l)/mp.pi))
        for j in range(first,last+1):
            x=start+(mp.pi*j-phase)/q
            if mp.mpf('1e-35')<x<length-mp.mpf('1e-35') and all(abs(x-z)>mp.mpf('1e-35') for z in found): found.append(x)
        c,s=mp.cos(q*l),mp.sin(q*l); y,v=c*y+s*v/q,-q*s*y+c*v; start+=l
    return len(found)

for length,rho in [(.125,.01),(.5,9.),(2.,1e-8),(8.,1e8)]:
    for bc in ['D','N']:
        roots,records=P.indexed_roots([(length,rho)],64,RightBoundary=bc)
        exact=np.pi*(np.arange(1,65)-(0.5 if bc=='N' else 0))/(length*np.sqrt(rho))
        check(f'constant {length} {rho} {bc}',np.max(abs(roots/exact-1))<2e-14,float(np.max(abs(roots/exact-1))))
        for count in [1,2,7,64]:
            small=P.indexed_roots([(length,rho)],count,RightBoundary=bc)
            check(f'prefix-roots {length} {rho} {bc} {count}',np.array_equal(small[0],roots[:count]) and small[1]==records[:count])
        if bc=='D': check(f'default-DD {length} {rho}',np.array_equal(roots,P.indexed_roots([(length,rho)],64)[0]))

# Compare interface angle maps to high-precision maps at and adjacent to axes.
max_angle_error=0.
for scale in [.01,.25,1.,4.,100.]:
    for k in range(1,41):
        for a in [k*np.pi/2,np.nextafter(k*np.pi/2,-np.inf),np.nextafter(k*np.pi/2,np.inf)]:
            ma=mp.mpf(a); turns=mp.floor(ma/mp.pi); rem=ma-turns*mp.pi
            ref=turns*mp.pi+mp.atan2(mp.mpf(scale)*mp.sin(rem),mp.cos(rem))
            err=float(abs(mp.mpf(float(P._angle_scale(a,scale)))-ref))
            max_angle_error=max(max_angle_error,err)
check('integer-half-integer-interface-lifts',max_angle_error<2e-11,max_angle_error)

layers=[[(.125,4.),(.25,1.)],[(.125,1.),(.0625,16.),(.3125,1.)],[(.21,100.),(.29,.01)],[(1e-8,1e6),(.24999999,1.),(.25,4.)],[(.0625,.25),(.125,9.),(.3125,2.)]]
layer_report=[]
for case,blocks in enumerate(layers):
    for bc in ['D','N']:
        roots,records=P.indexed_roots(blocks,24,RightBoundary=bc)
        check(f'layer-prefix {case} {bc}',np.array_equal(roots[:3],P.indexed_roots(blocks,3,RightBoundary=bc)[0]))
        for mode in [1,2,3,8,17,24]:
            guess=mp.mpf(float(roots[mode-1]))
            ref=mp.findroot(lambda z:endpoint(blocks,z,bc),(guess*(1-mp.mpf('1e-6')),guess*(1+mp.mpf('1e-6'))),tol=mp.mpf('1e-75'))
            error=float(abs(guess/ref-1)); zeros=nodal_count(blocks,ref)
            check(f'layer-physical-mode {case} {bc} {mode}',error<5e-11 and zeros==mode-1,dict(relative_frequency_error=error,interior_zeros=zeros))
            layer_report.append(error)
for name,blocks in [('lost-endpoint',[(1.,1.),(1e-20,2.)]),('optical-overflow',[(1e300,1e100)]),('optical-underflow',[(1e-300,1e-300)]),('lambda-overflow',[(1e-160,1.)]),('lambda-underflow',[(1e170,1.)]),('invalid-empty',[])]:
    reject(name,lambda b=blocks:H.half_spectrum(b,'D',4))
reject('refinement-unresolved',lambda:P.indexed_roots(layers[0],4,Refine=1,RightBoundary='N'))
reject('phase-frequency-overflow',lambda:P.lifted_phase([(1e150,1e150)],[1e150]))
for bad in [False,np.bool_(True),0,-2,1.5,np.nan]:
    reject('bad-count '+repr(bad),lambda b=bad:P.indexed_roots([(1.,1.)],b))

# Constant-density finite sums have an independent trigonometric formula.
max_sum_error=0.
for bc in ['D','N']:
    length,rho=.5,7.; blocks=[(length,rho)]
    table=H.half_spectrum(blocks,bc,80,return_table=True)
    reject('frozen-assignment '+bc,lambda:setattr(table,'boundary','D' if bc=='N' else 'N'))
    prefix=table.prefix(4); prefix[0]=-1
    check('detached-prefix '+bc,table.eigenvalues[0]>0)
    check('deeply-tuple-records '+bc,isinstance(table.blocks,tuple) and all(isinstance(x,tuple) for x in table.blocks) and all(isinstance(x,tuple) for row in table.phase_records for key,x in row if key in ['bracket','phase_bracket','comparison']))
    omega=(np.arange(1,81)-(0.5 if bc=='N' else 0))*np.pi/length
    exact_lam=omega**2/rho
    for count,mode in [(1,1),(4,1),(4,4),(16,2),(80,15)]:
        mu=table.eigenvalues[mode-1]
        for x,y in [(0.,.3),(.07,.19),(length,.2),(.2,.2)]:
            keep=np.arange(count)!=mode-1
            ref=np.sum((2/(rho*length))*np.sin(omega[:count][keep]*x)*np.sin(omega[:count][keep]*y)/(exact_lam[:count][keep]-mu))
            value=H._spectral_green(blocks,mu,mode-1,bc,x,y,count,spectrum=table)
            error=abs(value-ref); max_sum_error=max(max_sum_error,error)
            check(f'reduced-trig {bc} {count} {mode} {x} {y}',error<2e-14,error)
    for mu in [0.,-3.,table.eigenvalues[10]*1.01]:
        for count in [4,80]:
            x,y=.1,.37
            ref=np.sum(2/(rho*length)*np.sin(omega[:count]*x)*np.sin(omega[:count]*y)/(exact_lam[:count]-mu))
            value=H._spectral_full_green(blocks,mu,bc,x,y,count,spectrum=table)
            check(f'full-trig {bc} {count} {mu}',abs(value-ref)<2e-13,abs(value-ref))
    mu=table.eigenvalues[1]
    rejects=[('wrong-zero-mode',lambda:H._spectral_green(blocks,mu,0,bc,.1,.2,4,spectrum=table)),('wrong-target',lambda:H._spectral_green(blocks,table.eigenvalues[4],1,bc,.1,.2,10,spectrum=table)),('wrong-geometry',lambda:H._spectral_green([(np.nextafter(length,np.inf),rho)],mu,1,bc,.1,.2,4,spectrum=table)),('wrong-boundary',lambda:H._spectral_green(blocks,mu,1,'N' if bc=='D' else 'D',.1,.2,4,spectrum=table)),('outside-prefix',lambda:H._spectral_green(blocks,mu,1,bc,.1,.2,1,spectrum=table)),('past-table',lambda:H._spectral_green(blocks,mu,1,bc,.1,.2,81,spectrum=table)),('full-pole-outside-prefix',lambda:H._spectral_full_green(blocks,table.eigenvalues[20],bc,.1,.2,4,spectrum=table)),('full-near-pole',lambda:H._spectral_full_green(blocks,np.nextafter(mu,0),bc,.1,.2,4,spectrum=table)),('uncovered-full-target',lambda:H._spectral_full_green(blocks,table.eigenvalues[-1]*1.01,bc,.1,.2,4,spectrum=table)),('point-past-end',lambda:H._spectral_green(blocks,mu,1,bc,np.nextafter(length,np.inf),.2,4,spectrum=table))]
    for name,fn in rejects: reject(name+' '+bc,fn)

# Direct projection of each physical spectral summand, independent of Sigma formulas.
seed=json.loads(Path('scripts/op03_gap_table.json').read_text()); sector_report=[]
for n in [2,3]:
    for mode in ['sup','inf']:
        rc=Recon(n,4.,mode); edges=np.array(seed[f'n{n}_{mode.upper()}']['edges'])
        z=symmetric_root(rc,rc.widths_to_z(np.diff(np.r_[0.,edges,1.])))
        ed=eigen_data(rc,z); a,b=ed['lam_n'],ed['lam_np1']; u,up,eps=ed['u_n'],ed['u_np1'],ed['eps']; gap=b-a
        eye=np.eye(2*n); be=(eye[:,:n]+eye[:,::-1][:,:n])/np.sqrt(2); bo=(eye[:,:n]-eye[:,::-1][:,:n])/np.sqrt(2)
        sg=np.diag(eps); eh=np.diag(eps[:n]); jumps=np.diff(rc.pat)
        diagonal=(2*a*u*ed['up_n']-2*b*up*ed['up_np1'])/(b*jumps)
        rank=2*a*gap/b**2*np.outer(eps*u*u,eps*u*u)
        pair=2*a*(-np.outer(u*u,u*u)/gap-(a/b)*np.outer(eps*u*up,eps*u*up)/gap)
        for trunc in [n+1,20,80,160]:
            roots=roots_of(rc.blocks_from_z(z),trunc+1); rest=np.zeros((2*n,2*n))
            for j,w in enumerate(roots):
                if j in [n-1,n]: continue
                v=eigfun(rc.blocks_from_z(z),w,ed['edges']); p=u*v; q=eps*u*v
                rest+=2*a*(np.outer(p,p)/(w*w-b)-(a/b)*np.outer(q,q)/(w*w-a))
            add=rank+pair; raw=np.diag(diagonal)+add+rest
            data=sector_data(rc,z,N=trunc); full=np.diag(1/jumps)@analytic_jacobian_spectral(rc,z,N=trunc)
            refs={'Ke':be.T@raw@be,'Ko':bo.T@raw@bo,'He':be.T@rest@be,'Ho':bo.T@rest@bo,'Ee':be.T@add@be,'Eo':bo.T@add@bo,'KpEven':be.T@sg@raw@sg@be,'KpOdd':bo.T@sg@raw@sg@bo,'KpHe':be.T@sg@rest@sg@be,'KpHo':bo.T@sg@rest@sg@bo,'KpEe':be.T@sg@add@sg@be,'KpEo':bo.T@sg@add@sg@bo}
            errors={key:float(np.max(abs(np.array(data[key])-value))) for key,value in refs.items()}
            errors['full-J']=float(np.max(abs(full-raw)))
            check(f'independent-summand-sectors {n} {mode} {trunc}',max(errors.values())<3e-8,errors)
            check(f'coefficient-metadata {n} {mode} {trunc}',data['coefficient_target']=='c_e/c_o belong to KpEe/KpEo')
            wh=a*u[:n]**2
            check(f'legacy-coefficient-values {n} {mode} {trunc}',np.max(abs(np.array(data['KpEe'])-data['c_e']*np.outer(wh,wh)))<1e-13 and np.max(abs(np.array(data['KpEo'])-data['c_o']*np.outer(eps[:n]*wh,eps[:n]*wh)))<1e-13)
            sector_report.append(dict(n=n,mode=mode,N_argument=trunc,actual_modes=trunc+1,errors=errors))
        reject(f'sector-short-prefix {n} {mode}',lambda:sector_data(rc,z,N=n))
        zz=z.copy();zz[0]+=.01
        reject(f'sector-nonstationary {n} {mode}',lambda:sector_data(rc,zz,N=20))

for name in ['_gapn2_half_debug2','_gapn2_half_debug3']:
    mod=importlib.import_module(name)
    check('legacy-module-import '+name,mod.half_spectrum is H.half_spectrum and mod._spectral_green is H._spectral_green)

# Known-unresolvable finite-denominator regression: a finite result is invalid here.
blocks=[(1.,1e-306)]; table=H.half_spectrum(blocks,'D',4,return_table=True); mu=-np.finfo(float).max
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter('always')
    try:
        value=H._spectral_full_green(blocks,mu,'D',.25,.25,4,spectrum=table)
    except ArithmeticError as e: check('full-denominator-overflow-rejected',True,str(e))
    else:
        exact=sum(2*mp.sin(k*mp.pi/4)**2/(k*k*mp.pi**2-mp.mpf(blocks[0][1])*mp.mpf(mu)) for k in range(1,5))
        check('full-denominator-overflow-rejected',False,dict(returned=value,independent_finite_sum=str(exact),warnings=[str(w.message) for w in caught]))
result=dict(passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),max_layer_relative_error=max(layer_report),max_trig_sum_error=max_sum_error,sector_report=sector_report,checks=checks)
Path('../evidence/independent-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','sector_report']},indent=2))
print(json.dumps([c for c in checks if c['status']=='FAIL'],indent=2))
