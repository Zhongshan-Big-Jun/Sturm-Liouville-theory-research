"""Frozen-input audit; all generated files stay in this review directory."""
from pathlib import Path
from fractions import Fraction as F
import ast
import collections
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
SNAP = ROOT / 'snapshot'
sys.set_int_max_str_digits(1000000)
sys.dont_write_bytecode = True
sys.path.insert(0, str(SNAP / 'misc'))
from rigid1d import I, D2, I_sin, I_cos, d2_sin, PI

def check(ok, why):
    if not ok:
        raise RuntimeError(why)

def pair(v):
    a,b = map(F,v)
    check(a<=b, 'interval order')
    return a,b

def encloses(exact, display):
    a,b=pair(exact); l,h=pair(display)
    check(l<=a<=b<=h, 'inward display')
    if a<b:
        check(l<h, 'false singleton')

def endpoints(x):
    return [str(x.lo),str(x.hi)]

def witness(d, key, cmp, target):
    a,b=pair(d[key+'_exact'])
    encloses(d[key+'_exact'],d[key])
    margin=a-target if cmp in ('ge','gt') else target-b
    check(margin>0 if cmp in ('gt','lt') else margin>=0, 'failed actual predicate')
    check(F(d['margin_exact'])==margin,'exact margin')
    check(F(d['margin'])<=margin,'upward margin')
    check(d['ok'] is True,'unproved witness')
    return margin

tree=ast.parse((SNAP/'misc/e1_certificate_io.py').read_text())
specs=points=None
for node in tree.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
        if node.targets[0].id=='FACT_SPECS':
            specs=json.loads(ast.literal_eval(node.value.args[0]))
        if node.targets[0].id=='PRIMITIVE_POINTS':
            points=ast.literal_eval(node.value)
check(specs is not None and points is not None,'contract extraction')

raw=(SNAP/'misc/e1_cert_ledger.json').read_bytes()
ledger=json.loads(raw)
status=json.loads((SNAP/'misc/e1_cert_ledger.status.json').read_text())
check(status['status']=='PASS' and status['ledger_sha256']==hashlib.sha256(raw).hexdigest(),'publication binding')
check(ledger['schema']=='e1-exact-certificate/v2' and ledger['status']=='PASS','schema and status')
check(ledger['summary']=={'total':57,'passed':57,'failed':0,'errors':0},'complete summary')
for name,digest in ledger['meta']['source_sha256'].items():
    check(hashlib.sha256((SNAP/'misc'/name).read_bytes()).hexdigest()==digest,'source binding')
check(len(specs)==len(ledger['facts'])==57,'complete fact count')

counts=collections.Counter()
fact_results=[]
component_intervals={(F(p),F(p)) for p in points}
for row,spec in zip(ledger['facts'],specs):
    check(row['statement']==spec and row['name']==spec['name'] and row['kind']==spec['kind'],'statement identity')
    check(row['ok'] is True and row['status']=='PASS','row acceptance')
    d=row['detail']; cmp=spec['comparison']; target=F(spec['target'])
    margins=[]
    counts[spec['kind']]+=1
    if spec['kind']=='point':
        check(d['point']==spec['point'] and d['cmp']==cmp and F(d['target'])==target,'point contract')
        margins.append(witness(d,'val',cmp,target))
        if spec['expression']!='h':
            component_intervals.add((F(spec['point']),F(spec['point'])))
    elif spec['kind'] in ('value-taylor','deriv-taylor'):
        a,b=map(F,spec['domain']); n=spec['n']
        check(a<b and n>=1 and d['n']==n and len(d['pieces'])==n,'partition size')
        check(d['cmp']==cmp and F(d['target'])==target,'Taylor predicate')
        for j,p in enumerate(d['pieces']):
            lo=a+(b-a)*F(j,n); hi=a+(b-a)*F(j+1,n)
            c=(lo+hi)/2; w=(hi-lo)/2
            check(pair(p['cell'])==(lo,hi) and F(p['c'])==c,'exact partition/center')
            ck='fvc' if spec['kind']=='value-taylor' else 'fpc'
            center=pair(p[ck+'_exact'])
            encloses(p[ck+'_exact'],p[ck])
            slope=pair(p['slope_exact'])+pair(p['slope_center_exact'])
            M=max(abs(z) for z in slope); radius=M*w
            check(F(p['M_exact'])==M and F(p['corr_exact'])==radius,'exact Taylor radius')
            check(F(p['M'])>=M and F(p['corr'])>=radius,'radius display direction')
            check(pair(p['bound_exact'])==(center[0]-radius,center[1]+radius),'Taylor final bound')
            margins.append(witness(p,'bound',cmp,target))
            component_intervals.update(((lo,hi),(c,c)))
            counts['Taylor cells']+=1
    elif spec['kind']=='analytic':
        a=pair(d['A_exact']); s=pair(d['sin_exact']); co=pair(d['cos_exact'])
        check(min(a[0],s[0],co[0])>0,'B1 sign hypotheses')
        check(pair(d['bound_exact'])==(-3*co[1]-a[1]*s[1],-3*co[0]-a[0]*s[0]),'B1 derivative')
        margins.append(witness(d,'bound','lt',F(0)))
    else:
        check(spec['kind']=='concavity-reduction','supported proof kind')
        check(d['dependencies']==['h(gamma) >= m at 0.655','h(13/10) >= m'],'h endpoint dependencies')
        a,b=pair(d['argument_range_exact'])
        check(F(131,200)<=a<=b<=F(13,10),'h argument range')
    fact_results.append({'name':row['name'],'kind':row['kind'],'minimum_margin':str(min(margins)) if margins else None})

