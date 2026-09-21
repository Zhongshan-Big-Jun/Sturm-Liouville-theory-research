"""Freeze author sources only after development compilation succeeds."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess

BASE = Path(__file__).resolve().parent
PROJECT = Path('/mnt/f/LaTeX/BVE research')
ROOT = PROJECT / 'lean-proof'
BIN = Path('/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin')
PLUGIN = Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/lean-verify/2.0.0')

def digest(path):
	with Path(path).open('rb') as File:
		return hashlib.file_digest(File, 'sha256').hexdigest()

def write_json(path, value):
	Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def main():
	Snapshot = BASE / 'snapshot'
	Snapshot.mkdir(exist_ok=False)
	(Snapshot / 'SL').mkdir()
	for Name in ('SL/AuditRound5.lean', 'SL/AuditRound6.lean', 'lean-toolchain', 'lakefile.lean', 'lake-manifest.json'):
		shutil.copyfile(ROOT / Name, Snapshot / Name)
	Text = (Snapshot / 'SL/AuditRound6.lean').read_text()
	Expected = Text.split('theorem local_algebra_root :', 1)[1].split(' := by', 1)[0].strip()
	Names = {}
	for Module in ('AuditRound5', 'AuditRound6'):
		for Kind, Name in re.findall(r'^(?:noncomputable )?(def|theorem|lemma) (\w+)', (Snapshot / ('SL/' + Module + '.lean')).read_text(), re.M):
			Names[Name] = 'SL.' + Module + '.' + Name
	Names.update(X='Polynomial.X', C='Polynomial.C')
	Expected = re.sub(r'\b[A-Za-z_][A-Za-z0-9_]*\b', lambda Match: Names.get(Match[0], Match[0]), Expected)
	Positive = dict(file='SL/AuditRound6.lean', declaration='SL.AuditRound6.local_algebra_root', expected_type=Expected, universes=[])
	assert Expected.count('= 15360') == 1
	write_json(BASE / 'positive-contract.json', Positive)
	write_json(BASE / 'wrong-expected-contract.json', dict(Positive, expected_type=Expected.replace('= 15360', '= 15361')))
	Inputs = BASE / 'candidate-inputs'
	Inputs.mkdir()
	for Name in ('projection_and_moment_repairs.md', 'fractional_window_completion.md'):
		shutil.copyfile(PROJECT / 'research/artifacts/proof-audit-round6-20260921/submitted' / Name, Inputs / Name)
	Manifest = json.loads((ROOT / 'lake-manifest.json').read_text())
	Search = []
	PackageIdentities = []
	for Package in Manifest['packages']:
		Repo = ROOT / '.lake/packages' / Package['name']
		Build = Repo / '.lake/build/lib/lean'
		if Build.is_dir():
			Search.append(str(Build))
		Actual = subprocess.run(['git', '-C', str(Repo), 'rev-parse', 'HEAD'], capture_output=True, text=True)
		PackageIdentities.append(dict(name=Package['name'], pinned_rev=Package['rev'], actual_head=Actual.stdout.strip(), git_exit_code=Actual.returncode, build_directory_present=Build.is_dir()))
		assert Actual.returncode == 0 and Actual.stdout.strip() == Package['rev']
	write_json(BASE / 'runtime-config.json', dict(lean=str(BIN / 'lean.exe'), lake=str(BIN / 'lake.exe'), verifier=str(PLUGIN / 'scripts/verify_lean_project.py'), package_search_paths=Search, package_identities=PackageIdentities, runtime_kind='Windows PE invoked from WSL', old_project_objects_in_search_path=False))
	RuntimeTools = [BIN / 'lean.exe', BIN / 'lake.exe', *sorted(BIN.glob('*.dll'))]
	RuntimeTools += [PLUGIN / 'scripts' / n for n in ('verify_lean_project.py', 'lean_runtime.py', 'lean_evidence.py', 'LeanVerifyProbe.lean.template', 'lake_build_guard.py', 'run_manifest.schema.json')]
	Files = [*Snapshot.rglob('*.lean'), Snapshot / 'lean-toolchain', Snapshot / 'lake-manifest.json', *Inputs.glob('*.md')]
	Files += [BASE / n for n in ('CONTRACT.md', 'positive-contract.json', 'wrong-expected-contract.json', 'runtime-config.json', 'replay.py', 'prepare_package.py')]
	Frozen = dict(files={str(p.relative_to(BASE)): digest(p) for p in sorted(set(Files))}, runtime_and_tools={str(p): digest(p) for p in RuntimeTools}, original_source=str(ROOT / 'SL/AuditRound6.lean'), original_source_sha256=digest(ROOT / 'SL/AuditRound6.lean'), role='author_not_independent_reviewer')
	write_json(BASE / 'freeze.json', Frozen)
	print(json.dumps(dict(source_sha256=Frozen['original_source_sha256'], frozen_files=len(Frozen['files']), runtime_tools=len(Frozen['runtime_and_tools'])), indent=2))

if __name__ == '__main__':
	main()
