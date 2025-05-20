from pwn import *
import json
host, port = "socket.cryptohack.org", 13389
r = remote(host, port)
with open("message1.bin", "rb") as f:
    file1_hex = f.read().hex()
with open("message2.bin", "rb") as f:
    file2_hex = f.read().hex()
payload1 = {"document": file1_hex}
payload2 = {"document": file2_hex}
r.sendlineafter("Give me a document to store\n", json.dumps(payload1).encode())
response1 = r.recvline().decode().strip()
print(json.loads(response1))
r.sendline(json.dumps(payload2).encode())
response = r.recvline().decode().strip()
print(response)
# https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value
