# -*- coding: utf-8 -*-
src = open('misc/rigid1d.py', encoding='utf-8').read()
src = src.replace('''    def __truediv__(self, o):
        if not isinstance(o, D2): o = D2(o, I(0), I(0))
        inv = D2(I(1))/o
        return self * inv''',
'''    def __truediv__(self, o):
        if not isinstance(o, D2): o = D2(o, I(0), I(0))
        u, w = self, o
        w2 = w.v*w.v
        return D2(u.v/w.v,
                  (u.d1*w.v - u.v*w.d1)/w2,
                  (u.d2*w.v - u.v*w.d2)/w2 - 2*w.d1*(u.d1*w.v - u.v*w.d1)/(w2*w.v))''')
open('misc/rigid1d.py', 'w', encoding='utf-8').write(src)
print('fixed div')
