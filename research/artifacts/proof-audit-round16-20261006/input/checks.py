#!/usr/bin/env python3
"""Round16 checks: identify baseline defects and check new finite algebra.
These tests intentionally confirm wrong baseline outcomes. They are NOT a
post-repair acceptance suite and do not prove the infinite-dimensional theorem.
No asserts are used for acceptance, including under python -O.
"""
from __future__ import annotations
import argparse, hashlib, json, math, platform, sys, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source'))
from variation_excerpt import SpectralProbe, q_formula, block_direction, quadrature_rule
from taylor_excerpt import der_sign2, der_sign_adaptive
from physical_excerpt import eigenfunction_states, real_green_matrix, Recon
from _sl_prufer import indexed_roots
from _sl_spectral_identity import IndexedSpectrum, spectral_denominators, spectrum_for

ROWS=[]
def check(name, condition, **data):
    status=bool(condition)
    ROWS.append(dict(name=name,confirmed=status,**data))
    print(('CONFIRMED ' if status else 'FAILED ')+name,flush=True)
    if not status: raise RuntimeError(name)

def analytic_pairings(blocks,roots,coeff):
    """Exact trigonometric formula, evaluated in float64 at moderate phases.
    This is an audit reference, not a general small-phase-stable replacement.
    No quadrature nodes are used. See analytic_notes.md for the formula.
    """
    ends=np.r_[0.,np.cumsum([b[0] for b in blocks])]
    mat=np.zeros((len(roots),len(roots)))
    mids=(ends[:-1]+ends[1:])/2
    values=np.array([eigenfunction_states(blocks,s,mids) for s in roots])
    for i,(L,rho) in enumerate(blocks):
        om=roots*np.sqrt(rho); c=values[:,i,0];d=values[:,i,1]/om
        dm=(om[:,None]-om[None,:])*L/2
        dp=(om[:,None]+om[None,:])*L/2
        mat+=coeff[i]*L/2*((np.outer(c,c)+np.outer(d,d))*np.sinc(dm/np.pi)
                         +(np.outer(c,c)-np.outer(d,d))*np.sinc(dp/np.pi))
    return mat

def quadrature_checks():
    logs=[]
    for order in (32,64,128):
        p=SpectralProbe([(1.,2.)],Modes=61,Order=order)
        lam,C,Cw,diag=p.pairings(lambda x:2*np.ones_like(x))
        for n in (2,20,60):
            out=q_formula(lam,C,Cw,n,diag);exact=(2*n+1)*math.pi**2/2
            logs.append(dict(order=order,n=n,Q=out,exact=exact,relative_error=out/exact-1))
        if order==64:
            check('oscillatory_Gram_not_identity_at_default_order',np.max(np.abs(C-np.eye(61)))>.3,
                  max_Gram_error=float(np.max(np.abs(C-np.eye(61)))))
            check('constant_scaling_Q_wrong_at_default_order',abs(logs[-1]['relative_error'])>1,
                  **logs[-1])
            energy=float(np.sum(C[59]**2))
            check('computed_pairings_violate_exact_Bessel_budget',energy>1.9,
                  finite_pairing_energy=energy,exact_full_energy=1.0)
            M=analytic_pairings(p.blocks,p.roots,[2.])
            out=q_formula(lam,M,2*M,60,np.diag(M))
            check('same_roots_analytic_pairing_removes_error',abs(out-121*math.pi**2/2)<2e-7,
                  Q=out,expected=121*math.pi**2/2,Gram_error=float(np.max(np.abs(M-np.eye(61)))))
        if order==32:
            r=logs[-2]
            check('quadrature_can_reverse_Q_sign',r['Q']<0<r['exact'],**r)
        if order==128:
            check('higher_order_positive_control',max(abs(r['relative_error']) for r in logs[-3:])<1e-8,
                  rows=logs[-3:])
    p=SpectralProbe([(0.5,2.),(0.5,2.)],Modes=61,Order=64)
    lam,C,Cw,diag=p.pairings(lambda x:2*np.ones_like(x))
    val=q_formula(lam,C,Cw,60,diag)
    original=next(row['Q'] for row in logs if row['order']==64 and row['n']==60)
    check('equal_density_split_changes_quadrature_not_problem',abs(val-original)>100,
          Q_one_block=original,Q_two_identical_blocks=val,expected=121*math.pi**2/2,
          note='two halves improve but do not meet the earlier 2e-7 positive-control target')
    p4=SpectralProbe([(0.25,2.)]*4,Modes=61,Order=64)
    lam4,C4,W4,d4=p4.pairings(lambda x:2*np.ones_like(x))
    val4=q_formula(lam4,C4,W4,60,d4)
    check('four_identical_blocks_positive_control_same_tolerance',abs(val4-121*math.pi**2/2)<2e-7,
          Q=val4,expected=121*math.pi**2/2)
    return logs

