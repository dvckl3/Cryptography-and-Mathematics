from math import gcd
import os
from Crypto.Util.number import getPrime, bytes_to_long

e = 19
while True:
    p = getPrime(2048)
    q = getPrime(2048)
    if gcd((p - 1) * (q - 1), e) == 1:
        break
n = p * q

flag = os.environ.get("FLAG", "Alpaca{**** REDACTED ****}")
assert len(flag) == 26 and flag.startswith("Alpaca{") and flag.endswith("}")

m = bytes_to_long((flag * 1337).encode())
c = pow(m, e, n)

print(f"{n = }")
print(f"{e = }")
print(f"{c = }")
