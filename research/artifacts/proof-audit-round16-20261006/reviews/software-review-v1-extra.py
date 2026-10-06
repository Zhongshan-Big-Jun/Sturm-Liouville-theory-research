"""Independent Round 16 software checks; only the frozen 15-file package.

The oracle for local integrals uses 90-digit physical transfers and direct
tanh-sinh integration, or closed-form constant-density eigenfunctions.
No assertions are used for acceptance so -O has the same acceptance logic.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import ast
import hashlib
import importlib
import json
import math
import platform
import sys
import time
import warnings

import mpmath as mp
import numpy as np

ROOT = Path('F:/tools/math-audit-round16-20261006/software-review-v1/root')
BASE = ROOT.parent.parent
sys.path.insert(0, str(ROOT/'misc'))
sys.path.insert(0, str(ROOT/'scripts'))
T = importlib.import_module('rigid1d')
V = importlib.import_module('_gapn2_second_variation_probe')
S = importlib.import_module('_gapn2_symmetry_recon')
P = importlib.import_module('_sl_prufer')
I = importlib.import_module('_sl_spectral_identity')
J = importlib.import_module('_gapn2_jacobian_probe')
JA = importlib.import_module('_gapn2_jacobian_analytic')
JS = importlib.import_module('_gapn2_jacobian_spectral')
E = importlib.import_module('e1_certgen')
EIO = importlib.import_module('e1_certificate_io')
O = importlib.import_module('op03_gap_fixed')

ROWS = []


def check(name, condition, **details):
    passed = bool(condition)
    ROWS.append(dict(name=name, passed=passed, **details))
    if not passed:
        print('FAIL', name, details, flush=True)


def rejects(name, fn, types=(TypeError, ValueError, ArithmeticError)):
    try:
        fn()
    except types as exc:
        check(name, True, error_type=type(exc).__name__, error=str(exc))
        return str(exc)
    except Exception as exc:
        check(name, False, error_type=type(exc).__name__, error=str(exc))
        return str(exc)
    else:
        check(name, False, error='returned rather than rejecting')
        return None


def exact_poly_checks():
    false_int = lambda z: (z-z*z/2)/15-F(1,2**62)*z
    false_adj = lambda z: (1+F(3,2**54))*z-z*z/2
    # Explicit exact derivatives at the vulnerable right endpoints.
    check('integer counterexample has negative exact endpoint derivative', -F(1,2**62)<0)
    check('adjacent float counterexample has negative exact endpoint derivative', 1+F(3,2**54)-F(math.nextafter(1.,2.)) == -F(1,2**54))
    for name, fn, a, b, count in (
        ('integer', false_int, 0, 1, 3),
        ('rational-offset', lambda z: false_int(z-F(2,7)), F(2,7), F(9,7), 5),
        ('adjacent-float', false_adj, 1., math.nextafter(1.,2.), 1),
    ):
        result = T.der_sign2(fn,a,b,True,base_n=count,max_n=count)
        check('independent false Taylor '+name, result[0] is False, result=str(result))
        result = T.der_sign_adaptive(fn,a,b,True,max_boxes=37)
        check('independent false adaptive '+name, result[0] is False, result=str(result))
    fn = lambda z: 3*z-z*z/7
    for left, right in ((F(0),F(1,3)),(F(-2,5),F(7,13)),(F(1),F(math.nextafter(1.,2.)))):
        lower, upper, bound = T._derivative_bounds(fn,left,right)
        check('exact center halfwidth Taylor bound '+str((left,right)),
              (lower,upper,bound)==(3-2*right/7,3-2*left/7,F(2,7)),
              exact_bounds=list(map(str,(lower,upper,bound))))
    seen=[]
    def tracked(z):
        seen.append((z.v.lo,z.v.hi))
        return z+z*z
    yes=T.der_sign2(tracked,F(-1,4),F(3,4),True,base_n=7,max_n=7)
    expected=[]
    for idx in range(7):
        left, right=F(-1,4)+F(idx,7), F(-1,4)+F(idx+1,7)
        expected.extend(((left,right),((left+right)/2,(left+right)/2)))
    check('seven nonbinary cells and centers exactly cover declared domain',yes[0] and seen==expected)
    for budget in (1,2,3,4,8,13):
        calls=[]
        def unresolved(z):
            calls.append((z.v.lo,z.v.hi))
            return z*z
        result=T.der_sign_adaptive(unresolved,-1,1,True,max_boxes=budget,min_w=F(1,2**100))
        check('adaptive exact budget '+str(budget),result[0] is False and len(calls)<=2*budget,
              callbacks=len(calls),maximum_callbacks=2*budget,result=str(result))
    for kw in (dict(max_n=0),dict(max_n=True),dict(max_n=2.0),dict(base_n=False),dict(base_n=8,max_n=7)):
        rejects('invalid uniform parameter '+str(kw),lambda kw=kw:T.der_sign2(lambda z:z,0,1,True,**kw))
    for kw in (dict(max_boxes=F(1)),dict(max_boxes=np.int64(3)),dict(min_w=float('nan')),dict(min_w=complex(.1)),dict(min_w=F(3,2))):
        rejects('invalid adaptive parameter '+str(kw),lambda kw=kw:T.der_sign_adaptive(lambda z:z,0,1,True,**kw))
    for fn in (T.der_sign2,T.der_sign_adaptive):
        rejects('nonbool requested sign '+fn.__name__,lambda fn=fn:fn(lambda z:z,0,1,1))
        rejects('noncallable function '+fn.__name__,lambda fn=fn:fn(None,0,1,True))
    for a,b,fn,positive in ((F(-2),F(-1),lambda z:z*z,False),(-1,2,lambda z:3*z+z**3,True),(1.,2.,lambda z:-z-z**3,False)):
        check('honest sign independent '+str((a,b,positive)),T.der_sign2(fn,a,b,positive,base_n=5,max_n=20)[0])
    names={node.id for node in ast.walk(ast.parse(Path(E.__file__).read_text(encoding='utf-8'))) if isinstance(node,ast.Name)}
    check('E1 specialized generator has no dependency on repaired sign helpers',not {'der_sign2','der_sign_adaptive'} & names)
    check('E1 named obligation contract still contains 57 unique facts',len(EIO.FACT_SPECS)==57 and len({x['name'] for x in EIO.FACT_SPECS})==57)
    okay,pieces=E._taylor(fn=lambda z:3*z-z*z/7,a=0,b=1,Comparison='gt',Target=0,n=3,Derivative=True)
    check('E1 independent exact Fraction partition',okay and
          [list(map(F,row['cell'])) for row in pieces]==[[F(k,3),F(k+1,3)] for k in range(3)] and
          [F(row['c']) for row in pieces]==[F(2*k+1,6) for k in range(3)] and
          all(F(row['corr_exact'])==F(1,21) for row in pieces))
    okay,pieces=E._taylor(false_int,0,1,'gt',0,3,True)
    check('E1 dedicated path rejects integer false derivative',not okay and F(pieces[-1]['bound_exact'][0]) == -F(1,2**62))


def mp_product_cell(wi,wj,length):
    with mp.workdps(90):
        wi,wj,length=mp.mpf(float(wi)),mp.mpf(float(wj)),mp.mpf(float(length))
        cosine=mp.quad(lambda x:mp.cos(wi*x)*mp.cos(wj*x),[-length/2,0,length/2])
        sine=mp.quad(lambda x:(mp.sin(wi*x)/wi)*(mp.sin(wj*x)/wj),[-length/2,0,length/2])
        return float(cosine),float(sine)


def local_integral_checks():
    for waves,length in (([.01,.2,1.3],.02),([1e-12,1e-5,1.,20.],.01),
                         ([99.,math.nextafter(99.,100.),199.],.03),([3.,5.,9.],2**-50)):
        waves=np.asarray(waves)
        cc,ss=V._cos_sin_integrals(waves,length)
        worst=0.
        for i in range(len(waves)):
            for j in range(i,len(waves)):
                ec,es=mp_product_cell(waves[i],waves[j],length)
                error=max(abs(cc[i,j]-ec)/max(abs(ec),1e-300),abs(ss[i,j]-es)/max(abs(es),1e-300))
                worst=max(worst,error)
        check('independent local small/close wave integrals '+str((waves.tolist(),length)),worst<2e-11,worst_relative_error=worst)
        check('local products symmetric '+str((waves.tolist(),length)),np.array_equal(cc,cc.T) and np.array_equal(ss,ss.T))


def constant_reference(coeff,edges,modes,density=1.):
    with mp.workdps(90):
        vals=np.zeros((modes,modes))
        energy=np.zeros(modes)
        for k in range(modes):
            wk=(k+1)*mp.pi
            for l in range(k,modes):
                wl=(l+1)*mp.pi
                c=mp.mpf(0)
                for h,a,b in zip(coeff,edges[:-1],edges[1:]):
                    a,b,h=mp.mpf(float(a)),mp.mpf(float(b)),mp.mpf(float(h))
                    value=mp.quad(lambda x:2/mp.mpf(density)*mp.sin(wk*x)*mp.sin(wl*x),[a,b])
                    c+=h*value
                    if k==l:
                        energy[k]+=float(h*h/mp.mpf(density)*value)
                vals[k,l]=vals[l,k]=float(c)
        return vals,energy


def mp_physical_reference(blocks,roots,coeff,edges):
    # This oracle propagates and integrates the original physical (0,1) IVP.
    with mp.workdps(90):
        segments=[]
        densities=[mp.mpf(c) for _,c in blocks]
        starts=[mp.mpf(0)]
        for length,_ in blocks:
            starts.append(starts[-1]+mp.mpf(length))
        def transfer(value,derivative,wave,offset):
            return (value*mp.cos(wave*offset)+derivative*mp.sin(wave*offset)/wave,
                    -value*wave*mp.sin(wave*offset)+derivative*mp.cos(wave*offset))
        for root in roots:
            row=[]; value=mp.mpf(0); derivative=mp.mpf(1); mass=mp.mpf(0)
            for idx,(length,density) in enumerate(blocks):
                length,density,root=mp.mpf(length),mp.mpf(density),mp.mpf(float(root))
                wave=root*mp.sqrt(density)
                a,b=value,derivative
                mass+=density*mp.quad(lambda t:(a*mp.cos(wave*t)+b*mp.sin(wave*t)/wave)**2,[0,length])
                row.append((a,b,wave))
                value,derivative=transfer(value,derivative,wave,length)
            segments.append((row,mass))
        allcuts=sorted(set(starts+[mp.mpf(float(x)) for x in edges]))
        def value_at(k,idx,x):
            a,b,wave=segments[k][0][idx]
            return (a*mp.cos(wave*(x-starts[idx]))+b*mp.sin(wave*(x-starts[idx]))/wave)/mp.sqrt(segments[k][1])
        n=len(roots); result=np.zeros((n,n)); energy=np.zeros(n)
        for left,right in zip(allcuts[:-1],allcuts[1:]):
            idx=max(i for i,s in enumerate(starts[:-1]) if s<=left)
            direction_idx=max(i for i,s in enumerate(edges[:-1]) if mp.mpf(float(s))<=left)
            height=mp.mpf(float(coeff[direction_idx]))
            for k in range(n):
                for l in range(k,n):
                    integral=mp.quad(lambda x:value_at(k,idx,x)*value_at(l,idx,x),[left,right])
                    result[k,l]+=float(height*integral)
                    if k==l:
                        energy[k]+=float(height**2/densities[idx]*integral)
        for k in range(n):
            for l in range(k):result[k,l]=result[l,k]
        return result,energy


def pairing_checks():
    negative_raw_seen=0
    for blocks in ([(1.,2.)],[(.25,2.)]*4):
        probe=V.SpectralProbe(blocks,61,64)
        result=probe.pairings(V.block_direction([2.]*len(blocks),probe.edges))
        lam,cu,cw,diag=result
        roots3=P.indexed_roots(blocks,3)[0]
        check('61 retained frequencies preserve exact indexed prefix '+str(len(blocks)),np.array_equal(probe.roots[:3],roots3))
        check('constant unweighted identity '+str(len(blocks)),np.max(abs(cu-np.eye(61)))<3e-12)
        check('rho-weighted pairing has distinct density factor '+str(len(blocks)),np.max(abs(cw-2*np.eye(61)))<6e-12)
        for n in (20,60):
            q=V.q_formula(lam,cu,cw,n,diag); target=(2*n+1)*math.pi**2/2
            check('independent 61-mode rho2 h2 Q '+str((len(blocks),n)),abs(q-target)<3e-8,Q=q,target=target)
        points=np.array([0.,.17,.5,.79,1.])
        for k in (0,19,59):
            states=S.eigenfunction_states(blocks,probe.roots[k],points)
            exact=np.column_stack((np.sin((k+1)*math.pi*points),(k+1)*math.pi*np.cos((k+1)*math.pi*points)))
            check('physical value derivative share mass '+str((len(blocks),k+1)),np.max(abs(states-exact))/max(1.,np.max(abs(exact)))<3e-13)
            check('eigfun is same shared normalized value '+str((len(blocks),k+1)),np.array_equal(states[:,0],S.eigfun(blocks,probe.roots[k],points)))
        raw=np.array(result.diagnostics['parseval_remainder_raw'])
        independent_raw=np.array(result.diagnostics['parseval_total_energy'])-np.sum(cu**2,axis=1)
        check('signed Parseval residual not silently truncated '+str(len(blocks)),np.array_equal(raw,independent_raw))
        negative_raw_seen+=int(np.count_nonzero(raw<0))
    check('roundoff-negative Parseval residues actually preserved',negative_raw_seen>0,count=negative_raw_seen)
    probe=V.SpectralProbe([(1.,2.)],61,64)
    for max_order in (64,128,255,256,512,1023):
        sampled=[]
        def callback(points):
            sampled.append(len(points));return np.full(len(points),2.)
        rejects('callback resolution/convergence budget '+str(max_order),lambda:probe.pairings(callback,MaxOrder=max_order))
        check('callback budget status remains unresolved '+str(max_order),probe.last_pairing_diagnostics is not None and probe.last_pairing_diagnostics['status']=='UNRESOLVED',diagnostics=probe.last_pairing_diagnostics)
        check('callback has no order above explicit budget '+str(max_order),all(count<=max_order for count in sampled),sample_orders=sampled)
    lam,cu,cw,diag,info=probe.pairings(lambda x:np.full(len(x),2.),return_diagnostics=True)
    check('ordinary callback explicitly reports estimated errors not enclosure',info['status']=='CONVERGED_NUMERICAL_ESTIMATE' and info['black_box_error_enclosure'] is None and info['sign_certified'] is False and info['spectral_tail_certification']=='NOT_CERTIFIED_FLOAT_INPUT',diagnostics=info)
    check('ordinary callback uses resolved finite order',info['order']==1024 and info['previous_order']==512)
    check('ordinary resolved callback Q60',abs(V.q_formula(lam,cu,cw,60,diag)-121*math.pi**2/2)<3e-8)
    # Direction breakpoints entirely inside one density block.
    for exponent in (40,50):
        delta=2.**-exponent
        for center in (.125,.375,.5,.875):
            direction=V.block_direction([0.,1/delta,0.],[0.,center,center+delta,1.])
            probe=V.SpectralProbe([(1.,1.)],4,64)
            lam,cu,cw,diag,info=probe.pairings(direction,return_diagnostics=True)
            reference,energy=constant_reference(direction.coefficients,direction.edges,4)
            check('new thin direction cuts included '+str((exponent,center)),info['intervals']==3)
            check('new thin direction recovers exact mass '+str((exponent,center)),F(float(direction.coefficients[1]))*(F(float(direction.edges[2]))-F(float(direction.edges[1])))==1)
            check('new thin direction local pairings independently matched '+str((exponent,center)),np.max(abs(cu-reference))<3e-12,error=float(np.max(abs(cu-reference))),C00=float(cu[0,0]))
            check('new thin direction Parseval energy independently matched '+str((exponent,center)),np.max(abs(np.array(info['parseval_total_energy'])-energy))/max(1.,np.max(abs(energy)))<3e-12)
            if exponent==50:
                rejects('ordinary new thin cut node collapse '+str(center),lambda:probe.pairings(lambda x:direction(x),direction.edges[1:-1]))
            else:
                points,weights,_=V.quadrature_rule(probe.blocks,64,direction.edges[1:-1])
                check('2^-40 ordinary positive control '+str(center),len(np.unique(points))==len(points) and abs(weights@direction(points)-1)<2e-12)
    # Density and direction discontinuities differ; weighting must select TRUE blocks.
    blocks=[(.25,1.),(.5,4.),(.25,2.)]
    direction=V.block_direction([2.,-3.,.5,7.],[0.,.125,.5,.875,1.])
    probe=V.SpectralProbe(blocks,4,64)
    _,cu,cw,_,info=probe.pairings(direction,(.625,),return_diagnostics=True)
    reference,energy=mp_physical_reference(blocks,probe.roots,direction.coefficients,direction.edges)
    check('density versus direction split block ownership',np.max(abs(cu-reference))<2e-11,error=float(np.max(abs(cu-reference))))
    check('every true cut plus optional cut included',info['intervals']==7,intervals=info['intervals'])
    check('density-block Parseval weighting oracle',np.max(abs(np.array(info['parseval_total_energy'])-energy))<2e-10)
    _,cuq,cwq,_,iq=probe.pairings(lambda x:direction(x),direction.edges[1:-1],return_diagnostics=True)
    check('weighted/unweighted block ownership matches resolved callback',np.max(abs(cu-cuq))<3e-11 and np.max(abs(cw-cwq))<7e-11)
    # Genuine thin density block, arbitrary positive densities, independent physical IVP.
    for exponent in (40,50):
        delta=2.**-exponent;blocks=[(.5,1.),(delta,7.),(.5-delta,3.)]
        probe=V.SpectralProbe(blocks,3,64)
        direction=V.block_direction([0.,1/delta,0.],probe.edges)
        _,cu,_,_,info=probe.pairings(direction,return_diagnostics=True)
        reference,energy=mp_physical_reference(blocks,probe.roots,direction.coefficients,direction.edges)
        check('genuine thin density analytic pairing '+str(exponent),np.max(abs(cu-reference))<3e-11,error=float(np.max(abs(cu-reference))))
        check('genuine thin density common mass '+str(exponent),info['modal_Gram_error']<3e-11)
    # Ill-resolved density coordinates must reject, rather than reinterpret widths.
    rejects('unresolved cumulative narrow density width',lambda:V.SpectralProbe([(.3,1.),(1e-16,2.),(.7-1e-16,1.)],3,64).pairings(V.block_direction([0,1e16,0],[0.,.3,.3+1e-16,1.])))
    probe=V.SpectralProbe([(1.,1.)],3,64)
    rejects('nonfinite direction sample',lambda:probe.pairings(lambda x:np.full(len(x),np.nan)))
    rejects('wrong shape direction sample',lambda:probe.pairings(lambda x:np.zeros((2,len(x)))))
    rejects('complex direction sample',lambda:probe.pairings(lambda x:np.full(len(x),1+1j)))
    rejects('invalid MaxOrder bool',lambda:probe.pairings(lambda x:x,MaxOrder=True))
    rejects('invalid callback error tolerance',lambda:probe.pairings(lambda x:x,AbsTol=0))
    for width in (2**-50,2**-40):
        rejects('unresolved P3 bump width '+str(width),lambda width=width:V.checked_bump_breaks(probe.blocks,[.5],width,64))
    breaks=V.checked_bump_breaks(probe.blocks,[.25,.75],.001,64)
    check('resolvable P3 support positive control',set(breaks)=={.249,.251,.749,.751})


def retained_interface_checks():
    blocks=[(.125,1.),(.75,10000.),(.125,1.)]
    roots=O.lams_precise(blocks,6)
    check('R15 enumerator prefix persists under large contrast',np.array_equal(roots[:3],O.lams_precise(blocks,3)) and np.array_equal(roots[:1],O.lams_precise(blocks,1)))
    phase=P.lifted_phase(blocks,roots)
    check('R15 enumerator frequencies still bind claimed index',np.max(abs(phase-np.arange(1,7)*math.pi))<2e-8)
    rejects('R15 unresolved tol remains rejected',lambda:O.lams_precise(blocks,3,tol=2**-70))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        same=O.lams_precise(blocks,3,smax_scale=2)
    check('deprecated R15 range scale affects no index',np.array_equal(same,roots[:3]) and any(issubclass(w.category,DeprecationWarning) for w in caught))
    pts=np.array([1.,0.,.25,.75,.25])
    for boundary in ('D','N'):
        actual=S.real_green_matrix([(1.,2.)],0.,pts,RightBoundary=boundary)
        exact=np.minimum(pts[:,None],pts[None,:])
        if boundary=='D':exact*=1-np.maximum(pts[:,None],pts[None,:])
        check('R14 zero Green coordinate order and duplicates '+boundary,np.max(abs(actual-exact))<2e-15)
    k=math.sqrt(6.)
    expected=np.sinh(k*np.minimum(pts[:,None],pts[None,:]))*np.sinh(k*(1-np.maximum(pts[:,None],pts[None,:])))/(k*math.sinh(k))
    check('R14 negative Green parameter still supported',np.max(abs(S.real_green_matrix([(1.,2.)],-3.,pts)-expected))<3e-15)
    rejects('R14 exact Green pole remains rejected',lambda:S.real_green_matrix([(1.,2.)],math.pi**2/2,[.2,.8]))
    table=I.IndexedSpectrum([(1.,2.)],'D',12)
    rejects('R14 spectrum wrong geometry',lambda:I.spectrum_for([(1.,1.)],'D',12,table))
    rejects('R14 spectrum wrong boundary',lambda:I.spectrum_for([(1.,2.)],'N',12,table))
    rejects('R14 reduced target wrong mode',lambda:JS.gtilde_spectral_blocks([(1.,2.)],table.eigenvalues[1],0,[.2,.8],N=11,spectrum=table))
    rejects('R14 reduced target arbitrary positive is not eigenvalue',lambda:JS.gtilde_spectral_blocks([(1.,2.)],1.,0,[.2,.8],N=11,spectrum=table))
    rejects('R14 reduced requested pole outside coverage',lambda:JS.gtilde_spectral_blocks([(1.,2.)],table.eigenvalues[5],5,[.2,.8],N=4,spectrum=table))
    check('R14 valid reduced Green kernel finite symmetric',np.all(np.isfinite(JS.gtilde_spectral_blocks([(1.,2.)],table.eigenvalues[1],1,[.8,.2,.2],N=11,spectrum=table))))
    rc,z,_,_=V.build_case(2,4.,'sup')
    check('R14 shared stationarity guard accepts actual ordinary solved point',rc.stationarity_diagnostics(z)['accepted'])
    check('R14 explicit failed solver result rejects stationary label',rc.stationarity_diagnostics(z,solver_success=False)['accepted'] is False)
    changed=z+np.array([.09,-.03,.02,.01,-.04])
    check('R14 nonstationary perturbation not relabeled stationary',rc.stationarity_diagnostics(changed)['accepted'] is False)
    tiny=rc.widths_to_z([1e-20,.2,.6,.1,.1])
    check('R14 tiny denominator configuration not accepted as stationary',rc.stationarity_diagnostics(tiny)['accepted'] is False)
    jfd,evidence=J.jac_fd(rc,z,return_diagnostics=True)
    cross1,cross2,sector=J.jacobian_cross_blocks(jfd,2,return_diagnostics=True)
    check('R14 faithful independent edge roundtrips retained',all(row['max_motion_error']<=row['geometry_error_budget'] for row in evidence['columns']))
    check('R14 Jacobian CROSS sectors retained',sector['diagonal_block_max']<1e-6 and abs(np.linalg.det(jfd)-np.linalg.det(cross1)*np.linalg.det(cross2))/max(1.,abs(np.linalg.det(jfd)))<1e-9)
    rejects('R14 commuting identity cannot be Jacobian CROSS decomposition',lambda:J.jacobian_cross_blocks(np.eye(4),2))
    data=JA.eigen_data(rc,changed)
    u,v=data['u_n'],data['u_np1'];a,b=data['lam_n'],data['lam_np1'];jumps=np.diff(rc.pat)
    expected=(2*a*np.outer(u**2,u**2)-2*b*np.outer(v**2,v**2)-np.outer(a*u**2-b*v**2,v**2))*jumps[None,:]
    terms=JA.jacobian_terms(data,jumps,np.zeros((4,4)),np.zeros((4,4)))
    check('R14 general quotient Jacobian term retained off stationarity',np.array_equal(terms['M1'],expected) and np.max(abs(terms['correction']))>1e-5)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    started=time.monotonic();error=None
    try:
        exact_poly_checks();local_integral_checks();pairing_checks();retained_interface_checks()
    except Exception as exc:
        error=repr(exc)
        check('unexpected independent check execution error',False,error=error)
        import traceback;traceback.print_exc()
    manifest=json.loads((ROOT.parent/'manifest.json').read_text())
    inputs={row['path']:hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest() for row in manifest}
    unchanged=all(inputs[row['path']]==row['sha256'] and (ROOT/row['path']).stat().st_size==row['bytes'] for row in manifest)
    check('all frozen input bytes remain unchanged after independent checks',unchanged)
    dependencies={name:str(Path(sys.modules[name].__file__).resolve()) for name in
                  ('rigid1d','_gapn2_second_variation_probe','_gapn2_symmetry_recon','_sl_prufer','_sl_spectral_identity',
                   '_gapn2_jacobian_probe','_gapn2_jacobian_analytic','_gapn2_jacobian_spectral','e1_certgen','e1_certificate_io',
                   'op03_gap_fixed','reflection_seeds')}
    check('every active project module loaded from frozen root',all(Path(p).is_relative_to(ROOT) for p in dependencies.values()))
    result=dict(all_passed=all(x['passed'] for x in ROWS),count=len(ROWS),failed=[x for x in ROWS if not x['passed']],
                rows=ROWS,error=error,elapsed_seconds=time.monotonic()-started,
                meaning='independent finite software review; no interval, infinite-tail or all-integer certification',
                environment=dict(python=sys.version,optimize=sys.flags.optimize,numpy=np.__version__,mpmath=mp.__version__,platform=platform.platform()),
                sources=inputs,loaded_dependencies=dependencies,
                reviewer_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('PASS' if result['all_passed'] else 'FAIL',result['count'],'independent checks',flush=True)
    return 0 if result['all_passed'] else 1


if __name__=='__main__':
    sys.exit(main())
