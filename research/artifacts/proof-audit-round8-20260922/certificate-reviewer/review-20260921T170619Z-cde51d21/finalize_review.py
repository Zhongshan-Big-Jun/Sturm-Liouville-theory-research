from pathlib import Path
from collections import Counter
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
packet=json.loads((ROOT/'packet.json').read_text())
original_packet=Path('/mnt/f/LaTeX/BVE research/research/library/reviews/packets/10a8bec28d19a7d77cfe96c73814e1faf51ebe754d590cebb6709145e980a042/packet.json')
post_inputs={}
for name,v in packet['inputs'].items():
    observed=sha(original_packet.parent/v['snapshot'])
    if observed!=v['sha256']:raise ArithmeticError('Frozen input changed: '+name)
    post_inputs[name]=observed
if sha(original_packet)!=sha(ROOT/'packet.json'):raise ArithmeticError('Packet changed')
run_rows=[]
for p in sorted((ROOT/'fresh_runs').glob('*/receipt.json')):
    row=json.loads(p.read_text())
    if not row['expectation_matched']:raise ArithmeticError('Unexpected execution: '+p.parent.name)
    for name,h in row['files_sha256'].items():
        if sha(p.parent/name)!=h:raise ArithmeticError('Fresh receipt mismatch: '+str(p.parent/name))
    run_rows.append({'run':p.parent.name,'exit_code':row['exit_code'],'receipt_sha256':sha(p),'receipt':str(p.relative_to(ROOT))})
counts=Counter(str(r['exit_code']) for r in run_rows)
if len(run_rows)!=67 or counts!=Counter({'0':11,'1':56}):raise ArithmeticError('Fresh run inventory mismatch')
review={
 'packet_sha256':sha(original_packet),
 'verdict':'APPROVED',
 'checked_paths':list(packet['inputs']),
 'claim_results':[
  {'id':'certificate-soundness','verdict':'APPROVED','reason':'Exact interval operations, division/domain guards, signed grid rounding, Machin branch and alternating bounds, and Taylor remainders are sound. Independently checked derivatives and endpoint limits justify root uniqueness and increasing endpoint propagation; the T3 enclosures and margins follow. The three-range analytic argument covers every t in (pi/2,pi), with upper bounds 8, 4380649/500000 and 4761/800, all below 9. The Cz enclosure and positive scalar denominators give Q=893460803/1082206710<0.8256 under the stated interface hypotheses. Decimal displays are outward and never reused as proof inputs.'},
  {'id':'certificate-execution','verdict':'APPROVED','reason':'Fresh copied executions passed all 22 supplied checks in ordinary and -O modes, and all 19 certificate groups in ordinary, -O, -S and -O -S modes. All 14 negative controls rejected at their intended guards in all four modes (56 preserved failures). Independent edge regressions passed 3950 assertions per tested mode; 22 symbolic identity/endpoint checks also passed. Exact certificate outputs reproduce the frozen results. Raw argv, exit status, stdout/stderr, source hashes and the complete review manifest are saved at '+str(ROOT/'manifest.json')+'.'},
  {'id':'certificate-provenance','verdict':'APPROVED','reason':'Verified all seven packet hashes, six duplicate snapshot identities, all 497 archive-manifest entries, 14 intake copies, and 65 archived author receipts (9 successes, 56 intended failures). The three supplied historical source files reproduce their reported Git blob IDs. Original success logs and the earlier symbolic failure log remain preserved. Fresh local execution reproduces the pinned legacy libm counterexample; its platform dependence is retained. Ordinary startup hooks were observed and absent in the -S inventories; no complete import or machine isolation is inferred.'}
 ],
 'findings':[],
 'limitations':[
  'Approval covers the requested certificate scope only, not complete formalization, T1, full sliver coverage, the INF-limit theorem, or upstream spectral-deficit and global phase-branch claims.',
  'The supplied numerical asymptotic and finite-index regression checks do not establish universal or limiting claims; ancillary analytic-repair claims outside the certificate scope were not certified.',
  'The original failed symbolic-check source revision and original exit-code receipt were unavailable; only the preserved failure log could be checked.',
  'Git commit membership and historical claims requiring the three original source files absent from the archive were not checked against external or working-tree data.',
  'Executions used the installed Python 3.14.4 runtime. Post-execution module inventories and -S runs do not provide complete process or full-machine isolation; no Lean execution was performed.'
 ]
}
(ROOT/'final_review.json').write_text(json.dumps(review,indent=2)+'\n')
(ROOT/'completion.json').write_text(json.dumps({'packet_sha256':review['packet_sha256'],'frozen_inputs_unchanged':post_inputs,'fresh_processes':len(run_rows),'fresh_exit_code_counts':dict(counts),'fresh_receipts':run_rows,'scope_notes':'review_notes.md','final_review':'final_review.json'},indent=2)+'\n')
files={str(p.relative_to(ROOT)):{'sha256':sha(p),'size_bytes':p.stat().st_size} for p in sorted(ROOT.rglob('*')) if p.is_file() and p!=ROOT/'manifest.json'}
manifest={'algorithm':'SHA-256','packet_sha256':review['packet_sha256'],'root':str(ROOT),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'excludes':['manifest.json'],'files':files}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for name,v in files.items():
    if sha(ROOT/name)!=v['sha256'] or (ROOT/name).stat().st_size!=v['size_bytes']:raise ArithmeticError('Final manifest verification failed: '+name)
print(json.dumps({'verdict':review['verdict'],'fresh_runs':len(run_rows),'exit_counts':dict(counts),'manifest_entries':len(files),'manifest_sha256':sha(ROOT/'manifest.json'),'manifest_path':str(ROOT/'manifest.json'),'final_review_sha256':sha(ROOT/'final_review.json'),'frozen_input_hashes_unchanged':True},indent=2))
