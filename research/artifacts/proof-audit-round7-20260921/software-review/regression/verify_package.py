"""Verify frozen package hashes without importing or executing project code."""
import hashlib
import json
from pathlib import Path
import sys

Base=Path(__file__).resolve().parents[1]


def main():
	ManifestPath=Base/'manifest.json'
	Manifest=json.loads(ManifestPath.read_text(encoding='utf-8'))
	Problems=[]
	for Rel,Expected in Manifest['package_files'].items():
		P=Base/Rel
		if not P.is_file():
			Problems.append('missing: '+Rel)
			continue
		Actual=hashlib.sha256(P.read_bytes()).hexdigest()
		if Actual!=Expected['sha256'] or P.stat().st_size!=Expected['bytes']:
			Problems.append('changed: '+Rel)
	Expected=(Base/'manifest.sha256').read_text(encoding='ascii').split()[0]
	if hashlib.sha256(ManifestPath.read_bytes()).hexdigest()!=Expected:
		Problems.append('manifest digest mismatch')
	print(json.dumps(dict(files_checked=len(Manifest['package_files']),passed=not Problems,problems=Problems),indent=2))
	return int(bool(Problems))

if __name__=='__main__':
	sys.exit(main())
