"""Independent frozen-package review, /root/r16_software_review_v3.

Only imports the permitted root modules. Does not use package checks.py or
authors' reference routines for its own numerical oracles. No asserts.
"""
import argparse
import ast
from fractions import Fraction
import hashlib
import importlib
import json
import math
from pathlib import Path
import platform
import sys
import time

import mpmath as mp
import numpy as np

ROOT = Path('F:/tools/math-audit-round16-20261006/software-review-v3/root')
sys.path.insert(0, str(ROOT/'misc'))
sys.path.insert(0, str(ROOT/'scripts'))
T = importlib.import_module('rigid1d')
V = importlib.import_module('_gapn2_second_variation_probe')
Physical = importlib.import_module('_gapn2_symmetry_recon')
Identity = importlib.import_module('_sl_spectral_identity')
Spectral = importlib.import_module('_gapn2_jacobian_spectral')
Jacobian = importlib.import_module('_gapn2_jacobian_probe')
Analytic = importlib.import_module('_gapn2_jacobian_analytic')
Legacy = importlib.import_module('op03_gap_fixed')
ROWS = []


def check(name, condition, **data):
    ok = bool(condition)
    ROWS.append(dict(name=name, passed=ok, **data))


def rejects(name, fn, types=(TypeError, ValueError, ArithmeticError)):
    try:
        fn()
    except types as exc:
        check(name, True, exception=type(exc).__name__, message=str(exc))
    else:
        check(name, False)


def taylor_review():
    # Callback gets only exact Fraction coordinates, before any operation on
    # endpoint-derived values. Nonbinary grid size is deliberately five.
    seen = []
    def fn(z):
        seen.append((z.v.lo, z.v.hi))
        return z + z*z/7
    passed, n = T.der_sign2(fn, 0, 1, True, base_n=5, max_n=5)
    check('independent exact fifths', passed and n == 5
          and [seen[2*i] for i in range(5)] == [(Fraction(i,5), Fraction(i+1,5)) for i in range(5)]
          and all(type(x) is Fraction for a,b in seen for x in (a,b)))
    a, b = -math.nextafter(1.,2.), -1.
    seen.clear()
    passed, _ = T.der_sign2(fn,a,b,True,base_n=5,max_n=5)
    check('negative adjacent floats exact endpoints', passed and seen[0][0] == Fraction(a)
          and seen[-2][1] == Fraction(b) and sum((seen[2*i][1]-seen[2*i][0] for i in range(5)),Fraction(0)) == Fraction(b)-Fraction(a))
    false_int = lambda z:(z-z*z/2)/15-Fraction(1,2**62)*z
    false_float = lambda z:(1+Fraction(3,2**54))*z-z*z/2
    for tag,f,a,b,n in [('integer3',false_int,0,1,3),('float1',false_float,1.,math.nextafter(1.,2.),1)]:
        answer,info=T.der_sign2(f,a,b,True,base_n=n,max_n=n)
        check('false sign fixed '+tag, answer is False and 'unproved' in info)
        answer,info=T.der_sign_adaptive(f,a,b,True,max_boxes=15)
        check('false sign adaptive '+tag,answer is False and 'unproved' in info)
    # Strict derivative at an endpoint zero must not pass either sign.
    for want in (True,False):
        check('strict endpoint zero fixed '+str(want),T.der_sign2(lambda z:z*z,0,1,want,base_n=3,max_n=3)[0] is False)
        check('strict endpoint zero adaptive '+str(want),T.der_sign_adaptive(lambda z:z*z,0,1,want,max_boxes=5)[0] is False)
    # A non-power-of-two upper budget must never be crossed.
    seen.clear()
    def positive(z):
        seen.append(z)
        return z*z
    answer,info=T.der_sign2(positive,-1,1,True,base_n=3,max_n=5)
    check('fixed does not round budget upward',answer is False and 'n=3' in info and len(seen)==2)
    seen.clear()
    answer,info=T.der_sign_adaptive(positive,-1,1,True,max_boxes=3,min_w=Fraction(1,2**30))
    check('adaptive budget exact',answer is False and 'max_boxes=3' in info and len(seen)==6)
    for kw in [dict(max_n=True),dict(max_n=3.0),dict(base_n=2,max_n=1)]:
        rejects('fixed invalid '+str(kw),lambda kw=kw:T.der_sign2(lambda z:z,0,1,True,**kw))
    for kw in [dict(want_pos=1),dict(want_pos=np.bool_(True))]:
        rejects('exact bool contract '+str(kw),lambda kw=kw:T.der_sign_adaptive(lambda z:z,0,1,**kw))
    # AST-only E1 trace; do not execute the E1 ledger or its 57 obligations.
    source=(ROOT/'misc/e1_certgen.py').read_text(encoding='utf-8-sig')
    tree=ast.parse(source)
    imports=[node for node in ast.walk(tree) if isinstance(node,ast.ImportFrom) and node.module=='rigid1d']
    names=[alias.name for node in imports for alias in node.names]
    calls=[node.func.id for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Name)]
    body=next(node.body for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='_taylor')
    first=body[0]
    check('E1 static dedicated conversion precedes arithmetic',isinstance(first,ast.Assign)
          and isinstance(first.targets[0],ast.Tuple)
          and [node.id for node in first.targets[0].elts]==['a','b','Target']
          and isinstance(first.value,ast.Tuple)
          and [ast.unparse(node) for node in first.value.elts]==['F(a)','F(b)','F(Target)'],first_statement=ast.unparse(first))
    check('E1 static no generic Taylor dependency',all(name not in names+calls for name in ('der_sign2','der_sign_adaptive')))


