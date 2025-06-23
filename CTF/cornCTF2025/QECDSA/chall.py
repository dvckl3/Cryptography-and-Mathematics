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


if __name__ == "__main__":
    d = randbelow(q)
    P = d * G

    pp, qq = getPrime(0xB0), getPrime(0xB0)
    while pp % 4 != 3 or qq % 4 != 3:
        pp, qq = getPrime(0xB0), getPrime(0xB0)

    x = randbelow(pp*qq)
    rng = BlumBlumShub(pp, qq, x)

    sigs = []
    for m, k in zip(msgs, rng):
        z = int.from_bytes(sha256(m).digest(), "big") % q
        r, s = sign(d, z, k)
        assert verify(P, z, r, s)
        sigs.append((r, s))
    print(f"{sigs = }")

    with open("flag.txt", "rb") as f:
        flag = f.read().strip()
    key = sha256(str(d).encode()).digest()
    cipher = AES.new(key, AES.MODE_CTR)
    ct = cipher.encrypt(flag)
    nonce = cipher.nonce
    print(f"{ct = }")
    print(f"{nonce = }")

