from pwn import *
import json 
import codecs
import base64
import random 
from Crypto.Util.number import bytes_to_long,long_to_bytes

host,port = "socket.cryptohack.org", 13377
r = remote(host,port)
def json_recv():
    line = r.recvline()
    return json.loads(line.decode())
def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)
for i in range(100):
    response=json_recv()
    print(response)
    if response["type"] == "hex":
        ct = response["encoded"]
        pt = bytes.fromhex(ct).decode()
        payload = {"decoded" : pt}
        json_send(payload)
    if response["type"] == "utf-8":
        ct = response["encoded"]
        pt = ''.join([chr(b) for b in ct])
        payload = {"decoded" : pt}
        json_send(payload)
    if response["type"] == "base64":
        ct = response["encoded"]
        pt = base64.b64decode(ct).decode()
        payload = {"decoded": pt}
        json_send(payload)
    if response["type"] == "rot13":
        ct = response["encoded"]
        pt = codecs.decode(ct,'rot_13')
        payload = {"decoded": pt}
        json_send(payload)
    if response["type"] == "bigint":
        ct = response["encoded"]
        pt = long_to_bytes(int(ct,16)).decode()
        payload = {"decoded":pt}
        json_send(payload)
response=json_recv()
print(response)
