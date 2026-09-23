"""Run the same unequal-width regression against source or replacement."""
import ast
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np


def main():
	Source = Path(sys.argv[1])
	Tree = ast.parse(Source.read_text(encoding='utf-8'))
	Widths = np.array([0.25, 0.75])
	Integral = np.array([-3 * np.pi ** 2 / 4 - np.pi / 2, -9 * np.pi ** 2 / 4 + np.pi / 2])
	Initial = np.array([0.0, 1.0])
	if any(isinstance(Node, ast.FunctionDef) and Node.name == 'project_tangent' for Node in Tree.body):
		Spec = importlib.util.spec_from_file_location('candidate', Source)
		Module = importlib.util.module_from_spec(Spec)
		Spec.loader.exec_module(Module)
		Projected = Module.project_tangent(Initial, Integral)
		Mechanism = 'candidate.project_tangent'
	else:
		Nodes = [Node for Node in ast.walk(Tree) if isinstance(Node, ast.AugAssign)
			and isinstance(Node.target, ast.Name) and Node.target.id == 'b'
			and 'fblock' in ast.unparse(Node)]
		if len(Nodes) != 2:
			raise RuntimeError('Expected the actual two P1/P2 projection statements')
		Scope = {'b': Initial.copy(), 'fblock': Integral / Widths}
		exec(compile(ast.Module(body=[Nodes[0]], type_ignores=[]), str(Source), 'exec'), Scope)
		Projected = Scope['b']
		Mechanism = 'actual P1 source AST statement (P2 identical)'
	Residual = float(Projected @ Integral)
	Result = {'source': str(Source), 'mechanism': Mechanism, 'A': Integral.tolist(),
		'b': Projected.tolist(), 'true_derivative': Residual,
		'legacy_average_dot': float(Projected @ (Integral / Widths)),
		'passed': abs(Residual) < 1e-12}
	print(json.dumps(Result, indent=2))
	return 0 if Result['passed'] else 1


if __name__ == '__main__':
	sys.exit(main())
