from pathlib import Path
import collections
import datetime
import hashlib
import json

OUT = Path('/mnt/f/tools/math-audit-round4-20260921/lean-author')
PROJECT = Path('/mnt/f/LaTeX/BVE research/lean-proof')
ROOT = OUT / 'final/build/SL/AuditRound4.olean'
SOURCE = PROJECT / 'SL/AuditRound4.lean'


def digest(PathValue):
	with Path(PathValue).open('rb') as Handle:
		return hashlib.file_digest(Handle, 'sha256').hexdigest()


def save(Name, Value):
	(OUT / Name).write_text(json.dumps(Value, ensure_ascii=False, indent=2) + '\n')


def item(PathValue):
	PathValue = Path(PathValue)
	return {'path': str(PathValue), 'sha256': digest(PathValue), 'bytes': PathValue.stat().st_size}


Baseline = json.loads((OUT / 'source-baseline.json').read_text())
Comparison = [{'path': P, 'before': Hash, 'after': digest(P), 'unchanged': digest(P) == Hash}
	for P, Hash in Baseline.items()]
assert all(R['unchanged'] for R in Comparison)
save('protected-source-comparison.json', {'count': len(Comparison), 'all_byte_identical': True, 'files': Comparison})
assert SOURCE.read_bytes() == (OUT / 'final/AuditRound4.lean').read_bytes()
assert '--' not in SOURCE.read_text() and '/-' not in SOURCE.read_text()
assert digest(ROOT) == digest(OUT / 'replay/build/SL/AuditRound4.olean')
RootHash = digest(ROOT)

DeclarationData = json.loads((OUT / 'final/declarations.json').read_text())
Declarations = DeclarationData['declarations']
Nodes = {N['name']: N for N in DeclarationData['dependencies']}
assert not any(N.get('missing') or N.get('unsafe') for N in Nodes.values())
Closures = []
for Declaration in Declarations:
	Stack = [Declaration['declaration']]
	Seen = set()
	while Stack:
		Name = Stack.pop()
		if Name in Seen:
			continue
		Seen.add(Name)
		assert Name in Nodes
		Node = Nodes[Name]
		Stack += Node['type_dependencies'] + Node['body_dependencies']
	assert Seen == set(Declaration['transitive_dependencies'])
	Axioms = {N for N in Seen if Nodes[N]['kind'] == 'axiom'}
	assert Axioms == set(Declaration['transitive_axioms'])
	assert Axioms <= {'propext', 'Classical.choice', 'Quot.sound'}
	Closures.append({'declaration': Declaration['declaration'], 'closure_nodes': len(Seen),
		'axioms': sorted(Axioms), 'graph_matches_Lean': True})
save('closure-consistency.json', {'declarations': Closures, 'all_match': True})

Loaded = json.loads((OUT / 'final/loaded-modules.json').read_text())
Modules = json.loads((OUT / 'final/module-artifact-hashes.json').read_text())
assert Loaded['module_count'] == len(Loaded['modules']) == Modules['module_count'] == len(Modules['modules'])
assert {M['module'] for M in Loaded['modules']} == {M['module'] for M in Modules['modules']}
assert len({M['module'] for M in Loaded['modules']}) == Loaded['module_count']
ActualRoot = [M for M in Modules['modules'] if M['module'] == 'SL.AuditRound4']
assert len(ActualRoot) == 1 and ActualRoot[0]['resolved_olean'] == str(ROOT)
assert ActualRoot[0]['artifacts'][0]['sha256'] == RootHash
for Module in Modules['modules']:
	for Artifact in Module['artifacts']:
		Stat = Path(Artifact['path']).stat()
		assert (Stat.st_size, Stat.st_mtime_ns, Stat.st_ctime_ns) == (
			Artifact['bytes'], Artifact['mtime_ns'], Artifact['ctime_ns']), Artifact['path']

Environment = json.loads((OUT / 'environment.json').read_text())
for File in Environment['runtime_files'] + Environment['configuration']:
	assert digest(File['path']) == File['sha256']
Adaptation = json.loads((OUT / 'DEPENDENCY_ADAPTATION.json').read_text())
for File in Adaptation['files']:
	assert digest(File['original']) == File['original_sha256']
	assert digest(File['copy']) == File['copy_sha256']
	assert File['body_after_first_import_byte_identical']
	assert Path(File['copy']).read_bytes().split((Adaptation['replacement_header']+'\n').encode(), 1)[1] == Path(File['original']).read_bytes().split(b'import Mathlib\n', 1)[1]

