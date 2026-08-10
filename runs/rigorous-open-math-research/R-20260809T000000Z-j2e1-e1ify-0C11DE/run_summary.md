# Run summary - R-20260809T000000Z-j2e1-e1ify-0C11DE

## Title
J2_2d < 0 证明中 55 项单变量事实的完全解析化 (E1): 消除 O3a 文档最后一处对区间
验证器 (E2) 的依赖 (lem:brackets / lem:track(iv) / eq:endpoints 的 55 项事实).

## Status
COMPLETED (continuation session 44, 2026-08-09). 问题契约的所有完成标准满足:
1. 55 项单变量事实逐一有显式 E1 证明 (证书台账 misc/e1_cert_ledger.json 57/57 PASS,
   含 3 项 h 凹性归约; 证书总表在文档附录 A);
2. tex 更新完毕: rem:riv 改为注 5.13 有理包络方法 (rem:env), lem:brackets /
   lem:track(iv) / eq:endpoints 的 E2 认证全部换成 E1 有理区间链, 证据分层只剩
   E1 (严格解析) + E3 (数值扫描, 仅交叉检验, 不作为结论);
3. xelatex 两遍编译零警告零错误 (40 页), 无未定义引用, 无 Overfull/Underfull.

## What was done in this session
- 修复 misc/rigid1d.py 的 I.sqrt bug (原写 `F(isqrt(...), den)+1`, 宽度恒为 1.0;
  改为 `F(isqrt(...)+1, den)`), 这是 TB 点事实失败的根因.
- 生成 E1 证书链: misc/e1_certgen.py -> misc/e1_cert_ledger.json (57/57 PASS,
  约 266 秒, 需 py -X utf8 与 sys.set_int_max_str_digits(1000000)).
- 生成证书表: misc/e1_cert_tables.py -> misc/e1_cert_tables.tex (5 张表:
  tab:envprims, tab:envpoints, tab:envsigns, tab:envrange, tab:envderiv).
- 表格显示规范化: fmt_name 把 >=/<= 映射为 \ge/\le, 目标 2/1 归一为 2;
  显示精度 6/12 位小数向外取整, 显示区间包含认证区间 (E1 有效性保持);
  原语表 \footnotesize + \tabcolsep 3pt, 长表局部 \tabcolsep 3pt, 消除
  Overfull (原 envprims 154pt, envderiv 10pt).
- 修复两处段落 Overfull (L7-L9 哈希项改为 quote 块 + 显式换行; 附录产物清单
  旧验证器三件套项显式换行).
- 哈希行更新: L12 = dce5c453... (misc/e1_cert_tables.py); L10/L11 未变.
- 历史清理: 旧十进制区间引擎 (rigid_dec.py / zz_verify_e1_dec.py /
  e1_facts_ledger.json, L7-L9) 与二维叶盒族全部标注为历史复现记录, 不影响结论.

## Certificate chain (content hashes)
- L10 misc/e1_certgen.py: 375209e2574aea15e3966b442316e2326070d75d4b9445d4bdb9ccf74dfec57c
- L11 misc/e1_cert_ledger.json: ec9ce5ff7af7d9684bdd2097368e789e6f0b1dae798a04e62aef3d073fd68d30
- L12 misc/e1_cert_tables.py: dce5c4538397257b823cd92cf1a7d4180a0ac24ba6e62b9d30d7d1efa33bb249
- misc/e1_cert_tables.tex: 93eac8e0c4a5ed7b2bf7b90ab9daae62a35dd2b8a16610b00758c6ecb54c0265
- misc/rigid1d.py (精确有理区间内核): 1dec97d9c59185fa38a94058c5ca94b0573e3ed36c268826b61ce537e1095ddc
- docs/SL_gap_n1_O3a_phase_rigidity_proof.tex: d8e83f4472f1044ca8694b76ca724f0bf326f10c4d17fe405e72329b753af183
- docs/build/SL_gap_n1_O3a_phase_rigidity_proof.pdf (40 页, 零警告): 72836e20d36cf85c955669509383d35a14e48b1b620e222f4cb6397c77e48408

## Evidence layering (per project discipline)
- E1 (STRICT, 结论依据): 闭式恒等式, 初等不等式, 单调性, 以及注 5.13 有理包络
  方法生成的有限精确有理数不等式链 (附录 A 证书总表, 可人工复核).
