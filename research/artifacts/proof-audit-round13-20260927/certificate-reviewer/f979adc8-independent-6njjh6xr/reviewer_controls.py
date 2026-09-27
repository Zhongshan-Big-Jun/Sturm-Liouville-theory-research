from pathlib import Path
from fractions import Fraction as F
import json,sys,subprocess,os,hashlib,time,copy
ROOT=Path(__file__).resolve().parent
SNAP=ROOT/'snapshots';MISC=SNAP/'misc'; OUT=ROOT/'controls';OUT.mkdir(exist_ok=True)
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(ROOT/'tmp'))
RESULTS=[]
def require(c,m):
 if not c:raise RuntimeError(m)
def run(label,argv):
 start=time.monotonic();p=subprocess.run(argv,env=ENV,cwd=ROOT,text=True,capture_output=True,timeout=300)
 (OUT/(label+'.stdout')).write_text(p.stdout);(OUT/(label+'.stderr')).write_text(p.stderr)
 row={'name':label,'argv':list(map(str,argv)),'returncode':p.returncode,'seconds':time.monotonic()-start};RESULTS.append(row);print(json.dumps(row),flush=True);return p
CODE=r'''
from pathlib import Path
import sys
sys.path.insert(0,sys.argv[1])
import e1_certgen as G
from rigid1d import I,D2
mode=sys.argv[2];original=G.quantity;old_eval=G._evaluate
def changed(key,g):
 if key=='B1':
  if mode=='exception':raise ArithmeticError('independent reviewer deliberate exception')
  return D2(I(-1),I(0),I(0))
 return original(key,g)
if mode in ('false','exception'):G.quantity=changed
if mode=='unknown':
 def changed_eval(spec,ledger):
  if spec['kind']=='point':return None,{'reason':'reviewer deliberate unknown'}
  return old_eval(spec,ledger)
 G._evaluate=changed_eval
raise SystemExit(G.main(['--output',sys.argv[3]]))
'''
RAW=(MISC/'e1_cert_ledger.json').read_bytes()
STATUS=(MISC/'e1_cert_ledger.status.json').read_bytes()
for mode,opt in [('normal',[]),('optimized',['-O'])]:
 prefix=[sys.executable,*opt,'-B']
 positive=run(mode+'-receiver-positive',prefix+[str(MISC/'e1_cert_receive.py'),str(MISC/'e1_cert_ledger.json')])
 require(positive.returncode==0 and json.loads(positive.stdout)['facts']==57,'positive reception failed')
 table=OUT/(mode+'-positive.tex')
 p=run(mode+'-table-positive',prefix+[str(MISC/'e1_cert_tables.py'),'--ledger',str(MISC/'e1_cert_ledger.json'),'--output',str(table)])
 require(p.returncode==0,'positive export failed')
 require(table.read_bytes()==(MISC/'e1_cert_tables.tex').read_bytes(),'table bytes differ')
 # The exact invocation in the frozen test fails before reception even on good input.
 p=run(mode+'-supplied-test-cli-on-valid-ledger',prefix+[str(MISC/'e1_cert_receive.py'),'--ledger',str(MISC/'e1_cert_ledger.json')])
 require(p.returncode==2 and 'unrecognized arguments: --ledger' in p.stderr,'CLI evidence differs')
 for fault,exit_code in [('false',1),('exception',2),('unknown',1)]:
  directory=OUT/(mode+'-'+fault);directory.mkdir(exist_ok=True)
  ledger=directory/'ledger.json';ledger.write_bytes(RAW);ledger.with_suffix('.status.json').write_bytes(STATUS)
  table=directory/'table.tex';table.write_text('prior table sentinel\n')
  p=run(mode+'-'+fault+'-generation',prefix+['-c',CODE,str(MISC),fault,str(ledger)])
  require(p.returncode==exit_code,'wrong generation exit')
  require(ledger.read_bytes()==RAW,'failed generation changed accepted ledger')
  status=json.loads(ledger.with_suffix('.status.json').read_text());require(status['status'] in ('ERROR','NOT_CERTIFIED'),'failed generation has successful status')
  p=run(mode+'-'+fault+'-reception',prefix+[str(MISC/'e1_cert_receive.py'),str(ledger)])
  require(p.returncode==1 and json.loads(p.stderr)['status']=='REJECTED' and 'last generation did not succeed' in json.loads(p.stderr)['message'],'receiver failed to reject current status')
  p=run(mode+'-'+fault+'-export',prefix+[str(MISC/'e1_cert_tables.py'),'--ledger',str(ledger),'--output',str(table)])
  require(p.returncode!=0 and 'last generation did not succeed' in p.stderr,'table exporter failed to reject current status')
  require(table.read_text()=='prior table sentinel\n','failed exporter changed table')
 # Check a semantically damaged certificate with matching transport hash.
 directory=OUT/(mode+'-mutated-contract');directory.mkdir(exist_ok=True)
 sys.set_int_max_str_digits(1000000)
 data=json.loads(RAW);data['facts'][1]['detail']['target']='0/1'
 ledger=directory/'ledger.json';ledger.write_text(json.dumps(data)+'\n')
 ledger.with_suffix('.status.json').write_text(json.dumps({'status':'PASS','ledger_sha256':hashlib.sha256(ledger.read_bytes()).hexdigest()})+'\n')
 p=run(mode+'-mutated-contract-reception',prefix+[str(MISC/'e1_cert_receive.py'),str(ledger)])
 require(p.returncode==1 and 'point contract mismatch' in json.loads(p.stderr)['message'],'contract tamper not rejected')
(OUT/'results.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
print('ALL_INDEPENDENT_CONTROLS_PASSED',flush=True)
