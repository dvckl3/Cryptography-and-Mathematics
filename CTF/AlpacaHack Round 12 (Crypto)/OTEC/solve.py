from pwn import remote
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes
from itertools import zip_longest

def decrypt(ciphertext, key):
    return unpad(AES.new(key, AES.MODE_ECB).decrypt(ciphertext), 16)

host = "34.170.146.252"
port = 62340
G = secp256k1.G

def get_flag_part_1():
    r = remote(host, port)
    A_x = int(r.recvline().decode().split('=')[1])
    A_y = int(r.recvline().decode().split('=')[1])
    A = Point(A_x, A_y, secp256k1)
    r.sendline(f"{G.x}, {G.y}".encode())
    r.recvuntil('B>')
    ct0 = r.recvline().decode().strip()
    ct1 = r.recvline().decode().strip()
    ct2 = r.recvline().decode().strip()
    ct0_bytes = bytes.fromhex(ct0)
    key = long_to_bytes(A.x, 32)
    r.close()
    return decrypt(ct0_bytes, key)

def get_flag_part_2():
    r = remote(host, port)
    A_x = int(r.recvline().decode().split('=')[1])
    A_y = int(r.recvline().decode().split('=')[1])
    A = Point(A_x, A_y, secp256k1)
    B = G + A
    r.sendline(f"{B.x}, {B.y}".encode())
    r.recvuntil('B>')
    ct0 = r.recvline().decode().strip()
    ct1 = r.recvline().decode().strip()
    ct2 = r.recvline().decode().strip()
    ct1_bytes = bytes.fromhex(ct1)
    key = long_to_bytes(A.x, 32)
    r.close()
    return decrypt(ct1_bytes, key)

def get_flag_part_3():
    r = remote(host, port)
    A_x = int(r.recvline().decode().split('=')[1])
    A_y = int(r.recvline().decode().split('=')[1])
    A = Point(A_x, A_y, secp256k1)
    order = secp256k1.q
    scale = pow(2, -1, order)
    B = A * scale
    r.sendline(f"{B.x}, {B.y}".encode())  
    r.recvuntil('B>')
    ct0 = r.recvline().decode().strip()
    ct1 = r.recvline().decode().strip()
    ct2 = r.recvline().decode().strip()
    ct2_bytes = bytes.fromhex(ct2)
    key = bytes([0] * 32)
    r.close()
    return decrypt(ct2_bytes, key)

if __name__ == "__main__":
    flag0 = get_flag_part_1()
    flag1 = get_flag_part_2()
    flag2 = get_flag_part_3()
    full_flag = bytes(
        [c for tup in zip_longest(flag0, flag1, flag2) for c in tup if c is not None]
    )
    print(full_flag.decode())
