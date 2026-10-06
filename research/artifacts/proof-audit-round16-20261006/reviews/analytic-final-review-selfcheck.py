from fractions import Fraction as F
import sys, json, hashlib
from pathlib import Path

ROOT = Path(r'F:\tools\math-audit-round16-20261006')
PACKAGE = ROOT / 'analytic-final-review'
OUTPUT = ROOT / 'analytic-final-review-selfcheck.json'
checks = []

def check(name, condition, detail=None):
    if not condition:
        raise AssertionError(name)
    checks.append({'name': name, 'passed': True, 'detail': detail})

def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def add(p, q):
    a = [F(0)] * max(len(p), len(q))
    for i, v in enumerate(p): a[i] += v
    for i, v in enumerate(q): a[i] += v
    return trim(a)

def scale(p, a): return trim([a * v for v in p])

def mul(p, q):
    a = [F(0)] * (len(p) + len(q) - 1)
    for i, v in enumerate(p):
        for j, w in enumerate(q): a[i+j] += v*w
    return trim(a)

def deriv(p, n=1):
    for _ in range(n):
        p = trim([F(i)*p[i] for i in range(1, len(p))] or [F(0)])
    return p

def at(p, x):
    out = F(0)
    for a in reversed(p): out = out*x+a
    return out

def integral(p):
    return sum((F(2)*v/F(i+1) for i,v in enumerate(p) if i % 2 == 0), F(0))

def pair(p, q): return integral(mul(p,q))

def J(p):
    q = [F(0)] + [v/F(i+1) for i,v in enumerate(p)]
    q[0] -= at(q, F(-1))
    return trim(q)

def Jn(p,n):
    for _ in range(n): p = J(p)
    return p

def K(p,c): return add(scale(p,c),scale(deriv(p,2),F(-1)))

def Km(p,c,m):
    for _ in range(m): p=K(p,c)
    return p

def delta(p): return at(p,F(1))-at(p,F(-1))

def B(p):
    d=delta(p)/2
    dp=deriv(p)
    return (at(dp,F(1))-d,at(dp,F(-1))-d)

