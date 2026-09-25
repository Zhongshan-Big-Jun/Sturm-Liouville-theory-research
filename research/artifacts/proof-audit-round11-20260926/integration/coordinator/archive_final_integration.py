from pathlib import Path
import json, hashlib

O = Path('/mnt/f/tools/math-audit-round11-20260926')
R = Path('/mnt/f/LaTeX/BVE research')
A = R / 'research/artifacts/proof-audit-round11-20260926'
V = json.loads((O / 'library-verification.json').read_text())
if V['status'] != 'PASS':
    raise RuntimeError('Final retrieval has not passed')
Stages = [json.loads(s) for s in (O / 'final-library-pipeline.jsonl').read_text().splitlines()]
if [s['name'] for s in Stages] != ['release-current-final', 'index-library', 'query-library'] or any(s['exit_code'] != 0 for s in Stages):
    raise RuntimeError('Pipeline needs reconciliation before archiving')

Files = [
    'current-release-results.json', 'index-result.json', 'retrieval-result.json',
    'library-verification.json', 'release-current-final.log', 'index-library.log',
    'query-library.log', 'final-library-pipeline.jsonl', 'final-library-pipeline.log',
    'native-operations.jsonl', 'progress-result.json', 'checkpoint-result.json',
    'remote-preflight.json', 'continuity-lock-cleanup.json',
]
Scripts = [
    'run_native_posix.py', 'review_ops.py', 'final_library_pipeline.py',
    'release_current_final.py', 'index_library.py', 'query_library.py',
    'finish_documents.py', 'finish_checkpoint.py', 'final_document_check.py',
    'publication.py', 'archive_final_integration.py', 'clean_continuity_lock.py',
]
Rows = []
def copy(name, relative):
    source, target = O / name, A / relative
    raw = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_bytes() != raw:
        raise RuntimeError('Refusing to overwrite differing archived evidence ' + str(target))
    target.write_bytes(raw)
    Rows.append(dict(source=name, path=relative, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw)))

for name in Files:
    copy(name, 'integration/' + name)
for name in Scripts:
    copy(name, 'integration/coordinator/' + name)
copy('formal-readback-first-dispatch-failure.json', 'integration/coordinator-failures/formal-readback-first-dispatch-failure.json')
Manifest = dict(
    schema='round11-final-integration-archive/v1', files=Rows,
    scope='Exact coordinator API, retrieval, continuity and publication-preparation records. These are not independent mathematical reviews. Public reproduction helpers retain the original absolute paths; run outside the repository and use the original plugin modules. The actual final commit and remote readback are stored externally to avoid a self-referential commit hash.'
)
(A / 'integration/archive-manifest.json').write_text(json.dumps(Manifest, ensure_ascii=False, indent=2) + '\n')
print('Final integration archive saved', len(Rows), 'exact files', flush=True)
