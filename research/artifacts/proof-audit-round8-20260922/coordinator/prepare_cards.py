from pathlib import Path
import sys,json,hashlib,datetime
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round8-20260922');A='research/artifacts/proof-audit-round8-20260922'
sys.path.insert(0,str(R/'_xsoc1_work/plugins/manage-math-research-program/skills/manage-math-research-program/scripts'))
import research_library as L
B=json.loads((O/'baseline.json').read_text())
Authors=['01a06f46-dd03-7c83-9267-32048412c359','01a0c4c7-52f9-71e3-bc0b-ef3e30abb78e','01a0c4c7-595b-7a40-9740-ec99ceb721a6','01a0c4cc-45bc-77e1-8ce3-f79b2f3d31aa']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
done=json.loads((O/'cards.json').read_text()) if (O/'cards.json').exists() else {}
specs=[
('cot-series-certificate','cot-card.md','余切余项的部分分式与精确有理常数','0<z<pi 的正确 Laurent 幂次与局部一致收敛; 0<z<=pi/8 时余项<=Cz*z, Cz<0.337; 新精确证书替代旧 libm 区间.',[],['0<z<pi; uniform convergence only on compact subintervals','Cz bound only for 0<z<=pi/8']),
('delta-bracketing','delta-card.md','对称阱族的相位分支与括号','全域使用无极点匹配; 奇相位>pi/2和delta括号仅在R>=1500,w>=2应用. arctan上界趋于pi/2而不发散.',['cot-series-certificate'],['Dirichlet symmetric [R,1,R], R>1, 0<u<1/2','Delta brackets require R>=1500,w=u*sqrt(R)>=2']),
('lemma-A-doubleprime','lemma-card.md',"大 w 区域的 INF 比较引理 A''",'R>=1500,w>=2 时 G>Dbar+ell/(R*u^3); 初等差量 d1>4alpha,d2<3alpha. 不覆盖薄层, 不依赖旧浮点证书.',['delta-bracketing','cot-series-certificate'],['Dirichlet symmetric [R,1,R], R>=1500,0<u<1/2,w>=2']),
('inf-limit-comparison','inf-card.md','对称阱族 INF 极限与连续相位比较','对称阱族 R*m_R->M, 误差O(1/R), R*eta_R->0近极小化子趋于u*. 连续相位覆盖全部薄层; T1不依赖T3数值. 固定内部u首项C(u)/R.',['lemma-A-doubleprime','delta-bracketing'],['Dirichlet symmetric [R,1,R],0<u<1/2','Global lower bound for R>=1500; fixed-u expansions are uniform only on interior compact intervals'])]
for name,file,title,summary,deps,conditions in specs:
	loc='tools/'+name+'.md'
	if name in done:
		if sha(R/loc)!=done[name]['sha256']: raise RuntimeError('Saved card changed')
		continue
	if sha(R/loc)!=B['tracked'][loc]: raise RuntimeError('Unrecorded card change '+loc)
	front,_,_=L.read_metadata((R/loc).read_bytes())
	data=json.loads(json.dumps(front,default=lambda x:x.isoformat() if isinstance(x,(datetime.date,datetime.datetime)) else str(x)))
	data.update(title=title,summary=summary,updated='2026-09-22',author_ids=Authors,content=(O/file).read_text(),conditions=conditions,status='第八轮范围明确的修订; 检索复用由当前精确版本纠错回执控制',evidence_status='ROUND8_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT',dependencies=[dict(location=done[n]['location'],sha256=done[n]['sha256']) for n in deps],sources=[dict(path='docs/SL_gap_n1_inf_limit_proof.tex',locator='Round8 corrected phases, A doubleprime, continuous sliver, T1/T2/T3 and fixed-u rate')],resources=[dict(path=A+'/certificate/certificate.py',kind='exact-computation',locator='Fraction/Machin/Taylor scalar certificate, no full spectral formalization'),dict(path=A+'/certificate/results.json',kind='author-execution',locator='Exact scalar outputs; independent review receipt required')])
	if name=='cot-series-certificate': data['sources'].append(dict(source_id='bb729c250eb36b380f0ab4f7be158562340ba3b2bf505887681952e3aab405e6',url='https://dlmf.nist.gov/4.22.E3',locator='Equation4.22.3 actually retrieved formula and pole exclusions'))
	done[name]=L.save_card(R,data,loc,B['tracked'][loc]);save(O/'cards.json',done);print('SAVED',name,done[name]['sha256'],flush=True)
