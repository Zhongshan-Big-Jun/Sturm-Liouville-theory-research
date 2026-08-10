import mpmath as mp
mp.mp.dps = 40
def alpha(x, m): return mp.atan2(mp.sin(x)/m, mp.cos(x))

# find failing pair for alpha-reflection
m = mp.sqrt(4)
fail = None
for i in range(1,200):
    for j in range(1,200):
        x = mp.pi*i/200; y = mp.pi*j/200
        if x+y > mp.pi and alpha(x,m)+alpha(y,m) <= mp.pi:
            fail = (x,y,alpha(x,m)+alpha(y,m)); break
    if fail: break
print("failing pair:", fail and (mp.nstr(fail[0],8), mp.nstr(fail[1],8), mp.nstr(fail[2],8)))
