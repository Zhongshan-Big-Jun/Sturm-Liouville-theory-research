import ast
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
import traceback

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
mp.mp.dps = 100
GATES = []
REPORT = {"execution_role": "fresh independent finite-check verifier", "supplemental_precision_digits": 100}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read(rel):
    return json.loads((ROOT / rel).read_text())

def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

def gate(label, condition, details=None):
    result = {"name": label, "passed": bool(condition)}
    if details is not None:
        result["details"] = details
    GATES.append(result)
    return result["passed"]

def num(value):
    return mp.mpf(str(value))

def text(value):
    return mp.nstr(value, 80)

def numerical_gate(label, value, expected, tolerance):
    err = abs(value - expected)
    gate(label, err <= mp.mpf(tolerance), {"absolute_error": text(err), "tolerance": tolerance})
    return err

def main():
    packet = read("PACKET.json")
    initial = read(str(OUT.relative_to(ROOT) / "input_hashes.before.json"))
    after = []
    for previous in initial["records"]:
        rel = previous["path"]
        data = (ROOT / rel).read_bytes()
        sha = digest(data)
        row = {"path": rel, "size_bytes": len(data), "sha256": sha, "unchanged_from_before": sha == previous["sha256"]}
        if rel in packet["files"]:
            row["matches_packet"] = sha == packet["files"][rel]
        gate("input unchanged and bound: " + rel, row["unchanged_from_before"] and row.get("matches_packet", True))
        after.append(row)
    write(OUT / "input_hashes.after.json", {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "records": after})
    preflight = read(str(OUT.relative_to(ROOT) / "preflight.json"))
    gate("manifest and all four snapshot entries supplied", preflight["snapshot_count"] == 4 and preflight["all_snapshots_supplied_and_bound"])
    source_groups = preflight["static_inspection"]["checks.py"]["groups"]
    expected_names = [g["name"] for g in source_groups]
    gate("source has 25 unique named groups", len(expected_names) == len(set(expected_names)) == 25)
    gate("checks and runner contain no Python assert gates", all(v["assert_count"] == 0 for v in preflight["static_inspection"].values()))

    outer = read(str(OUT.relative_to(ROOT) / "outer.execution.json"))
    gate("actual required outer argv and cwd", outer["argv"] == ["/usr/bin/python3", "-B", "run_checks.py"] and outer["cwd"] == str(ROOT))
    gate("outer exited zero without timeout", outer["returncode"] == 0 and not outer["outer_timeout"])
    gate("all 15 runner outputs observed as fresh", len(outer["generated_outputs"]) == 15 and not outer["expected_outputs_not_observed_as_fresh"])
    for row in outer["generated_outputs"]:
        gate("fresh output hash: " + row["path"], digest((ROOT / row["path"]).read_bytes()) == row["sha256"])
    for channel in ["stdout", "stderr"]:
        data = (ROOT / outer[channel + "_path"]).read_bytes()
        gate("outer " + channel + " capture binding", digest(data) == outer[channel + "_sha256"] and data.decode() == outer[channel])

    runtime = {"python": sys.version, "executable": sys.executable, "python_binary_resolved": str(Path(sys.executable).resolve()), "python_binary_sha256": digest(Path(sys.executable).read_bytes()), "sympy": sp.__version__, "mpmath": mp.__version__, "package_entrypoints": [{"path": mod.__file__, "sha256": digest(Path(mod.__file__).read_bytes())} for mod in [sp, mp]], "runtime_hash_scope": "Interpreter binary and package entrypoints only; not a dependency-closure hash of the installed runtime."}
    write(OUT / "runtime.json", runtime)
    cases = [("normal", [], "outputs.json", 0), ("optimized", ["-O"], "outputs.optimized.json", 0), ("negative-normal-old-fh", [], None, 1), ("negative-optimized-old-fh", ["-O"], None, 1)]
    processes = []
    for name, opts, output, expected_code in cases:
        receipt = read("receipts/" + name + ".execution.json")
        actual_argv = ["/usr/bin/python3", "-B"] + opts + [str(ROOT / "checks.py")]
        actual_argv += ["--output", output] if output else ["--negative-control", "old-fh"]
        gate(name + " process identity", receipt["argv"] == actual_argv and receipt["cwd"] == str(ROOT))
        gate(name + " actual expected exit", receipt["returncode"] == receipt["expected_exitcode"] == expected_code)
        gate(name + " source hash bindings", receipt["checks_sha256"] == packet["files"]["checks.py"] and receipt["runner_sha256"] == packet["files"]["run_checks.py"])
        for channel in ["stdout", "stderr"]:
            data = (ROOT / receipt[channel + "_path"]).read_bytes()
            gate(name + " " + channel + " binding", digest(data) == receipt[channel + "_sha256"])
            receipt[channel] = data.decode()
        if output:
            gate(name + " payload binding", digest((ROOT / output).read_bytes()) == receipt["output_sha256"])
            gate(name + " empty stderr", receipt["stderr"] == "")
        else:
            pattern = r"RuntimeError: intentional old FH formula rejection: error=([0-9.eE+-]+)\s*$"
            match = re.search(pattern, receipt["stderr"])
            gate(name + " intentional formula failure, not unrelated crash", bool(match) and num(match.group(1)) > 20 and receipt["stdout"] == "")
            receipt["observed_old_formula_absolute_error"] = match.group(1) if match else None
        processes.append(receipt)
    REPORT["child_processes"] = processes

    normal, optimized = read("outputs.json"), read("outputs.optimized.json")
    for label, payload, opt, receipt in [("normal", normal, 0, processes[0]), ("optimized", optimized, 1, processes[1])]:
        groups = payload["groups"]
        gate(label + " counts independently recomputed", len(groups) == 25 and sum(g["status"] == "PASS" for g in groups) == 25 and payload["passed_groups"] == payload["total_groups"] == 25 and payload["failed_groups"] == 0)
        gate(label + " exact source group names and order", [g["name"] for g in groups] == expected_names)
        gate(label + " group kinds match source", [g["kind"] for g in groups] == [g["kind"] for g in source_groups])
        gate(label + " all groups have substantive detail records", all(bool(g.get("details")) and "error" not in g for g in groups))
        expected_stdout = "".join("PASS " + name + "\n" for name in expected_names) + "25/25 groups passed; optimize=" + str(opt) + "\n"
        gate(label + " 25 distinct actual stdout PASS lines", receipt["stdout"] == expected_stdout)
        gate(label + " optimization and debug flags", payload["optimize"] == opt and payload["__debug__"] == (opt == 0))
        gate(label + " runtime and precision", payload["python"] == sys.version and payload["executable"] == "/usr/bin/python3" and payload["mpmath"] == mp.__version__ and payload["sympy"] == sp.__version__ and payload["decimal_precision"] == 90)
        gate(label + " payload input identities", payload["checks_sha256"] == packet["files"]["checks.py"] and payload["input_manifest_sha256"] == packet["files"]["inputs/manifest.json"])
    def stable(payload):
        return [{k: g[k] for k in ["name", "kind", "status", "details"]} for g in payload["groups"]]
    a, b = stable(normal), stable(optimized)
    gate("normal/-O all named mathematical details equal", a == b)
    canonical = lambda obj: json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    REPORT["normal_optimized_equality"] = {"equal": a == b, "fields": ["name", "kind", "status", "details"], "canonical_serialization": "UTF-8 JSON, sorted keys, ensure_ascii=False, separators comma/colon; no trailing newline", "normal_sha256": digest(canonical(a)), "optimized_sha256": digest(canonical(b)), "excluded_fields": ["elapsed_seconds", "optimize", "__debug__"], "raw_output_files_equal": (ROOT/"outputs.json").read_bytes() == (ROOT/"outputs.optimized.json").read_bytes()}
    REPORT["kind_counts"] = dict(Counter(g["kind"] for g in a))
    REPORT["category_counts"] = {"symbolic_or_exact_mathematics": sum(g["kind"] not in ["high_precision_finite", "high_precision_counterexample", "execution_integrity"] for g in a), "high_precision_real_numeric": sum(g["kind"] in ["high_precision_finite", "high_precision_counterexample"] for g in a), "execution_bookkeeping": sum(g["kind"] == "execution_integrity" for g in a)}
    REPORT["groups"] = a
    byname = {g["name"]: g["details"] for g in a}

    # Recheck reported finite sample cardinalities and arithmetic, not just PASS labels.
    gate("Chebyshev exact sample set and two identities per n", byname["W_finite_exact_Chebyshev_certificates"] == {"n": [1, 2, 3, 4, 5, 8, 12], "identities_per_n": 2})
    plateau = byname["trial_plateau_bound_finite_exact_instances"]["instances"]
    gram = byname["center_vanishing_subspace_finite_Gram_bounds"]["cases"]
    spectral = byname["thin_density_spectral_bound_samples"]["samples"]
    gate("20 plateau cases", [(r["n"], r["R"]) for r in plateau] == [(n,R) for n in [1,2,3,5,8] for R in [8,1000,1000000,1000000000]])
    gate("12 finite polynomial Gram cases and 45 cells", [(r["n"],r["R"]) for r in gram] == [(n,R) for n in [1,2,3,5] for R in [8,1000,1000000]] and sum(r["cells_checked"] for r in gram) == 45)
    gate("four spectral samples", [(r["n"],r["R"]) for r in spectral] == [(1,1000),(2,1000),(3,1000),(2,1000000)])
    for row in spectral:
        gate("reported spectral inequalities " + str((row["n"],row["R"])), 0 < num(row["lambda_n"]) <= num(row["upper_lambda_n"]) and num(row["lower_lambda_n_plus_1"]) <= num(row["lambda_n_plus_1"]) <= num(row["upper_cap"]))
    shooting = byname["nonstationary_shooting_index_and_residual"]
    fhdata = byname["symmetric_FH_vs_independent_central_difference"]
    fh = num(fhdata["FH"])
    gate("nonstationary sample", abs(num(shooting["f_a"])) > 1 and abs(fh) > 50)
    numerical_gate("reported derivative is -6 f(a)", fh, -6*num(shooting["f_a"]), "1e-62")
    gate("three distinct central difference steps", [r["h"] for r in fhdata["differences"]] == ["1e-5","1e-8","1e-11"])
    errors=[]
    for row in fhdata["differences"]:
        err=abs(num(row["central_difference"])-fh)
        numerical_gate("reported FD error " + row["h"], err, num(row["error"]), "1e-62")
        errors.append(err)
    gate("second order convergence at each step", all(errors[i+1] < errors[i]*num("2e-6") for i in range(2)))
    gate("mirrored derivative finite tolerance", errors[-1] <= num("1e-18"))
    numerical_gate("one interface differs by mirror factor two", num(byname["one_interface_parameter_has_no_mirror_factor"]["central_difference"]), fh/2, "1e-18")
    for rec in processes[2:]:
        numerical_gate(rec["name"] + " observed wrong-formula discrepancy", num(rec["observed_old_formula_absolute_error"]), abs(num(fhdata["differences"][-1]["central_difference"])-num(byname["legacy_symmetric_formula_is_half"]["old"])), "1e-62")

    # New finite exact computations: no import or execution of checks.py here.
    x, n, t = sp.symbols("x n t", real=True)
    u, v = sp.sqrt(2)*sp.sin(2*sp.pi*x), sp.sqrt(2)*sp.sin(3*sp.pi*x)
    w = sp.simplify((u*sp.diff(v,x)-v*sp.diff(u,x)).subs(x,sp.Rational(1,2)))
    coeff = sp.expand(sp.series(4*sp.pi**2*u**2-9*sp.pi**2*v**2,x,0,4).removeO()).coeff(x,2)
    gate("independent W(1/2)=-4pi", sp.simplify(w+4*sp.pi)==0)
    gate("independent n2 coefficient=-130pi^4", sp.simplify(coeff+130*sp.pi**4)==0)
    # Product over both algebraic roots via a polynomial resultant, without radical root substitution.
    P=sp.Poly(144*t**2-88*t+9,t)
    B=sp.Poly(t*(1-t)**3*sp.diff(P.as_expr(),t)**2,t)
    product=sp.resultant(P.as_expr(),B.as_expr(),t)/P.LC()**B.degree()
    determinant=sp.simplify((16*sp.pi**2/81)**2*product)
    expected_det=sp.Rational(7030400000,4782969)*sp.pi**4
    gate("independent normalized determinant by resultant", sp.simplify(determinant-expected_det)==0)
    REPORT["independent_exact_samples"]={"wronskian_n2_half":str(w),"n2_x2_coefficient":str(coeff),"n2_four_interface_determinant":str(determinant),"determinant_method":"resultant of P(t)=144t^2-88t+9 and t(1-t)^3 P'(t)^2, using product over both roots; normalized F=f/(9*pi^2)"}

    # Alternative half-interval formulation: Neumann/Dirichlet conditions at x=1/2.
    # At a=1/4 the seeds are closed-form roots, separate from the frozen phase solver.
    a0=mp.mpf(1)/4
    seeds=[4*mp.acos(mp.sqrt(mp.mpf(5)/6)),4*mp.acos(1/mp.sqrt(3))]
    def characteristic(s,a,mode):
        alpha=s*a
        beta=2*s*(mp.mpf(1)/2-a)
        if mode==0:
            return mp.cos(alpha)*mp.cos(beta)-2*mp.sin(alpha)*mp.sin(beta)
        return mp.sin(alpha)*mp.cos(beta)+mp.cos(alpha)*mp.sin(beta)/2
    def root(a,mode):
        seed=seeds[mode]
        return mp.findroot(lambda s:characteristic(s,a,mode),(seed*num("0.999"),seed*num("1.001")),tol=num("1e-95"))
    lambdas=[]
    u_squares=[]
    implicit_derivatives=[]
    masses=[]
    residuals=[]
    for mode,s in enumerate(seeds):
        eigenvalue=s*s
        lambdas.append(eigenvalue)
        numerical_gate("half-domain closed root residual " + str(mode+1),characteristic(s,a0,mode),mp.mpf(0),"1e-95")
        numerical_gate("half-domain independently known eigenvalue " + str(mode+1),eigenvalue,num(shooting["lambda_"+str(mode+1)]),"1e-62")
        y1=lambda xx:mp.sin(s*xx)/s
        ya,dya=y1(a0),mp.cos(s*a0)
        y2=lambda xx:ya*mp.cos(2*s*(xx-a0))+dya*mp.sin(2*s*(xx-a0))/(2*s)
        mass=2*(mp.quad(lambda xx:y1(xx)**2,[0,a0])+4*mp.quad(lambda xx:y2(xx)**2,[a0,mp.mpf(1)/2]))
        u2=ya*ya/mass
        implicit=-2*s*mp.diff(lambda aa:characteristic(s,aa,mode),a0)/mp.diff(lambda ss:characteristic(ss,a0,mode),s)
        numerical_gate("half-domain eigenvalue derivative " + str(mode+1),implicit,6*eigenvalue*u2,"1e-90")
        masses.append(mass)
        u_squares.append(u2)
        implicit_derivatives.append(implicit)
        residuals.append(characteristic(s,a0,mode))
    independent_fh=6*(lambdas[1]*u_squares[1]-lambdas[0]*u_squares[0])
    implicit_gap=implicit_derivatives[1]-implicit_derivatives[0]
    h=num("1e-12")
    fresh_roots=[]
    for aa in [a0+h,a0-h]:
        roots=[root(aa,mode) for mode in [0,1]]
        fresh_roots.append(roots)
        for mode,s in enumerate(roots):
            numerical_gate("perturbed half-domain root residual " + text(aa) + " mode=" + str(mode),characteristic(s,aa,mode),mp.mpf(0),"1e-90")
    fd=((fresh_roots[0][1]**2-fresh_roots[0][0]**2)-(fresh_roots[1][1]**2-fresh_roots[1][0]**2))/(2*h)
    numerical_gate("independent half-domain FH versus frozen output",independent_fh,fh,"1e-62")
    numerical_gate("independent implicit versus FH derivative",implicit_gap,independent_fh,"1e-90")
    numerical_gate("independent perturbed-root FD versus FH",fd,independent_fh,"1e-20")
    gate("independent old formula fails substantially",abs(fd-independent_fh/2)>20)
    REPORT["independent_nonstationary_mirror_sample"]={"model":"-u''=lambda*rho*u; Dirichlet endpoints; rho=(1,4,1) at a=1/4,1-a=3/4; both interfaces move", "method":"Independent half-domain characteristic roots with Neumann first mode and Dirichlet second mode; weighted normalization by quadrature; implicit derivative and separately perturbed root finite difference. No checker import.","closed_form_sqrt_lambdas":["4*acos(sqrt(5/6))","4*acos(1/sqrt(3))"],"lambda_values":[text(v) for v in lambdas],"weighted_masses":[text(v) for v in masses],"normalized_u_a_squared":[text(v) for v in u_squares],"characteristic_residuals":[text(v) for v in residuals],"individual_implicit_derivatives":[text(v) for v in implicit_derivatives],"FH_gap_derivative":text(independent_fh),"implicit_gap_derivative":text(implicit_gap),"finite_difference_h":text(h),"perturbed_sqrt_lambdas":[[text(v) for v in row] for row in fresh_roots],"finite_difference":text(fd),"FD_absolute_error":text(abs(fd-independent_fh)),"old_half_formula":text(independent_fh/2),"old_formula_absolute_error":text(abs(fd-independent_fh/2)),"scope":"One finite nonstationary example at 100-digit working precision. Numerical tolerances are not certified interval enclosures."}
    summary=read("receipts/execution-summary.json")
    gate("runner summary agrees with independently inspected results",summary["mathematical_results_identical"] is True and summary["normal"]=={"passed":25,"total":25,"optimize":0} and summary["optimized"]=={"passed":25,"total":25,"optimize":1} and summary["intentional_old_fh_negative_controls"]=={"normal_exit":1,"optimized_exit":1,"expected_exit":1})
    REPORT["provenance_labels"]={"frozen_checker_payload_role":normal["role"],"frozen_runner_summary_role":summary["role"],"interpretation":"These unchanged author strings describe code provenance. This execution and its verification were performed by the fresh independent verifier."}

try:
    main()
except Exception as exc:
    REPORT["unexpected_error"]={"type":type(exc).__name__,"message":str(exc),"traceback":traceback.format_exc()}
    gate("verification completed without exception",False)
REPORT["verification_gates"]=GATES
REPORT["passed_verification_gates"]=sum(g["passed"] for g in GATES)
REPORT["failed_verification_gates"]=[g for g in GATES if not g["passed"]]
REPORT["verdict"]="PASS" if not REPORT["failed_verification_gates"] else "INCOMPLETE"
write(OUT/"verification.json",REPORT)
print(json.dumps({"verdict":REPORT["verdict"],"passed_verification_gates":REPORT["passed_verification_gates"],"failed_verification_gates":REPORT["failed_verification_gates"],"category_counts":REPORT.get("category_counts"),"independent_exact_samples":REPORT.get("independent_exact_samples"),"independent_nonstationary_mirror_sample":REPORT.get("independent_nonstationary_mirror_sample"),"unexpected_error":REPORT.get("unexpected_error")},indent=2))
sys.exit(0 if REPORT["verdict"]=="PASS" else 1)
