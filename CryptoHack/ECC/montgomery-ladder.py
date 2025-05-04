from Crypto.Util.number import *
from sage.all import *
B = 1
A = 486662
p = 2 ** 255 - 19
K=GF(p)
E_mont=EllipticCurve(GF(p),[0,A,0,B,0])
print(E_mont)
G_x=9
G=E_mont.lift_x(K(G_x),all=True)[1]
k=0x1337c0decafe
def double_montgomery(P):
    x,y=P.xy()
    alpha=((3*x**2+2*A*x+1)*inverse(2*B*y,p)) % p
    x1=(B*alpha**2-A-2*x)%p
    y1=(alpha*(x-x1)-y)%p
    return E_mont(x1,y1)
def add_montgomery(P,Q):
    assert P[0] != Q[0] or P[1] != Q[1]
    x1,y1=P.xy()
    x2,y2=Q.xy()
    a=((y2-y1)*inverse(x2-x1,p))%p
    x3=(B*a**2-A-x1-x2) % p
    y3=(a*(x1-x3)-y1)%p
    return E_mont(x3,y3)
def bin_montgomery(k,P):
    R0=P
    R1=double_montgomery(P)
    for bit in bin(k)[3:]:
        if bit == '0':
            R0,R1=double_montgomery(R0),add_montgomery(R0,R1)
        else:
            R0,R1=add_montgomery(R0,R1),double_montgomery(R1)
    return R0
Q=bin_montgomery(k,G)
print(Q[0]) 
