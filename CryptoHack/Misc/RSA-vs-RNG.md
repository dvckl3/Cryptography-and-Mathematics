# RSA vs RNG
Source code của bài:
```python
from Crypto.Util.number import *
import json

MOD = 2**512
A = 2287734286973265697461282233387562018856392913150345266314910637176078653625724467256102550998312362508228015051719939419898647553300561119192412962471189
B = 4179258870716283142348328372614541634061596292364078137966699610370755625435095397634562220121158928642693078147104418972353427207082297056885055545010537

FLAG = b'crypto{???????????????????????????}'

class PRNG:
    def __init__(self, seed):
        self.state = (seed % MOD)

    def get_num(self):
        self.state = (A * self.state + B) % MOD
        return self.state

    def get_prime(self):
        p = self.get_num()
        while not isPrime(p):
            p = self.get_num()
        return p

seed = getRandomRange(1, MOD)
rng = PRNG(seed)

P = rng.get_prime()
Q = rng.get_prime()

N = P * Q
E = 0x10001
pt = bytes_to_long(FLAG)
ct = long_to_bytes(pow(pt, E, N))

json.dump({{"N": 95397281288258216755316271056659083720936495881607543513157781967036077217126208404659771258947379945753682123292571745366296203141706097270264349094699269750027004474368460080047355551701945683982169993697848309121093922048644700959026693232147815437610773496512273648666620162998099244184694543039944346061, "E": 65537, "ciphertext": "04fee34327a820a5fb72e71b8b1b789d22085630b1b5747f38f791c55573571d22e454bfebe0180631cbab9075efa80796edb11540404c58f481f03d12bb5f3655616df95fb7a005904785b86451d870722cc6a0ff8d622d5cb1bce15d28fee0a72ba67ba95567dc5062dfc2ac40fe76bc56c311b1c3335115e9b6ecf6282cca"}
    'N': N,{"N": 95397281288258216755316271056659083720936495881607543513157781967036077217126208404659771258947379945753682123292571745366296203141706097270264349094699269750027004474368460080047355551701945683982169993697848309121093922048644700959026693232147815437610773496512273648666620162998099244184694543039944346061, "E": 65537, "ciphertext": "04fee34327a820a5fb72e71b8b1b789d22085630b1b5747f38f791c55573571d22e454bfebe0180631cbab9075efa80796edb11540404c58f481f03d12bb5f3655616df95fb7a005904785b86451d870722cc6a0ff8d622d5cb1bce15d28fee0a72ba67ba95567dc5062dfc2ac40fe76bc56c311b1c3335115e9b6ecf6282cca"}
    'E': E,
    'ciphertext': ct.hex()
}, open('flag.enc', 'w'))
```
Và một file json data chứa các tham số $N$, $E$ và ciphertext
```
{"N": 95397281288258216755316271056659083720936495881607543513157781967036077217126208404659771258947379945753682123292571745366296203141706097270264349094699269750027004474368460080047355551701945683982169993697848309121093922048644700959026693232147815437610773496512273648666620162998099244184694543039944346061, "E": 65537, "ciphertext": "04fee34327a820a5fb72e71b8b1b789d22085630b1b5747f38f791c55573571d22e454bfebe0180631cbab9075efa80796edb11540404c58f481f03d12bb5f3655616df95fb7a005904785b86451d870722cc6a0ff8d622d5cb1bce15d28fee0a72ba67ba95567dc5062dfc2ac40fe76bc56c311b1c3335115e9b6ecf6282cca"}
```
Bài cho ta một modulo và cặp số $A,B$. `class PRNG` sẽ lấy đầu vào là một seed. 

Ta gọi state ban đầu là $\displaystyle x$ chẳng hạn thì $\displaystyle state=seed\ \bmod MOD$. 

Ở mỗi bước, khi ta gọi hàm `get_num` nó sẽ tính $\displaystyle ( Ax+B) \ \bmod 2^{512}$ còn khi gọi `get_prime` thì nó sẽ lấy $\displaystyle p=( Ax+B)\bmod 2^{512}$ liên tục cho tới khi $\displaystyle p$ là số nguyên tố.


