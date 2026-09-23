from pathlib import Path
import sys,hashlib,json
P=Path("/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts")
sys.path.insert(0,str(P))
import research_library as L
print(json.dumps(dict(python=sys.executable,yaml=L.yaml is not None,sources={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ["research_library.py","research_corrections.py","research_review.py"]})))
