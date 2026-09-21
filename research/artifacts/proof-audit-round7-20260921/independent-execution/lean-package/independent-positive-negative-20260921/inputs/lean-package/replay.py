"""Recompile the round-7 candidate and rerun author machine controls in a new directory.

Usage: python3 -B replay.py /mnt/f/tools/math-audit-round7-20260921/lean-author/replay-new
Uses the existing Windows Lean/mathlib installation. No network or Lake build.
The result records author execution only; independent semantic review is pending.
"""
from pathlib import Path
import argparse, json, re, sys
from run_lean import BASE, digest, environment, run, win, write_json

def require(condition, message):
	if not condition:
		raise RuntimeError(message)

def inspection_source(output, source):
	Entries = re.findall(r'^(def|theorem|lemma) (\w+)', source.read_text(), re.M)
	Names = ['SL.AuditRound7.' + Name for Kind, Name in Entries]
	Lines = ['import Lean', 'import SL.AuditRound7', 'set_option maxRecDepth 100000',
		'set_option maxHeartbeats 0', 'set_option pp.universes true', 'set_option pp.fullNames true']
	for (Kind, _), Name in zip(Entries, Names):
		Lines += ['#check ' + Name, '#print axioms ' + Name]
		if Kind == 'def':
			Lines.append('#print ' + Name)
	Lines += ['open Lean Elab Command in', 'run_cmd do', '  let Env := (← getEnv).setExporting false',
		'  let Targets : Array Name := #[' + ', '.join('`' + Name for Name in Names) + ']',
		'  let mut Results : Array Json := #[]',
		'  for Target in Targets do',
		'    let some Info := Env.checked.get.find? Target | throwError "Missing public declaration: {Target}"',
		'    let Type ← liftTermElabM <| withOptions (fun O => O.setBool `pp.universes true |>.setBool `pp.fullNames true) do',
		'      return (← ppExpr Info.type).pretty',
		'    let Axioms ← collectAxioms Target',
		'    Results := Results.push <| Json.mkObj [',
		'      ("declaration", toJson Target.toString), ("actual_type", toJson Type),',
		'      ("is_theorem", toJson Info.isTheorem),',
		'      ("universes", toJson (Info.levelParams.map Name.toString)),',
		'      ("transitive_axioms", toJson (Axioms.toList.map Name.toString))]',
		'  IO.FS.writeFile ' + json.dumps(win(output / 'public-declarations.json')) + ' ((Json.arr Results).pretty ++ "\\n")']
	Probe = output / 'Inspection.lean'
	Probe.write_text('\n'.join(Lines) + '\n')
	return Probe, Names

