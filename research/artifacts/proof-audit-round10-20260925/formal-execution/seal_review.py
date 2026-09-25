from pathlib import Path
import json,hashlib,datetime,re,gzip
BASE=Path(__file__).resolve().parent
packet=Path(json.loads((BASE/'config.json').read_text())['packet']);p=json.loads(packet.read_text())
def digest(f):
 with Path(f).open('rb') as h:return hashlib.file_digest(h,'sha256').hexdigest()
def write(f,v):f.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
checks=json.loads((BASE/'evidence/final-identity-check.json').read_text())
root=json.loads((BASE/'evidence/root-comparison.json').read_text())
export=json.loads((BASE/'evidence/export-comparison.json').read_text())
env=json.loads((BASE/'evidence/environment-artifact-check.json').read_text())
all_decls=json.loads((BASE/'evidence/all-declaration-audit.json').read_text())
assert checks['all_snapshots_still_match'] and checks['all_frozen_project_copies_unchanged']
assert export['identical'] and export['entries_actual']==38
assert root['comparison']['status']=='matched' and root['root_type_expression_matches_author'] and root['dependencies_match_author']
assert not root['unsafe_dependencies'] and not root['missing_dependencies']
assert env['matches'] and not env['changed_on_final_stat']
assert len(all_decls)==38 and all(not d['unsafe'] and set(d['axioms'])<={'propext','Classical.choice','Quot.sound'} for d in all_decls)
commands=[]
expected_failures={'negative-flip','negative-reflection','negative-index','reviewer-boundaries-and-all-axioms'}
for f in sorted((BASE/'commands').glob('*/command.json')):
 c=json.loads(f.read_text());label=f.parent.name
 assert c['exit_code']==(1 if label in expected_failures else 0),(label,c.get('exit_code'))
 assert c['inputs_unchanged'] and not c.get('timeout',False)
 for stream in ['stdout','stderr']:assert digest(f.parent/(stream+'.log'))==c[stream+'_sha256']
 commands.append({'label':label,'exit_code':c['exit_code'],'command_record':str(f.relative_to(BASE)),'command_sha256':digest(f),'seconds':c['seconds'],'stdout_sha256':c['stdout_sha256'],'stderr_sha256':c['stderr_sha256']})
