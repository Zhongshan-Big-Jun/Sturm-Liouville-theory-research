from pathlib import Path
Root=Path('/mnt/f/LaTeX/BVE research/scripts')
Own=Path(__file__).resolve().parent
# New multiword parameter follows the project's PascalCase local convention.
for Name in ['_gapn2_symmetry_recon.py','_gapn2_jacobian_analytic.py','_gapn2_half_problem_probe.py']:
	PathName=Root/Name
	Text=PathName.read_text().replace('right_boundary','RightBoundary')
	PathName.write_text(Text)
PathName=Own/'test_round13.py'
Text=PathName.read_text().replace('right_boundary','RightBoundary')
Text=Text.replace("for Boundary in ['D','N']:\n\t\trejects('hyperbolic-overflow-'", "for Boundary in ['D','N']:\n\t\tfor Mu in [0.,-1.,np.nan,np.inf]:\n\t\t\trejects(f'reduced-positive-domain-{Boundary}-{Mu}',lambda:Half.green_regularized([(.5,1)],Mu,.1,.2,Boundary))\n\t\trejects('hyperbolic-overflow-'")
PathName.write_text(Text)
PathName=Root/'_gapn2_half_problem_probe.py'
Text=PathName.read_text().replace('eigfun, solution_states, real_green_matrix','eigfun, solution_states, real_green_matrix, _real_parameter')
Target='\tClosed form: Gt = B - u(x)P(y) (see module docstring), exact A1/A2.\n\t"""\n\tL = sum(b[0] for b in hblocks)'
Replacement='\tClosed form: Gt = B - u(x)P(y) (see module docstring), exact A1/A2.\n\tThis positive-eigenvalue formula is not an ordinary resolvent at mu<=0.\n\t"""\n\tmu = _real_parameter(mu, \'eigenvalue\')\n\tif mu <= 0:\n\t\traise ValueError(\'reduced Green requires a positive eigenvalue; use green_regular at mu<=0\')\n\tL = sum(b[0] for b in hblocks)'
if Target not in Text:
	raise RuntimeError('exact reduced-Green edit target is missing')
PathName.write_text(Text.replace(Target,Replacement))
print('Adjusted new local naming and made reduced-Green positive-eigenvalue domain explicit.')
