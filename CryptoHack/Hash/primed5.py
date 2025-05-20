from Crypto.Util.number import isPrime, bytes_to_long, long_to_bytes
import hashlib

x = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2"
y = "4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2"

print("x : ", bytes_to_long(bytes.fromhex(x)))

print("md5(x) : ", hashlib.md5(bytes.fromhex(x)).hexdigest())
print("md5(y) : ", hashlib.md5(bytes.fromhex(y)).hexdigest())

z = 1

xx = 0
yy = 0

while True:
    # append 1s till prime
    xx = bytes_to_long(bytes.fromhex(x) + long_to_bytes(z))
    yy = bytes_to_long(bytes.fromhex(y) + long_to_bytes(z))
    if isPrime(xx) and not isPrime(yy):
        p1=xx
        p2=yy
        break
    z += 2
print("x+z :", xx)
print("y+z :", yy)

print("md5(x+z) : ", hashlib.md5(long_to_bytes(xx)).hexdigest())
print("md5(y+z) : ", hashlib.md5(long_to_bytes(yy)).hexdigest())


from pwn import *
import json
r=remote("socket.cryptohack.org",13392)
p1=1042949915673747639548394979539773519387432406920217853474982925582324441002369106807062644005773384014539089496972340217284225886262811961269251256830829063
p2=1042949915673747639548394979539773519387432406920217853474982925582324441002369106807076447498466965142113959008696894268189128104207757197289383619865780743
payload1 = {"option": "sign","prime":p1}
r.recvline()
r.send(json.dumps(payload1).encode())
response=r.recvline().decode().strip()
payload=json.loads(response)
print(payload)
sig=payload["signature"]
payload2={"option":"check","prime":p2,"signature":sig,"a":298319899459}
r.send(json.dumps(payload2).encode())
response=r.recvline().decode().strip()
print(response)
