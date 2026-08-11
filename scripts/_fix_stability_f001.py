# -*- coding: utf-8 -*-
# 2026-08-11: F-001 修正 - SL_stability_moment_jump.tex 定理 2.1/2.2 假设更正为 A_m - B_m >= c_0.
# 与证明实际使用 (及 Lean 形式化 StabilityGrowth.lean 采用) 的假设一致。
import io, os

p = r'docs\SL_stability_moment_jump.tex'
raw = open(p, 'rb').read()
bom = raw[:3] == b'\xef\xbb\xbf'
data = raw.decode('utf-8-sig' if bom else 'utf-8')
lines = data.splitlines(keepends=True)   # 保留每行原有行尾 (全部 CRLF)
EOL = '\r\n'

def find_line(substr, start=0, stop=None):
    if stop is None:
        stop = len(lines)
    for i in range(start, stop):
        if substr in lines[i]:
            return i
    raise SystemExit('NOT FOUND: ' + substr)

# 1) 定理 2.1 (thm:growth) 假设: A_m >= B_m -> A_m - B_m >= c_0
i1 = find_line('满足 $B_m \\geq 0$, $A_m \\geq B_m$ ($m \\geq 2$).')
assert lines[i1].count('$A_m \\geq B_m$') == 1, lines[i1]
lines[i1] = lines[i1].replace('$A_m \\geq B_m$', '$A_m - B_m \\geq c_0$', 1)
assert '$A_m - B_m \\geq c_0$' in lines[i1]

# 2) 日期
i_date = find_line('\\date{2026-08-05}')
assert lines[i_date].count('\\date{2026-08-05}') == 1
lines[i_date] = lines[i_date].replace('\\date{2026-08-05}', '\\date{2026-08-11 (修订版; 首版 2026-08-05)}', 1)

# 3) 定理 2.2 (thm:stability) 假设 (此时 '$A_m \geq B_m$' 在全文唯一, 位于该行)
i2 = find_line('$A_m \\geq B_m$')
assert lines[i2].count('$A_m \\geq B_m$') == 1 and '$A_m' + chr(39) + ' \\geq B_m' + chr(39) + '$' in lines[i2], lines[i2]
lines[i2] = lines[i2].replace('$A_m \\geq B_m$, $A_m', '$A_m - B_m \\geq c_0$, $A_m', 1)
lines[i2] = lines[i2].replace('$A_m' + chr(39) + ' \\geq B_m' + chr(39) + '$,', '$A_m' + chr(39) + ' - B_m' + chr(39) + ' \\geq c_0$ (从而 $\\varepsilon_k, \\varepsilon_k' + chr(39) + ' \\geq 0$),', 1)
assert '$A_m - B_m \\geq c_0$' in lines[i2] and '$A_m' + chr(39) + ' - B_m' + chr(39) + ' \\geq c_0$' in lines[i2]

# 4) 定理 2.2 中 epsilon 定义处补 >= 0
i3 = find_line('这里 $\\varepsilon_k = (A_k - B_k - c_0)/c_0$, $')
lines[i3] = lines[i3].replace('(A_k - B_k - c_0)/c_0$, $', '(A_k - B_k - c_0)/c_0 \\geq 0$, $', 1)
assert '\\geq 0$, $\\varepsilon_k' + chr(39) in lines[i3]

# 5) 在 thm:growth 后的 remark 之后插入"假设的强度"注
i4 = find_line('正是这一思路的封装.')
i5 = i4 + 1
assert lines[i5].strip() == '\\end{remark}', lines[i5]
remark = [
    '\\begin{remark}[假设的强度]' + EOL,
    '\t定理 \\ref{thm:growth} 的统一假设是 $B_m \\geq 0$ 且 $A_m - B_m \\geq c_0$' + EOL,
    '\t($m \\geq 2$), 它保证 $u_m$ 单调不减与 $\\varepsilon_m \\geq 0$.' + EOL,
    '\t仅假定 $A_m \\geq B_m$ 是不够的: 取 $c_0 = 1$, $A_m = B_m = 1$ 时递推解为' + EOL,
    '\t$0, 1, 1, 0, -1, \\dots$, 单调性与非负性均失败; 即使 $A_m - B_m \\geq 0$' + EOL,
    '\t(但不 $\\geq c_0$, 如 $c_0 = 1$, $A_m = 3/2$, $B_m = 1$) 也失败:' + EOL,
    '\t$u_5 = -11/16 < (1/2)^4 = \\prod_{k=2}^{5}(A_k - B_k)/c_0$.' + EOL,
    '\t故保证比值连乘所需的最小门槛正是 $A_m - B_m \\geq c_0$.' + EOL,
    '\\end{remark}' + EOL,
]
lines[i5 + 1:i5 + 1] = remark

# 6) 审计节加入"假设更正"条目 (在"已解决 (本版)"之前)
i6 = find_line('\\item[已解决 (本版)]')
audit_item = [
    '\t\\item[假设更正 (2026-08-11, F-001)] 定理 \\ref{thm:growth} 与' + EOL,
    '\t\t\\ref{thm:stability} 的陈述原写 $A_m \\geq B_m$, 弱于证明实际使用的' + EOL,
    '\t\t$A_m - B_m \\geq c_0$ (Lean 形式化审计 F-001). 本版已统一更正为' + EOL,
    '\t\t$B_m \\geq 0$ 且 $A_m - B_m \\geq c_0$; 反例表明弱假设下单调性与乘积' + EOL,
    '\t\t下界均失败 (见定理 \\ref{thm:growth} 后的注). 形式化文件' + EOL,
    '\t\t\\texttt{SL/StabilityGrowth.lean} 一直采用正确假设, 无需改动.' + EOL,
]
lines[i6:i6] = audit_item

out = ''.join(lines)
tmp = p + '.tmp'
with io.open(tmp, 'wb') as f:
    f.write((('\ufeff' if bom else '') + out).encode('utf-8'))
os.replace(tmp, p)
print('patched OK; lines now', len(lines))