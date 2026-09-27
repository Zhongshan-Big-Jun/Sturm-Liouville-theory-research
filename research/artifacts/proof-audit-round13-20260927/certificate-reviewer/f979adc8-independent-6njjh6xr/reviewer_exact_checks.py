from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import ast,json,sys,re,hashlib
ROOT=Path(__file__).resolve().parent;SNAP=ROOT/'snapshots';sys.dont_write_bytecode=True
sys.set_int_max_str_digits(1000000)
sys.path.insert(0,str(SNAP/'misc'))
import rigid1d as R
# The witness checks below do not call the supplied validator or display functions.
data=json.loads((SNAP/'misc/e1_cert_ledger.json').read_text())
def check(c,m):
 if not c:raise RuntimeError(m)
def interval(v):
 a,b=map(F,v);check(a<=b,'reversed interval');return a,b
def shown(exact,display):
 a,b=interval(exact);l,u=interval(display);check(l<=a<=b<=u,'inward display')
def pred(bounds,cmp,target):
 a,b=bounds;t=F(target)
 margin=a-t if cmp in ['gt','ge'] else t-b
 check(cmp in ['lt','le','gt','ge'],'bad comparator')
 check(margin>0 if cmp in ['lt','gt'] else margin>=0,'failed exact predicate')
 return margin
specs=[];primitive_points=None
for n in ast.parse((SNAP/'misc/e1_certificate_io.py').read_text()).body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
  if n.targets[0].id=='FACT_SPECS':specs=json.loads(ast.literal_eval(n.value.args[0]))
  if n.targets[0].id=='PRIMITIVE_POINTS':primitive_points=ast.literal_eval(n.value)
check(len(specs)==len(data['facts'])==57,'fact coverage')
point_ct=cell_ct=0;all_margins=[];component_calls=set();h_calls=set()
for p in primitive_points:component_calls.add((F(p),F(p)))
for row,spec in zip(data['facts'],specs):
 check(row['statement']==spec,'statement mismatch');d=row['detail'];k=spec['kind'];exp=spec['expression']
 cmp,t=spec['comparison'],spec['target']
 check(row['ok'] is True and row['status']=='PASS','non-PASS row')
 if k=='point':
  shown(d['val_exact'],d['val']);margin=pred(interval(d['val_exact']),cmp,t)
  check(F(d['margin_exact'])==margin and F(d['margin'])<=margin,'point margin direction')
  x=F(spec['point']);(h_calls if exp=='h' else component_calls).add((x,x))
  point_ct+=1;all_margins.append(margin)
 elif k in ('value-taylor','deriv-taylor'):
  a,b=map(F,spec['domain']);n=spec['n'];check(len(d['pieces'])==n,'cell count')
  for i,p in enumerate(d['pieces']):
   l=a+(b-a)*F(i,n);u=a+(b-a)*F(i+1,n);c=(l+u)/2;w=(u-l)/2
   check(interval(p['cell'])==(l,u) and F(p['c'])==c,'cell identity')
   ckey='fvc' if k=='value-taylor' else 'fpc';center=interval(p[ckey+'_exact'])
   shown(p[ckey+'_exact'],p[ckey])
   slopes=interval(p['slope_exact'])+interval(p['slope_center_exact']);m=max(abs(v) for v in slopes)
   check(F(p['M_exact'])==m and F(p['M'])>=m,'M direction')
   correction=m*w;check(F(p['corr_exact'])==correction and F(p['corr'])>=correction,'radius direction')
   bounds=(center[0]-correction,center[1]+correction)
   check(interval(p['bound_exact'])==bounds,'bound arithmetic');shown(p['bound_exact'],p['bound'])
   margin=pred(bounds,cmp,t);check(F(p['margin_exact'])==margin and F(p['margin'])<=margin,'margin direction')
   check(p['ok'] is True,'false cell');all_margins.append(margin);cell_ct+=1
   calls=h_calls if exp=='h' else component_calls;calls.update([(l,u),(c,c)])
 elif k=='analytic':
  a,s,c=[interval(d[key]) for key in ['A_exact','sin_exact','cos_exact']]
  check(min(a[0],s[0],c[0])>0,'B1 factors')
  bound=(-3*c[1]-a[1]*s[1],-3*c[0]-a[0]*s[0]);check(bound==interval(d['bound_exact']),'B1 identity')
  shown(d['bound_exact'],d['bound']);margin=pred(bound,cmp,t);check(F(d['margin_exact'])==margin and F(d['margin'])<=margin,'B1 margin')
 elif k=='concavity-reduction':
  check(d['dependencies']==['h(gamma) >= m at 0.655','h(13/10) >= m'],'concavity premises')
 else:raise RuntimeError('unexpected kind')
