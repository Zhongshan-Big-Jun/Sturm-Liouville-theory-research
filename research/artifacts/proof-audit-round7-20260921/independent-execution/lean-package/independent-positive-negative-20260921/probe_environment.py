#!/usr/bin/env python3
"""Inspect all constants owned by the fresh candidate module, without author helpers."""
from pathlib import Path
import json, os, subprocess, time
from executor import BASE, RUN, digest, pointer, save, stamp
config=json.loads((BASE/'lean-package/runtime-config.json').read_text())
contract=json.loads((BASE/'lean-package/positive-contract.json').read_text())
libraries=list((RUN/'replay/positive/lean-verification-runs').glob('*/lib'))
if len(libraries)!=1: raise RuntimeError('expected one fresh positive library')
library=libraries[0]
obj=library/'SL/AuditRound7.olean'
if not obj.is_file(): raise RuntimeError('fresh olean absent')
output=RUN/'all-module-declarations.json'
probe=RUN/'AllModuleDeclarations.lean'
win=lambda p: subprocess.check_output(['wslpath','-w',str(p)],cwd=BASE,text=True).strip()
lean='''import Lean
import SL.AuditRound7
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option pp.universes true
set_option pp.fullNames true
set_option pp.all true
open Lean Elab Command Meta
run_cmd do
  let env := (← getEnv).setExporting false
  let mut rows : Array Json := #[]
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      if env.header.moduleNames[idx.toNat]! == `SL.AuditRound7 then
        let typ ← liftTermElabM do return (← ppExpr info.type).pretty
        let val ← match info.value? (allowOpaque := true) with
          | some v => if info.isTheorem then pure Json.null else do
              let p ← liftTermElabM do return (← ppExpr v).pretty
              pure <| Json.mkObj [("pretty", toJson p), ("expression", toJson (reprStr v))]
          | none => pure Json.null
        let axioms ← collectAxioms name
        rows := rows.push <| Json.mkObj [
          ("declaration", toJson name.toString),
          ("is_theorem", toJson info.isTheorem),
          ("is_unsafe", toJson info.isUnsafe),
          ("is_internal_name", toJson name.isInternal),
          ("universes", toJson (info.levelParams.map Name.toString)),
          ("actual_type", toJson typ),
          ("type_expression", toJson (reprStr info.type)),
          ("definition", val),
          ("transitive_axioms", toJson (axioms.map Name.toString))]
  let resolved ← findOLean `SL.AuditRound7
  let result := Json.mkObj [
    ("module", toJson "SL.AuditRound7"),
    ("resolved_olean", toJson resolved.toString),
    ("owned_constant_count", toJson rows.size),
    ("declarations", Json.arr rows)]
  IO.FS.writeFile OUTPUT (result.pretty ++ "\\n")
example : EXPECTED := SL.AuditRound7.local_algebra_root
'''
lean=lean.replace('OUTPUT',json.dumps(win(output))).replace('EXPECTED',contract['expected_type'])
probe.write_text(lean)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',LEAN_PATH=win(library)+';'+config['LEAN_PATH'],LEAN_SRC_PATH='')
temp=RUN/'tmp';temp.mkdir(exist_ok=True)
env.update(TMPDIR=str(temp),TEMP=win(temp),TMP=win(temp))
env['WSLENV']=':'.join([v for v in env.get('WSLENV','').split(':') if v and v.split('/')[0] not in ('LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP')]+['LEAN_PATH','LEAN_SRC_PATH','TEMP','TMP'])
argv=[config['lean'],win(probe)]
start=time.monotonic()
receipt={'argv':argv,'cwd':str(BASE),'started_at_utc':stamp(),'probe':pointer(probe),'driver':pointer(__file__),'input_olean_before':pointer(obj),'lean':pointer(config['lean']),'environment':{k:env[k] for k in ('LEAN_PATH','LEAN_SRC_PATH','WSLENV','TEMP','TMP','TMPDIR')}}
with (RUN/'all-module-declarations.stdout.log').open('xb') as out,(RUN/'all-module-declarations.stderr.log').open('xb') as err:
    p=subprocess.Popen(argv,cwd=BASE,env=env,stdout=out,stderr=err)
    receipt['pid']=p.pid
    save(RUN/'all-module-declarations.execution.json',receipt)
    code=p.wait()
receipt.update(returncode=code,ended_at_utc=stamp(),seconds=time.monotonic()-start,input_olean_after=pointer(obj),stdout=pointer(RUN/'all-module-declarations.stdout.log'),stderr=pointer(RUN/'all-module-declarations.stderr.log'))
if output.is_file(): receipt['export']=pointer(output)
save(RUN/'all-module-declarations.execution.json',receipt)
print('independent module export exit',code,'seconds',round(receipt['seconds'],2),flush=True)
if code: print((RUN/'all-module-declarations.stdout.log').read_text(),flush=True)
raise SystemExit(code)
