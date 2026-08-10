# -*- coding: utf-8 -*-
import io
p = r"F:\LaTeX\BVE research\AGENTS.md"
with io.open(p, "rb") as f:
    data = f.read()
print("size", len(data))
# locate all bytes that are invalid in UTF-8 by testing each byte as potential continuation
# Fast approach: try decoding the whole file with surrogateescape to find raw bytes >= 0x80 that are not part of valid sequences
dec = data.decode("utf-8", errors="surrogateescape")
positions = []
for i, ch in enumerate(dec):
    if 0xDC80 <= ord(ch) <= 0xDCFF:  # escaped invalid byte
        positions.append(i)
print("number of escaped invalid bytes:", len(positions))
if positions:
    print("first few positions:", positions[:20])
    for pos in positions[:6]:
        lo = max(0, pos-60); hi = min(len(dec), pos+60)
        print("--- around", pos, "---")
        print(dec[lo:hi])
print("head 40:", dec[:40])