from sage.all import *
from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from fastecdsa.curve import secp256k1
from hashlib import sha256
from secrets import randbelow


G = secp256k1.G
q = secp256k1.q


def sign(d, z, k):
    r = (k * G).x
    s = (z + r * d) * pow(k, -1, q) % q
    return r, s


def verify(P, z, r, s):
    u1 = z * pow(s, -1, q) % q
    u2 = r * pow(s, -1, q) % q
    x = (u1 * G + u2 * P).x
    return x == r


def BlumBlumShub(p: int, q: int, seed: int):
    assert q % 4 == 3 and p % 4 == 3
    M = q * p
    xn = seed * q % M
    while True:
        xn = (xn * xn) % M
        yield xn
    

msgs = [
    b"https://www.youtube.com/watch?v=COeeb-dMdls",
    b"https://www.youtube.com/watch?v=-LRYfH3yy6Q",
    b"https://www.youtube.com/watch?v=s01k6hooTg0",
    b"https://www.youtube.com/watch?v=clSD6wX96Bo",
    b"https://www.youtube.com/watch?v=BNyiQyOz_8g",
    b"https://www.youtube.com/watch?v=cLjXsVkPUPc",
    b"https://www.youtube.com/watch?v=OEMFsEpm9Tg"
]

sigs = [(34157310969598839165020823267578826895648515675619978262514680951491430172658, 5112666564240248882809538022395694948780679143581025544587295608546432738566), (81474307292381542801094668781061629150821916819688082620439198544528568539292, 50643646984179044735238516852199185526042237136594676306234314270001161711708), (113542324762610776437072768412796281491553845023367451408397949067699802908300, 59200362408107407295921463127168482530188496177503929217425579826584630651942), (96378116170285244331054642805274109551392523202264798128983135781613505529225, 93260598576404823080995310921623537487938656634383364444941698104604123342760), (77839139577325611159429319891069500573653290799738037449423678407080007991617, 48818759505422033138175079627907090638704104486956773638802624745514802326745), (55196598662099499362979912760006387571341048443130808945815946776864817840913, 8005551821799845968817709145829865534294908858929653586870278219562640694678), (32413705847960341669487502722360428842837643497685089853410054178113631927899, 88583444154102521526843991325196555691405405323638728504879015276435020936519)]
ct = b'\xe0v\xfb\x0b\xb8\x10\xd3?K%\xef\x1aG\xdf\x06L\xe8\xd2)\xa5w\xed\xa4/\xb8\xd3\x80#\x00\n\x1df\xdf3'
nonce = b'Dt\x99\x0c\xcc\xe0\x1f\xa6'

# s = k^-1 * (z + r * d) (mod q)
# k_i = s_i^-1 * (z_i + r_i * d) + t_i * q
# t_i <= M // q

# k_i - k_j = 0 (mod qq)
#           = (s_i^-1 * (z_i + r_i * d) + t_i * q) - (s_j^-1 * (z_j + r_j * d) + t_j * q) + u_{i, j} * qq
# u_{i, j} <= M // qq

R = GF(q)["d, x"]
d = R.gen()
rs = [r for r, _ in sigs]
ss = [s for _, s in sigs]

ks = [pow(s, -1, q) * (z + r * d) for (r, s), z in zip(sigs, map(lambda m: int.from_bytes(sha256(m).digest(), "big") % q, msgs))]

t = 1
M = Matrix(ZZ, len(ks), 2 * t)
for i in range(len(ks) - t + 1):
    for j in range(t):
        M[i, 2 * j] = ks[i + j].constant_coefficient()
        M[i, 2 * j + 1] = ks[i + j].monomial_coefficient(d)

L = Matrix.block(ZZ, [
    [1, M],
    [0, q],
])

for i in range(M.nrows(), L.ncols()):
    L.rescale_col(i, 2**1024)

L = L.LLL()

rows = []
for row in L:
    if row[-M.ncols():].is_zero():
        rows.append(row[:-M.ncols()])

M = Matrix(ZZ, rows).T

L = Matrix.block(ZZ, [
    [1, M],
    [0, q],
])

for i in range(M.nrows(), L.ncols()):
    L.rescale_col(i, 2**1024)

L = L.LLL()

rows = []
for row in L:
    if row[-M.ncols():].is_zero():
        print(row[:-M.ncols()])
        rows.append(row[:-M.ncols()])

M = Matrix(GF(q), rows)

ks_prime = R.gen(1) * M.row(0)

polys = [k0 - k1 for k0, k1 in zip(ks, ks_prime)]

M, mons = Sequence(polys).coefficients_monomials(sparse=False)

M, rhs = M[:, :-1], -M.column(-1)

sol = M.solve_right(rhs)
d = int(sol[0])

key = sha256(str(d).encode()).digest()
cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
flag = cipher.decrypt(ct)
print(flag)
