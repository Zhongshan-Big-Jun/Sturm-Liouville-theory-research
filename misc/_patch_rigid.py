# -*- coding: utf-8 -*-
import io
p = 'misc/rigid1d.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = ("        if self.hi <= 0:\r\n"
       "            if n % 2 == 0: return I((-self.hi)**n, (-self.lo)**n)\r\n"
       "            return I((-self.hi)**n, (-self.lo)**n) if False else I((-self.hi)**n, (-self.lo)**n)")
new = ("        if self.hi <= 0:\r\n"
       "            if n % 2 == 0: return I((-self.hi)**n, (-self.lo)**n)\r\n"
       "            return I(self.lo**n, self.hi**n)")
assert old in s, 'block not found'
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('pow fixed')
