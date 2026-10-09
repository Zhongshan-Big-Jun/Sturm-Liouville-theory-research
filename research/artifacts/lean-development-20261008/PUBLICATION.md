# 2026-10-09 联合增量上传范围与复现

用户在本地验收后要求上传最新插件与研究仓库. 本次提交最近完成的Lean和manage
联合增量, 保留原KP-DET脏稿、原未跟踪工作、旧benchmark与原冻结字节.
插件配对源码commit为 [af360f8f1fdf](https://github.com/xsoc1/rigorous-open-math-research/commit/af360f8f1fdf2df60c8c0f18d84d4e3740a13776),
manage2.1.0/lean-verify2.1.2/workflow2.0.2/rigorous2.0.1.
244文件的受审源码身份见插件 docs/v2.1-evidence/source-manifest-v13.json.
本机全局安装未升级, 发布不增加工具库/Blueprint接收或新的数学批准.

## 大证据还原

18份大JSON的原始路径和字节在本机保持, 以12个按原SHA去重的gzip发布,
总压缩大小243495258字节. [映射](large-evidence.json) 给出18个原路径、
原SHA/字节数及每个压缩包的SHA. 各唯一包解压的SHA和大小均已实际核对.
Git普通文件不含这18份超限JSON; 不截短类型、不改manifest、不改变旧审查绑定.

克隆后先运行, 再使用原验证器重查收据:

```powershell
$PublicationPython = 'python'
$EvidenceDir = 'research/artifacts/lean-development-20261008'
& $PublicationPython -B "$EvidenceDir/restore_large_evidence.py"
& $PublicationPython -B "$EvidenceDir/restore_large_evidence.py" --check
```

还原器仅向映射内路径写入经过SHA核对的完整原文, 已有同字节文件保持,
已有异字节文件拒绝覆盖. 可用 --target-dir 单独指定副本根, --only 选择精确路径.
还原不执行Lean, 也不把另一机器的路径/环境认作原验收环境.
移植或重新证明仍按现有接口选择新输出位置, 不覆盖原verification/verification-v3.

## 本轮证据与实际发布

- [Lean原验收与开放连接](README.md), [manage五问与限制](../manage-context-20261009/README.md).
- manage原生完成/负面回执的引用副本在 ../manage-context-20261009/reviews/,
  副本不构成在另一项目重新接收. 完整原件路径保留在数据中.
- 插件对应候选CI见 [实际run](https://github.com/xsoc1/rigorous-open-math-research/actions/runs/37890770801),
  最终结果按对应commit的真实CI读取, 不沿用旧job的完成标签.
- 精确暂存清单、origin后fork的推送及远端commit/tree/blob读回在本机
  F:/tools/joint-publication-20261009/DELIVERY.json. 本文记录授权与打包,
  不预先报告尚未完成的推送. 旧记录的本地/未发布状态保留其当时语境.
