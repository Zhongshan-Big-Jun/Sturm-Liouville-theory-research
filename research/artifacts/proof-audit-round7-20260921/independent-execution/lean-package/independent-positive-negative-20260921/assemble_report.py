#!/usr/bin/env python3
"""Assemble a small execution report from completed independent checks only."""
from pathlib import Path
import json, os, subprocess
from executor import BASE,RUN,pointer,digest,save,stamp

def read(name): return json.loads((RUN/name).read_text())
def main():
    checks=read('independent-checks.json');lean=read('lean-crosscheck.json');numeric=read('numerical-crosscheck.json');commands=read('command-inventory.json');runtime=read('runtime-stability.json');pre=read('preflight.json');ident=read('final-input-identity.json')
    if 'returncode' not in read('executor-logs/supplemental-wrong-target-verifier.json'):
        raise RuntimeError('supplemental verifier has not finished')
    excluded={'independent-execution.json','README.md','evidence-index.json','SHA256SUMS','SHA256SUMS.sha256','delivery-integrity.json'}
    files=[]
    for p in sorted(RUN.rglob('*')):
        if p.is_file() and str(p.relative_to(RUN)) not in excluded and not p.is_relative_to(RUN/'tmp'):
            files.append({'relative_path':str(p.relative_to(RUN)),**pointer(p)})
    save(RUN/'evidence-index.json',{'scope':'Files produced in this new run; raw manifests and large inventories preserved byte-for-byte. Input/runtime SHA pointers are in preflight.json and runtime inventories. Reports and this index are bound separately by SHA256SUMS. Temporary directory excluded.','file_count':len(files),'total_bytes':sum(p['bytes'] for p in files),'files':files})
    links={name:pointer(RUN/name) for name in ('preflight.json','runner-review.json','runtime-before.json','runtime-after-imports.json','runtime-stability.json','final-input-identity.json','executor-logs/lean-replay.json','executor-logs/lean-replay.stderr.log','replay/logs/04-all-declarations.stdout.txt','replay/Inspection.lean','replay/positive/run-manifest.json','supplemental-negative/run-manifest.json','all-module-declarations.json','all-module-declarations.execution.json','independent-root-artifact.json','lean-crosscheck.json','numerical-crosscheck.json','numeric-observation-normal.json','numeric-observation-optimized.json','command-inventory.json','independent-checks.json','evidence-index.json')}
    programs=[pointer(p) for p in sorted(RUN.glob('*.py'))]+[pointer(p) for p in sorted(RUN.glob('*.lean'))]
    result={
      'schema':'independent-execution/1','generated_at_utc':stamp(),'status':'INCOMPLETE','execution_role':'independent executor of the supplied isolated packet; no final semantic review verdict issued','run_directory':str(RUN),
      'blockers':[
       {'id':'LEAN_RUNNER_INSPECTION_SYNTAX','returncode':1,'location':str(RUN/'replay/Inspection.lean')+':75:8','actual_error':'unsupported pattern in syntax match: Type','effect':'Supplied replay stops at step 4 of 7; public-declarations.json, original resolution and original negative steps are not completed. The input replay.py is unchanged.','evidence_keys':['executor-logs/lean-replay.json','executor-logs/lean-replay.stderr.log','replay/logs/04-all-declarations.stdout.txt','replay/Inspection.lean']},
       {'id':'NUMERICAL_MISSING_MANIFEST','path':str(BASE/'numerical/inputs/manifest.json'),'actual_error':'FileNotFoundError','effect':'normal and -O each log 24 PASS and 1 FAIL, then payload construction fails again; no original normal/optimized outputs.json and no successful execution-summary.json. No inputs fabricated.','evidence_keys':['numerical-crosscheck.json','numeric-observation-normal.json','numeric-observation-optimized.json']}
      ],
      'verified_execution_observations':{
       'source_recompiled':True,'candidate_source_recompilations':commands['candidate_source_recompilations'],'positive_exact_target':lean['manifests']['positive']['exact_root_passed'],'positive_target_root_status':lean['manifests']['positive']['root_status'],'new_olean_import_verified':'Independent import/findOLean and supplemental --deps both resolve to the fresh positive object, with matching SHA256.',
       'source_named_public_declarations':lean['source_declarations'],'source_named_theorems':lean['source_theorems'],'source_named_definitions':lean['source_definitions'],'all_module_constants_exported':lean['all_module_constants'],'all_definition_bodies_exported':lean['public_definition_bodies_exported'],'transitive_axiom_union':lean['axiom_union'],
       'wrong_target':{'verifier_exit':read('executor-logs/supplemental-wrong-target-verifier.json')['returncode'],'machine_compilation_passed':True,'exact_root_passed':lean['manifests']['negative']['exact_root_passed'],'root_status':lean['manifests']['negative']['root_status'],'native_lean_exit':read('executor-logs/supplemental-wrong-target-native.json')['returncode'],'actual_and_requested':'-4*pi versus -6*pi'},
       'wrong_mirror_factor':{'exit':read('executor-logs/supplemental-wrong-mirror-factor.json')['returncode'],'failure':'Type mismatch: factor 2 versus requested factor 1'},
       'numeric':numeric['direct_modes'],'numeric_24_completed_details_identical':numeric['captured_detail_comparison']['same_completed_24_groups'],'numeric_negative_controls':numeric['negative_controls'],
       'important_caveat':'Successful supplemental observations do not convert either original runner failure into success; total packet execution remains INCOMPLETE.'},
      'counts':{
       'frozen_input_hashes_checked_before_and_after':len(pre['checks']),'prehashed_runtime_artifacts':runtime['baseline_artifact_count'],'posthashed_actual_external_import_artifacts':runtime['post_run_sha256_rechecked_loaded_artifacts'],'positive_loaded_modules':lean['manifests']['positive']['loaded_modules'],'negative_loaded_modules':lean['manifests']['negative']['loaded_modules'],'actual_lean_lake_executable_processes':commands['total_lean_lake_processes'],'original_lean_runner_steps_executed':lean['runner_steps'],'original_lean_runner_steps_succeeded':sum(c==0 for c in lean['step_exit_codes'].values()),'original_lean_runner_steps_failed':sum(c!=0 for c in lean['step_exit_codes'].values()),'original_lean_runner_steps_planned':7,'candidate_recompilations':commands['candidate_source_recompilations'],'verifier_helper_compilations':commands['inspection_helper_recompilations'],'numeric_checks_script_executions':numeric['check_script_executions'],'direct_group_invocations':50,'direct_group_passes':48,'direct_group_failures':2,'additional_observer_group_invocations':50,'additional_observer_group_passes':48,'additional_observer_group_failures':2,'independent_evidence_consistency_checks':{'total':checks['total'],'passed':checks['passed'],'failed':checks['failed']}},
      'frozen_inputs_unchanged':ident['all_match'] and ident['packet_unchanged'],'loaded_external_artifacts_unchanged':runtime['all_loaded_sha256_match'],'read_write_scope':{'input_packet':pre['packet'],'read':'PACKET, freeze-listed Lean files/run scripts, the two numerical scripts, permitted existing execution runtimes and listed external file hashes, and outputs created by this execution. No prior author output/README, project AGENTS, memory, other task history, or manuscript parsing.','writes':str(BASE),'original_inputs_modified':False,'source_project_or_external_runtime_modified_by_intended_commands':False,'commit_performed':False,'limitation':'Not a system-wide filesystem syscall audit; external runtime byte and metadata checks cover the stated inventories.'},
      'trust_boundaries':[
       'Lean 4.31.0 compiler/kernel, existing imported Lean/mathlib compiled artifacts, system libraries, WSL/Windows/Linux, filesystem and hardware are trusted. No independent second kernel or full mathlib rebuild.',
       '4365 loaded modules in verifier include the candidate and its inspection helper. External .olean/.server/.private artifacts are hash-bound and compared before/after, not rebuilt from dependency sources.',
       'Unused prehashed runtime objects were restatted at the end; byte hashes were rechecked for actual imported artifacts. Metadata-preserving edits to unused objects are outside the end-of-run byte check.',
       'Exact target means the supplied Lean expected_type in the recorded environment. It does not establish fidelity to an unreviewed manuscript or a global mathematical theorem.',
       'The FH interface formulas are explicit scalar hypotheses. Spectral differentiability/general Feynman-Hellmann hypotheses were not formalized here. No infinite-dimensional Volterra estimates, uniform Taylor remainder, min-max proof or general spectral limit was certified in Lean.',
       'The numerical scripts use SymPy and mpmath (90 decimal digits). Symbolic and finite high-precision checks are not interval certificates or proofs of infinite-dimensional/general operator claims. Python executable is frozen; library versions and observed module file hashes are recorded, but the full OS/native/bytecode loading chain is not independently attested.',
       'The input integrity group is incomplete because its manifest is absent. Original runners did not complete; this report leaves both failures visible.',
       'No final semantic review verdict is issued. Supplemental scripts are executor-authored and their scope is observed compilation, rejection, export, hashing and comparison.'
      ],
      'unformalized':['spectral differentiability and general FH premises','infinite-dimensional Volterra estimates','uniform Taylor remainders','min-max and full variational arguments','general spectral limit/branch classification'],
      'semantic_review_verdict':'not_issued','executor_audit_attempts':{'first':pointer(RUN/'executor-logs/independent-evidence-audit.json'),'first_exit_code':read('executor-logs/independent-evidence-audit.json')['returncode'],'final':pointer(RUN/'executor-logs/independent-evidence-audit-fast.json'),'final_exit_code':read('executor-logs/independent-evidence-audit-fast.json')['returncode'],'reason':pointer(RUN/'audit-retry-reason.json')},'programs':programs,'evidence':links,'large_evidence_policy':'Large generated manifests and inventories remain at their original paths and bytes. Read this small report or README for retrieval.'
    }
    if checks['failed']:
        result['additional_evidence_check_failures']=[x for x in checks['checks'] if not x['passed']]
    save(RUN/'independent-execution.json',result)
    report=pointer(RUN/'independent-execution.json')
    def ref(name):
        item=links[name]
        return f"`{name}` — SHA256 `{item['sha256']}`"
    text=f'''# 独立执行摘要：INCOMPLETE

完整新运行目录：`{RUN}`

本报告记录隔离执行及证据核对，不给出最终数学语义 review verdict。

## 两个实际阻断

1. 原 Lean replay 返回 **1**。第 2 步 exact target 与第 3 步直接正对照成功；第 4 步生成的 `replay/Inspection.lean:75:8` 使用 `let Type`，编译器报 `unsupported pattern in syntax match`。原 replay 只执行了 4/7 步，其 `public-declarations.json` 未生成，后续负对照未由原 replay 执行。
2. 原数值 runner 返回 **1**。`numerical/inputs/manifest.json` 缺失，且不在 PACKET 数值输入清单中。normal 与补跑的 `-O` 都是 **24 PASS + 1 FAIL / 25 组**；汇总构造又因同一缺失输入失败，未产生原定结果 JSON。没有补造 manifest 或替换输入。

## 实际完成的补充核查

| 项目 | 本次实际结果 |
|---|---|
| 冻结身份 | {len(pre['checks'])} 项 SHA256 前后匹配；PACKET 本身也未变 |
| 候选源码重新编译 | {commands['candidate_source_recompilations']} 次，有独立进程与新产物生成观察 |
| 正 exact target | `local_algebra_root`，`closed`，expected_type matched；直接正对照通过 |
| 实际 import | 独立 Lean import/findOLean 与补跑 `--deps` 都指向本次新 `.olean` |
| 全量声明导出 | 27 个源声明＝20 定理＋7 定义；环境共 32 项（额外 5 个自动生成项）；类型、传递公理及 7 个定义体实际导出 |
| 传递公理 | 仅 `propext`、`Classical.choice`、`Quot.sound` |
| 错误 target | 补跑原 wrong-target contract：verifier 返回 1，`target_mismatch`；原生 Lean 也报告实际结论 `W₂(1/2)=−4π` 与要求 `W₂(1/2)=−6π` 的类型不匹配 |
| 错误镜像因子 | 原 `WrongMirrorFactor.lean` 返回 1；Type mismatch 明确为系数 2 对系数 1 |
| 数值 normal / -O | 各 24/25；额外观察运行在原异常抛出后读取 traceback 中 Results，24 组已完成详情完全一致，两个观察运行仍返回 1 |
| 旧 FH 公式负对照 | 两种模式均返回 1；原因均为公式误差约 26.9404860801203，而非缺文件或导入失败 |
| 依赖身份 | 预哈希 {runtime['baseline_artifact_count']} 个现有 runtime 产物；实际载入的 {runtime['post_run_sha256_rechecked_loaded_artifacts']} 个外部产物完成运行后 SHA256 复核 |

独立导出与补跑结果没有覆盖或消除原 runner 的失败。其用途是保留已实际观察到的执行事实。没有用 `author_machine_checks_passed` 标签作为独立性证明；原 runner 实际上未执行到该状态。

## 执行数量与检索

- Lean/Lake 可执行进程共 **{commands['total_lean_lake_processes']}** 个（含版本/依赖查询），候选源码编译 2 次，验证器检查模块编译 2 次。
- `checks.py` 共执行 **6 次**：原 runner normal 1 次，直接 `-O` 1 次，旧 FH 负对照 2 次，保留异常的结果观察 2 次。
- 直接 normal/-O 合计 50 组调用：48 通过、2 失败；观察运行另有相同 50 组调用。负对照走独立分支，不计入 25 组。
- 独立证据一致性核查：**{checks['passed']}/{checks['total']}**。该计数表示预期成功/失败与证据相符，不表示原任务整体通过。
- 可检索关键词：`LEAN_RUNNER_INSPECTION_SYNTAX`、`NUMERICAL_MISSING_MANIFEST`、`target_mismatch`、`all-module-declarations`、`old-fh`。

关键数值（有限计算观察）：Wronskian 样例为 `-4*pi`、旧式 `-6*pi`；正确镜像 FH 值约 `53.88097216024057`、旧式约 `26.94048608012029`；n=2 归一化行列式为 `7030400000*pi^4/4782969`。详情与范围标签见数值证据，不将其提升为无限维证明。

## 信任边界

依赖现有 Lean 4.31.0 编译器/内核、mathlib 编译产物、Python/SymPy/mpmath 及 OS/WSL/硬件；未使用第二内核，未全面重编译 mathlib。运行后逐字节复核覆盖实际载入的外部 Lean 产物；其余预哈希产物仅核对最终元数据。不是整个系统的文件写入审计。

exact target 仅指包中 expected_type 在记录环境中匹配。FH 单界面公式仍是显式标量前提，不代表谱可微性或一般 FH 定理已形式化。Volterra 无限维估计、统一 Taylor 余项、min-max 与一般谱极限未获本次 Lean 认证。数值结果含符号运算和有限高精度运算，不是区间证明。

没有读取旧作者输出/README、项目 AGENTS、记忆、其它任务历史或解析新稿。列明的外部审计报告仅做字节哈希。所有主动写入均位于 `independent-execution`；输入脚本、原项目和外部 runtime 未修改，未 commit。最终语义审查留待独立 reviewer。

独立汇总曾有一次未完成尝试：重复解析已给出的绝对路径造成大量挂载文件系统元数据访问，执行者以 SIGTERM 停止自己的该进程（退出码 -15），保留原程序、原收据及当时输入核对记录；随后只将该路径处理改为清单绝对路径的直接匹配，重新执行完整且相同的字节哈希及证据检查。详见 `audit-retry-reason.json` 和 `executor-logs/independent-evidence-audit*.json`，没有改动输入程序或 Lean/数值结果。

## SHA256 指针

小型机器报告：`independent-execution.json` — SHA256 `{report['sha256']}`。

全部本次程序、日志、原始 manifest、声明和运行前后清单均列于 `evidence-index.json` 与 `SHA256SUMS`；索引中的每条记录含路径、完整 SHA256、字节数。外部程序和输入的完整 SHA256 在 `preflight.json`，载入依赖在 runtime 清单，Python 观察模块在 `python-loaded-files-*.json`。大型清单保持原始字节，未改写或截短。

'''
    for key in ('evidence-index.json','preflight.json','runner-review.json','runtime-before.json','runtime-after-imports.json','final-input-identity.json','executor-logs/lean-replay.json','replay/Inspection.lean','replay/positive/run-manifest.json','supplemental-negative/run-manifest.json','all-module-declarations.json','independent-root-artifact.json','numerical-crosscheck.json','command-inventory.json','independent-checks.json'):
        text+='- '+ref(key)+'\n'
    text+='\n执行者新增程序（输入程序另见 preflight）：\n\n'
    for p in sorted(RUN.glob('*.py')):
        text+=f'- `{p.name}` — SHA256 `{digest(p)}`\n'
    (RUN/'README.md').write_text(text)
    sums=[]
    for p in sorted(RUN.rglob('*')):
        rel=str(p.relative_to(RUN))
        if p.is_file() and rel not in ('SHA256SUMS','SHA256SUMS.sha256','delivery-integrity.json') and not p.is_relative_to(RUN/'tmp'):
            sums.append(digest(p)+'  '+rel)
    (RUN/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    (RUN/'SHA256SUMS.sha256').write_text(digest(RUN/'SHA256SUMS')+'  SHA256SUMS\n')
    print(json.dumps({'status':'INCOMPLETE','run_directory':str(RUN),'summary':pointer(RUN/'independent-execution.json'),'readme':pointer(RUN/'README.md'),'checksums':pointer(RUN/'SHA256SUMS'),'evidence_checks':[checks['passed'],checks['total']]},ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
