import json
from pwn import *
BLOCK_SIZE = 32
def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len]*padding_len)
m1=b'\x01'*32
print(m1)
m2=b'\x01'*31
print(len(m2))
print(m2)
assert m1==pad(m2)
r = remote('socket.cryptohack.org', 13405)
response = r.recvuntil(b'JSON: ')
print(response)
r.send(json.dumps({'m1': m1.hex(), 'm2': m2.hex()}).encode())
flag = r.recvline()
print(flag)
