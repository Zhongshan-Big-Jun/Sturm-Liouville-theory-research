from pathlib import Path
import json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round11-20260926')
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
Result=L.make_index(R,ReadmePath='tools/README.md')
(O/'index-result.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({K:V for K,V in Result.items() if K!='issues'}),flush=True)
if Result['verdict']!='INDEXED' or Result['indexed']!=90 or Result['blocked']!=1:raise RuntimeError('Unexpected final index state')