Expected = {
	'09-inspect-root': 0, '10-positive-controls': 0, '11-wrong-reduction': 1,
	'12-perturbed-table': 1, '13-input-contract-check': 1,
	'14-fresh-root-replay': 0, '15-resolve-inspection-imports': 0, '16-contract-normalization': 0,
}
Bindings = []
for Name, Code in Expected.items():
	Record = json.loads((OUT / 'logs' / (Name + '.json')).read_text())
	assert Record['exit_code'] == Code
	assert Record['local_objects_before'][str(ROOT)] == RootHash
	assert Record['local_objects_after'][str(ROOT)] == RootHash
	assert Record['source_unchanged_during_run']
	assert Record['source_sha256_before'][str(SOURCE)] == digest(SOURCE)
	Stdout = OUT / 'logs' / (Name + '.stdout.txt')
	Stderr = OUT / 'logs' / (Name + '.stderr.txt')
	assert digest(Stdout) == Record['stdout_sha256']
	assert digest(Stderr) == Record['stderr_sha256']
	if Name in ['11-wrong-reduction', '12-perturbed-table']:
		assert '⊢ False' in Stdout.read_text()
		assert 'CONTROL_ROOT=F:\\tools\\math-audit-round4-20260921\\lean-author\\final\\build\\SL\\AuditRound4.olean' in Stdout.read_text()
	Bindings.append({'execution': Name, 'exit_code': Code, 'root_before_sha256': RootHash,
		'root_after_sha256': RootHash, 'source_before_after_sha256': digest(SOURCE),
		'receipt': item(OUT / 'logs' / (Name + '.json'))})
save('root-object-bindings.json', {'actual_root': item(ROOT), 'bindings': Bindings})

Logs = []
for P in sorted((OUT / 'logs').glob('*.json')):
	Record = json.loads(P.read_text())
	if 'argv' in Record:
		Logs.append({'name': P.stem, 'exit_code': Record.get('exit_code'),
			'duration_seconds': Record.get('duration_seconds'), 'record': item(P)})
save('command-index.json', Logs)

ReadbackFiles = [OUT / 'final' / N for N in ['AuditRound4.lean', 'declarations.json',
	'formal-statements.txt', 'formal-statements-fully-explicit.txt', 'local-definition-closure.txt']]
save('final/READBACK_INPUTS.json', {'kind': 'actual_object_exports_without_intent_comments',
	'root_source': item(SOURCE), 'actual_imported_root': item(ROOT),
	'files': [item(P) for P in ReadbackFiles], 'review_status': 'not_performed_by_author'})
SemanticFiles = ReadbackFiles + [OUT / N for N in ['CONTRACT.md', 'ContractChecks.lean',
	'source-snapshot/proof_audit_round4_20260920.md', 'source-snapshot/constructive_repairs.md',
	'final/loaded-modules.json', 'final/module-artifact-hashes.json', 'environment.json',
	'root-object-bindings.json', 'closure-consistency.json', 'DEPENDENCY_ADAPTATION.json',
	'negative-control-results.json', 'protected-source-comparison.json', 'command-index.json']]
save('SEMANTIC_REVIEW_INPUTS.json', {'kind': 'author_scope_for_separate_semantic_review',
	'files': [item(P) for P in SemanticFiles], 'review_status': 'not_performed_by_author'})

