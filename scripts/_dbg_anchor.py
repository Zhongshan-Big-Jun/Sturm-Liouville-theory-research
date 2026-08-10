import io
s = io.open(r'docs\SL_stability_moment_jump.tex', encoding='utf-8').read()
print('anchor found:', r'\subsection{Krein 族的稳健性}' in s)
print('len:', len(s))
