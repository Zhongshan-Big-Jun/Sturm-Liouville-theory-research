from pathlib import Path
from fractions import Fraction as F
import hashlib, importlib.util, json, math, sys, time
import numpy as np
import mpmath as mp
import _sl_prufer as sl
import _gapn2_symmetry_recon as recon
import _gapn2_second_variation_probe as probe
import reflection_seeds as seeds
root=Path(__file__).resolve().parent.parent
sys.set_int_max_str_digits(100000)
rows=[]
def record(name,ok,detail=None):
    rows.append(dict(name=name,passed=bool(ok),detail=detail))
    if not ok: print('FAILED',name,detail,flush=True)
def rejects(name,fn,types=(ValueError,ArithmeticError)):
    try: value=fn()
    except types as e: record(name,True,dict(type=type(e).__name__,message=str(e))); return e
    except Exception as e: record(name,False,dict(unexpected=type(e).__name__,message=str(e))); return e
    record(name,False,dict(returned=str(value))); return None

def physical(blocks,w,dps=85):
    with mp.workdps(dps):
        w=mp.mpf(w); y=mp.mpf(0); yp=mp.mpf(1); count=0; x=mp.mpf(0); locations=[]
        for length,density in blocks:
            length=mp.mpf(float(length)); density=mp.mpf(float(density)); k=w*mp.sqrt(density)
            a,b=y,yp/k
            offset=mp.atan2(a,b)
            for j in range(int(mp.floor(offset/mp.pi))-1,int(mp.ceil((offset+k*length)/mp.pi))+2):
                t=(j*mp.pi-offset)/k
                if 0<t<=length:
                    count+=1; locations.append(mp.nstr(x+t,25))
            co,si=mp.cos(k*length),mp.sin(k*length)
            y,yp=a*co+b*si,k*(-a*si+b*co)
            scale=max(abs(y),abs(yp)); y,yp=y/scale,yp/scale; x+=length
        return count, float(y), locations

# Old callable only, no historical main.
spec=importlib.util.spec_from_file_location('_gapn2_before_symmetry_recon',root/'before/_gapn2_symmetry_recon.py')
old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)
cluster=[(.02,10000.),(.96,1.),(.02,10000.)]
legacy=old.roots_of(cluster,2); modern,metadata=sl.indexed_roots(cluster,8)
record('legacy-failure-recomputed-new-low-prefix',abs(legacy[0]-3.2671480773046255)<1e-13 and modern[3]<legacy[0],dict(old=legacy.tolist(),new=modern.tolist(),old_first_physical_zeros=physical(cluster,float(legacy[0]))[0]))

# Exact rational endpoint enclosures, rebuilt independently by full state propagation.
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):
    p=[x*y for x in a for y in b];return min(p),max(p)
