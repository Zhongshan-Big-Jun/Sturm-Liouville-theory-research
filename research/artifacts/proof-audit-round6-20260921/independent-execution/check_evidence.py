"""Independent structural checks of this session's actual Lean evidence."""
from pathlib import Path
import collections
import hashlib
import json
import os
import re
import sys
import time
from execute import OUT, AUTHOR, PROJECT, now, digest, write_json, identities

ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
ROOT = 'SL.AuditRound6.local_algebra_root'
CHECKS = []

def check(name, passed, evidence, details=None):
	CHECKS.append(dict(id=name, status='PASS' if passed else 'FAIL', evidence=evidence, details=details))

def load(path):
	return json.loads(Path(path).read_text())

def json_hash(value):
	return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def normalize(path):
	return str(path).replace('\\', '/').lower()

def windows(path):
	Text = str(path)
	if Text.startswith('/mnt/') and len(Text) > 7 and Text[6] == '/':
		return Text[5].upper() + ':' + Text[6:].replace('/', '\\')
	return Text

def expression_facts(expression):
	Constants, Tags, Binders = set(), collections.Counter(), []
	Pending = [expression]
	while Pending:
		Item = Pending.pop()
		if not isinstance(Item, list) or not Item or not isinstance(Item[0], str):
			raise ValueError('Malformed expression AST')
		Tag = Item[0]
		Tags[Tag] += 1
		if Tag == 'const':
			assert len(Item) == 2 and isinstance(Item[1], list) and len(Item[1]) == 2
			Constants.add(Item[1][0])
		elif Tag == 'app':
			assert len(Item) == 3
			Pending.extend(Item[1:])
		elif Tag in ('lam', 'forall'):
			assert len(Item) == 4
			Pending.extend(Item[2:])
		elif Tag == 'let':
			assert len(Item) == 5
			Pending.extend(Item[1:4])
		elif Tag == 'projection':
			assert len(Item) == 4
			Constants.add(Item[1])
			Pending.append(Item[3])
		elif Tag in ('bvar', 'fvar', 'mvar', 'sort', 'literal'):
			assert len(Item) == 2
		else:
			raise ValueError('Unrecognized expression tag: ' + Tag)
	Item = expression
	while Item[0] == 'forall':
		Binders.append(Item[1])
		Item = Item[3]
	return dict(constants=Constants, tags=Tags, binders=Binders)

def closure(graph, roots):
	Visited, Missing, Pending = set(), set(), list(roots)
	while Pending:
		Name = Pending.pop()
		if Name in Visited:
			continue
		Visited.add(Name)
		Node = graph.get(Name)
		if Node is None or Node.get('missing'):
			Missing.add(Name)
			continue
		Pending.extend(Node['type_dependencies'])
		Pending.extend(Node['body_dependencies'])
	Axioms = sorted(Name for Name in Visited if graph.get(Name, {}).get('kind') == 'axiom')
	Unsafe = sorted(Name for Name in Visited if graph.get(Name, {}).get('unsafe'))
	return dict(nodes=Visited, missing=sorted(Missing), axioms=Axioms, unsafe=Unsafe)

def node_identity(node):
	return {Key:node.get(Key) for Key in ('name','kind','universes','unsafe','type_dependencies','body_dependencies','missing')}

def log_check(record, stdout, stderr):
	return record.get('exit_code') == 0 and all(digest(File) == record[Stream + '_sha256'] for Stream, File in [('stdout', stdout), ('stderr', stderr)])

