from Crypto.Util.number import *
from sage.all import *
from math import prod
from secrets import randbelow
import random
e=0x10001
N=... 
ct=...
def get_prime(seed):
    p=1
    r=random.Random()
    r.seed(seed)
    while not isPrime(p):
        p=r._randbelow(2**256) | 1
    return p
primes_list=[]
msg=[]
for seed in range(2**128):
    p=get_prime(seed)
    if N % p == 0:
        print(f"thử với seed = {seed}")
        print(p)
        primes_list.append(p)
        d_i=pow(e,-1,p-1)
        m=pow(ct,d_i,p)
        msg.append(m)
    if len(primes_list)==5:
        break
m=crt(msg,primes_list)
print(long_to_bytes(m))
