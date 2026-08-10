# -*- coding: utf-8 -*-
import io, os

ROOT = r"F:\LaTeX\BVE research"
p = os.path.join(ROOT, "AGENTS.md")
with io.open(p, "rb") as f:
    data = f.read()

# find the first byte where strict UTF-8 decode starts failing (first invalid byte)
head = None
for cut in range(len(data) - 1, 0, -1):
    try:
        data[:cut].decode("utf-8")
        head = cut
        break
    except UnicodeDecodeError:
        continue
if head is None:
    raise SystemExit("no valid UTF-8 prefix found")
tail = data[head:]
print("valid UTF-8 head size:", head, "tail size:", len(tail))

# decode tail as GB18030
tail_text = tail.decode("gb18030")
print("tail text length:", len(tail_text))
print("tail head:", tail_text[:80])

# renumber Plato record 会话 26 -> keep as is (coordinator 会话 26/27 numbering)
# Actually: previous sessions end at 25 (coordinator). Plato's record is now 26. Keep it.
new_text = data[:head].decode("utf-8") + tail_text
with io.open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(new_text)
print("AGENTS.md repaired; total chars:", len(new_text))