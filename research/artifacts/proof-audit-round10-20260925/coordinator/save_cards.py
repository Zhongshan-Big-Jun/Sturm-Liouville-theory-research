from pathlib import Path
import sys,json
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round10-20260925');A='research/artifacts/proof-audit-round10-20260925'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
B=json.loads((O/'baseline.json').read_text());Coord='01a06f46-dd03-7c83-9267-32048412c359'
Done=json.loads((O/'cards.json').read_text()) if (O/'cards.json').exists() else {}
Names=['band-selfconsistency-equivariance','green-half-inertia','half-problem-regularized-green','second-variation-weighted-eigenvalues']
Common='''## 第十轮: 数值谱序号与反射种子的适用边界

共享旧求根器存在漏掉成对低频根的真实反例. 根残差、正性和递增性不能确定谱序号;
旧数值输出保留为历史, 未经针对性重算不能继续作为已核实低模态证据.
这不否定本卡独立解析恒等式, 也不由反例推断默认R=4的旧数据全错.
当前引擎按连续提升的第n*pi相位定位, 高精度和有限差分仍限定同一指标.
浮点括区不是严格区间证书; 共用同一枚举器的两种计算不构成独立谱计数.

接口反射为 R(x)=1-Jx. 保持扇区 d=(v-Jv)/2 满足Jd=-d,
破缺扇区 d=(v+Jv)/2 满足Jd=d. 旧asym赋值仅是-Jv, 撤回其纯扇区解释.
旧(a,-a[::-1])及相同形式的网格平面保持几何反射, 不能提供离开该子空间的证据.
新种子检查零投影、严格可行步长及参数转换后实际位移; 标签只指初值而非完整优化轨迹.

算法推导、程序范围和历史传播见[第十轮修订](../research/artifacts/proof-audit-round10-20260925/analytic-repair.md).
最终重算/审查范围见[第十轮报告](../reports/proof-audit-round10-20260925/REPORT.md).
本轮不证明Hessian定性、G1'、全R分支或全局唯一性; 下列保留内容按其各自审查范围阅读.

'''
for Name in Names:
	Loc='tools/'+Name+'.md'
	if Name in Done:
		if L.digest((R/Loc).read_bytes())!=Done[Name]['sha256']:raise RuntimeError('Saved card drift')
		continue
	Front,Body,_=L.read_metadata((R/Loc).read_bytes());Data=json.loads(json.dumps(Front,default=str))
	Head,Sep,Tail=Body.partition('\n')
	Content=Head+'\n\n'+Common+Tail if Head.startswith('# ') else Common+Body
	Sources=[dict(X) for X in Data.get('sources',[])]
	for X in Sources:
		if X.get('path')=='docs/SL_gap_nge2_symmetry_recon.tex':
			X.pop('sha256',None);X['locator']='Historical reconnaissance with round10 numerical-evidence and reflection-sector corrections'
	Sources.append(dict(path=A+'/analytic-repair.md',locator='S1-S4,R1-R2; independent analytic identities retain their prior scope'))
	Data.update(content=Content,updated='2026-09-25',sources=Sources,
		author_ids=sorted(set(Data.get('author_ids',[])+[Coord])),
		status='第十轮数值依据/反射扇区纠错; 精确版本经独立纠错回执后方可复用',
		evidence_status='ROUND10_SCOPED_REPAIR; CHECK_EXACT_CORRECTION_RECEIPT',
		summary=Data.get('summary','')+' 第十轮: 旧扫描不能认证谱序号, 旧asym非扇区投影; 新相位索引与可行扇区种子另审, 不据历史数值扩张解析结论.')
	Done[Name]=L.save_card(R,Data,Loc,B['tracked'][Loc]);(O/'cards.json').write_text(json.dumps(Done,ensure_ascii=False,indent=2)+'\n');print('Saved',Name,Done[Name]['sha256'],flush=True)
