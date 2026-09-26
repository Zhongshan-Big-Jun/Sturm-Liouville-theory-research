# -*- coding: utf-8 -*-
"""Reconnaissance: are all self-consistent stationary points of D_n = lambda_{n+1}-lambda_n
(within the (2n+1)-block bang-bang family, 1<=rho<=R, Dirichlet) reflection-symmetric?

Method: solve the band self-consistency system f(x_j) = 0, j=1..2n, where
f = lambda_n u_n^2 - lambda_{n+1} u_{n+1}^2, from many random seeds AND from
checked preserve/break reflection-sector seeds at mirror-symmetric bases.  For every root we
report: D, asymmetry max_j |x_j + x_{2n+1-j} - 1|, band-matching.

Usage:  python _gapn2_symmetry_recon.py [n] [R] [seeds] [mode] [workers]
mode in {both, sup, inf}
"""
import sys, json, time, argparse, hashlib
from pathlib import Path
from reflection_seeds import generate_sector_seed, SeedGenerationError
import numpy as np
from scipy.optimize import least_squares

# ----------------------------------------------------------------------------
# spectral engine (transfer matrix, Dirichlet)
# ----------------------------------------------------------------------------
from _sl_prufer import indexed_roots


def roots_of(blocks, k, npts=20000, refine=60):
	"""First k Dirichlet frequencies, indexed by lifted phase n*pi.

	Numerical only, not interval-certified. npts remains an unused compatibility
	argument; no frequency scan is performed. Unresolved enumeration raises.
	"""
	return indexed_roots(blocks, k, refine)[0]


def D_scalar(blocks, s):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    for L, c in blocks:
        w = s * np.sqrt(c); wL = w * L
        cw = np.cos(wL); sw = L * np.sinc(wL / np.pi); sw2 = -w * np.sin(wL)
        M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, \
                             sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
    return M01


def eigfun(blocks, s, pts):
    """Normalized eigenfunction values at pts (L^2(rho) normalization)."""
    xs = [0.0]
    for L, _ in blocks:
        xs.append(xs[-1] + L)
    starts = []
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    starts.append((0.0, M00, M01, M10, M11))
    for L, c in blocks:
        w = s * np.sqrt(c); wL = w * L
        cw = np.cos(wL); sw = L * np.sinc(wL / np.pi); sw2 = -w * np.sin(wL)
        M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, \
                             sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
        starts.append((xs[len(starts)], M00, M01, M10, M11))
    norm = 0.0
    for bi, (L, c) in enumerate(blocks):
        _, M00, M01, M10, M11 = starts[bi]
        w = s * np.sqrt(c)
        A = M01; B = M11 / w
        Icos = 0.5 * (L + np.sin(2 * w * L) / (2 * w))
        Isin = 0.5 * (L - np.sin(2 * w * L) / (2 * w))
        Icross = np.sin(w * L) ** 2 / (2 * w)
        norm += c * (A * A * Icos + B * B * Isin + 2 * A * B * Icross)
    out = np.zeros(len(pts))
    for j, p in enumerate(pts):
        bi = max(i for i in range(len(xs) - 1) if xs[i] <= p)
        _, M00, M01, M10, M11 = starts[bi]
        L, c = blocks[bi]
        w = s * np.sqrt(c); d = p - xs[bi]
        out[j] = M01 * np.cos(w * d) + (M11 / w) * np.sin(w * d)
    return out / np.sqrt(norm)


