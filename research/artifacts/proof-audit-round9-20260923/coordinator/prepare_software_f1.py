from pathlib import Path
import json,shutil,hashlib
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round9-20260923');D=O/'software-f1-author';D.mkdir()
for N in ['_gapn2_second_variation_probe.py','_gapn2_symmetry_recon.py','_gapn2_jacobian_probe.py','_gapn2_jacobian_analytic.py','op03_gap_table.json']:shutil.copyfile(R/'scripts'/N,D/N)
P=D/'_gapn2_second_variation_probe.py';S=P.read_text()
Function='''def checked_bump_breaks(Blocks, Centers, HalfWidth, Order):
	"""Reject unresolved fixed-width bumps; this is no quadrature certificate.

	Keep at least 2**20 coordinate spacings per half-width, so endpoint
	rounding cannot silently remove a finite fraction of the requested mass.
	Also check the actual interval quadrature nodes, including high orders.
	"""
	Centers = finite_vector(Centers, 'bump centers')
	HalfWidth = positive_scalar(HalfWidth, 'bump width')
	Blocks = validate_blocks(Blocks)
	Total = float(np.sum([L for L, _ in Blocks]))
	Left, Right = Centers - HalfWidth, Centers + HalfWidth
	if np.any(Left <= 0) or np.any(Right >= Total):
		raise ValueError('bumps must remain inside the domain')
	Spacing = np.spacing(np.abs(Centers))
	if np.any(HalfWidth < (2 ** 20) * Spacing):
		raise ValueError('bump width cannot be resolved reliably in double-precision coordinates')
	if np.any(Left >= Centers) or np.any(Right <= Centers):
		raise ValueError('bump support endpoints collapse in double precision')
	RadiusErrors = np.r_[np.abs((Centers - Left) / HalfWidth - 1),
		np.abs((Right - Centers) / HalfWidth - 1)]
	if np.any(RadiusErrors > 1e-6):
		raise ValueError('bump support rounding changes the requested width')
	Breaks = tuple(np.r_[Left, Right])
	Points, _, Knots = quadrature_rule(Blocks, Order, Breaks)
	Rows = Points.reshape(len(Knots) - 1, Order)
	if (np.any(np.diff(Rows, axis=1) <= 0)
		or np.any(Rows[:, 0] <= Knots[:-1]) or np.any(Rows[:, -1] >= Knots[1:])):
		raise ValueError('bump quadrature nodes cannot be resolved in double-precision coordinates')
	return Breaks


'''
if 'def checked_bump_breaks(' in S:raise RuntimeError('Already repaired')
S=S.replace('class SpectralProbe:',Function+'class SpectralProbe:',1)
S=S.replace('\tWidths = np.array([L for L, _ in Blocks])\n\tProbe =', '\tWidths = np.array([L for L, _ in Blocks])\n\tif IncludeP3:\n\t\tchecked_bump_breaks(Blocks, np.cumsum(Widths)[:-1], BumpWidth, Order)\n\tProbe =',1)
S=S.replace('\t\tBreaks = tuple(np.r_[Edges - BumpWidth, Edges + BumpWidth])','\t\tBreaks = checked_bump_breaks(Blocks, Edges, BumpWidth, Order)',1)
S=S.replace('failure of a limiting identity. No bump-width limit is evaluated here.','failure of a limiting identity. No bump-width limit is evaluated here.\nUnresolved supports or quadrature nodes are rejected before producing P3 values.',1)
P.write_text(S)
Rows={N:hashlib.sha256((D/N).read_bytes()).hexdigest() for N in [X.name for X in D.iterdir() if X.is_file()]}
(D/'input-manifest.json').write_text(json.dumps(dict(author='01a06f46-dd03-7c83-9267-32048412c359',files=Rows),indent=2)+'\n')
(D/'AGENTS.md').write_text('# Software F1 repair\n\nCoordinator author only; fresh independent acceptance must follow. Frozen first candidate/review remain unchanged. Reject unresolved bump supports and verify normal/-O behavior plus unchanged default results. Work only in this external directory until the original rejection has been received by the library.\n')
print('Candidate prepared',Rows['_gapn2_second_variation_probe.py'])