def oracle_modes(blocks, roots):
    """Physical IVP at exactly the supplied binary64 frequency, mp90.

    Each original binary length and density is lifted exactly; the propagated
    data and L2(rho) mass are obtained independently by physical ODE formulas
    and direct high-precision integration of squares.
    """
    modes=[]
    for root in roots:
        frequency=mp.mpf(float(root)); start=mp.mpf(0); u=mp.mpf(0); d=mp.mpf(1)
        parts=[]; mass=mp.mpf(0)
        for length,density in blocks:
            length,density=mp.mpf(float(length)),mp.mpf(float(density))
            wave=frequency*mp.sqrt(density)
            A,B=u,d/wave
            parts.append((start,length,density,wave,A,B))
            mass += density*mp.quad(lambda x:(A*mp.cos(wave*x)+B*mp.sin(wave*x))**2,[0,length])
            u,d=A*mp.cos(wave*length)+B*mp.sin(wave*length),wave*(-A*mp.sin(wave*length)+B*mp.cos(wave*length))
            start += length
        modes.append((parts,mass))
    return modes


def sample_mode(mode,x,normalize=True):
    parts,mass=mode
    part=next(p for p in reversed(parts) if p[0] <= x)
    start,length,density,wave,A,B=part
    u=A*mp.cos(wave*(x-start))+B*mp.sin(wave*(x-start))
    return u/mp.sqrt(mass) if normalize else u


def thin_case(name,blocks,left,mode_index,modes=8,height=None):
    probe=V.SpectralProbe(blocks,modes,8)
    right=math.nextafter(left,math.inf); width=right-left
    direction=V.block_direction([0.,1/width if height is None else height,0.],[0.,left,right,probe.edges[-1]])
    result=probe.pairings(direction)
    with mp.workdps(100):
        physical=oracle_modes(blocks,probe.roots)
        ml,mw=mp.mpf(left),mp.mpf(width)
        factor=mw*mp.mpf(float(direction.coefficients[1]))
        cross=factor*mp.quad(lambda t:sample_mode(physical[0],ml+mw*t)*sample_mode(physical[mode_index],ml+mw*t),[0,1])
        square=factor*mp.quad(lambda t:sample_mode(physical[mode_index],ml+mw*t)**2,[0,1])
        scales=np.array([Physical.eigenfunction_states(blocks,float(w),[0.])[0,1] for w in probe.roots])
        relative_mass=max(float(abs(mp.mpf(float(scale))*mp.sqrt(mode[1])-1)) for scale,mode in zip(scales,physical))
        cp,sp=result[1][0,mode_index],result[1][mode_index,mode_index]
        cross_error=float(abs(mp.mpf(float(cp))-cross))
        square_relative=float(abs(mp.mpf(float(sp))/square-1)) if square else 0.
        # Near-zero cross tolerance is independent of ordinary O(1) relative
        # tests and checks the preserved local half-width at physical nodes.
        tol=max(3e-29,3e-13*float(abs(cross)))
        check('oracle thin cross '+name,cross_error<=tol,actual=float(cp),reference=mp.nstr(cross,35),abs_error=cross_error,tolerance=tol)
        check('oracle thin square '+name,square_relative<3e-12,actual=float(sp),reference=mp.nstr(square,35),relative_error=square_relative)
        check('oracle common mass '+name,relative_mass<3e-12,max_relative_mass_error=relative_mass)
    check('all cuts and honest diagnostics '+name,result.diagnostics['intervals']==len(np.unique(np.r_[probe.edges,direction.edges]))-1
          and not result.diagnostics['sign_certified'] and result.diagnostics['roundoff_enclosure'] is None)
    # This actual Gauss path must reject the geometric one-ulp cell even when
    # an arbitrary callback simply wraps a perfectly valid BlockDirection.
    rejects('ordinary one-ulp guard '+name,lambda:V.quadrature_rule(blocks,8,(left,right)))
    rejects('callback one-ulp guard '+name,lambda:probe.pairings(lambda x:direction(x),(left,right)))
    return probe


