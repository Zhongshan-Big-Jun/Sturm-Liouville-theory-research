"""Author regressions. Only AST-selected Recon geometry methods are executed."""

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from reflection_seeds import (
	SeedGenerationError,
	SeedValidationError,
	ZeroProjectionError,
	check_sector_seed,
	generate_sector_seed,
	interfaces_to_widths,
	reflection_direction,
)


SourcePath = Path('/mnt/f/LaTeX/BVE research/scripts/_gapn2_symmetry_recon.py')
SourceEvidence = {}
SeedEvidence = {}
SourceBytes = None


def load_recon_geometry():
	global SourceBytes
	if SourceBytes is None:
		SourceBytes = SourcePath.read_bytes()
	Source = SourceBytes
	Tree = ast.parse(Source, filename=str(SourcePath))
	ReconNode = next(Node for Node in Tree.body if isinstance(Node, ast.ClassDef) and Node.name == 'Recon')
	MethodNames = ('widths_to_z', 'z_to_widths')
	Methods = [Node for Node in ReconNode.body if isinstance(Node, ast.FunctionDef) and Node.name in MethodNames]
	if len(Methods) != 2:
		raise RuntimeError('Expected exactly the two Recon conversion methods')
	Namespace = {'np': np}
	for Method in Methods:
		if Method.decorator_list:
			raise RuntimeError('Unexpected decorated conversion method')
		exec(compile(ast.Module(body=[Method], type_ignores=[]), str(SourcePath), 'exec'), Namespace)
	GeometryClass = type('ReconGeometry', (), {Name: Namespace[Name] for Name in MethodNames})
	Geometry = GeometryClass()
	Geometry.nb = 5
	SourceEvidence.update({
		'Path': str(SourcePath),
		'Sha256': hashlib.sha256(Source).hexdigest(),
		'MethodSha256': {
			Method.name: hashlib.sha256(ast.get_source_segment(Source.decode('utf-8'), Method).encode()).hexdigest()
			for Method in Methods
		},
		'MethodSource': {Method.name: ast.get_source_segment(Source.decode('utf-8'), Method) for Method in Methods},
		'ExecutionScope': 'Only the two AST-selected conversion methods; no module import, main or spectral functions',
	})
	return Geometry


class SequenceRng:
	def __init__(self, Vectors):
		self.Vectors = Vectors
		self.Calls = 0

	def standard_normal(self, Size):
		Vector = self.Vectors[min(self.Calls, len(self.Vectors) - 1)]
		self.Calls += 1
		if len(Vector) != Size:
			raise ValueError('Test fixture has the wrong size')
		return np.asarray(Vector, dtype=float)


class ReflectionTests(unittest.TestCase):
	def test_vector_1234_projectors_and_complementarity(self):
		Vector = np.array([1., 2., 3., 4.])
		Preserve = reflection_direction(Vector, 'preserve')
		Break = reflection_direction(Vector, 'break')
		assert_array_equal(Preserve, [-1.5, -0.5, 0.5, 1.5])
		assert_array_equal(Break, [2.5, 2.5, 2.5, 2.5])
		assert_array_equal(Preserve + Break, Vector)
		self.assertEqual(float(Preserve @ Break), 0.)
		assert_array_equal(reflection_direction(Preserve, 'preserve'), Preserve)
		assert_array_equal(reflection_direction(Break, 'break'), Break)
		assert_array_equal(Vector, [1., 2., 3., 4.])

	def test_normalized_and_extreme_finite_directions(self):
		for Sector in ('preserve', 'break'):
			for Scale in (1., 1e300, 1e-300):
				with self.subTest(Sector=Sector, Scale=Scale):
					Direction = reflection_direction(Scale * np.arange(1., 5.), Sector, Normalize=True)
					self.assertAlmostEqual(float(np.linalg.norm(Direction)), 1.)
					Sign = -1 if Sector == 'preserve' else 1
					assert_array_equal(Direction, Sign * Direction[::-1])

	def test_zero_projection_is_never_a_direction(self):
		for Sector, Vector in (('preserve', [1, 2, 2, 1]), ('break', [1, 2, -2, -1]), ('preserve', [0, 0]), ('preserve', [1])):
			for Normalize in (False, True):
				with self.subTest(Sector=Sector, Vector=Vector, Normalize=Normalize):
					with self.assertRaises(ZeroProjectionError):
						reflection_direction(Vector, Sector, Normalize=Normalize)

	def test_illegal_projector_inputs(self):
		for Vector in ([], 1., [[1, 2]], [np.nan, 1], [np.inf, 1], [1 + 1j, 2], ['1', '2'], [True, False]):
			with self.subTest(Vector=Vector), self.assertRaises(ValueError):
				reflection_direction(Vector, 'preserve')
		for Sector in ('sym', 'antisym', '', None, 0):
			with self.subTest(Sector=Sector), self.assertRaises(ValueError):
				reflection_direction([1, 2], Sector)

	def test_odd_dimension_and_middle_interface(self):
		Direction = reflection_direction([1, 2, 3], 'preserve')
		assert_array_equal(Direction, [-1, 0, 1])
		Seed = generate_sector_seed([0.2, 0.5, 0.8], 'preserve', 0.05, Vector=[1, 2, 3])
		self.assertEqual(Seed.Edges[1], 0.5)
		with self.assertRaises(SeedGenerationError):
			generate_sector_seed([0.5], 'preserve', 0.01, Rng=SequenceRng([[1]]), MaxResamples=3)


