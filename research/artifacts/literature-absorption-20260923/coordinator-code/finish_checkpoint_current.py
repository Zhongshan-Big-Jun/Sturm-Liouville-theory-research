from pathlib import Path
import json,sys,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/sl-literature-absorption-20260923')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts')
import research_state as S
inputs=['research_map.md','index/tools.json','literature/absorption-20260923/source-catalog.json','reports/literature-absorption-20260923/REPORT.md','research/artifacts/literature-absorption-20260923/integration/integration-check.json']
for group in ['domains','approximation','interfaces']:
    inputs.extend(x['location'] for x in json.loads((O/(group+'-cards.json')).read_text()))
for name in ['domains3','approximation','interfaces']:
    inputs.append('research/artifacts/literature-absorption-20260923/reviews/'+name+'/runtime/report.json')
inputs.append(json.loads((O/'bibliography-review2-dispatch.json').read_text())['bundle']+'/report.json')
result=S.checkpoint(R,Inputs=inputs)
path=Path(result['snapshot']);data=json.loads(path.read_text());paths=[path.relative_to(R).as_posix(),'.research-state/progress/'+data['progress_sha256']+'.md']
assert data['progress_sha256']==S.digest((R/data['progress']).read_bytes())
assert data['inputs']==S.input_snapshot(R,inputs)
assert S.digest(path.read_bytes())==result['sha256']
previous=json.loads((O/'checkpoint-files.json').read_text()) if (O/'checkpoint-files.json').exists() else []
paths=list(dict.fromkeys(previous+paths))
(O/'checkpoint-files.json').write_text(json.dumps(paths,indent=2)+'\n')
result.update(current_inputs_match=True,input_count=len(data['inputs']),progress_archive='.research-state/progress/'+data['progress_sha256']+'.md')
(O/'checkpoint-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
dest=R/'research/artifacts/literature-absorption-20260923/integration/checkpoint-current.json';raw=(O/'checkpoint-result.json').read_bytes()
if dest.exists():assert dest.read_bytes()==raw
else:dest.write_bytes(raw)
print('Checkpoint saved and verified:',result['sha256'],len(data['inputs']),'bound inputs.')
