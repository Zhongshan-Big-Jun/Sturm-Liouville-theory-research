import sympy as s
l,k=s.symbols('l k',positive=True)
s2,c2,s4,c4=s.sin(2*k*l),s.cos(2*k*l),s.sin(4*k*l),s.cos(4*k*l)
o={}
o['C2,iCC']=l*l/8+l*s2/(8*k)+(1-c4)/(64*k*k)
o['C2,iSS']=l*l/8+l*s2/(8*k)+(c2-1)/(8*k*k)-(1-c4)/(64*k*k)
o['C2,iCS']=l/(16*k)-s4/(64*k*k)
o['CS,iCC']=-l*c2/(8*k)+s2/(16*k*k)+l/(16*k)-s4/(64*k*k)
o['CS,iSS']=-l*c2/(8*k)+s2/(16*k*k)-l/(16*k)+s4/(64*k*k)
o['CS,iCS']=-(c2-1)/(16*k*k)+(c4-1)/(64*k*k)
o['S2,iCC']=l*l/8-l*s2/(8*k)-(c2-1)/(8*k*k)-(1-c4)/(64*k*k)
o['S2,iSS']=l*l/8-l*s2/(8*k)+(1-c4)/(64*k*k)
o['S2,iCS']=3*l/(16*k)-s2/(8*k*k)+s4/(64*k*k)
f={'C2':s.cos(k*l)**2,'CS':s.cos(k*l)*s.sin(k*l),'S2':s.sin(k*l)**2}
g={'iCC':l/2+s2/(4*k),'iCS':(1-c2)/(4*k),'iSS':l/2-s2/(4*k)}
for key,expr in o.items():
 a,b=key.split(','); diff=s.trigsimp(s.expand_trig(s.diff(expr,l)-f[a]*g[b]));val=s.simplify(expr.subs(l,0)); print(key,diff,val)
