# -*- coding: utf-8 -*-
import io, os

ROOT = r"F:\LaTeX\BVE research"

def repair(path):
    with io.open(path, "rb") as f:
        data = f.read()
    head = None
    for cut in range(len(data) - 1, 0, -1):
        try:
            data[:cut].decode("utf-8")
            head = cut
            break
        except UnicodeDecodeError:
            continue
    if head is None:
        print("NO VALID HEAD:", path)
        return
    tail = data[head:]
    try:
        tail_text = tail.decode("gb18030")
    except Exception as e:
        print("TAIL NOT GB18030:", path, e)
        return
    new_text = data[:head].decode("utf-8") + tail_text
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_text)
    print("repaired:", os.path.relpath(path, ROOT), "head", head, "tail", len(tail))

for rel in [r"tools\key-lemma-decomposition.md", r"tools\README.md"]:
    repair(os.path.join(ROOT, rel))