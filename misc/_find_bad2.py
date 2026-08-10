# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
p = r"F:\LaTeX\BVE research\AGENTS.md"
with io.open(p, "rb") as f:
    data = f.read()
print("first 96 bytes hex:")
print(data[:96].hex(" "))
# try to find all invalid-byte islands
bad = []
i = 0
while i < len(data):
    try:
        data[i:].decode("utf-8")
        break
    except UnicodeDecodeError as e:
        bad.append((e.start + i, e.end + i))
        i = e.end + 1
print("invalid islands:", bad[:20])