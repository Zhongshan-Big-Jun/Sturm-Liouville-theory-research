from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927');A='research/artifacts/proof-audit-round13-20260927/'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_corrections as C
import research_review as V
Old=json.loads((O/'certificate-review-spec.json').read_text());Rows=[x for x in json.loads((O/'revisions.json').read_text()) if x['name'] in ['rational-envelope-certificates','true-curve-region-decomposition']]
Inputs={};Claims={};Authors=set(Old['author_ids'])
for Row in Rows:
 Req=C.review_requirements(R,Row['revision'])
 (O/(Row['revision']+'-requirements.json')).write_text(json.dumps(Req,ensure_ascii=False,indent=2)+'\n')
 for x in Req['inputs']:Inputs[x['path']]=x
 for x in Req['claims']:Claims[x['id']]=x
 Authors.update(Req['author_ids'])
for x in Old['inputs']:
 if x['role']!='correction-review-input':Inputs.setdefault(x['path'],dict(path=x['path'],role=x['role']))
for p in ['certificate-repair-v2.md','certificate-review-receipt.json','certificate-checks-v2/results.json','certificate-checks-v2/normal.log','certificate-checks-v2/optimized.log']:
 Inputs[A+p]=dict(path=A+p,role='current-repair-or-explicit-prior-findings')
Claim=dict(next(x for x in Old['claims'] if x['id']=='R13-exact-certificate'))
Claim['statement']+=' Also independently resolve first isolated review findings F1-F3: same-interface positive and genuine rejection controls (not argparse errors), all active true-curve dependencies, Q interior versus closed image with correctly justified boundary inequalities. The prior reviewer is evidence of findings, not approval. Write own files only under /mnt/f/tools/math-audit-round13-20260927/certificate-reviewer-v2 (superseding the earlier output-directory instruction).'
Claims[Claim['id']]=Claim
Spec=dict(kind='mathematics',author_ids=sorted(Authors),inputs=list(Inputs.values()),claims=list(Claims.values()))
(O/'certificate-v2-review-spec.json').write_text(json.dumps(Spec,ensure_ascii=False,indent=2)+'\n')
Result=V.create_packet(R,Spec)
(O/'certificate-v2-review-packet.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print('packet',Result['packet_sha256'],len(Inputs),len(Claims),flush=True)