def pairing_review():
    for rho in (2.,):
        for order in (8,16):
            probe=V.SpectralProbe([(1.,rho)],61,order)
            result=probe.pairings(V.block_direction([2.],[0.,1.]))
            check('61 constant pairing order'+str(order),np.max(np.abs(result[1]-np.eye(61)))<3e-12,error=float(np.max(np.abs(result[1]-np.eye(61)))))
            for n in (1,17,58,60):
                q=V.q_formula(*result[:3],n,result[3]); exact=(2*n+1)*math.pi**2/2
                check('61 exact Q '+str((order,n)),abs(q-exact)<3e-8,Q=q,exact=exact)
            # A raw floating residual may be tiny negative and is retained.
            energy=np.array(result.diagnostics['parseval_total_energy'])
            raw=energy-np.sum(result[1]**2,axis=1)
            check('raw residual retained order'+str(order),np.array_equal(raw,np.array(result.diagnostics['parseval_remainder_raw'])))
    thin_case('constant rho3.7 node2/7',[(1.,3.7)],float(2/7),6)
    thin_case('constant rho0.25 node1/7',[(1.,.25)],float(1/7),6)
    thin_case('internal rho9 odd node1/2',[(.25,1.),(.5,9.),(.25,1.)],.5,1)
    thin_case('internal rho0.125 odd node1/2',[(.125,7.),(.75,.125),(.125,7.)],.5,3)
    thin_case('binary 1/3 rho7 near modal3',[(1.,7.)],float(1/3),2)
    # Independently locate a physical IVP node in a nonuniform, asymmetric
    # four-block problem, then round once to the supplied binary geometry.
    blocks=[(.125,2.),(.25,5.),(.375,.7),(.25,3.)]
    seed=V.SpectralProbe(blocks,8,8)
    with mp.workdps(100):
        data=oracle_modes(blocks,seed.roots)
        grid=[mp.mpf(i)/100 for i in range(39,75)]
        bracket=next((a,b) for a,b in zip(grid[:-1],grid[1:]) if sample_mode(data[5],a)*sample_mode(data[5],b)<0)
        a,b=bracket
        for _ in range(330):
            c=(a+b)/2
            if sample_mode(data[5],a)*sample_mode(data[5],c)<=0:b=c
            else:a=c
        left=float((a+b)/2)
    thin_case('asymmetric internal rho0.7 mp-located-node6',blocks,left,5)
    # The tiny density cell and independent direction cuts must both survive.
    delta=2.**-50
    blocks=[(.5,1.),(delta,7.),(.5-delta,1.75)]
    probe=V.SpectralProbe(blocks,8,8)
    h=V.block_direction([0.,1/delta,0.,-2.],[0.,.5,.5+delta,.75,1.])
    result=probe.pairings(h)
    with mp.workdps(100):
        modes=oracle_modes(blocks,probe.roots)
        for i,j in [(0,0),(0,6),(6,6)]:
            thin=mp.quad(lambda t:sample_mode(modes[i],mp.mpf(.5)+mp.mpf(delta)*t)*sample_mode(modes[j],mp.mpf(.5)+mp.mpf(delta)*t),[0,1])
            broad=mp.quad(lambda x:sample_mode(modes[i],x)*sample_mode(modes[j],x),[mp.mpf(.75),mp.mpf(1)])
            unweighted=thin-2*broad
            weighted=7*thin-2*mp.mpf(1.75)*broad
            check('thin distinct density unweighted '+str((i,j)),abs(float(unweighted)-result[1][i,j])<5e-12,actual=float(result[1][i,j]),reference=float(unweighted))
            check('thin distinct density weighted '+str((i,j)),abs(float(weighted)-result[2][i,j])<5e-11,actual=float(result[2][i,j]),reference=float(weighted))
    check('density and direction full cut union',result.diagnostics['intervals']==4 and result.diagnostics['modal_Gram_error']<3e-12)
    rejects('ordinary thin distinct density fails actual nodes',lambda:V.quadrature_rule(blocks,64))
    # Stable small/unequal phase local sine products, beyond the supplied cases.
    for waves,length in [(np.array([1e-14,.4,1.]),.09),(np.array([.01,1.,100.]),.02),(np.array([1e-10,2.,20.]),.35)]:
        cc,ss=V._cos_sin_integrals(waves,length)
        with mp.workdps(90):
            for i,j in [(0,0),(0,2),(1,2),(2,2)]:
                wi,wj,l=mp.mpf(float(waves[i])),mp.mpf(float(waves[j])),mp.mpf(length)
                reference=mp.quad(lambda x:mp.sin(wi*x)*mp.sin(wj*x)/(wi*wj),[-l/2,l/2])
                relative=float(abs(mp.mpf(float(ss[i,j]))/reference-1))
                check('independent phase product '+str((waves.tolist(),length,i,j)),relative<4e-13,relative_error=relative)
    for slow in (.01,1e-4,1e-7):
        waves=np.array([slow,100.]);length=2*math.pi/100
        cc,ss=V._cos_sin_integrals(waves,length)
        with mp.workdps(100):
            wi,wj,l=mp.mpf(float(waves[0])),mp.mpf(float(waves[1])),mp.mpf(length)
            reference=mp.quad(lambda x:mp.cos(wi*x)*mp.cos(wj*x),[-l/2,l/2])
            relative=float(abs(mp.mpf(float(cc[0,1]))/reference-1))
            check('independent cosine sum cancellation '+str(slow),relative<4e-13,actual=float(cc[0,1]),reference=mp.nstr(reference,40),relative_error=relative)
    # Concrete use of that mixed-scale helper by the actual public pairing
    # entrypoint. The direction is bounded, the binary geometry is legitimate,
    # all physical mass and requested modal indices remain the same.
    delta=2.**-20;blocks=[(.5,1.),(delta,4e10),(.5-delta,1.)]
    probe=V.SpectralProbe(blocks,61,8);length=.021;height=1e10
    result=probe.pairings(V.block_direction([height,0.],[0.,length,1.]))
    with mp.workdps(100):
        physical=oracle_modes(blocks,probe.roots[:1])
        reference=mp.mpf(height)*mp.quad(lambda x:sample_mode(physical[0],x)**2,[0,mp.mpf(length)])
        relative=float(abs(mp.mpf(float(result[1][0,0]))/reference-1))
        check('actual pairing mixed phase accuracy',relative<3e-12,blocks=blocks,first_frequency=float(probe.roots[0]),last_frequency=float(probe.roots[-1]),direction_height=height,direction_width=length,
              actual=float(result[1][0,0]),reference=mp.nstr(reference,40),relative_error=relative)
    check('mixed phase actual accepted numerical scope only',result.diagnostics['modal_Gram_error']<2e-8 and result.diagnostics['sign_certified'] is False and result.diagnostics['roundoff_enclosure'] is None,
          Gram_error=result.diagnostics['modal_Gram_error'])
    for length in (2.**-400,2.**-600):
        rejects('local positive integral underflow '+str(length),lambda length=length:V._cos_sin_integrals(np.array([math.pi]),length))
    rejects('pairing energy overflow fails closed',lambda:V.SpectralProbe([(1.,1.)],3,8).pairings(V.block_direction([1e308],[0.,1.])))
    rejects('unresolvable cumulative density width fails closed',lambda:V.SpectralProbe([(1.,1.),(2.**-54,2.)],3,8))


