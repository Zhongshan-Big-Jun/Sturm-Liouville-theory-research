# -*- coding: utf-8 -*-
"""Patch rigid1d: make I ops defer to D when the operand is a D."""
import re
src = open('misc/rigid1d.py', encoding='utf-8').read()
# Add NotImplemented guards in I methods for D operands
src = src.replace('''    def __add__(self, o):
        o = o if isinstance(o, I) else I(o); return I(self.lo+o.lo, self.hi+o.hi)''',
'''    def __add__(self, o):
        if isinstance(o, D): return NotImplemented
        o = o if isinstance(o, I) else I(o); return I(self.lo+o.lo, self.hi+o.hi)''')
src = src.replace('''    def __sub__(self, o):
        o = o if isinstance(o, I) else I(o); return I(self.lo-o.hi, self.hi-o.lo)''',
'''    def __sub__(self, o):
        if isinstance(o, D): return NotImplemented
        o = o if isinstance(o, I) else I(o); return I(self.lo-o.hi, self.hi-o.lo)''')
src = src.replace('''    def __mul__(self, o):
        o = o if isinstance(o, I) else I(o)
        a,b,c,d = self.lo*o.lo, self.lo*o.hi, self.hi*o.lo, self.hi*o.hi''',
'''    def __mul__(self, o):
        if isinstance(o, D): return NotImplemented
        o = o if isinstance(o, I) else I(o)
        a,b,c,d = self.lo*o.lo, self.lo*o.hi, self.hi*o.lo, self.hi*o.hi''')
src = src.replace('''    def __truediv__(self, o):
        o = o if isinstance(o, I) else I(o)
        if o.lo <= 0 <= o.hi: raise ZeroDivisionError('div by interval containing 0')''',
'''    def __truediv__(self, o):
        if isinstance(o, D): return NotImplemented
        o = o if isinstance(o, I) else I(o)
        if o.lo <= 0 <= o.hi: raise ZeroDivisionError('div by interval containing 0')''')
# D ops: handle I operands (o may be I) - D(o, I(0)) works since D init converts via I()
# but D(o) with o an I: D.__init__ does self.v = v if isinstance(v, I) else I(v) -> ok
open('misc/rigid1d.py', 'w', encoding='utf-8').write(src)
print('patched')
