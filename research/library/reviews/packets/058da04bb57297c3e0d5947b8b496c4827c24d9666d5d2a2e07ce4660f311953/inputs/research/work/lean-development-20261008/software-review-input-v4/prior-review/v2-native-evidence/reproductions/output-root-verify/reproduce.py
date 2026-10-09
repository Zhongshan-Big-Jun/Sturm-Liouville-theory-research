import json, tempfile, sys
from pathlib import Path
from unittest.mock import patch
scripts = Path(r'F:\LaTeX\BVE research\research\library\reviews\packets\5e98a16d78949e397e42b429a05b03ab0c475b54818140b9c03a55ab42483ede\inputs\research\work\lean-development-20261008\software-review-input-v2\source\plugins\lean-verify\scripts')
sys.path.insert(0,str(scripts))
import lean_develop as d
from lean_evidence import recheck_manifest
from lean_runtime import write_json, source_snapshot
with tempfile.TemporaryDirectory(prefix='review-v2-output-root-') as scratch:
    project = Path(scratch) / 'project'
    (project / 'Src').mkdir(parents=True)
    (project / 'lean-toolchain').write_text('leanprover/lean4:v4.31.0\n',encoding='utf-8')
    target = project / 'Src/Main.lean'
    target.write_text('theorem result (n : Nat) : n + 0 = n := Nat.add_zero n\n',encoding='utf-8')
    targets = project / 'targets.json'
    write_json(targets,{'targets':[{'id':'one','file':'Src/Main.lean','declaration':'result','expected_type':'∀ n : Nat, n + 0 = n'}]})
    args=d.make_parser().parse_args(['--project',str(project),'--output',str(project),'--lean',r'C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe','--lake',r'C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe','--direct','--timeout','60','verify','--targets',str(targets)])
    observed=[]
    def actual_recheck_then_edit_source(path):
        checked=recheck_manifest(path)
        observed.append(checked['exact_root_passed'])
        target.write_text('theorem result : False := by sorry\n',encoding='utf-8')
        return checked
    with patch('lean_develop.recheck_manifest',side_effect=actual_recheck_then_edit_source):
        result=d.verify_targets(args)
    post=recheck_manifest(result['targets'][0]['manifest'])
    print(json.dumps({'scope':'Actual Lean with supplied tool snapshots, disposable project and valid output equal to project root','source_file':'Src/Main.lean','batch_observed_sources':source_snapshot(project,[project]),'full_sources':source_snapshot(project),'observed_terminal_checks':observed,'returned_status':result['status'],'returned_exact_root_passed':result['exact_root_passed'],'batch_current':result['batch']['current'],'batch_changed':result['batch']['changed'],'post_recheck':post},ensure_ascii=True,indent=2),flush=True)