from run import *
import re

BLIND = BASE / 'formal-only'
BLIND.mkdir(exist_ok=False)
SOURCE = (PROJECT / 'AuditRound10.lean').read_text()
REMOVED = '-- BEGIN GENERATED ROOT\n'
assert SOURCE.count(REMOVED) == 1
NEUTRAL = SOURCE.replace(REMOVED, '')
assert not re.search(r'/\-|^\s*--', NEUTRAL, re.M)
(BLIND / 'AuditRound10.lean').write_text(NEUTRAL)
for Name in ['lean-toolchain', 'lakefile.toml', 'lake-manifest.json']:
	shutil.copyfile(PROJECT / Name, BLIND / Name)
shutil.copyfile(BASE / 'formal-declarations-full.json', BLIND / 'declarations-full.json')
shutil.copyfile(BASE / 'commands/print-main-01/stdout.log', BLIND / 'print-and-axioms.log')
shutil.copyfile(PROJECT / 'PrintAuditRound10.lean', BLIND / 'PrintAuditRound10.lean')
Env = environment()
Packages = json.loads((PROJECT / 'lake-manifest.json').read_text())['packages']
Environment = {
	'lean_executable':str(LEAN), 'lean_executable_sha256':digest(LEAN),
	'lean_version':(BASE / 'commands/runtime-version/stdout.log').read_text().strip(),
	'lean_path':Env['LEAN_PATH'], 'packages':Packages,
	'lean_toolchain_sha256':digest(PROJECT / 'lean-toolchain'),
	'lake_manifest_sha256':digest(PROJECT / 'lake-manifest.json')}
write_json(BLIND / 'environment.json', Environment)
Object = BASE / 'objects/blind-source-01/AuditRound10.olean'
Object.parent.mkdir(parents=True, exist_ok=False)
Result = run('blind-source-01', [LEAN, '-R', win(BLIND), '-o', win(Object), win(BLIND / 'AuditRound10.lean')],
	Cwd=BLIND, Inputs=[Path(__file__), BLIND / 'AuditRound10.lean', BLIND / 'lean-toolchain'])
if Result['exit_code'] != 0:
	raise RuntimeError('blind copy compilation failed')
write_json(BASE / 'blind-transform.json', {
	'input':str(PROJECT / 'AuditRound10.lean'), 'input_sha256':digest(PROJECT / 'AuditRound10.lean'),
	'output':str(BLIND / 'AuditRound10.lean'), 'output_sha256':digest(BLIND / 'AuditRound10.lean'),
	'transformation':'Remove only the single generation marker comment; retain imports, options, definitions, theorem names, statements and proofs verbatim.',
	'compilation_record':'commands/blind-source-01/command.json',
	'readback_review':'not performed by this author'})
write_json(BLIND / 'packet.json', {
	'root_declaration':'AuditRound10.root',
	'declarations':json.loads((BASE / 'declaration-names.json').read_text())['main'],
	'files':{str(P.relative_to(BLIND)):{'sha256':digest(P),'bytes':P.stat().st_size} for P in sorted(BLIND.iterdir()) if P.is_file()}})
print('Frozen formal-only files and compiled the comment-stripped source.')
