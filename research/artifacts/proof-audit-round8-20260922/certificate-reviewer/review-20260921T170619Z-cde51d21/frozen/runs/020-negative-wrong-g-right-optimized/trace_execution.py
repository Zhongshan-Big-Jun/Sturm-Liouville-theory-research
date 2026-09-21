"""Record actual loaded modules without restricting or filtering imports."""
import hashlib
import json
import platform
import runpy
import sys
from pathlib import Path


def main():
	TracePath = Path(sys.argv[1])
	TargetPath = Path(sys.argv[2]).resolve()
	sys.argv = [str(TargetPath), *sys.argv[3:]]
	sys.path.insert(0, str(TargetPath.parent))
	try:
		runpy.run_path(str(TargetPath), run_name="__main__")
	finally:
		ModuleRows = []
		for name, module in sorted(tuple(sys.modules.items())):
			ModulePath = getattr(module, "__file__", None)
			row = {"name": name, "file": ModulePath}
			if ModulePath and Path(ModulePath).is_file():
				row["sha256"] = hashlib.sha256(Path(ModulePath).read_bytes()).hexdigest()
			ModuleVersion = getattr(module, "__version__", None)
			if isinstance(ModuleVersion, str):
				row["version"] = ModuleVersion
			ModuleRows.append(row)
		TracePath.write_text(json.dumps({
			"python": sys.version, "executable": sys.executable,
			"platform": platform.platform(), "libc": platform.libc_ver(),
			"optimize": sys.flags.optimize, "sys_path": sys.path,
			"modules": ModuleRows,
			"scope": "Observed sys.modules after target execution, including trace-driver imports; no import filtering or sandbox.",
		}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
	main()
