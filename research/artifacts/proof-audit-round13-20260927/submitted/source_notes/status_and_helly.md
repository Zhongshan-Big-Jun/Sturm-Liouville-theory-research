# 核对过的文稿状态与 Helly 工具原文

固定提交：`4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983`。以下是精确文件定位与简短摘录/转述，不是全文件副本。

## Helly 卡

`tools/helly-compactness.md`，blob `006a701325dbbb78fcbb8cc5cdc8c1f6b2e1f613`。

原文把“单调有界函数族存在逐点收敛子列”接到“目标泛函在子列极限处连续，因此 inf 或 sup 被达到”，但未要求极限仍属于容许类。

## 当前研究地图

`research_map.md`，blob `524634f49d3315b25751dd732b500d9584ce02be`。

A1 为完整窗口 `0<=s<7/2`；A12 为该窗口全部余有限闭包；B10 为第十二轮半谱/极点/扇区修订。该地图还将 `docs/SL_spectral_topics_summary.tex` 第5节列为当前开放问题总览入口。

## 仍旧的总览

`docs/SL_spectral_topics_summary.tex`，blob `13f32e0f9e4adb92fd3b753647439ed6ec7e8f00`。

摘要仍将自身表述为“当前进展”，已知完备性只写 `0<=s<=3`；同时保留 G2 已全局闭合、仅余 G1' 的旧表述，而当前地图对历史 G2 的量词对齐另有限定。

## 稳定性正文

`docs/SL_stability_moment_jump.tex`，blob `072458dc296c03f92ff2427a5d1e41fc57611ac6`。

第1节对原族完备性范围的当前进度说明仍落在三阶，并保留更高分数窗口未判定的旧状态。其后全指标增长、对角级数判据与扰动反例的限定不能随着状态更新被机械放宽。

## 退役状态必须保留

`docs/SL_gap_n1_O3a_phase_rigidity_proof.tex` 的“证据层次与历史复现合同”明确说旧 Decimal 引擎与旧55事实验证器已退役，由有理包络方法及 `misc/e1_certgen.py`/`misc/e1_cert_ledger.json` 取代。

但是 `tools/interval-dec-directed-rounding.md` 仍作为工具卡介绍保证向外包络、55事实已认证及随机检查零违反。修复应明确停止默认可信复用，不能仅因旧脚本仍存在就断言当前主定理仍依赖它。
