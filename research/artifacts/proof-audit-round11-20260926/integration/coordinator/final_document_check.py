from pathlib import Path
import re,json,hashlib,gzip
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round11-20260926');A='research/artifacts/proof-audit-round11-20260926';Report='reports/proof-audit-round11-20260926'
Paths=['AGENTS.md','README.md','README_EN.md','research_map.md','docs/PROJECT_UNDERSTANDING.md','docs/research-guide.md','scripts/README.md','tools/README.md','literature/maps/FRONTIER.md','lean-proof/README.md','lean-proof/STATUS.md','lean-proof/LEMMA_INDEX.md',Report+'/REPORT.md',A+'/README.md','tools/krein-cofinite-closure-all-orders.md']
Rows=[];Bad=[];Links=0
def sha(P):return hashlib.sha256(P.read_bytes()).hexdigest()
for N in Paths:
	P=R/N;B=P.read_bytes();Text=B.decode()
	for M in re.finditer(r'\]\((<?[^)\n]+>?)\)',Text):
		Link=M[1].strip('<>').split('#')[0]
		if not Link or re.match(r'[a-zA-Z]+:',Link):continue
		Dest=(P.parent/Link).resolve();Links+=1
		if Dest==R/Report/'publication-manifest.json':continue
		if not Dest.exists():Bad.append(dict(path=N,link=Link))
	Rows.append(dict(path=N,sha256=hashlib.sha256(B).hexdigest()))
if Bad:raise RuntimeError('Broken active links '+json.dumps(Bad,ensure_ascii=False))
if '2026-09-26 第十一轮审计修缮 (修订与验收完成)' not in (R/'AGENTS.md').read_text():raise RuntimeError('Completion entry missing')
M=(R/'research_map.md').read_text()
for Id in ['A8','A9','A10','A11','A12','B7','B8','B9']:
	if len(re.findall(r'^\| '+Id+r' \|',M,re.M))!=1:raise RuntimeError('Missing or duplicated node '+Id)
if '\n\n| A12' in M or '\n\n| B9' in M:raise RuntimeError('Detached table row')
if 'PARTIAL' not in next(L for L in M.splitlines() if L.startswith('| B4 |')):raise RuntimeError('Global status expanded')
Index=json.loads((R/'index/tools.json').read_text())
if len(Index['items'])!=90 or len(Index['blocked_items'])!=1:raise RuntimeError('Unexpected library state')
Inv=json.loads((R/A/'caller-inventory.json').read_text())
for X in Inv['entries']:
	if sha(R/X['path'])!=X['sha256']:raise RuntimeError('Caller identity drift '+X['path'])
Checkpoint=json.loads((O/'checkpoint-result.json').read_text());CP=json.loads(Path(Checkpoint['snapshot']).read_text())
if sha(R/CP['progress'])!=CP['progress_sha256']:raise RuntimeError('Progress drift')
for N,Info in CP['inputs'].items():
	if sha(R/N)!=Info['sha256']:raise RuntimeError('Checkpoint input drift '+N)
Pdf=json.loads((R/A/'pdf-build/visual-inspection.json').read_text())
if sha(R/'docs/SL_cofinite_all_orders.pdf')!=Pdf['pdf_sha256'] or sha(R/'docs/SL_cofinite_all_orders.tex')!=Pdf['source_sha256']:raise RuntimeError('PDF/source drift')
Library=json.loads((O/'library-verification.json').read_text());assert Library['status']=='PASS'
Formal=json.loads((R/A/'formal-execution/verification-record.json').read_text())
if sha(R/'lean-proof/SL/AuditRound11.lean')!=Formal['source_sha256'] or not Formal['required_checks_complete']:raise RuntimeError('Formal source or execution differs')
ArchiveCount=0
for N in ['lean-author-archive-manifest.json','formal-execution-archive-manifest.json']:
	D=json.loads((R/A/N).read_text())
	for X in D['files']:
		B=(R/A/X['path']).read_bytes()
		if hashlib.sha256(B).hexdigest()!=X['sha256']:raise RuntimeError('Archive encoding drift '+X['path'])
		if X.get('encoding')=='gzip' and hashlib.sha256(gzip.decompress(B)).hexdigest()!=X['original_sha256']:raise RuntimeError('Archive raw drift '+X['path'])
		ArchiveCount+=1
Reviews=json.loads((R/A/'review-summary.json').read_text())['reviews']
if len(Reviews)!=6 or len({X['reviewer_id'] for X in Reviews})!=6 or any(X['verdict']!='APPROVED' for X in Reviews):raise RuntimeError('Independent reviews incomplete')
ReviewInputs=0
for Review in Reviews:
	Name=Review['kind'];RootFile=O/(Name+'-root.json');Root=Path(json.loads(RootFile.read_text())['project']) if RootFile.exists() else R
	PacketFile=Root/json.loads((O/(Name+'-packet.json')).read_text())['packet']
	if sha(PacketFile)!=Review['packet_sha256']:raise RuntimeError('Review packet identity differs '+Name)
	for N,Info in json.loads(PacketFile.read_text())['inputs'].items():
		if sha(Root/N)!=Info['sha256'] or sha(PacketFile.parent/Info['snapshot'])!=Info['sha256']:raise RuntimeError('Reviewed current or snapshot input differs '+Name+' '+N)
		ReviewInputs+=1
Result=dict(status='PASS',scope='Current navigation, scope, exact caller/source/PDF/formal/archive identities and checkpoint; not an additional mathematical proof.',files=Rows,local_links_checked=Links,broken_links=Bad,caller_bindings=len(Inv['entries']),formal_archive_files_checked=ArchiveCount,review_packet_current_and_snapshot_inputs_checked=ReviewInputs,checkpoint=Checkpoint['sha256'],checkpoint_inputs=len(CP['inputs']),publication_manifest='Generated and checked by publication prepare/stage after this check.')
(O/'final-document-check.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n');(R/Report/'final-document-check.json').write_bytes((O/'final-document-check.json').read_bytes())
print('Final document/identity check PASS',len(Rows),'documents',Links,'links',ArchiveCount,'archive files',flush=True)
