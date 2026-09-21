"""Create a separate, honestly rehashed old-filter-only test mutant."""
from pathlib import Path
import hashlib, json, shutil

base = Path(__file__).resolve().parents[1]
dest = base / 'evidence/final-filter-only-mutation'
dest.mkdir(exist_ok=False)
manifest = json.loads((base / 'manifest.json').read_text())
for rel in (*manifest['package_files'], 'manifest.json', 'manifest.sha256'):
    path = dest / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(base / rel, path)
path = dest / 'regression/provenance.py'
source = path.read_text()
needle = '    module_files = collect_modules()\n'
replacement = ('    module_files = {name: path for name, path in collect_modules().items()\n'
               '                    if Path(path).resolve().is_relative_to(base.resolve())}\n')
if source.count(needle) != 1:
    raise RuntimeError('mutation anchor ambiguous')
path.write_text(source.replace(needle, replacement))
manifest['state'] = 'filter-only sensitivity mutant; not the final repaired input freeze'
manifest['package_files']['regression/provenance.py'] = dict(
    sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size)
p = dest / 'manifest.json'
p.write_text(json.dumps(manifest, indent=2)+'\n')
(dest / 'manifest.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  manifest.json\n')
(base / 'evidence/final-filter-only-mutation-description.json').write_text(json.dumps(dict(
    changed_only='regression/provenance.py observation-time Base filter; manifest truthfully rebound',
    before=needle, after=replacement, original_sha256=hashlib.sha256(source.encode()).hexdigest(),
    mutant_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), expected_suite_exit=1,
    expected_outside_child_exit=0, expected_missing_child_exit=86), indent=2)+'\n')
print(dest)
