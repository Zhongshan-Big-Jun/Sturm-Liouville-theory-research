#!/usr/bin/env python3
"""Observe locals after unmodified checks.py fails; preserve its failure exit."""
from pathlib import Path
import json, runpy, sys, traceback
from executor import BASE, RUN, pointer, save, stamp
source=BASE/'numerical/checks.py'
mode='optimized' if sys.flags.optimize else 'normal'
output=RUN/('numeric-observation-'+mode+'.json')
if output.exists():
    raise RuntimeError('never replace an earlier observation')
if (BASE/'numerical/inputs/manifest.json').exists():
    raise RuntimeError('packet state changed: undeclared manifest appeared; do not read it')
sys.argv=[str(source),'--output','outputs.optimized.json' if sys.flags.optimize else 'outputs.json']
try:
    runpy.run_path(str(source),run_name='__main__')
except BaseException as error:
    tb=error.__traceback__;observed=None;globs=None
    while tb is not None:
        if Path(tb.tb_frame.f_code.co_filename)==source and tb.tb_frame.f_code.co_name=='main':
            observed=tb.tb_frame.f_locals.get('Results');globs=tb.tb_frame.f_globals
        tb=tb.tb_next
    if observed is None:
        raise
    modules={}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name and Path(name).is_file():
            p=Path(name).resolve()
            modules[str(p)]=pointer(p)
    module_path=RUN/('python-loaded-files-'+mode+'.json')
    save(module_path,{'scope':'Files associated with sys.modules in this observed execution; builtin/frozen native dependencies and already-unloaded modules are not exhaustive here.', 'files':list(modules.values())})
    save(output,{'status':'INCOMPLETE','utc':stamp(),'observation_method':'runpy executes original bytes; after the unchanged exception escapes, read main Results from traceback locals. No supplied functions, gates, inputs, or results were replaced.', 'source':pointer(source),'observer':pointer(__file__), 'python':pointer(Path(sys.executable).resolve()),'optimize':sys.flags.optimize,'__debug__':__debug__,'exception':{'type':type(error).__name__,'message':str(error)},'groups':observed,'counts':{'total':len(observed),'passed':sum(g['status']=='PASS' for g in observed),'failed':sum(g['status']=='FAIL' for g in observed)},'runtime':{'mpmath':globs['mp'].__version__,'sympy':globs['sp'].__version__,'decimal_precision':globs['mp'].mp.dps,'module_files':pointer(module_path)}})
    traceback.print_exc()
    print('INDEPENDENT_OBSERVER retained 25 group records; original execution remains INCOMPLETE',flush=True)
    raise SystemExit(error.code if isinstance(error,SystemExit) else 1)
else:
    raise RuntimeError('unexpected success: missing-manifest failure was not preserved')
