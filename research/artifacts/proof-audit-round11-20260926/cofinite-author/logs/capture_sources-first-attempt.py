#!/usr/bin/env python3
"""Freeze only actually read author inputs under the authorized output root."""
from pathlib import Path
import datetime
import hashlib
import html
import json
import re
import urllib.request

Root = Path('/mnt/f/tools/math-audit-round11-20260926/cofinite-author')
Intake = json.loads((Root / 'logs/intake.json').read_text())
SourceSpecs = {
	'AGENTS.md': ('CONTROL-PROJECT', 'project-AGENTS.md',
		[(1, 151, 'Project instructions; present task narrows the write scope')]),
	'SKILL.md': ('CONTROL-SKILL', 'rigorous-open-math-research-2.0.1-SKILL.md',
		[(1, 60, 'Author proof development, preservation, and separate independent review')]),
	'cofinite_all_orders_proof.md': ('IN-SUBMITTED', 'submitted-cofinite_all_orders_proof.md',
		[(1, 219, 'All sections; unverified input candidate, not independent acceptance')]),
	'SL_fractional_left_definite.tex': ('P-FRAC', 'SL_fractional_left_definite.tex', [
		(38, 70, 'eq:operator-domain; eq:original-family; definitions and scope'),
		(74, 133, 'prop:operator; h2 estimate; positivity, surjectivity, self-adjointness'),
		(135, 194, 'normalized-modes and spectral-norm; full eigenbasis'),
		(207, 317, 'lem:coefficient-upper; thm:all-thresholds; all named members'),
		(339, 355, 'lem:square-domain; genuine product domain'),
		(356, 444, 'four-trace-matrix; h4-approximation; h4-core mechanism'),
		(461, 500, 'thm:main; h4-embedding; spectral cutoff density')]),
	'01-parity-unitary.md': ('P-PARITY', '01-parity-unitary.md',
		[(1, 13, 'Actual operator and fixed-c conventions'),
		 (32, 84, 'P2-P3: domain invariance, parity gluing and spectral calculus')]),
	'02-fractional-trace-dictionary.md': ('P-DICT', '02-fractional-trace-dictionary.md',
		[(5, 38, 'D1: separated-operator applicability bridge'),
		 (39, 97, 'D2-D3: boundary thresholds, critical weighted residual and equivalent norm'),
		 (98, 112, 'D4: centre trace thresholds and logarithmic Fourier construction'),
		 (113, 117, 'D5: model scope and limitations')]),
	'03-s3-cofinite-closure.md': ('P-S3', '03-s3-cofinite-closure.md',
		[(13, 49, 'C1: actual Hc3 space and centre traces'),
		 (50, 65, 'C2: all-degree complete-tail algebra'),
		 (66, 98, 'C3-C4: local highest-derivative cutoff and finite boundary right inverse'),
		 (99, 118, 'C5: exact s=3 cofinite closure and limits')]),
	'krein-s3-cofinite-three-traces.json': ('CONTEXT-CARD', 'predecessor-s3-card.json',
		[(1, 40, 'Candidate-card shape and predecessor scope; not a mathematical assumption')]),
}
Bindings = []
for Entry in Intake['files']:
	Source = Path(Entry['path'])
	Data = Source.read_bytes()
	Digest = hashlib.sha256(Data).hexdigest()
	if Digest != Entry['sha256']:
		raise RuntimeError('Input drift after actual reading: ' + str(Source))
	SourceId, TargetName, Locators = SourceSpecs[Source.name]
	Target = Root / 'sources' / TargetName
	Target.write_bytes(Data)
	LineCount = len(Data.splitlines())
	Bindings.append({
		'source_id': SourceId, 'original_path': str(Source),
		'project_relative_path': str(Source.relative_to('/mnt/f/LaTeX/BVE research'))
			if Source.is_relative_to('/mnt/f/LaTeX/BVE research') else None,
		'sha256': Digest, 'size_bytes': len(Data), 'line_count': LineCount,
		'frozen_copy': str(Target),
		'role': Entry['role'], 'read_status': 'ACTUALLY_READ_IN_THIS_AUTHOR_SESSION',
		'read_extent': 'Complete file read; proof-use locators listed separately',
		'locators': [{'line_start': Start, 'line_end': min(End, LineCount), 'description': Description}
			for Start, End, Description in Locators],
	})
