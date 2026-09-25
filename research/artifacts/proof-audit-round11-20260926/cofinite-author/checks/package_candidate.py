#!/usr/bin/env python3
"""Build a hash-bound candidate card and an author delivery summary, not an acceptance."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json
import re

Root = Path('/mnt/f/tools/math-audit-round11-20260926/cofinite-author')
Status = 'CANDIDATE_PENDING_INDEPENDENT_REVIEW'


def digest(FilePath):
	return hashlib.sha256(FilePath.read_bytes()).hexdigest()


def artifact(RelativePath):
	FilePath = Root / RelativePath
	return {'path': str(FilePath), 'relative_path': RelativePath,
		'sha256': digest(FilePath), 'size_bytes': FilePath.stat().st_size}


def write_json(RelativePath, Data):
	(Root / RelativePath).write_text(json.dumps(Data, ensure_ascii=False, indent=2) + '\n')


Bindings = json.loads((Root / 'source-bindings.json').read_text())
ProofPath = Root / 'cofinite-all-orders.md'
ProofText = ProofPath.read_text()
ProofLines = ProofText.splitlines()
ExecutionFiles = sorted((Root / 'logs').glob('algebra-*.execution.json'))
if not ExecutionFiles:
	raise RuntimeError('No actual exact algebra execution record')
ExecutionPath = ExecutionFiles[-1]
Execution = json.loads(ExecutionPath.read_text())
AlgebraPath = Path(Execution['stdout']['path'])
Algebra = json.loads(AlgebraPath.read_text())
if Execution['returncode'] != 0:
	raise RuntimeError('Exact algebra process failed')
ProofSources = [{'path': str(ProofPath), 'sha256': digest(ProofPath),
	'locator': 'Theorem 1 (1.5), sections 2-9; Corollary 3 in section 10',
	'kind': 'CURRENT_AUTHOR_PROOF_PENDING_INDEPENDENT_REVIEW'}]
for Source in Bindings['sources']:
	if Source['source_id'] in ['IN-SUBMITTED', 'P-FRAC', 'P-DICT', 'P-S3', 'P-PARITY']:
		ProofSources.append({'source_id': Source['source_id'], 'path': Source['original_path'],
			'sha256': Source['sha256'], 'frozen_copy': Source['frozen_copy'],
			'locators': Source['locators'],
			'kind': Source['role']})
ProofSteps = [
	{'id': 'OP', 'locator': '2.1-2.2, equations (2.1)-(2.9)',
		'claim': 'Actual positive self-adjoint Krein realization and exact D(Kc^2) with equivalent H4 Sobolev norm.'},
	{'id': 'MEMBERSHIP', 'locator': '3, equations (3.1)-(3.6)',
		'claim': 'Every original member is in Hc^s for every 0<=s<7/2, with both parity branches and normalization handled.'},
	{'id': 'SPECTRAL_DENSITY', 'locator': '2.3, equation (2.11)',
		'claim': 'Hc^4 is dense in Hc^s by spectral cutoffs; no reliance on polynomial density.'},
	{'id': 'LOCAL_NORM', 'locator': '4.1-4.3, equations (4.2)-(4.9)',
		'claim': 'Direct quadratic K-functional interpolation gives fixed interior multiplier bounds in both directions, including critical orders through 7/2.'},
	{'id': 'HIGH_VANISHING_CORE', 'locator': '5, equations (5.2)-(5.11)',
		'claim': 'For each even L>=4, closure in Hc^4 of x^L C[x] intersect D(Kc^2) is the kernel of four centre traces.'},
	{'id': 'TAIL_ALGEBRA', 'locator': '6, equations (6.1)-(6.2)',
		'claim': 'Every complete retained high tail equals compatible polynomials divisible by x^(2m0-2), by finite leading-term elimination for every degree.'},
	{'id': 'DUAL_COMPRESSION', 'locator': '7, equation (7.1)',
		'claim': 'Any continuous functional annihilating a cofinite retained family restricts to a linear combination of four centre traces.'},
	{'id': 'CRITICAL_LINEAR_COMBINATIONS', 'locator': '8, equations (8.1)-(8.7)',
		'claim': 'The logarithmic Fourier sequence excludes every highest nonzero derivative coefficient when s<=r+1/2, including arbitrary complex linear combinations.'},
	{'id': 'COFINITE_CLOSURE', 'locator': '9, equations (9.1)-(9.2), and Theorem 1',
		'claim': 'Exact annihilator, closure, density criterion and complex codimension; equality points lie on the fewer-traces side.'},
]
Cases = [
	{'s_condition': '0 <= s <= 1/2', 'essential_indices': [], 'trace_derivative_orders': []},
	{'s_condition': '1/2 < s <= 3/2', 'essential_indices': [0], 'trace_derivative_orders': [0]},
	{'s_condition': '3/2 < s <= 5/2', 'essential_indices': [0, 1], 'trace_derivative_orders': [0, 1]},
	{'s_condition': '5/2 < s < 7/2', 'essential_indices': [0, 1, 4], 'trace_derivative_orders': [0, 1, 2]},
]
Card = {
	'candidate_id': 'round11-krein-cofinite-closure-all-orders',
	'id_scope': 'LOCAL_NEW_CARD_CANDIDATE_ONLY_NOT_A_REGISTERED_LIBRARY_ID',
	'status': Status, 'evidence_status': Status,
	'title': '原稀疏多项式族在全部 0<=s<7/2 Krein 幂域中的余有限闭包',
	'summary': '固定 c>0 的复 Krein 幂域中, 每个余有限保留集的闭包恰由遗漏且连续的中心迹刻画. 必须保留的指标依次为 {}, {0}, {0,1}, {0,1,4}; 三个等号点属于较少迹的一侧.',
	'conditions': [
		'For every fixed real c>0, use complex L2(-1,1), with inner product linear in its first argument.',
		'Kc f=-f_second+c f, D(Kc)={f in ordinary H2: f_prime(1)=f_prime(-1)=(f(1)-f(-1))/2}.',
		'Hc^s=D(Kc^(s/2)), with norm ||Kc^(s/2)f||_2; every real 0<=s<7/2 is included.',
		'D={0,1} union {4,5,...}; p0=1, p1=x, p_(2m)=x^(2m)-m/(m-1)x^(2m-2), p_(2m+1)=x^(2m+1)-m/(m-1)x^(2m-1), every integer m>=2.',
		'For every N subset D with D\\N finite. Spans consist of finite complex linear combinations.',
	],
	'scope': 'All and only cofinite retained subsets of the specified original family in the stated fixed-c complex power spaces.',
	'content': 'closure_Hc^s span_C{p_n:n in N}={f in Hc^s: tau_j(f)=0 for all j in I(s)\\N}, where tau_0=f(0), tau_1=f_prime(0), tau_4=f_second(0). The complex codimension is |I(s)\\N| and density is equivalent to I(s) subset N.',
	'trace_index_dictionary': {'0': 'f(0)', '1': 'f_prime(0)', '4': 'f_second(0)'},
	'cases': Cases,
	'critical_cases': [
		{'s': '1/2', 'essential_indices': [], 'forbidden_extra_condition': 'f(0)=0'},
		{'s': '3/2', 'essential_indices': [0], 'forbidden_extra_condition': 'f_prime(0)=0'},
		{'s': '5/2', 'essential_indices': [0, 1], 'forbidden_extra_condition': 'f_second(0)=0'},
	],
	'proof_steps': ProofSteps,
	'analytic_strengthening': 'Both directions of fixed interior multiplier control are proved from the L2 and H4 endpoints by an explicit quadratic K-functional computation. No closure/interpolation interchange and no unverified full-domain-dictionary dependence.',
	'corollary': 'Deleting only p6 leaves a dense family at every requested order. Hence the original family, under any nonzero termwise complex scaling and any bijective enumeration, is neither a Schauder basis nor a Riesz basis in that window.',
	'exclusions': ['c=0', 'uniform constants as c tends to zero', 's>=7/2 original nonaffine members',
		'arbitrary infinite deletions', 'arbitrary constraint-generated or projected families',
		'approximation rates', 'frame bounds', 'orthogonalized or otherwise reconstructed replacement systems'],
	'predecessor_relation': 'Extends the s=3 cofinite three-trace pattern as an author candidate. The old s3 proof and domain dictionary are unmodified inputs and are not overwritten or reaccepted.',
	'new_card_requested': True, 'replaces_existing_cards': [],
	'sources': ProofSources,
	'source_bindings': artifact('source-bindings.json'),
	'exact_author_evidence': {
		'script': artifact('checks/exact_algebra.py'),
		'execution_manifest': artifact(str(ExecutionPath.relative_to(Root))),
		'stdout': artifact(str(AlgebraPath.relative_to(Root))),
		'returncode': 0,
		'category_counts': Algebra['category_counts'],
		'certifies_infinite_dimensional_analysis': False,
	},
	'author_assessment': {'requested_scope_derivation': 'COMPLETE_CANDIDATE',
		'remaining_analytic_gaps_identified_by_author': [], 'scope_reduction_needed_by_author': False},
	'review': {'independent_review_performed': False, 'review_agent_started': False,
		'required': 'Fresh independent mathematical review by the coordinator under a separate task.',
		'priority_obligations': [Step['id'] for Step in ProofSteps]},
	'formalization': {'new_lean_files': 0, 'lean_verification_claim': False},
	'novelty_claim': False,
	'integration_status': 'PROPOSED_ONLY_NOT_CANONICAL_NOT_ACCEPTED',
}
write_json('card.json', Card)

Validation = {'role': 'AUTHOR_ARTIFACT_INTEGRITY_CHECK_NOT_MATHEMATICAL_ACCEPTANCE',
	'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
	'checks': [], 'warnings': []}


def record(Name, Passed, Evidence):
	Validation['checks'].append({'name': Name, 'passed': bool(Passed), 'evidence': Evidence})
	if not Passed:
		raise RuntimeError(Name)


record('proof status is first line', ProofLines[0] == Status, ProofLines[0])
record('card status and independent-review boundary',
	Card['status'] == Status and not Card['review']['independent_review_performed'],
	{'status': Card['status'], 'review_performed': Card['review']['independent_review_performed']})
record('exact-check returncode', Execution['returncode'] == 0, Execution['returncode'])
record('exact-check script identity',
	digest(Root / 'checks/exact_algebra.py') == Execution['script_sha256'], Execution['script_sha256'])
for Kind in ['stdout', 'stderr']:
	record('exact-check ' + Kind + ' identity',
		digest(Path(Execution[Kind]['path'])) == Execution[Kind]['sha256'], Execution[Kind])
record('actual exact-check counts', len(Algebra['checks']) == Algebra['total_checks']
	and Counter(Check['category'] for Check in Algebra['checks']) == Counter(Algebra['category_counts'])
	and all(Check['passed'] for Check in Algebra['checks']),
	{'total': Algebra['total_checks'], 'categories': Algebra['category_counts']})
for Source in Bindings['sources']:
	record('frozen source identity ' + Source['source_id'],
		digest(Path(Source['frozen_copy'])) == Source['sha256'], Source['frozen_copy'])
	CurrentHash = digest(Path(Source['original_path']))
	record('read source remained identical ' + Source['source_id'],
		CurrentHash == Source['sha256'], {'path': Source['original_path'], 'sha256': CurrentHash})
	Lines = Path(Source['frozen_copy']).read_text(encoding='utf-8-sig').splitlines()
	record('source locator range ' + Source['source_id'],
		all(1 <= Locator['line_start'] <= Locator['line_end'] <= len(Lines)
			for Locator in Source['locators']), Source['locators'])
Tags = re.findall(r'\\tag\{([^}]+)\}', ProofText)
record('proof equation tags are unique', len(Tags) == len(set(Tags)), len(Tags))
for Section in range(1, 12):
	record('proof section ' + str(Section), bool(re.search(r'^## ' + str(Section) + r'\. ', ProofText, re.M)), Section)
record('display delimiters balanced', ProofText.count(r'\[') == ProofText.count(r'\]'),
	{'open': ProofText.count(r'\['), 'close': ProofText.count(r'\]')})
record('English punctuation in Chinese proof',
	not any(Character in ProofText for Character in '，。；：！？（）【】“”‘’、'), 'No listed fullwidth Chinese punctuation')
record('card proof SHA matches delivered proof', Card['sources'][0]['sha256'] == digest(ProofPath), digest(ProofPath))
record('source bindings SHA matches card', Card['source_bindings']['sha256'] == digest(Root / 'source-bindings.json'),
	digest(Root / 'source-bindings.json'))
External = Bindings['external_primary_source']
record('external raw source identity', digest(Path(External['raw_path'])) == External['raw_sha256'], External['raw_path'])
record('external targeted excerpt identity',
	digest(Path(External['excerpt_path'])) == External['excerpt_sha256'], External['excerpt_path'])
record('actual theorem and equation locators', all(Needle in Path(External['excerpt_path']).read_text()
	for Needle in ['id="A1.Thmtheorem3"', 'id="A1.E15"', 'id="A1.E16"']), External['verified_anchor'])
OutputFiles = [PathToCheck for PathToCheck in Root.rglob('*') if PathToCheck.is_file()]
record('all delivered paths resolve under authorized root',
	all(PathToCheck.resolve().is_relative_to(Root.resolve()) for PathToCheck in OutputFiles),
	{'root': str(Root), 'file_count_before_summary': len(OutputFiles)})
Validation['limitations'] = [
	'These checks establish artifact identities, actual local execution and document structure, not independent proof acceptance.',
	'Read-input hashes are compared. This is not a fresh full-repository byte audit of concurrent coordinator work.',
]
Validation['status'] = 'AUTHOR_ARTIFACT_INTEGRITY_PASSED'
write_json('logs/delivery-validation.json', Validation)

Now = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (Root / 'SESSION_LOG.md').open('a') as File:
	File.write('\n## Batch 4: candidate card and final delivery\n\n'
		'Packaged card.json with the full theorem contract, critical cases, proof obligations, source hashes, exact algebra evidence and explicit pending-review status. Validated all 8 frozen/read-source hashes, theorem source locators, proof equation tags, display delimiters and English punctuation. The main mathematical sources remain byte-identical to this author intake. These integrity checks do not constitute a full-repository audit or independent mathematical review. All outputs are in the authorized author directory. No commit/push, plugin edits, canonical writes or acceptance agent were performed. summary.json is the final machine-readable handoff.\n')
with (Root / 'AGENTS.md').open('a') as File:
	File.write('\n2026-09-26: Completed the candidate card, source bindings, 94-check author execution record and artifact integrity checks. The complete theorem remains CANDIDATE_PENDING_INDEPENDENT_REVIEW. Handoff entry: summary.json; detailed method and dialogue: SESSION_LOG.md.\n')
Artifacts = {}
for RelativePath in ['cofinite-all-orders.md', 'card.json', 'source-bindings.json', 'checks/exact_algebra.py',
	'checks/run_self_check.py', 'checks/capture_sources.py', 'checks/package_candidate.py',
	'logs/delivery-validation.json', 'AGENTS.md', 'SESSION_LOG.md']:
	Artifacts[RelativePath] = artifact(RelativePath)
Summary = {
	'status': Status, 'role': 'ROUND11_ANALYTIC_AUTHOR_NOT_INDEPENDENT_REVIEWER',
	'completed_at_utc': Now, 'output_root': str(Root),
	'result': 'Complete author candidate for every fixed c>0, complex Krein power spaces, every 0<=s<7/2 and every cofinite retained subset of the original family.',
	'formula': Card['content'], 'essential_index_cases': Cases,
	'critical_values_included': ['1/2', '3/2', '5/2'],
	'author_mathematical_assessment': Card['author_assessment'],
	'key_repairs_and_expansions': [
		'High-vanishing H4 polynomial core using the shrinking local fourth-derivative norm.',
		'Explicit parity matrices, actual four-residual matrix, fixed right inverse and exact all-degree tail elimination.',
		'Independent local norm control via a directly computed quadratic K-functional and two fixed interior multipliers, including t=7/2.',
		'Spectral cutoff proof that Hc^4 is dense in Hc^s.',
		'Complex highest-nonzero-trace exclusion by logarithmic Fourier sequences, treating the equality points.',
		'Exact annihilator and codimension, followed by the original-family non-basis corollary.',
	],
	'author_algebra_execution': {
		'execution_manifest': artifact(str(ExecutionPath.relative_to(Root))),
		'stdout': artifact(str(AlgebraPath.relative_to(Root))),
		'stderr': artifact(str(Path(Execution['stderr']['path']).relative_to(Root))),
		'returncode': 0, 'total_checks': Algebra['total_checks'],
		'category_counts': Algebra['category_counts'],
		'evidence_boundary': 'Author exact algebra only. Does not replace or mechanically certify the infinite-dimensional proof.',
	},
	'artifact_integrity': {'status': Validation['status'],
		'checks': len(Validation['checks']), 'read_source_hashes_unchanged': True,
		'full_repository_audit_performed': False},
	'primary_source_crosscheck': {
		'url': External['verified_anchor'], 'version': External['version'],
		'locator': External['locator'],
		'use': 'Consistency reference for self-adjoint power interpolation; direct weighted proof supplied in manuscript.',
		'whole_paper_read_or_audited': False,
	},
	'review_state': {
		'independent_review_performed': False, 'acceptance_agent_started': False,
		'canonical_accepted': False, 'novelty_asserted': False, 'lean_formalization_performed': False,
		'next_owner': 'Coordinator: arrange a fresh independent review of the frozen candidate if desired under its authorization.',
	},
	'write_scope': {'allowed_root': str(Root), 'main_repository_written_by_this_author': False,
		'old_evidence_or_plugins_modified': False, 'git_commit_or_push_performed': False},
	'preserved_process_issues': [
		'Initial functions.exec JavaScript template parse failure: no shell command executed; recorded in SESSION_LOG.md.',
		'Optional arXiv v2 HTML request returned 404; actual v1 used.',
		'First local excerpt extraction matched a cross-reference rather than the theorem; original extraction preserved under logs/, corrected by actual HTML id without a network refetch.',
	],
	'artifacts': Artifacts,
	'remaining_work_in_this_author_assignment': [],
	'limitations': Card['exclusions'],
}
write_json('summary.json', Summary)
print(json.dumps({'status': Status, 'artifact_validation_checks': len(Validation['checks']),
	'exact_algebra_checks': Algebra['total_checks'], 'summary': str(Root / 'summary.json'),
	'proof_sha256': digest(ProofPath), 'card_sha256': digest(Root / 'card.json')}, ensure_ascii=False, indent=2))
