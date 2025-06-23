import secrets
from Crypto.Util.number import bytes_to_long
import sys

FLAG = b"There was an actual flag here once"
FLAG = sys.argv[1].encode() if len(sys.argv) > 1 else FLAG
BS = 1024
FLAG = bytes_to_long(FLAG)
set_random_seed(secrets.randbelow(int(2**64)))
p = random_prime(2 ** (BS), lbound=2 ** (BS - 1))
q = random_prime(2** (BS), lbound=2 ** (BS - 1))
n = p * q
e = 0x10001
c = pow(FLAG, e, n)

print(f"n = {n:x}")
print(f"e = {e:x}")
print(f"c = {int(c):x}")

pp, qq = (
    p.digits(base=7, padto=int(log(2 ** (BS + 1), 7)) + 2),
    q.digits(base=7, padto=int(log(2 ** (BS + 1), 7)) + 2),
)
V = vector([(pp[i] + qq[i]) % 7 for i in range(len(pp))])
print(V)
