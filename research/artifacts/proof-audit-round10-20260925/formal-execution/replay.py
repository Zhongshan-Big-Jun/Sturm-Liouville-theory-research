from pathlib import Path
import datetime, hashlib, json, os, subprocess, time, sys, gzip, re

BASE=Path(__file__).resolve().parent
CONF=json.loads((BASE/'config.json').read_text())
PACKET=Path(CONF['packet'])
P=json.loads(PACKET.read_text())
PROJECT=BASE/'project'
RUNTIME=Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0')
LEAN=RUNTIME/'bin/lean.exe'
LAKE=RUNTIME/'bin/lake.exe'
PACKAGE_BASE=Path('/mnt/f/LaTeX/BVE research/lean-proof/.lake/packages')

def digest(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def frozen(k):return PACKET.parent/P['inputs'][k]['snapshot']
def win(p):return subprocess.check_output(['wslpath','-w',str(Path(p).resolve())],text=True).strip()
def environment():
 e=os.environ.copy()
 paths=[BASE/'objects']+[PACKAGE_BASE/p['name']/'.lake/build/lib/lean' for p in json.loads((PROJECT/'lake-manifest.json').read_text())['packages']]
 e['LEAN_PATH']=';'.join(win(p) for p in paths if p.is_dir())
 e['LEAN_SRC_PATH']='';e['PYTHONDONTWRITEBYTECODE']='1'
 e['TMPDIR']=str(BASE/'tmp');e['TEMP']=e['TMP']=win(BASE/'tmp')
 keys=['LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP']
 e['WSLENV']=':'.join([s for s in e.get('WSLENV','').split(':') if s and s.split('/')[0] not in keys]+keys)
 return e

def run(label,args,inputs=()):
 out=BASE/'commands'/label;out.mkdir(exist_ok=False)
 e=environment(); inp=[Path(__file__),PROJECT/'lean-toolchain',PROJECT/'lakefile.toml',PROJECT/'lake-manifest.json',*map(Path,inputs)]
 local=list((BASE/'objects').glob('*'))
 before={str(p):digest(p) for p in inp+local if p.is_file()}
 rec={'role':'independent-reviewer','argv':list(map(str,args)),'cwd':str(PROJECT),'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs_before':before,'environment':{k:e.get(k) for k in ['LEAN_PATH','LEAN_SRC_PATH','WSLENV','TMPDIR','TEMP','TMP','PYTHONDONTWRITEBYTECODE']}}
 write(out/'command.json',rec); start=time.monotonic()
 with (out/'stdout.log').open('wb') as so,(out/'stderr.log').open('wb') as se:
  proc=subprocess.Popen(rec['argv'],cwd=PROJECT,env=e,stdout=so,stderr=se)
  rec['pid']=proc.pid;write(out/'command.json',rec)
  try:rec['exit_code']=proc.wait(timeout=300)
  except subprocess.TimeoutExpired:
   proc.kill();proc.wait();rec['exit_code']=proc.returncode;rec['timeout']=True
 rec.update(seconds=time.monotonic()-start,utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs_after={p:digest(p) for p in before},stdout_sha256=digest(out/'stdout.log'),stderr_sha256=digest(out/'stderr.log'))
 rec['inputs_unchanged']=rec['inputs_before']==rec['inputs_after'];write(out/'command.json',rec)
 print(label,rec['exit_code'],round(rec['seconds'],2),flush=True)
 if rec['exit_code']!=0:print((out/'stdout.log').read_text(errors='replace')[-3000:],flush=True)
 return rec

def compile(label,name):
 src=PROJECT/name
 return run(label,[LEAN,'-R',win(PROJECT),'-o',win(BASE/'objects'/src.with_suffix('.olean').name),win(src)],[src])

def main():
 m=json.loads(gzip.decompress(frozen('inputs/exact-root/run-manifest.json.gz').read_bytes()))
 runtime={name:{'actual':digest(RUNTIME/name),'expected':h} for name,h in m['environment']['binary_hashes'].items()}
 for x in runtime.values():x['matches']=x['actual']==x['expected']
 write(BASE/'evidence'/'runtime-identities.json',runtime)
 assert all(x['matches'] for x in runtime.values())
 assert run('lean-version',[LEAN,'--version'])['exit_code']==0
 assert run('lake-version',[LAKE,'--version'])['exit_code']==0
 assert run('discover-imports',[LEAN,'--run',win(PROJECT/'DiscoverImports.lean'),win(PROJECT/'AuditRound10.lean')],[PROJECT/'DiscoverImports.lean',PROJECT/'AuditRound10.lean'])['exit_code']==0
 assert run('main-deps',[LEAN,'--deps',win(PROJECT/'AuditRound10.lean')],[PROJECT/'AuditRound10.lean'])['exit_code']==0
 assert compile('main','AuditRound10.lean')['exit_code']==0
 assert compile('positive-controls','Counterexamples.lean')['exit_code']==0
 assert run('controls-deps',[LEAN,'--deps',win(PROJECT/'Counterexamples.lean')],[PROJECT/'Counterexamples.lean'])['exit_code']==0
 for label,name in [('negative-flip','NegativeFlip.lean'),('negative-reflection','NegativeReflection.lean'),('negative-index','NegativeIndex.lean')]:
  assert compile(label,name)['exit_code']==1
 for label,name in [('print-main','PrintAuditRound10.lean'),('print-controls','PrintCounterexamples.lean')]:
  assert compile(label,name)['exit_code']==0
 contract=json.loads(frozen('inputs/root-contract.json').read_text())
 literal=frozen('inputs/root-exact-type.lean.txt').read_text()
 assert literal.strip()==contract['expected_type'].strip()
 preamble='import LeanVerifyProbe\nimport Counterexamples\nopen AuditRound10\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\nset_option linter.unusedVariables false\n'
 root=preamble+'theorem Reviewer.literal_root :\n'+literal+' := by\n  exact AuditRound10.root\n'
 root+='\n#print axioms AuditRound10.root\n#print axioms Reviewer.literal_root\n'
 root+='#lean_verify_v2 AuditRound10.root expected Reviewer.literal_root output '+json.dumps(win(BASE/'evidence'/'root-inspection.json'))+'\n'
 (PROJECT/'LiteralRoot.lean').write_text(root)
 assert compile('probe','LeanVerifyProbe.lean')['exit_code']==0
 assert run('root-deps',[LEAN,'--deps',win(PROJECT/'LiteralRoot.lean')],[PROJECT/'LiteralRoot.lean'])['exit_code']==0
 assert compile('literal-root','LiteralRoot.lean')['exit_code']==0
 controls='import Counterexamples\nopen AuditRound10\nnamespace Reviewer\n'
 for file,decl in [('NegativeFlip.lean','flip_not_projection'),('NegativeReflection.lean','reflection_plus_sign_false'),('NegativeIndex.lean','phase_off_by_one_false')]:
  s=(PROJECT/file).read_text();prop=s.split('example :',1)[1].split(':= by',1)[0].strip()
  controls+='theorem exact_negation_'+decl+' : ¬ ('+prop+') := AuditRound10Controls.'+decl+'\n'
 controls+='end Reviewer\n';(PROJECT/'LiteralNegations.lean').write_text(controls)
 assert compile('literal-negations','LiteralNegations.lean')['exit_code']==0
 src=frozen('inputs/project/ReadbackExportFull.lean').read_text()
 old=src.split('\n#export_round10 ',1)[1].strip()
 src=src.replace(old,json.dumps(win(BASE/'evidence'/'formal-declarations-full.json')))
 (PROJECT/'PrivateExport.lean').write_text(src)
 assert compile('full-export','PrivateExport.lean')['exit_code']==0
 export=json.loads((BASE/'evidence'/'formal-declarations-full.json').read_text()); orig=json.loads(frozen('inputs/formal-declarations-full.json').read_text())
 eq={'entries_actual':len(export),'entries_expected':len(orig),'identical':export==orig,'actual_sha256':digest(BASE/'evidence'/'formal-declarations-full.json'),'expected_sha256':digest(frozen('inputs/formal-declarations-full.json'))}
 write(BASE/'evidence'/'export-comparison.json',eq);print('EXPORT_COMPARISON',eq,flush=True)
 expected=json.loads(frozen('inputs/per-declaration-axioms.json').read_text());actual={}
 for label in ['print-main','print-controls']:
  for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",(BASE/'commands'/label/'stdout.log').read_text()):
   actual[n]=re.findall(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*',re.sub(r'\.\{[^}]*\}','',a))
 comp={'actual':actual,'all_match':set(actual)==set(expected) and all(set(a)==set(expected[n]['axioms']) for n,a in actual.items())}
 write(BASE/'evidence'/'axiom-comparison.json',comp)
 t=json.loads((BASE/'evidence'/'root-inspection.json').read_text())
 rootcheck={'comparison':{k:v for k,v in t['comparison'].items() if k!='expected_type_expression'},'axioms':t['axioms'],'unsafe_dependencies':[d['name'] for d in t['dependencies'] if d.get('unsafe')],'missing_dependencies':[d['name'] for d in t['dependencies'] if d.get('missing')],'loaded_module_count':t['loaded_module_count'],'dependency_count':len(t['dependencies']),'semantic_dependency_count':len(t['semantic_dependencies']),'root_type_expression_matches_author':t['type_expression']==m['target']['type_expression'],'semantic_dependencies_match_author':t['semantic_dependencies']==m['target']['semantic_dependencies'],'dependencies_match_author':t['dependencies']==m['target']['dependencies']}
 write(BASE/'evidence'/'root-comparison.json',rootcheck);print('ROOT_COMPARISON',rootcheck,flush=True)
 print('REPLAY_FINISHED',str(BASE),flush=True)

if __name__=='__main__':main()
