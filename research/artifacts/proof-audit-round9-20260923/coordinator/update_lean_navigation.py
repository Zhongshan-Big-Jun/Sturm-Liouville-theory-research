from pathlib import Path
import json
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923')
P=R/'lean-proof/STATUS.md';B=P.read_bytes();NL='\r\n' if B.count(b'\r\n')==B.count(b'\n') else '\n';S=B.decode().replace('\r\n','\n')
T='''## 2026-09-23 第九轮局部形式化

新增[AuditRound9.lean](SL/AuditRound9.lean): 全维有限实向量的积分法向量投影代数、零法向量与幂等性、线性泛函归一化的核修正、真实2×2归一化矩阵的J共轭与任意n乘积反射、从状态相似变换到物理F的频率因子及内部零点等价. 15合取根包含25个具名定理和13个定义/缩写, 机器导出59项声明(含辅助项). 作者当前实跑通过, 三类错误目标均拒收; 新盲读与独立语义/执行验收进行中, 最终以[第九轮报告](../reports/proof-audit-round9-20260923/REPORT.md)为准.

使用固定Windows PE Lean4.31.0及原Mathlib依赖, 根闭包只含propext、Classical.choice、Quot.sound. 未形式化从积分到有限法向量的解析识别、本征函数可微性、无限谱展开/Green核、ODE传输矩阵来源、2n根计数、候选极限或全局极值; 可选的块宽加权投影未在新文件覆盖. 49份旧SL源码和原环境保留字节, 未执行全工程Lake build.

旧ReflectionSymmetry.lean证明的是固定omega参数下的矩阵恒等式. 对文稿中omega(y)=y/(s*t)的物理函数, 严格对称的是omega*F; F(pi-y)=y/(pi-y)*F(y). 本轮新增文件补上该代数桥接, 旧文件保持历史原字节.

'''
S=S.replace('## 2026-09-22 第八轮局部形式化',T+'## 2026-09-22 第八轮局部形式化',1)
S=S.replace('源中 y=ω√R·t 相位归一化与谱论连接未形式化','源中变化ω的物理F不能据此宣称值对称; 第九轮AuditRound9补齐归一化/物理频率因子代数桥接, 谱论连接仍未形式化')
S=S.replace('部分: ReflectionSymmetry (J-共轭反射对称 F_n(pi-y)=F_n(y), 固定 ω 参数); 平衡定理的 2n-根计数/闭式仍依赖数值证据, 未形式化','部分: ReflectionSymmetry限固定ω; AuditRound9证明归一化/物理F的代数桥接. 第九轮已有全部n的解析2n根计数及候选单调极限证明, 这些谱论结论尚未形式化')
P.write_bytes(S.replace('\n',NL).encode())
P=R/'README_EN.md';S=P.read_text();S=S.replace('Fixed-n ratio optima and remaining monotonicity questions. Later STRICT results already cover the 2n root count; see','Fixed-n global ratio optima and properties of the actual supremum sequence. Root count, monotonicity and the limit of the prescribed balanced candidates are proved; see');P.write_text(S)
C=json.loads((O/'CURRENT.json').read_text());C.update(stage='review-f1-repaired-software-and-formal-verification',software_author='COMPLETED_CLOSED',lean_author='COMPLETED_CLOSED',math_review1='CHANGES_REQUIRED_CLOSED: signed mass convergence missing from card; fixed in new version',math_reviewer='01a0cc08-556e-7cd0-bb4b-751a35d9c749',renewal_review='APPROVED_CLOSED; 22 exact releases in progress',software_reviewer='01a0cc01-fdb9-7b52-92f0-36d95f648e01',pending='math review2, software review, formal blind/semantic/replay, current library gate, exact publication')
(O/'CURRENT.json').write_text(json.dumps(C,ensure_ascii=False,indent=2)+'\n')
with (R/'state/AGENTS_SESSION_LOG.md').open('ab') as F:F.write('''

第九轮进展: 首次数学隔离检验退回二阶变分卡一句过强表述, 明确有界总变差还需有符号质量收敛才得到集中极限. 保留旧卡与CHANGES_REQUIRED, 仅修订该句/摘要并交新会话. 十二张数学未变卡的22项旧义务已通过另一新会话续检, 正逐事项续发; 不删除旧失效回执. 软件已集成并交新执行检验, Lean作者已完成15合取局部根/真实编译与三类负对照, 尚待盲读和独立语义执行. 两份PDF、研究图、项目理解和阅读入口更新, 所有全局O1/O2/G1边界保留. 详见本轮证据、报告草稿及外部CURRENT.json.
'''.encode())
print('Lean scope and continuity updated.')
