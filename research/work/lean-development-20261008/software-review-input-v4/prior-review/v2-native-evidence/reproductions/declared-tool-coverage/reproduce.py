import json, tempfile, shutil, sys
from pathlib import Path
from unittest.mock import patch
packet_path = Path(r'F:\LaTeX\BVE research\research\library\reviews\packets\5e98a16d78949e397e42b429a05b03ab0c475b54818140b9c03a55ab42483ede\packet.json')
packet = json.loads(packet_path.read_bytes())
source_prefix = 'research/work/lean-development-20261008/software-review-input-v2/source/'
with tempfile.TemporaryDirectory(prefix='review-v2-tools-') as scratch:
    scratch = Path(scratch)
    source_root = scratch / 'source'
    for name, entry in packet['inputs'].items():
        if name.startswith(source_prefix):
            target = source_root / name[len(source_prefix):]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(packet_path.parent / entry['snapshot'], target)
    scripts = source_root / 'plugins/lean-verify/scripts'
    sys.path.insert(0, str(scripts))
    import lean_develop as d
    from lean_evidence import recheck_manifest
    from lean_runtime import sha256_file, write_json
    project, output = scratch / 'project', scratch / 'output'
    project.mkdir()
    (project / 'lean-toolchain').write_text('leanprover/lean4:v4.31.0\n', encoding='utf-8')
    (project / 'First.lean').write_text('theorem first (n : Nat) : n + 0 = n := Nat.add_zero n\n', encoding='utf-8')
    (project / 'Second.lean').write_text('theorem second (n : Nat) : n + 0 = n := Nat.add_zero n\n', encoding='utf-8')
    targets = project / 'targets.json'
    write_json(targets, {'targets':[{'id':'first','file':'First.lean','declaration':'first','expected_type':'∀ n : Nat, n + 0 = n'},{'id':'second','file':'Second.lean','declaration':'second','expected_type':'∀ n : Nat, n + 0 = n'}]})
    lean = r'C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
    lake = r'C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe'
    args = d.make_parser().parse_args(['--project',str(project),'--output',str(output),'--lean',lean,'--lake',lake,'--direct','--timeout','60','verify','--targets',str(targets)])
    tool_file = scripts / 'lake_build_guard.py'
    old_tool_hash = sha256_file(tool_file)
    observed = []
    def actual_recheck_then_change_tool(path):
        checked = recheck_manifest(path)
        observed.append(checked['exact_root_passed'])
        if len(observed) == 2:
            tool_file.write_bytes(tool_file.read_bytes() + b'\n# Independent review: changed verifier dependency after terminal checks.\n')
        return checked
    with patch('lean_develop.recheck_manifest', side_effect=actual_recheck_then_change_tool):
        result = d.verify_targets(args)
    post = [recheck_manifest(row['manifest']) for row in result['targets']]
    print(json.dumps({'scope':'Independent actual Lean run on copies of only supplied source snapshots; only disposable verifier tool changed','changed_tool':'lake_build_guard.py','before_tool_sha256':old_tool_hash,'after_tool_sha256':sha256_file(tool_file),'tool_list':list(d.tool_hashes()),'observed_terminal_checks':observed,'returned_status':result['status'],'returned_exact_root_passed':result['exact_root_passed'],'row_passed':[row['exact_root_passed'] for row in result['targets']],'batch':result['batch'],'post_rechecks':post}, ensure_ascii=True, indent=2), flush=True)