"""Independent finite review of the exact fifteen-file frozen software package.

No package checks/review state are imported. MP comparisons fix the SAME
binary64 frequency, rather than silently replacing it with an exact DD root.
"""
import ast
from decimal import Decimal
from fractions import Fraction as F
import hashlib
import importlib
import json
import math
from pathlib import Path
import sys
import time
import warnings

import mpmath as mp
import numpy as np

BASE = Path('F:/tools/math-audit-round16-20261006')
ROOT = BASE / 'software-review-v4/root'
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(ROOT/'misc'))
T = importlib.import_module('rigid1d')
V = importlib.import_module('_gapn2_second_variation_probe')
P = importlib.import_module('_gapn2_symmetry_recon')
S = importlib.import_module('_sl_spectral_identity')
J = importlib.import_module('_gapn2_jacobian_analytic')
JS = importlib.import_module('_gapn2_jacobian_spectral')
JP = importlib.import_module('_gapn2_jacobian_probe')
O = importlib.import_module('op03_gap_fixed')
ROWS = []


def check(name, condition, **data):
    row = dict(name=name, passed=bool(condition), **data)
    ROWS.append(row)
    if not row['passed']:
        raise RuntimeError(name)


def rejects(name, fn, types=(ValueError, TypeError, ArithmeticError)):
    try:
        fn()
    except types as error:
        check(name, True, error_type=type(error).__name__, error=str(error))
    else:
        check(name, False)


def raw_mode(blocks, frequency):
    """Independent physical IVP y(0)=0,y'(0)=1 and direct high-precision mass.

    The uncentered integral formula is independently evaluated at 110 digits;
    it does not use the package's midpoint/Taylor mass or anchor routine.
    """
    omega = mp.mpf(float(frequency))
    parts, start, value, derivative, mass = [], mp.mpf(0), mp.mpf(0), mp.mpf(1), mp.mpf(0)
    for width, density in blocks:
        length, rho = mp.mpf(float(width)), mp.mpf(float(density))
        wave = omega * mp.sqrt(rho)
        a, b = value, derivative/wave
        parts.append((start, length, rho, wave, a, b))
        angle = wave*length
        ic = length/2 + mp.sin(2*angle)/(4*wave)
        iss = length/2 - mp.sin(2*angle)/(4*wave)
        cross = mp.sin(angle)**2/(2*wave)
        mass += rho*(a*a*ic + b*b*iss + 2*a*b*cross)
        value, derivative = a*mp.cos(angle)+b*mp.sin(angle), wave*(-a*mp.sin(angle)+b*mp.cos(angle))
        start += length
    def states(x):
        first, length, rho, wave, a, b = next(part for part in reversed(parts) if part[0] <= x)
        q = wave*(x-first)
        return ((a*mp.cos(q)+b*mp.sin(q))/mp.sqrt(mass), wave*(-a*mp.sin(q)+b*mp.cos(q))/mp.sqrt(mass))
    return states, mass, parts


def thin_reference(blocks, frequency_i, frequency_j, left, right):
    a, _, _ = raw_mode(blocks, frequency_i)
    b, _, _ = raw_mode(blocks, frequency_j)
    lo, width = mp.mpf(float(left)), mp.mpf(float(right))-mp.mpf(float(left))
    return mp.quad(lambda t: a(lo+width*t)[0]*b(lo+width*t)[0], [0,1])


