"""Round13 mathematical transport/acceptance properties, normal and -O.
Run after regenerating misc/e1_cert_ledger.json. Negative subprocesses execute
actual build_ledger/main with one deliberately false, exceptional or unknown
fact. They never edit the working certificate or relax its contracts.
"""
from pathlib import Path
from fractions import Fraction as F
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

Root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Root / 'misc'))
import e1_certificate_io as IO
import e1_certgen as Gen
import e1_cert_tables as Tables
from rigid1d import I, D2

class CertificateProperties(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.Ledger = IO.load_accepted_ledger(Root / 'misc/e1_cert_ledger.json')

	def test_signed_directed_endpoints(self):
		for Value in [F(1,3),F(-1,3),F(0),F(17,20),F(-7),F(10**40+1,10**40),F(-10**40-1,10**40)]:
			for Digits in [0,6,12,70]:
				lo,hi = map(F,IO.display_interval((Value,Value),Digits))
				self.assertLessEqual(lo,Value)
				self.assertLessEqual(Value,hi)
				self.assertLess(hi-lo,F(2,10**Digits))
		self.assertNotEqual(*IO.display_interval((F(1,3),F(1,3))))

	def test_comparison_strength_and_equality(self):
		for Target in [F(27,10),F(19,10)]:
			Passed, Pieces=Gen.taylor_value(lambda g:D2(I(1),I(0),I(0)),F(1,2),F(3,4),True,1,target=Target,comparison='ge')
			self.assertFalse(Passed)
			self.assertLess(F(Pieces[0]['margin_exact']),0)
		for Cmp in ['lt','gt']:
			self.assertFalse(IO.predicate((F(13,10),F(13,10)),Cmp,F(13,10))[0])
		for Cmp in ['le','ge']:
			self.assertTrue(IO.predicate((F(13,10),F(13,10)),Cmp,F(13,10))[0])

	def test_complete_contracts(self):
		self.assertEqual(IO.validate_ledger(self.Ledger)['facts'],57)
		ByName={Row['name']:Row for Row in self.Ledger['facts']}
		for Name,Target in [('TA_B2 >= 27/10 on [0.723,0.724]',F(27,10)),('TC >= 19/10 on [0.82,0.83]',F(19,10))]:
			Row=ByName[Name]
			self.assertEqual(Row['statement']['comparison'],'ge')
			self.assertEqual(F(Row['statement']['target']),Target)
			for Piece in Row['detail']['pieces']:
				self.assertGreaterEqual(F(Piece['bound_exact'][0]),Target)
		self.assertEqual(ByName['tau(1.0472) < 13/10']['detail']['cmp'],'lt')

	def test_exact_transport_no_false_singletons(self):
		for Row in self.Ledger['facts']:
			Detail=Row['detail']
			if Row['kind']=='point':
				Bounds=IO.read_interval(Detail['val_exact'])
				IO.check_display(Bounds,Detail['val'])
				if Bounds[0]<Bounds[1]: self.assertNotEqual(*Detail['val'])
			for Piece in Detail.get('pieces',[]):
				self.assertGreaterEqual(F(Piece['M']),F(Piece['M_exact']))
				self.assertGreaterEqual(F(Piece['corr']),F(Piece['corr_exact']))
				self.assertLessEqual(F(Piece['margin']),F(Piece['margin_exact']))
				IO.check_display(IO.read_interval(Piece['bound_exact']),Piece['bound'])

	def test_tampered_or_missing_obligations_rejected(self):
		Mutations=[lambda d:d['facts'].pop(),lambda d:d['facts'][0].update(ok=False),lambda d:d['facts'][0].update(ok=None),lambda d:d.update(status='UNKNOWN'),lambda d:d['summary'].update(failed=1),lambda d:d['meta']['source_sha256'].update({'rigid1d.py':'0'*64}),lambda d:d['facts'][1]['detail'].update(target='0'),lambda d:d['facts'][1]['detail'].update(val=['0','0']),lambda d:d['facts'][3]['detail']['pieces'][0].update(corr_exact='0'),lambda d:d['proofs']['h-concavity']['cells'][0].update(second_derivative_exact=['0','1'])]
		for Mutate in Mutations:
			Changed=copy.deepcopy(self.Ledger);Mutate(Changed)
			with self.assertRaises((ValueError,KeyError,TypeError)):
				IO.validate_ledger(Changed)

	def test_incomplete_status_or_changed_bytes_rejected(self):
		with tempfile.TemporaryDirectory() as Directory:
			PathValue=Path(Directory)/'ledger.json'
			Raw=(Root/'misc/e1_cert_ledger.json').read_bytes();PathValue.write_bytes(Raw)
			StatusPath=PathValue.with_suffix('.status.json')
			for Status in ['RUNNING','ERROR','NOT_CERTIFIED','UNKNOWN',None]:
				IO.atomic_json(StatusPath,dict(status=Status,ledger_sha256=hashlib.sha256(Raw).hexdigest()))
				with self.assertRaises(ValueError): IO.load_accepted_ledger(PathValue)
			IO.atomic_json(StatusPath,dict(status='PASS',ledger_sha256=hashlib.sha256(Raw).hexdigest()))
			PathValue.write_bytes(Raw+b' ')
			with self.assertRaises(ValueError): IO.load_accepted_ledger(PathValue)

	def test_margin_and_table_outward_display(self):
		for Value in [F(1,3),F(2564567,10**11),F(123456,7),F(1,10**25)]:
			Text=Tables._margin_tex(Value)
			Mantissa,Exponent=Text.split(r'\times10^{')
			Shown=F(Mantissa)*F(10)**int(Exponent[:-1])
			self.assertLessEqual(Shown,Value)
			self.assertGreater(Shown,0)
		for lo,hi in [(F(1,3),F(1,3)+F(1,10**30)),(F(-7,3),F(-2))]:
			Shown=tuple(map(F,Tables._qpair(lo,hi,6)))
			self.assertLessEqual(Shown[0],lo);self.assertGreaterEqual(Shown[1],hi)
		Line=next(Line for Line in Tables.render_tables(self.Ledger).splitlines() if Line.startswith(r'$B_1(0.85)'))
		Match=re.search(r'& \$([0-9.]+)\\dots([0-9.]+)',Line)
		self.assertIsNotNone(Match,'nondegenerate certificate must show both endpoints')
		Bounds=next(Row['detail']['val_exact'] for Row in self.Ledger['facts'] if Row['name']=='B1(0.85) >= 1/200')
		self.assertLessEqual(F(Match.group(1)),F(Bounds[0]))
		self.assertGreaterEqual(F(Match.group(2)),F(Bounds[1]))

	def test_actual_failure_propagates_and_prevents_publication(self):
		Code = r"""
import sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import e1_certgen as G
from rigid1d import I,D2
Mode=sys.argv[2]
Original=G.quantity
OriginalEvaluate=G._evaluate
def quantity(Key,g):
	if Key=='B1':
		if Mode=='exception': raise RuntimeError('deliberate round13 negative control')
		return D2(I(-1),I(0),I(0))
	return Original(Key,g)
G.quantity=quantity
if Mode=='unknown':
	def evaluate(Spec,Ledger):
		if Spec['kind']=='point': return None,{'reason':'deliberately undecidable'}
		return OriginalEvaluate(Spec,Ledger)
	G._evaluate=evaluate
raise SystemExit(G.main(['--output',sys.argv[3]]))
"""
		with tempfile.TemporaryDirectory() as Directory:
			Dir=Path(Directory)
			for Mode,Expected in [('false',1),('exception',2),('unknown',1)]:
				Ledger=Dir/(Mode+'.json');Ledger.write_text('previous certificate bytes')
				Prefix=[sys.executable]+(['-O'] if not __debug__ else [])+['-B']
				Run=subprocess.run(Prefix+['-c',Code,str(Root/'misc'),Mode,str(Ledger)],text=True,capture_output=True,timeout=240)
				self.assertEqual(Run.returncode,Expected,Run.stdout+Run.stderr)
				self.assertEqual(Ledger.read_text(),'previous certificate bytes')
				Status=json.loads(Ledger.with_suffix('.status.json').read_text())
				self.assertNotEqual(Status['status'],'PASS')
				Failure=json.loads(Ledger.with_suffix('.failed.json').read_text())
				self.assertNotEqual(Failure['status'],'PASS')
				for Consumer in ['e1_cert_receive.py','e1_cert_tables.py']:
					Command=Prefix+[str(Root/'misc'/Consumer),'--ledger',str(Ledger)]
					Table=Dir/'table.tex';Table.write_text('previous table bytes')
					if Consumer.endswith('tables.py'):Command+=['--output',str(Table)]
					Result=subprocess.run(Command,text=True,capture_output=True,timeout=30)
					self.assertNotEqual(Result.returncode,0,Result.stdout+Result.stderr)
					self.assertEqual(Table.read_text(),'previous table bytes')
				print('negative control',Mode,'generator_exit',Run.returncode,'both consumers rejected',flush=True)

if __name__=='__main__':
	unittest.main(verbosity=2)