BindingObject = {
	'status': 'CANDIDATE_PENDING_INDEPENDENT_REVIEW',
	'role': 'ANALYTIC_AUTHOR_NOT_INDEPENDENT_REVIEWER',
	'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
	'project_root': '/mnt/f/LaTeX/BVE research',
	'project_head_at_intake': Intake['project_head_observed'],
	'identity_rule': 'Raw-file SHA-256, not an inherited review label or a Git commit alone.',
	'sources': Bindings,
	'dependency_boundary': {
		'P-FRAC': 'Current object/spectral/domain source; necessary arguments are rederived in manuscript sections 2-3.',
		'P-S3': 'Construction predecessor and s=3 comparison; not an all-orders closure input.',
		'P-DICT': 'Read and compared. Local multiplier bounds and continuous traces are independently derived in section 4; no dependence on the full all-orders dictionary theorem.',
		'P-PARITY': 'Object/parity context only; no transitive external extension theorem is imported.',
		'IN-SUBMITTED': 'Submitted candidate, unverified before this author development.',
		'CONTEXT-CARD': 'Card-format and scope context only.',
		'external_source': 'FGHL v1 Appendix A.3 is an interpolation consistency reference; the needed weighted estimate is proved directly.',
		'unread_references': 'Grubb original article and the original interpolation texts cited by FGHL were not read in this session and are not claimed as verified proof dependencies.',
	},
}
Url = 'https://arxiv.org/html/2408.01514v1'
Fetch = {'requested_url': Url,
	'started_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
	'purpose': 'Targeted source capture of Appendix A Theorem A.3, equations A.15-A.16',
	'prior_tool_result': 'An optional v2 HTML request returned 404; v1 was actually read through web tools.'}
try:
	Request = urllib.request.Request(Url, headers={'User-Agent': 'Math research author source verification'})
	with urllib.request.urlopen(Request, timeout=35) as Response:
		Data = Response.read()
		Fetch.update({'http_status': Response.status, 'final_url': Response.url})
	RawPath = Root / 'sources' / 'fghl-2408.01514v1.html'
	RawPath.write_bytes(Data)
	RawText = Data.decode('utf-8')
	Needle = re.search(r'<div[^>]*id="([^"]+)"[^>]*class="[^"]*ltx_theorem[^"]*"[^>]*>\s*<h6[^>]*>.*?Theorem A\.3', RawText, re.S)
	# Identify the local theorem container directly rather than importing unrelated text.
	HeadingIndex = RawText.find('Theorem A.3')
	if HeadingIndex < 0:
		raise ValueError('Theorem A.3 heading was not found in fetched HTML')
	Start = RawText.rfind('<div', 0, HeadingIndex)
	End = RawText.find('</div>', HeadingIndex)
	# The theorem contains nested divs; include both equations through A.16.
	A16 = RawText.find('(A.16)', HeadingIndex)
	if A16 < 0:
		A16 = RawText.find('A.16', HeadingIndex)
	if A16 < 0:
		raise ValueError('A.16 was not found after theorem heading')
	End = RawText.find('</table>', A16)
	if End < 0:
		End = A16 + 2000
	else:
		End += len('</table>')
	Excerpt = RawText[Start:End]
	ExcerptPath = Root / 'sources' / 'fghl-A3-excerpt.html'
	ExcerptPath.write_text(Excerpt)
	PlainText = html.unescape(re.sub('<[^>]+>', ' ', Excerpt))
	PlainText = re.sub(r'\s+', ' ', PlainText).strip()
	(Root / 'sources' / 'fghl-A3-excerpt.txt').write_text(PlainText + '\n')
	Fetch.update({'capture_status': 'ORIGINAL_HTML_CAPTURED',
		'raw_path': str(RawPath), 'raw_sha256': hashlib.sha256(Data).hexdigest(),
		'excerpt_path': str(ExcerptPath),
		'excerpt_sha256': hashlib.sha256(Excerpt.encode()).hexdigest(),
		'reading_status': 'Only Appendix A.3 and its nearby context used; capture is not whole-paper reading',
		'version': 'arXiv:2408.01514v1',
		'locator': 'Appendix A, Theorem A.3, equations (A.15)-(A.16)'})
	print(PlainText[:6000])
except Exception as Error:
	Fetch.update({'capture_status': 'FETCH_OR_EXTRACTION_FAILED', 'error': repr(Error),
		'reading_status': 'The targeted content was read using web tools; local capture failure is recorded.'})
Fetch['completed_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
(Root / 'logs/source-capture.json').write_text(json.dumps(Fetch, ensure_ascii=False, indent=2) + '\n')
BindingObject['external_primary_source'] = Fetch
(Root / 'source-bindings.json').write_text(json.dumps(BindingObject, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'bindings': len(Bindings), 'external_capture': Fetch['capture_status']}, indent=2))
