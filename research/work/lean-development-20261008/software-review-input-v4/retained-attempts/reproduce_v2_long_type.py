from pathlib import Path
import sys
Base = Path(r"F:\tools\lean-joint-20261008\plugin")
sys.path.insert(0, str(Base / "source-freeze-v2/plugins/lean-verify/scripts"))
from lean_develop import DevelopSession
from lean_runtime import LeanRuntime, write_json
Destination = Base / "pp-interface/long-type-v2"
if Destination.exists():
    raise SystemExit("retain previous PP reproduction")
Root = Destination / "project"
Root.mkdir(parents=True)
(Root / "lean-toolchain").write_text("leanprover/lean4:v4.31.0\n", encoding="utf-8")
def balanced(Depth):
    if Depth == 0:
        return "n + 0 = n", "Nat.add_zero n"
    Type, Proof = balanced(Depth - 1)
    return "(" + Type + ") ∧ (" + Type + ")", "And.intro (" + Proof + ") (" + Proof + ")"
Type, Proof = balanced(9)
(Root / "Main.lean").write_text("namespace Long\ntheorem result (n : Nat) : " + Type + " := " + Proof + "\nend Long\n", encoding="utf-8")
Runtime = LeanRuntime(Root, Destination / "output", r"C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe", r"C:\Users\HuangZY\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lake.exe", True)
Session = DevelopSession(Runtime, 120, "cli")
try:
    Result = Session.probe(["Long.result"], ["Main"])
    write_json(Destination / "REPRODUCTION.json", {"result": Result, "balanced_equality_leaves": 512})
    assert Result["status"] == "checked", Result
    Actual = Result["declarations"][0]["actual_type"]
    assert "⋯" in Actual, "old limits did not truncate this fixture"
    print("old v2 actual probe reported checked with omission count=" + str(Actual.count("⋯")), flush=True)
finally:
    Session.close()