def scale(a,c):return mul(a,(c,c))
def trig(x,cosine):
    v=sum(((-1)**(k//2))*x**k/F(math.factorial(k)) for k in range(0 if cosine else 1,81,2))
    err=abs(x)**81/F(math.factorial(81));return v-err,v+err
brackets=[('0.783424012239','0.783424012240'),('0.797807654414','0.797807654415'),('2.345707847544','2.345707847545'),('2.358540421082','2.358540421083')]
certificates=[]
for kind,lengths in [('decimal-rational',[F('0.02'),F('0.96'),F('0.02')]),('binary64-rational',[F(.02),F(.96),F(.02)])]:
    for idx,pair in enumerate(brackets,1):
        bounds=[]
        for endpoint in pair:
            frequency=F(endpoint); y=(F(0),F(0)); yp=(F(1),F(1))
            for length,rd in zip(lengths,[100,1,100]):
                k=frequency*rd; c=trig(k*length,True); s=trig(k*length,False)
                y,yp=add(mul(c,y),scale(mul(s,yp),1/k)),add(scale(mul(s,y),-k),mul(c,yp))
            sign=1 if y[0]>0 else -1 if y[1]<0 else 0
            bounds.append(dict(endpoint=endpoint,sign=sign,lower=str(y[0]),upper=str(y[1])))
        ok=bounds[0]['sign']*bounds[1]['sign']==-1
        record(f'exact-rational-physical-bracket-{kind}-{idx}',ok,dict(signs=[b['sign'] for b in bounds]))
        certificates.append(dict(kind=kind,index=idx,bounds=bounds))
(root/'results/rebuilt-rational-brackets.json').write_text(json.dumps(certificates,indent=2))

# Exact interface-zero seams and power-of-two changes in the physical scales.
for b in [[(1.,1.),(1.,4.)],[(.25,4.),(.5,1.),(.25,4.)],[(.5,1.),(.5,1.)]]:
    rt,rec=sl.indexed_roots(b,25)
    counts=[physical(b,float(rt[j-1]+.43*(rt[j]-rt[j-1])))[0] for j in range(1,len(rt))]
    record('interface-zero-seams-'+str(b),counts==list(range(1,len(rt))),dict(roots=rt.tolist(),nodal_counts=counts))
    for factor in [2.**-20,2.**20]:
        rr=sl.indexed_roots([(l*factor,c) for l,c in b],25)[0]
        record('length-scaling-'+str((b,factor)),np.allclose(rr*factor,rt,rtol=3e-13,atol=0))
    for factor in [2.**-30,2.**30]:
        rr=sl.indexed_roots([(l,c*factor) for l,c in b],25)[0]
        record('density-power-scaling-'+str((b,factor)),np.allclose(rr*np.sqrt(factor),rt,rtol=3e-13,atol=0))
for density in [1e-300,1e-100,1e100,1e300]:
    rr=sl.indexed_roots([(.25,density),(.75,density)],16)[0]
    exact=np.arange(1,17)*np.pi/np.sqrt(density)
    record('extreme-constant-'+str(density),np.allclose(rr,exact,rtol=3e-14,atol=0))

rng=np.random.default_rng(870391)
for case in range(18):
    b=list(zip(rng.dirichlet(np.ones(7)).tolist(),np.exp(rng.uniform(-5,8,7)).tolist()))
    rt,rec=sl.indexed_roots(b,19)
    counts=[physical(b,float(rt[0]*.413))[0]]+[physical(b,float(rt[j-1]+.413*(rt[j]-rt[j-1])))[0] for j in range(1,19)]
    record(f'independent-nodal-prefix-{case}',counts==list(range(19)),dict(blocks=b,roots=rt.tolist(),counts=counts))
    reflected=sl.indexed_roots(b[::-1],19)[0]
    split=sl.indexed_roots([(l/2,c) for l,c in b for _ in range(2)],19)[0]
    record(f'reflection-split-{case}',np.allclose(rt,reflected,rtol=2e-11,atol=1e-13) and np.allclose(rt,split,rtol=2e-11,atol=1e-13))

for b in [[(1.,1.),(1e-30,1.)],[(1e308,1.),(1e308,1.)],[(1e-300,1e-300)],[(1.,1e-320),(1.,1e308)],[(1.,float('inf'))]]:
    rejects('unresolved-blocks-'+str(b),lambda b=b:sl.indexed_roots(b,2))
for n,refine in [(True,60),(3,False),(1,0),(0,60),(2.,60),(2,2.)]:
    rejects('invalid-count-refine-'+str((n,refine)),lambda n=n,refine=refine:sl.indexed_roots(cluster,n,refine))
for w in [-1,float('inf'),float('nan'),1j]:rejects('invalid-phase-frequency-'+str(w),lambda w=w:sl.lifted_phase(cluster,w))
rejects('winding-bound',lambda:sl.indexed_roots([(1.,1.),(1.,1e28)],2))
rejects('insufficient-refinement',lambda:sl.indexed_roots(cluster,5,10))
record('D-scalar-zero-length-limit',recon.D_scalar([(2.,7.),(.5,31.)],0)==2.5)

# Consumer mode labels and same-index recovery in genuinely different cases.
with mp.workdps(75):
    precise=[(mp.mpf(l),mp.mpf(c)) for l,c in cluster]
    refined=[]
    for index in range(1,9):
        w,segments,mass=probe.refine_mp_root(precise,float(modern[7 if index<5 else 0]),75,index)
        refined.append(w)
        end=probe.mp_state(precise,w)[0]
        record('wrong-guess-retains-mode-'+str(index),abs(sl.mp_lifted_phase(precise,w)-index*mp.pi)<mp.mpf('1e-60') and abs(end)<mp.mpf('1e-60') and mass>0,dict(index=index,root=mp.nstr(w,65)))
    for n in [1,2,4]:
        tangent=probe.HighPrecisionTangent(cluster,n,75)
        record('tangent-index-'+str(n),all(abs(tangent.modes[j][0]-refined[n-1+j])<mp.mpf('1e-65') for j in range(2)))
    for index in range(5):
        fd,base,plus,minus=probe.fd_second(cluster,[c for _,c in cluster],index,h=.002,dps=75)
        h=mp.mpf(.002);expected=2*base/(1-h*h)
        record('fd-scaling-mode-'+str(index+1),abs(base-refined[index]**2)<mp.mpf('1e-60') and abs(plus-base/(1+h))<mp.mpf('1e-60') and abs(minus-base/(1-h))<mp.mpf('1e-60') and abs(fd-expected)<mp.mpf('1e-55'),dict(fd=mp.nstr(fd,55),mode=index+1))
actual_probe=probe.SpectralProbe(cluster,8,48)
record('spectral-probe-prefix',np.array_equal(actual_probe.roots,modern))
old_roots=probe.roots_of
try:
    for bad in [modern[1:4],modern[[0,2,3]],modern[:2]]:
        probe.roots_of=lambda *args,bad=bad,**kw:bad.copy()
        rejects('checked-roots-reject-missing-index-'+str(bad.tolist()),lambda:probe.checked_roots(cluster,3))
finally:probe.roots_of=old_roots
rejects('fd-nonpositive-endpoint',lambda:probe.fd_second([(1.,1.)],[2.],0,h=1,dps=60))
for metric in ['euclidean','width-weighted']:
    a=np.array([1.,-2.,4.])*1e-300;coeff=np.array([.2,.7,-.3]);width=np.array([.1,.2,.7])
    projected=probe.project_tangent(coeff,a,width,metric)
    record('true-integral-projection-tiny-'+metric,abs(float(projected@np.array([1.,-2.,4.])))<1e-14)

# Full imported Recon callbacks, geometric -J identities, evidence retention.
rc=recon.Recon(2,4,'sup');base=np.array([.1,.3,.7,.9])
seed_rows=[]
for sector in ['preserve','break']:
    for step in [1e-5,.2,10.]:
        s=seeds.generate_sector_seed(base,sector,step,Vector=[1,4,2,7],WidthsToZ=rc.widths_to_z,ZToWidths=rc.z_to_widths)
        actual=np.cumsum(rc.z_to_widths(s.Z))[:-1];d=actual-np.array(s.BaseEdges)
        sign=-1 if sector=='preserve' else 1
        reflected=1-actual[::-1];expected=actual if sector=='preserve' else 2*np.array(s.BaseEdges)-actual
        record(f'full-Recon-actual-sector-{sector}-{step}',np.max(np.abs(d-sign*d[::-1]))<=2e-8*np.max(np.abs(d)) and np.allclose(reflected,expected,rtol=0,atol=2e-15) and np.max(np.abs(d))>32*np.finfo(float).eps and min(s.Widths)>1e-7 and s.Evidence['Halvings']<=80,s.to_dict())
        seed_rows.append(s.to_dict())
    v=[1,3,3,1] if sector=='preserve' else [1,3,-3,-1]
    rejects('zero-vector-projection-'+sector,lambda:seeds.generate_sector_seed(base,sector,.1,Vector=v),(seeds.ZeroProjectionError,))
    err=rejects('bounded-large-step-'+sector,lambda:seeds.generate_sector_seed(base,sector,1e100,Vector=[1,4,2,7],MaxHalvings=4),(seeds.SeedGenerationError,))
    record('bounded-large-evidence-'+sector,err is not None and len(err.Evidence['Attempts'])==5)
    rejects('too-small-step-'+sector,lambda:seeds.generate_sector_seed(base,sector,1e-300,Vector=[1,4,2,7]),(seeds.SeedGenerationError,))
class Zeros:
    def __init__(self):self.count=0
    def standard_normal(self,size):self.count+=1;return np.zeros(size)
zrng=Zeros();err=rejects('bounded-resampling',lambda:seeds.generate_sector_seed(base,'break',.1,Rng=zrng,MaxResamples=5),(seeds.SeedGenerationError,))
record('bounded-resampling-count',zrng.count==5 and len(err.Evidence['Draws'])==5)
bad_center=np.array([.1,.31,.7,.9]);jobs,records=recon.sector_jobs(rc,bad_center,np.random.default_rng(12),1,1)
record('sector-jobs-reject-asymmetric-center',not jobs and len(records)==10 and all(r['status']=='rejected_seed' for r in records),records)
(root/'results/adversarial-seeds.json').write_text(json.dumps(seed_rows,indent=2))
(root/'results/asymmetric-table.json').write_text(json.dumps({'n2_SUP':{'edges':bad_center.tolist()},'n2_INF':{'edges':bad_center.tolist()}}))
report={'status':'PASS' if all(x['passed'] for x in rows) else 'FAIL','count':len(rows),'checks':rows,'scope':'independent finite behavior checks and rebuilt exact rational endpoint signs; no universal floating-point or interval root-index certification'}
(root/'results/adversarial.json').write_text(json.dumps(report,indent=2,allow_nan=False))
print(json.dumps({'status':report['status'],'count':len(rows),'failures':[x for x in rows if not x['passed']]}),flush=True)
