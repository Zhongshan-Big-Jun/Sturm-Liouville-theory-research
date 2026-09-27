# 第十三轮复核包

基线：`4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983`；审计日期：2026-09-27。

## 阅读

先读 `REPORT.md`，再按问题编号查 `analytic_notes.md`。`repair_prompt_astra_max.md` 可直接交给修复模型；它默认已提供本包。

本包只创建于审计工作目录，未修改GitHub仓库。

## 复现

安装 `requirements.txt` 中的依赖后，在本目录执行：

```sh
python run_e1.py
python checks.py
python -O run_e1.py
python -O checks.py
python independent_interface.py
```

`run_e1.py` 只在本包的 `work/` 子目录运行恢复的旧驱动及单条负对照，不覆盖远端或其他工程。它会更新本地 `evidence/` 下对应日志。

`checks.py` 的42项 CONFIRMED 包括确认源程序失败，**不是修后正确性测试，也不是42项仓库定理的形式认证**。修复模型必须保留基线反例，并另写修后性质回归；不能把旧错误继续复现视为修复成功。

## 来源

`source_manifest.json` 明确区分三份整文件Git blob匹配源码、函数摘录、测试适配器和本轮独立程序。`rational_excerpt.py` 只提供测试标量区间及常数回调所需的最小D/D2适配器，并未执行当前Fraction生成器的完整D2/55事实流程。

`independent_interface.py` 不调用仓库的求根、归一化或Jacobian公式，使用65位物理传播、块内质量积分及隐式求导。它给出有限高精度比较，不是区间认证。

## 内容

- REPORT.md：12组修订项、范围与优先级。
- analytic_notes.md：解析反例、修订公式和不能外推的边界。
- repair_prompt_astra_max.md：默认附件已给出的修复指令。
- source_excerpts/：三份原字节恢复文件及明确标注的函数摘录。
- source_notes/：当前证书调用、文稿状态与定位。
- checks.py、run_e1.py、independent_interface.py：实际复验代码。
- evidence/：普通/-O结果、完整旧驱动负对照、65位独立数据与执行记录。
- MANIFEST.json：除本清单自身之外的文件哈希。

## 未执行范围

没有全仓库检出或穷尽式代码搜索；GitHub代码搜索返回了不完整结果，故未据此声称调用清单完整。没有运行全部原CLI、全测试套件、Lean、完整M3/KP或当前Fraction证书生成器全流程。未给任何全参数浮点误差、谱尾或全局定号保证。

旧Decimal引擎已被当前主证明明确退役。其反例与当前有理证书输出问题必须区分；不能据旧代码失败直接撤回当前左定或n=1主定理。