Summary = {
	'schema': 'audit-round4-author-evidence-v1',
	'generated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
	'status': 'AUTHOR_CHECKS_COMPLETE_PENDING_INDEPENDENT_REVIEW',
	'new_project_source': item(SOURCE), 'inspected_root': item(ROOT),
	'fresh_replay_object': item(OUT / 'replay/build/SL/AuditRound4.olean'),
	'declarations': dict(collections.Counter(D['kind'] for D in Declarations)),
	'transitive_dependency_nodes': len(Nodes),
	'transitive_axioms_union': sorted({A for D in Declarations for A in D['transitive_axioms']}),
	'unsafe_or_missing_dependency_nodes': [],
	'loaded_modules': Loaded['module_count'], 'hashed_module_artifacts': Modules['artifact_count'],
	'hashed_module_bytes': Modules['bytes'],
	'all_module_metadata_unchanged_since_full_hashing': True,
	'positive_controls_passed': True, 'negative_controls_rejected_false_goals': 2,
	'input_contract_check_passed': True, 'fresh_replay_byte_identical': True,
	'protected_lean_sources_unchanged': len(Comparison),
	'original_local_dependencies_import_restricted_in_external_copies': True,
	'whole_lake_build': False, 'downloaded_dependencies': False,
	'author_semantic_acceptance': False, 'independent_review': 'not_performed',
	'canonical_changes': False, 'git_mutations': False,
	'remaining_linter_warning': 'One non-semantic unnecessarySeqFocus warning at root line 473.',
	'failed_attempts_preserved': ['Broad import cancellation (02)', 'Missing not-yet-built local object (03)',
		'Initial elaboration/algebra errors (05)', 'One inverse-conjugacy proof error (06)',
		'Input-contract simplification mismatch (13, fixed in 16)',
		'Inline diagnostic axiom-list ordering mistake (diagnostic-failure-record.json)',
		'Two intentional failed negative controls (11,12)'],
	'exclusions_document': str(OUT / 'CONTRACT.md'),
}
save('FINAL_CHECKS.json', Summary)

Report = '''# Fourth-round scoped Lean author delivery

41 theorems and 23 definitions compiled with native Lean 4.31.0. The actual imported root object was inspected; all 64 declaration closures were exported and independently recomputed from the dependency graph. The union of axioms is {propext, Classical.choice, Quot.sound}; no missing/unsafe node or sorryAx occurs in the inspected closure.

- Source: `/mnt/f/LaTeX/BVE research/lean-proof/SL/AuditRound4.lean`.
- Exact scope and exclusions: `CONTRACT.md`.
- Compiler/run summaries: `FINAL_CHECKS.json`, `command-index.json`, and unabridged `logs/`.
- Actual declarations and definitions: `final/declarations.json`, `final/formal-statements*.txt`, `final/local-definition-closure.txt`.
- Root identity before/after inspection and controls: `root-object-bindings.json`.
- Loaded environment: `environment.json`, `final/loaded-modules.json`, `final/module-artifact-hashes.json`.
- Blind readback entry: `final/READBACK_INPUTS.json`.
- Separate semantic review entry: `SEMANTIC_REVIEW_INPUTS.json`.
- Parallel-author coordination: `COORDINATION.md`.

Both intentional negative controls fail at False, while paired positive controls pass. The hand-written input contracts pass after recorded simplification repairs. Fresh compilation into a second external directory produces identical root bytes. All 44 prior project Lean sources remain byte-identical.

The original broad Mathlib import was cancelled. Four external source copies change only that import header and were freshly compiled; their mathematical bodies are byte-identical to the original files. The exact adapted-source/module provenance is disclosed in DEPENDENCY_ADAPTATION.json. No old project build object is on LEAN_PATH. All 3217 actually loaded modules and 12853 available artifact files are hash-pinned. No whole Lake build or download ran.

All failed source attempts, full Lean execution records, and the cancelled import are retained. One harmless linter warning remains; it does not affect theorem closure. The separate inline Python ordering diagnostic failure is recorded explicitly and the corrected set-based graph check passes.

This is author evidence ready for review, not independent acceptance. Concrete parity/moment results are rational-valued. General difference and reduction theorems are field-polymorphic. Sobolev/quotient convergence, analytic tail series and asymptotics, minimality, K(c), and all-degree rational classification are excluded. No docs, cards, statuses, AGENTS.md, canonical data, plugins, or git state were modified by this author.
'''
(OUT / 'REPORT.md').write_text(Report)
Files = sorted(P for P in OUT.rglob('*') if P.is_file() and P.name not in ['FILE_HASHES.sha256', 'FREEZE.json'])
(OUT / 'FILE_HASHES.sha256').write_text(''.join(digest(P) + '  ' + str(P.relative_to(OUT)) + '\n' for P in Files))
save('FREEZE.json', {'frozen_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
	'file_inventory': item(OUT / 'FILE_HASHES.sha256'), 'file_count': len(Files),
	'root_source': item(SOURCE), 'actual_imported_root': item(ROOT),
	'contract': item(OUT / 'CONTRACT.md'), 'status': Summary['status']})
print(json.dumps({K: Summary[K] for K in ['status', 'declarations', 'loaded_modules',
	'hashed_module_artifacts', 'protected_lean_sources_unchanged', 'fresh_replay_byte_identical']}, indent=2))
print('Frozen evidence files:', len(Files))
