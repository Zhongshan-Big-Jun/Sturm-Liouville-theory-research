from pathlib import Path
import hashlib,json,shutil,datetime
O=Path('/mnt/f/tools/math-audit-round9-20260923');R=Path('/mnt/f/LaTeX/BVE research');A=R/'research/artifacts/proof-audit-round9-20260923';D=A/'coordinator'
def require(v,m):
    if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['library-final-check','formal-isolated-semantic-received']:
    require((O/(name+'.json')).is_file(),'Incomplete dependency '+name)
require(json.loads((O/'CURRENT.json').read_text())['status']=='RESEARCH_ACCEPTED_PUBLICATION_PENDING','Documents not finalized')
D.mkdir(exist_ok=True)
Excluded={'baseline.json','protection-result.json','stage-paths.json','stage-expected-sha256.json','staged-verification.json','LOCAL_COMMIT_VERIFICATION.json','DELIVERY.json','final-document-check.json'}
Files=[p for p in O.iterdir() if p.is_file() and p.suffix in {'.json','.jsonl','.py','.md'} and p.name not in Excluded]
Files+=list((O/'transcripts').glob('*.json'))
Rows=[]
for p in sorted(Files):
    n=p.relative_to(O);t=D/n;t.parent.mkdir(parents=True,exist_ok=True)
    if t.exists():require(t.read_bytes()==p.read_bytes(),'Previously archived coordinator record changed '+str(n))
    else:shutil.copyfile(p,t)
    require(sha(t)==sha(p),'Archive copy failed '+str(n))
    Rows.append(dict(path=str(n),sha256=sha(t),bytes=t.stat().st_size))
(D/'README.md').write_text('''# Coordinator execution record

These files copy the actual native author/reviewer dispatch and completion envelopes, original plugin API receipts, correction/release records and final helper source snapshots. They are coordinator provenance, not additional independent mathematics approvals. Reviewer-authored execution archives and immutable review packets live in their separate linked artifact locations.

The baseline manifest stays outside the repository to avoid publishing unrelated original untracked paths. Publication staging and actual remote verification are performed after this evidence freeze and saved externally; they are not predicted here. The CURRENT snapshot records that precise publication boundary.

The first library intake exited 1 after its durable issue write because an inspection result contained tuple dictionary keys that could not be serialized as JSON. The durable issue was reconciled rather than duplicated; later native operations completed. Earlier helper source hashes in native-operations.jsonl identify the versions then executed; copied helper sources are their final versions, not invented reconstructions of old bytes.

queue-reschedule.json records intentionally stopping a waiting queue before it began any write, then moving independent formal reviews to their own scoped review project. This deliberate coordinator SIGTERM is separate from the Lean author's earlier unexplained outer exit143, which remains an incomplete run. No gate or approval was inferred from either interruption.
''',encoding='utf-8')
Rows.append(dict(path='README.md',sha256=sha(D/'README.md'),bytes=(D/'README.md').stat().st_size))
(D/'manifest.json').write_text(json.dumps(dict(status='EXACT_COORDINATOR_COPY_NOT_INDEPENDENT_APPROVAL',archived_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=str(O),excluded_private_baseline=True,files=Rows),ensure_ascii=False,indent=2)+'\n')
print('Archived actual coordinator records:',len(Rows))