class Recon:
    def __init__(self, n, R, mode):
        self.n = n
        self.R = R
        self.mode = mode  # 'sup' or 'inf'
        self.start_val = 1.0 if mode == 'sup' else R
        self.alt_val = R if mode == 'sup' else 1.0
        self.nb = 2 * n + 1
        self.pat = [self.start_val if i % 2 == 0 else self.alt_val for i in range(self.nb)]

    def z_to_widths(self, z):
        """softmax parameterization: strictly feasible widths, sum = 1."""
        z = np.asarray(z, dtype=float)
        ez = np.exp(z - np.max(z))
        sm = ez / np.sum(ez)
        return (1.0 - self.nb * 1e-7) * sm + 1e-7

    def widths_to_z(self, widths):
        """inverse softmax (up to shift): z_i = log(width_i - 1e-7)."""
        w = np.asarray(widths, dtype=float)
        w = np.clip(w, 2e-7, 1.0 - 2e-7)
        w = w / np.sum(w)
        return np.log(w - 1e-7)

    def blocks_from_z(self, z):
        w = self.z_to_widths(z)
        return [(float(w[i]), self.pat[i]) for i in range(self.nb)]

    def f_at(self, z, pts):
        """f = lam_n u_n^2 - lam_{n+1} u_{n+1}^2 at pts (normalized)."""
        blocks = self.blocks_from_z(z)
        ss = roots_of(blocks, self.n + 1)
        lam_n = ss[self.n - 1] ** 2
        lam_np1 = ss[self.n] ** 2
        u_n = eigfun(blocks, ss[self.n - 1], pts)
        u_np1 = eigfun(blocks, ss[self.n], pts)
        return lam_n * u_n ** 2 - lam_np1 * u_np1 ** 2, lam_n, lam_np1

    def residual(self, z):
        z = np.asarray(z, dtype=float)
        w = self.z_to_widths(z)
        edges = np.cumsum(w)[:-1]  # 2n interior switch points
        f, lam_n, lam_np1 = self.f_at(z, edges)
        return f / lam_np1

    def full_report(self, z):
        z = np.asarray(z, dtype=float)
        w = self.z_to_widths(z)
        edges = np.cumsum(w)[:-1]
        mids = np.cumsum(w) - 0.5 * w  # block midpoints
        f_e, lam_n, lam_np1 = self.f_at(z, edges)
        f_m, _, _ = self.f_at(z, mids)
        D = lam_np1 - lam_n
        n = self.n
        asym = max(abs(edges[j] + edges[2 * n - 1 - j] - 1.0) for j in range(2 * n))
        # band matching (delta D = int delta-rho f dx, numerically verified):
        #   SUP: f>0 on rho=R blocks, f<0 on rho=1 blocks;
        #   INF: f>0 on rho=1 blocks, f<0 on rho=R blocks
        expect = []
        for i in range(self.nb):
            if self.mode == 'sup':
                expect.append(1.0 if self.pat[i] == self.R else -1.0)
            else:
                expect.append(1.0 if self.pat[i] == 1.0 else -1.0)
        expect = np.array(expect)
        band_min = float(np.min(np.abs(f_m) / lam_np1))
        band_ok = bool(np.all(np.sign(f_m) == expect) and band_min > 1e-6)
        return dict(edges=edges.tolist(), widths=w.tolist(), D=float(D),
                    lam_n=float(lam_n), lam_np1=float(lam_np1),
                    asym=float(asym), band_ok=band_ok,
                    band_min=band_min,
                    res_max=float(np.max(np.abs(f_e) / lam_np1)))

    def solve(self, z0, max_nfev=250):
        res = least_squares(self.residual, np.asarray(z0, dtype=float),
                            xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=max_nfev)
        return res


def cluster_solutions(sols, tol=1e-6):
    kept = []
    for s in sols:
        e = np.array(s['edges'])
        dup = False
        for k in kept:
            if np.max(np.abs(e - np.array(k['edges']))) < tol:
                dup = True
                break
        if not dup:
            kept.append(s)
    return kept


def one_solve(job):
    """job = (n, R, mode, z0, label). Returns report dict or None."""
    n, R, mode, z0, label, *metadata = job
    rc = Recon(n, R, mode)
    r = rc.solve(z0)
    if np.max(np.abs(r.fun)) >= 1e-7:
        return None
    rep = rc.full_report(r.x)
    rep['seed'] = label
    if metadata:
        rep['seed_geometry'] = metadata[0]
    rep['cost'] = float(np.max(np.abs(r.fun)))
    return rep


def sector_jobs(Rc, Center, Rng, BreakRepeats=16, PreserveRepeats=8):
	"""Build initial seeds; subsequent optimization is not sector constrained."""
	Jobs, Records = [], []
	for Sector, Steps, Repeats in (
		('break', (1e-5, 1e-4, 1e-3, 1e-2, 3e-2, 1e-1, 2e-1), BreakRepeats),
		('preserve', (1e-4, 1e-2, 5e-2), PreserveRepeats)):
		for Step in Steps:
			for Index in range(Repeats):
				Label = f'pure_reflection:{Sector}:{Step}:{Index}'
				try:
					Seed = generate_sector_seed(Center, Sector, Step, Rng=Rng,
						WidthsToZ=Rc.widths_to_z, ZToWidths=Rc.z_to_widths, SymmetrizeBase=True)
				except (ValueError, SeedGenerationError) as Error:
					Records.append(dict(label=Label, status='rejected_seed', sector=Sector,
						reason=str(Error), evidence=getattr(Error, 'Evidence', {})))
					continue
				Record = dict(label=Label, status='accepted_seed', **Seed.to_dict())
				Records.append(Record)
				Jobs.append((Rc.n, Rc.R, Rc.mode, np.asarray(Seed.Z), Label, Record))
	return Jobs, Records