def exact_taylor():
    false_i = lambda x: (x-x*x/2)/15-F(1,2**62)*x
    false_f = lambda x: (F(1)+F(3,2**54))*x-x*x/2
    for name, fn, a, b, n in [('thirds',false_i,0,1,3),('adjacent-float',false_f,1.,math.nextafter(1.,2.),1)]:
        result=T.der_sign2(fn,a,b,True,base_n=n,max_n=n)
        adaptive=T.der_sign_adaptive(fn,a,b,True,max_boxes=101)
        check('false strict derivative '+name, result[0] is False and adaptive[0] is False, fixed=repr(result), adaptive=repr(adaptive))
    # Exercise exact arithmetic beyond finite binary64 and nonbinary partitions.
    for a,b in [(2**1500,2**1500+1),(F(-5,7),F(-1,9)),(-.8,math.nextafter(-.8,0.))]:
        seen=[]
        def fn(x):
            seen.extend((x.v.lo,x.v.hi))
            return 7*x+x*x*F(1,2**1600)
        check('honest exact endpoint '+str(type(a)), T.der_sign2(fn,a,b,True,base_n=7,max_n=7)[0] and all(type(x) is F for x in seen))
    for method in (T.der_sign2,T.der_sign_adaptive):
        for want in (1,None,'positive'):
            rejects('strict sign choice '+method.__name__+' '+repr(want),lambda method=method,want=want:method(lambda x:x,0,1,want))
        rejects('noncallable '+method.__name__,lambda method=method:method(3,0,1,True))
        for endpoint in (Decimal('0.2'),True,'0.2',complex(.2),float('-inf')):
            rejects('strict endpoint '+method.__name__+' '+repr(endpoint),lambda method=method,endpoint=endpoint:method(lambda x:x,endpoint,1,True))
    seen=[]
    def stalled(x):
        seen.append(x.v)
        return x*x
    answer=T.der_sign_adaptive(stalled,-1,1,True,max_boxes=3,min_w=F(1,2**30))
    check('adaptive three-box hard budget',answer[0] is False and len(seen)==6, calls=len(seen), result=repr(answer))
    # An inconclusive coarse enclosure is NOT evidence of a negative derivative.
    fn=lambda x:x+x*x*x
    coarse=T.der_sign2(fn,0,1,True,base_n=1,max_n=1)
    fine=T.der_sign2(fn,0,1,True,base_n=9,max_n=9)
    check('False means unproved only',coarse[0] is False and fine[0] is True)
    tree=ast.parse((ROOT/'misc/e1_certgen.py').read_text(encoding='utf-8'))
    affected={'der_sign2','der_sign_adaptive'}
    calls=[node for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in affected]
    function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='_taylor')
    first=function.body[0]
    check('E1 static independent Fraction preconversion',not calls and isinstance(first,ast.Assign) and all(isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='F' for node in first.value.elts))


