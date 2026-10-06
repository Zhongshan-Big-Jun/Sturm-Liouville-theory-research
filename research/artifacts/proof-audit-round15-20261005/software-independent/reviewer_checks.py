from pathlib import Path
import sys, json, hashlib, math, warnings, platform, time
import numpy as np
import mpmath as mp

ROOT=Path('F:/tools/math-audit-round15-20261005/review-input/software')
OUT=Path('F:/tools/math-audit-round15-20261005/reviews/software-run')
sys.path.insert(0, str(ROOT/'scripts'))
import op03_gap_fixed as O
import _sl_prufer as P

CHECKS=[]; DATA={}
def require(name, condition, detail=None):
    if not bool(condition):
        CHECKS.append(dict(name=name,ok=False,detail=detail))
        raise RuntimeError(name)
    CHECKS.append(dict(name=name,ok=True,detail=detail))
    print('PASS '+name,flush=True)
def reject(name, fn, kind=ValueError):
    try: fn()
    except kind as e:
        require(name,True,dict(type=type(e).__name__,message=str(e)));return
    require(name,False,'required rejection did not occur')

def mat(length,rho,w):
    q=w*mp.sqrt(rho);c=mp.cos(q*length);s=mp.sin(q*length)
    return mp.matrix([[c,s/q],[-q*s,c]])
def states(blocks,w):
    vals=[mp.matrix([[1,0],[0,1]])]
    for l,r in blocks: vals.append(mat(l,r,w)*vals[-1])
    return vals
def endpoint(blocks,w): return states(blocks,w)[-1][0,1]
def root_bisect(blocks,seed):
    lo=mp.mpf(float(seed))*(1-mp.mpf('1e-7'))
    hi=mp.mpf(float(seed))*(1+mp.mpf('1e-7'))
    fl=endpoint(blocks,lo);fh=endpoint(blocks,hi)
    if not fl*fh<0: raise RuntimeError('physical local root is not independently bracketed')
    for _ in range(220):
        mid=(lo+hi)/2;fm=endpoint(blocks,mid)
        if fm==0:return mid
        if fm*fl>0:lo=mid;fl=fm
        else:hi=mid
    return (lo+hi)/2

def zeros(blocks,w,st):
    ans=[];x=mp.mpf(0);L=sum(l for l,r in blocks);tol=mp.mpf('1e-55')
    for (l,r),s in zip(blocks,st):
        q=w*mp.sqrt(r);phi=mp.atan2(s[0,1],s[1,1]/q)
        for j in range(int(mp.floor(phi/mp.pi))-1,int(mp.ceil((phi+q*l)/mp.pi))+2):
            z=x+(j*mp.pi-phi)/q
            if x-tol<=z<=x+l+tol and tol<z<L-tol:
                if all(abs(z-a)>tol for a in ans):ans.append(z)
        x+=l
    return sorted(ans)

def physical(blocks,w,points):
    st=states(blocks,w);mass=mp.mpf(0);L=mp.mpf(0)
    for (l,r),s in zip(blocks,st):
        y,dy=s[0,1],s[1,1];q=w*mp.sqrt(r)
        mass+=r*mp.quad(lambda t:(y*mp.cos(q*t)+dy*mp.sin(q*t)/q)**2,[0,l])
    ends=[mp.mpf(0)]
    for l,r in blocks: ends.append(ends[-1]+l)
    vals=[]
    for p in points:
        pp=mp.mpf(float(p));i=min(max(j for j in range(len(blocks)) if ends[j]<=pp),len(blocks)-1)
        state=mat(pp-ends[i],blocks[i][1],w)*st[i]
        vals.append(state[0,1]/mp.sqrt(mass))
    return st,mass,vals,zeros(blocks,w,st)

