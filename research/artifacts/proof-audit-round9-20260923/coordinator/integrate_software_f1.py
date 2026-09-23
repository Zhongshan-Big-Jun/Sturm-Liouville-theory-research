from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A=R/'research/artifacts/proof-audit-round9-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as V
P=Path(json.loads((O/'software-review2-root.json').read_text())['project']);Bundle=json.loads((O/'software-isolated-review2-dispatch.json').read_text())['bundle']
if V.verify_review_bundle(P,Bundle)['verdict']!='APPROVED':raise RuntimeError('New software acceptance missing')
First=json.loads((O/'software-review-received.json').read_text())
if First['verdict']!='CHANGES_REQUIRED':raise RuntimeError('Original rejection was not received before source replacement')
Target=R/'scripts/_gapn2_second_variation_probe.py';Candidate=P/'inputs/candidate/_gapn2_second_variation_probe.py'
def sha(Q):return hashlib.sha256(Q.read_bytes()).hexdigest()
Old='53c5ccd85c28f1a5a1e2e37a4eed4e8dc450025eaf313aae15df028eb1f9d31e';New=sha(Candidate)
if sha(Target) not in [Old,New]:raise RuntimeError('Unexpected live numerical source')
for N in ['_gapn2_symmetry_recon.py','_gapn2_jacobian_probe.py','_gapn2_jacobian_analytic.py','op03_gap_table.json']:
	if sha(R/'scripts'/N)!=sha(P/'inputs/candidate'/N):raise RuntimeError('Live dependency drift '+N)
Target.write_bytes(Candidate.read_bytes());Out=A/'current-program-replay';Out.mkdir(exist_ok=True)
Record=Out/'execution.json'
if Record.exists():raise RuntimeError('Replay already exists; inspect before repeating')
Args=[sys.executable,'-B',str(Target),'2','4','sup','--output',str(Out/'results.json')];Start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (Out/'stdout.log').open('wb') as F,(Out/'stderr.log').open('wb') as E:Run=subprocess.run(Args,cwd=R,stdout=F,stderr=E)
D=dict(argv=Args,cwd=str(R),start=Start,end=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=Run.returncode,old_sha256=Old,accepted_new_sha256=New,actual_live_source_sha256=sha(Target),acceptance_project=str(P.relative_to(R)),acceptance_bundle=Bundle)
if Run.returncode==0:
	Actual=json.loads((Out/'results.json').read_text());Expected=json.loads((P/'inputs/candidate/n2R4SUP.json').read_text());Actual.pop('source_sha256');Expected.pop('source_sha256');D['numerical_payload_identical_to_accepted_candidate']=Actual==Expected
Record.write_text(json.dumps(D,indent=2)+'\n')
if Run.returncode!=0 or not D['numerical_payload_identical_to_accepted_candidate']:raise RuntimeError('Actual installed CLI mismatch')
(A/'software-final-integration.json').write_text(json.dumps(D,indent=2)+'\n');print('Accepted software integrated and actual CLI replay matched',New,flush=True)
