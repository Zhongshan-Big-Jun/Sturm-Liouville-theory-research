"""Receive the current complete E1 certificate; errors exit nonzero.

This is exact witness/contract validation, not an independent analytic replay.
The older Decimal replay and its receipts remain historical evidence.
"""
from pathlib import Path
import argparse
import json
import sys

from e1_certificate_io import load_accepted_ledger, validate_ledger


def main(argv=None):
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument('ledger', nargs='?', type=Path, default=Path(__file__).resolve().with_name('e1_cert_ledger.json'))
	Args = Parser.parse_args(argv)
	try:
		Result = validate_ledger(load_accepted_ledger(Args.ledger))
	except (OSError, ValueError, TypeError, KeyError) as Error:
		print(json.dumps(dict(status='REJECTED', error=type(Error).__name__, message=str(Error))), file=sys.stderr)
		return 1
	print(json.dumps(Result))
	return 0


if __name__ == '__main__':
	raise SystemExit(main())