i state ban đầ
Mấu chốt của bài này là hai số nguyên tố $\displaystyle p,q$ được sinh ra từ cùng 1 seed và ta phải tìm cách khôi phục lại 2 số này để giải RSA. 


Đầu tiên ta thử viết lại $\displaystyle p,q$ theo $\displaystyle A,B,x$.


Code giải:

```python
from sage.all import *
from Crypto.Util.number import *
MOD = 2**512
A = 2287734286973265697461282233387562018856392913150345266314910637176078653625724467256102550998312362508228015051719939419898647553300561119192412962471189
B = 4179258870716283142348328372614541634061596292364078137966699610370755625435095397634562220121158928642693078147104418972353427207082297056885055545010537

class PRNG:
    def __init__(self, seed):
        self.state = (seed % MOD)

    def get_num(self):
        self.state = (A * self.state + B) % MOD
        return self.state

    def get_prime(self):
        p = self.get_num()
        while not isPrime(p):
            p = self.get_num()
        return p

N = 95397281288258216755316271056659083720936495881607543513157781967036077217126208404659771258947379945753682123292571745366296203141706097270264349094699269750027004474368460080047355551701945683982169993697848309121093922048644700959026693232147815437610773496512273648666620162998099244184694543039944346061
E = 65537

ciphertext = "04fee34327a820a5fb72e71b8b1b789d22085630b1b5747f38f791c55573571d22e454bfebe0180631cbab9075efa80796edb11540404c58f481f03d12bb5f3655616df95fb7a005904785b86451d870722cc6a0ff8d622d5cb1bce15d28fee0a72ba67ba95567dc5062dfc2ac40fe76bc56c311b1c3335115e9b6ecf6282cca"
ct=int(ciphertext,16)

assert gcd(N,A)==1


# x = 0
# while True:
#     x+=1
#     print(x)
#     a = pow(A,x,MOD)
#     b = B * sum(pow(A,i,MOD) for i in range(x)) % MOD
#     c = - N 
#     try: 
#         det=int(Mod(b ** 2 - 4 * a * c, MOD).nth_root(2))
#         rt1=(-b + det) * pow(a, -1, MOD) % MOD
#         rt2=(-b - det) * pow(a, -1, MOD) % MOD
#         for k in range(2):
#             p=((rt1 % (MOD//2)) // 2 + k*(MOD//2))
#             if gcd(p,N)>1:
#                 break
#             else:
#                 print("failed")
#             q=N//p
#             phi=(p-1)*(q-1)
#             d=pow(E,-1,phi)
#             m=pow(ct,d,N)
#             print(m)
#         for k in range(2):
#             p=((rt2 % (MOD//2)) // 2 + k*(MOD//2))
#             if gcd(p,N)>1:
#                 break
#             else:
#                 print("failed")
#             q=N//p
#             phi=(p-1)*(q-1)
#             d=pow(E,-1,phi)
#             m=pow(ct,d,N)
#             print(m)
#     except:
#         print("error")
x=0
found = true
while found:
    x+=1
    print(x)
    a = pow(A,x,MOD)
    b = B * sum(pow(A,i,MOD) for i in range(x)) % MOD
    c = - N 
    try:
        det = int(Mod(b ** 2 - 4 * a * c, MOD).nth_root(2))
        rt1 = (-b + det) * pow(a,-1,MOD) % MOD
        rt2 = (-b - det) * pow(a,-1,MOD) % MOD
        for k in range(2):
            p = (rt1 % (MOD // 2)) // 2 + k * (MOD // 2)
            if N % p == 0:
                print(p)
                q=N//p
                phi=(p-1)*(q-1)
                d=pow(E,-1,phi)
                m=pow(ct,d,N)
                print(long_to_bytes(m).decode())
                found = false
            else:
                print("failed")
        for k in range(2):
            p = (rt2 % (MOD // 2)) // 2 + k * (MOD // 2)
            if N % p == 0:
                print(p)
                q=N//p
                phi=(p-1)*(q-1)
                d=pow(E,-1,phi)
                m=pow(ct,d,N)
                print(long_to_bytes(m).decode())
                found=false
            else:
                print("failed")
    except:
        print("failed")
```