class SeedTests(unittest.TestCase):
	def setUp(self):
		self.BaseEdges = np.array([0.1, 0.3, 0.7, 0.9])
		self.Geometry = load_recon_geometry()

	def make_seed(self, Sector='break', Step=0.01, **Options):
		return generate_sector_seed(self.BaseEdges, Sector, Step, Vector=[1, 2, 3, 4], **Options)

	def test_geometry_without_callbacks_and_public_checker(self):
		for Sector in ('preserve', 'break'):
			Seed = self.make_seed(Sector)
			Check = check_sector_seed(Seed.BaseEdges, Seed.Widths, Sector, Direction=Seed.Direction, ExpectedStep=Seed.UsedStep)
			self.assertIsNone(Seed.Z)
			self.assertLessEqual(Check['SectorRelativeResidual'], 1e-8)
			assert_allclose(Seed.Edges, np.cumsum(Seed.Widths)[:-1], atol=0, rtol=0)
			assert_allclose(Check['Displacement'], np.array(Seed.Edges) - self.BaseEdges, atol=0, rtol=0)
			self.assertTrue(all(Width > 1e-7 for Width in Check['InterfaceWidths']))
			self.assertAlmostEqual(Seed.ActualStep, Seed.UsedStep)
			self.assertEqual(Seed.Evidence['Origin'], 'pure_reflection_sector')
			self.assertEqual(Seed.Evidence['DirectionSource'], 'provided_vector')
			json.dumps(Seed.to_dict(), allow_nan=False)
			SeedEvidence['direct_' + Sector] = Seed.to_dict()

	def test_large_invalid_step_is_halved_without_sorting_or_clipping(self):
		Seed = self.make_seed('preserve', 10.)
		self.assertGreater(Seed.Evidence['Halvings'], 0)
		self.assertEqual(Seed.UsedStep, 10. * 0.5 ** Seed.Evidence['Halvings'])
		Target = self.BaseEdges + Seed.UsedStep * np.array(Seed.Direction)
		assert_array_equal(Seed.Evidence['TargetEdges'], Target)
		assert_array_equal(Seed.Widths, np.diff(np.r_[0., Target, 1.]))
		self.assertTrue(np.all(np.diff(Seed.Edges) > 0))
		self.assertTrue(np.all(np.asarray(Seed.Widths) > 1e-7))
		self.assertTrue(any(Attempt['Status'] == 'infeasible_target' for Attempt in Seed.Evidence['Attempts']))
		SeedEvidence['halved_large_step'] = Seed.to_dict()

	def test_actual_recon_softmax_roundtrip_has_the_requested_sector(self):
		for Sector in ('preserve', 'break'):
			for Step in (1e-5, 1e-3, 0.1, 1.0):
				with self.subTest(Sector=Sector, Step=Step):
					Seed = self.make_seed(Sector, Step, WidthsToZ=self.Geometry.widths_to_z, ZToWidths=self.Geometry.z_to_widths)
					Widths = self.Geometry.z_to_widths(Seed.Z)
					assert_array_equal(Widths, Seed.Widths)
					Actual = np.cumsum(Widths)[:-1] - np.asarray(Seed.BaseEdges)
					self.assertGreater(float(np.linalg.norm(Actual)), 1e-14)
					Sign = -1 if Sector == 'preserve' else 1
					assert_allclose(Actual, Sign * Actual[::-1], rtol=1e-8, atol=1e-16)
					assert_allclose(Actual, Seed.UsedStep * np.array(Seed.Direction), rtol=1e-8, atol=1e-16)
					if Sector == 'preserve':
						assert_allclose(np.array(Seed.Edges) + np.array(Seed.Edges)[::-1], 1., atol=2e-15, rtol=0)
					else:
						self.assertGreater(np.max(np.abs(np.array(Seed.Edges) + np.array(Seed.Edges)[::-1] - 1.)), 1e-6)
					SeedEvidence[f'softmax_{Sector}_{Step}'] = Seed.to_dict()

	def test_recon_clipping_is_detected_and_smaller_safe_step_used(self):
		BaseEdges = [3e-7, 0.3, 0.7, 1. - 3e-7]
		for Sector, Vector, Step in (('preserve', [-1, 0, 0, 1], 2.5e-7), ('break', [1, 1, 1, 1], 3.2e-7)):
			with self.subTest(Sector=Sector):
				Seed = generate_sector_seed(BaseEdges, Sector, Step, Vector=Vector, WidthsToZ=self.Geometry.widths_to_z, ZToWidths=self.Geometry.z_to_widths)
				self.assertGreater(Seed.Evidence['Halvings'], 0)
				self.assertEqual(Seed.Evidence['Attempts'][0]['Status'], 'rejected_roundtrip')
				self.assertGreater(min(Seed.Evidence['Attempts'][0]['TargetWidths']), 1e-7)
				self.assertLess(min(Seed.Evidence['Attempts'][0]['TargetWidths']), 2e-7)
				self.assertLess(Seed.Evidence['FinalCheck']['ExpectedRelativeResidual'], 1e-8)
				SeedEvidence['clipping_guard_' + Sector] = Seed.to_dict()

	def test_clipped_same_sector_is_not_accepted_with_wrong_step(self):
		BaseEdges = [3e-7, 0.3, 0.7, 1. - 3e-7]
		Direction = reflection_direction([-1, 0, 0, 1], 'preserve', Normalize=True)
		Step = 2.5e-7
		Widths = interfaces_to_widths(np.array(BaseEdges) + Step * Direction)
		ActualWidths = self.Geometry.z_to_widths(self.Geometry.widths_to_z(Widths))
		Check = check_sector_seed(BaseEdges, ActualWidths, 'preserve')
		self.assertLess(Check['SectorRelativeResidual'], 1e-8)
		with self.assertRaises(SeedValidationError):
			check_sector_seed(BaseEdges, ActualWidths, 'preserve', Direction=Direction, ExpectedStep=Step)

	def test_asymmetric_base_is_rejected_even_if_it_is_ordered(self):
		for SymmetrizeBase in (False, True):
			with self.subTest(SymmetrizeBase=SymmetrizeBase), self.assertRaises(ValueError):
				generate_sector_seed([0.1, 0.31, 0.7, 0.9], 'break', 0.01, Vector=[1, 2, 3, 4], SymmetrizeBase=SymmetrizeBase)

	def test_tolerance_symmetrization_is_explicit_and_recorded(self):
		BaseEdges = self.BaseEdges.copy()
		BaseEdges[0] += 5e-13
		with self.assertRaises(ValueError):
			generate_sector_seed(BaseEdges, 'break', 0.01, Vector=[1, 2, 3, 4])
		Seed = generate_sector_seed(BaseEdges, 'break', 0.01, Vector=[1, 2, 3, 4], SymmetrizeBase=True)
		self.assertTrue(Seed.Evidence['BaseWasSymmetrized'])
		assert_array_equal(Seed.Evidence['InputBaseEdges'], BaseEdges)
		assert_array_equal(np.array(Seed.BaseEdges) + np.array(Seed.BaseEdges)[::-1], np.ones(4))
		self.assertGreater(Seed.Evidence['BaseCorrectionMax'], 0.)
		self.assertLess(Seed.Evidence['BaseCorrectionMax'], 5e-13)
		SeedEvidence['explicit_base_symmetrization'] = Seed.to_dict()

	def test_invalid_base_step_and_options(self):
		for Base in ([0, .3, .7, 1], [.1, .7, .3, .9], [.1, .1, .9, .9], [1e-7, .3, .7, 1 - 1e-7], [np.nan, .3, .7, .9], [[.1, .3, .7, .9]]):
			with self.subTest(Base=Base), self.assertRaises(ValueError):
				generate_sector_seed(Base, 'preserve', .01, Vector=[1, 2, 3, 4])
		for Step in (0, -1, np.nan, np.inf, True):
			with self.subTest(Step=Step), self.assertRaises(ValueError):
				self.make_seed(Step=Step)
		for Options in ({'MinWidth': 0}, {'MinWidth': 1e-8}, {'MaxResamples': 0}, {'MaxHalvings': -1}, {'SectorTolerance': 1}, {'RoundTripTolerance': 1}, {'SymmetryTolerance': .1}, {'WidthsToZ': self.Geometry.widths_to_z}, {'ZToWidths': self.Geometry.z_to_widths}):
			with self.subTest(Options=Options), self.assertRaises(ValueError):
				self.make_seed(**Options)
		with self.assertRaises(ValueError):
			generate_sector_seed(self.BaseEdges, 'break', .01)
		with self.assertRaises(ValueError):
			self.make_seed(Rng=np.random.default_rng(1))
		with self.assertRaises(ValueError):
			generate_sector_seed(self.BaseEdges, 'break', .01, Vector=[1, 2])

	def test_zero_rng_projection_resamples_and_is_bounded(self):
		Rng = SequenceRng([[1, 1, 1, 1], [1, 2, 3, 4]])
		Seed = generate_sector_seed(self.BaseEdges, 'preserve', .01, Rng=Rng, MaxResamples=3)
		self.assertEqual(Rng.Calls, 2)
		self.assertEqual(len(Seed.Evidence['Draws']), 2)
		self.assertEqual(Seed.Evidence['DirectionSource'], 'projected_rng')
		Rng = SequenceRng([[1, 1, 1, 1]])
		with self.assertRaises(SeedGenerationError) as Caught:
			generate_sector_seed(self.BaseEdges, 'preserve', .01, Rng=Rng, MaxResamples=3)
		self.assertEqual(Rng.Calls, 3)
		self.assertEqual(len(Caught.exception.Evidence['Draws']), 3)
		SeedEvidence['bounded_zero_rng_failure'] = Caught.exception.Evidence

	def test_tiny_nonzero_requested_step_cannot_become_fake_seed(self):
		with self.assertRaises(SeedGenerationError) as Caught:
			self.make_seed(Step=1e-300)
		self.assertIn('resolvable', str(Caught.exception))
		SeedEvidence['unresolved_step_failure'] = Caught.exception.Evidence

	def test_converter_returning_base_is_rejected(self):
		BaseWidths = interfaces_to_widths(self.BaseEdges)
		with self.assertRaises(SeedGenerationError):
			self.make_seed(WidthsToZ=lambda Widths: Widths, ZToWidths=lambda Z: BaseWidths)

	def test_converter_introducing_wrong_sector_is_rejected(self):
		def wrong_sector(Widths):
			Edges = np.cumsum(Widths)[:-1]
			Delta = Edges - self.BaseEdges
			BadEdges = self.BaseEdges + np.linalg.norm(Delta) * np.array([-.5, -.5, .5, .5])
			return np.diff(np.r_[0., BadEdges, 1.])
		with self.assertRaises(SeedGenerationError) as Caught:
			self.make_seed(WidthsToZ=lambda Widths: Widths, ZToWidths=wrong_sector, MaxHalvings=4)
		self.assertEqual(len(Caught.exception.Evidence['Attempts']), 5)
		self.assertTrue(all(Attempt['Status'] == 'rejected_roundtrip' for Attempt in Caught.exception.Evidence['Attempts']))

	def test_invalid_callback_geometry_is_rejected(self):
		for Widths in ([.2] * 4, [.21] * 5, [1e-7, .25, .25, .25, .25 - 1e-7], [np.nan] * 5):
			with self.subTest(Widths=Widths), self.assertRaises((SeedGenerationError, ValueError)):
				self.make_seed(WidthsToZ=lambda Value: Value, ZToWidths=lambda Z: Widths, MaxHalvings=2)

	def test_callback_mutation_cannot_corrupt_stored_inputs(self):
		def encode(Widths):
			Z = self.Geometry.widths_to_z(Widths)
			Widths[:] = 0.
			return Z
		def decode(Z):
			Widths = self.Geometry.z_to_widths(Z)
			Z[:] = 0.
			return Widths
		Seed = self.make_seed(WidthsToZ=encode, ZToWidths=decode)
		assert_allclose(self.Geometry.z_to_widths(Seed.Z), Seed.Widths, rtol=0, atol=0)
		self.assertTrue(all(Width > 1e-7 for Width in Seed.Evidence['TargetWidths']))
		assert_array_equal(self.BaseEdges, [.1, .3, .7, .9])

	def test_public_checker_rejects_wrong_sector_and_zero_actual_move(self):
		Seed = self.make_seed()
		with self.assertRaises(SeedValidationError):
			check_sector_seed(self.BaseEdges, Seed.Widths, 'preserve')
		with self.assertRaises(SeedValidationError):
			check_sector_seed(self.BaseEdges, interfaces_to_widths(self.BaseEdges), 'break')

	def test_finite_seeded_sweep_and_reproducibility(self):
		for Sector in ('preserve', 'break'):
			FirstRng = np.random.default_rng(20260925)
			SecondRng = np.random.default_rng(20260925)
			for Index in range(16):
				Options = dict(WidthsToZ=self.Geometry.widths_to_z, ZToWidths=self.Geometry.z_to_widths)
				First = generate_sector_seed(self.BaseEdges, Sector, .2, Rng=FirstRng, **Options)
				Second = generate_sector_seed(self.BaseEdges, Sector, .2, Rng=SecondRng, **Options)
				self.assertEqual(First.to_dict(), Second.to_dict())
				self.assertLess(First.Evidence['FinalCheck']['SectorRelativeResidual'], 1e-8)


