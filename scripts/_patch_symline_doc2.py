# -*- coding: utf-8 -*-
# 二次补丁: 加 Claim A 引理 (修复抽象里的未定义引用 thm:claimA) +
# 章节标题数学的 hyperref PDF-string 警告 (零警告目标).
import io, sys

p = r"F:\LaTeX\BVE research\docs\SL_gap_n1_symline_allR_proof.tex"
s = io.open(p, encoding="utf-8").read()

def rep(old, new, must=True):
    global s
    if old not in s:
        print("NOT FOUND >>>", old[:110].replace("\n", " / "))
        if must:
            sys.exit(1)
        return
    s = s.replace(old, new, 1)
    print("OK >>>", old[:60].replace("\n", " / "))

# 1. 抽象里的措辞 (可选) 与 Claim A 引理插入
rep(r"(关键定理 (Claim A, 定理 \ref{thm:claimA})",
    r"(关键引理 (Claim A, 引理 \ref{thm:claimA})")

old_ins = r"""\end{proof}

\begin{lemma}[Claim A 推出 KEY LEMMA]\label{lem:claimAtoKL}
设对一切 $\tilde q\in(0,1)$, $\gamma\in[\gamma_0^*,\gamma_0(\tilde q)]$ 有
$\rho(\tilde q,\gamma)<1$. 则定理 \ref{thm:main} 成立.
\end{lemma}"""
new_ins = r"""\end{proof}

\begin{lemma}[Claim A]\label{thm:claimA}
对一切 $\tilde q\in(0,1)$ 与 $\gamma\in[\gamma_0^*,\gamma_0(\tilde q)]$ 有
$\rho(\tilde q,\gamma)<1$. (证明在 \S\ref{sec:chain}--\S\ref{sec:rho0}:
链定理 \ref{thm:chain} 与定理 \ref{thm:rho0}.)
\end{lemma}

\begin{lemma}[Claim A 推出 KEY LEMMA]\label{lem:claimAtoKL}
设引理 \ref{thm:claimA} (Claim A) 成立, 即对一切 $\tilde q\in(0,1)$,
$\gamma\in[\gamma_0^*,\gamma_0(\tilde q)]$ 有 $\rho(\tilde q,\gamma)<1$.
则定理 \ref{thm:main} 成立.
\end{lemma}"""
rep(old_ins, new_ins)

# 2. 章节标题 hyperref 警告
rep(r"\section{张力比链: $\rho\le\rho_0$}\label{sec:chain}",
    r"\section{张力比链: \texorpdfstring{$\rho\le\rho_0$}{rho <= rho_0}}\label{sec:chain}")
rep(r"\section{一维不等式: $\rho_0(\gamma)<1$}\label{sec:rho0}",
    r"\section{一维不等式: \texorpdfstring{$\rho_0(\gamma)<1$}{rho_0(gamma) < 1}}\label{sec:rho0}")
rep(r"\section{KEY LEMMA 全 $R$ 的证明}\label{sec:proof}",
    r"\section{KEY LEMMA 全 \texorpdfstring{$R$}{R} 的证明}\label{sec:proof}")
rep(r"\section{推论: INF 侧全 $R$ 闭合}\label{sec:cor}",
    r"\section{推论: INF 侧全 \texorpdfstring{$R$}{R} 闭合}\label{sec:cor}")

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("PATCHED 2 OK")
