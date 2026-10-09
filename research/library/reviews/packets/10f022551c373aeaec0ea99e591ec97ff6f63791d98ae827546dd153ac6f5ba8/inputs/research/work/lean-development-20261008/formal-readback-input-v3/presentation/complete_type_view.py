"""Lossless parenthesis sharing for reviewing a complete actual Lean type.

No tokens, whitespace, proof terms, binders or instances are removed. Integer
parts refer only to previously defined nodes; expand them to recover the exact
original actual_type string and check its SHA256. This is a presentation view,
not a Lean checker, contract generator or substitute for the compiler extract.
"""

import argparse
import hashlib
import json
from pathlib import Path


def read_type(PathValue):
	Raw = b""
	with Path(PathValue).open("rb") as Handle:
		while(True):
			Chunk = Handle.read(1024 * 1024)
			if(not Chunk):
				raise ValueError("complete actual_type field unavailable")
			Raw += Chunk
			try:
				Text = Raw.decode("utf-8")
				Marker = '"actual_type":'
				if(Marker in Text):
					Value, _ = json.JSONDecoder().raw_decode(Text[Text.index(Marker) + len(Marker):].lstrip())
					if(not isinstance(Value, str)):
						raise ValueError("actual_type is not text")
					return Value
			except (UnicodeDecodeError, json.JSONDecodeError):
				continue


def make_view(Text):
	Nodes = []
	Known = {}
	Stack = [{"parts": [], "start": 0}]
	InString = False
	InQuotedName = False
	Escaped = False
	Occurrences = 0
	for Index, Character in enumerate(Text):
		if(InString):
			if(Escaped):
				Escaped = False
			elif(Character == "\\"):
				Escaped = True
			elif(Character == '"'):
				InString = False
			continue
		if(InQuotedName):
			if(Character == "»"):
				InQuotedName = False
			continue
		if(Character == '"'):
			InString = True
		elif(Character == "«"):
			InQuotedName = True
		elif(Character == "("):
			Frame = Stack[-1]
			if(Frame["start"] < Index):
				Frame["parts"].append(Text[Frame["start"]:Index])
			Stack.append({"parts": [], "start": Index + 1})
		elif(Character == ")"):
			if(len(Stack) == 1):
				raise ValueError("unbalanced parenthesis")
			Frame = Stack.pop()
			if(Frame["start"] < Index):
				Frame["parts"].append(Text[Frame["start"]:Index])
			Key = tuple(Frame["parts"])
			if(Key not in Known):
				Known[Key] = len(Nodes)
				Nodes.append(Frame["parts"])
			Stack[-1]["parts"].append(Known[Key])
			Stack[-1]["start"] = Index + 1
			Occurrences += 1
	if(len(Stack) != 1 or InString or InQuotedName):
		raise ValueError("unclosed grouping or literal")
	Frame = Stack[0]
	if(Frame["start"] < len(Text)):
		Frame["parts"].append(Text[Frame["start"]:])
	return {"format": "complete-actual-type-lossless-parenthesis-view/v1", "actual_type_sha256": hashlib.sha256(Text.encode("utf-8")).hexdigest(), "actual_type_chars": len(Text), "root_parts": Frame["parts"], "nodes": Nodes, "parenthesis_occurrences": Occurrences, "unique_parenthesis_nodes": len(Nodes), "scope": __doc__}


def expand_view(View):
	Rendered = []
	for Node in View["nodes"]:
		if(any(type(Part) not in (str, int) for Part in Node)):
			raise ValueError("node part is neither literal text nor integer reference")
		if(any(type(Part) is int and (Part < 0 or Part >= len(Rendered)) for Part in Node)):
			raise ValueError("forward, missing or cyclic node reference")
		Rendered.append("(" + "".join(Rendered[Part] if type(Part) is int else Part for Part in Node) + ")")
	if(any(type(Part) not in (str, int) or (type(Part) is int and (Part < 0 or Part >= len(Rendered))) for Part in View["root_parts"])):
		raise ValueError("invalid root part")
	return "".join(Rendered[Part] if type(Part) is int else Part for Part in View["root_parts"])


def main():
	Parser = argparse.ArgumentParser()
	Parser.add_argument("--source", required=True)
	Parser.add_argument("--output", required=True)
	Args = Parser.parse_args()
	Text = read_type(Args.source)
	View = make_view(Text)
	Expanded = expand_view(View)
	if(Expanded != Text):
		raise ValueError("lossless presentation reconstruction failed")
	View["source"] = str(Path(Args.source).resolve())
	Output = Path(Args.output)
	Output.parent.mkdir(parents=True, exist_ok=True)
	Raw = (json.dumps(View, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
	if(Output.exists() and Output.read_bytes() != Raw):
		raise ValueError("already frozen presentation view differs")
	Output.write_bytes(Raw)
	print(json.dumps({"source": Args.source, "output": str(Output), "type_chars": len(Text), "view_bytes": len(Raw), "unique_nodes": len(View["nodes"]), "parenthesis_occurrences": View["parenthesis_occurrences"], "exact_reconstruction": Expanded == Text, "ellipsis_count": Text.count("⋯"), "scope": "Lossless inspection view only, no proof or semantic acceptance inferred."}, ensure_ascii=False))


if(__name__ == "__main__"):
	main()
