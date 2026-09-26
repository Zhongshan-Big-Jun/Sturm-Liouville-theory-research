from pathlib import Path
import json,re
Base=Path(__file__).resolve().parent
Source=Base/'project/AuditRound12.lean'
Text=Source.read_text()
Text=Text.split('\ntheorem audit_root :')[0] if '\ntheorem audit_root :' in Text else Text.removesuffix('end\nend AuditRound12\n')
Names=re.findall(r'^theorem (\w+)',Text,re.M)
Terms=[]
for Name in Names:
 Header=Text.split('theorem '+Name,1)[1].split(' := by',1)[0]
 Binders,Body=Header.split(' :\n',1)
 Terms.append('('+('∀ '+Binders.strip()+',\n' if Binders.strip() else '')+Body.strip()+')')
Type=' ∧\n'.join(Terms)
Source.write_text(Text+'\ntheorem audit_root :\n'+Type+' := by\n  exact ⟨'+', '.join('@'+Name for Name in Names)+'⟩\n\nend\nend AuditRound12\n')
Contract={'file':'AuditRound12.lean','declaration':'AuditRound12.audit_root','expected_type':'open scoped Matrix in open AuditRound12 in (\n'+Type+'\n)','universes':[], 'author_role':'local author, independent review pending', 'principal_theorems':['AuditRound12.'+N for N in Names], 'scope':'arbitrary finite n real matrix mirror sector algebra, not spectral analysis'}
(Base/'contract.json').write_text(json.dumps(Contract,ensure_ascii=False,indent=2)+'\n')
print(len(Names),'component theorems; plus audit_root')
