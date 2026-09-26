from pathlib import Path
import gzip
import hashlib
import json

Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round12-20260926')
Rows = []

def copy(Source, Name):
	Data = Source.read_bytes()
	Row = dict(source=str(Source), path=Name, sha256=hashlib.sha256(Data).hexdigest(), bytes=len(Data))
	if len(Data) > 2000000:
		Row.update(original_path=Name, original_sha256=Row['sha256'], original_bytes=len(Data), encoding='gzip')
		Data = gzip.compress(Data, mtime=0)
		Row.update(path=Name + '.gz', sha256=hashlib.sha256(Data).hexdigest(), bytes=len(Data))
	Target = Artifact / Row['path']
	Target.parent.mkdir(parents=True, exist_ok=True)
	if Target.exists() and Target.read_bytes() != Data:
		raise RuntimeError('Immutable evidence drift: ' + Name)
	Target.write_bytes(Data)
	Rows.append(Row)

for Name in ['check-normal.json', 'check-normal.err', 'check-optimized.json', 'check-optimized.err', 'check2-normal.json', 'check2-normal.err', 'check2-optimized.json', 'check2-optimized.err']:
	copy(Out / Name, 'coordinator-checks/' + Name)
copy(Out / 'check_repair.py', 'coordinator-checks/check_repair.py')
for Source in sorted((Out / 'repaired-runs').rglob('*')):
	if Source.is_file() and '__pycache__' not in Source.parts:
		copy(Source, 'coordinator-runs/' + Source.relative_to(Out / 'repaired-runs').as_posix())
for Name in ['analytic-author', 'formal-author', 'software-review', 'software-review2', 'formal-readback', 'formal-readback2', 'formal-comparison', 'math-review', 'renewal-review']:
	for Suffix in ['spec', 'packet', 'root', 'spawn', 'dispatch', 'completion', 'received', 'verified', 'close', 'input1', 'input2', 'input3']:
		Source = Out / (Name + '-' + Suffix + '.json')
		if Source.is_file():
			copy(Source, 'native-transcripts/' + Source.name)
for Source in sorted(Out.glob('*-requirements.json')):
	copy(Source, 'correction-requirements/' + Source.name)
for Name in ['authors-wait1.json', 'authors-wait2.json', 'formal-author-completion-attempt.json', 'blind2-prepare-failure.json']:
	if (Out / Name).is_file():
		copy(Out / Name, 'native-transcripts/' + Name)
for Name in ['cards.json', 'revisions.json', 'current-revisions.json', 'renewals.json', 'renewal-inspection.json', 'annotations.json', 'annotated-cards.json', 'obligations-inspection.json', 'remote-preflight2.json', 'formal-execution-identity-check.json', 'review-inputs-midflight-check.json', 'progress-initial.json', 'progress-review-stage.json']:
	copy(Out / Name, 'integration/' + Name)
for Source in sorted(Out.glob('*.py')):
	copy(Source, 'integration/coordinator/' + Source.name)
for Name in ['AGENTS.md', 'REPORT.template.md', 'ARTIFACT_README.template.md', 'formal-details.md']:
	copy(Out / Name, 'integration/coordinator/' + Name)
(Artifact / 'coordinator-archive-manifest.json').write_text(json.dumps(dict(files=Rows, scope='Coordinator evidence, actual native tool envelopes and exact helper sources. These are not substitutes for independent mathematical reviews. Historical failed snapshots remain separate. Publication and final remote IDs are external to avoid a self-referential hash.'), ensure_ascii=False, indent=2) + '\n')
print('Archived coordinator evidence', len(Rows), 'files', flush=True)