def thin_checks():
    rows=[]
    for exponent in (40,50):
        delta=2.**(-exponent)
        blocks=[(.5,1.),(delta,1.),(.5-delta,1.)]
        for order in (64,128):
            p=SpectralProbe(blocks,Modes=3,Order=order)
            direction=block_direction([0.,1/delta,0.],p.edges)
            points,weights,values,knots=p.quadrature()
            lam,C,Cw,diag=p.pairings(direction)
            local=points.reshape(3,order)[1]
            rows.append(dict(exponent=exponent,order=order,
                  integrated_direction=float(np.dot(weights,direction(points))),
                  first_pairing=float(C[0,0]),unique_nodes=int(len(np.unique(local))),
                  nodes_at_right=int(np.sum(local==.5+delta))))
    r=rows[2]
    check('resolved_geometry_unresolved_thin_cell_nodes',r['unique_nodes']==9 and r['nodes_at_right']>0,
          **r)
    # Exact lower bound sin z/z >= 1-z²/6, pi<22/7.
    delta=F(1,2**50);lower=F(2)-(2*F(22,7)*delta)**2/6
    check('thin_pairing_loses_positive_mass',F.from_float(r['first_pairing'])<F(19,10)<lower,
          exact_lower_bound=str(lower),**r)
    check('increasing_order_does_not_fix_coordinate_loss',rows[3]['first_pairing']<1.9,
          rows=rows[2:])
    check('thicker_resolved_cell_positive_control',all(abs(x['first_pairing']-2)<2e-12 for x in rows[:2]),
          rows=rows[:2])
    return rows

def taylor_checks():
    a=1.;b=math.nextafter(a,2.);t=F(1)+F(3,2**54)
    fn=lambda z:t*z-z**2/2
    adaptive=der_sign_adaptive(fn,a,b,True,max_boxes=40,min_w=F(1,2**60))
    grid=der_sign2(fn,a,b,True,base_n=1,max_n=1)
    check('float_endpoints_false_adaptive_certificate',adaptive[0] and t-F(b)<0,
          returned=adaptive,derivative_at_right=str(t-F(b)),a=a.hex(),b=b.hex(),t=str(t))
    check('float_endpoints_false_grid_certificate',grid[0] and t-F(b)<0,returned=grid)
    aa=der_sign_adaptive(fn,F(a),F(b),True,max_boxes=40,min_w=F(1,2**60))
    gg=der_sign2(fn,F(a),F(b),True,base_n=1,max_n=1)
    check('Fraction_endpoints_reject_false_claim',not aa[0] and not gg[0],adaptive=aa,grid=gg)
    eps=F(1,2**62);fn2=lambda z:(z-z*z/2)/15-eps*z
    bad=der_sign2(fn2,0,1,True,base_n=3,max_n=3)
    good=der_sign2(fn2,F(0),F(1),True,base_n=3,max_n=3)
    check('plain_integer_endpoints_still_float_division',bad[0] and not good[0],
          returned_integer=bad,returned_Fraction=good,derivative_at_one=str(-eps))
    true=lambda z:z+z**2
    check('honest_positive_polynomial_control',der_sign2(true,F(0),F(1),True,base_n=3,max_n=3)[0]
          and der_sign_adaptive(true,F(0),F(1),True)[0])

x=sp.Symbol('x');c=sp.Symbol('c',positive=True)
def J(poly):
    p=sp.integrate(poly,x)
    return sp.expand(p-p.subs(x,-1))
def high(r,n):
    p=sp.legendre(n,x)
    for _ in range(r):p=J(p)
    return p

def hermite_lifts(r):
    """Exact rational Hermite construction, no floating rank tests."""
    deg=2*r
    H=sp.Matrix([[sp.diff(x**k,x,j).subs(x,side) for k in range(deg)]
                 for side in (-1,1) for j in range(r)])
    free=[(j,side) for j in range(0,r,2) for side in (-1,1)]
    polys=[]
    for target in free:
        vals={key:sp.Integer(key==target) for key in free}
        data=[]
        for side in (-1,1):
            for j in range(r):
                data.append(vals[(j,side)] if j%2==0 else (vals[(j-1,1)]-vals[(j-1,-1)])/2)
        coeff=H.inv()*sp.Matrix(data)
        polys.append(sp.expand(sum(coeff[k]*x**k for k in range(deg))))
    return free,polys

def B(poly):
    delta=(poly.subs(x,1)-poly.subs(x,-1))/2
    return [sp.expand(sp.diff(poly,x).subs(x,side)-delta) for side in (-1,1)]
def K(poly,cv=1):return sp.expand(-sp.diff(poly,x,2)+cv*poly)
def kp(poly,m,cv=1):
    for _ in range(m):poly=K(poly,cv)
    return poly

def integrate(p):
    p=sp.Poly(sp.expand(p),x)
    return sp.factor(sum(coef*sp.Rational(2,exp[0]+1) for exp,coef in p.terms() if exp[0]%2==0))