assert any(c['label']=='reviewer-boundaries-and-all-axioms-02' and c['exit_code']==0 for c in commands)
# Preserve the exact failed reviewer-side preparation snippet; it was not a frozen-source failure.
failed_prep='''from pathlib import Path
import json
b=Path('/mnt/f/tools/math-audit-round10-20260925/formal-reviewer/independent-35c0ed5b7a9f')
p=b/'project'/'ReviewerChecks.lean'
s=p.read_text()
w='F:'+str(b/'evidence'/'all-declaration-audit.json')[len('/mnt/f'):].replace('/','\\\\')
assert '#audit_all "' not in s
p.write_text(s+'\\n#audit_all '+json.dumps(w)+'\\n')
'''
(BASE/'evidence/failed-preparation-source.py.txt').write_text(failed_prep)
reasons=[
 {'id':'R10-formal-reflection-fidelity','verdict':'APPROVED','reason':'The actual carrier is Fin(2*n) -> R for every natural n, including zero. J is constructed as a real linear coordinate reversal; P_preserve=(I-J)/2 and P_break=(I+J)/2 are constructed linear maps. The declarations prove their eigen-sign identities, decomposition, both idempotences and annihilations, fixed-point characterizations, reversal-invariance of the finite dot product, and orthogonality for independently quantified inputs. Reflection is the affine map 1-Jx, so its perturbation has the minus sign. Only the two fixed-point perturbation statements assume reflect x=x. All real step sizes are allowed. Source, 21 root conjuncts, full declaration export and supplied blind translation agree. Fresh supplementary proofs exercise n=0 and the nonzero symmetric and antisymmetric vectors in dimension two. These claims establish no interface feasibility, clipping behavior, normalization, Hessian result or optimizer confinement.'},
 {'id':'R10-formal-index-interface-fidelity','verdict':'APPROVED','reason':'phase_root Phi k x is exactly 0<=x and Phi(x)=(k:R)*pi, with Phi:R->R and k:N including zero. Uniqueness and order equivalence retain strict monotonicity on [0,infinity); continuity is required only for bracket existence and the resulting sequence-existence theorem. The bracket theorem retains 0<=a<=b and Phi(a)<=k*pi<=Phi(b), and asserts exactly one root in the closed interval. Endpoints and a=b are valid; fresh proofs include degenerate brackets at levels zero and one. Enumeration quantifies over arbitrary strictly increasing index:N->N and left,right:N->R, assumes a valid bracket for every natural m, and then existentially supplies one increasing real sequence. Its classical choice is not executable enumeration. Increasing indices need not be consecutive; the fresh 2*m example illustrates omitted odd levels. Neither automatic brackets, unrestricted level coverage, negative-input monotonicity, a Sturm operator nor spectral identification is asserted.'},
 {'id':'R10-independent-formal-execution','verdict':'APPROVED','reason':'Personally replayed in '+str(BASE)+'. All 55 packet snapshot hashes and all unchanged frozen project copies were verified. Lean 4.31.0, Lake and the shared runtime binary match the recorded hashes; all 12,480 external import artifacts match the supplied manifest. The actual module, positive counterexamples, both declaration/axiom print files, literal root type, literal negations of all three negative propositions, and full exporter compiled with exit 0. Each supplied negative file exited 1 at its intended false mathematical goal. Fresh AuditRound10 and probe objects match the recorded object hashes, and import inspection resolves local modules only to this new private directory. The regenerated 38-entry export is byte-identical. The root type expression and all 16,235 dependency records match the supplied evidence; its 2,219 semantic dependencies match as well. The root and all 38 declarations have only propext, Classical.choice and Quot.sound, with no unsafe, missing or custom-axiom dependencies. Author machine evidence, supplied blind translation and this fresh semantic/execution decision were assessed separately. Evidence manifest: '+str(BASE/'evidence-manifest.json')+'.'}
]
limitations=[
 'Approval is restricted to the three requested current claims and their local formal interfaces; it does not assert complete formalization of the research project.',
 'Execution was a direct declaration replay using the pinned installed Lean/Mathlib objects. No full Lake build, library rebuild, independent kernel implementation or provenance audit of the installed compiler binaries was performed.',
 'The Python solver, floating-point root-loss experiment, Sturm/Pruefer ODE, eigenvalue-phase identification, interval certification, solver termination, physical feasibility and global extrema are outside this formal contract and were not checked.',
 'The supplied blind-readback receipt is coordinator-attested provenance. Its supplied source/export bindings and translation were checked; the original external reviewer identity and unsupplied historical runs were not independently authenticated or retrieved.',
 'Two reviewer-only harness attempts failed during supplementary preparation/compilation; the errors were corrected and the final supplementary compile exited 0. Their records and failed source are retained. They are not defects in the frozen claims.',
 'All new scripts, actual exits, logs, hashes, imported-object records and supplemental proofs are saved at '+str(BASE)+'. The manifest is '+str(BASE/'evidence-manifest.json')+'. No packet input or source-project file was modified.'
]
readback='For every n:N, V_n=Fin(2*n)->R, J_n(v)(i)=v(i.rev), P_n=(I-J_n)/2, Q_n=(I+J_n)/2, and R_n(x)(i)=1-x(i.rev). The linear and projection assertions quantify over all vectors of the indicated dimension, and their scalars are arbitrary reals. They give J_n^2=I, complementary idempotent projections with mutually annihilating ranges, J_n P_n=-P_n, J_n Q_n=Q_n, the two fixed-point equivalences, reversal-invariant finite dot product and dot(P_n u,Q_n v)=0 for every u,v. For every x,v and t:R, R_n(R_n x)=x and R_n(x+t*v)=R_n x-t*J_n v. For every x,u,v,t with R_n x=x, R_n(x+t*(P_n u+Q_n v))=x+t*(P_n u-Q_n v); for every x,v with R_n x=x, R_n(x+v)=x+v iff J_n v=-v. For every Phi:R->R, k:N and x:R, H(Phi,k,x) means 0<=x and Phi(x)=k*pi. If Phi is strictly increasing on [0,infinity), all x,y satisfying H at the same k are equal, and for all j,k:N and roots x,y at those levels, x<y iff j<k. If Phi is also continuous there, then for every k:N and a,b:R with 0<=a<=b and Phi(a)<=k*pi<=Phi(b), there exists exactly one real x in [a,b] satisfying H(Phi,k,x). Given strict half-line monotonicity, every index:N->N and roots:N->R with StrictMono(index) and H(Phi,index(m),roots(m)) for every m:N yield StrictMono(roots). Given both half-line hypotheses, every strictly increasing index and every left,right:N->R with 0<=left(m)<=right(m) and Phi(left(m))<=index(m)*pi<=Phi(right(m)) for all m admit a sequence roots:N->R lying in those brackets, satisfying those levels and strictly increasing. The root theorem is the closed conjunction of the 21 complete independently quantified component statements. The generated helper declarations witness pointwise linearity, scalar commutation, the numeral 2, definition equations and well-defined reversed Fin coordinates; they add no hypotheses to those statements.'
review={'packet_sha256':digest(packet),'verdict':'APPROVED','checked_paths':list(p['inputs']),'claim_results':reasons,'findings':[],'limitations':limitations,'readback':readback}
write(BASE/'review.json',review)
write(BASE/'evidence/command-summary.json',commands)
files={str(f.relative_to(BASE)):{'sha256':digest(f),'bytes':f.stat().st_size} for f in sorted(BASE.rglob('*')) if f.is_file() and f.name not in ['evidence-manifest.json','evidence-manifest.sha256']}
manifest={'schema':'independent-formal-review-evidence/v1','role':'independent-reviewer','packet_sha256':digest(packet),'base':str(BASE),'utc_sealed':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'frozen mathematics comparison and independent direct Lean execution','verdict':'APPROVED','review':'review.json','command_count':len(commands),'source_project_modified':False,'files':files}
write(BASE/'evidence-manifest.json',manifest)
(BASE/'evidence-manifest.sha256').write_text(digest(BASE/'evidence-manifest.json')+'  evidence-manifest.json\n')
print(json.dumps({'verdict':review['verdict'],'command_count':len(commands),'files_sealed':len(files),'snapshot_count':len(review['checked_paths']),'evidence_manifest':str(BASE/'evidence-manifest.json'),'manifest_sha256':digest(BASE/'evidence-manifest.json'),'review_sha256':digest(BASE/'review.json')},indent=2))
