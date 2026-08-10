import io
p = r'docs\SL_stability_moment_jump.tex'
s = io.open(p, encoding='utf-8').read()
old = r"\newtheorem{definition}[theorem]{定义}"
new = r"\newtheorem{definition}[theorem]{定义}" + "\n" + r"\newtheorem{proposition}[theorem]{命题}"
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print("added proposition env")
