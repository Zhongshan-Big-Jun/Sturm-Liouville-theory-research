# -*- coding: utf-8 -*-
src = open('misc/rigid1d.py', encoding='utf-8').read()
src = src.replace('''    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0: return D(I(1), I(0))
        return D(self.v**n, self.d*(n*self.v**(n-1)))''',
'''    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0: return D(I(1), I(0))
        return D(self.v**n, self.d*(n*self.v**(n-1)))
    def sqrt(self):
        r = self.v.sqrt()
        return D(r, self.d/(I(2)*r))''')
open('misc/rigid1d.py', 'w', encoding='utf-8').write(src)
print('patched sqrt')
