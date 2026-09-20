from pathlib import Path
import hashlib,json,subprocess
Root=Path('/mnt/f/LaTeX/BVE research');Out=Path('/mnt/f/tools/math-audit-round4-20260921');Base=json.loads((Out/'baseline.json').read_text())
Allowed=set('''AGENTS.md
README.md
README_EN.md
docs/PROJECT_UNDERSTANDING.md
docs/research-guide.md
docs/SL_krein_c0_limit.tex
docs/SL_krein_c0_limit.pdf
docs/SL_third_order_recurrence_theory.tex
docs/SL_third_order_recurrence_theory.pdf
docs/SL_spectral_topics_summary.tex
docs/SL_spectral_topics_summary.pdf
research_map.md
scripts/README.md
scripts/d4_third_order_theory.py
lean-proof/STATUS.md
state/RESUME.md
state/AGENTS_SESSION_LOG.md
tools/README.md
tools/krein-sobolev-polynomials.md
tools/third-order-recurrence.md
tools/third-order-minimal-K1.md
tools/jump-stability.md
index/tools.json
research/library/card-bindings/catalog.json
research/library/corrections-journal.json'''.splitlines())
def digest(P):
	with P.open('rb') as F:return hashlib.file_digest(F,'sha256').hexdigest()
Changed=[];Kept=0
for Name,H in Base['tracked'].items():
	P=Root/Name;assert P.is_file(),('removed baseline file',Name)
	if digest(P)!=H:
		assert Name in Allowed,('changed outside assigned scope',Name)
		Changed.append(Name)
	else: Kept+=1
for Name,H in Base['untracked'].items():assert (Root/Name).is_file() and digest(Root/Name)==H,('changed preexisting untracked file',Name)
PriorLean=[N for N in Base['tracked'] if N.startswith('lean-proof/SL/') and N.endswith('.lean')]
assert len(PriorLean)==44
for N in PriorLean:assert digest(Root/N)==Base['tracked'][N]
CurrentHead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=Root,text=True).strip()
assert CurrentHead==Base['head']
Result={'status':'PASS','baseline_head':Base['head'],'original_tracked':len(Base['tracked']),'unchanged_original_tracked':Kept,'authorized_changed_tracked':Changed,'unchanged_original_untracked':len(Base['untracked']),'old_Lean_sources_preserved':len(PriorLean),'canonical_and_old_immutable_evidence':'Every original file outside explicit active-file allowlist retains baseline SHA256. Original library immutable snapshots, reviews, correction requests/events are included.','original_dirty_preserved':['.gitattributes','index/artifacts.json','index/runs.json','research/runs/R-20260831T020156Z-g1p-kpdet/workspace/AGENTS.md','state/activity.jsonl','state/current.json']}
(Out/'protection-result.json').write_text(json.dumps(Result,indent=2)+'\n')
print(json.dumps({K:V for K,V in Result.items() if K not in ['authorized_changed_tracked','canonical_and_old_immutable_evidence']}))
