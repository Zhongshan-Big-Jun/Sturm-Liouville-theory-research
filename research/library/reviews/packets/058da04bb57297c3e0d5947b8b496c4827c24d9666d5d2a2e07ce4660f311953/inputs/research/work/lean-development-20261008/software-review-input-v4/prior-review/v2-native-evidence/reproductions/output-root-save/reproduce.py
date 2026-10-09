import json, tempfile, sys
from pathlib import Path
from unittest.mock import patch
scripts=Path(r'F:\LaTeX\BVE research\research\library\reviews\packets\5e98a16d78949e397e42b429a05b03ab0c475b54818140b9c03a55ab42483ede\inputs\research\work\lean-development-20261008\software-review-input-v2\source\plugins\lean-verify\scripts')
sys.path.insert(0,str(scripts))
from lean_develop import DevelopSession
from lean_runtime import LeanRuntime, sha256_file, source_snapshot
from verify_lean_project import verify_project, make_parser
with tempfile.TemporaryDirectory(prefix='review-v2-save-root-') as scratch:
    scratch=Path(scratch)
    project=scratch/'project'
    (project/'Pkg').mkdir(parents=True)
    (project/'lean-toolchain').write_text('leanprover/lean4:v4.31.0\n',encoding='utf-8')
    helper=project/'Pkg/Helper.lean'
    helper.write_text('def value : Nat := 0\n',encoding='utf-8')
    candidate=scratch/'Candidate.lean'
    candidate.write_text('import Pkg.Helper\ntheorem result : value = 0 := rfl\n',encoding='utf-8')
    lean=r'C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe'
    lake=r'C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe'
    runtime=LeanRuntime(project,project,lean,lake,True)
    session=DevelopSession(runtime,60,'cli')
    try:
        trial=session.trial('Main.lean',candidate)
        receipt=json.loads(Path(trial['receipt']).read_bytes())
        real_imports=session.import_identity
        events=[]
        def actual_import_query_then_edit(text):
            imports=real_imports(text)
            assert imports==receipt['import_artifacts']
            helper.write_text('def value : Nat := 1\n',encoding='utf-8')
            events.append({'imports_unchanged':True,'dependency_source_changed':True})
            return imports
        with patch.object(session,'import_identity',side_effect=actual_import_query_then_edit):
            saved=session.save(trial['receipt'])
        unchanged=all(sha256_file(item['path'])==item['sha256'] for item in receipt['import_artifacts'].values())
    finally:
        session.close()
    args=make_parser().parse_args(['--project',str(project),'--output',str(scratch/'verify-current'),'--lean',lean,'--lake',lake,'--direct','--target-file','Main.lean','--declaration','result','--expected-type','value = 0','--strict-exit'])
    current,_=verify_project(args)
    print(json.dumps({'scope':'Actual Lean using frozen tool snapshots, output equal to project root, disposable source fixture only','trial_status':trial['status'],'trial_input_hashes':receipt['input_hashes'],'events':events,'imported_artifacts_unchanged':unchanged,'save':saved,'destination_created':(project/'Main.lean').exists(),'actual_current_root_passed':current['exact_root_passed'],'actual_current_machine':current['machine'],'actual_current_build_status':current['build']['status']},ensure_ascii=True,indent=2),flush=True)