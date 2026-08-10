# -*- coding: utf-8 -*-
import io
p = r"F:\LaTeX\BVE research\AGENTS.md"
with io.open(p, "rb") as f:
    data = f.read()

dec = data.decode("utf-8", errors="surrogateescape")
# walk to find runs of escaped bytes with byte positions
runs = []
i = 0
bytepos = 0
while i < len(dec):
    ch = dec[i]
    if 0xDC80 <= ord(ch) <= 0xDCFF:
        start_char = i; start_byte = bytepos
        while i < len(dec) and 0xDC80 <= ord(dec[i]) <= 0xDCFF:
            bytepos += 1
            i += 1
        runs.append((start_byte, bytepos, dec[start_char:i]))
    else:
        bytepos += len(ch.encode("utf-8"))
        i += 1
print("runs:", len(runs))
for (a, b, s) in runs[:10]:
    print("byte range", a, b, "len", b-a)
# total escaped bytes
tot = sum(b-a for (a,b,_) in runs)
print("total escaped bytes:", tot)
# check if the corrupted spans decode as GB18030 into CJK
for (a, b, s) in runs[:3]:
    raw = data[a:b]
    try:
        g = raw.decode("gb18030")
        cjk = sum(1 for ch in g if '\u4e00' <= ch <= '\u9fff')
        print("span", a, b, "gb18030 ok, cjk count", cjk, "/", len(g))
        print("  sample:", g[:120])
    except Exception as e:
        print("span", a, b, "gb18030 fail:", e)