concavity=data['proofs']['h-concavity'];a,b=F(131,200),F(13,10)
for i,p in enumerate(concavity['cells']):
 l=a+(b-a)*F(i,8);u=a+(b-a)*F(i+1,8);check(interval(p['cell'])==(l,u),'concavity coverage');h_calls.add((l,u))
 # Independent symbolic second-derivative formula, using the proved rational primitives.
 x=R.I(l,u);independent=2*R.I_cos(2*x)-2*x*R.I_sin(2*x)
 check(independent.hi<0,'independent concavity enclosure failed')
 check(interval(p['second_derivative_exact'])[1]<0,'recorded concavity not strict')
check(len(concavity['cells'])==8,'concavity count')
check(F(1309,1250)<R.PI.lo/2 and F(13,10)<R.PI.lo/2,'branch bounds')
# Every primitive call domain is derived from the actual frozen generator loops:
# component points, Taylor cells and centers; h points/cells; B1 analytic interval.
min_cos=None;min_arg=None;min_sqrt=None;max_width=F(0)
for l,u in sorted(component_calls):
 check(F(131,200)<=l<=u<=F(1309,1250),'gamma domain')
 x=R.I(l,u);s,c=R.I_sin(x),R.I_cos(x)
 check(s.lo>0 and c.lo>0,'tangent denominator or sign')
 argument=2*s/c;root_arg=1+3*s*s;root=root_arg.sqrt()
 check(argument.lo>1,'actual atan branch differs');check(root_arg.lo>0 and root.lo>0,'sqrt domain')
 min_cos=c.lo if min_cos is None else min(min_cos,c.lo)
 min_arg=argument.lo if min_arg is None else min(min_arg,argument.lo)
 min_sqrt=root_arg.lo if min_sqrt is None else min(min_sqrt,root_arg.lo)
 max_width=max(max_width,(u-l)/2)
for l,u in h_calls:
 check(a<=l<=u<=b,'h domain');max_width=max(max_width,(u-l)/2)
max_width=max(max_width,(F(1309,1250)-F(131,200))/2)
check(max_width<=1,'trig offset beyond narrow branch')
for row in data['primitives']:
 for key in ['sg','cg','A','D','tau']:shown(row[key+'_exact'],row[key])
# Exact secondary constants used in the analytic h reduction in the document.
y=R.I(F(131,100));check(R.I_cos(y).hi<F(26,100),'h proof cosine constant')
check(F(131,200)*R.I_sin(y).lo>F(3,5),'h proof sine constant')
# A few universal algorithm consequences checked with rational boundary witnesses.
check(R.I_cos(R.I(F(-1,10),F(1,10))).hi>=1,'cos interior maximum')
check(R.I_sin(R.I(-2,2)).hi>=1,'sin interior maximum')
check(not (R.I(F(997,1000))-R.I_cos(R.I(F(-1,10),F(1,10)))).is_pos(),'old false-positive cosine')
check(not (R.I(F(19,20))-R.I_sin(R.I(-2,2))).is_pos(),'old false-positive sine')
x=R.I_atan(R.I(F(9,10),F(11,10)));check(x.lo<=R.PI.lo/4<=R.PI.hi/4<=x.hi,'cross-one atan enclosure')
summary={'status':'PASS','fact_count':len(data['facts']),'point_witnesses':point_ct,'Taylor_cells':cell_ct,'concavity_cells':8,'primitive_rows':len(data['primitives']),'unique_component_call_intervals':len(component_calls),'unique_h_call_intervals':len(h_calls),'max_trig_offset_radius_exact':str(max_width),'minimum_actual_cos_lower_gt_2_over_5':min_cos>F(2,5),'minimum_actual_atan_argument_lower_gt_1':min_arg>1,'minimum_sqrt_input_lower_gt_2':min_sqrt>2,'smallest_exact_margin_positive':min(all_margins)>0,'saved_table_embedded':(SNAP/'misc/e1_cert_tables.tex').read_text() in (SNAP/'docs/SL_gap_n1_O3a_phase_rigidity_proof.tex').read_text(),'scope':'Independent finite witness arithmetic and actual call-domain enumeration; analytic enclosure proof was checked separately, not inferred from probes.'}
(ROOT/'independent-exact-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
