from sage.all import *
from Crypto.Util.number import *
from ast import literal_eval
p = 1789850433742566803999659961102071018708588095996784752439608585988988036381340404632423562593
a = 62150203092456938230366891668382702110196631396589305390157506915312399058961554609342345998
b = 1005820216843804918712728918305396768000492821656453232969553225956348680715987662653812284211
F = GF(p)
E = EllipticCurve(F, [a, b])
G = E.gens()[0]
order = G.order()
factors = factor(order)
with open('output.txt','r') as f:
    data = f.read()
data = data.replace(' : 1)', ')').replace(' :', ',')
data_raw = literal_eval(data)
data = [(a, b, E(*R_data)) for a, b, R_data in data_raw]
a1, b1, R1 = data[0]
a2, b2, R2 = data[1]
P = inverse_mod(a1*b2-a2*b1,order)*(b2*R1-b1*R2)
print(P)
Q = inverse_mod(a2*b1-a1*b2,order)*(a2*R1-a1*R2)
print(Q)
def dlog(G, nG):
    dlogs, new_factors = [], []
    for p, e in factors:
        new_factors.append(p ** e)
        t = order // new_factors[-1]
        dlogs.append(discrete_log(t * nG, t * G, operation='+'))

    return CRT(dlogs, new_factors)
secret = int(dlog(P,Q))
print(bytes_to_long(secret))