def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument('output', type=Path)
	Args = Parser.parse_args()
	Output = Args.output.resolve()
	require(Output.is_relative_to(BASE) and Output != BASE, 'Output must be a new child of lean-author')
	Output.mkdir(parents=True, exist_ok=False)
	Freeze = json.loads((BASE / 'freeze.json').read_text())
	Checks = {Name:digest(BASE / Name) == Hash for Name, Hash in Freeze['files'].items()}
	Checks.update({Name:digest(Name) == Hash for Name, Hash in Freeze['external_inputs'].items()})
	write_json(Output / 'input-identity-checks.json', Checks)
	require(all(Checks.values()), 'Frozen source/runtime/tool/config identity mismatch')
	Config = json.loads((BASE / 'runtime-config.json').read_text())
	Snapshot = BASE / 'snapshot'
	Source = Snapshot / 'SL/AuditRound7.lean'
	Env = environment()
	require(Env['LEAN_PATH'] == Config['LEAN_PATH'], 'Package search path changed')
	Common = [sys.executable, '-B', Config['verifier'], '--project', str(Snapshot), '--direct',
		'--lean', Config['lean'], '--lake', Config['lake'], '--strict-exit', '--build-timeout', '1800']
	# Preserve small local source/config snapshots; external binaries and packages are hash-bound only.
	Inputs = [BASE / N for N in Freeze['files']]
	Version = run(Output, '01-version', [Config['lean'], '--version'], Env, Snapshot, [Source])
	require(Version['exit_code'] == 0, 'Lean version command failed')
	VersionText = (Output / 'logs/01-version.stdout.txt').read_text()
	require('version 4.31.0, x86_64-w64-windows-gnu' in VersionText, 'Unexpected Lean version')
	Positive = run(Output, '02-exact-root', Common + ['--contract', str(BASE / 'positive-contract.json'),
		'--output', str(Output / 'positive')], Env, Snapshot, Inputs)
	ManifestPath = Output / 'positive/run-manifest.json'
	Manifest = json.loads(ManifestPath.read_text())
	require(Positive['exit_code'] == 0 and Manifest['machine_verification_passed'] and Manifest['exact_root_passed'],
		'Exact root not closed; inspect retained positive manifest and logs')
	Library = Path(Manifest['evidence']['run_directory']) / 'lib'
	ProbeEnv = environment([Library])
	Contract = json.loads((BASE / 'positive-contract.json').read_text())
	Control = Output / 'PositiveControl.lean'
	Control.write_text('import SL.AuditRound7\nopen SL.AuditRound7\nexample : ' +
		Contract['expected_type'] + ' := SL.AuditRound7.local_algebra_root\n')
	ControlRun = run(Output, '03-positive-control', [Config['lean'], win(Control)], ProbeEnv, Snapshot, [Source, Control])
	require(ControlRun['exit_code'] == 0, 'Direct positive control failed')
	Probe, Names = inspection_source(Output, Source)
	ProbeRun = run(Output, '04-all-declarations', [Config['lean'], win(Probe)], ProbeEnv, Snapshot, [Source, Probe])
	require(ProbeRun['exit_code'] == 0, 'Public declaration inspection failed')
	Public = json.loads((Output / 'public-declarations.json').read_text())
	require([P['declaration'] for P in Public] == Names, 'Public inventory mismatch')
	Allowed = {'propext', 'Classical.choice', 'Quot.sound'}
	require(all(set(P['transitive_axioms']) <= Allowed for P in Public), 'Disallowed public axiom')
	Resolution = run(Output, '05-import-resolution', [Config['lean'], '--deps', win(Control)], ProbeEnv, Snapshot, [Source, Control])
	require(Resolution['exit_code'] == 0, 'Root resolution failed')
	Object = Library / 'SL/AuditRound7.olean'
	Resolved = (Output / 'logs/05-import-resolution.stdout.txt').read_text().splitlines()
	require(win(Object).replace('\\', '/').lower() in [S.replace('\\', '/').lower() for S in Resolved],
		'Imported root did not resolve to newly compiled object')
	write_json(Output / 'root-artifact.json', dict(source_path=str(Source), source_sha256=digest(Source),
		declaration=Contract['declaration'], olean_path=str(Object), olean_sha256=digest(Object),
		resolution_log='logs/05-import-resolution.stdout.txt'))
	Negative = run(Output, '06-wrong-target', Common + ['--contract', str(BASE / 'wrong-target-contract.json'),
		'--output', str(Output / 'negative')], Env, Snapshot, Inputs)
	NegativeManifest = json.loads((Output / 'negative/run-manifest.json').read_text())
	NegativeOK = (Negative['exit_code'] == 1 and NegativeManifest['machine_verification_passed'] and
		not NegativeManifest['exact_root_passed'] and NegativeManifest['root_closure']['status'] == 'target_mismatch')
	require(NegativeOK, 'Old Wronskian expected target was not rejected with target_mismatch')
	WrongFactor = BASE / 'controls/WrongMirrorFactor.lean'
	Factor = run(Output, '07-old-mirror-factor', [Config['lean'], win(WrongFactor)], ProbeEnv, Snapshot, [Source, WrongFactor])
	FactorText = (Output / 'logs/07-old-mirror-factor.stdout.txt').read_text()
	require(Factor['exit_code'] != 0 and 'Type mismatch' in FactorText, 'Old mirror factor did not fail as intended')
	After = {Name:digest(BASE / Name) == Hash for Name, Hash in Freeze['files'].items()}
	After.update({Name:digest(Name) == Hash for Name, Hash in Freeze['external_inputs'].items()})
	write_json(Output / 'final-input-identity-checks.json', After)
	require(all(After.values()), 'An input changed during replay')
	Summary = dict(status='author_machine_checks_passed', role='local_lean_author', independent_execution='not_performed_by_this_runner',
		independent_semantic_review='pending', source_sha256=digest(Source), declaration=Contract['declaration'],
		exact_root_passed=Manifest['exact_root_passed'], root_axioms=Manifest['target']['axioms'],
		public_declarations=len(Public), public_theorems=sum(P['is_theorem'] for P in Public),
		public_definitions=sum(not P['is_theorem'] for P in Public), wrong_target_rejected=NegativeOK,
		wrong_mirror_factor_exit_code=Factor['exit_code'], positive_control_exit_code=ControlRun['exit_code'],
		inputs_unchanged=True, environment_sha256=Manifest['target']['environment_sha256'],
		semantic_sha256=Manifest['target']['semantic_sha256'], loaded_module_count=Manifest['target']['loaded_module_count'],
		import_artifact_count=len(Manifest['target']['import_artifacts']),
		positive_manifest=dict(path=str(ManifestPath), sha256=digest(ManifestPath)),
		negative_manifest=dict(path=str(Output / 'negative/run-manifest.json'), sha256=digest(Output / 'negative/run-manifest.json')),
		unformalized=['infinite-dimensional Volterra estimates', 'Taylor expansion and remainder',
			'spectral differentiability/Feynman-Hellmann premises', 'spectral limits and min-max analysis'])
	write_json(Output / 'evidence.json', Summary)
	print(json.dumps(Summary, indent=2, ensure_ascii=False), flush=True)
	return 0

if __name__ == '__main__':
	sys.exit(main())
