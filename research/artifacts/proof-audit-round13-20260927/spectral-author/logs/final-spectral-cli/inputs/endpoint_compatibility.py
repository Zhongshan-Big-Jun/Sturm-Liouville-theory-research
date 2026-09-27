from pathlib import Path
Root=Path('/mnt/f/LaTeX/BVE research/scripts')
Own=Path(__file__).resolve().parent
PathName=Root/'_gapn2_symmetry_recon.py'
Text=PathName.read_text()
Text=Text.replace('def _propagation_input(blocks, mu, pts):','def _propagation_input(blocks, mu, pts, *, EndpointRoundoff=False):')
Text=Text.replace("\tif np.any(Points < 0) or np.any(Points > Ends[-1]):\n\t\traise ValueError('evaluation point lies outside the interval')\n\treturn Blocks, Mu, Points, Ends", "\tTolerance = 8 * len(Blocks) * np.finfo(float).eps * Ends[-1] if EndpointRoundoff else 0.0\n\tif np.any(Points < -Tolerance) or np.any(Points > Ends[-1] + Tolerance):\n\t\traise ValueError('evaluation point lies outside the interval')\n\tif EndpointRoundoff:\n\t\tPoints = np.clip(Points, 0.0, Ends[-1])\n\treturn Blocks, Mu, Points, Ends")
Text=Text.replace('\tNo normalization is reconstructed from point values, even at nodes.','\tNo normalization is reconstructed from point values, even at nodes.\n\tOnly this normalized sampler snaps endpoint roundoff within 8*m*eps*L,\n\tfor legacy unit-interval grids whose block sums differ by a few ulps.\n\tGreen/unnormalized propagation retain strict coordinate rejection.')
Text=Text.replace('_propagation_input(blocks, np.float64(Frequency)**2, pts)','_propagation_input(blocks, np.float64(Frequency)**2, pts, EndpointRoundoff=True)')
PathName.write_text(Text)
PathName=Own/'test_round13.py'
Text=PathName.read_text()
Target="\tfor Point in [-1e-9,1.00001,np.nan,np.inf]:"
Insertion="\tRoundoffBlocks=[(.1,1.),(.2,4.),(.3,1.),(.3999999999999998,4.)]\n\tEnd=float(np.cumsum(np.array(RoundoffBlocks)[:,0])[-1])\n\tclose('normalized-endpoint-roundoff',ReconModule.eigenfunction_states(RoundoffBlocks,3,[1.]),ReconModule.eigenfunction_states(RoundoffBlocks,3,[End]),0)\n\trejects('Green-keeps-strict-endpoint',lambda:Analytic.green_kernel(RoundoffBlocks,0,[1.]))\n"
if Target not in Text:
	raise RuntimeError('test insertion target missing')
PathName.write_text(Text.replace(Target,Insertion+Target))
print('Bounded endpoint-roundoff compatibility only for normalized sampling; Green stays strict.')
