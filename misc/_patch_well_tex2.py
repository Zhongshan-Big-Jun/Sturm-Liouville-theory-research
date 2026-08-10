# -*- coding: utf-8 -*-
"""Plain-ify section titles (no math) and use \\url for long filenames."""
import io
p = r"docs\SL_gap_n1_well_rigidity_R32.tex"
src = io.open(p, encoding="utf-8-sig").read()

repl = [
    (r"\section{\texorpdfstring{相位比 $r_{\tau}$ 的严格单调性 ($0\le q\le 1/2$)}{相位比 r_tau 的严格单调性 (0<=q<=1/2)}}\label{sec:mono}",
     r"\section{相位比函数的严格单调性 (q 不超过 1/2)}\label{sec:mono}"),
    (r"\section{\texorpdfstring{$R>3/2$: 离轴分支与候选路线}{R>3/2: 离轴分支与候选路线}}\label{sec:route}",
     r"\section{R>3/2: 离轴分支与候选路线}\label{sec:route}"),
    (r"\subsection{候选路线 (若成立则把刚性推到一般 $R$)}",
     r"\subsection{候选路线 (若成立则把刚性推到一般 R)}"),
    # long filenames -> \url (breaks allowed with [hyphens])
    (r"\texttt{SL\_gap\_n1\_O3a\_phase\_rigidity\_proof.pdf}.",
     r"\url{SL_gap_n1_O3a_phase_rigidity_proof.pdf}."),
    (r"见 \texttt{SL\_gap\_n1\_inf\_limit\_proof.tex}.",
     r"见 \url{SL_gap_n1_inf_limit_proof.tex}."),
    (r"\texttt{misc/\_well\_explore\_log.md}; 本会话验证矩阵",
     r"\url{misc/_well_explore_log.md}; 本会话验证矩阵"),
    (r"(\texttt{scripts/\_well\_rigid\_verify.py})",
     r"(\url{scripts/_well_rigid_verify.py})"),
    (r"均在 \texttt{scripts/}, 除注明外",
     r"均在 \url{scripts/}, 除注明外"),
    (r"\texttt{\_well\_landscape2.py}, \texttt{\_well\_crit.py}, \texttt{\_well\_explore1..3.py} (\texttt{misc/});",
     r"\url{_well_landscape2.py}, \url{_well_crit.py}, \url{_well_explore1..3.py} (\url{misc/});"),
    (r"\texttt{\_well\_symline.py}, \texttt{\_well\_fzeros.py}, \texttt{\_well\_fine.py};",
     r"\url{_well_symline.py}, \url{_well_fzeros.py}, \url{_well_fine.py};"),
    (r"\texttt{\_well\_verify\_thm.py}, \texttt{\_well\_verify\_rc.py}, \texttt{\_well\_branch\_threshold.py}, \texttt{\_well\_psitilde.py}, \texttt{\_well\_psi\_factor.py};",
     r"\url{_well_verify_thm.py}, \url{_well_verify_rc.py}, \url{_well_branch_threshold.py}, \url{_well_psitilde.py}, \url{_well_psi_factor.py};"),
    (r"\texttt{\_well\_n1curve.py}, \texttt{\_well\_n1refine.py}, \texttt{\_well\_energy\_ratio.py};",
     r"\url{_well_n1curve.py}, \url{_well_n1refine.py}, \url{_well_energy_ratio.py};"),
    (r"\texttt{\_well\_H.py}, \texttt{\_well\_system\_derive.py}, \texttt{\_well\_rigid\_verify.py}, \texttt{\_well\_signcheck.py}.",
     r"\url{_well_H.py}, \url{_well_system_derive.py}, \url{_well_rigid_verify.py}, \url{_well_signcheck.py}."),
]
for old, new in repl:
    if old not in src:
        print("MISS:", old[:60])
    src = src.replace(old, new)
io.open(p, "w", encoding="utf-8-sig", newline="\r\n").write(src)
print("patched OK")