def gram(a,b,r,cv=1):
    aa=kp(a,r//2,cv);bb=kp(b,r//2,cv)
    if r%2==0:return integrate(aa*bb)
    da=aa.subs(x,1)-aa.subs(x,-1);db=bb.subs(x,1)-bb.subs(x,-1)
    return sp.factor(integrate(sp.diff(aa,x)*sp.diff(bb,x)+cv*aa*bb)-da*db/2)

def algebra_checks():
    summary=[]
    for r in (1,2,3,4,5,6):
        free,polys=hermite_lifts(r)
        T=sp.Matrix([[sp.diff(p,x,j).subs(x,side) for p in polys] for j,side in free])
        ok=T==sp.eye(len(free))
        for p in polys:
            for j in range(r//2):ok=ok and B(sp.diff(p,x,2*j))==[0,0]
        for n in range(r,r+3):
            b=high(r,n)
            ok=ok and sp.expand(sp.diff(b,x,r)-sp.legendre(n,x))==0
            ok=ok and all(sp.diff(b,x,j).subs(x,side)==0 for side in (-1,1) for j in range(r))
        N=2*r+2;cols=polys+[high(r,n) for n in range(r,N-r+1)]
        A=sp.Matrix([[sp.expand(p).coeff(x,k) for p in cols] for k in range(N+1)])
        rank=A.rank();expected=N+1-2*(r//2)
        ok=ok and rank==expected and rank==len(cols)
        check('Hermite_and_finite_span_r%d'%r,ok,order=r,low_columns=len(free),
              degree_cutoff=N,exact_rank=rank)
        summary.append(dict(r=r,lifts=[str(p) for p in polys]))
    for r in (1,2,3,4):
        far=gram(high(r,r),high(r,3*r+2),r,c)
        par=gram(high(r,r),high(r,r+1),r,c)
        check('exact_high_band_and_parity_r%d'%r,far==0 and par==0)
    free,polys=hermite_lifts(3)
    cols=polys+[high(3,3),high(3,4)]
    G=sp.Matrix([[gram(a,b,3) for b in cols] for a in cols])
    _,D=G.LDLdecomposition(hermitian=False)
    pivots=[sp.factor(D[i,i]) for i in range(len(cols))]
    check('new_odd_order_Gram_positive_exactly',all(p>0 for p in pivots),LDL_pivots=[str(p) for p in pivots])
    # Constant rho=2, h=2*cos(pi*x): only adjacent mode pairings are 1/2.
    n=sp.Symbol('n',integer=True,positive=True)
    eig=lambda k:k*k*sp.pi**2/2
    a,b,d=eig(n),eig(n+1),eig(n+2)
    lowerS=sp.Rational(1,4)*(1/(eig(n-1)-a)+1/(b-a))
    QN=a*a*lowerS-b*b*sp.Rational(1,4)/(a-b)
    Qfull=a*a*lowerS-b*b*sp.Rational(1,4)*(1/(a-b)+1/(d-b))
    check('bounded_direction_tail_lower_bound_is_sharp',sp.simplify(Qfull-QN+b*b/(4*(d-b)))==0,
          direction='rho=2, h=2 cos(pi x), n>=2, N=n+1',
          exact_difference=str(sp.factor(Qfull-QN)))
    return summary

def retained_regressions():
    roots=[]
    for bc in ('D','N'):
        tables=[IndexedSpectrum([(.5,100.)],bc,k) for k in (4,80,160)]
        a=tables[0].prefix(4)
        n=np.arange(1,5,dtype=float)-(0.5 if bc=='N' else 0)
        exact=(n*math.pi/5)**2
        check('current_half_spectrum_'+bc,all(np.array_equal(a,t.prefix(4)) for t in tables)
              and np.max(np.abs(a-exact))<1e-12)
    tab=IndexedSpectrum([(1.,1.)],'D',4)
    rejected=False
    try:spectral_denominators(tab,tab.eigenvalues[0],4,PoleMode=2)
    except ValueError:rejected=True
    check('current_wrong_pole_pairing_rejected',rejected)
    pts=[.75,0.,.25,1.]
    G=real_green_matrix([(1.,1.)],0.,pts)
    exact=np.minimum.outer(pts,pts)*(1-np.maximum.outer(pts,pts))
    check('current_Green_zero_parameter_and_order',np.max(np.abs(G-exact))<1e-14)
    rc=Recon(2,4.,'sup');d=1e-6
    ev=rc.stationarity_diagnostics(rc.widths_to_z([d,d,1-4*d,d,d]))
    check('round14_endpoint_pseudostationary_still_rejected',not ev['accepted'],evidence=ev)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    start=time.time();results={}
    try:
        retained_regressions()
        results['quadrature']=quadrature_checks();results['thin_cells']=thin_checks()
        taylor_checks();results['integer_lifts']=algebra_checks()
        success=True
    except Exception as exc:
        success=False;results['error']=repr(exc)
        raise
    finally:
        result=dict(baseline_commit='ec45bf99ae746b0a3699557e06700a3c00c5a831',
                    meaning='baseline defects confirmed plus finite regression/algebra; not theorem certification',
                    all_confirmed=all(row['confirmed'] for row in ROWS) and success,
                    count=len(ROWS),checks=ROWS,data=results,elapsed_s=time.time()-start,
                    environment=dict(python=sys.version,optimize=sys.flags.optimize,numpy=np.__version__,
                                     sympy=sp.__version__,platform=platform.platform()))
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