def gram(p,q,r,c):
    p,q=Km(p,c,r//2),Km(q,c,r//2)
    if r % 2:
        return pair(deriv(p),deriv(q))-delta(p)*delta(q)/2+c*pair(p,q)
    return pair(p,q)

def solve(a, b):
    n=len(a)
    M=[list(row)+[b[i]] for i,row in enumerate(a)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if M[i][k])
        M[k],M[pivot]=M[pivot],M[k]
        lead=M[k][k]
        M[k]=[v/lead for v in M[k]]
        for i in range(n):
            if i==k: continue
            factor=M[i][k]
            if factor: M[i]=[v-factor*w for v,w in zip(M[i],M[k])]
    return trim([M[i][-1] for i in range(n)])

def rank(rows):
    if not rows: return 0
    M=[list(row) for row in rows]
    k=0
    for j in range(len(M[0])):
        piv=next((i for i in range(k,len(M)) if M[i][j]),None)
        if piv is None: continue
        M[k],M[piv]=M[piv],M[k]
        v=M[k][j]
        M[k]=[a/v for a in M[k]]
        for i in range(k+1,len(M)):
            v=M[i][j]
            if v: M[i]=[a-v*b for a,b in zip(M[i],M[k])]
        k+=1
        if k==len(M): break
    return k

def positive_definite(M):
    M=[list(row) for row in M]
    for k in range(len(M)):
        pivot=M[k][k]
        if pivot<=0: return False
        for i in range(k+1,len(M)):
            for j in range(k+1,len(M)):
                M[i][j]-=M[i][k]*M[k][j]/pivot
    return True

manifest=json.loads((PACKAGE/'manifest.json').read_text(encoding='utf-8-sig'))
identities=[]
for row in manifest:
    data=(PACKAGE/row['name']).read_bytes()
    sha=hashlib.sha256(data).hexdigest()
    check('manifest:'+row['name'],len(data)==row['bytes'] and sha==row['sha256'])
    identities.append({'name':row['name'],'bytes':len(data),'sha256':sha})

P=[[F(1)],[F(0),F(1)]]
for n in range(1,30):
    P.append(scale(add(scale(mul([F(0),F(1)],P[n]),F(2*n+1)),scale(P[n-1],F(-n))),F(1,n+1)))

for r in range(1,7):
    matrix=[]
    for k in range(r):
        for end in (F(-1),F(1)):
            matrix.append([at(deriv([F(0)]*i+[F(1)],k),end) for i in range(2*r)])
    free=[(k,end) for k in range(0,r,2) for end in (F(-1),F(1))]
    hs=[]
    for target in free:
        rhs=[]
        for k in range(r):
            for end in (F(-1),F(1)):
                if k%2==0:
                    rhs.append(F((k,end)==target))
                else:
                    rhs.append((F((k-1,F(1))==target)-F((k-1,F(-1))==target))/2)
        h=solve(matrix,rhs)
        check(f'hermite_jets:r{r}:{target}',[at(deriv(h,k),end) for k in range(r) for end in (F(-1),F(1))]==rhs)
        check(f'hermite_boundary:r{r}:{target}',all(B(deriv(h,2*j))==(F(0),F(0)) for j in range(r//2)))
        hs.append(h)
    check(f'free_dimension:r{r}',len(hs)==2*((r+1)//2))
    highs={n:Jn(P[n],r) for n in range(r,3*r+4)}
    for n,p in highs.items():
        check(f'zero_jets:r{r}:n{n}',all(at(deriv(p,k),end)==0 for k in range(r) for end in (F(-1),F(1))))
        check(f'derivative_identity:r{r}:n{n}',deriv(p,r)==P[n])
    for N in range(2*r-1,2*r+4):
        cols=hs+[highs[n] for n in range(r,N-r+1)]
        rows=[[p[i] if i<len(p) else F(0) for p in cols] for i in range(N+1)]
        check(f'finite_span_dimension:r{r}:N{N}',rank(rows)==N+1-2*(r//2))
    for c in (F(1,3),F(1),F(7,2)):
        finite=hs+[highs[n] for n in range(r,r+4)]
        G=[[gram(p,q,r,c) for q in finite] for p in finite]
        check(f'finite_gram_positive:r{r}:c{c}',positive_definite(G))
        for n,p in highs.items():
            if n>3*r-1:
                check(f'low_high_zero:r{r}:c{c}:n{n}',all(gram(h,p,r,c)==0 for h in hs))
            for ell,q in highs.items():
                if ell<n and (abs(n-ell)>2*r or (n-ell)%2):
                    check(f'high_band_zero:r{r}:c{c}:n{n}:l{ell}',gram(p,q,r,c)==0)

# Exact physical tail counterexample, with pi^2 divided out.
# rho=2, h=2 cos(2 pi x), n=1, N=2.
a,b,d=F(1,2),F(2),F(9,2)
e_a=e_b=F(1,4)
q_N=-a/4
T_a=e_a/(F(9,2)-a)
T_b=e_b/(F(8)-b)
q=q_N+a*a*T_a-b*b*T_b
check('tail_counterexample_QN',q_N==F(-1,8))
check('tail_counterexample_Q',q==F(-53,192))
left=q_N-b*b*e_b/(d-b)
a_upper=F(5)
wrong_right=q_N+a_upper*a_upper*e_a/(d-a_upper)
check('tail_current_written_conditions',F(0)<=a<=a_upper and d>b)
check('tail_interval_claim_fails',q>wrong_right)
check('tail_interval_claim_reversed',left>wrong_right)
correct_a_upper=min(a_upper,b)
correct_right=q_N+correct_a_upper**2*e_a/(d-correct_a_upper)
check('tail_interval_repair_covers_exact_Q',left<=q<=correct_right)

result={
    'runtime':sys.executable,
    'python_version':sys.version,
    'package':str(PACKAGE),
    'inputs':identities,
    'passed_checks':len(checks),
    'arithmetic':'exact fractions; no floating point',
    'limitations':'Finite r=1,...,6 checks do not prove the general integer theorem; no actual source/runtime acceptance, Lean, TeX compilation or R15 proof was used.',
    'counterexample_coefficients_divided_by_pi_squared':{
        'a':str(a),'b':str(b),'d_lower':str(d),'a_upper':str(a_upper),
        'e_a_upper':str(e_a),'e_b_upper':str(e_b),
        'Q_N':str(q_N),'Q':str(q),'stated_lower':str(left),
        'stated_upper':str(wrong_right),'repaired_upper':str(correct_right)
    },
    'checks':checks
}
OUTPUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed_checks':len(checks),'output':str(OUTPUT),'counterexample':result['counterexample_coefficients_divided_by_pi_squared']},ensure_ascii=False))
