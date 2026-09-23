from pathlib import Path
import sys,json,datetime
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');A='research/artifacts/proof-audit-round9-20260923'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
B=json.loads((O/'baseline.json').read_text());Coord='01a06f46-dd03-7c83-9267-32048412c359'
Done=json.loads((O/'cards.json').read_text()) if (O/'cards.json').exists() else {}
Specs=[('second-variation-weighted-eigenvalues','second-variation-card.md','加权特征值二阶变分与归一化、切向及接口路径规范','正密度线性路径的二阶谱公式; 归一化导数含核分量. 分块切向使用块积分, 窄脉冲Green极限有限; 移动接口另有有限加速度项. 不证明切空间负定或G1定号.','V1-V4',[]),('secular-chebyshev-jacobi-rootcount','rootcount-card.md','平衡交替配置的归一化世俗函数与2n简单根','物理F的反射有y/(pi-y)因子; omega*F才严格对称. 对R>1,n>=1的规定平衡交替配置, 归一化Chebyshev/Jacobi表示证明2n个简单根. 不证明全局最优.','B1-B2',[]),('bloch-band','bloch-card.md','规定平衡候选序列的严格单调与带边极限','固定R>1的规定平衡候选c_n严格递减至((pi-phi)/phi)^2, phi=arccos((sqrt(R)-1)/(sqrt(R)+1)). 嵌套Jacobi最小谱证明全部n; Lambda_n全局最优及O1/O2仍开放.','B2',['secular-chebyshev-jacobi-rootcount'])]
for Name,File,Title,Summary,Locator,Deps in Specs:
	Loc='tools/'+Name+'.md'
	if Name in Done:
		if L.digest((R/Loc).read_bytes())!=Done[Name]['sha256']:raise RuntimeError('Saved card drift')
		continue
	Front,_,_=L.read_metadata((R/Loc).read_bytes());Data=json.loads(json.dumps(Front,default=str))
	Data.update(title=Title,summary=Summary,updated='2026-09-23',author_ids=[Coord],content=(O/File).read_text(),status='第九轮范围明确的解析修订; 当前版本复用由独立纠错回执控制',evidence_status='ROUND9_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT',dependencies=[dict(location=Done[d]['location'],sha256=Done[d]['sha256']) for d in Deps],sources=[dict(path=A+'/analytic-repair.md',locator=Locator)])
	if Name!='second-variation-weighted-eigenvalues':Data['sources'].append(dict(path='docs/SL_fixed_n_supremum.tex',locator='Normalized reflection, Jacobi root count and candidate limit'))
	Done[Name]=L.save_card(R,Data,Loc,B['tracked'][Loc]);(O/'cards.json').write_text(json.dumps(Done,ensure_ascii=False,indent=2)+'\n');print('Saved',Name,Done[Name]['sha256'],flush=True)
