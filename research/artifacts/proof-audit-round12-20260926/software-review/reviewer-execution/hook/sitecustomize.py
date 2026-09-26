import atexit, json, os, sys
from pathlib import Path
@atexit.register
def record_origins():
    dest=os.environ.get('R12_ORIGIN_FILE')
    if dest:
        origins={name:str(Path(mod.__file__).resolve()) for name,mod in list(sys.modules.items()) if getattr(mod,'__file__',None)}
        versions={name:str(getattr(sys.modules.get(name),'__version__','not loaded')) for name in ['numpy','scipy','mpmath']}
        Path(dest).write_text(json.dumps(dict(argv=sys.argv,cwd=os.getcwd(),executable=sys.executable,python=sys.version,modules=origins,versions=versions),indent=2))
