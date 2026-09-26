from pathlib import Path
import hashlib,json,re,shutil
Base=Path(__file__).resolve().parent
Source=Base/'project/AuditRound12.lean'
Text=Source.read_text()
# This delivered source has no string literals or quoted identifiers; fail if that changes.
if '"' in Text or '«' in Text:
 raise ValueError('comment stripper needs a string-aware upgrade for changed source')
Out=[];I=0;Depth=0;Line=False
while I<len(Text):
 C=Text[I];N=Text[I:I+2]
 if Line:
  Out.append('\n' if C=='\n' else ' ')
  if C=='\n': Line=False
  I+=1
 elif Depth:
  if N=='/-': Depth+=1;Out.append('  ');I+=2
  elif N=='-/': Depth-=1;Out.append('  ');I+=2
  else: Out.append('\n' if C=='\n' else ' ');I+=1
 elif N=='--': Line=True;Out.append('  ');I+=2
 elif N=='/-': Depth=1;Out.append('  ');I+=2
 else: Out.append(C);I+=1
if Depth: raise ValueError('unclosed comment')
Blind=Base/'blind';Blind.mkdir(exist_ok=True)
(Blind/'AuditRound12.lean').write_text(''.join(Out))
shutil.copyfile(Base/'project/lean-toolchain',Blind/'lean-toolchain')
Declarations=json.loads((Base/'declarations.json').read_text())
Lines=[]
for D in Declarations:
 Lines += [D['name'], 'kind: '+D['kind'], 'universes: '+json.dumps(D['universes']),
  'binder_kinds: '+json.dumps(D['binder_kinds']), 'actual_type (explicit/universes):',D['type_readable'],
  'actual_type (pp.all):',D['type_explicit'], 'transitive_axioms: '+json.dumps(D['transitive_axioms']),
  'unsafe: '+str(D['unsafe'])]
 if D['definition_value_explicit'] is not None: Lines += ['definition_value (pp.all):',D['definition_value_explicit']]
 Lines += ['']
(Base/'declarations.txt').write_text('\n'.join(Lines))
for Name in ['declarations.json','declarations.txt']: shutil.copyfile(Base/Name,Blind/Name)
Authored=re.findall(r'^(?:theorem|def|abbrev) (\w+)',Text,re.M)
Exported={D['name'] for D in Declarations}
Missing=['AuditRound12.'+N for N in Authored if 'AuditRound12.'+N not in Exported]
assert not Missing,Missing
assert all(not D['unsafe'] for D in Declarations)
assert not {A for D in Declarations for A in D['transitive_axioms']}-{'propext','Quot.sound','Classical.choice'}
Result={'role':'actual formal artifacts only; no informal contract or author interpretation',
 'authored_declarations':len(Authored),'exported_namespace_declarations':len(Declarations),
 'authored_missing_from_export':Missing,'source_sha256':hashlib.sha256(Source.read_bytes()).hexdigest(),
 'files':{P.name:hashlib.sha256(P.read_bytes()).hexdigest() for P in sorted(Blind.iterdir()) if P.is_file() and P.name!='manifest.json'}}
(Blind/'manifest.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(Result,ensure_ascii=False,indent=2))
