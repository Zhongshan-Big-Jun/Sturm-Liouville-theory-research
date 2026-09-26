from pathlib import Path
import hashlib
import json

Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Artifact = Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round12-20260926')
Verified = json.loads((Out / 'library-verification.json').read_text())
if Verified['status'] != 'PASS':
	raise RuntimeError('Library retrieval not complete')
Stages = [json.loads(Line) for Line in (Out / 'final-library-pipeline.jsonl').read_text().splitlines()]
if [Row['name'] for Row in Stages] != ['release-current-final', 'annotate-cards', 'index-library', 'query-library'] or any(Row['exit_code'] != 0 for Row in Stages):
	raise RuntimeError('Pipeline requires saved-result reconciliation')
Names = ['current-release-results.json', 'index-result.json', 'retrieval-result.json', 'library-verification.json', 'release-current-final.log', 'annotate-cards.log', 'index-library.log', 'query-library.log', 'final-library-pipeline.jsonl', 'final-library-pipeline.log', 'native-operations.jsonl', 'progress-result.json', 'checkpoint-result.json', 'checkpoint-files.json', 'continuity-lock-cleanup.json', 'coordinator-helper-syntax.json']
Rows = []
for Name in Names:
	Source, Target = Out / Name, Artifact / 'integration' / Name
	Data = Source.read_bytes()
	Target.parent.mkdir(parents=True, exist_ok=True)
	if Target.exists() and Target.read_bytes() != Data:
		raise RuntimeError('Integration archive drift: ' + Name)
	Target.write_bytes(Data)
	Rows.append(dict(source=Name, path='integration/' + Name, sha256=hashlib.sha256(Data).hexdigest(), bytes=len(Data)))
(Artifact / 'integration/archive-manifest.json').write_text(json.dumps(dict(schema='round12-final-integration/v1', files=Rows, scope='Actual original-API release/annotation/index/query and continuity records. Final commit and remote readback are external to avoid a self-referential commit hash.'), ensure_ascii=False, indent=2) + '\n')
print('Final integration archive:', len(Rows), 'files', flush=True)
