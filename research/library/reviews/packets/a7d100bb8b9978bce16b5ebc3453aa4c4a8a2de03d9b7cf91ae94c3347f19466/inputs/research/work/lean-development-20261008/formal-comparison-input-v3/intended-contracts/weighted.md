# Weighted first increment, source contract written before proof

Source versions: research HEAD f3b78f402497c6a2ecdf8e53770fe84bab308198,
docs/SL_ratio_proof.tex (problem definition), docs/SL_inf_ratio_proof.tex
(constant-density modes), docs/SL_bounded_direction_spectral_tail.md Section 1.

For every real Length>0, Rho>0 and integer mathematical index n>=1, define
k=n*pi/Length, omega=k/sqrt(Rho), lambda=omega^2, A=sqrt(2/(Rho*Length)).
The complex-valued function u(x)=ofReal(A*sin(k*x)) and its actual derivative
v(x)=ofReal(A*k*cos(k*x)) solve u'=v and v'=-lambda*Rho*u on the interval.
Both integral identities from these derivatives must be proved by the FTC,
with actual interval-integrability. u(0)=u(Length)=0 and
integral_0^Length Rho*norm(u)^2=1. The model includes arbitrary measurable
positive bounded densities and DD/DN boundary predicates, but this root is
only the constant-density DD family. It asserts neither completeness nor
an identification of n with the full spectral ordering.

No conclusion or normalization is assumed in the formal root's hypotheses.
The expected contract must retain all Length, Rho, n quantifiers and positivity
hypotheses, and must compare against the above model's actual definitions.

Later extension obligations: general-density existence and regularity,
equivalence to weak Sobolev solutions, full weighted L2 norm and completeness,
all eigenvalues and their ordering, DN explicit family, and spectral tail.
