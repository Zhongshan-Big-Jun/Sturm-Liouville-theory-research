from pathlib import Path
import json
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_library as Library

Cards = json.loads((Out / 'cards.json').read_text())
Rows = [
	('band-selfconsistency-equivariance', '原矩阵与共轭矩阵的扇区及 H/E 分量', '第十二轮从保留的逐模 Sigma 表达核对出旧 sector_data 输出属于 Kp=SKS；当前无前缀 Ke/Ko/He/Ho/Ee/Eo 统一为原 K，对共轭块提供 Kp* 字段。负秩一 Sherman--Morrison 判据属于 KpOdd，等价于原 Ke。旧 H_o-E_o 的减号不能给 H_o+E_o 的正定下界，该一般充分性解释撤回。历史扫描仍保留原字节；本轮没有重新认证其单块标签、全参数定性或 G1。'),
	('green-half-inertia', '交叉 Green 式的对象与自身极点约化核', '第十二轮明确交叉 Green 式是 KpOdd=E Ke E；n=2、固定有限 R>1、对称五层驻点的解析稿逐项推导归一化、源项、投影与半区间因子。原 Ko 使用自身极点约化核并保留秩一项。有限点核惯性并不由无限维谱计数自动得到，旧全 R 定性义务仍开放。Lean 只覆盖有限维扇区代数及坐标/归一化桥接。'),
	('half-problem-regularized-green', '谱身份必须贯穿请求规模、去极点与求和', '第十二轮旧完整源码复现了独立网格漏模和请求 N/2N 时序号漂移。当前 DD/DN 按整数/半整数相位目标定位，绑定几何和边界的共享谱表维持每阶身份；去极点同时检查实际目标、序号、覆盖及全部分母。独立检验还发现极端浮点减法溢出会伪造有限零值，已改为明确拒绝并由新的无状态会话复验。数值误差半径、Richardson 和有限回归都不是区间认证。')]
Path = Out / 'annotations.json'
Done = json.loads(Path.read_text()) if Path.exists() else []
for Name, Locator, Text in Rows:
	Card = Cards[Name]
	if any(Note['tool_path'] == Card['location'] and Note['tool_sha256'] == Card['sha256'] and Note['locator'] == Locator for Note in Done):
		continue
	Note = Library.annotate(Root, Card['location'], Card['sha256'], 'agent:round12-20260926', 'correction-experience', Locator, Text + ' 精确推导与回执见 reports/proof-audit-round12-20260926/REPORT.md。')
	Done.append(Note)
	Path.write_text(json.dumps(Done, ensure_ascii=False, indent=2) + '\n')
(Out / 'annotated-cards.json').write_text(json.dumps(Cards, ensure_ascii=False, indent=2) + '\n')
print('Saved', len(Done), 'exact-version annotations', flush=True)
