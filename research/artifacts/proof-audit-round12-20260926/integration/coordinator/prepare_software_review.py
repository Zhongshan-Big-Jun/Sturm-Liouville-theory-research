from pathlib import Path
import json
import shutil
import sys

Root = Path('/mnt/f/LaTeX/BVE research')
Out = Path('/mnt/f/tools/math-audit-round12-20260926')
Project = Root / 'research/artifacts/proof-audit-round12-20260926/software-review'
sys.path.insert(0, '/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/2.0.1/skills/manage-math-research-program/scripts')
import research_review as Review
Project.mkdir()
Scripts = Project / 'inputs/scripts'
Scripts.mkdir(parents=True)
Names = ['_sl_prufer.py', '_gapn2_half_problem_probe.py', '_gapn2_half_debug2.py', '_gapn2_half_debug3.py', '_gapn2_sector_decomposition.py', '_gapn2_green_inertia_probe.py', '_gapn2_symmetry_recon.py', '_gapn2_jacobian_probe.py', '_gapn2_jacobian_analytic.py', '_gapn2_jacobian_spectral.py', '_gapn2_rawko_closed.py', 'reflection_seeds.py', 'op03_gap_table.json']
for Name in Names:
	shutil.copyfile(Root / 'scripts' / Name, Scripts / Name)
shutil.copyfile(Out / 'check_repair.py', Project / 'inputs/check_repair.py')
(Project / 'AGENTS.md').write_text('# Round12 isolated review\n\nOnly frozen inputs. Write own execution evidence under a fresh private external directory. Do not change input files, the parent repository, plugins or global settings. No history, conversation, memory or prior verdict as a premise. No commit/push.\n')
(Project / 'inputs/execution-scope.md').write_text('''# Round12 software and finite execution contract

Read only this frozen packet, not repository history, memory or prior verdicts. Use standard installed Python scientific libraries. Copy all inputs to a new directory under /mnt/f/tools/math-audit-round12-20260926/software-reviewer; use that directory as cwd and record its identity. Examine source before running. Do not write main repository or frozen inputs. No full historical scans.

Run python -B check_repair.py PRIVATE_ROOT and python -B -O check_repair.py PRIVATE_ROOT. These finite tests are candidates to inspect, not proof by test count. Add your own meaningful adversarial tests: DD/DN constant and layered spectra, first modes versus truncation, integer and half-integer phase levels, nonresolvable geometry or root scale, valid and inconsistent pole identities, table BC/geometry/prefix mismatches, retained near poles, full target coverage and finite Green behavior. Check loaded project modules without filtering unexpected locations before asserting isolation. Distinguish floating error guards from rigorous interval bounds. The default Dirichlet API must remain compatible.

Personally execute both half-problem CLIs: python -B scripts/_gapn2_half_problem_probe.py 4 sup 80 and inf 80. Also run both _gapn2_rawko_closed.py 4 sup/inf 80, and _gapn2_green_inertia_probe.py (its fixed four n2/n3 R4 cases). Inspect numerical output, not just exit codes. In n2, reduced-kernel raw Ko must agree with physical edge FD within ordinary finite tolerance; cross-parity kernels target KpOdd=E Ke E. Full spectral truncations have visible tail errors, so do not mistake these for machine identity checks. Compare sector_data raw Ke/Ko and explicit KpEven/KpOdd with the full spectral Jacobian at matching truncation; verify H/E summands and their raw or conjugated convention. No all-R inertia/sign claim.

The historical debug2/debug3 main routines involve large quadrature and deprecated NumPy APIs outside this task; do not execute them. Inspect only their changed use of shared indexed tables, pole arguments and module compatibility. This limitation must remain in the report. Other historical scans are not revalidated.

Keep your own argv/cwd, times, return codes, stdout/stderr, module origins, source SHA256 before/after, independent test sources/results and all failures. Give your evidence directory in the final JSON. Source code and finite checks cannot certify the infinite-dimensional Green formula or complete ODE/numerical implementation. Review the requested behavior and these explicit limits.
''')
Inputs = [dict(path=File.relative_to(Project).as_posix(), role='candidate-source-or-execution-contract') for File in sorted((Project / 'inputs').rglob('*')) if File.is_file()]
Claims = [dict(id='R12-indexed-DD-DN', verification='software', statement='Independently inspect and execute right D/N indexed phase enumeration, unchanged default D contract, prefix stability and explicit unresolved-input behavior. Mathematical identity is distinct from floating execution and no rigorous numerical certificate is claimed.'), dict(id='R12-bound-pole-sums', verification='software', statement='Independently verify shared immutable numerical spectrum tables bind actual geometry, BC, one-based mode identity via legacy zero-based API, target value, prefix and denominator resolvability. Wrong pole or inconsistent table cannot silently produce an infinite reduced kernel. Check actual main and targeted legacy-call changes.'), dict(id='R12-raw-conjugated-sectors', verification='numerical', statement='Independently execute the stated current CLIs and compare raw K sectors, Kp sectors and projected full spectral Jacobians under exact matching conventions. Explicitly distinguish finite truncation from identity, and inspect raw H/E summands and legacy coefficient metadata. No extension to full historical scans, global signs or interval certification.')]
Spec = dict(kind='mathematics', author_ids=['01a06f46-dd03-7c83-9267-32048412c359'], inputs=Inputs, claims=Claims)
for Name, Data in [('software-review-spec.json', Spec), ('software-review-packet.json', Review.create_packet(Project, Spec)), ('software-review-root.json', dict(project=str(Project)))]:
	(Out / Name).write_text(json.dumps(Data, ensure_ascii=False, indent=2) + '\n')
print('Software packet frozen', len(Inputs), flush=True)
