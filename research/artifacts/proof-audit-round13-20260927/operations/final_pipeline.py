from pathlib import Path
import json,sys,runpy,shutil
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927');A=R/'research/artifacts/proof-audit-round13-20260927'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as V
D=json.loads((O/'certificate-v2-review-dispatch.json').read_text())
Completion=json.loads((O/'certificate-v2-review-completion.json').read_text())
Receipt=V.receive_review(R,D['bundle'],Completion)
(O/'certificate-v2-review-receipt.json').write_text(json.dumps(Receipt,ensure_ascii=False,indent=2)+'\n')
print('final certificate receive',Receipt['verdict'],flush=True)
if Receipt['verdict']!='APPROVED':raise RuntimeError('Certificate receipt did not pass current verification')
sys.argv=[str(O/'release_cards_v2.py')]
runpy.run_path(str(O/'release_cards_v2.py'),run_name='__main__')
runpy.run_path(str(O/'final_library.py'),run_name='__main__')
runpy.run_path(str(O/'finalize_docs.py'),run_name='__main__')
print('Final reception, library and active documentation completed',flush=True)
