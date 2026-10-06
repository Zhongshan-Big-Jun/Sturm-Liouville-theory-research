---
{"author_ids": ["/root"], "conditions": ["Fixed c>0 and genuine complex Hc^s=D(Kc^(s/2)), 0<=s<7/2, original named family.", "V is the joint kernel of finitely many continuous complex-linear functionals on Hc^s; NV={n:p_n belongs to V}.", "Individual-member filtering only; not linear recombination or orthogonal projection."], "created": "2026-10-05", "dependencies": [{"location": "tools/krein-infinite-deletion-subclasses.md", "sha256": "99fb4727e989ee99fa206ac1b93d14dbdb44d36b4675c944730b5a229cdb9042"}], "evidence_status": "ROUND15_NATIVE_INDEPENDENT_ANALYTIC_REVIEW; AUTOMATIC_RECEIPT_NOT_RECEIVED", "lean_status": "NOT_RUN", "review_status": {"automatic_receipt": "UNAVAILABLE_NATIVE_ADAPTER", "current_evidence": "research/artifacts/proof-audit-round15-20261005/analytic-initial-review.md"}, "scope": "C15-A3-KREIN: finite-codimension subclass in this fixed Krein model only.", "sources": [{"locator": "Section7 corollary3 and proof; sections1-6 prerequisites", "path": "docs/SL_full_window_deletions_and_finite_constraints.md", "sha256": "75c3664fcd6b0091fc1097eaa49fd1ad1577390859fbe7bcb4690494fe8fa99b"}], "summary": "In the Krein member window, individual named members that lie in a finite-codimensional continuous-constraint subspace V span densely in V iff V is a coordinate intersection of a subset of the current continuous central trace kernels. Four order intervals give1/2/4/8 distinct feasible subspaces, with critical equalities on the fewer-trace side. General H A3/A4 and infinite constraints remain open.", "title": "Finite continuous constraints: individual-member filtering in the Krein scale", "tool_id": "krein-finite-constraint-filtering", "updated": "2026-10-05"}
---
# 有限余维约束的逐项筛选

V=intersection_(j=1..M)ker Lj, Lj 为目标 Hc^s 上连续复线性泛函.
NV={n:p_n in V}; QV={p_n:n in NV}. 则 closure span QV=V iff
V=intersection_(j in J)ker tau_j for some J subset I(s).
I(s)={}, {0}, {0,1}, {0,1,4}, 对应 [0,1/2], (1/2,3/2], (3/2,5/2], (5/2,7/2).
可行不同子空间数量=1/2/4/8. 迹 tau0=f(0),tau1=f'(0),tau4=f''(0).

证明: 若稠密, 有限余维排除任一奇偶和收敛, 两和发散时 A11 的精确闭包强迫 V 为迹坐标核交.
反向, 低列迹矩阵 diag(1,1,-4) 给 NV=D minus J, A12 的余有限闭包正好为 V.
同一矩阵满秩说明2^|I|个坐标核交确实互异.
例如 s=2, V=ker(f(0)+f'(0)): p0,p1 同时被筛掉, 闭包是 ker f(0) intersect ker f'(0), 严格小于 V.

这里只关闭本 Krein 模型有限连续约束的逐个成员筛选. 一般非对角 H 的 A3/A4、无限约束、先组合再约束、投影族、稳定基和误差率另计.
完整证明与独立原生复审见 [第十五轮报告](../reports/proof-audit-round15-20261005/REPORT.md).
自动接收格式缺口保持, 不继承旧回执为本卡自动批准.
