from collections import defaultdict


def count_paths(Start):
	Time = 48
	Width = 8
	Endpoint = 4
	Counts = {(Start, Start == 0, Start == Width): 1}

	for _ in range(Time):
		NextCounts = defaultdict(int)
		for (Position, VisitedZero, VisitedWidth), Count in Counts.items():
			for NextPosition in (Position - 1, Position + 1):
				if(0 <= NextPosition <= Width):
					Key = (
						NextPosition,
						VisitedZero or NextPosition == 0,
						VisitedWidth or NextPosition == Width,
					)
					NextCounts[Key] += Count
		Counts = NextCounts

	return Counts.get((Endpoint, True, True), 0)


Expected = [
	1000894788882,
	1029170933020,
	1017584921004,
	1029170933020,
	1000894788882,
]
Observed = [count_paths(Start) for Start in range(0, 9, 2)]
assert Observed == Expected
Signs = ["+" if Right > Left else "-" if Right < Left else "0" for Left, Right in zip(Observed, Observed[1:])]
assert Signs == ["+", "-", "+", "-"]
print("PASS exact one-turn counterexample")
print(Observed)
print(Signs)
