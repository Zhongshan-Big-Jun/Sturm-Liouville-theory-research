from run import *

MAIN = BASE / 'objects/final-source-01/AuditRound10.olean'
if not MAIN.is_file():
	raise RuntimeError('final main object missing')
PLANS = [
	('positive-refutations-01', 'Counterexamples.lean', 0, []),
	('negative-flip-01', 'NegativeFlip.lean', 1, []),
	('negative-reflection-01', 'NegativeReflection.lean', 1, []),
	('negative-index-01', 'NegativeIndex.lean', 1, []),
	('print-main-01', 'PrintAuditRound10.lean', 0, []),
	('print-controls-01', 'PrintCounterexamples.lean', 0, ['positive-refutations-01']),
	('explicit-export-01', 'ReadbackExport.lean', 0, []),
]
OBSERVED = []
for Label, File, Expected, Dependencies in PLANS:
	Source = PROJECT / File
	Object = BASE / 'objects' / Label / Source.with_suffix('.olean').name
	Object.parent.mkdir(parents=True, exist_ok=False)
	Extra = [MAIN.parent] + [BASE / 'objects' / D for D in Dependencies]
	Inputs = [Path(__file__), Source, PROJECT / 'AuditRound10.lean', PROJECT / 'lean-toolchain', MAIN]
	for D in Dependencies:
		Inputs += sorted((BASE / 'objects' / D).glob('*.olean'))
	Record = run(Label, [LEAN, '-R', win(PROJECT), '-o', win(Object), win(Source)], Inputs=Inputs, Extra=Extra)
	OBSERVED.append({'label':Label, 'expected_exit':Expected, 'actual_exit':Record['exit_code'], 'inputs_unchanged':Record['inputs_unchanged']})
	write_json(BASE / 'control-execution.json', OBSERVED)
	if Record['exit_code'] != Expected:
		raise RuntimeError('unexpected compiler exit for ' + Label)
print('All recorded command exits matched their expected success/failure classes.')
