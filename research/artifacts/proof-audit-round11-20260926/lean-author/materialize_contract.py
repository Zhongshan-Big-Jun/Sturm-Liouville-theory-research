from pathlib import Path
import re,json
Base=Path(__file__).resolve().parent
P=Base/'project/AuditRound11.lean'
S=P.read_text()
assert 'theorem root' not in S
Clauses=[]
for Match in re.finditer(r'^theorem (\w+)(.*?) := by',S,re.M|re.S):
	Name,Header=Match.groups()
	Depth=0
	for I,C in enumerate(Header):
		if C in '([{': Depth+=1
		elif C in ')]}': Depth-=1
		elif C==':' and Depth==0:
			Params,Conclusion=Header[:I].strip(),Header[I+1:].strip()
			break
	else: raise ValueError(Name)
	Type=('∀ '+Params+',\n  '+Conclusion) if Params else Conclusion
	Clauses.append({'declaration':'AuditRound11.'+Name,'type':Type})
RootType=' ∧\n'.join('('+C['type']+')' for C in Clauses)
Proof='⟨'+',\n    '.join('@'+C['declaration'].split('.')[1] for C in Clauses)+'⟩'
S=S.replace('end AuditRound11','theorem root :\n'+RootType+' := by\n  exact '+Proof+'\n\nend AuditRound11')
P.write_text(S)
(Base/'root-clauses.json').write_text(json.dumps(Clauses,ensure_ascii=False,indent=2)+'\n')
Names=[M[1] for M in re.finditer(r'^(?:noncomputable )?(?:def|abbrev|theorem) (\w+)',S,re.M)]
Expected=re.sub(r'\b('+'|'.join(sorted(Names,key=len,reverse=True))+r')\b',lambda M:'AuditRound11.'+M[0],RootType)
Expected='open scoped Matrix in ('+Expected+')'
Contract={'file':'AuditRound11.lean','declaration':'AuditRound11.root','expected_type':Expected,'universes':[]}
(Base/'contract.json').write_text(json.dumps(Contract,ensure_ascii=False,indent=2)+'\n')
(Base/'root-exact-type.lean.txt').write_text(Expected+'\n')
(Base/'project/CheckContract.lean').write_text('import AuditRound11\nexample : '+Expected+' := AuditRound11.root\n')
with (Base/'AGENTS.md').open('a') as F:F.write('\nmain-02 passed all 13 interfaces. Materialized a literal 13-clause conjunction as theorem root (14 named theorems total). Machine expected type contains the full quantifiers and no reference to root; generated from declared headers, so equality to this contract is not an independent semantic review. The human contract records coordinate and analytic limitations explicitly.\n')
print('root clauses',len(Clauses))
