from pathlib import Path
import json,sys
import sympy as s
x=s.symbols('x',real=True)
p=s.pi; sn=s.sin(x); co=s.cos(x); ta=s.tan(x)
h=3+3*x*s.cot(x)-x*x/sn**2
J=4*x**3*s.cot(x)+6*x*x-p*p
G=8*x**3*sn**2-p*p*(2*x-s.sin(2*x))
b=x-ta; u=x/(2*b); D=(x*x-p*p/4)/u**2
N=x*x+x*sn*co-2*sn**2; r=(1/x-s.cot(x))/x
checks={
 'h derivative':s.diff(h,x)*sn**3-(3*co*sn**2-5*x*sn+2*x*x*co),
 'J derivative':s.diff(J,x)-4*x*h,
 'G derivative':s.diff(G,x)-4*sn**2*J,
 'u derivative':s.diff(u,x)-(x-s.sin(2*x)/2)/(2*co**2*b**2),
 'D derivative in a':s.diff(D,x)+b*G/(x**3*co**2),
 'D derivative in u':s.diff(D,x)/s.diff(u,x)+4*b**3*G/(x**3*(2*x-s.sin(2*x))),
 'B rational identity':2*x**4/(x*x+(-x*s.cot(x))**2-x*s.cot(x))-2*x**3*sn**2/(x-sn*co),
 'q second derivative':s.diff(x*sn,x,2)-(2*co-x*sn),
 'r derivative':s.diff(r,x)-N/(x**3*sn**2),
 'N second derivative':s.diff(N,x,2)-4*sn*(sn-x*co),
 'sin minus x cos derivative':s.diff(sn-x*co,x)-x*sn,
}
results=[]
for name,expr in checks.items():
    simplified=s.trigsimp(expr)
    ok=simplified==0
    results.append({'identity':name,'passed':ok,'residual':str(simplified)})
    if not ok: raise ArithmeticError(name+': '+str(simplified))
endpoints={
 'h(pi/2)': (h.subs(x,p/2),3-p*p/4),
 'J(pi/2)': (J.subs(x,p/2),p*p/2),
 'G(pi/2)': (G.subs(x,p/2),s.Integer(0)),
 'G(pi)': (G.subs(x,p),-2*p**3),
 'N(0)': (N.subs(x,0),s.Integer(0)),
 "N'(0)": (s.diff(N,x).subs(x,0),s.Integer(0)),
 'r(0+)': (s.limit(r,x,0,dir='+'),s.Rational(1,3)),
 'u(pi/2+)':(s.limit(u,x,p/2,dir='+'),s.Integer(0)),
 'u(pi-)':(s.limit(u,x,p,dir='-'),s.Rational(1,2)),
 'h(pi-)':(s.limit(h,x,p,dir='-'),-s.oo),
 'J(pi-)':(s.limit(J,x,p,dir='-'),-s.oo),
}
for name,(actual,expected) in endpoints.items():
    if actual!=expected and s.simplify(actual-expected)!=0:raise ArithmeticError(name+': '+str(actual))
    results.append({'identity':name,'passed':True,'value':str(actual)})
Path(sys.argv[1]).write_text(json.dumps({'status':'PASS','symbolic_checks':results,'sympy':s.__version__,'scope':'Identity and endpoint checks only; signs, domains and global conclusions reviewed analytically.'},indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(results),'sympy':s.__version__}))
