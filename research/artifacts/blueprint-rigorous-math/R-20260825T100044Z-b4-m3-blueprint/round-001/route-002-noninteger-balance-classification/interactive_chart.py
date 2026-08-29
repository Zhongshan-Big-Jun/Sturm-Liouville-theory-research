"""Hash-bound interactive exact-coefficient session for route 002."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import sympy as sp


REPO = Path(__file__).resolve().parents[6]
EXPECTED = {
    "scripts/_gapn2_largeR_Pbuild.py":
        "58c98af44d074bdfd9412a1541d4a7a393f0cf3e074653c1108964b62ea6caea",
}
for rel, expected in EXPECTED.items():
    got = hashlib.sha256((REPO / rel).read_bytes()).hexdigest()
    if got != expected:
        raise SystemExit(f"hash mismatch {rel}: {got}")

source = REPO / "scripts/_gapn2_largeR_Pbuild.py"
spec = importlib.util.spec_from_file_location("gapn2_pbuild_bound", source)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
P = module.build()

u = sp.symbols("u", positive=True)
K, A, B, C = sp.symbols("K A B C", real=True)
q, D = sp.symbols("q D", real=True)
E = {
    eq: sp.expand(sum(P[(eq, m)] * u**m for name, m in P if name == eq))
    for eq in ("E1", "E2", "E5", "E6")
}
print(f"READY sympy={sp.__version__} keys={len(P)}")
