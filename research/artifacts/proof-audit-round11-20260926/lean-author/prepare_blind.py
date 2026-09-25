from run import *
import re
Blind=BASE/'formal-only'
Blind.mkdir(exist_ok=False)
Source=PROJECT/'AuditRound11.lean'
Text=Source.read_text()
assert '/-' not in Text and not re.search(r'^\s*--',Text,re.M)
shutil.copyfile(Source,Blind/'AuditRound11.lean')
shutil.copyfile(PROJECT/'lean-toolchain',Blind/'lean-toolchain')
shutil.copyfile(BASE/'declarations-full.json',Blind/'declarations-full.json')
shutil.copyfile(PROJECT/'PrintDeclarations.lean',Blind/'PrintDeclarations.lean')
shutil.copyfile(BASE/'commands/print-01/stdout.log',Blind/'print-and-axioms.log')
Env=environment()
OriginalManifest=ORIGINAL/'lake-manifest.json'
write_json(Blind/'environment.json',{
	'lean_executable':str(LEAN),'lean_executable_sha256':digest(LEAN),
	'lean_version':(BASE/'commands/lean-version-01/stdout.log').read_text().strip(),
	'lean_path':Env['LEAN_PATH'], 'packages':json.loads(OriginalManifest.read_text())['packages'],
	'original_manifest_path':str(OriginalManifest),'original_manifest_sha256':digest(OriginalManifest),
	'toolchain_sha256':digest(Blind/'lean-toolchain'),
	'complete_imported_artifact_inventory':'provided separately in the root machine run manifest; no dependencies are copied into this packet'})
Object=BASE/'objects/blind-01/AuditRound11.olean'
Object.parent.mkdir(parents=True,exist_ok=False)
R=run('blind-01',[LEAN,'-R',win(Blind),'-o',win(Object),win(Blind/'AuditRound11.lean')],Cwd=Blind,Inputs=[Path(__file__),Blind/'AuditRound11.lean',Blind/'lean-toolchain'])
if R['exit_code']!=0: raise RuntimeError('blind packet compilation failed')
write_json(BASE/'blind-transform.json',{'source':str(Source),'source_sha256':digest(Source),'blind_source':str(Blind/'AuditRound11.lean'),'blind_sha256':digest(Blind/'AuditRound11.lean'),'transformation':'The authored Lean source has no comments; copying it byte-for-byte yields comment-free formal material. No identifiers, types, proof bodies or imports were changed.','compilation':'commands/blind-01/command.json','readback':'pending; not performed by this author'})
write_json(Blind/'packet.json',{'root_declaration':'AuditRound11.root','named_declarations':json.loads((BASE/'declaration-names.json').read_text()),'exported_namespace_declarations':37,'files':{str(P.relative_to(Blind)):{'sha256':digest(P),'bytes':P.stat().st_size} for P in sorted(Blind.iterdir()) if P.is_file()}})
print('Comment-free formal packet compiled; independent readback is pending.')
