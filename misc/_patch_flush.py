# -*- coding: utf-8 -*-
import io
p = 'misc/zz_verify_e1.py'
s = io.open(p, encoding='utf-8', newline='').read()
old = "def add(name, ok): results.append((name, ok)); print('%s: %s' % (name, 'PASS' if ok else 'FAIL'))"
new = "def add(name, ok): results.append((name, ok)); print('%s: %s' % (name, 'PASS' if ok else 'FAIL'), flush=True)"
assert old in s, 'old add not found'
s = s.replace(old, new)
s = s.replace("print('ALL PASS' if allok else 'SOME FAILED')", "print('ALL PASS' if allok else 'SOME FAILED', flush=True)")
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched')
