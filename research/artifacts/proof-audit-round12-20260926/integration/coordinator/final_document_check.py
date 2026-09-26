from pathlib import Path
import gzip
import hashlib
import json
import re

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Root / 'research/artifacts/proof-audit-round12-20260926'
Report = Root / 'reports/proof-audit-round12-20260926'
Paths = ['AGENTS.md', 'README.md', 'README_EN.md', 'research_map.md', 'docs/PROJECT_UNDERSTANDING.md', 'docs/research-guide.md', 'scripts/README.md', 'tools/README.md', 'literature/maps/FRONTIER.md', 'lean-proof/README.md', 'lean-proof/STATUS.md', 'lean-proof/LEMMA_INDEX.md', 'reports/proof-audit-round12-20260926/REPORT.md', 'research/artifacts/proof-audit-round12-20260926/README.md']
Rows, Bad = [], []
Links = 0

def sha(Path):
	return hashlib.sha256(Path.read_bytes()).hexdigest()

for Name in Paths:
	Path = Root / Name
	Data = Path.read_bytes()
	Text = Data.decode()
	for Match in re.finditer(r'\]\((<?[^)\n]+>?)\)', Text):
		Link = Match[1].strip('<>').split('#')[0]
		if not Link or re.match(r'[a-zA-Z]+:', Link):
			continue
		Destination = (Path.parent / Link).resolve()
		Links += 1
		if Destination in [Report / 'publication-manifest.json', Report / 'final-document-check.json']:
			continue
		if not Destination.exists():
			Bad.append(dict(path=Name, link=Link))
	Rows.append(dict(path=Name, sha256=hashlib.sha256(Data).hexdigest()))
if Bad:
	raise RuntimeError('Broken current navigation links: ' + json.dumps(Bad, ensure_ascii=False))
if '2026-09-26 第十二轮审计修缮 (修订与验收完成)' not in (Root / 'AGENTS.md').read_text():
	raise RuntimeError('AGENTS completion missing')
Map = (Root / 'research_map.md').read_text()
for Name in ['A12', 'B7', 'B8', 'B9', 'B10']:
	if len(re.findall(r'^\| ' + Name + r' \|', Map, re.M)) != 1:
		raise RuntimeError('Missing or duplicated map node: ' + Name)
if 'PARTIAL' not in next(Line for Line in Map.splitlines() if Line.startswith('| B4 |')):
	raise RuntimeError('Global scope was expanded')
Index = json.loads((Root / 'index/tools.json').read_text())
if len(Index['items']) != 90 or len(Index['blocked_items']) != 1:
	raise RuntimeError('Library count differs')
Inventory = json.loads((Artifact / 'caller-inventory.json').read_text())
for Row in Inventory['entries']:
	if sha(Root / Row['path']) != Row['sha256']:
		raise RuntimeError('Caller drift: ' + Row['path'])
Checkpoint = json.loads((Out / 'checkpoint-result.json').read_text())
Snapshot = json.loads(Path(Checkpoint['snapshot']).read_text())
if sha(Root / Snapshot['progress']) != Snapshot['progress_sha256']:
	raise RuntimeError('Progress changed after checkpoint')
for Name, Info in Snapshot['inputs'].items():
	if sha(Root / Name) != Info['sha256']:
		raise RuntimeError('Checkpoint input drift: ' + Name)
if sha(Root / 'lean-proof/SL/AuditRound12.lean') != '21f0a2d46770474e6c32f78ead52c977dcec2f0e589308584d5499c253efa768':
	raise RuntimeError('Formal source differs')
ArchiveCount = 0
for Name in ['lean-author-archive-manifest.json', 'formal-export2-archive-manifest.json', 'formal-execution-archive-manifest.json', 'coordinator-archive-manifest.json', 'integration/archive-manifest.json']:
	Manifest = json.loads((Artifact / Name).read_text())
	for Row in Manifest['files']:
		Data = (Artifact / Row['path']).read_bytes()
		if hashlib.sha256(Data).hexdigest() != Row['sha256']:
			raise RuntimeError('Archive encoding drift: ' + Row['path'])
		if Row.get('encoding') == 'gzip' and hashlib.sha256(gzip.decompress(Data)).hexdigest() != Row['original_sha256']:
			raise RuntimeError('Archive decoded drift: ' + Row['path'])
		ArchiveCount += 1
Reviews = json.loads((Artifact / 'review-summary.json').read_text())['reviews']
if len(Reviews) != 5 or len({Row['reviewer_id'] for Row in Reviews}) != 5 or any(Row['verdict'] != 'APPROVED' for Row in Reviews):
	raise RuntimeError('Independent final reviews incomplete')
ReviewInputs = 0
for Review in Reviews:
	Name = Review['kind']
	RootFile = Out / (Name + '-root.json')
	Project = Path(json.loads(RootFile.read_text())['project']) if RootFile.exists() else Root
	PacketFile = Project / json.loads((Out / (Name + '-packet.json')).read_text())['packet']
	if sha(PacketFile) != Review['packet_sha256']:
		raise RuntimeError('Packet changed: ' + Name)
	for Input, Info in json.loads(PacketFile.read_text())['inputs'].items():
		if sha(Project / Input) != Info['sha256'] or sha(PacketFile.parent / Info['snapshot']) != Info['sha256']:
			raise RuntimeError('Review current/snapshot binding differs: ' + Name + ' ' + Input)
		ReviewInputs += 1
Software = Artifact / 'software-review2/inputs/scripts'
for Path in Software.iterdir():
	if Path.is_file() and sha(Root / 'scripts' / Path.name) != sha(Path):
		raise RuntimeError('Actual program differs from reviewed snapshot: ' + Path.name)
Library = json.loads((Out / 'library-verification.json').read_text())
if Library['status'] != 'PASS':
	raise RuntimeError('Library retrieval not verified')
Result = dict(status='PASS', scope='Current navigation, scopes, exact caller/source/archive/review identities and checkpoint. This is not an additional mathematical proof.', files=Rows, local_links_checked=Links, broken_links=Bad, caller_bindings=len(Inventory['entries']), archive_files_checked=ArchiveCount, review_packet_current_and_snapshot_inputs_checked=ReviewInputs, checkpoint=Checkpoint['sha256'], checkpoint_inputs=len(Snapshot['inputs']))
(Out / 'final-document-check.json').write_text(json.dumps(Result, ensure_ascii=False, indent=2) + '\n')
(Report / 'final-document-check.json').write_bytes((Out / 'final-document-check.json').read_bytes())
print('Final document/identity check PASS:', len(Rows), 'documents,', Links, 'links,', ArchiveCount, 'archive files', flush=True)
