from pathlib import Path
import gzip
import hashlib
import json
import shutil

Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Source = Out / 'formal-export2'
Artifact = Path('/mnt/f/LaTeX/BVE research/research/artifacts/proof-audit-round12-20260926')
Records = json.loads((Source / 'declarations.json').read_text())
Old = json.loads((Out / 'formal-author/declarations.json').read_text())
if len(Records) != 59 or [Row['name'] for Row in Records] != [Row['name'] for Row in Old]:
	raise RuntimeError('Export declaration set differs')
for Row in Records:
	for Key in ['type_explicit', 'type_readable', 'definition_value_explicit']:
		if Row.get(Key) and ('⋯' in Row[Key] or '...' in Row[Key]):
			raise RuntimeError('Export still contains elision: ' + Row['name'] + ' ' + Key)
for Before, After in zip(Old, Records):
	for Key in ['name', 'kind', 'universes', 'binder_kinds', 'transitive_axioms', 'unsafe', 'type_dependencies', 'body_dependencies']:
		if Before[Key] != After[Key]:
			raise RuntimeError('Export metadata changed: ' + Key)
Parts = []
for Row in Records:
	Parts.extend([Row['name'], 'kind: ' + Row['kind'], 'universes: ' + json.dumps(Row['universes']), 'binder_kinds: ' + json.dumps(Row['binder_kinds']), 'actual_type (explicit/universes):', Row['type_readable'], 'actual_type (pp.all):', Row['type_explicit'], 'transitive_axioms: ' + json.dumps(Row['transitive_axioms']), 'unsafe: ' + str(Row['unsafe'])])
	if Row['definition_value_explicit'] is not None:
		Parts.extend(['definition_value (pp.all):', Row['definition_value_explicit']])
	Parts.append('\n')
(Source / 'declarations.txt').write_text('\n'.join(Parts))
Blind = Source / 'blind'
Blind.mkdir(exist_ok=True)
for Name in ['AuditRound12.lean', 'lean-toolchain']:
	shutil.copyfile(Out / 'formal-author/blind' / Name, Blind / Name)
for Name in ['declarations.json', 'declarations.txt']:
	shutil.copyfile(Source / Name, Blind / Name)
Files = {Path.name: hashlib.sha256(Path.read_bytes()).hexdigest() for Path in sorted(Blind.iterdir()) if Path.is_file() and Path.name != 'manifest.json'}
(Blind / 'manifest.json').write_text(json.dumps(dict(files=Files), indent=2) + '\n')
Note = json.loads((Source / 'coordinator-note.json').read_text())
Note.update(status='COMPLETE_EXPORT_PENDING_NEW_INDEPENDENT_READBACK', declaration_count=59, no_elisions_in_types_or_definition_bodies=True, unchanged_metadata_fields=['kind', 'universes', 'binder_kinds', 'transitive_axioms', 'unsafe', 'type_dependencies', 'body_dependencies'], changed_export_names=[After['name'] for Before, After in zip(Old, Records) if Before != After])
(Source / 'coordinator-note.json').write_text(json.dumps(Note, indent=2) + '\n')
Rows = []
for Path in sorted(Source.rglob('*')):
	if not Path.is_file() or any(Part in ['objects', 'tmp', '__pycache__'] for Part in Path.relative_to(Source).parts):
		continue
	Data = Path.read_bytes()
	Name = 'formal-export2/' + Path.relative_to(Source).as_posix()
	Row = dict(path=Name, sha256=hashlib.sha256(Data).hexdigest(), bytes=len(Data))
	if len(Data) > 2000000:
		Row.update(original_path=Path.relative_to(Source).as_posix(), original_sha256=Row['sha256'], original_bytes=len(Data), encoding='gzip')
		Data = gzip.compress(Data, mtime=0)
		Row.update(path=Name + '.gz', sha256=hashlib.sha256(Data).hexdigest(), bytes=len(Data))
	Target = Artifact / Row['path']
	Target.parent.mkdir(parents=True, exist_ok=True)
	if Target.exists() and Target.read_bytes() != Data:
		raise RuntimeError('Archive drift')
	Target.write_bytes(Data)
	Rows.append(Row)
(Artifact / 'formal-export2-archive-manifest.json').write_text(json.dumps(dict(files=Rows, scope='Coordinator export repair; unchanged theorem source; actual fresh compile and all failed attempts retained. Not independent acceptance.'), indent=2) + '\n')
print('Complete export', len(Records), 'declarations; changed renderings', Note['changed_export_names'], flush=True)
