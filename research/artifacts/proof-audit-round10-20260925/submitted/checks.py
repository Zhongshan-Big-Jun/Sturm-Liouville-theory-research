"""Independent round-10 audit checks. Not a full repository test or proof assistant.
The root scanner is a semantic reproduction in probe_roots.py of the fetched
roots_of/D_scalar logic. No author workflow or external repository is modified.
"""
from fractions import Fraction as F
from math import factorial
import json,sys,platform
# The exact rational certificates intentionally contain integers with >4300 digits.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
from pathlib import Path
import numpy as np
import sympy as s
import mpmath as mp
from probe_roots import roots_of, D_scalar

OUT=Path(__file__).resolve().parent
records=[]
def check(name,cond,kind,detail=None):
    if not bool(cond):raise RuntimeError('FAILED: '+name)
    records.append({'name':name,'kind':kind,'confirmed':True,'detail':detail})

# Directed rational intervals, with no floating-point endpoints in the certificates.
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[1],-a[0])
def sub(a,b): return add(a,neg(b))
def mul(a,b):
    vals=[x*y for x in a for y in b]
    return min(vals),max(vals)
def scale(a,c):return mul(a,(c,c))
def trig(x,which,N=80):
    x=F(x); parity=1 if which=='sin' else 0
    p=sum((F((-1)**j,factorial(2*j+parity))*x**(2*j+parity) for j in range((N-parity)//2+1)),F(0))
    # Lagrange remainder for the Taylor polynomial of degree N (including zero coefficients).
    err=abs(x)**(N+1)/factorial(N+1)
    return p-err,p+err
def half_at(w,binary=False):
    w=F(w)
    u=F(float(.02)) if binary else F(1,50)
    ell=F(float(.96))/2 if binary else F(12,25)
    th=100*u*w; zz=ell*w
    c1,c2=trig(th,'cos'),trig(zz,'cos')
    s1,s2=trig(th,'sin'),trig(zz,'sin')
    even=sub(mul(c1,c2),scale(mul(s1,s2),F(1,100)))
    odd=add(scale(mul(s1,c2),F(1,100)),mul(c1,s2))
    return even,odd

def sig(a):
    if a[0]>0:return 1
    if a[1]<0:return -1
    return 0

brackets=[('even','0.783424012239','0.783424012240'),
          ('odd','0.797807654414','0.797807654415'),
          ('even','2.345707847544','2.345707847545'),
          ('odd','2.358540421082','2.358540421083')]
cert=[]
for name,l,r in brackets:
    idx=0 if name=='even' else 1
    left,right=half_at(F(l))[idx],half_at(F(r))[idx]
    bl,br=half_at(F(l),True)[idx],half_at(F(r),True)[idx]
    if sig(bl)*sig(br)!=-1: raise RuntimeError('binary input bracket failed')
    check('exact_bracket_'+name+'_'+l,sig(left)*sig(right)==-1,'exact rational Taylor remainder',
          {'interval':[l,r],'endpoint_signs':[sig(left),sig(right)],'binary_input_endpoint_signs':[sig(bl),sig(br)]})
    cert.append({'parity':name,'left':l,'right':r,
                 'left_value_bounds':[str(x) for x in left],
                 'right_value_bounds':[str(x) for x in right],
                 'binary_left_value_bounds':[str(x) for x in bl],
                 'binary_right_value_bounds':[str(x) for x in br]})
(OUT/'root_bracket_certificates.json').write_text(json.dumps(cert,indent=2))

blocks=[(.02,10000.),(.96,1.),(.02,10000.)]
scan={}
for count in (2,3,61):
    ans=roots_of(blocks,count)
    scan[str(count)]=ans.tolist()
    check('scanner_misses_four_lower_roots_count_'+str(count),len(ans)==count and np.all(np.diff(ans)>0) and F(float(ans[0])) > F(22,7),
          'numerical execution plus four exact lower brackets',{'first_returned':float(ans[0]),'max_secular_residual':float(max(abs(D_scalar(blocks,x)) for x in ans)), 'first_frequency_exceeds_22_over_7':True})
# Explicit grid cell containing the first pair, same-sign exact endpoint checks.
k=3;smax=np.pi*100*(k+2)+20.;npts=max(20000,int(np.ceil(smax/.02)))
grid=np.linspace(1e-9,smax,npts)
i=np.searchsorted(grid,.783424012239)-1
left,right=F(float(grid[i])),F(float(grid[i+1]))
product_left=mul(*half_at(left,True));product_right=mul(*half_at(right,True))
check('first_pair_in_same_same_sign_scan_cell',left<F(brackets[0][1]) and F(brackets[1][2])<right and sig(product_left)==sig(product_right)!=0,
      'exact rational inclusion and Taylor sign',{'cell':[float(left),float(right)],'signs':[sig(product_left),sig(product_right)],'grid_count':npts})

# Symmetry-sector construction: source's all-index assignment is NOT a projection.
a=np.array([1.,2.,3.,4.]); a[3-np.arange(4)]=-a
check('source_assignment_is_not_symmetry_sector',np.array_equal(a,[-4.,-3.,-2.,-1.]) and not np.allclose(a,a[::-1]) and not np.allclose(a,-a[::-1]),
      'exact integer-valued numpy execution',{'transformed':a.tolist()})
b=np.array([1.,2.,3.,4.]); preserve=(b-b[::-1])/2; breaking=(b+b[::-1])/2
check('reflection_sector_repairs',np.array_equal(preserve,-preserve[::-1]) and np.array_equal(breaking,breaking[::-1]) and np.array_equal(b,preserve+breaking),'finite exact algebra')

# Polynomial and boundary algebra for newly added proofs.
x,c,t=s.symbols('x c t',real=True)
def ip(p,q):return s.integrate(s.expand(p*q),(x,-1,1))
def B(p):
    d=p.subs(x,1)-p.subs(x,-1)
    return s.Matrix([s.diff(p,x).subs(x,1)-d/2,s.diff(p,x).subs(x,-1)-d/2])
def kc(p):return s.expand(c*p-s.diff(p,x,2))
def J(p):return s.expand(s.integrate(p.subs(x,t),(t,-1,x)))
def Jr(p,r):
    for _ in range(r):p=J(p)
    return p
p4=x**4-2*x**2;p5=x**5-2*x**3
q6=x**6-5*x**4+7*x**2;q7=x**7-s.Rational(21,5)*x**5+s.Rational(27,5)*x**3
check('krein_boundary_obstruction_and_cancellation',B(p4)==s.zeros(2,1) and B(s.diff(p4,x,2))==s.Matrix([24,-24]) and B(q6)==B(s.diff(q6,x,2))==s.zeros(2,1),'symbolic polynomial identity')
trace=s.Matrix([[s.diff(p,x,j).subs(x,0) for p in [s.Integer(1),x,p4]] for j in range(3)])
check('s3_three_trace_matrix',trace==s.diag(1,1,-4) and s.diff(p5,x,2).subs(x,0)==0,'symbolic finite traces')
for r in (2,4):
    good=True
    for n in range(r,r+5):
        en=s.sqrt(s.Rational(2*n+1,2))*s.legendre(n,x); b=Jr(en,r)
        good &= s.simplify(s.diff(b,x,r)-en)==0
        good &= all(s.simplify(s.diff(b,x,j).subs(x,z))==0 for j in range(r) for z in (-1,1))
    check('integrated_Legendre_endpoints_r'+str(r),good,'symbolic finite sample n=r,...,r+4')
E=(3-q6)/16;O=(11*x-5*q7)/48
lifts=[s.Integer(1),x,E,O]
vals=s.Matrix([[p.subs(x,z) for p in lifts] for z in (1,-1)]+[[s.diff(p,x,2).subs(x,z) for p in lifts] for z in (1,-1)])
check('four_low_lifts_and_boundary_matrix',all(B(p)==B(s.diff(p,x,2))==s.zeros(2,1) for p in lifts) and vals==s.Matrix([[1,1,0,0],[1,-1,0,0],[0,0,1,1],[0,0,1,-1]]),'symbolic polynomial identity')
M=s.expand(sum(ip(kc(kc(p)),kc(kc(p))) for p in lifts))
claimed=s.Rational(8,405405)*(136657*c**4+24984*c**3+487890*c**2+4890600*c+22297275)
check('M_c_squared_exact_polynomial',s.simplify(M-claimed)==0,'symbolic polynomial integration',{'M_c_squared':str(M)})
# Verify the high-high sparsity on representative separated index pairs.
for r,op in [(2,kc),(4,lambda p:kc(kc(p)))]:
    u=Jr(s.sqrt(s.Rational(2*r+1,2))*s.legendre(r,x),r)
    v=Jr(s.sqrt(s.Rational(2*(r+2*r+2)+1,2))*s.legendre(r+2*r+2,x),r)
    check('high_Gram_zero_outside_band_r'+str(r),s.simplify(ip(op(u),op(v)))==0,'symbolic exact example')

# Reproduce polynomial arithmetic-progression integration (D8,D9) exactly.
bm=lambda m:t**m-s.Rational(m,m-1)*t**(m-1)
a0,d0=3,2; co=[s.Integer(2),s.Integer(-3),s.Integer(5)]
rp=sum(co[j]*t**(d0*j) for j in range(3))
actual=s.integrate((t-1)*t**(a0-2)*rp,(t,0,x))
expected=sum(co[j]/(a0+d0*j)*bm(a0+d0*j).subs(t,x) for j in range(3))
check('arithmetic_progression_integration',s.expand(actual-expected)==0,'symbolic polynomial identity')
# Scalar exact cutoff example, with all conventions explicit.
lam=[F(1),F(1,100)];eps=F(1,20)
check('Gram_vs_synthesis_cutoff', [z>eps for z in lam]==[True,False] and [F(1)>eps,F(1,10)>eps]==[True,True],'exact rational threshold')
T=s.Matrix([[1,s.I,0],[0,1,0]])
G=T.conjugate().T*T
check('complex_finite_Gram_psd',G==G.conjugate().T and G.rank()==2 and set(G.eigenvals().keys())=={s.Integer(0),(3+s.sqrt(5))/2,(3-s.sqrt(5))/2},'exact complex matrix algebra')

# Single-interface transfer calibration: independent implicit differentiation.
mp.mp.dps=70
sec=lambda w,a:(3*mp.sin(w*(2-a))+mp.sin(w*(3*a-2)))/(4*w)
th=mp.acos(1/mp.sqrt(3));cal=[]
for label,w in [('first',2*th),('second',2*(mp.pi-th))]:
    a=mp.mpf('.5');Fw=mp.diff(lambda z:sec(z,a),w);Fa=mp.diff(lambda z:sec(w,z),a)
    wp=-Fa/Fw
    Faa=mp.diff(lambda z:sec(w,z),a,2);Fww=mp.diff(lambda z:sec(z,a),w,2)
    Fwa=mp.diff(lambda z:mp.diff(lambda b:sec(z,b),a),w)
    wpp=-(Faa+2*Fwa*wp+Fww*wp**2)/Fw
    lp=2*w*wp;lpp=2*wp**2+2*w*wpp
    expected=6*w**2+mp.mpf('1.5')*w**3*mp.tan(w/2)
    check('moving_interface_implicit_calibration_'+label,abs(lp-2*w**2)<mp.mpf('1e-55') and abs(lpp-expected)<mp.mpf('1e-55'),'70-digit independent implicit differentiation',{'lambda':mp.nstr(w*w,45),'first_derivative':mp.nstr(lp,45),'second_derivative':mp.nstr(lpp,45)})
    cal.append([mp.nstr(w*w,40),mp.nstr(lp,40),mp.nstr(lpp,40)])

out={'scope':'Independent finite checks plus analytic root-existence certificates; not full theorem certification.',
     'repository_commit':'5bb6b2605122d2daf472863b4bec0f35a9c192e1',
     'python':sys.version,'optimization_level':sys.flags.optimize,'numpy':np.__version__,'sympy':s.__version__,'mpmath':mp.__version__,
     'count':len(records),'checks':records,'source_scan_outputs':scan}
(OUT/'check_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'confirmed_groups':len(records),'scan_first_three':scan['3'],'all_confirmed':True},indent=2))