def main():
	assert os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'
	Replay = OUT / 'replay'
	Before, Session = load(OUT/'preflight.json'), load(OUT/'native-session.json')
	Command = load(OUT/'replay-command.json')
	Manifest, Summary = load(Replay/'positive/run-manifest.json'), load(Replay/'REPLAY_RESULT.json')
	Contract = load(AUTHOR/'positive-contract.json')
	Target, Evidence = Manifest['target'], Manifest['evidence']
	RunDir = Path(Evidence['run_directory'])
	Raw = load(RunDir/'declaration.json')
	Public, Nodes = load(Replay/'public-declarations.json'), load(Replay/'shared-public-dependency-graph.json')
	Definitions = load(Replay/'local-definitions.json')
	Graph = {Node['name']:Node for Node in Nodes}
	RootGraph = {Node['name']:Node for Node in Raw['dependencies']}
	ExpectedGraph = {Node['name']:Node for Node in Raw['expected_statement']['dependencies']}
	check('real_native_session', Session['CODEX_THREAD_ID'] == os.environ.get('CODEX_THREAD_ID') == Command['CODEX_THREAD_ID'], ['native-session.json','replay-command.json'], {'CODEX_THREAD_ID':Session['CODEX_THREAD_ID']})
	ExpectedCommand = ['python3','-B',str(AUTHOR/'replay.py'),str(Replay),'--skip-negative-control']
	check('requested_once_fresh_replay', Command['argv'] == ExpectedCommand and Command['attempts'] == 1 and Command['replay_directory_existed_at_start'] is False and log_check(Command, OUT/'replay.stdout.txt', OUT/'replay.stderr.txt'), ['replay-command.json','replay.stdout.txt','replay.stderr.txt'], {'exit_code':Command['exit_code'], 'duration_seconds':Command['duration_seconds']})
	Outer = [(PathName, load(PathName)) for PathName in sorted((Replay/'command-logs').glob('*.json'))]
	check('five_replay_stages_raw_logs', len(Outer) == 5 and all(log_check(Record, PathName.with_suffix('.stdout.txt'), PathName.with_suffix('.stderr.txt')) for PathName,Record in Outer), ['replay/command-logs'], [{'stage':PathName.stem,'exit_code':Record.get('exit_code'),'seconds':Record.get('duration_seconds')} for PathName,Record in Outer])
	Version = (Replay/'command-logs/01-runtime-version.stdout.txt').read_text().strip()
	check('actual_lean_4_31_0', 'version 4.31.0, x86_64-w64-windows-gnu' in Version and Manifest['environment']['lean_version'] == Version and Manifest['environment']['mode'] == 'direct' and Manifest['environment']['lean_toolchain'] == 'leanprover/lean4:v4.31.0', ['replay/command-logs/01-runtime-version.stdout.txt','replay/positive/run-manifest.json'], Version)
	Freeze = load(AUTHOR/'freeze.json')
	SourceBindings = {Name: Manifest['input_hashes'].get(Name) == Freeze['files']['snapshot/'+Name] for Name in Before['snapshot_files']}
	check('compiled_snapshot_bound_to_freeze', all(SourceBindings.values()), ['preflight.json','replay/positive/run-manifest.json'], SourceBindings)
	Builds = [Entry for Entry in Manifest['build']['commands'] if Entry.get('kind') == 'target']
	LocalRows = []
	for Entry in Builds:
		Object = Path(Entry['olean'])
		Relative = Entry['file']
		ExpectedObject = (RunDir/'lib'/Relative).with_suffix('.olean')
		ExpectedSource = AUTHOR/'snapshot'/Relative
		Passed = Entry['status'] == 'passed' and Entry['exit_code'] == 0 and Object == ExpectedObject and Object.is_relative_to(OUT) and Object.is_file() and Entry['command'][-3] == '-o' and normalize(Entry['command'][-2]) == normalize(windows(Object)) and normalize(Entry['command'][-1]) == normalize(windows(ExpectedSource)) and Evidence['compiled_artifacts'].get(str(Object)) == digest(Object)
		LocalRows.append(dict(file=Relative, passed=Passed, object=str(Object), object_sha256=digest(Object), source_sha256=digest(ExpectedSource), command=Entry['command'], job_record=Entry['job_record'], elapsed_seconds=Entry['elapsed_seconds']))
	write_json(OUT/'local-build-checks.json', LocalRows)
	check('round5_and_round6_fresh_source_compilation', [Row['file'] for Row in LocalRows] == ['SL/AuditRound5.lean','SL/AuditRound6.lean'] and all(Row['passed'] for Row in LocalRows), ['local-build-checks.json'], LocalRows)
	Modules = Target['imported_modules']
	ModuleMap = {Entry['module']:Entry['olean'] for Entry in Modules}
	LocalImportOK = all(normalize(ModuleMap.get(Module,'')) == normalize(windows(RunDir/'lib'/Path(*Module.split('.')).with_suffix('.olean'))) for Module in ('SL.AuditRound5','SL.AuditRound6','LeanVerifyProbe'))
	check('actual_loaded_import_inventory', Target['module_inventory_scope'] == 'loaded_environment' and len(Modules) == Target['loaded_module_count'] == len(ModuleMap) and LocalImportOK, ['replay/positive/run-manifest.json','receipt.stdout.txt'], {'loaded_modules':len(Modules),'hashed_import_artifacts':len(Target['import_artifacts']),'local_objects':{Name:ModuleMap[Name] for Name in ('SL.AuditRound5','SL.AuditRound6','LeanVerifyProbe')}})
	Config = load(AUTHOR/'runtime-config.json')
	AllowedRoots = [RunDir/'lib', Path(Manifest['environment']['prefix'])/'lib/lean'] + [Path(Name) for Name in Config['package_search_paths']]
	AllowedPrefixes = [normalize(windows(PathName)).rstrip('/')+'/' for PathName in AllowedRoots]
	Outside = [Entry for Entry in Modules if not any(normalize(Entry['olean']).startswith(Prefix) for Prefix in AllowedPrefixes)]
	check('no_old_project_object_resolution', not Outside and {Entry['module'] for Entry in Modules if Entry['module'].startswith('SL.')} == {'SL.AuditRound5','SL.AuditRound6'} and LocalImportOK, ['replay/positive/run-manifest.json','receipt.stdout.txt'], {'objects_outside_allowed_roots':Outside,'allowed_roots':[str(PathName) for PathName in AllowedRoots]})
	RootArtifact = load(Replay/'root-artifact.json')
	check('exact_root_object_resolution_and_hash', RootArtifact['declaration'] == ROOT and RootArtifact['olean'] == str(RunDir/'lib/SL/AuditRound6.olean') and RootArtifact['olean_sha256'] == digest(RootArtifact['olean']) and RootArtifact['source_sha256'] == Freeze['original_source_sha256'], ['replay/root-artifact.json','replay/command-logs/05-root-resolution.stdout.txt'], RootArtifact)
	Comparison = Target['comparison']
	check('actual_expected_type_matching', Target['declaration'] == Contract['declaration'] == ROOT and Target['kind'] == 'theorem' and Target['expected_type'] == Contract['expected_type'] and Evidence['contract'] == Contract and Comparison['status'] == 'matched' and all(Comparison[Name] is True for Name in ('definitionally_equal','universe_parameters_match','binder_kinds_match')) and Target['universes'] == [] and Target['binder_kinds'] == [] and Comparison['expected_type_expression'] == Target['expected_statement']['type_expression'], ['replay/positive/run-manifest.json','replay/PositiveControl.lean','replay/command-logs/03-compiling-positive-control.json'], {Name:Value for Name,Value in Comparison.items() if Name != 'expected_type_expression'})
	PositiveSource = 'import SL.AuditRound6\nexample : ' + Contract['expected_type'] + ' := ' + ROOT + '\n'
	check('independently_compiled_positive_control', (Replay/'PositiveControl.lean').read_text() == PositiveSource and load(Replay/'command-logs/03-compiling-positive-control.json')['exit_code'] == 0, ['replay/PositiveControl.lean','replay/command-logs/03-compiling-positive-control.stdout.txt'])
	RootClosure = closure(RootGraph, [ROOT])
	check('root_transitive_closure_recomputed', RootClosure['nodes'] == set(RootGraph) and len(RootGraph) == len(Raw['dependencies']) and RootClosure['axioms'] == sorted(Raw['axioms']) and set(RootClosure['axioms']) <= ALLOWED and not RootClosure['missing'] and not RootClosure['unsafe'], ['replay/positive/run-manifest.json'], {'nodes':len(RootClosure['nodes']),'axioms':RootClosure['axioms'],'unsafe':RootClosure['unsafe'],'missing':RootClosure['missing']})
	ExpectedFacts = expression_facts(Raw['expected_statement']['type_expression'])
	ExpectedClosure = closure(ExpectedGraph, ExpectedFacts['constants'])
	check('expected_type_closure_recomputed', ExpectedClosure['nodes'] == set(ExpectedGraph) and ExpectedClosure['axioms'] == sorted(Raw['expected_statement']['axioms']) and set(ExpectedClosure['axioms']) <= ALLOWED and not ExpectedClosure['missing'] and not ExpectedClosure['unsafe'] and 'LeanVerifyV2.expected_statement' not in RootGraph and 'LeanVerifyV2.expected_statement' not in ExpectedGraph, ['replay/positive/run-manifest.json'], {'nodes':len(ExpectedClosure['nodes']),'axioms':ExpectedClosure['axioms'],'synthetic_comparison_axiom_excluded':True})
	Entries = re.findall(r'^(?:noncomputable )?(def|theorem|lemma) (\w+)', (AUTHOR/'snapshot/SL/AuditRound6.lean').read_text(), re.M)
	Declared = {'SL.AuditRound6.'+Name:('definition' if Kind=='def' else 'theorem') for Kind,Name in Entries}
	check('all_explicit_public_declarations_exported', len(Public) == len(Declared) and {Entry['declaration']:Entry['kind'] for Entry in Public} == Declared, ['replay/public-declarations.json','preflight.json'], {'public_declarations':len(Public),'theorems':sum(Entry['kind']=='theorem' for Entry in Public),'definitions':sum(Entry['kind']=='definition' for Entry in Public),'scope':'Every explicit public definition/theorem in frozen AuditRound6; compiler-generated helpers participate through dependency closure.'})
	PublicRows, Union = [], set()
	for Entry in Public:
		Name = Entry['declaration']
		Node = Graph.get(Name,{})
		Facts, Closed = expression_facts(Entry['type_expression']), closure(Graph,[Name])
		Union.update(Closed['nodes'])
		TypeChecks = dict(kind=Node.get('kind') == Entry['kind'], universes=Node.get('universes') == Entry['universes'], binder_kinds=Facts['binders'] == Entry['binder_kinds'], type_constants=Facts['constants'] == set(Entry['type_dependencies']), type_edges=Node.get('type_dependencies') == Entry['type_dependencies'], body_edges=Node.get('body_dependencies') == Entry['body_dependencies'], no_free_metavariables=not Facts['tags']['mvar'] and not Facts['tags']['fvar'], actual_types_present=bool(Entry['actual_type'].strip()) and bool(Entry['fully_explicit_type'].strip()))
		AxiomOK = Closed['axioms'] == sorted(Entry['transitive_axioms']) and set(Closed['axioms']) <= ALLOWED and not Closed['unsafe'] and not Closed['missing']
		PublicRows.append(dict(declaration=Name, kind=Entry['kind'], passed=all(TypeChecks.values()) and AxiomOK, type_checks=TypeChecks, type_expression_sha256=json_hash(Entry['type_expression']), closure_nodes=len(Closed['nodes']), reported_axioms=Entry['transitive_axioms'], recomputed_axioms=Closed['axioms'], axioms_match=AxiomOK, unsafe=Closed['unsafe'], missing=Closed['missing']))
	write_json(OUT/'public-declaration-checks.json', PublicRows)
	check('every_public_type_and_axiom_closure_consistent', all(Row['passed'] for Row in PublicRows), ['public-declaration-checks.json','replay/public-declarations.json','replay/shared-public-dependency-graph.json'], {'checked':len(PublicRows),'failed':[Row['declaration'] for Row in PublicRows if not Row['passed']]})
	check('shared_graph_exact_public_union', len(Graph) == len(Nodes) and Union == set(Graph) and not any(Node.get('unsafe') or Node.get('missing') for Node in Nodes) and {Node['name'] for Node in Nodes if Node.get('kind')=='axiom'} <= ALLOWED, ['replay/shared-public-dependency-graph.json','public-declaration-checks.json'], {'nodes':len(Graph),'duplicate_nodes':len(Nodes)-len(Graph),'extra_nodes':sorted(set(Graph)-Union),'absent_nodes':sorted(Union-set(Graph))})
	NodeMismatch = [Name for Name,Node in RootGraph.items() if Name not in Graph or node_identity(Node) != node_identity(Graph[Name])]
	RootPublic = next(Entry for Entry in Public if Entry['declaration']==ROOT)
	check('root_matches_shared_export', not NodeMismatch and RootPublic['type_expression'] == Raw['type_expression'] and RootPublic['universes'] == Raw['universes'] and RootPublic['binder_kinds'] == Raw['binder_kinds'] and RootPublic['transitive_axioms'] == Raw['axioms'], ['replay/public-declarations.json','replay/shared-public-dependency-graph.json','replay/positive/run-manifest.json'], {'node_mismatches':NodeMismatch})
	DefinitionRows = []
	for Entry in Definitions:
		Name = Entry['name']
		Node = Graph.get(Name,{})
		TypeFacts = expression_facts(Entry['type_expression'])
		ValueFacts = expression_facts(Entry['value_expression'])
		RootNode = RootGraph.get(Name,{})
		Matches = TypeFacts['constants'] == set(Node.get('type_dependencies',[])) and ValueFacts['constants'] == set(Node.get('body_dependencies',[])) and all(RootNode.get(Key,Entry[Key]) == Entry[Key] for Key in ('type_expression','value_expression'))
		DefinitionRows.append(dict(name=Name, passed=Matches, root_type_ast_compared='type_expression' in RootNode, root_value_ast_compared='value_expression' in RootNode, type_expression_sha256=json_hash(Entry['type_expression']), value_expression_sha256=json_hash(Entry['value_expression'])))
	write_json(OUT/'local-definition-checks.json', DefinitionRows)
	ExpectedDefs = {Name for Name,Node in Graph.items() if Name.startswith('SL.') and Node.get('kind') in ('definition','opaque')}
	check('reachable_local_definitions_consistent', {Entry['name'] for Entry in Definitions} == ExpectedDefs and len(Definitions)==len(ExpectedDefs) and all(Row['passed'] for Row in DefinitionRows), ['local-definition-checks.json','replay/local-definitions.json'], {'count':len(Definitions),'failed':[Row['name'] for Row in DefinitionRows if not Row['passed']],'missing':sorted(ExpectedDefs-{Entry['name'] for Entry in Definitions})})
	check('no_unproved_or_unsafe_root_dependencies', Target['unexpected_axioms']==[] and Target['unsafe_dependencies']==[] and Target['unknown_dependencies']==[] and Target['missing_artifacts']==[] and Manifest['sorry_axiom_hits']==[] and 'sorryAx' not in Graph and not any(Node.get('kind')=='axiom' and Node['name'] not in ALLOWED for Node in Nodes), ['replay/positive/run-manifest.json','replay/shared-public-dependency-graph.json'], {'root_axioms':RootClosure['axioms'],'source_scan_is_supplementary':True})
	check('machine_and_exact_root_closed', Manifest['machine_verification_passed'] is True and Manifest['exact_root_passed'] is True and Manifest['root_closure']['status']=='closed' and Manifest['machine']['status']=='passed' and Manifest['machine']['scope']=='exact_declaration' and Evidence['status']=='current' and all(Evidence[Key]==[] for Key in ('changed_inputs','changed_imports','changed_tools')), ['replay/positive/run-manifest.json'])
	write_json(OUT/'structural-checkpoint.json', dict(generated_at=now(), checks=CHECKS, receipt_recheck_pending=True, final_verdict=False))
	print(json.dumps(dict(phase='structural_checks_complete', checked=len(CHECKS), failed=[Entry['id'] for Entry in CHECKS if Entry['status']=='FAIL'], awaiting='receipt recheck only')), flush=True)
	while 'exit_code' not in (ReceiptCommand := load(OUT/'receipt-command.json')):
		time.sleep(1)
	Receipt = load(OUT/'receipt.stdout.txt')
	check('receipt_current_hashes_and_resolution', log_check(ReceiptCommand, OUT/'receipt.stdout.txt', OUT/'receipt.stderr.txt') and Receipt.get('status') == 'current' and Receipt.get('snapshot_current') is True and Receipt.get('exact_root_passed') is True and Receipt.get('reasons') == [], ['receipt-command.json','receipt.stdout.txt','receipt.stderr.txt'], Receipt)
	After = identities()
	write_json(OUT/'postflight.json', After)
	check('frozen_inputs_before_and_after', Before['passed'] and After['passed'] and Before['freeze_sha256'] == After['freeze_sha256'] and Before['snapshot_files'] == After['snapshot_files'], ['preflight.json','postflight.json'], {'identity_checks_each':len(Before['checks']), 'freeze_sha256':Before['freeze_sha256']})
	Jobs = [load(PathName) for PathName in RunDir.parent.rglob('*.job.json')]
	Forbidden = [Job['command'] for Job in Jobs if any(Path(str(Arg)).name.lower() in ('lake','lake.exe') for Arg in Job['command']) and 'build' in Job['command']]
	Bytecode = [str(PathName) for Base in (OUT, AUTHOR/'snapshot') for PathName in Base.rglob('*') if PathName.name=='__pycache__' or PathName.suffix in ('.pyc','.pyo')]
	check('no_full_lake_build_or_bytecode', not Forbidden and not Bytecode and all(Record['PYTHONDONTWRITEBYTECODE']=='1' for _,Record in Outer) and Command['PYTHONDONTWRITEBYTECODE']=='1' and ReceiptCommand['PYTHONDONTWRITEBYTECODE']=='1', ['replay-command.json','receipt-command.json','replay/command-logs'], {'forbidden_commands':Forbidden,'bytecode_in_output_or_snapshot':Bytecode})
	check('negative_control_explicitly_not_run', Summary['wrong_expected_type_rejected'] is None and not (Replay/'negative').exists() and not any('negative' in PathName.stem for PathName,_ in Outer), ['replay/REPLAY_RESULT.json','replay-command.json'], {'independently_run':False,'status':'NOT_RUN_BY_REQUEST','author_evidence':'Not read or adopted; separate semantic review must assess it.'})
	check('role_and_semantic_boundary_preserved', Summary['role']=='author_execution_not_independent_review' and Summary['independent_review']=='not_performed' and Session['final_semantic_approval'] is False, ['native-session.json','replay/REPLAY_RESULT.json'], {'replay_role_field':'Frozen generic script text, not this native session identity. Preserved unmodified.','actual_role':Session['role'],'semantic_result':Manifest['semantic']})
	Failed = [Entry['id'] for Entry in CHECKS if Entry['status']=='FAIL']
	Result = dict(schema_version=1, generated_at=now(), verdict='PASS' if not Failed else 'FAIL', scope='Independent execution verification of the frozen local real-algebra target; no final semantic approval.', CODEX_THREAD_ID=Session['CODEX_THREAD_ID'], negative_control='NOT_RUN_BY_REQUEST', checks=CHECKS, passed=sum(Entry['status']=='PASS' for Entry in CHECKS), failed=Failed, public_declarations=len(Public), root_dependency_nodes=len(RootGraph), shared_public_dependency_nodes=len(Graph), loaded_modules=len(Modules), imported_artifact_files=len(Target['import_artifacts']), source_sha256=Freeze['original_source_sha256'], freeze_sha256=Before['freeze_sha256'], replay_seconds=Command['duration_seconds'])
	write_json(OUT/'CHECKS.json', Result)
	print(json.dumps({Key:Result[Key] for Key in ('verdict','passed','failed','public_declarations','root_dependency_nodes','shared_public_dependency_nodes','loaded_modules','imported_artifact_files')},ensure_ascii=False,indent=2),flush=True)
	return 0 if not Failed else 1

if __name__=='__main__':
	sys.exit(main())
