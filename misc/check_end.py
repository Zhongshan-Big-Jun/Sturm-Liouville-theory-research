tex = open(r"docs/SL_gap_n1_O3a_phase_rigidity_proof.tex", encoding="utf-8").read()
print("has end document:", "\\end{document}" in tex)
print("last 200 chars:", repr(tex[-200:]))
print("total lines:", tex.count("\n"))
# check around line 1180-1201
lines = tex.splitlines()
for i in range(1180, len(lines)):
    print(i+1, repr(lines[i]))