def main(argv=None):
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument('n', nargs='?', type=int, default=2)
	Parser.add_argument('R', nargs='?', type=float, default=4.0)
	Parser.add_argument('seeds', nargs='?', type=int, default=200)
	Parser.add_argument('mode', nargs='?', choices=('both', 'sup', 'inf'), default='both')
	Parser.add_argument('workers', nargs='?', type=int, default=8)
	Parser.add_argument('--output-dir', type=Path, help='directory for results and actual seed evidence')
	Parser.add_argument('--table', type=Path)
	Parser.add_argument('--break-repeats', type=int, default=16)
	Parser.add_argument('--preserve-repeats', type=int, default=8)
	Args = Parser.parse_args(argv)
	if (Args.n < 1 or not np.isfinite(Args.R) or Args.R < 1 or Args.seeds < 0
		or Args.workers < 1 or Args.break_repeats < 0 or Args.preserve_repeats < 0):
		Parser.error('require n/workers>=1, finite R>=1 and nonnegative seed counts')
	import multiprocessing as mp
	Started = time.time()
	Rng = np.random.default_rng(20260812)
	Output = Args.output_dir or Path(__file__).resolve().parent
	Output.mkdir(parents=True, exist_ok=True)
	TablePath = Args.table or Path(__file__).resolve().parent / 'op03_gap_table.json'
	Known, TableError = {}, None
	try:
		Table = json.loads(TablePath.read_text(encoding='utf-8'))
		for Mode in ('sup', 'inf'):
			Key = f'n{Args.n}_{Mode.upper()}'
			if Key in Table:
				Known[Mode] = np.asarray(Table[Key]['edges'], dtype=float)
	except (OSError, ValueError, KeyError, TypeError) as Error:
		TableError = str(Error)
	Sources = [Path(__file__).resolve(), Path(__file__).resolve().parent/'_sl_prufer.py',
		Path(__file__).resolve().parent/'reflection_seeds.py']
	if TablePath.is_file():
		Sources.append(TablePath.resolve())
	Identities = {str(Source): hashlib.sha256(Source.read_bytes()).hexdigest() for Source in Sources}
	with mp.Pool(processes=Args.workers) as Pool:
		for Mode in (['sup', 'inf'] if Args.mode == 'both' else [Args.mode]):
			Rc = Recon(Args.n, Args.R, Mode)
			print(f'=== n={Args.n} R={Args.R} mode={Mode}; finite sampled evidence ===', flush=True)
			Jobs, RandomRecords = [], []
			for Index in range(Args.seeds):
				Widths = Rng.dirichlet(np.ones(Rc.nb))
				Z = Rc.widths_to_z(Widths)
				Label = f'random_width:{Index}'
				Jobs.append((Args.n, Args.R, Mode, Z, Label))
				RandomRecords.append(dict(label=Label, origin='random_width',
					requested_widths=Widths.tolist(), actual_widths=Rc.z_to_widths(Z).tolist()))
			Results = Pool.map(one_solve, Jobs, chunksize=1)
			Solutions = [Result for Result in Results if Result is not None]
			Center, CenterSource = None, None
			if Mode in Known and len(Known[Mode]) == 2 * Args.n:
				Center, CenterSource = Known[Mode], 'stored R4 table geometry; stationarity at requested R is not assumed'
			else:
				Candidates = [Row for Row in Solutions if Row['band_min'] > 1e-7 and Row['asym'] <= 1e-12]
				if Candidates:
					Center = np.asarray(min(Candidates, key=lambda Row: Row['asym'])['edges'])
					CenterSource = 'computed mirror-symmetric numerical root'
			PerturbationJobs, SectorRecords = [], []
			if Center is not None:
				PerturbationJobs, SectorRecords = sector_jobs(Rc, Center, Rng, Args.break_repeats, Args.preserve_repeats)
				Results = Pool.map(one_solve, PerturbationJobs, chunksize=1)
				Solutions.extend(Result for Result in Results if Result is not None)
			Unique = cluster_solutions(Solutions)
			print(f'  accepted pure seeds={len(PerturbationJobs)} rejected={sum(Row["status"]=="rejected_seed" for Row in SectorRecords)}', flush=True)
			print(f'  converged roots={len(Solutions)}, distinct sampled roots={len(Unique)}', flush=True)
			for Index, Row in enumerate(sorted(Unique, key=lambda Value: Value['D'])):
				print(f'  [{Index}] D={Row["D"]:.10f} asym={Row["asym"]:.3e} band={Row["band_ok"]} res={Row["res_max"]:.2e}', flush=True)
			Stem = f'_gapn2_symmetry_recon_n{Args.n}_{Mode}'
			(Output/(Stem+'.json')).write_text(json.dumps(Unique, indent=2, allow_nan=False)+'\n', encoding='utf-8')
			Evidence = dict(scope='finite numerical experiment; sectors label initial seeds only; no uniqueness or interval certificate',
				n=Args.n, R=Args.R, mode=Mode, random_seed=20260812, source_sha256=Identities,
				table_error=TableError, center=None if Center is None else Center.tolist(), center_source=CenterSource,
				random_seeds=RandomRecords, sector_seeds=SectorRecords, converged=len(Solutions), distinct=len(Unique))
			(Output/(Stem+'-seeds.json')).write_text(json.dumps(Evidence, indent=2, allow_nan=False)+'\n', encoding='utf-8')
	print(f'total wall time {time.time()-Started:.2f}s', flush=True)
	return 0


if __name__ == '__main__':
	sys.exit(main())
