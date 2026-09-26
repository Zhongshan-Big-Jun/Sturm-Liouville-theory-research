"""Independent, bounded review tests; no source mutation or universal inference."""
from dataclasses import FrozenInstanceError
import importlib
import json
from pathlib import Path
import sys
import traceback
import numpy as np
import mpmath as mp

audit = Path(__file__).resolve().parent
root = audit / 'payload'
sys.path.insert(0, str(root / 'scripts'))
import _sl_prufer as phase
import _gapn2_half_problem_probe as half
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_jacobian_spectral import analytic_jacobian_spectral
from _gapn2_sector_decomposition import sector_data

records = []
failures = []


def require(condition, detail=''):
    if not bool(condition):
        raise RuntimeError(str(detail))


def case(name, operation):
    try:
        result = operation()
        records.append({'name': name, 'status': 'PASS', 'result': result})
    except Exception as error:
        record = {'name': name, 'status': 'FAIL', 'type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc()}
        records.append(record)
        failures.append(record)


def reject(operation):
    try:
        operation()
    except (ValueError, ArithmeticError) as error:
        return {'exception': type(error).__name__, 'message': str(error)}
    raise RuntimeError('Input was silently accepted')


def constant_phase():
    blocks = [(0.7, 3.25)]
    out = {}
    for bc in ('D', 'N'):
        w, metadata = phase.indexed_roots(blocks, 65, RightBoundary=bc)
        exact = (np.arange(1, 66) - (0.5 if bc == 'N' else 0)) * np.pi / (0.7 * np.sqrt(3.25))
        error = float(np.max(abs(w / exact - 1)))
        require(error < 4e-15, error)
        for count in (1, 2, 7, 31):
            require(np.array_equal(w[:count], phase.indexed_roots(blocks, count, RightBoundary=bc)[0]), count)
        for i, row in enumerate(metadata):
            require(row['index'] == i + 1 and row['right_boundary'] == bc and row['certified'] is False)
            require(row['phase_bracket'][0] <= row['target_phase'] <= row['phase_bracket'][1])
        out[bc] = error
    require(np.array_equal(phase.indexed_roots(blocks, 7)[0], phase.indexed_roots(blocks, 7, RightBoundary='D')[0]))
    require(np.array_equal(roots_of(blocks, 7, npts=1), phase.indexed_roots(blocks, 7)[0]))
    require(float(phase.lifted_phase(blocks, 0.)) == 0.)
    return out


case('constant-DD-DN-first-mode-prefix-default-API', constant_phase)


def exact_interfaces():
    examples = [([(0.25, 1.), (0.125, 4.)], 'D', 2, 4*np.pi),
                ([(0.25, 1.), (0.25, 4.)], 'N', 2, 2*np.pi),
                ([(0.125, 4.), (0.5, 1.)], 'N', 2, 2*np.pi)]
    errors = []
    for blocks, bc, mode, exact in examples:
        w, _ = phase.indexed_roots(blocks, 8, RightBoundary=bc)
        error = abs(float(w[mode-1]/exact-1))
        require(error < 4e-15, (blocks, bc, error))
        errors.append(error)
    for scale in (0.125, 0.5, 2., 8.):
        for k in range(9):
            integer = k*np.pi
            half_turn = (k+0.5)*np.pi
            require(abs(float(phase._angle_scale(integer, scale))-integer) < 2e-14)
            require(abs(float(phase._angle_scale(half_turn, scale))-half_turn) < 2e-14)
            neighbourhood = integer + np.array([-1e-8, 0., 1e-8]) if k else np.array([0., 1e-8, 2e-8])
            mapped = phase._angle_scale(neighbourhood, scale)
            require(np.all(np.diff(mapped) > 0), (scale, k, mapped.tolist()))
    return errors


case('integer-half-integer-interface-levels-and-neighbourhoods', exact_interfaces)

# Reference integration uses (y,y') transfer, not a lifted-angle recurrence.
mp.mp.dps = 85


def transfer_reference(blocks, frequency, bc, zeros=False):
    y, yp = mp.mpf(0), mp.mpf(1)
    offset = mp.mpf(0)
    total = sum(mp.mpf(float(length)) for length, _ in blocks)
    interior = []
    for length, density in blocks:
        length, density = mp.mpf(float(length)), mp.mpf(float(density))
        k = frequency*mp.sqrt(density)
        if zeros:
            local_angle = mp.atan2(y, yp/k)
            a = int(mp.floor(local_angle/mp.pi))-1
            b = int(mp.ceil((local_angle+k*length)/mp.pi))+1
            for j in range(a, b+1):
                t = (j*mp.pi-local_angle)/k
                position = offset+t
                if -mp.mpf('1e-65') <= t <= length+mp.mpf('1e-65') and mp.mpf('1e-60') < position < total-mp.mpf('1e-60'):
                    if all(abs(position-p) > mp.mpf('1e-60') for p in interior):
                        interior.append(position)
        c, s = mp.cos(k*length), mp.sin(k*length)
        y, yp = y*c+yp*s/k, -k*y*s+yp*c
        offset += length
    return len(interior) if zeros else (y if bc == 'D' else yp)


def layered_transfer():
    samples = [[(0.17, 0.3), (0.04, 25.), (0.29, 2.)],
               [(0.003, 900.), (0.397, 0.8), (0.1, 7.)],
               [(0.25, 1.), (0.125, 4.)],
               [(0.25, 1.), (0.25, 4.)]]
    output = []
    for blocks in samples:
        for bc in ('D', 'N'):
            w, _ = phase.indexed_roots(blocks, 40, RightBoundary=bc)
            require(np.array_equal(w[:3], phase.indexed_roots(blocks, 3, RightBoundary=bc)[0]))
            for mode in (1, 2, 3, 9, 23, 40):
                start = mp.mpf(float(w[mode-1]))
                root_w = mp.findroot(lambda s: transfer_reference(blocks, s, bc),
                                     (start*(1-mp.mpf('1e-6')), start*(1+mp.mpf('1e-6'))), tol=mp.mpf('1e-75'))
                count = transfer_reference(blocks, root_w, bc, zeros=True)
                relerr = float(abs(mp.mpf(float(w[mode-1]))/root_w-1))
                require(count == mode-1 and relerr < 2e-12, (blocks, bc, mode, count, relerr))
                output.append({'blocks': blocks, 'bc': bc, 'mode': mode, 'interior_zeros': count, 'frequency_relative_error': relerr})
    return output


case('independent-85-digit-layer-transfer-and-nodal-index', layered_transfer)

for name, operation in [
    ('unresolved-cumulative-endpoint', lambda: half.half_spectrum([(1., 1.), (1e-20, 2.)], 'D', 2)),
    ('optical-underflow', lambda: half.half_spectrum([(1e-250, 1e-200)], 'N', 2)),
    ('frequency-overflow', lambda: phase.indexed_roots([(1e-300, 1e-20)], 2)),
    ('eigenvalue-overflow', lambda: half.half_spectrum([(1e-154, 1.)], 'D', 2)),
    ('eigenvalue-underflow', lambda: half.half_spectrum([(1e170, 1.)], 'N', 2)),
    ('excessive-phase-winding', lambda: phase.indexed_roots([(0.5, 1.), (0.5, 1e30)], 3)),
    ('insufficient-refinement', lambda: phase.indexed_roots([(0.2, 1.), (0.3, 5.)], 4, Refine=2, RightBoundary='N')),
    ('zero-refinement', lambda: phase.indexed_roots([(0.5, 1.)], 2, Refine=0)),
    ('invalid-boolean-count', lambda: half.half_spectrum([(0.5, 1.)], 'D', np.bool_(True))),
]:
    case(name, lambda operation=operation: reject(operation))


def immutable_table():
    blocks = np.array([[0.2, 1.], [0.3, 4.]])
    table = half.half_spectrum(blocks, 'N', 16, return_table=True)
    old = table.eigenvalues
    blocks[:] = 7
    require(table.blocks == ((0.2, 1.), (0.3, 4.)))
    prefix = table.prefix(4)
    prefix[:] = -1
    require(table.eigenvalues == old)
    try:
        table.boundary = 'D'
    except FrozenInstanceError:
        pass
    else:
        raise RuntimeError('Frozen assignment accepted')
    require(isinstance(table.phase_records, tuple) and all(isinstance(record, tuple) for record in table.phase_records))
    return {'input_detached': True, 'prefix_detached': True, 'frozen_assignment_rejected': True}


case('supported-table-immutability', immutable_table)


def analytic_constant_sums():
    length, density, count = 0.8, 7., 32
    blocks = [(length, density)]
    errors = []
    for bc in ('D', 'N'):
        table = half.half_spectrum(blocks, bc, count, return_table=True)
        wave = (np.arange(1,count+1)-(0.5 if bc=='N' else 0))*np.pi/length
        lambdas = wave**2/density
        for prefix in (2, 7, 32):
            for x,y in ((0., 0.37), (0.21, 0.37), (length, length), (length, 0.31)):
                products = 2/(density*length)*np.sin(wave[:prefix]*x)*np.sin(wave[:prefix]*y)
                keep = np.arange(prefix) != 1
                mu = table.eigenvalues[1]
                exact = np.sum(products[keep]/(lambdas[:prefix][keep]-mu))
                actual = half._spectral_green(blocks, mu, 1, bc, x, y, prefix, spectrum=table)
                errors.append(abs(actual-exact))
                for target in (0., -3., float((lambdas[2]+lambdas[3])/2)):
                    expected = np.sum(products/(lambdas[:prefix]-target))
                    got = half._spectral_full_green(blocks, target, bc, x, y, prefix, spectrum=table)
                    errors.append(abs(got-expected))
                require(abs(actual-half._spectral_green(blocks, mu, 1, bc, y, x, prefix, spectrum=table)) < 2e-15)
        empty_sum = half._spectral_green(blocks, table.eigenvalues[0], 0, bc, .2, .3, 1, spectrum=table)
        require(empty_sum == 0.)
    require(max(errors) < 2e-13, max(errors))
    return {'max_absolute_error': float(max(errors)), 'comparisons': len(errors), 'empty_reduced_prefix': 0.}


case('closed-sine-finite-Green-DD-DN-endpoints-negative-targets', analytic_constant_sums)

blocks = [(0.5, 100.)]
table = half.half_spectrum(blocks, 'N', 24, return_table=True)
mu = table.eigenvalues[1]
for name, operation in [
    ('wrong-pole-mode', lambda: half._spectral_green(blocks, mu, 0, 'N', .1, .2, 12, spectrum=table)),
    ('wrong-target', lambda: half._spectral_green(blocks, table.eigenvalues[4], 1, 'N', .1, .2, 12, spectrum=table)),
    ('wrong-density', lambda: half._spectral_green([(0.5,101.)], mu, 1, 'N', .1, .2, 12, spectrum=table)),
    ('wrong-length', lambda: half._spectral_green([(np.nextafter(.5,1.),100.)], mu, 1, 'N', .1, .2, 12, spectrum=table)),
    ('wrong-boundary', lambda: half._spectral_green(blocks, mu, 1, 'D', .1, .2, 12, spectrum=table)),
    ('pole-outside-prefix', lambda: half._spectral_green(blocks, mu, 1, 'N', .1, .2, 1, spectrum=table)),
    ('prefix-too-long', lambda: half._spectral_green(blocks, mu, 1, 'N', .1, .2, 25, spectrum=table)),
    ('non-table-object', lambda: half._spectral_green(blocks, mu, 1, 'N', .1, .2, 12, spectrum=table.prefix(24))),
    ('near-retained-pole', lambda: half._spectral_full_green(blocks, np.nextafter(table.eigenvalues[6], 0.), 'N', .1, .2, 12, spectrum=table)),
    ('near-tail-pole-outside-prefix', lambda: half._spectral_full_green(blocks, np.nextafter(table.eigenvalues[20], 0.), 'N', .1, .2, 4, spectrum=table)),
    ('target-above-covered-table', lambda: half._spectral_full_green(blocks, 2*table.eigenvalues[-1], 'N', .1, .2, 4, spectrum=table)),
    ('right-endpoint-exceeded', lambda: half._spectral_green(blocks, mu, 1, 'N', .1, np.nextafter(.5,1.), 12, spectrum=table)),
    ('invalid-negative-pole-index', lambda: half._spectral_green(blocks, mu, -1, 'N', .1, .2, 12, spectrum=table)),
    ('nonfinite-target', lambda: half._spectral_full_green(blocks, float('inf'), 'N', .1, .2, 12, spectrum=table)),
]:
    case(name, lambda operation=operation: reject(operation))


def direct_summand_projection():
    seeds = json.loads((root/'scripts/op03_gap_table.json').read_text())
    outputs = []
    for n in (2,3):
        for mode in ('sup','inf'):
            rc = Recon(n,4.,mode)
            e0 = np.array(seeds[f'n{n}_{mode.upper()}']['edges'])
            z = symmetric_root(rc,rc.widths_to_z(np.diff(np.r_[0.,e0,1.])))
            require(z is not None)
            data = eigen_data(rc,z)
            ln,lp = data['lam_n'],data['lam_np1']
            u,eps = data['u_n'],data['eps']
            S = np.diag(eps)
            U = np.diag(u)
            c2 = ln/lp
            v = u*u
            r = 2*ln*(lp-ln)/lp**2
            jumps = np.diff(rc.pat)
            local = (2*ln*data['u_n']*data['up_n']-2*lp*data['u_np1']*data['up_np1'])/(lp*jumps)
            eye = np.eye(2*n)
            Be = (eye[:,:n]+eye[:,::-1][:,:n])/np.sqrt(2)
            Bo = (eye[:,:n]-eye[:,::-1][:,:n])/np.sqrt(2)
            Efull = r*np.outer(eps*v,eps*v)-2*ln*(1+c2*c2)/(lp-ln)*np.outer(v,v)
            fd, geometry = jac_fd(rc,z,return_diagnostics=True)
            Kfd = np.diag(1/jumps)@fd
            for N in (n+1,17,80,160):
                w = roots_of(rc.blocks_from_z(z),N+1)
                Hfull = np.zeros((2*n,2*n))
                for j,frequency in enumerate(w):
                    if j in (n-1,n):
                        continue
                    phi = eigfun(rc.blocks_from_z(z),frequency,data['edges'])
                    outer = np.outer(phi,phi)
                    Hfull += 2*ln*U@(outer/(frequency**2-lp)-c2*S@outer@S/(frequency**2-ln))@U
                raw = np.diag(local)+Hfull+Efull
                sector = sector_data(rc,z,N=N)
                expected = {'Ke':Be.T@raw@Be,'Ko':Bo.T@raw@Bo,
                            'KpEven':Be.T@S@raw@S@Be,'KpOdd':Bo.T@S@raw@S@Bo,
                            'He':Be.T@Hfull@Be,'Ho':Bo.T@Hfull@Bo,
                            'Ee':Be.T@Efull@Be,'Eo':Bo.T@Efull@Bo,
                            'KpHe':Be.T@S@Hfull@S@Be,'KpHo':Bo.T@S@Hfull@S@Bo,
                            'KpEe':Be.T@S@Efull@S@Be,'KpEo':Bo.T@S@Efull@S@Bo}
                errors = {key:float(np.max(abs(np.array(sector[key])-value))) for key,value in expected.items()}
                require(max(errors.values())<3e-8, (n,mode,N,errors))
                js = np.diag(1/jumps)@analytic_jacobian_spectral(rc,z,N=N)
                full_error = float(np.max(abs(raw-js)))
                require(full_error<3e-8,full_error)
                require(sector['coefficient_target']=='c_e/c_o belong to KpEe/KpEo')
                wh = ln*v[:n]
                require(np.max(abs(np.array(sector['KpEe'])-sector['c_e']*np.outer(wh,wh)))<1e-12)
                require(np.max(abs(np.array(sector['KpEo'])-sector['c_o']*np.outer(eps[:n]*wh,eps[:n]*wh)))<1e-12)
                outputs.append({'n':n,'mode':mode,'N_argument':N,'actual_modes':len(w),'summand_errors':errors,
                                'full_jacobian_error':full_error,'finite_tail_vs_FD':float(np.max(abs(raw-Kfd))),
                                'FD_max_geometry_error':max(row['max_motion_error'] for row in geometry['columns'])})
    return outputs


case('independent-raw-full-summands-projected-into-all-sector-keys', direct_summand_projection)


def legacy_import_and_calls():
    debug2 = importlib.import_module('_gapn2_half_debug2')
    debug3 = importlib.import_module('_gapn2_half_debug3')
    require(debug2._spectral_green is half._spectral_green and debug3._spectral_green is half._spectral_green)
    blocks = [(0.2,4.),(0.2,1.),(.1,4.)]
    errors = []
    for bc,pole in (('D',0),('N',1)):
        table = half.half_spectrum(blocks,bc,80,return_table=True)
        mu = table.eigenvalues[pole]
        u0 = 1/np.sqrt(half._norm2(blocks,mu,(0.,1.)))
        vf = half.second_solution(blocks,mu)
        a1,a2 = half._a1a2_exact(blocks,mu,u0)
        for x,y in ((.2,.2),(.2,.4),(.4,.4),(.4,.2)):
            b = debug3.bracket(blocks,mu,x,y,u0,vf)
            other = debug2.gprime_bracket(blocks,mu,x,y,u0,vf)
            require(abs(b-other)<1e-14)
            cf = b-u0*half._propagate(blocks,mu,x)[0]*debug2.pbracket(blocks,mu,y,u0,vf,a1,a2)
            require(abs(cf-half.green_regularized(blocks,mu,x,y,bc))<1e-14)
            sp = debug2._spectral_green(blocks,mu,pole,bc,x,y,80,spectrum=table)
            require(np.isfinite(sp))
            errors.append(float(abs(sp-cf)))
    return {'legacy_changed_calls_finite':True,'largest_finite_80_mode_tail':max(errors),'historical_main_routines_executed':False}


case('legacy-module-imports-and-targeted-shared-table-calls', legacy_import_and_calls)

output = {'status':'PASS' if not failures else 'FAIL','records':records,'failures':failures,
          'scope':'finite tests and formula inspection only; no interval or universal certification'}
(audit/'adversarial-results.json').write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
print(json.dumps({'status':output['status'],'cases':len(records),'failures':failures},indent=2))
sys.exit(0 if not failures else 1)
