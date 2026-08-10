# -*- coding: utf-8 -*-
import mpmath as mp
pi = mp.pi
a0 = mp.acos(mp.mpf(1)/4)/pi
s15 = mp.sqrt(15)
def phi_num(b):
    fc = 15*pi**3*s15/4
    R1_1 = pi*(1920*s15*pi**2*a0**2 - 1920*s15*pi**2*a0*b + 64*s15*pi*a0*mp.sin(2*pi*b)
               + 448*s15*pi*a0*mp.sin(4*pi*b) + 2700*pi*a0 - 1920*pi*b*mp.cos(2*pi*b)**2
               + 960*pi*b*mp.cos(2*pi*b) + 960*pi*b + 960*mp.sin(2*pi*b) - 480*mp.sin(4*pi*b)
               + 1920*pi*mp.cos(2*pi*b)**2 - 960*pi*mp.cos(2*pi*b) - 2310*pi - 225*s15)/1024
    return -R1_1/fc
