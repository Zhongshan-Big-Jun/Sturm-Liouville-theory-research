from pathlib import Path
import re,json,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A='research/artifacts/proof-audit-round10-20260925';Report='reports/proof-audit-round10-20260925'
Paths=['AGENTS.md','README.md','README_EN.md','research_map.md','docs/PROJECT_UNDERSTANDING.md','docs/research-guide.md','scripts/README.md','tools/README.md','literature/maps/FRONTIER.md','lean-proof/README.md','lean-proof/STATUS.md','lean-proof/LEMMA_INDEX.md',Report+'/REPORT.md']
Rows=[];Bad=[];Links=0
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
for Rel,Stale in [('README.md','第十轮审计修订进行中:'),('README_EN.md','Round10 repair in progress.')]:
 if Stale in (R/Rel).read_text():raise RuntimeError('Current landing-page status stale '+Rel)
if '2026-09-25 第十轮审计修缮 (修订与验收完成)' not in (R/'AGENTS.md').read_text():raise RuntimeError('Maintenance completion entry missing')
M=(R/'research_map.md').read_text()
for Id in ['A8','A9','A10','A11','B7','B8']:
 if len(re.findall(r'^\| '+Id+r' \|',M,re.M))!=1:raise RuntimeError('Map node missing/duplicated '+Id)
if '\n\n| B8' in M or 'review pending' in M or 'independent review in progress' in M:raise RuntimeError('Map table/status stale')
if 'PARTIAL' not in next(L for L in M.splitlines() if L.startswith('| B4 |')):raise RuntimeError('Global status expanded')
Index=json.loads((R/'index/tools.json').read_text())
if len(Index['items'])!=89 or len(Index['blocked_items'])!=1:raise RuntimeError('Unexpected library state')
for X in json.loads((R/A/'caller-inventory.json').read_text())['callers']:
 if hashlib.sha256((R/X['path']).read_bytes()).hexdigest()!=X['sha256']:raise RuntimeError('Caller identity drift '+X['path'])
Checkpoint=json.loads((O/'checkpoint-result.json').read_text());CP=json.loads(Path(Checkpoint['snapshot']).read_text())
if hashlib.sha256((R/CP['progress']).read_bytes()).hexdigest()!=CP['progress_sha256']:raise RuntimeError('Progress drift')
for N,Info in CP['inputs'].items():
 if hashlib.sha256((R/N).read_bytes()).hexdigest()!=Info['sha256']:raise RuntimeError('Checkpoint source drift '+N)
Pdf=json.loads((R/A/'pdf-reviewed-final/run.json').read_text())
if Pdf['exit_code']!=0 or hashlib.sha256((R/'docs/SL_gap_nge2_symmetry_recon.pdf').read_bytes()).hexdigest()!=Pdf['pdf_sha256']:raise RuntimeError('PDF drift')
if hashlib.sha256((R/Pdf['source']).read_bytes()).hexdigest()!=Pdf['source_sha256']:raise RuntimeError('PDF source drift')
Library=json.loads((O/'library-verification.json').read_text());assert Library['status']=='PASS'
Result=dict(status='PASS',scope='Current navigation, numerical/formal boundaries, exact caller/source/PDF identities and checkpoint; not an additional mathematical proof.',files=Rows,local_links_checked=Links,broken_links=Bad,caller_bindings=76,checkpoint=Checkpoint['sha256'],checkpoint_inputs=len(CP['inputs']),publication_manifest='Generated and checked by publication prepare/stage after this check.')
(O/'final-document-check.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
(R/Report/'final-document-check.json').write_bytes((O/'final-document-check.json').read_bytes())
print('Final navigation and identity check PASS:',len(Rows),'documents',Links,'links',len(CP['inputs']),'checkpoint inputs')
