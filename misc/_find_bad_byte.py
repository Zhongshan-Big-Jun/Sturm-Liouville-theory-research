# -*- coding: utf-8 -*-
import io
p = r"F:\LaTeX\BVE research\AGENTS.md"
with io.open(p, "rb") as f:
    data = f.read()
# find first invalid UTF-8 byte position
pos = None
for i in range(len(data)):
    try:
        data[i:i+1].decode("utf-8")
    except UnicodeDecodeError:
        pos = i
        break
print("first invalid byte at", pos, "of", len(data))
print("context (decoded lossy):")
chunk = data[max(0,pos-400):pos+400]
print(chunk.decode("utf-8", errors="replace"))