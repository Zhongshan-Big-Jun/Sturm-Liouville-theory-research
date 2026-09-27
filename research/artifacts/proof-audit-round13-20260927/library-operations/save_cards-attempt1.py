from pathlib import Path
import hashlib,json,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round13-20260927');A='research/artifacts/proof-audit-round13-20260927/'
sys.path.insert(0,'/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as L
Author='01a06f46-dd03-7c83-9267-32048412c359'
Contents={}
Contents['rational-envelope-certificates']='''# 有理包络证书：精确端点与完整命题

当前入口为 misc/e1_certgen.py → misc/e1_cert_ledger.json 及其 .status.json → misc/e1_cert_receive.py / misc/e1_cert_tables.py。本轮重算保留 57 条完整命题，不以函数正性替代非零阈值。TA_B2>=27/10、TC>=19/10 与严格 tau<13/10 都进入实际谓词。

sin/cos 点包络使用有界导数 Taylor 余项；区间使用完整偏移值域，包含内部极值，宽偏移使用 [-1,1]。atan 单调端点算法在跨 1 时也终止。支持域、平方根和导数条件详见本轮解析修订。精确有理端点、Taylor 中心、斜率、M、M*w、最终界和裕量存入台账。下端向下，上端向上；半径向上、裕量向下；不得把窄区间显示成漏真值的单点。

生成器只有全部事实验收才发布 PASS；失败、异常和不可判定均退出非零。接收器核对本次状态、精确台账哈希、当前源文件哈希、完整合同与有理见证。它不构成独立超越函数引擎或 Lean 证明。解析包络论证、有理数运算、浮点交叉检验及形式化认证必须区分。

B1(.85) 的当前显示区间为 [0.009851718322,0.009851718323]，仍大于 1/200。本轮未降低原阈值，也未撤回 O3a 相应命题。全部实际命令与负对照见本轮报告；使用前仍须检查函数域和命题合同。

旧 rigid_dec.py、zz_verify_e1_dec.py、旧 Decimal 重放 audit_o3a_cert_replay.py 及其 PASS 记录只保留历史身份，不提供当前可信入口。随机包含性自检不能排除本轮明确反例。旧卡字节在工具库版本历史中保留。当前依据见 [证书修订](../research/artifacts/proof-audit-round13-20260927/certificate-repair.md) 与活动 O3a 正文附录。
'''
Helly=(O/'status-author/helly-compactness-candidate.md').read_text();Helly=Helly.replace('Author candidate for R13-11. The coordinator owns card versioning, source bindings and independent release. This text replaces the unconditional attainment claim; it does not withdraw measurable-box existence.','R13-11 correction. Reuse requires the exact current correction receipt. Selection and attainment are distinct; measurable-box existence is preserved.');Contents['helly-compactness']=Helly
Front,Body,_=L.read_metadata((R/'tools/true-curve-region-decomposition.md').read_bytes())
old='''  由区间引擎认证 (`misc/rigid_dec.py` + `misc/zz_verify_e1_dec.py` +
  `misc/e1_facts_ledger.json`, 哈希 L7/L8/L9), 不再需要 67 叶盒证书'''
new='''  由当前 [[rational-envelope-certificates]] 的解析包络与精确有理证据支持；第十三轮重新验收 57 条完整台账命题，包含原非零阈值。
  `misc/e1_certgen.py` / `misc/e1_cert_receive.py` 是当前生成与接收入口；旧 Decimal 三件套和 L7/L8/L9 仅保留历史身份。此链不再需要 67 叶盒证书'''
if old not in Body:raise RuntimeError('true-curve anchor missing')
Contents['true-curve-region-decomposition']=Body.replace(old,new)+'''\n第十三轮修复的是原语包络、证书显示与完整谓词/失败传播；保留 T1/T2 原解析目标。旧浮点扫描不据此升级为区间认证，未扩展全局 G1/M3/KP。\n'''
Contents['interval-dec-directed-rounding']='''# 旧 Decimal 区间引擎：退役与复用阻断

本卡是失效提示，不是可靠引擎推荐。原 misc/rigid_dec.py 的 sqrt、取负和三角内部极值存在明确漏包反例；旧 zz_verify_e1_dec.py 的失败事实仍可能成功退出。本轮保留原代码、原台账、4800 次随机自检记录及原卡版本，不能将它们重写成新的通过记录。

默认可信复用已撤回。需要历史复现时必须显式标注旧版本、不可信包络与失败退出码缺陷；若以后确需 Decimal 路线，应建立新版本并独立验证，不能凭提高精度或追加随机样本恢复信任。当前主证明已退役此引擎；这里的错误不直接反证当前主定理。

当前替代入口是 [[rational-envelope-certificates]] 的精确 Fraction 包络与完整接收合同。反例和原始证据见 [第十三轮原包](../research/artifacts/proof-audit-round13-20260927/submitted/REPORT.md) R13-03/05/06。旧独立 Decimal 重放脚本也只作历史材料，不作为当前证书接收器。
'''
Contents['bang-bang']='''# bang-bang 原理：存在性、变分符号和零集分别检验

先证明实际容许类中的极值存在。Helly 选择只给子列；推出取到极值还需容许类在所用拓扑下闭合，以及目标的相应半连续性，见 [[helly-compactness]]。本项目完整可测盒 0<a<=rho<=A 的固定模态谱目标采用弱星紧性与谱连续性；这不适用于附加连续端值条件而不闭的类。

若盒上极大值 rho* 的一阶变分是 integral Phi(x)*delta_rho(x) dx，且允许盒内的局部方向变分，则 Phi>0 处 rho*=A，Phi<0 处 rho*=a 几乎处处。极小值的符号相反。仅当零集 Phi=0 的测度为零等非退化条件另行得到时，才可断言极值为两值。零泛函就是所有密度都极值的简单边界，不能由“仿射/单调”直接断言每个极值两值。

两值不自动等于有限跳点阶梯；有限开关数还需要 SL 结构/振荡论证。特征值比值并非密度的仿射泛函，其变分公式及开关结构须分别核对 [[keller-variational]] 和具体项目证明。未在本轮重新认证所有 Keller/MW 文献定理或所有极值结构。

本轮仅修正原 Helly 存在性桥与相应使用前提。完整可测盒的依据在 docs/SL_gap_nge2_finite_reduction_proof.tex 的 lem:wscompact、lem:wscont、cor:attain；连续单调端值类不取到下确界的反例保留在 Helly 卡及原审计包中。
'''
Front,Body,_=L.read_metadata((R/'tools/jump-stability.md').read_bytes());Contents['jump-stability']=Body+'''\n2026-09-27：活动稳定性稿的引言已对齐 A1/A12，局部 H3 运输、递推证明及其假设保持原范围。本文数学主体未因证书/谱助手缺陷撤回；当前整文件来源哈希已更新，旧回执保留并由本轮独立复核续接。\n'''
Meta={
 'rational-envelope-certificates':dict(summary='57 条完整有理证书；精确端点、正确值域、非零阈值及失败传播。解析包络与接收器均须核对，不是 Lean 证明。',sources=[dict(path='docs/SL_gap_n1_O3a_phase_rigidity_proof.tex',locator='Current rational envelope, certificate tables and explicit trust boundary'),dict(path=A+'certificate-repair.md',locator='R13-01..06 proof and evidence scope')]),
 'helly-compactness':dict(summary='统一有界且统一TV的 Helly 子列；取到极值另需拓扑、容许类闭性及相应半连续性。保留连续单调端值类不取到反例，可测盒存在性独立成立。',sources=[dict(path=A+'submitted/analytic_notes.md',locator='R13-11 nonattainment example'),dict(path='docs/SL_gap_nge2_finite_reduction_proof.tex',locator='lem:wscompact, lem:wscont, cor:attain')]),
 'true-curve-region-decomposition':dict(summary='保留真曲线 T1/T2 原解析分解范围；T2 单变量事实使用修订后的精确有理证书。旧 Decimal 和历史 PASS 标签不作当前可信入口。',sources=[dict(path='docs/SL_gap_n1_O3a_phase_rigidity_proof.tex',locator='Original T1/T2 scope with corrected current certificates')]),
 'interval-dec-directed-rounding':dict(summary='WITHDRAWN：旧 Decimal 的 sqrt、负号、三角内部极值漏包及失败退出码反例已确认，仅供历史复现；当前入口是有理包络证书。',evidence_status='WITHDRAWN_RETIRED_ENGINE',status='已退役；默认可信复用撤回',sources=[dict(path=A+'submitted/REPORT.md',locator='R13-03/05/06')]),
 'bang-bang':dict(summary='存在性先检验实际闭类和谱连续性；一阶变分符号决定盒端点，零集与有限开关数需另证。Helly 选择不能单独推出存在性。',sources=[dict(path='docs/SL_gap_nge2_finite_reduction_proof.tex',locator='Measurable-box existence; switching structure separate'),dict(path='tools/helly-compactness.md',locator='Corrected hypotheses and nonattainment boundary')]),
 'jump-stability':dict(summary='保留一般递推下界、实际解判据、B=0模型及全指标扰动前提；活动引言已对齐 A1/A12，局部 s=3 证明未扩张。',sources=[dict(path='docs/SL_stability_moment_jump.tex',locator='Original local proof and corrected current introductory scope'),dict(path='docs/SL_fractional_left_definite.tex',locator='Separate fixed-c full member window')])
}
Results={}
for Name,Body in Contents.items():
 PathValue='tools/'+Name+'.md';Raw=(R/PathValue).read_bytes();Backup=R/A/'before'/PathValue;Backup.parent.mkdir(parents=True,exist_ok=True)
 if not Backup.exists():Backup.write_bytes(Raw)
 Data=dict(content=Body,updated='2026-09-27',author_ids=[Author,'01a0e2aa-7f3b-7c71-87a6-16e984423a97'],status='第十三轮修订；按精确版本回执检索',evidence_status='ROUND13_SCOPED_CORRECTION_REQUIRES_CURRENT_RECEIPT',**{k:v for k,v in Meta[Name].items() if k not in ['status','evidence_status']})
 Data.update({k:v for k,v in Meta[Name].items() if k in ['status','evidence_status']})
 Results[Name]=L.save_card(R,Data,PathValue,hashlib.sha256(Raw).hexdigest())
 (O/'cards.json').write_text(json.dumps(Results,ensure_ascii=False,indent=2)+'\n');print('Saved',Name,flush=True)