- E3 (EVIDENCE, 仅交叉检验): 数值扫描数据 (注 rem:explore 等) 与 E3 侦察裕量
  (最紧 h(0.655)-m ~ 2.6e-5), 不构成任何结论依据.
- E2 (历史): 旧十进制区间验证器与二维叶盒证书已全部退役, 文档只作历史复现记录.
- 未完成缺口: 无 (本契约范围内). 后续可选项: 证书链的独立第三方重放, 以及把
  证书表进一步压缩到更少行 (文档宽度已满足, 属美学选项).

## Reproduction
```
cd "F:\LaTeX\BVE research"
py -X utf8 misc\e1_certgen.py        # ~266 s, 57/57 PASS
py -X utf8 misc\e1_cert_tables.py    # -> misc/e1_cert_tables.tex
cd docs
xelatex -interaction=nonstopmode -output-directory=build SL_gap_n1_O3a_phase_rigidity_proof.tex
# 连跑两遍; 零警告零错误, 40 页
```

## Session 45 addendum (2026-08-09): independent symbolic audit
- Two audit scripts (misc/_audit_symbolic_a.py 21 checks, misc/_audit_symbolic_b.py
  67 checks) independently re-derive every identity in the O3a chain: all PASS.
- Key: J2 = 2 A^2 cg W / Delta^4 verified from the raw eq:G definition modulo
  circle relations (Groebner reduction -> 0); 50-digit numeric cross-check
  1e-49. lem:j2dec is now fully self-contained.
- Fixed: tex line 344 sign typo; tex line 1437 sin(17/10) >= cos(13/100);
  misc/_verify_identity.py (now reports modulo-relations identity True).
- e1_certgen replay: 57/57 PASS (241.6 s), L10/L11/L12 hashes unchanged.
- Recompiled 38 pages, zero warnings. Details: audit_report.md.

## Session 48 addendum (2026-08-10): Audit E - replay + dual audit + F-210/F-211
- Independent replay: misc/audit_o3a_cert_replay.py (decimal.Decimal 80 digits,
  directed rounding, alternating-series sin/cos/atan + Machin pi) vs exact Fraction
  generator: 71/71 PASS (57 facts + 11 primitive rows + 3 structural checks);
  replay.py 3a8672f4..., replay.json c239092d... (see repro_manifest).
- Dual-subagent adversarial audit: Curie (lines 1-559) REPAIRABLE_GAP, single defect
  F-210 (phase-branch selection); Linnaeus (lines 559-2396) PASS with independent
  re-derivations, two harmless remarks. No E3 used as a premise.
- F-210 fixed: new lemma lem:phasebranch (Prufer phase theta, theta' = s(cos^2 +
  rho sin^2) > 0; y1 even/y2 odd; explicit mid-region solutions; E(alpha1) = c alpha1,
  O(alpha2) = c alpha2; uniqueness via monotonicity).
- F-211 fixed: thm:j1e1 step (iv) extended to [pi/3, 1122/1000]; tail uses exact
  rational envelopes at x0 = 1122/1000 (sin/cos sandwich, 765791/250000 > 0).
- xelatex twice: 40 pages, zero warnings. tex d8e83f44..., pdf 72836e20...;
  certificate data unchanged (e1_certgen/ledger hashes identical).
- Status: CANDIDATE_COMPLETE_PROOF maintained; O3a "completely rigorous" bar met
  (71/71 replay + dual audit PASS + phase-branch gap closed).

## Session 49 addendum (2026-08-10): completeness-audit script fixes (E3)
- Re-ran all 8 completeness-audit scripts (E3 evidence, cross-check only): ALL PASS.
- Fixed two scripts with grid/precision defects unrelated to the E1 proof:
  part2b (eigvals grid top 2*pi-1e-7 -> 3*pi; R list [1.1..1000] without 1e6),
  part2c (xi scan to 0.4999995; mpmath refinement keeps xi* as mpf throughout;
  R=1000 R1=-5.44e-44, R=1e6 R1=-2.76e-46).
- No E1 proof text or certificate data changed; document recompiled after
  completing the sec:certs audit-script list with part2b (40 pages, zero
  warnings; tex 2c331257..., pdf ecc7ef62..., log c9be8560...). Status unchanged:
  CANDIDATE_COMPLETE_PROOF (71/71 replay + dual audit PASS + phase-branch gap closed).