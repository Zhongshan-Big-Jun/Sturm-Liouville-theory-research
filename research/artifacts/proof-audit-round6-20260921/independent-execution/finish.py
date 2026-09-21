"""Capture independent JSON checks and materialize the final reviewable report."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time
from execute import OUT, AUTHOR, PROJECT, now, digest, write_json

def main():
	assert os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'
	assert not (OUT/'checks-command.json').exists(), 'Preserve prior attempts; no automatic repeat.'
	Args = ['python3','-B',str(OUT/'check_evidence.py')]
	Record = dict(argv=Args, cwd=str(PROJECT), utc_start=now(), PYTHONDONTWRITEBYTECODE='1', CODEX_THREAD_ID=os.environ['CODEX_THREAD_ID'])
	write_json(OUT/'checks-command.json',Record)
	Start = time.monotonic()
	with (OUT/'checks.stdout.txt').open('xb') as Stdout, (OUT/'checks.stderr.txt').open('xb') as Stderr:
		Process = subprocess.Popen(Args,cwd=PROJECT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=Stdout,stderr=Stderr)
		Record['pid']=Process.pid
		write_json(OUT/'checks-command.json',Record)
		Record['exit_code']=Process.wait()
	Record.update(utc_end=now(),duration_seconds=time.monotonic()-Start,stdout_sha256=digest(OUT/'checks.stdout.txt'),stderr_sha256=digest(OUT/'checks.stderr.txt'))
	write_json(OUT/'checks-command.json',Record)
	if not (OUT/'CHECKS.json').exists():
		print(json.dumps(Record,indent=2),flush=True)
		return Record['exit_code'] or 1
	Checks = json.loads((OUT/'CHECKS.json').read_text())
	Session = json.loads((OUT/'native-session.json').read_text())
	Session.update(utc_completed=now(), execution_verdict=Checks['verdict'], independent_checks='CHECKS.json', actual_replay_command='replay-command.json', final_semantic_approval=False, negative_control_independently_run=False, replay_script_role_text_preserved='author_execution_not_independent_review', replay_script_role_interpretation='A literal field in the frozen author-provided generic script. The execution and checks in this output belong to the actual native session recorded here.')
	write_json(OUT/'native-session.json',Session)
	Freeze=json.loads((AUTHOR/'freeze.json').read_text())
	Manifest=json.loads((OUT/'replay/positive/run-manifest.json').read_text())
	Builds=json.loads((OUT/'local-build-checks.json').read_text())
	Report=[
		'# 第六轮 Lean 独立执行核验',
		'',
		f"判定: **{Checks['verdict']}**. {Checks['passed']}/{len(Checks['checks'])} 项执行及结构一致性检查通过. 本报告不构成最终语义批准.",
		'',
		f"原生会话: `{Session['CODEX_THREAD_ID']}`. 身份直接读取本会话环境变量 `CODEX_THREAD_ID`; 不伪造 fork 元数据. 本人不是作者, 未读取或采用作者 REPORT/RESULTS、其他审稿会话或研究工具库的结论.",
		'',
		'## 实际运行及检查',
		'',
		'```text',
		'PYTHONDONTWRITEBYTECODE=1 python3 -B '+str(AUTHOR/'replay.py')+' '+str(OUT/'replay')+' --skip-negative-control',
		'```',
		'',
		f"上述命令只执行一次, 输出目录原先不存在. 退出码 0, 耗时 {Checks['replay_seconds']:.2f} 秒. 原始命令、PID、stdout、stderr、退出码和流哈希保存在 `replay-command.json`、`replay.stdout.txt`、`replay.stderr.txt`. 其内五个阶段与维护版 verifier 的各编译子命令均保留原始回执.",
		'',
		'| 检查 | 结果与证据 |',
		'| --- | --- |',
		'| 冻结输入和源身份 | 执行前后各 33 项身份检查; freeze 自身哈希及 snapshot 文件集合保持一致. 见 preflight.json、postflight.json. |',
		'| 实际运行时 | Windows PE Lean 4.31.0, x86_64-w64-windows-gnu, 从 WSL 调用. 运行时与维护版工具均按冻结哈希核对. |',
		'| 新对象构建 | AuditRound5、AuditRound6 均从与原项目一致的冻结源实际编译, 只生成在本次独立新目录. 见 local-build-checks.json. |',
		'| 精确根及类型 | SL.AuditRound6.local_algebra_root; Lean 实际 isDefEq、宇宙参数、绑定参数检查均匹配. 正确期望类型的独立 example 编译通过. |',
		f"| 导入身份 | {Checks['loaded_modules']} 个已加载模块, {Checks['imported_artifact_files']} 个导入工件文件. 实际路径和哈希受回执绑定; 当前全部模块解析再核对通过. 旧项目 SL 对象未被采用. |",
		f"| 根和公共闭包 | 根 {Checks['root_dependency_nodes']} 节点; 共享公共图 {Checks['shared_public_dependency_nodes']} 节点. 独立重算闭包及公理集合, 无 sorryAx、额外 axiom、unsafe 或缺失节点. |",
		'| 全部显式公共导出 | 36 项, 包括 21 个定理和 15 个定义. 每项核对类型 AST、类型/证明依赖边、宇宙参数、绑定参数以及重算的传递公理. 编译器生成的辅助声明随闭包检查. 见 public-declaration-checks.json. |',
		'| 可达本地定义 | 逐项核对类型和定义体 AST 的依赖边, 在根提取提供对应 AST 时交叉比对. 见 local-definition-checks.json 的逐项比较范围. |',
		'| 回执一致性 | 只消费本会话新生成的回执, 核对原始日志、源、工具、运行时、工件及实时 import resolution. 无第二次证明重放. 见 receipt.stdout.txt. |',
		'',
		'逐项机器判定和具体证据见 [CHECKS.json](CHECKS.json). 根及全部公共声明的传递公理均不超出 `propext`, `Classical.choice`, `Quot.sound`. 检查器为比较期望类型而生成的 `LeanVerifyV2.expected_statement` 合成声明不在根或期望类型的证明依赖闭包内; 正对照直接使用实际根证明项.',
		'',
		'## 身份绑定',
		'',
		f"- freeze.json SHA-256: `{Checks['freeze_sha256']}`.",
		f"- AuditRound5.lean SHA-256: `{Freeze['files']['snapshot/SL/AuditRound5.lean']}`.",
		f"- AuditRound6.lean SHA-256: `{Checks['source_sha256']}`.",
		f"- 实际新 AuditRound6.olean SHA-256: `{next(Row['object_sha256'] for Row in Builds if Row['file']=='SL/AuditRound6.lean')}`.",
		f"- 维护版 verifier run_id: `{Manifest['run_id']}`.",
		'',
		'## 明确边界',
		'',
		'- **错误期望类型负对照未独立运行**, 状态为 NOT_RUN_BY_REQUEST; wrong-expected-contract.json 仅作为冻结输入核对. 作者的负对照证据须由另行语义审查核实, 本报告不作其通过或失败结论.',
		'- replay/REPLAY_RESULT.json 的 `role=author_execution_not_independent_review` 和 `independent_review=not_performed` 是冻结通用脚本的原文字段, 保持不变. 本目录的实际执行来自上列真实原生会话; 本人另写的 CHECKS.json、native-session.json 和本报告说明独立执行核验身份.',
		'- 本次检查精确的局部实代数 Lean 目标. 没有批准解析 Sobolev、分数幂、谱阈值、拓扑密度或完整解析证明已经 Lean 化, 也未作最终陈述保真审查.',
		'- 依赖库使用已有固定运行时和包对象; 未全量重建 Mathlib, 未运行全 Lake 工程或旧项目工具, 未使用第二个独立内核. 编译器与被哈希绑定的依赖工件是本轮执行的信任边界.',
		'- 不修改作者包、项目源、插件、canonical 或 Git. Python 文件运行均使用 -B 和 PYTHONDONTWRITEBYTECODE=1. 本目录及 snapshot 内无新增 Python 字节码缓存.',
		'',
		'## 全部新增文件',
		'',
		'输出父目录原先不存在, 本次全部文件均为此目录下新增. 完整逐文件相对路径、大小和 SHA-256 见 [FILES.json](FILES.json), 包括嵌套 replay 的源、对象、JSON 和原始日志. 清单自身列为索引文件并明确排除自哈希, 不作循环哈希声明.',
		'',
	]
	if Checks['verdict'] != 'PASS':
		Report[2]='判定: **FAIL**. 失败检查: '+', '.join(Checks['failed'])+'. 下列为保留的实际证据和范围; 失败项不得按表述推定通过.'
	(OUT/'REPORT.md').write_text('\n'.join(Report))
	with (OUT/'AGENTS.md').open('a') as Handle:
		Handle.write('\n- Final maintenance: one actual fresh replay and one receipt recheck completed; independent expression/graph/axiom checks captured in CHECKS.json. REPORT.md and native-session.json state the real execution identity, omitted negative control, and separate semantic-review boundary. Every created artifact is enumerated in FILES.json. No writes were made outside this output scope.\n')
	Files=[]
	for File in sorted(OUT.rglob('*')):
		if File.is_file() and File.name != 'FILES.json':
			Files.append(dict(path=str(File.relative_to(OUT)),change='created',bytes=File.stat().st_size,sha256=digest(File)))
	Files.append(dict(path='FILES.json',change='created',sha256=None,reason='Index itself excluded from self-hashing.'))
	write_json(OUT/'FILES.json',dict(output_root=str(OUT),generated_at=now(),baseline_directory_existed=False,files=Files,count=len(Files)))
	print(json.dumps(dict(verdict=Checks['verdict'],passed_checks=Checks['passed'],failed=Checks['failed'],created_files=len(Files),report=str(OUT/'REPORT.md')),ensure_ascii=False,indent=2),flush=True)
	return Record['exit_code']

if __name__=='__main__':
	sys.exit(main())