concavity=ledger['proofs']['h-concavity']
check(concavity['domain']==['131/200','13/10'] and len(concavity['cells'])==8,'h coverage')
for j,cell in enumerate(concavity['cells']):
    a,b=F(131,200),F(13,10)
    lo=a+(b-a)*F(j,8); hi=a+(b-a)*F(j+1,8)
    check(pair(cell['cell'])==(lo,hi),'concavity exact partition')
    check(pair(cell['second_derivative_exact'])[1]<0,'strict concavity witness')
    g=D2(I(lo,hi),1,0)
    h=g*d2_sin(g)*__import__('rigid1d').d2_cos(g)
    check(pair(cell['second_derivative_exact'])==(h.d2.lo,h.d2.hi),'recomputed h derivative enclosure')

check([r['point'] for r in ledger['primitives']]==points,'primitive coverage')
for r in ledger['primitives']:
    for k in ('sg','cg','tau','A','D'):
        encloses(r[k+'_exact'],r[k])
check(pair(ledger['proofs']['pi_exact'])==(PI.lo,PI.hi),'pi witness')

# These are every distinct gamma interval passed to comps2 by this generator.
# Denominator positivity is proved by enclosing the whole interval, not sampling.
domain_rows=[]
for lo,hi in sorted(component_intervals):
    g=I(lo,hi); s=I_sin(g); c=I_cos(g); den=I(1)+3*s*s
    check(F(131,200)<=lo<=hi<=F(1309,1250)<PI.lo/2,'gamma branch')
    check(s.lo>0 and c.lo>0 and den.lo>0,'division and square root hypotheses')
    arg=2*s/c
    check(arg.lo>1,'actual atan branch')
    check((hi-lo)/2<=1,'actual trig offset domain')
    check(den.sqrt().lo>0,'dual sqrt derivative denominator')
    domain_rows.append({'interval':[str(lo),str(hi)],'cosine_lower':str(c.lo),'sqrt_input_lower':str(den.lo),'atan_argument_lower':str(arg.lo)})

# Independent boundary calculations used by the stated Q-image correction.
check(PI.hi<F(3927,1250) and PI.lo>F(6283,2000),'rational pi bounds')
x=F(841,1000)
check(1-x*x/2+x**4/24-x**6/720>F(2,3),'alpha1 lower endpoint')
check(5*PI.hi/14<F(561,500) and PI.hi/3<F(1309,1250),'upper phase endpoints')
prims={r['point']:r for r in ledger['primitives']}
check(F(2,5)*(PI.lo-F(131,200))>F(prims['131/200']['tau_exact'][1]),'gamma lower endpoint')

# Recheck the rational T1 estimates, using a supporting tangent to certify the
# minimum between .96 and .97 rather than inferring it from the endpoint minima.
def fun(x):
    return F(89,100)*d2_sin(F(4,5)*x)-(x-F(89,250))*d2_sin(2*x)
l=fun(D2(I(F(24,25)),1,0)); r=fun(D2(I(F(97,100)),1,0))
check(l.v.lo>F(1,20) and -F(1,20)<l.d1.lo<=l.d1.hi<0<r.d1.lo,'T1 endpoint values and slopes')
support=l.v.lo+l.d1.lo/F(100)
check(support>F(49,1000),'supporting tangent lower bound at right endpoint')
# F''>3/2 on the entire domain is established via the source's monotone g(y)
# reduction and the following independently enclosed rational endpoints.
co=__import__('rigid1d').I_cos
check((F(3,2)*I_sin(I(F(359,400)))-F(383,500)*co(I(F(359,400)))).lo>0,'g increasing bound')
lower=(4*(F(97,200)*co(I(F(13,100)))+co(I(F(3649,2500))))-F(356,625)*I_sin(I(F(561,625)))).lo
check(lower>F(3,2),'T1 F convexity lower bound')
check(4+F(187,100)-(F(89,100)**2*8-F(4,3))==F(6499,7500),'T1 final arithmetic')
check(F(6499,7500)>F(1733,2000)>0,'T1 boundary margin')
mu=[F(11,5)+F(3,10)+F(57,50),F(13,5)+F(3,10)+F(3,2),F(27,10)+F(3,10)+F(3,2),F(13,5)+F(3,10)+F(3,2),F(2)+F(3,20)+F(3,2),F(2)+F(3,20)+F(19,10),F(19,10)+F(1,10)+F(19,10),F(9,5)+F(1,10)+F(19,10),F(3,5)+F(1,25)+F(4,3),F(3,8)+F(1,40)+F(11,10)-F(63,100)*F(33,200)]
check(min(mu)==F(27921,20000)>F(139,100),'T2 closed-domain margin')

table=(SNAP/'misc/e1_cert_tables.tex').read_text()
doc=(SNAP/'docs/SL_gap_n1_O3a_phase_rigidity_proof.tex').read_text()
check(table.strip() in doc,'embedded table identity')

results={'status':'PASS','counts':dict(counts),'primitive_rows':len(points),'concavity_cells':8,'component_argument_intervals':len(component_intervals),'table_embedded_verbatim':True,'T1_supporting_tangent_lower_bound':str(support),'T1_convexity_lower_bound':str(lower),'T2_minimum_mu':str(min(mu)),'facts':fact_results,'domains':domain_rows}
(ROOT/'outputs/independent_checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if k not in ('facts','domains','T1_supporting_tangent_lower_bound','T1_convexity_lower_bound')},indent=2))
