from fractions import Fraction as F
from decimal import Decimal, getcontext
from math import factorial
from pathlib import Path
from collections import Counter
import json, sys
import certificate as c

counts=Counter()
def ensure(value, group, detail=''):
    counts[group]+=1
    if not value: raise ArithmeticError('Reviewer check failed: '+group+' '+detail)
def rejects(fn, message, kind=ArithmeticError):
    try: fn()
    except kind as e: ensure(message in str(e), 'guard error identity', str(e))
    else: raise ArithmeticError('Expected rejection missing: '+message)
def pair(x): return (x.lo,x.hi)
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def neg(x): return (-x[1],-x[0])
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    z=[a*b for a in x for b in y]; return (min(z),max(z))
def div(x,y):
    if y[0]<=0<=y[1]:raise ArithmeticError('reference denominator contains zero')
    z=[a/b for a in x for b in y]; return (min(z),max(z))
def pt(x): return (F(x),F(x))
def scale(x,k): return mul(x,pt(k))
def square(x): return (0 if x[0]<=0<=x[1] else min(a*a for a in x), max(a*a for a in x))
def contains(outer,inner): return outer[0]<=inner[0] and inner[1]<=outer[1]
def reference_trig(x,n):
    s=sum(((-1)**j*x**(2*j+1)/factorial(2*j+1) for j in range((n+1)//2)),F(0))
    co=sum(((-1)**j*x**(2*j)/factorial(2*j) for j in range(n//2+1)),F(0))
    rem=abs(x)**(n+1)/factorial(n+1)
    return (s-rem,s+rem),(co-rem,co+rem)
def reference_atan(x,n):
    p=sum(((-1)**j*x**(2*j+1)/(2*j+1) for j in range(n)),F(0))
    q=p+(-1)**n*x**(2*n+1)/(2*n+1)
    return (min(p,q),max(p,q))
def encoded_pair(x): return F(x['lower']['exact']),F(x['upper']['exact'])
def validate_display(x):
    if isinstance(x,dict):
        if 'exact' in x:
            ensure(F(x['display_lower'])<=F(x['exact'])<=F(x['display_upper']), 'directed rational displays')
        if 'outward_display' in x:
            lo,hi=encoded_pair(x)
            ensure(lo<=hi and F(x['outward_display'][0])<=lo and hi<=F(x['outward_display'][1]), 'directed interval displays')
        for v in x.values(): validate_display(v)
    elif isinstance(x,list):
        for v in x:validate_display(v)

values=[F(-3),F(-1),F(-1,3),F(0),F(1,3),F(1),F(3)]
boxes=[c.Interval(a,b) for i,a in enumerate(values) for b in values[i:]]
for x in boxes:
    sample=[x.lo,(x.lo+x.hi)/2,x.hi]
    ensure(pair(-x)==(-x.hi,-x.lo),'interval negation')
    for n in range(7):
        ys=[v**n for v in sample]
        if n and n%2==0 and x.lo<=0<=x.hi:ys.append(F(0))
        ensure(pair(x**n)==(min(ys),max(ys)),'integer powers',str((x,n)))
    for n in [-1,-2,-3,-4]:
        if x.lo<=0<=x.hi:rejects(lambda x=x,n=n:x**n,'Divisor interval contains zero')
        else:
            ys=[v**n for v in sample]
            ensure(pair(x**n)==(min(ys),max(ys)),'negative integer powers')
    for digits in [0,1,7,90,200]:
        grid=c.outward_grid(x,digits)
        ensure(grid.lo<=x.lo<=x.hi<=grid.hi and x.lo-grid.lo<F(1,10**digits) and grid.hi-x.hi<F(1,10**digits),'rational floor ceiling grids')
    for y in boxes:
        ys=[y.lo,(y.lo+y.hi)/2,y.hi]
        ensure(pair(x+y)==(x.lo+y.lo,x.hi+y.hi),'interval addition')
        ensure(pair(x-y)==(x.lo-y.hi,x.hi-y.lo),'interval subtraction')
        products=[a*b for a in sample for b in ys]
        ensure(pair(x*y)==(min(products),max(products)),'interval multiplication')
        if y.lo<=0<=y.hi:rejects(lambda x=x,y=y:x/y,'Divisor interval contains zero')
        else:
            quotients=[a/b for a in sample for b in ys]
            ensure(pair(x/y)==(min(quotients),max(quotients)),'interval division signs')

for value in [True,False,0.1,Decimal('0.1'),'1',None,complex(1,0)]:
    rejects(lambda value=value:c.Interval.point(value),'Only exact int or Fraction',TypeError)
    rejects(lambda value=value:c.trig_point(value),'Only exact int or Fraction',TypeError)
for n in [False,True,F(2),2.0,'2']:
    rejects(lambda n=n:c.Interval(-2,3)**n,'Interval power must be an integer')
for digits in [-1,201,False,F(90),90.0]:
    rejects(lambda digits=digits:c.outward_grid(c.Interval(-1,1),digits),'Invalid rational grid precision')
for degree in [0,-1,False,True,F(2),2.0]:
    rejects(lambda degree=degree:c.trig_point(F(1),degree),'Taylor degree must be a positive integer')
for count in [0,-1,False,True,F(2),2.0]:
    rejects(lambda count=count:c.atan_small(F(1,5),count),'Arctan term count must be positive')
for x in [F(-1),F(0),F(1),F(2)]:
    rejects(lambda x=x:c.atan_small(x,2),'Arctan series requires 0 < x < 1')
for x in [F(-7,2),F(-1),F(-1,100),F(0),F(1,100),F(1),F(7,2)]:
    for n in [1,2,3,4,9,10,30,110]:
        actual=c.trig_point(x,n); independent=reference_trig(x,n)
        for a,b in zip(actual,independent):
            ensure(contains(pair(a),b) and b[0]-a.lo<F(1,10**90) and a.hi-b[1]<F(1,10**90),'independent Taylor parity sign zero')
for x in [F(1,239),F(1,5),F(9,10)]:
    for n in range(1,9):
        ensure(pair(c.atan_small(x,n))==reference_atan(x,n),'alternating arctan odd even counts')
pi_ref=sub(scale(reference_atan(F(1,5),85),16),scale(reference_atan(F(1,239),28),4))
Pi=c.machin_pi()
ensure(contains(pair(Pi),pi_ref),'independent Machin rational enclosure')
for a in [Pi.lo/2,Pi.hi/2,Pi.lo,Pi.hi,F(0),F(4)]:
    rejects(lambda a=a:c.g_point(a,Pi),'Phase must be certified inside')
    rejects(lambda a=a:c.u_point(a,Pi),'Phase must be certified inside')
    rejects(lambda a=a:c.f_point(a,F(1,3),Pi),'Phase must be certified inside')
for u in [F(-1),F(0),F(1,2),F(1)]:
    rejects(lambda u=u:c.f_point(F(2),u,Pi),'Root parameter must lie')
for bracket in [c.Interval(2,2),c.Interval(2,3)]:
    if bracket.lo==bracket.hi:
        rejects(lambda bracket=bracket:c.check_g_bracket(bracket,Pi),'G bracket needs distinct ordered endpoints')
        rejects(lambda bracket=bracket:c.check_root_bracket(F(1,3),bracket,Pi),'Root bracket needs distinct ordered endpoints')
for l,h in [(F(0),F(1,3)),(F(1,3),F(1,2)),(F(3,8),F(1,3))]:
    rejects(lambda l=l,h=h:c.monotone_root_image(l,h,c.Interval(2,F(12,5)),c.OldRootBracket,Pi),'Invalid parameter interval')
root_same=c.monotone_root_image(F(1,3),F(1,3),c.Interval(2,F(12,5)),c.Interval(2,F(12,5)),Pi)
ensure(pair(root_same)==(F(2),F(12,5)),'zero width parameter interval')
rejects(lambda:c.increasing_image(c.Interval(3,4),c.Interval(1,2)),'Inconsistent increasing endpoint images')
for bad in [c.Interval(-2,-1),c.Interval(0,2),c.Interval(2,3),c.Interval(1,1)]:
    rejects(lambda bad=bad:c.check_sqrt_two(bad),'Invalid sqrt(2) enclosure')
rejects(lambda:c.Interval(2,1),'Reversed interval')

def g_ref(a):
    s,_=reference_trig(a,110); s2,_=reference_trig(2*a,130)
    return sub(scale(square(s),8*a**3),mul(square(pi_ref),sub(pt(2*a),s2)))
def u_ref(a):
    s,co=reference_trig(a,110)
    return div(pt(a),scale(sub(pt(a),div(s,co)),2))
aL,aH=c.RootBracket.lo,c.RootBracket.hi
gL,gH=g_ref(aL),g_ref(aH)
ensure(gL[0]>0 and gH[1]<0,'independent strict root signs')
Ul,Uh=u_ref(aL),u_ref(aH); ur=(Ul[0],Uh[1])
dr=div(sub(square((aL,aH)),scale(square(pi_ref),F(1,4))),square(ur))
ensure(F('0.32992250812006654958')<ur[0]<ur[1]<F('0.32992250812006654960'),'independent public u enclosure')
ensure(F('24.9438661384324768968')<dr[0]<dr[1]<F('24.9438661384324769084'),'independent public D enclosure')
ensure(25-dr[1]>F('0.0561') and sub(scale(square(pi_ref),3),dr)[0]>F('4.664947'),'independent T3 margins')
result=c.certificate_checks()
ensure(len(result['checks'])==19 and all(v['exact_comparison_passed'] for v in result['checks']),'all 19 certificate groups')
ensure(contains(pair(result['u_star']),ur) and contains(pair(result['d_star']),dr),'certificate contains independent ungridded evaluation')
archived=json.loads(Path('author_results.json').read_text())
encoded=c.encode(result)
ensure(all(encoded[k]==archived[k] for k in encoded),'all exact author results equality')
validate_display(archived)
old_precision=getcontext().prec
getcontext().prec=3
try: ensure(c.certificate_checks()==result,'proof arithmetic independent of Decimal precision')
finally:getcontext().prec=old_precision
for x in [F(-1,7),F(1,7),F(0),F(-10**60-1,17),F(1,10**150)]:
    ensure(F(c.directed_decimal(x,False))<=x<=F(c.directed_decimal(x,True)),'independent display signs and magnitudes')
output={'status':'PASS','check_counts':dict(counts),'total_checks':sum(counts.values()),
 'certificate_groups':19,'reference_method':'Direct exact factorial sums and ungridded rational intervals; no transcendental floating oracle',
 'limitations':['Finite API regression tests supplement the mathematical review; they do not prove every possible Python input.']}
Path(sys.argv[1]).write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
