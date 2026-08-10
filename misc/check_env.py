import re
tex = open(r"docs/SL_gap_n1_O3a_phase_rigidity_proof.tex", encoding="utf-8").read()
# find all begin/end environments
pat = re.compile(r'\\(begin|end)\{([a-zA-Z*]+)\}')
stack = []
for m in pat.finditer(tex):
    kind, env = m.group(1), m.group(2)
    if kind == 'begin':
        stack.append((env, tex.count('\n', 0, m.start())+1))
    else:
        if not stack:
            print("UNMATCHED end", env, "at line", tex.count('\n',0,m.start())+1); break
        top, ln = stack.pop()
        if top != env:
            print("MISMATCH: opened", top, "at line", ln, "closed by", env, "at line", tex.count('\n',0,m.start())+1)
            break
else:
    print("balanced; leftover open:", stack)
