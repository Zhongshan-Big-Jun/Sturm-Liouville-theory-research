# -*- coding: utf-8 -*-
import io
p = r"F:\LaTeX\BVE research\AGENTS.md"
with io.open(p, "rb") as f:
    data = f.read()
head, tail = data[:72622], data[72622:]
print("tail size:", len(tail))
try:
    g = tail.decode("gb18030")
    cjk = sum(1 for ch in g if '\u4e00' <= ch <= '\u9fff')
    print("gb18030 decode OK, len", len(g), "cjk", cjk)
    with io.open(r"F:\LaTeX\BVE research\misc\_tail_gb18030.txt", "w", encoding="utf-8") as f:
        f.write(g)
except Exception as e:
    print("fail:", e)