# F11: Boundary n=1, y=0, y=pi, y=pi/2, and R=1 audit

## STATEMENT
Boundary checks:
n=1: Q_1(x)=alpha x^2 - s, roots x=±sqrt(s/alpha)=±s/(s+1), both in (-1,1); G has exactly 2 zeros in (0,pi). y=0: G=0 because sin y=0, endpoint zero not counted. y=pi: same. y=pi/2: Q_1(0)=-s !=0, so G !=0. R=1 (s=1): alpha=4, P=2x^2-1, Q_n(x)=U_n(2x^2-1)+U_{n-1}(2x^2-1)=U_{2n}(x), hence G=sin((2n+1)y), which has exactly 2n simple zeros in (0,pi) at y=k pi/(2n+1).

## PROOF / JUSTIFICATION
n=1 follows from the general proof and the explicit Q_1. Endpoints are due to sin y. At y=pi/2, x=0 in hyperbolic region, and the general no-root fact applies. For R=1, use the identity U_k(cos 2theta)=sin(2(k+1)theta)/sin(2theta); sum gives sin((2n+1)theta)/sin theta = U_{2n}(cos theta) after cancellation of cos theta (valid by continuity at theta=pi/2). Then G=sin y U_{2n}(cos y)=sin((2n+1)y). The zeros in (0,pi) are k pi/(2n+1), k=1,...,2n, all simple.

## TAGS
STRICT boundary audit; separate audits completed
