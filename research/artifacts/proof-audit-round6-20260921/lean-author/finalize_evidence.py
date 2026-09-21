"""Summarize actual replay evidence; does not change Lean sources or receipts."""
from pathlib import Path
import hashlib, json, sys

BASE = Path(__file__).resolve().parent

def digest(path):
	with Path(path).open('rb') as File:
		return hashlib.file_digest(File, 'sha256').hexdigest()

def write_json(path, value):
	Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def main():
	Replay = Path(sys.argv[1]).resolve()
	Result = json.loads((Replay / 'REPLAY_RESULT.json').read_text())
	assert Result['status'] == 'passed'
	Manifest = json.loads((Replay / 'positive/run-manifest.json').read_text())
	Target = Manifest['target']
	Public = json.loads((Replay / 'public-declarations.json').read_text())
	Nodes = {Node['name']: Node for Node in json.loads((Replay / 'shared-public-dependency-graph.json').read_text())}
	Checks = []
	for Declaration in Public:
		Pending = [Declaration['declaration']]
		Used = set()
		while Pending:
			Name = Pending.pop()
			if Name in Used:
				continue
			Used.add(Name)
			Node = Nodes.get(Name, {})
			Pending.extend(Node.get('type_dependencies', []) + Node.get('body_dependencies', []))
		Axioms = sorted(Name for Name in Used if Nodes.get(Name, {}).get('kind') == 'axiom')
		Missing = sorted(Name for Name in Used if Name not in Nodes or Nodes[Name].get('missing'))
		Unsafe = sorted(Name for Name in Used if Nodes.get(Name, {}).get('unsafe'))
		Passed = Axioms == sorted(Declaration['transitive_axioms']) and not Missing and not Unsafe
		Checks.append(dict(declaration=Declaration['declaration'], reachable_nodes=len(Used), graph_axioms=Axioms, lean_collectAxioms=Declaration['transitive_axioms'], missing=Missing, unsafe=Unsafe, passed=Passed))
	write_json(BASE / 'closure-consistency.json', dict(shared_nodes=len(Nodes), per_declaration=Checks, passed=all(c['passed'] for c in Checks)))
	assert all(c['passed'] for c in Checks)
	Before = json.loads((BASE / 'protected-before.json').read_text())
	Changed = [Name for Name, Hash in Before.items() if not Path(Name).is_file() or digest(Name) != Hash]
	GitPolicy = '/mnt/f/LaTeX/BVE research/lean-proof/SL/.gitattributes'
	ConcurrentGit = []
	if GitPolicy in Changed:
		Data = Path(GitPolicy).read_bytes()
		Suffix = b'\n# Sixth-round materialized algebra root.\nAuditRound6.lean -text\n'
		assert Data.endswith(Suffix) and hashlib.sha256(Data[:-len(Suffix)]).hexdigest() == Before[GitPolicy]
		ConcurrentGit.append(dict(path=GitPolicy, before_sha256=Before[GitPolicy], after_sha256=digest(GitPolicy), exact_appended_text=Suffix.decode(), author_modified=False, area_owner='coordinator; individual writer identity not independently established'))
	Unexpected = [Name for Name in Changed if Name != GitPolicy]
	write_json(BASE / 'protection-check.json', dict(protected_count=len(Before), unchanged_count=len(Before)-len(Changed), all_baseline_files_unchanged=not Changed, changed_paths=Changed, concurrent_git_policy_changes=ConcurrentGit, unexpected_changes=Unexpected, passed=not Unexpected, scope='No protected Lean source, pin/config or object change; the separately recorded Git attributes append is not counted as unchanged.'))
	assert not Unexpected
	Frozen = json.loads((BASE / 'freeze.json').read_text())
	Original = Path(Frozen['original_source'])
	assert digest(Original) == Result['source_sha256'] == Frozen['original_source_sha256']
	LocalImport = Target['import_artifacts']['SL.AuditRound5']
	assert Path(LocalImport['path']).is_relative_to(Replay)
	Bindings = dict(root=json.loads((Replay / 'root-artifact.json').read_text()), rebuilt_AuditRound5=LocalImport, AuditRound5_source_sha256=digest(BASE / 'snapshot/SL/AuditRound5.lean'), loaded_module_count=Target['loaded_module_count'], module_artifact_count=len(Target['import_artifacts']), type_sha256=Target['type_sha256'], semantic_sha256=Target['semantic_sha256'], environment_sha256=Target['environment_sha256'], shared_manifest=str(Replay / 'positive/run-manifest.json'))
	write_json(BASE / 'root-object-bindings.json', Bindings)
	Inputs = {
		'blind_readback': [Replay / 'public-types.txt', Replay / 'local-definitions.txt', Replay / 'local-definitions.json'],
		'semantic_review': [BASE / 'CONTRACT.md', BASE / 'HANDOFF_RULES.md', BASE / 'candidate-inputs/projection_and_moment_repairs.md', BASE / 'candidate-inputs/fractional_window_completion.md', BASE / 'snapshot/SL/AuditRound5.lean', BASE / 'snapshot/SL/AuditRound6.lean', Replay / 'public-declarations.json', Replay / 'local-definitions.json'],
		'execution_review': [BASE / 'freeze.json', BASE / 'runtime-config.json', BASE / 'positive-contract.json', BASE / 'wrong-expected-contract.json', BASE / 'replay.py', Replay / 'positive/run-manifest.json', Replay / 'negative/run-manifest.json', Replay / 'root-artifact.json', Replay / 'shared-public-dependency-graph.json', BASE / 'closure-consistency.json', BASE / 'root-object-bindings.json', BASE / 'protection-check.json']
	}
	Handoff = {Group: [dict(path=str(p), sha256=digest(p)) for p in Paths] for Group, Paths in Inputs.items()}
	Handoff['instructions'] = {'blind_readback': 'Actual types and elaborated reachable definitions only, including R5 definitions. No full R5/R6 source, proof scripts, intended-meaning comments, CONTRACT or author verdict. This selection implements the coordinator follow-up and supersedes the older packet suggestion in frozen CONTRACT.md.', 'semantic_review': 'Compare the real-algebra elaboration with the two candidate appendices; unchanged full R5 source is available here. No complex/Sobolev/density/spectral claim is established by this package.', 'execution_review': 'Use python3 -B replay.py NEW_OUTPUT_DIR. Commands, raw stdout/stderr, generated probes and artifacts are under the replay directory; original runs must remain unchanged.'}
	write_json(BASE / 'HANDOFF.json', Handoff)
	Summary = dict(Result, root_closure=Manifest['root_closure'], semantic_review=Manifest['semantic'], local_definitions=len(json.loads((Replay / 'local-definitions.json').read_text())), protected_old_files_unchanged=len(Before)-len(Changed), concurrent_git_policy_changes=ConcurrentGit, shared_dependency_nodes=len(Nodes), closure_consistency_passed=True, loaded_module_count=Target['loaded_module_count'], module_artifact_count=len(Target['import_artifacts']), replay_directory=str(Replay), root_object_sha256=Bindings['root']['olean_sha256'], omitted_optional_targets=['general Hilbert projection identity', 'finite-dimensional tail-obstacle injection lemma'], analytic_scope='No complex analytic, Sobolev, spectral, series convergence, graph-core, fractional-window or topological-density theorem')
	write_json(BASE / 'RESULTS.json', Summary)
	print(json.dumps(Summary, indent=2, ensure_ascii=False))
	return 0

if __name__ == '__main__':
	sys.exit(main())
