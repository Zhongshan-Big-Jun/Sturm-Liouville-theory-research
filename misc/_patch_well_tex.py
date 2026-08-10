# -*- coding: utf-8 -*-
"""Fix warnings in SL_gap_n1_well_rigidity_R32.tex (hyperref PDF strings, overfull/underfull)."""
import io
p = r"docs\SL_gap_n1_well_rigidity_R32.tex"
src = io.open(p, encoding="utf-8-sig").read()

# 1) section titles with math -> texorpdfstring
src = src.replace(
    r"\section{相位比 $r_{\tau}$ 的严格单调性 ($0\le q\le 1/2$)}\label{sec:mono}",
    r"\section{\texorpdfstring{相位比 $r_{\tau}$ 的严格单调性 ($0\le q\le 1/2$)}{相位比 r_tau 的严格单调性 (0<=q<=1/2)}}\label{sec:mono}")
src = src.replace(
    r"\section{$R>3/2$: 离轴分支与候选路线}\label{sec:route}",
    r"\section{\texorpdfstring{$R>3/2$: 离轴分支与候选路线}{R>3/2: 离轴分支与候选路线}}\label{sec:route}")

# 2) remark at 475-477: put long filename on its own line to avoid 50pt overfull
old = "垒族对应定理 (对一切 $R>1$ 成立) 见 \\texttt{SL\\_gap\\_n1\\_O3a\\_phase\\_rigidity\\_proof.pdf}.\n\t阱族需要 $R\\le3/2$ 的原因见注 \\ref{rem:vsbarrier}; 阈值精确性见注 \\ref{rem:threshold}."
new = "垒族对应定理 (对一切 $R>1$ 成立) 见文档\n\t\\texttt{SL\\_gap\\_n1\\_O3a\\_phase\\_rigidity\\_proof.pdf}.\n\t阱族需要 $R\\le3/2$ 的原因见注 \\ref{rem:vsbarrier}; 阈值精确性见注 \\ref{rem:threshold}."
assert old in src, "remark block not found"
src = src.replace(old, new)

# 3) underfull at 506-509: rephrase item (c) to avoid short line
old3 = "该定理给出 INF 极限值 $I(R)\\sim 24.943866/R$ (数值), 其证明链\n\t\t(Lemma A$''$) 尚需独立验证器复核, 见 \\texttt{SL\\_gap\\_n1\\_inf\\_limit\\_proof.tex}."
new3 = "该定理 (对称阱族 $R\\to\\infty$ 极限, INF 极限值 $I(R)\\sim 24.943866/R$, 数值) 的\n\t\t证明链 (Lemma A$''$) 尚需独立验证器复核, 见 \\texttt{SL\\_gap\\_n1\\_inf\\_limit\\_proof.tex}."
assert old3 in src, "item c not found"
src = src.replace(old3, new3)

# 4) overfull 1.1pt at 557-569: turn the script list into an itemize
old4 = "见附录 \\ref{app:verify}. 关键既有脚本:\n\\texttt{\\_well\\_landscape2.py} (阱道快速求解器), \\texttt{\\_well\\_crit.py},\n\\texttt{\\_well\\_symline.py}, \\texttt{\\_well\\_fzeros.py}, \\texttt{\\_well\\_fine.py},\n\\texttt{\\_well\\_verify\\_thm.py}, \\texttt{\\_well\\_verify\\_rc.py},\n\\texttt{\\_well\\_n1curve.py}, \\texttt{\\_well\\_n1refine.py},\n\\texttt{\\_well\\_energy\\_ratio.py}, \\texttt{\\_well\\_branch\\_threshold.py},\n\\texttt{\\_well\\_psitilde.py}, \\texttt{\\_well\\_psi\\_factor.py},\n\\texttt{\\_well\\_H.py}, \\texttt{\\_well\\_system\\_derive.py},\n\\texttt{\\_well\\_explore1..3.py} (misc/)."
new4 = "见附录 \\ref{app:verify}. 关键既有脚本 (均在 \\texttt{scripts/}, 除注明外):\n\\begin{itemize}\\setlength{\\itemsep}{0pt}\n\t\\item 阱道求解与临界点: \\texttt{\\_well\\_landscape2.py}, \\texttt{\\_well\\_crit.py}, \\texttt{\\_well\\_explore1..3.py} (\\texttt{misc/});\n\t\\item 对称线与单峰: \\texttt{\\_well\\_symline.py}, \\texttt{\\_well\\_fzeros.py}, \\texttt{\\_well\\_fine.py};\n\t\\item 相位比与阈值: \\texttt{\\_well\\_verify\\_thm.py}, \\texttt{\\_well\\_verify\\_rc.py}, \\texttt{\\_well\\_branch\\_threshold.py}, \\texttt{\\_well\\_psitilde.py}, \\texttt{\\_well\\_psi\\_factor.py};\n\t\\item $N_1$ 与能量比: \\texttt{\\_well\\_n1curve.py}, \\texttt{\\_well\\_n1refine.py}, \\texttt{\\_well\\_energy\\_ratio.py};\n\t\\item 恒等式与验证: \\texttt{\\_well\\_H.py}, \\texttt{\\_well\\_system\\_derive.py}, \\texttt{\\_well\\_rigid\\_verify.py}, \\texttt{\\_well\\_signcheck.py}.\n\\end{itemize}"
assert old4 in src, "script list not found"
src = src.replace(old4, new4)

io.open(p, "w", encoding="utf-8-sig", newline="\r\n").write(src)
print("patched OK")