def main():
    manifest=json.loads((ROOT/'hashes.json').read_text(encoding='utf-8'))
    actual={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in manifest}
    require('input_manifest_11_matches',len(actual)==11 and actual==manifest,actual)
    DATA['input_sha256']=actual
    cases={'high_contrast':[(.021,10000.),(.958,1.),(.021,10000.)],
           'R4_control':[(.3,1.),(.4,4.),(.3,1.)],
           'homogeneous':[(1.,1.)],
           'tiny_positive_blocks':[(1e-12,3.),(1-2e-12,1.),(1e-12,7.)]}
    originals={};records=[]
    real=P.indexed_roots
    def spy(*args,**kwargs):
        result=real(*args,**kwargs)
        records.append(dict(blocks=np.asarray(args[0]).tolist(),count=int(args[1]),Refine=kwargs.get('Refine'),RightBoundary=kwargs.get('RightBoundary'),records=result[1]))
        return result
    P.indexed_roots=spy
    try:
        for label,b in cases.items():
            n=6 if label=='high_contrast' else 3
            roots=O.lams_precise(b,n)
            originals[label]=roots
            require('direct_exact_count_'+label,len(roots)==n and np.all(np.diff(roots)>0))
            require('delegated_DD_'+label,records[-1]['count']==n and records[-1]['RightBoundary']=='D')
            require('default_tol_bracket_'+label,all(t['bracket'][1]-t['bracket'][0]<=1e-15*max(1,t['frequency']) for t in records[-1]['records']))
        for k in (np.int64(1),3,6):
            require('bitwise_prefix_'+str(k),np.array_equal(O.lams_precise(cases['high_contrast'],k),originals['high_contrast'][:int(k)]))
        for tol in (1e-8,1e-15,.5):
            roots=O.lams_precise(cases['high_contrast'],6,tol=tol)
            require('direct_tol_width_'+str(tol),all(t['bracket'][1]-t['bracket'][0]<=tol*max(1,t['frequency']) for t in records[-1]['records']))
            require('loose_tol_keeps_indices_'+str(tol),np.array_equal(roots,originals['high_contrast']))
    finally:P.indexed_roots=real
    DATA['backend_calls']=records
    require('omega_not_lambda_homogeneous',np.max(abs(originals['homogeneous']-np.pi*np.arange(1,4)))<2e-14)
    for scale in (.001,2.,5.,1e5):
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter('always');rr=O.lams_precise(cases['high_contrast'],6,smax_scale=scale)
        require('scale_compatibility_'+str(scale),np.array_equal(rr,originals['high_contrast']) and len(ws)==(0 if scale==5. else 1) and all(issubclass(w.category,DeprecationWarning) for w in ws))
    # Intentional backend faults: validate wrapper's return units and fail-closed tol handling.
    def sentinel(*args,**kwargs):
        return np.array([.5,3.5]),[dict(bracket=[.5,.5]),dict(bracket=[3.5,3.5])]
    P.indexed_roots=sentinel
    try: require('negative_squaring_mutation_guard',np.array_equal(O.lams_precise([(1.,1.)],2),[.5,3.5]))
    finally:P.indexed_roots=real
    def too_wide(*args,**kwargs):
        return np.array([1.]),[dict(bracket=[.9,1.1])]
    P.indexed_roots=too_wide
    try:reject('injected_unresolved_backend_width_rejected',lambda:O.lams_precise([(1.,1.)],1,tol=1e-8),ArithmeticError)
    finally:P.indexed_roots=real
    def broken(*args,**kwargs):raise ArithmeticError('intentional independent engine failure')
    P.indexed_roots=broken
    try:reject('backend_failure_propagates_without_scan_fallback',lambda:O.lams_precise([(1.,1.)],1),ArithmeticError)
    finally:P.indexed_roots=real
    reject('actual_unresolved_tol_rejected',lambda:O.lams_precise([(1.,1.)],3,tol=1e-30),ArithmeticError)
    for k in (np.bool_(True),np.float64(3),0,-2,math.nan,None,[1]):
        reject('independent_bad_count_'+repr(k),lambda k=k:O.lams_precise([(1.,1.)],k))
    for name in ('tol','smax_scale'):
        for v in (np.bool_(True),np.complex128(1),np.float64(math.nan),np.float64(math.inf),-1,0,None):
            reject('independent_bad_'+name+'_'+repr(v),lambda name=name,v=v:O.lams_precise([(1.,1.)],1,**{name:v}))
    for b in ([[(1+0j),1]],np.array([[1.,1.],[np.inf,1.]]),[[1.,1.],[1e-20,1.]],[[1.,1.],[1e-12,0.]]):
        reject('independent_bad_geometry_'+repr(b),lambda b=b:O.lams_precise(b,1))
    # Independent mp full physical transfer and mass quadrature, no project reference import.
    with mp.workdps(80):
        for label,b in cases.items():
            mb=[(mp.mpf(float(l)),mp.mpf(float(r))) for l,r in b]
            L=sum(l for l,r in b)
            points=[L,.2*L,.37*L,0.,.63*L,.91*L]+list(np.cumsum(np.array(b)[:,0])[:-1])
            table=O.eigfuns_precise(b,originals[label],np.array(points))
            mode_records=[];matrix_error=0.;sample_error=0.;mass_error=0.
            for i,seed in enumerate(originals[label],1):
                w=root_bisect(mb,seed);st,mass,vals,zs=physical(mb,w,points)
                require('physical_index_'+label+'_'+str(i),len(zs)==i-1,len(zs))
                require('physical_root_'+label+'_'+str(i),abs(float(w)-seed)<2e-12*max(1,seed),dict(omega=mp.nstr(w,25),error=abs(float(w)-seed)))
                sample_error=max(sample_error,max(abs(table[i-1,j]-float(v)) for j,v in enumerate(vals)))
                ds=O.prop_to(b,float(w))
                for d,s in zip(ds,st):
                    dm=np.array(d[1:]).reshape(2,2)
                    matrix_error=max(matrix_error,max(abs(dm[j,k]-float(s[j,k]))/max(1.,abs(float(s[j,k]))) for j in range(2) for k in range(2)))
                # Block Gauss integration of actual eigfuns, independent of its closed normalization.
                gx,gw=np.polynomial.legendre.leggauss(48);integ=0.;start=0.
                for l,r in b:
                    xx=start+l*(gx+1)/2;vv=O.eigfuns_precise(b,[float(seed)],xx)[0]
                    integ+=r*l/2*np.dot(gw,vv*vv);start+=l
                mass_error=max(mass_error,abs(integ-1))
                mode_records.append(dict(index=i,omega=mp.nstr(w,50),eigenvalue=mp.nstr(w*w,50),internal_zero_count=len(zs),right_residual=mp.nstr(st[-1][0,1],10),mass=mp.nstr(mass,30)))
            require('physical_prop_to_multiplication_'+label,matrix_error<1e-11,matrix_error)
            require('physical_normalized_samples_'+label,sample_error<1e-10,sample_error)
            require('quadrature_actual_weighted_mass_'+label,mass_error<2e-11,mass_error)
            DATA[label]=dict(frequencies=originals[label].tolist(),modes=mode_records,matrix_error=matrix_error,sample_error=sample_error,mass_error=mass_error)
        b=cases['high_contrast'];mb=[(mp.mpf(float(l)),mp.mpf(float(r))) for l,r in b]
        omitted=originals['high_contrast'][2:4]
        counts=[len(zeros(mb,root_bisect(mb,w),states(mb,root_bisect(mb,w)))) for w in omitted]
        require('negative_omitted_first_pair_is_rejected_as_indices_1_2',counts==[2,3],counts)
        wrong=originals['homogeneous']**2
        residuals=[abs(endpoint([(mp.mpf(1),mp.mpf(1))],mp.mpf(float(w)))) for w in wrong]
        require('negative_lambda_as_omega_fails_DD',min(residuals)>mp.mpf('1e-4'),list(map(float,residuals)))
        # Explicit single scan-cell endpoint values: two verified DD roots leave the same endpoint sign.
        smax=math.pi*100*5+20;step=(smax-1e-7)/29999
        rootpair=originals['high_contrast'][:2]
        cell=int((rootpair[0]-1e-7)//step)
        aa=mp.mpf(float(1e-7+cell*step));bb=mp.mpf(float(1e-7+(cell+1)*step))
        fa,fb=endpoint(mb,aa),endpoint(mb,bb)
        require('negative_single_sign_cell_hides_two_first_DD_roots',aa<rootpair[0]<rootpair[1]<bb and fa*fb>0,dict(cell=[float(aa),float(bb)],endpoint_values=[mp.nstr(fa,25),mp.nstr(fb,25)]))
    # Thin blocks remain exactly supplied instead of being clipped to a fixed width floor.
    thin=cases['tiny_positive_blocks']
    returned=P.positive_blocks(thin)
    require('no_width_floor_or_repair',np.array_equal(returned,np.array(thin)) and returned[0,0]<1e-7)
    imported={n:str(Path(m.__file__).resolve()) for n,m in list(sys.modules.items()) if getattr(m,'__file__',None) and (n.startswith('_sl_') or n.startswith('op03_'))}
    require('frozen_project_import_provenance',all(str(ROOT).lower() in p.lower() for p in imported.values()),imported)
    DATA['imported_project_modules']=imported

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();started=time.time();error=None
    try:main()
    except Exception as e:error=dict(type=type(e).__name__,message=str(e))
    result=dict(task_name='/root/r15_software_review',python=sys.version,platform=platform.platform(),optimized=not __debug__,seconds=time.time()-started,test_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),count=len(CHECKS),passed=sum(x['ok'] for x in CHECKS),checks=CHECKS,data=DATA,error=error,scope='Independent finite software and physical diagnostic checks; no Lean, interval certification or tool-library reception.')
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(dict(count=result['count'],passed=result['passed'],error=error)),flush=True)
    if error:raise SystemExit(1)
