# -*- coding: utf-8 -*-
import io
p = 'misc/rigid_dec.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = "        S = S + t if (k-1) % 2 == 0 else S - t"
new = "        S = S + t if ((k-1)//2) % 2 == 0 else S - t"
assert old in s
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('atan parity fixed')