def callback_review():
    probe=V.SpectralProbe([(1.,2.)],61,8)
    calls=[]
    def fn(x):
        calls.append(len(x))
        return 2*np.ones_like(x)
    rejects('callback modal budget unresolved',lambda:probe.pairings(fn,MaxOrder=128))
    check('phase rejects before callback execution',calls==[] and probe.last_pairing_diagnostics['status']=='UNRESOLVED',callback_calls=calls)
    rejects('callback only one comparison insufficient',lambda:probe.pairings(fn,MaxOrder=512))
    check('phase and comparison budget exact',calls==[256,512] and probe.last_pairing_diagnostics['status']=='UNRESOLVED',callback_calls=calls)
    calls.clear()
    result=probe.pairings(fn,MaxOrder=1024)
    diag=result.diagnostics
    check('callback two consecutive comparisons',calls==[256,512,1024] and diag['order']==1024 and diag['previous_order']==512,callback_calls=calls)
    check('callback estimate no sign envelope',len(diag['estimated_absolute_errors'])==4 and diag['black_box_error_enclosure'] is None and diag['sign_certified'] is False)
    # An oscillatory callback with a stringent tolerance must not be quietly
    # accepted after the fixed budget, even if modal phases themselves resolve.
    probe=V.SpectralProbe([(1.,1.)],4,8)
    rejects('callback convergence exhaustion',lambda:probe.pairings(lambda x:np.sin(500*x),MaxOrder=64,AbsTol=1e-14,RelTol=1e-14))
    check('callback exhaustion status honest',probe.last_pairing_diagnostics['status']=='UNRESOLVED')
    rejects('callback nonfinite input',lambda:probe.pairings(lambda x:np.full_like(x,np.nan)))
    rejects('callback wrong shape input',lambda:probe.pairings(lambda x:np.array([1.])))
    rejects('callback invalid MaxOrder',lambda:probe.pairings(lambda x:x,MaxOrder=True))


