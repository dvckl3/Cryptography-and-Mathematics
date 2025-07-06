import os
import signal
import secrets
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes

signal.alarm(60)

flag = os.environ.get("FLAG", "Alpaca{**** REDACTED ****}").encode()

# Oblivious Transfer using Elliptic Curves
G = secp256k1.G
a = secrets.randbelow(secp256k1.q)
A = a * G

print(f"{A.x = }")
print(f"{A.y = }")

x, y = map(int, input("B> ").split(","))
B = Point(x, y, secp256k1)

k0 = long_to_bytes((a * B).x, 32)
k1 = long_to_bytes((a * (B - A)).x, 32)

def encrypt(message, key):
    return AES.new(key, AES.MODE_ECB).encrypt(pad(message, 16))

print(encrypt(flag[0::3], k0).hex())
print(encrypt(flag[1::3], k1).hex())
print(encrypt(flag[2::3], bytes(c0 ^ c1 for c0, c1 in zip(k0, k1))).hex())
    