def main():
	global SourcePath
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument('--recon-source', dest='ReconSource', type=Path, default=SourcePath)
	Parser.add_argument('--evidence', dest='EvidencePath', type=Path)
	Arguments = Parser.parse_args()
	SourcePath = Arguments.ReconSource
	Suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
	Result = unittest.TextTestRunner(verbosity=2).run(Suite)
	if Arguments.EvidencePath:
		Payload = {
			'Role': 'implementation_author_self_checks_not_independent_acceptance',
			'RunUTC': datetime.now(timezone.utc).isoformat(),
			'Python': sys.version,
			'NumPy': np.__version__,
			'AuthorFileSha256': {
				Name: hashlib.sha256(Path(__file__).with_name(Name).read_bytes()).hexdigest()
				for Name in ('reflection_seeds.py', 'test_reflection_seeds.py')
			},
			'ReconSource': SourceEvidence,
			'TestsRun': Result.testsRun,
			'Success': Result.wasSuccessful(),
			'Failures': [(str(Test), Trace) for Test, Trace in Result.failures + Result.errors],
			'Cases': SeedEvidence,
		}
		Arguments.EvidencePath.write_text(json.dumps(Payload, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
	return 0 if Result.wasSuccessful() else 1


if __name__ == '__main__':
	raise SystemExit(main())
