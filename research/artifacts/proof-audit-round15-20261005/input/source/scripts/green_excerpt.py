# Current gtilde_spectral_blocks/gtilde_spectral source bodies, local import adaptation only.
import numpy as np
from physical_excerpt import eigfun
from _sl_spectral_identity import (positive_count, legacy_pole_mode, spectrum_for,
    green_points, spectral_denominators)

def gtilde_spectral_blocks(blocks, lam, k, edges, N=2000, *, spectrum=None):
	"""DD reduced finite sum through mode N+1, with checked legacy index k.

	k is zero-based; the shared contract uses the one-based mode k+1. The
	target lam must uniquely match that mode and every retained denominator
	must be finite and numerically resolvable. N is not a certified tail bound.
	"""
	Count = positive_count(N, 'spectral truncation') + 1
	PoleMode = legacy_pole_mode(k, 'k')
	if PoleMode > Count:
		raise ValueError('pole mode is outside the requested prefix')
	Table = spectrum_for(blocks, 'D', Count, spectrum)
	Points = green_points(Table, edges)
	Modes, Keep, Denominators = spectral_denominators(Table, lam, Count, PoleMode=PoleMode)
	Frequencies = Table.frequency_prefix(Count)[Keep]
	G = np.zeros((len(Points), len(Points)))
	with np.errstate(divide='raise', invalid='raise', over='raise', under='ignore'):
		for Frequency, Denominator in zip(Frequencies, Denominators):
			Values = eigfun(Table.blocks, Frequency, Points)
			if not np.all(np.isfinite(Values)):
				raise ArithmeticError('spectral eigenfunction values are not finite')
			G += np.outer(Values, Values) / Denominator
	if not np.all(np.isfinite(G)):
		raise ArithmeticError('Green spectral sum is not finite')
	return G


def gtilde_spectral(rc, z, lam, k, edges, N=2000, *, spectrum=None):
	"""Full DD wrapper; k retains its checked legacy zero-based meaning."""
	return gtilde_spectral_blocks(rc.blocks_from_z(z), lam, k, edges, N=N, spectrum=spectrum)