def preservation_contract_review():
    # R15 prefix enumeration in a high-contrast geometry, using counts beyond
    # the original k1/k3/k6 examples and independent exact phase indexing.
    blocks=[(.375,1.),(.25,1e6),(.375,1.)]
    reference=Legacy.lams_precise(blocks,9)
    for n in (1,2,4,7):
        values=Legacy.lams_precise(blocks,n)
        check('R15 high contrast prefix '+str(n),np.array_equal(values,reference[:n]))
    check('R15 high contrast index phase',np.max(np.abs(V.lifted_phase(blocks,reference)-np.pi*np.arange(1,10)))<2e-8)
    rejects('R15 impossible tolerance rejects',lambda:Legacy.lams_precise(blocks,3,tol=1e-300))
    # Physical Green matrices must retain ordering, duplicates, zero and
    # negative parameters, and reject unresolved poles.
    points=np.array([.75,.25,.75,0.,1.,.5])
    for boundary in ('D','N'):
        g=Physical.real_green_matrix([(1.,1.)],0.,points,RightBoundary=boundary)
        exact=np.minimum(points[:,None],points[None,:])*(1-np.maximum(points[:,None],points[None,:])) if boundary=='D' else np.minimum(points[:,None],points[None,:])
        check('R14 coordinate Green zero '+boundary,np.max(np.abs(g-exact))<2e-15)
        g=Physical.real_green_matrix([(1.,1.)],-3.,points,RightBoundary=boundary)
        k=math.sqrt(3); lo=np.minimum(points[:,None],points[None,:]); hi=np.maximum(points[:,None],points[None,:])
        exact=np.sinh(k*lo)*np.sinh(k*(1-hi))/(k*np.sinh(k)) if boundary=='D' else np.sinh(k*lo)*np.cosh(k*(1-hi))/(k*np.cosh(k))
        check('R14 coordinate Green negative '+boundary,np.max(np.abs(g-exact))<3e-15)
    rejects('R14 physical Green DD pole',lambda:Physical.real_green_matrix([(1.,1.)],math.pi**2,points))
    table=Identity.IndexedSpectrum([(1.,1.)],'D',6)
    other=Identity.IndexedSpectrum([(1.,2.)],'D',6)
    rejects('R14 indexed geometry rejects',lambda:Identity.spectrum_for([(1.,1.)],'D',6,other))
    rejects('R14 indexed boundary rejects',lambda:Identity.spectrum_for([(1.,1.)],'N',6,table))
    rejects('R14 full table coverage rejects',lambda:Identity.spectral_denominators(table,table.eigenvalues[-1]*1.01,4))
    rejects('R14 wrong pole identity rejects',lambda:Spectral.gtilde_spectral_blocks([(1.,1.)],table.eigenvalues[2],1,points,N=5,spectrum=table))
    rejects('R14 retained pole refuses silent division',lambda:Identity.spectral_denominators(table,table.eigenvalues[1],6))
    good=Spectral.gtilde_spectral_blocks([(1.,1.)],table.eigenvalues[2],2,points,N=5,spectrum=table)
    check('R14 reduced Green explicit index finite',np.all(np.isfinite(good)) and np.max(np.abs(good-good.T))<3e-15)
    # General M1 must include the off-stationary quotient correction.
    rc=Physical.Recon(2,4.,'sup'); z=rc.widths_to_z([.08,.21,.13,.25,.33])
    data=Analytic.eigen_data(rc,z); jumps=np.diff(rc.pat)
    terms=Analytic.jacobian_terms(data,jumps,np.zeros((4,4)),np.zeros((4,4)))
    a,b=data['lam_n'],data['lam_np1']; u,v=data['u_n'],data['u_np1']
    full=np.array([[jumps[i]*(2*a*u[j]**2*u[i]**2-2*b*v[j]**2*v[i]**2-(a*u[j]**2-b*v[j]**2)*v[i]**2) for i in range(4)] for j in range(4)])
    check('R14 general quotient Jacobian retained',np.max(np.abs(terms['M1']-full))<1e-12 and np.max(np.abs(terms['correction']))>1e-2)
    check('R14 nonstationary guard rejects',rc.stationarity_diagnostics(z)['accepted'] is False)
    check('R14 unsuccessful solver guard rejects',rc.stationarity_diagnostics(z,solver_success=False)['status']=='not_converged')
    # A representable small width stays small; no fixed width floor.
    widths=rc.z_to_widths(np.array([-35.,0.,0.,0.,0.]))
    check('R14 pure softmax has no width floor',0<widths[0]<1e-14,width=float(widths[0]))
    rejects('R14 unrepresentable softmax rejects',lambda:rc.z_to_widths(np.array([-1000.,0.,0.,0.,0.])))
    # Correct sector decomposition is crossed for an anticommuting Jacobian.
    rng=np.random.default_rng(734); M=rng.normal(size=(6,6)); P=np.eye(6)[::-1]
    J=(M-P@M@P)/2
    C,D,evidence=Jacobian.jacobian_cross_blocks(J,3,return_diagnostics=True)
    plus=np.vstack([np.eye(6)[i]+np.eye(6)[5-i] for i in range(3)])
    minus=np.vstack([np.eye(6)[i]-np.eye(6)[5-i] for i in range(3)])
    check('R14 crossing preserved',np.max(np.abs(C-plus@J@minus.T/2))<1e-15 and np.max(np.abs(D-minus@J@plus.T/2))<1e-15 and not evidence['certified'])
    rejects('R14 commuting matrix rejected by cross routine',lambda:Jacobian.jacobian_cross_blocks(np.eye(6),3))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    start=time.monotonic();error=None
    try:
        taylor_review();pairing_review();callback_review();preservation_contract_review()
    except Exception as exc:
        error=repr(exc)
    finally:
        result=dict(identity='/root/r16_software_review_v3',all_passed=error is None and all(r['passed'] for r in ROWS),count=len(ROWS),checks=ROWS,error=error,elapsed_seconds=time.monotonic()-start,
            environment=dict(python=sys.version,optimize=sys.flags.optimize,numpy=np.__version__,mpmath=mp.__version__,platform=platform.platform()),
            meaning='Independent finite numerical and interface checks; no interval, all-integer, Lean or canonical certification',
            harness_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('PASS' if result['all_passed'] else 'FAIL',result['count'],error or '')
    return 0 if result['all_passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
