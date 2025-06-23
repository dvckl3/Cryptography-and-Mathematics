from pwn import *
from tqdm import tqdm
from Crypto.Util.number import long_to_bytes

r = remote('ecrsa.challs.cornc.tf', 1337, ssl=True)
#r = process(["sage", "ecrsa.sage"])

#print(r.recvline().strip().decode())
r.recvline()
r.recvline()
r.recvline()

e = 0x10001
n = int(r.recvline()[3:].strip().decode())
enc_flag = int(r.recvline()[6:].strip().decode())

points = []
for i in range(4):
	r.sendline(b"1")
	r.recvuntil(b"Enter message: ")
	r.sendline(str(i + 10).encode())
	r.recvuntil(b"nate of your point: ")
	r.sendline(b"15742124811802261825032151445683304673585166434467766384677222858894448558416209481343780954514298296776044430144242408031444603984183667690328921038037481")
	pt = r.recvline().split(b": ")[-1].strip().decode()[1: -1].split(", ")
	point = [int(pt[0]), int(pt[1])]
	points.append(point)

P.<a, b> = PolynomialRing(ZZ)
polys = []
for point in points:
	polys.append(point[0]^3 + point[0]*a + b - point[1]^2)

a1 = polys[0].resultant(polys[1], b)
a2 = polys[1].resultant(polys[2], b)
a3 = polys[2].resultant(polys[3], b)
curve_p = int(list(factor(gcd(a1.resultant(a2, a), a2.resultant(a3, a))))[-1][0])

def rec(p, x1, y1, x2, y2):
    a = pow(x1 - x2, -1, p) * (pow(y1, 2, p) - pow(y2, 2, p) - (pow(x1, 3, p) - pow(x2, 3, p))) % p
    b = (pow(y1, 2, p) - pow(x1, 3, p) - a * x1) % p
    return int(a), int(b)

a, b = rec(curve_p, points[0][0], points[0][1], points[1][0], points[1][1])

K = GF(curve_p)
a = K(a)
b = K(b)
E = EllipticCurve(K, (a, b))
#order = E.order()
order = 16069075899419272706313306230384148392684766596987923274252840802156807638348274231565457533546984784193487763139164096443059279726687808489053779972143886
E.set_order(order)

my_point = E.lift_x(15742124811802261825032151445683304673585166434467766384677222858894448558416209481343780954514298296776044430144242408031444603984183667690328921038037481)
new_m = pow(2,e,n)

r.sendline(b"1")
r.recvuntil(b"Enter message: ")
r.sendline(str(new_m).encode())
r.recvuntil(b"nate of your point: ")
r.sendline(b"15742124811802261825032151445683304673585166434467766384677222858894448558416209481343780954514298296776044430144242408031444603984183667690328921038037481")
pt = r.recvline().split(b": ")[-1].strip().decode()[1: -1].split(", ")
point = E(int(pt[0]), int(pt[1]))

secret_point = point - 2*my_point

r.sendline(b"1")
r.recvuntil(b"Enter message: ")
r.sendline(str(enc_flag).encode())
r.recvuntil(b"nate of your point: ")
r.sendline(b"15742124811802261825032151445683304673585166434467766384677222858894448558416209481343780954514298296776044430144242408031444603984183667690328921038037481")
pt = r.recvline().split(b": ")[-1].strip().decode()[1: -1].split(", ")
test_point = E(int(pt[0]), int(pt[1]))

upper_limit = n
lower_limit = 0

prev = test_point - secret_point
for i in tqdm(range(1, 512)):
	test = (enc_flag * pow(2**i,e,n)) % n
	r.sendline(b"1")
	r.recvuntil(b"Enter message: ")
	r.sendline(str(test).encode())
	r.recvuntil(b"nate of your point: ")
	r.sendline(b"15742124811802261825032151445683304673585166434467766384677222858894448558416209481343780954514298296776044430144242408031444603984183667690328921038037481")
	pt = r.recvline().split(b": ")[-1].strip().decode()[1: -1].split(", ")
	pt = E(int(pt[0]), int(pt[1]))
	if prev*2 == pt - secret_point:
		upper_limit = (upper_limit + lower_limit)//2
	else:
		lower_limit = (lower_limit + upper_limit)//2
	prev = pt-secret_point

print(long_to_bytes(upper_limit)[:-1] + b"}")


