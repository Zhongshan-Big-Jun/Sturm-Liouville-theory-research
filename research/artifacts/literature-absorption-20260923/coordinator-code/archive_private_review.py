from pathlib import Path
import json,sys,hashlib,shutil
O=Path('/mnt/f/tools/sl-literature-absorption-20260923');R=Path('/mnt/f/LaTeX/BVE research');Name=sys.argv[1];Group=sys.argv[2] if len(sys.argv)>2 else Name;Q=O/'verification'/Name
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as V
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and p.read_bytes()!=raw:raise RuntimeError('Immutable archive conflict '+str(p))
    if not p.exists():p.write_bytes(raw)
def jput(p,d):put(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
Dispatch=json.loads((O/(Name+'-review-dispatch.json')).read_text());Check=V.verify_review_bundle(Q,Dispatch['bundle'])
if Check['verdict'] not in ['APPROVED','CHANGES_REQUIRED','INCOMPLETE']:raise RuntimeError('Unrecognized review verdict')
PacketInfo=json.loads((O/(Name+'-review-packet.json')).read_text());Packet=json.loads((Q/PacketInfo['packet']).read_text());A=R/'research/artifacts/literature-absorption-20260923/reviews'/Name
put(A/'packet.json',(Q/PacketInfo['packet']).read_bytes())
for p in (Q/Dispatch['bundle']).iterdir():
    if p.is_file():put(A/'runtime'/p.name,p.read_bytes())
for n in ['spawn','completion','received']:
    put(A/(n+'.json'),(O/(Name+'-review-'+n+'.json')).read_bytes())
Rows=[]
for p,info in Packet['inputs'].items():
    raw=(Q/p).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=info['sha256']:raise RuntimeError('Private packet drift '+p)
    row=dict(input_path=p,sha256=info['sha256'],role=info['role'])
    if p.startswith('private/') and not p.startswith('private/checks/'):
        row.update(availability='PRIVATE_PRIMARY_ORIGINAL_OR_EXTRACTION',local_path=str(Q/p),recovery='Use primary URL/version/hash in the author manifest and source-catalog; original source bodies are not redistributed in this export.')
    elif p=='private-sources/publisher-web-search.json' or p.startswith('private-sources/'):
        row.update(availability='PRIVATE_PRIMARY_SOURCE',local_path=str(Q/p),recovery='Use exact source-catalog and author manifest; no whole-source copy in public export.')
    else:
        candidate=R/p[len('project/'):] if p.startswith('project/') else R/'literature/absorption-20260923'/Group/p
        if candidate.exists() and sha(candidate)==info['sha256']:
            row.update(availability='PUBLIC_EXACT_INPUT',public_path=candidate.relative_to(R).as_posix())
        else:
            candidate=A/'supplemental-inputs'/p;put(candidate,raw)
            row.update(availability='PUBLIC_EXACT_INPUT',public_path=candidate.relative_to(R).as_posix())
    Rows.append(row)
Meta=dict(schema='private-source-review-export/v1',verdict=Check['verdict'],packet_sha256=PacketInfo['packet_sha256'],reviewer_id=Dispatch['reviewer_id'],fork_context=False,original_review_project=str(Q),original_runtime_bundle=Dispatch['bundle'],local_runtime_verification=Check,public_export_scope='Native dispatch/completion/report and exact public-input mapping. Raw third-party primary papers/extractions remain private. This directory is an evidence export, not a complete in-repository research_review runtime bundle.',inputs=Rows)
jput(A/'provenance.json',Meta)
if Group=='interfaces':
    T=Path('/tmp/sl-stateless-e7e17f4f-review-zlg4nf1v')
    for n in ['check_calibrations.py','stdout.json','stderr.log']:
        if (T/n).exists():put(A/'independent-replay'/n,(T/n).read_bytes())
print('Archived native review',Name,Check['verdict'],'with',len(Rows),'exact input pointers; private source bodies excluded.')
