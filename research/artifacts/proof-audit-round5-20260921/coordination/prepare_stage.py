from pathlib import Path
import hashlib,json,subprocess
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round5-20260921');Base=json.loads((Out/'baseline.json').read_text())
Protection=json.loads((Out/'protection-result.json').read_text());assert Protection['status']=='PASS'
Paths=set(Protection['authorized_changed_tracked'])
for Prefix in ['reports/proof-audit-round5-20260921','research/artifacts/proof-audit-round5-20260921','research/library']:
	for P in (Root/Prefix).rglob('*'):
		if not P.is_file():continue
		Name=str(P.relative_to(Root))
		if Name in Base['tracked'] or Name in Base['untracked']:continue
		assert '__pycache__' not in P.parts and P.suffix!='.pyc',('unintended build cache',Name)
		assert not (Name.startswith('research/library/') and (P.name=='writer.lock' or P.name.startswith('.library-'))),('unfinished library writer',Name)
		assert P.stat().st_size<100_000_000,('oversized artifact',Name)
		Paths.add(Name)
Paths.update(['lean-proof/SL/AuditRound5.lean','docs/SL_cofinite_left_definite.tex','docs/SL_cofinite_left_definite.pdf','docs/.gitattributes','lean-proof/SL/.gitattributes','tools/.gitattributes'])
assert not Paths.intersection(Base['untracked'])
assert not Paths.intersection(Protection['original_dirty_preserved'])
Expected={Name:hashlib.sha256((Root/Name).read_bytes()).hexdigest() for Name in sorted(Paths)}
(Out/'stage-paths.json').write_text(json.dumps(sorted(Paths),indent=2)+'\n');(Out/'stage-expected-sha256.json').write_text(json.dumps(Expected,indent=2)+'\n')
Current=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=Root).decode().rstrip('\0').split('\0')
Unassigned=[N for N in Current if N and N not in Paths and N not in Base['untracked']]
assert not Unassigned,('unassigned newly created files require inspection',Unassigned)
print('Exact candidate paths',len(Paths))
