"""Assemble author receipts and verify the final input-only freeze after execution."""
from pathlib import Path
import datetime, hashlib, json, tarfile

base = Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(rel):
    return json.loads((base / rel).read_text())

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

before = read('evidence/before/input-hashes.json')['files']
freeze = read('evidence/freeze-receipt.json')
actual = {p.relative_to(base / 'final-inputs').as_posix(): digest(p)
          for p in (base / 'final-inputs').rglob('*') if p.is_file()}
require(actual == freeze['freeze_sha256'], 'final freeze changed or gained files')
require(digest(base / 'final-inputs.tar') == freeze['archive_sha256'], 'archive changed')
require('inputs/tools-AGENTS.md' not in actual, 'private context unexpectedly included')
with tarfile.open(base / 'final-inputs.tar', 'r') as archive:
    require(sorted(archive.getnames()) == sorted(actual), 'archive input inventory differs')
    for member in archive:
        require(member.isfile(), 'non-file archive member')
        require(hashlib.sha256(archive.extractfile(member).read()).hexdigest() == actual[member.name],
                'archive member mismatch: ' + member.name)
review = read('prior-review.json')
require(review['verdict'] == 'CHANGES_REQUIRED', 'prior rejection modified')
require(digest(base / 'prior-review.json') == before['prior-review.json']['sha256'], 'prior review bytes changed')
for rel in before:
    if rel.startswith(('originals/', 'candidates/', 'inputs/')) or rel in (
            'regression/backend_probe.py', 'regression/capture_run.py', 'regression/verify_package.py'):
        require(digest(base / rel) == before[rel]['sha256'], 'unrelated supplied input changed: ' + rel)
        require(digest(base / 'final-inputs' / rel) == before[rel]['sha256'], 'frozen preservation failure: ' + rel)
executions = []
summaries = {}
expected_status = {1: 1, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0}
for directory in sorted((base / 'evidence/executions').iterdir()):
    receipt = json.loads((directory / 'receipt.json').read_text())
    number = int(directory.name[:2])
    require(receipt['exit_code'] == expected_status[number], 'unexpected execution status: ' + directory.name)
    require(receipt['inputs_unchanged'], 'execution inputs changed: ' + directory.name)
    for name, sha in receipt['streams'].items():
        require(digest(directory / name) == sha, 'raw stream changed')
    item = dict(name=directory.name, receipt=str((directory / 'receipt.json').relative_to(base)),
                receipt_sha256=digest(directory / 'receipt.json'), argv=receipt['argv'],
                cwd=receipt['cwd'], pid=receipt['pid'], exit_code=receipt['exit_code'],
                seconds=receipt['seconds'], inputs_unchanged=True)
    stdout = (directory / 'stdout.txt').read_text()
    lines = [line for line in stdout.splitlines() if line.startswith('AUTHOR REPLAY ')]
    if lines:
        path = Path(lines[-1].split(' ', 3)[3]).resolve()
        require(path.is_relative_to(base), 'summary path outside author directory')
        summary = json.loads(path.read_text())
        summaries[number] = summary
        item.update(replay_summary=str(path.relative_to(base)), replay_summary_sha256=digest(path),
                    child_processes=len(summary['runs']), accepted_child_cases=sum(r['accepted'] for r in summary['runs']))
        require(summary['inputs_unchanged'], 'replay source changed')
        for rel, sha in summary['output_sha256'].items():
            require(digest(path.parent / rel) == sha, 'replay output changed: ' + rel)
    executions.append(item)
require(len(executions) == 6, 'execution inventory incomplete')
for number in (3, 6):
    summary = summaries[number]
    require(summary['accepted'] and len(summary['runs']) == 14, 'required replay did not pass')
    require(all(r['accepted'] for r in summary['runs']), 'required child case failed')
    require(all(r['exit_code'] == 86 for r in summary['runs'] if r['name'].endswith(('-outside', '-missing'))),
            'negative control not refused')
require(summaries[6]['optimize'] == 1, 'portable parent was not optimized')
mutant = summaries[4]
outside = [r for r in mutant['runs'] if r['name'].endswith('-outside')]
missing = [r for r in mutant['runs'] if r['name'].endswith('-missing')]
require(not mutant['accepted'] and len(outside) == len(missing) == 4, 'mutation inventory invalid')
require(all(r['exit_code'] == 0 and not r['accepted'] for r in outside), 'old filter did not fail the outside tests')
require(all(r['exit_code'] == 86 and r['accepted'] for r in missing), 'missing checks altered by filter-only mutation')
mutation = read('evidence/final-filter-only-mutation-description.json')
require(mutation['original_sha256'] == actual['regression/provenance.py'], 'mutation not bound to final helper')
for path in (base / 'final-inputs/regression').glob('*.py'):
    if path.name != 'provenance.py':
        require(digest(path) == digest(base / 'evidence/final-filter-only-mutation/regression' / path.name),
                'mutation harness differs beyond declared filter')
