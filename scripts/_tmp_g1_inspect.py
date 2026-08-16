import sys, os
sys.path.insert(0,'scripts')
import numpy as np
import importlib.util
spec=importlib.util.spec_from_file_location('gd','scripts/_gapn2_green_inertia_probe.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
# inspect signatures
print('functions', [x for x in dir(m) if not x.startswith('__')])
print(inspect.signature(m.reduced_resolvent))
