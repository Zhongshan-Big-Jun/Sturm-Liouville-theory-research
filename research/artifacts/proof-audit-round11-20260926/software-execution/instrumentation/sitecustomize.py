import atexit, hashlib, json, os, pathlib, sys
root=pathlib.Path(os.environ['AUDIT_PRIVATE_ROOT']).resolve()
manifest=json.loads((root/'manifest.json').read_text())
expected={str((root/k).resolve()):v['sha256'] for k,v in manifest['sources'].items()}
def audit_origins():
    rows=[]
    for name,module in sorted(list(sys.modules.items())):
        file=getattr(module,'__file__',None)
        stem=pathlib.Path(file).stem if file else ''
        if not (name.startswith('_gapn2') or name in ('_sl_prufer','reflection_seeds') or stem.startswith('_gapn2') or stem in ('_sl_prufer','reflection_seeds')):
            continue
        path=str(pathlib.Path(file).resolve()) if file else None
        digest=hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest() if path and path in expected else None
        rows.append({'module':name,'origin':path,'sha256':digest,'expected_sha256':expected.get(path),'matches_frozen_private_source':path in expected and digest==expected[path]})
    record={'argv':sys.argv,'cwd':os.getcwd(),'modules':rows,'all_match':bool(rows) and all(row['matches_frozen_private_source'] for row in rows)}
    pathlib.Path(os.environ['AUDIT_ORIGINS_OUTPUT']).write_text(json.dumps(record,indent=2)+'\n')
atexit.register(audit_origins)
