# 第十一轮审计复核包

首先阅读 `proof_audit_round11_20260925.md`。

`cofinite_all_orders_proof.md` 是本轮新补证：整个 $0\le s<7/2$ 内的余有限闭包，包括三个临界中心迹阶数；尚未写回仓库或经另一位独立审稿人验收。

运行 `python checks.py` 与 `python -O checks.py` 可重放本轮 20 组有限检查。原始 JSON 和日志在 `evidence/`。源码恢复文件的字节身份见 `source_manifest.json`。

检查不访问网络、不修改远端仓库；未执行仓库完整 CLI、完整测试套件或 Lean。反例中的常密度适配器是为排除谱数值误差而独立编写的，不是把它冒充原侦察主程序。