def numeric_pairings():
    probe=V.SpectralProbe([(1.,2.)],61,8)
    result=probe.pairings(V.block_direction([2.],[0.,1.]))
    lam,cu,cw,diagonal=result
    check('61 modes analytic identity independent low order',np.max(abs(cu-np.eye(61)))<2e-12 and np.max(abs(cw-2*np.eye(61)))<4e-12,error=float(np.max(abs(cu-np.eye(61)))))
    for n in (1,3,17,59,60):
        q=V.q_formula(lam,cu,cw,n,diagonal)
        exact=(2*n+1)*math.pi**2/2
        check('independent constant Q '+str(n),abs(q-exact)<2e-7,q=q,exact=exact)
    info=result.diagnostics
    raw=np.array(info['parseval_total_energy'])-np.sum(cu*cu,axis=1)
    check('raw Parseval retained bit-for-bit',np.array_equal(raw,np.array(info['parseval_remainder_raw'])),minimum=float(np.min(raw)),negative_entries=int(np.sum(raw<0)))
    check('analytic diagnostic estimate boundary',info['sign_certified'] is False and info['roundoff_enclosure'] is None and info['spectral_tail_certification']=='NOT_CERTIFIED_FLOAT_INPUT')
    cases=[
        ('half constant',[(1.,1.)],.5,1),
        ('one-third constant rho3',[(1.,3.)],float(1/3),2),
        ('half symmetric nonconstant',[(.25,1.),(.5,9.),(.25,1.)],.5,1),
        ('one-third nonconstant',[(.125,2.),(.75,7.),(.125,2.)],float(1/3),2),
    ]
    with mp.workdps(110):
        for name,blocks,left,index in cases:
            probe=V.SpectralProbe(blocks,7,8)
            right=math.nextafter(left,1.)
            width=right-left
            _,cu,cw,_=probe.pairings(V.block_direction([0.,1/width,0.],[0.,left,right,1.]))
            for i,j in [(0,index),(index,index)]:
                expected=thin_reference(blocks,probe.roots[i],probe.roots[j],left,right)
                error=abs(mp.mpf(float(cu[i,j]))-expected)
                rel=error/abs(expected) if expected else error
                check('one-ulp physical IVP '+name+' '+str((i,j)),rel<mp.mpf('2e-12'),actual=float(cu[i,j]),reference=mp.nstr(expected,45),relative_error=mp.nstr(rel,12))
            density=blocks[min(int(np.searchsorted(probe.edges,left,side='right'))-1,len(blocks)-1)][1]
            check('one-ulp weighted physical density '+name,abs(cw[index,index]/(density*cu[index,index])-1)<3e-15)
            # Preserve exactly the one common normalization from the physical sampler.
            anchors=probe._analytic_anchor_states(np.array([0.,left]))
            scales=np.array([P.eigenfunction_states(blocks,root,[0.])[0,1] for root in probe.roots])
            check('one shared mass '+name,np.array_equal(anchors[:,0,1],scales))
        # Density and direction cuts differ; the thin cell is physical, not a mask.
        delta=2.**-50
        blocks=[(.25,2.),(delta,5.),(.75-delta,.75)]
        probe=V.SpectralProbe(blocks,5,32)
        edges=[0.,.25-delta,.25,.25+delta,.25+2*delta,1.]
        heights=[0.,.5/delta,1./delta,-.25/delta,0.]
        _,cu,_,_,info=probe.pairings(V.block_direction(heights,edges),return_diagnostics=True)
        expected=mp.mpf(0)
        for h,left,right in zip(heights,edges[:-1],edges[1:]):
            if h:
                expected+=mp.mpf(h)*(mp.mpf(right)-mp.mpf(left))*thin_reference(blocks,probe.roots[0],probe.roots[1],left,right)
        relative=abs(mp.mpf(float(cu[0,1]))-expected)/abs(expected)
        check('thin rho/h all cuts physical IVP',info['intervals']==5 and relative<mp.mpf('5e-12'),actual=float(cu[0,1]),reference=mp.nstr(expected,45),relative_error=mp.nstr(relative,12))
        rejects('thin rho actual Gauss folding',lambda:V.quadrature_rule(blocks,32))
        # A different high-contrast real spectrum from the package check.
        delta=2.**-19
        rejects('unresolved asymmetric contrast explicitly refused',lambda:V.SpectralProbe([(.375,1.),(delta,1e11),(.625-delta,1.)],61,32))
        blocks=[(.25,1.),(delta,1e11),(.75-delta,1.)]
        probe=V.SpectralProbe(blocks,61,32)
        length=.018
        direction=V.block_direction([3e8,0.],[0.,length,1.])
        _,cu,_,_=probe.pairings(direction)
        phases=probe.roots*length/2
        check('actual 61-mode spectrum straddles local Taylor branch',phases[0]<.05<phases[-1],lowest_phase=float(phases[0]),highest_phase=float(phases[-1]),lowest_frequency=float(probe.roots[0]),highest_frequency=float(probe.roots[-1]))
        for i,j in [(0,0),(0,1),(0,60),(1,60)]:
            expected=mp.mpf(3e8)*mp.mpf(length)*thin_reference(blocks,probe.roots[i],probe.roots[j],0.,length)
            relative=abs(mp.mpf(float(cu[i,j]))-expected)/abs(expected)
            check('different high-contrast physical IVP '+str((i,j)),relative<mp.mpf('8e-12'),actual=float(cu[i,j]),reference=mp.nstr(expected,45),relative_error=mp.nstr(relative,12))
        for waves,length in [(np.array([1e-60,.7,95.]),.025),(np.array([1e-140,5.,77.]),.012),(np.array([.01,.04,.09]),.1)]:
            c,s=V._cos_sin_integrals(waves,length)
            for i,j in [(0,0),(0,2),(1,2),(2,2)]:
                wi,wj=mp.mpf(float(waves[i])),mp.mpf(float(waves[j]))
                half=mp.mpf(length)/2
                sine=2*mp.quad(lambda x:mp.sin(wi*x)*mp.sin(wj*x)/(wi*wj),[0,half])
                cosine=2*mp.quad(lambda x:mp.cos(wi*x)*mp.cos(wj*x),[0,half])
                check('local extreme mixed phase '+str((float(waves[0]),i,j)),abs(mp.mpf(float(s[i,j]))/sine-1)<mp.mpf('2e-13') and abs(mp.mpf(float(c[i,j]))/cosine-1)<mp.mpf('2e-13'),sine_relative_error=mp.nstr(abs(mp.mpf(float(s[i,j]))/sine-1),12))
    rejects('positive local integral underflow',lambda:V._cos_sin_integrals(np.array([1.]),2.**-400))
    rejects('positive phase underflow',lambda:V._cos_sin_integrals(np.array([2.**-1000]),2.**-100))


