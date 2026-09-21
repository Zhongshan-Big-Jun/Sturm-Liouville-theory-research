"""Exact bounded byte replacements; never reads/writes the main repository."""
from pathlib import Path
import difflib

Base=Path(__file__).resolve().parents[1]
Edits={
'op03_gap_fh.py':[
('Test dD/du = (1-R)*f(u) for [1,R,1] (SUP) numerically.','Test dD/du = 2*(1-R)*f(u) for [1,R,1] (SUP), with int rho*u_k^2 = 1.'),
('from op03_gap_precise import lams_precise, eigfuns_precise','# The legacy precise backend composes block propagators in the wrong order.\nfrom op03_gap_fixed import lams_precise, eigfuns_precise'),
('(1-R)f={ (1-R)*f:+.4e}','2(1-R)f={ 2*(1-R)*f:+.4e}')],
'gap_n1_grad.py':[
('        # FH prediction\n        gFH = ((R-1)*(f[1]-f[0]), (R-1)*f[1])','        # Widths (a,b) give edges (a,a+b); reverse both jumps for INF.\n        gFH = ((R-1)*(f[1]-f[0]), (R-1)*f[1]) if mode == "SUP" else ((R-1)*(f[0]-f[1]), -(R-1)*f[1])')],
'_tmp_fh_paradox.py':[
('Check: for symmetric [1,R,1]_u family, is f(u)==f(1-u) and dD/du==0?','Check paired interface chain rule for symmetric SUP/INF, weighted norm one.'),
('        fh = (R-1)*(f[0]-f[1])   # dD/du via FH with symmetric variation\n        fh2 = -2*(R-1)*f[0]      # handoff formula','        # Left moves right and right moves left: the two contributions add.\n        fh = -(R-1)*(f[0]+f[1]) if mode=="SUP" else (R-1)*(f[0]+f[1])\n        fh2 = -2*(R-1)*f[0] if mode=="SUP" else 2*(R-1)*f[0]  # symmetry')],
 'tmp_fh_test.py':[
('    fh1 = lam[0]*(R-1)*(u1[0]**2 + u1[1]**2)','    fh1 = -lam[0]*(R-1)*(u1[0]**2 + u1[1]**2)'),
('    fh2 = lam[1]*(R-1)*(u2[0]**2 + u2[1]**2)','    fh2 = -lam[1]*(R-1)*(u2[0]**2 + u2[1]**2)'),
('FH(lam1*(R-1)*sum u1^2)','FH(-lam1*(R-1)*sum u1^2)'),
('FH(lam2*(R-1)*sum u2^2)','FH(-lam2*(R-1)*sum u2^2)'),
('FH(-2(R-1)f) = {-2*(R-1)*','FH(+2(R-1)f) = {2*(R-1)*')],
 'tmp_verify_endpoints.py':[
('        fh = -2*(R-1)*f if mode=="INF" else 2*(R-1)*f','        fh = 2*(R-1)*f if mode=="INF" else -2*(R-1)*f'),
('FH-2(R-1)f={fh:+.4f}','FH_paired={fh:+.4f}')],
 '_gapn2_hess_verify.py':[
('(1) dD/dx_j = s_j * f(x_j) at band-consistent points (FD gradient in edge coords).','(1) dD/dx_j = -s_j * f(x_j) for independent right-moving edges.'),
('(2) Hess(D) vs lambda * diag(s) * J  (both orders: J and J^T) at h=1e-3.','(2) At F=f/lambda_{n+1}=0 only: Hess(D) = -lambda * diag(s) @ J,\n    J=D_xF (or its transposed expression), tested at h=1e-3. Away from F=0,\n    add -diag(s) @ outer(F, grad(lambda_{n+1})). Weighted norms equal one.'),
("        f = lam * ed['u_n'] ** 2 * 0 + (lam * ed['u_n'] ** 2 - lam * ed['u_np1'] ** 2)","        f = ed['lam_n'] * ed['u_n'] ** 2 - lam * ed['u_np1'] ** 2"),
('vs s_j f(x_j) = {np.round(s * f, 6)}','vs -s_j f(x_j) = {np.round(-s * f, 6)}'),
('np.abs(g - s * f)','np.abs(g + s * f)'),
('# (2) FD Hessian (h=1e-3) vs lambda * diag(s) * J and J^T versions','# (2) Stationary (F=0) Hessian (h=1e-3) vs -lambda * diag(s) @ J.'),
('        H1 = lam * np.diag(s) @ J','        H1 = -lam * np.diag(s) @ J'),
('        H2 = lam * J.T @ np.diag(s)','        H2 = -lam * J.T @ np.diag(s)'),
('H - lam diag(s) J','H + lam diag(s) J'),
('H - lam J^T diag(s)','H + lam J^T diag(s)')],
 '_gapn2_hess_sign_and_bigR.py':[
('"""Probe: (1) verify Hess(D_n) = +/- diag(s) * lambda_{n+1} * J at band-consistent','"""Probe: (1) compare +/- lambda_{n+1} * diag(s) @ J at stationary (F=0)'),
('All output is EVIDENCE.','The correct sign is minus for s=rho_right-rho_left, J=D_x(f/lambda_{n+1}),\nwith weighted norms one. The simple Hessian formula requires F=0.\nAll output is EVIDENCE.'),
('            H = sign * np.diag(s) * lam * J','            H = (sign * lam * np.diag(s)) @ J')],
 '_gapn2_jacobian_analytic.py':[
('       critical point (verified 2026-08-12 vs FD Hessian, h=1e-4, err 4.6e-3 on','       critical point F=0 (historically verified 2026-08-12 vs FD Hessian, h=1e-4, err 4.6e-3 on'),
('            # Hessian spectrum: Hess = diag(s) * lambda_{n+1} * J','            # Stationary F=0 only: Hess = -lambda_{n+1} * diag(s) @ J.'),
('            H = -np.diag(s) * lam_np1 * Jfd','            H = (-lam_np1 * np.diag(s)) @ Jfd')],
 '_gapn2_o3_scan.py':[
('                evH = np.linalg.eigvalsh(-np.diag(s) * lam_np1 * J)  # Hessian','                # Stationary F=0 only; K above includes its separate lambda scaling.\n                evH = np.linalg.eigvalsh((-lam_np1 * np.diag(s)) @ J)  # full Hessian')],
 '_gapn2_second_variation_probe.py':[
('    Hess = -np.diag(s) * lam_np1 * Jfd','    # Stationary F=0 only; this repair does not re-audit the density-path probes.\n    Hess = (-lam_np1 * np.diag(s)) @ Jfd')]
}
Patch=[]
for Name,Changes in Edits.items():
    P=Base/'candidates'/'scripts'/Name
    Raw=P.read_bytes()
    Old=Raw
    for Before,After in Changes:
        B=Before.encode(); A=After.encode()
        if Raw.count(B)!=1: raise RuntimeError(f'{Name}: expected unique replacement: {Before!r}, got {Raw.count(B)}')
        Raw=Raw.replace(B,A)
    P.write_bytes(Raw)
    Patch.extend(difflib.unified_diff(Old.decode('utf-8-sig').splitlines(keepends=True),Raw.decode('utf-8-sig').splitlines(keepends=True),fromfile='originals/scripts/'+Name,tofile='candidates/scripts/'+Name))
(Base/'change.patch').write_text(''.join(Patch),encoding='utf-8')
P=Base/'AGENTS.md'
with P.open('a',encoding='utf-8') as F:
    F.write('- 2026-09-21: 后端真实 IVP/加权积分检查返回旧 precise 范数 0.94870/0.93136, fixed 样本误差约 1.3e-12. 仅在已分配 op03_gap_fh 切换到同签名所需接口的 fixed, 不改依赖文件. 十候选完成直接公式/符号/矩阵乘法修订, 原字节和差异已保存.\n')
    F.write('- 2026-09-21: 用户补充非驻点 Hessian 的秩一项与驻点简式边界. 回归分别覆盖两者, 不将简式推广到全域. 首次 harness 的格式化 AST 选择器有歧义, 保留原始失败并修正测试选择器; 修正后原版本 117 项中 79 项真实失败, 无异常.\n')
print('Revised exactly',len(Edits),'target candidates; dependencies unchanged.')
