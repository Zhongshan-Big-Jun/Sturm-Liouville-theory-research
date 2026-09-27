"""Independent mpmath physical transfer, quadrature, and implicit differentiation.

No project imports. Numerical references only; no interval certificates.
"""
import mpmath as mp

mp.mp.dps = 70


def blocks_from_edges(Edges, Densities):
	Ends = [mp.mpf(0), *map(mp.mpf, Edges), mp.mpf(1)]
	return [(Right-Left, mp.mpf(Density)) for Left, Right, Density in zip(Ends, Ends[1:], Densities)]


def transfer(Mu, Width, Density, State):
	Y, Derivative = State
	if Mu == 0:
		return Y+Width*Derivative, Derivative
	Wave = mp.sqrt(Mu*Density)
	C, S = mp.cos(Wave*Width), mp.sin(Wave*Width)
	return (Y*C+Derivative*S/Wave, Derivative*C-Wave*Y*S)


def states(Mu, Blocks, Initial=(0, 1)):
	States = [tuple(map(mp.mpf, Initial))]
	for Width, Density in Blocks:
		States.append(transfer(Mu, Width, Density, States[-1]))
	return States


def physical(Mu, Blocks, X, Initial=(0, 1)):
	Y = tuple(map(mp.mpf, Initial))
	Start = mp.mpf(0)
	for Width, Density in Blocks:
		if X <= Start+Width:
			return transfer(Mu, X-Start, Density, Y)
		Y = transfer(Mu, Width, Density, Y)
		Start += Width
	return Y


def mass(Mu, Blocks, States=None):
	if States is None:
		States = states(Mu, Blocks)
	return sum(Density*mp.quad(lambda T: transfer(Mu,T,Density,State)[0]**2,[0,Width])
		for (Width,Density),State in zip(Blocks,States))


def roots(Blocks, Count, Boundary='D'):
	Index = 0 if Boundary == 'D' else 1
	Length = sum(Width for Width, _ in Blocks)
	Step = mp.pi/(8*Length*mp.sqrt(max(Density for _,Density in Blocks)))
	Secular = lambda Frequency: states(Frequency**2, Blocks)[-1][Index]
	Left = Step/100
	Previous = Secular(Left)
	Roots = []
	for _ in range(100000):
		Right = Left+Step
		Current = Secular(Right)
		if Current*Previous < 0:
			Frequency = mp.findroot(Secular,(Left,Right),tol=mp.mpf('1e-65'))
			if not Left < Frequency < Right or abs(Secular(Frequency)) > mp.mpf('1e-55'):
				raise RuntimeError('independent root not inside sign bracket')
			Roots.append(Frequency**2)
			if len(Roots) == Count:
				return Roots
		Left, Previous = Right, Current
	raise RuntimeError('independent physical root scan exhausted')


def normalized(Mu, Blocks, Points):
	Scale = mp.sqrt(mass(Mu, Blocks))
	return [[mp.re(Value/Scale) for Value in physical(Mu,Blocks,mp.mpf(X))] for X in Points]


def residual(Lambdas, Edges, Densities):
	Blocks = blocks_from_edges(Edges,Densities)
	Values = []
	for Mu in Lambdas:
		States = states(Mu,Blocks)
		Norm = mass(Mu,Blocks,States)
		Values.append([State[0]**2/Norm for State in States[1:-1]])
	A,B = Lambdas
	return mp.matrix([A*U/B-V for U,V in zip(*Values)])


def implicit_jacobian(Edges, Densities, N):
	Edges = list(map(mp.mpf,Edges))
	Blocks = blocks_from_edges(Edges,Densities)
	Lambdas = roots(Blocks,N+1)[-2:]
	J = mp.matrix(len(Edges),len(Edges))
	for i in range(len(Edges)):
		def moved(T):
			Result = Edges.copy()
			Result[i] = T
			return Result
		LambdaDerivatives = []
		for Mu in Lambdas:
			Spatial = mp.diff(lambda T: states(Mu,blocks_from_edges(moved(T),Densities))[-1][0],Edges[i])
			Spectral = mp.diff(lambda L: states(L,Blocks)[-1][0],Mu)
			LambdaDerivatives.append(-Spatial/Spectral)
		Fixed = mp.diff(lambda T:residual(Lambdas,moved(T),Densities),Edges[i])
		for k,Derivative in enumerate(LambdaDerivatives):
			def vary(L):
				Pair = Lambdas.copy()
				Pair[k] = L
				return residual(Pair,Edges,Densities)
			Fixed += mp.diff(vary,Lambdas[k])*Derivative
		for j in range(len(Edges)):
			J[j,i] = Fixed[j]
	return Lambdas, residual(Lambdas,Edges,Densities), J


def green(Mu, Blocks, X, Y, Boundary='D'):
	# Construct the second global solution by imposing the right boundary on
	# the independently propagated initial basis (different assembly from source).
	LeftEnd = states(Mu,Blocks,(0,1))[-1]
	OtherEnd = states(Mu,Blocks,(1,0))[-1]
	Index = 0 if Boundary=='D' else 1
	Coefficient = OtherEnd[Index]/LeftEnd[Index]
	Low,High = sorted([mp.mpf(X),mp.mpf(Y)])
	Phi = physical(Mu,Blocks,Low)[0]
	Psi = physical(Mu,Blocks,High,(1,0))[0]-Coefficient*physical(Mu,Blocks,High)[0]
	return mp.re(Phi*Psi)
