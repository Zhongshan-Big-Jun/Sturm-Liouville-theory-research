# -*- coding: utf-8 -*-
p = r'docs\SL_gap_n1_symline_proof.tex'
t = open(p, encoding='utf-8').read()
reps = [
 (r'\section{易区 (c>=1/2): F_e(c)<0}\label{sec:easy}',
  r'\section{易区 c>=1/2}\label{sec:easy}'),
 (r'\section{KEY LEMMA: \texorpdfstring{$0<c<1/2$}{0<c<1/2} 的唯一零点}\label{sec:keylemma}',
  r'\section{KEY LEMMA: 唯一零点}\label{sec:keylemma}'),
 (r'\section{\texorpdfstring{端点极限 $D$}{端点极限 D}}\label{sec:endpoints}',
  r'\section{端点极限 D}\label{sec:endpoints}'),
 (r'\subsection{\texorpdfstring{$\widetilde F_e$}{F-e} 与降维恒等式}',
  r'\subsection{Fe 与降维恒等式}'),
]
for a, b in reps:
    assert a in t, 'MISSING: ' + a[:60]
    t = t.replace(a, b)
open(p, 'w', encoding='utf-8').write(t)
print('OK')