def callback_contract():
    probe=V.SpectralProbe([(1.,1.)],3,16)
    calls=[]
    def constant(x):
        calls.append(len(x))
        return np.ones_like(x)
    answer=probe.pairings(constant,MaxOrder=64)
    check('callback actual two successive comparisons',calls==[16,32,64] and answer.diagnostics['order']==64,calls=calls)
    check('callback diagnostics no invented enclosure',answer.diagnostics['black_box_error_enclosure'] is None and answer.diagnostics['sign_certified'] is False and len(answer.diagnostics['estimated_absolute_errors'])==4)
    for budget in (16,32,63):
        calls.clear()
        rejects('callback bounded budget '+str(budget),lambda budget=budget:probe.pairings(constant,MaxOrder=budget))
        check('callback no further evaluations '+str(budget),max(calls)<=budget and probe.last_pairing_diagnostics['status']=='UNRESOLVED',calls=list(calls))
    calls.clear()
    def changing(x):
        calls.append(len(x))
        return np.ones_like(x)*(1+1e-3*(len(calls)%2))
    rejects('callback unconverged refused',lambda:probe.pairings(changing,MaxOrder=128))
    check('callback unresolved retained',calls==[16,32,64,128] and probe.last_pairing_diagnostics['status']=='UNRESOLVED',calls=list(calls))
    high=V.SpectralProbe([(1.,2.)],61,16)
    calls.clear()
    rejects('high-frequency callback phase resolution and insufficient budget',lambda:high.pairings(constant,MaxOrder=128))
    check('phase resolution skips callback before sampling',not calls and high.last_pairing_diagnostics['status']=='UNRESOLVED')