final_run = Path(summaries[6]['root'])
observations = {}
for name in ('candidates-normal', 'candidates-optimized', 'op03-cli-normal', 'op03-cli-optimized'):
    data = json.loads((final_run / 'results' / (name + '.json')).read_text())
    gate = data.get('provenance', data)
    categories = {}
    for item in gate['modules'].values():
        categories[item['category']] = categories.get(item['category'], 0) + 1
    require(categories.get('standard-library', 0) > 0 and categories.get('installed-package', 0) > 0,
            'unfiltered runtime provenance absent')
    observations[name] = dict(file_backed_modules=len(gate['module_files']), required_bindings=len(gate['required']),
                              categories=categories, accepted=gate['accepted'])
summary = dict(schema='r7-software-author-v2-evidence-v1', created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    role='bounded software repair author, not independent reviewer', status='AUTHOR_BOUNDED_CHECKS_PASSED',
    prior_review_verdict='CHANGES_REQUIRED', independent_review='Pending; a new agent must review the final freeze',
    scope='Observed file-backed runtime module provenance and replay acceptance only; no OS sandbox or malicious sys.modules evasion guarantee',
    supplied_ten_candidates_and_eight_dependencies_unchanged=True, original_tree_unchanged=True,
    source_integrity='evidence/source-integrity.json', source_integrity_sha256=digest(base / 'evidence/source-integrity.json'),
    final_freeze=dict(directory='final-inputs', archive='final-inputs.tar', files=len(actual), manifest_sha256=freeze['manifest_sha256'],
                      archive_sha256=freeze['archive_sha256'], unchanged_after_execution=True, input_only=True),
    package_verifier='Unchanged regression/verify_package.py, now runnable with supplied manifest.json and manifest.sha256; execution 05 exit 0',
    executions=executions, final_clean_observations=observations,
    negative_controls=dict(repaired='Eight real outside/missing controls per replay refused with exit 86 in normal and -O numerical/CLI processes',
                           filter_only_mutant='Four real outside children incorrectly exit 0; unchanged suite fails with exit 1; four missing controls still refuse'),
    first_failures_retained=dict(v2='Execution 01 and its full fresh run retained, exit 1 due to three site startup hooks; corrected with controlled -S startup',
        mutation='Both executions 02 and 04 retained with expected suite exit 1',
        earlier='Unchanged supplied prior-review.json and evidence/before/README.md retain older failure records; raw older directories were not supplied or accessed'),
    omitted_private_context='inputs/tools-AGENTS.md deliberately not supplied; unrelated non-executable private workspace context; historical source-manifest references retained',
    extra_mathematical_scans=False, memory_used=False, main_tree_or_other_author_directories_accessed=False)
(base / 'evidence/author-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
(base / 'evidence/AGENTS.md').write_text('''# Author evidence maintenance

Only append new execution directories and retain earlier failed raw streams, source copies, receipts and immutable inputs. This directory contains author evidence, not independent approval. Tools here read only this author-v2 delivery and the permitted installed runtime.

2026-09-21 completion record: six actual outer executions retained. Execution 01 failed due to startup hooks; 02 and 04 are intentionally failing old-filter-only control suites; 03 repaired replay passed; 05 supplied package verifier passed; 06 optimized portable replay of the final freeze passed all fourteen normal/-O child cases. All 36 supplied original/candidate files and the independent rejection remain unchanged. Rehashed all replay output receipts and checked the archive inventory/member digests against the unchanged 52-file input-only freeze. Final independent review remains pending. Full details: author-summary.json.
''')
# A receipt index binds all retained artifacts without trying to hash itself.
paths = [p for root in ('evidence', 'work') for p in (base / root).rglob('*')
         if p.is_file() and p != base / 'evidence/artifact-hashes.json']
paths += [base / 'final-inputs.tar', base / 'final-inputs.tar.sha256']
(base / 'evidence/artifact-hashes.json').write_text(json.dumps({p.relative_to(base).as_posix():digest(p) for p in sorted(paths)},indent=2)+'\n')
print(json.dumps(dict(status=summary['status'], freeze_files=len(actual), executions=len(executions), final_clean_observations=observations,
                      manifest_sha256=freeze['manifest_sha256'], archive_sha256=freeze['archive_sha256']),indent=2))
