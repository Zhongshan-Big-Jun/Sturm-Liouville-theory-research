from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round11-20260926');A='research/artifacts/proof-audit-round11-20260926'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts')
import research_state as S
Inputs=['research_map.md','docs/PROJECT_UNDERSTANDING.md','literature/maps/FRONTIER.md','index/tools.json','reports/proof-audit-round11-20260926/REPORT.md','docs/SL_cofinite_all_orders.tex','docs/SL_cofinite_all_orders.pdf','scripts/_gapn2_jacobian_probe.py','scripts/_gapn2_o3_scan.py','scripts/_gapn2_second_variation_probe.py','lean-proof/SL/AuditRound11.lean',A+'/jacobian-repair.md',A+'/cofinite-author/cofinite-all-orders.md',A+'/caller-inventory.json',A+'/review-summary.json',A+'/integration/library-verification.json']
Inputs.extend(X['location'] for X in json.loads((O/'annotated-cards.json').read_text()).values())
Inputs.extend(X['target']['location'] for X in json.loads((O/'renewals.json').read_text()))
Inputs.extend(X['bundle']+'/report.json' for X in json.loads((R/A/'review-summary.json').read_text())['reviews'])
Result=S.checkpoint(R,Inputs=Inputs);P=Path(Result['snapshot']);D=json.loads(P.read_text())
if D['inputs']!=S.input_snapshot(R,Inputs) or S.digest(P.read_bytes())!=Result['sha256']:raise RuntimeError('Checkpoint mismatch')
if D['progress_sha256']!=S.digest((R/D['progress']).read_bytes()):raise RuntimeError('Progress mismatch')
Paths=[P.relative_to(R).as_posix(),'.research-state/progress/'+D['progress_sha256']+'.md']
(O/'checkpoint-files.json').write_text(json.dumps(Paths,indent=2)+'\n');Result.update(input_count=len(D['inputs']),current_inputs_match=True,progress_archive=Paths[1])
(O/'checkpoint-result.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n');(R/A/'integration/checkpoint.json').write_bytes((O/'checkpoint-result.json').read_bytes())
print('Current checkpoint verified',Result['sha256'],len(D['inputs']),'inputs',flush=True)
