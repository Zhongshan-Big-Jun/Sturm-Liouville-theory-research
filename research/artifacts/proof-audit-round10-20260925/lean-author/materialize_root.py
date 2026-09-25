from pathlib import Path
import json, re

BASE = Path(__file__).resolve().parent
PATH = BASE / 'project/AuditRound10.lean'
SOURCE = PATH.read_text()
MARKER = '\n-- BEGIN GENERATED ROOT\n'
if MARKER in SOURCE:
	SOURCE = SOURCE.split(MARKER)[0] + '\nend AuditRound10\n'

def split_header(Header):
	Depth = 0
	for I, Char in enumerate(Header):
		if Char in '({[':
			Depth += 1
		elif Char in ')}]':
			Depth -= 1
		elif Char == ':' and Depth == 0:
			return Header[:I].strip(), Header[I+1:].strip()
	raise ValueError(Header)

Entries = []
for Match in re.finditer(r'^theorem (\w+)\s+', SOURCE, re.M):
	Header = SOURCE[Match.end():].split(':=', 1)[0].strip()
	Binders, Goal = split_header(Header)
	Type = '∀ ' + Binders + ',\n' + Goal if Binders else Goal
	Entries.append({'name': 'AuditRound10.' + Match[1], 'type_in_namespace': Type})
Root = ' ∧\n'.join('(' + E['type_in_namespace'] + ')' for E in Entries)
Proof = '⟨' + ',\n    '.join('@' + E['name'].split('.')[-1] for E in Entries) + '⟩'
SOURCE = SOURCE.rsplit('\nend AuditRound10', 1)[0]
SOURCE += MARKER + '\nset_option linter.unusedVariables false in\ntheorem root :\n' + Root + ' := by\n  exact ' + Proof + '\n\nend AuditRound10\n'
PATH.write_text(SOURCE)
Names = ['Vec', 'J', 'P_preserve', 'P_break', 'reflect', 'phase_root']
Qualified = re.sub(r'\b(' + '|'.join(Names) + r')\b', lambda M: 'AuditRound10.' + M[1], Root)
(BASE / 'root-contract.json').write_text(json.dumps({'file':'AuditRound10.lean', 'declaration':'AuditRound10.root', 'expected_type':Qualified, 'universes':[]}, ensure_ascii=False, indent=2)+'\n')
(BASE / 'root-clauses.json').write_text(json.dumps(Entries, ensure_ascii=False, indent=2)+'\n')
(BASE / 'root-exact-type.lean.txt').write_text(Qualified+'\n')
print('Materialized explicit conjunction with', len(Entries), 'clauses; source and intended contract both require review.')
