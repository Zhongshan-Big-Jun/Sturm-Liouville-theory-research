# -*- coding: utf-8 -*-
import io
p = r'docs\SL_gap_n1_symline_summary.tex'
lines = open(p, encoding='utf-8').read().splitlines(keepends=True)
new = {
 74:  r'\subsection{易区 c>=1/2}' + '\n',
 83:  r'\subsection{路线 1: F-e 二阶导整符号路线 (放弃)}' + '\n',
 90:  r'\subsection{路线 2: G2>=0 只对曲线成立 (修正)}' + '\n',
 97:  r'\subsection{路线 3: W0 全域正性的初版误判 (关键更正)}' + '\n',
}
for n, s in new.items():
    assert lines[n-1].strip().startswith('\\subsection'), (n, lines[n-1])
    lines[n-1] = s
open(p, 'w', encoding='utf-8').write(''.join(lines))
print('patched by line')
