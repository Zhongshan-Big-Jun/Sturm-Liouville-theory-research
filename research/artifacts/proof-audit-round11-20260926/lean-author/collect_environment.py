from run import *
Info={'scope':'author runtime and read-only dependency identity; loaded module hashes are in exact-root run-manifest.json','lean_executable':str(LEAN),'lean_executable_sha256':digest(LEAN),'lean_version':(BASE/'commands/lean-version-01/stdout.log').read_text().strip(),'lean_toolchain':(PROJECT/'lean-toolchain').read_text().strip(),'lean_path':environment()['LEAN_PATH'],'main_repository':str(ORIGINAL.parent),'dependency_manifest':str(ORIGINAL/'lake-manifest.json'),'dependency_manifest_sha256':digest(ORIGINAL/'lake-manifest.json'),'packages':[],'runtime_files':{},'plugin_files':{}}
for P in [LEAN,LAKE,LEAN.parent/'libleanshared.dll']:
	if P.is_file():Info['runtime_files'][str(P)]={'sha256':digest(P),'bytes':P.stat().st_size}
for P in sorted((PLUGIN/'scripts').glob('*')):
	if P.is_file() and P.suffix in ('.py','.template','.json'):
		Info['plugin_files'][str(P)]=digest(P)
for Pkg in json.loads((ORIGINAL/'lake-manifest.json').read_text())['packages']:
	Repo=ORIGINAL/'.lake/packages'/Pkg['name']
	Command=['git','-C',str(Repo),'rev-parse','HEAD']
	R=subprocess.run(Command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
	Info['packages'].append({'name':Pkg['name'],'path':str(Repo),'declared_rev':Pkg['rev'],'actual_head':R.stdout.strip(),'exit_code':R.returncode,'stderr':R.stderr,'matches_declared':R.returncode==0 and R.stdout.strip()==Pkg['rev'],'build_library':str(Repo/'.lake/build/lib/lean')})
write_json(BASE/'environment-baseline.json',Info)
print('runtime bound; dependency revisions:',sum(P['matches_declared'] for P in Info['packages']),'/',len(Info['packages']))
