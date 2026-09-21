"""Own, separately rebound old-filter mutant; original packet remains untouched."""
import difflib
import json
import sys
from run_owned import OWN, PACKET, create_copy, package_hashes, sha, capture

package = create_copy('mutant-filter-only')
source = package / 'regression/provenance.py'
before = source.read_text()
old = "            if getattr(module, '__file__', None)}"
new = "            if getattr(module, '__file__', None) and Path(module.__file__).resolve().is_relative_to(Path(__file__).resolve().parents[1])}"
if before.count(old) != 1:
    raise RuntimeError('mutation target is not unique')
source.write_text(before.replace(old, new))
manifest_path = package / 'manifest.json'
manifest = json.loads(manifest_path.read_text())
manifest['package_files']['regression/provenance.py'] = dict(sha256=sha(source), bytes=source.stat().st_size)
manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
(package/'manifest.sha256').write_text(sha(manifest_path)+'  manifest.json\n')
diff = ''.join(difflib.unified_diff(before.splitlines(True), source.read_text().splitlines(True), fromfile='frozen/regression/provenance.py', tofile='MUTANT/regression/provenance.py'))
(OWN/'filter-only-mutation.diff').write_text(diff)
changed = {p:dict(frozen_sha256=v, mutant_sha256=sha(package/p)) for p,v in PACKET['files'].items() if sha(package/p)!=v}
if set(changed) != {'regression/provenance.py','manifest.json','manifest.sha256'}:
    raise RuntimeError('unexpected mutation scope')
(OWN/'filter-only-mutation.json').write_text(json.dumps(dict(role='reviewer sensitivity experiment, NOT submitted candidate', restoration='old filter at collection time only; required binding checks and controls retained', changed=changed, all_other_49_inputs_identical=True, rebound_input_sha256=package_hashes(package)),indent=2)+'\n')
for mode in ('normal','optimized'):
    flags = ['-B'] + (['-O'] if mode=='optimized' else [])
    capture('mutant-verify-'+mode,package,[sys.executable,*flags,str(package/'regression/verify_package.py')],0,package)
    capture('mutant-replay-'+mode,package,[sys.executable,*flags,str(package/'regression/replay.py'),'--controls-only','--label','independent-filter-only-mutant-'+mode],1,package)