def prior_contracts():
    blocks=[(.18,1.),(.64,1e8),(.18,1.)]
    roots={k:O.lams_precise(blocks,k) for k in (1,3,6)}
    check('R15 1/3/6 enumeration prefixes identical',np.array_equal(roots[1],roots[6][:1]) and np.array_equal(roots[3],roots[6][:3]),frequencies=roots[6].tolist())
    from _sl_prufer import lifted_phase
    check('R15 prefixes retain one-based DD index',np.max(abs(lifted_phase(blocks,roots[6])-np.arange(1,7)*math.pi))<2e-8)
    rejects('R15 unresolved tolerance refuses',lambda:O.lams_precise([(1.,1.)],2,tol=1e-30))
    with warnings.catch_warnings(record=True) as found:
        warnings.simplefilter('always')
        O.lams_precise([(1.,1.)],2,smax_scale=2.)
    check('R15 smax default compatibility explicit deprecation',len(found)==1 and issubclass(found[0].category,DeprecationWarning))
    points=np.array([.7,.2,.7,0.,1.,.4])
    green=P.real_green_matrix([(1.,2.)],0.,points)
    exact=np.minimum(points[:,None],points[None,:])-np.outer(points,points)
    check('R14 physical Green zero parameter coordinate order',np.max(abs(green-exact))<3e-16)
    table=S.IndexedSpectrum([(1.,2.)],'D',8)
    lam=table.eigenvalues[1]
    g=JS.gtilde_spectral_blocks([(1.,2.)],lam,1,points,N=7,spectrum=table)
    check('R14 reduced finite DD kernel target usable',np.all(np.isfinite(g)) and np.max(abs(g-g.T))<2e-16)
    rejects('R14 reduced target wrong spectral index',lambda:JS.gtilde_spectral_blocks([(1.,2.)],lam,0,points,N=7,spectrum=table))
    rejects('R14 spectral prefix coverage guard',lambda:S.spectral_denominators(table,lam,9,PoleMode=2))
    rejects('R14 geometry-bound table',lambda:S.spectrum_for([(1.,3.)],'D',4,table))
    rejects('R14 boundary-bound table',lambda:S.spectrum_for([(1.,2.)],'N',4,table))
    data=dict(lam_n=2.,lam_np1=7.,u_n=np.array([.3,.4]),u_np1=np.array([.6,.2]),up_n=np.array([.7,-.3]),up_np1=np.array([-.2,.8]))
    jumps=np.array([3.,-3.])
    terms=J.jacobian_terms(data,jumps,np.zeros((2,2)),np.zeros((2,2)))
    f=data['lam_n']*data['u_n']**2-data['lam_np1']*data['u_np1']**2
    quotient=-np.outer(f,data['u_np1']**2)*jumps[None,:]
    expected=(2*data['lam_n']*np.outer(data['u_n']**2,data['u_n']**2)-2*data['lam_np1']*np.outer(data['u_np1']**2,data['u_np1']**2))*jumps[None,:]+quotient
    error=float(np.max(abs(terms['M1']-expected)))
    check('R14 general Jacobian quotient retained',error<2e-15*float(np.max(abs(expected))) and np.max(abs(quotient))>.1,absolute_error=error)
    rc,z,_,_=V.build_case(2,4.,'sup')
    jac,fd=JP.jac_fd(rc,z,return_diagnostics=True)
    c,d,info=JP.jacobian_cross_blocks(jac,2,return_diagnostics=True)
    check('R14 stationary acceptance and Jacobian cross blocks',rc.stationarity_diagnostics(z)['accepted'] and abs(np.linalg.det(jac)-np.linalg.det(c)*np.linalg.det(d))<1e-5 and all(row['used_step']>0 for row in fd['columns']),anticommutator=info['anticommutator_max'])
    rejects('R14 cross API refuses commuting Hessian',lambda:JP.jacobian_cross_blocks(np.eye(4),2))
    rejects('R14 physical Green near pole refusal',lambda:P.real_green_matrix([(1.,2.)],math.pi**2/2,points))
    # A tiny absolute residual alone must not manufacture a stationary point.
    check('R14 extreme softmax geometry not stationary',not rc.stationarity_diagnostics(np.array([0.,-25.,-25.,-25.,0.]))['accepted'])


def cli_readback():
    data=json.loads((BASE/'software-review-v4-cli-R4-sup.json').read_text(encoding='utf-8'))
    check('full R4 CLI P1/P2/P2b/P3 executed',all(data.get(group) for group in ('P1','P2','P2b','P3')) and len(data['P3'])==3,counts={group:len(data.get(group,[])) for group in ('P1','P2','P2b','P3')})
    for group in ('P1','P2','P2b','P3'):
        check('CLI saved diagnostics '+group,all(row['pairing_diagnostics']['sign_certified'] is False and 'parseval_remainder_raw' in row['pairing_diagnostics'] for row in data[group]))
    check('CLI P2b projection diagnostics saved',len(data['P2b_projection_pairing_diagnostics'])==8)


if __name__=='__main__':
    start=time.monotonic()
    error=None
    try:
        exact_taylor()
        numeric_pairings()
        callback_contract()
        prior_contracts()
        cli_readback()
    except Exception as exc:
        error=repr(exc)
    sources={str(path):hashlib.sha256(path.read_bytes()).hexdigest() for path in (ROOT/'misc/rigid1d.py',ROOT/'scripts/_gapn2_second_variation_probe.py',Path(__file__))}
    output=BASE/('software-review-v4-independent-'+('optimized' if sys.flags.optimize else 'normal')+'.json')
    output.write_text(json.dumps(dict(identity='/root/r16_software_review_v4',all_passed=error is None,count=len(ROWS),error=error,elapsed_seconds=time.monotonic()-start,optimize=sys.flags.optimize,python=sys.version,checks=ROWS,sources=sources),ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('PASS' if error is None else 'FAIL',len(ROWS),'independent properties',error or '')
    if error:
        raise RuntimeError(error)
