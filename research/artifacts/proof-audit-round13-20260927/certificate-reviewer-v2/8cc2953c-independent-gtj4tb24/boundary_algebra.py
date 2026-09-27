"""Exact readout of the supplied G/J/W formulas, no omitted source imports."""
import json
from pathlib import Path
import sympy as S

root=Path(__file__).resolve().parent
x,q,c,si,co=S.symbols('x q c si co')
A,t,sg,cg,st,ct=S.symbols('A t sg cg st ct')
phi=co**2+q**2*si**2
den=q+c*phi
u=x*phi/den
G=-phi*(3+2*x*co/si)/den+2*c*x*phi*(q**2-1)*si*co/den**2
dx=lambda e:S.diff(e,x)+co*S.diff(e,si)-si*S.diff(e,co)
J=S.factor(G*G+S.diff(G,c)-u*dx(G))
print('G/J partial derivatives constructed',flush=True)
subs={x:A,si:sg,co:-cg,q:st*cg/(ct*sg),c:t/A}
actual=S.factor(J.subs(subs))
B1=A*cg-2*sg
B2=4*A**2*cg**2-A**2-12*A*cg*sg+6*sg**2
M=2*A**2*cg**2-A**2-8*A*cg*sg+6*sg**2
B4=7*A*cg**2-A*sg**2-4*cg*sg
B5=A**2*cg**2-A**2*sg**2+2*A**2+12*A*cg*sg-12*sg**2
B7=3*A*cg**2+A*sg**2+8*cg*sg
W=(-2*A**3*B1*st**2*ct**4+A**2*cg*B2*st**2*ct**2
   -2*A**3*sg*t*st*ct**5+A**2*sg*t*B4*st*ct**3
   -A*cg**2*sg*t*B5*st*ct+4*A**2*cg*sg**2*t**2*ct**4
   -A*cg*sg**2*t**2*B7*ct**2+6*cg**3*sg**4*t**2)
delta=A*st*ct+t*sg*cg
expected=2*A**2*cg*W/delta**4
num,denom=S.fraction(S.factor(actual-expected))
print('Rational difference formed',flush=True)
remainder=S.rem(S.Poly(num,st),S.Poly(st**2+ct**2-1,st)).as_expr()
remainder=S.rem(S.Poly(remainder,sg),S.Poly(sg**2+cg**2-1,sg)).as_expr()
remainder=S.factor(remainder)
if remainder!=0:
    raise RuntimeError('J2 decomposition not identical: '+str(remainder))
if S.expand(M-(B2-2*A*cg*B1))!=0:
    raise RuntimeError('B1/B2/M identity')

# The T1 decomposition of G_c and the u_x formula are checked independently.
W0=3+2*x*co/si
expected_Gc=phi**2*W0/den**2+2*x*phi*(q**2-1)*si*co*(q-c*phi)/den**3
expected_ux=phi/den+2*x*q*(q**2-1)*si*co/den**2
def zero_mod_circle(expr):
    n,_=S.fraction(S.factor(expr))
    return S.rem(S.Poly(n,si),S.Poly(si**2+co**2-1,si)).as_expr()==0
if not zero_mod_circle(S.diff(G,c)-expected_Gc):
    raise RuntimeError('T1 G_c identity')
if not zero_mod_circle(dx(u)-expected_ux):
    raise RuntimeError('T1 u_x identity')
result={'status':'PASS','sympy_version':S.__version__,'checks':['J2=2 A^2 cg W/Delta^4 modulo both unit-circle identities','M=B2-2 A cg B1','T1 G_c=t1+t2','T1 u_x identity'],'scope':'Exact symbolic identities only; positivity and nonzero denominators established separately on the stated closed domains.'}
(root/'outputs/boundary_algebra.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
