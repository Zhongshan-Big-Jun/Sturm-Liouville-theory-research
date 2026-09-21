"""Rebuild and check the frozen round-6 target into a NEW output directory.

Usage: python3 -B replay.py /mnt/f/tools/.../new-output
No source edits, downloads, Lake build, old project objects, or plugin writes.
The maintained verifier is called unchanged; author controls are separate.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess, sys, time

BASE = Path(__file__).resolve().parent

def digest(path):
	with Path(path).open('rb') as File:
		return hashlib.file_digest(File, 'sha256').hexdigest()

def write_json(path, value):
	Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def win(path):
	return subprocess.check_output(['wslpath', '-w', str(path)], text=True).strip()

def run(output, label, args, env, cwd):
	Record = dict(argv=list(map(str, args)), cwd=str(cwd), utc_start=datetime.datetime.now(datetime.timezone.utc).isoformat(), LEAN_PATH=env['LEAN_PATH'], PYTHONDONTWRITEBYTECODE=env['PYTHONDONTWRITEBYTECODE'])
	Logs = output / 'command-logs'
	Logs.mkdir(exist_ok=True)
	Prefix = Logs / label
	assert not Prefix.with_suffix('.json').exists()
	write_json(Prefix.with_suffix('.json'), Record)
	Start = time.monotonic()
	with Prefix.with_suffix('.stdout.txt').open('xb') as Stdout, Prefix.with_suffix('.stderr.txt').open('xb') as Stderr:
		Process = subprocess.Popen(args, cwd=cwd, env=env, stdout=Stdout, stderr=Stderr)
		Record['pid'] = Process.pid
		write_json(Prefix.with_suffix('.json'), Record)
		Record['exit_code'] = Process.wait()
	Record.update(duration_seconds=time.monotonic()-Start, utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat())
	for Stream in ('stdout', 'stderr'):
		Record[Stream + '_sha256'] = digest(Prefix.with_suffix('.' + Stream + '.txt'))
	write_json(Prefix.with_suffix('.json'), Record)
	print(label, 'exit', Record['exit_code'], 'seconds', round(Record['duration_seconds'], 2), flush=True)
	return Record

def public_probe(output, source):
	Entries = re.findall(r'^(?:noncomputable )?(def|theorem|lemma) (\w+)', source.read_text(), re.M)
	Names = ['SL.AuditRound6.' + Name for Kind, Name in Entries]
	Probe = '''import LeanVerifyProbe
import SL.AuditRound6
set_option maxRecDepth 100000
set_option maxHeartbeats 0
open Lean Elab Command Meta LeanVerifyV2 in
run_cmd do
  let Env := (← getEnv).setExporting false
'''
	Probe += '  let Targets : Array Name := #[' + ', '.join('`' + Name for Name in Names) + ']\n'
	Probe += '  let Out := ' + json.dumps(win(output)) + '\n'
	Probe += '''  let mut Results : Array Json := #[]
  let mut Readable := ""
  for Target in Targets do
    let some Info := Env.checked.get.find? Target
      | throwError "Missing public declaration: {Target}"
    let ActualType ← liftTermElabM <| withOptions
      (fun O => O.setBool `pp.universes true |>.setBool `pp.fullNames true) do
        return (← ppExpr Info.type).pretty
    let FullType ← liftTermElabM <| withOptions
      (fun O => O.setBool `pp.all true |>.setBool `pp.proofs true) do
        return (← ppExpr Info.type).pretty
    let Axioms ← collectAxioms Target
    Results := Results.push <| Json.mkObj [
      ("declaration", toJson Target.toString), ("kind", toJson (kind_name Info)),
      ("actual_type", toJson ActualType), ("fully_explicit_type", toJson FullType),
      ("type_expression", expr_json Info.type),
      ("universes", toJson (Info.levelParams.map Name.toString)),
      ("binder_kinds", toJson (binder_kinds Info.type)),
      ("transitive_axioms", names_json Axioms),
      ("type_dependencies", names_json Info.type.getUsedConstants),
      ("body_dependencies", names_json (body_dependencies Info))]
    Readable := Readable ++ kind_name Info ++ " " ++ Target.toString ++ " :\\n" ++ ActualType ++ "\\n\\n"
  let Used := dependency_closure Env Targets.toList
  let Nodes := Used.toArray.qsort Name.lt |>.map fun N => node_json Env N false
  let mut Definitions : Array Json := #[]
  let mut DefinitionText := ""
  for N in Used.toArray.qsort Name.lt do
    if N.toString.startsWith "SL." then
      if let some Info := Env.checked.get.find? N then
        if !Info.isTheorem then
          if let some Value := Info.value? (allowOpaque := true) then
            let T ← liftTermElabM <| withOptions
              (fun O => O.setBool `pp.fullNames true |>.setBool `pp.universes true) do
                return (← ppExpr Info.type).pretty
            let V ← liftTermElabM <| withOptions
              (fun O => O.setBool `pp.fullNames true |>.setBool `pp.universes true) do
                return (← ppExpr Value).pretty
            Definitions := Definitions.push <| Json.mkObj [
              ("name", toJson N.toString), ("type", toJson T), ("body", toJson V),
              ("type_expression", expr_json Info.type), ("value_expression", expr_json Value)]
            DefinitionText := DefinitionText ++ N.toString ++ " :\\n" ++ T ++ "\\n:=\\n" ++ V ++ "\\n\\n"
  IO.FS.writeFile (Out ++ "/public-declarations.json") ((Json.arr Results).compress ++ "\\n")
  IO.FS.writeFile (Out ++ "/public-types.txt") Readable
  IO.FS.writeFile (Out ++ "/shared-public-dependency-graph.json") ((Json.arr Nodes).compress ++ "\\n")
  IO.FS.writeFile (Out ++ "/local-definitions.json") ((Json.arr Definitions).compress ++ "\\n")
  IO.FS.writeFile (Out ++ "/local-definitions.txt") DefinitionText
'''
	Path(output / 'PublicEvidence.lean').write_text(Probe)
	return output / 'PublicEvidence.lean'

def main():
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument('output', type=Path)
	Parser.add_argument('--skip-negative-control', action='store_true')
	Args = Parser.parse_args()
	Output = Args.output.resolve()
	Output.mkdir(parents=True, exist_ok=False)
	Freeze = json.loads((BASE / 'freeze.json').read_text())
	Checks = {Name: digest(BASE / Name) == Hash for Name, Hash in Freeze['files'].items()}
	Checks.update({Name: digest(Name) == Hash for Name, Hash in Freeze['runtime_and_tools'].items()})
	write_json(Output / 'input-identity-checks.json', Checks)
	if not all(Checks.values()):
		raise RuntimeError('Frozen input/runtime/tool identity mismatch; see input-identity-checks.json')
	Config = json.loads((BASE / 'runtime-config.json').read_text())
	Env = os.environ.copy()
	Env['PYTHONDONTWRITEBYTECODE'] = '1'
	Env['LEAN_PATH'] = ';'.join(win(p) for p in Config['package_search_paths'])
	Env['LEAN_SRC_PATH'] = ''
	Env['WSLENV'] = ':'.join([v for v in Env.get('WSLENV', '').split(':') if v and v.split('/')[0] not in ('LEAN_PATH', 'LEAN_SRC_PATH')] + ['LEAN_PATH', 'LEAN_SRC_PATH'])
	Snapshot = BASE / 'snapshot'
	Verifier = Path(Config['verifier'])
	Lean = Config['lean']
	Common = [sys.executable, '-B', str(Verifier), '--project', str(Snapshot), '--direct', '--lean', Lean, '--lake', Config['lake'], '--strict-exit', '--build-timeout', '1800']
	Version = run(Output, '01-runtime-version', [Lean, '--version'], Env, Snapshot)
	assert Version['exit_code'] == 0
	assert 'version 4.31.0, x86_64-w64-windows-gnu' in (Output / 'command-logs/01-runtime-version.stdout.txt').read_text()
	Positive = run(Output, '02-maintained-positive', Common + ['--contract', str(BASE / 'positive-contract.json'), '--output', str(Output / 'positive')], Env, Snapshot)
	ManifestPath = Output / 'positive/run-manifest.json'
	Manifest = json.loads(ManifestPath.read_text())
	if Positive['exit_code'] != 0 or not Manifest['exact_root_passed']:
		write_json(Output / 'REPLAY_RESULT.json', dict(status='positive_failed', manifest=str(ManifestPath)))
		return 1
	Library = Path(Manifest['evidence']['run_directory']) / 'lib'
	ProbeEnv = dict(Env, LEAN_PATH=win(Library) + ';' + Env['LEAN_PATH'])
	Contract = json.loads((BASE / 'positive-contract.json').read_text())
	PositiveSource = Output / 'PositiveControl.lean'
	PositiveSource.write_text('import SL.AuditRound6\nexample : ' + Contract['expected_type'] + ' := SL.AuditRound6.local_algebra_root\n')
	Control = run(Output, '03-compiling-positive-control', [Lean, win(PositiveSource)], ProbeEnv, Snapshot)
	assert Control['exit_code'] == 0
	ProbeSource = public_probe(Output, Snapshot / 'SL/AuditRound6.lean')
	Inspection = run(Output, '04-public-inspection', [Lean, win(ProbeSource)], ProbeEnv, Snapshot)
	assert Inspection['exit_code'] == 0
	Resolution = run(Output, '05-root-resolution', [Lean, '--deps', win(PositiveSource)], ProbeEnv, Snapshot)
	assert Resolution['exit_code'] == 0
	ResolvedLines = (Output / 'command-logs/05-root-resolution.stdout.txt').read_text().splitlines()
	ExpectedObject = Library / 'SL/AuditRound6.olean'
	assert win(ExpectedObject).replace('\\', '/').lower() in [s.replace('\\', '/').lower() for s in ResolvedLines]
	write_json(Output / 'root-artifact.json', dict(source_sha256=digest(Snapshot / 'SL/AuditRound6.lean'), source_path=str(Snapshot / 'SL/AuditRound6.lean'), declaration=Contract['declaration'], olean=str(ExpectedObject), olean_sha256=digest(ExpectedObject), resolution_log='command-logs/05-root-resolution.stdout.txt'))
	Public = json.loads((Output / 'public-declarations.json').read_text())
	Allowed = {'propext', 'Classical.choice', 'Quot.sound'}
	assert all(set(d['transitive_axioms']) <= Allowed for d in Public)
	NegativeOK = None
	if not Args.skip_negative_control:
		Negative = run(Output, '06-maintained-wrong-expected-type', Common + ['--contract', str(BASE / 'wrong-expected-contract.json'), '--output', str(Output / 'negative')], Env, Snapshot)
		NegativeManifest = json.loads((Output / 'negative/run-manifest.json').read_text())
		NegativeOK = (Negative['exit_code'] == 1 and NegativeManifest['machine_verification_passed'] and not NegativeManifest['exact_root_passed'] and NegativeManifest['root_closure']['status'] == 'target_mismatch')
		assert NegativeOK
	After = {Name: digest(BASE / Name) == Hash for Name, Hash in Freeze['files'].items()}
	assert all(After.values())
	Summary = dict(status='passed', role='author_execution_not_independent_review', source_sha256=digest(Snapshot / 'SL/AuditRound6.lean'), declaration=Contract['declaration'], exact_root_passed=Manifest['exact_root_passed'], root_axioms=Manifest['target']['axioms'], public_declarations=len(Public), public_theorems=sum(d['kind']=='theorem' for d in Public), wrong_expected_type_rejected=NegativeOK, positive_control_exit_code=Control['exit_code'], inputs_unchanged=True, positive_manifest=str(ManifestPath), independent_review='not_performed')
	write_json(Output / 'REPLAY_RESULT.json', Summary)
	print(json.dumps(Summary, indent=2), flush=True)
	return 0

if __name__ == '__main__':
	sys.exit(main())
