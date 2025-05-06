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
Giả sử thực hiện $\displaystyle i$ lần. Thì khi đó $\displaystyle p=Ax_{i} +B$. Giả sử $\displaystyle i\geqslant 3$ chẳng hạn, mình muốn tìm một công thức gọn hơn cho $\displaystyle p$ theo $\displaystyle A,x,B$, trong đó $\displaystyle x_{1} =x=seed$

$$\begin{gather*}
x_{i} =Ax_{i-1} +B\\
\Longrightarrow p=Ax_{i} +B=A( Ax_{i-1} +B) +B=A^{2} x_{i-1} +AB+B\\
=A^{2}( Ax_{i-2} +B) +AB+B\\
=A^{3} x_{i-2} +A^{2} B+AB+B=B\left( A^{2} +A+1\right) +A^{3} x_{i-2}\\
=....=A^{i} x+B\sum _{j=0}^{i-1} A^{j} =A^{i} x+B\frac{A^{i} -1}{A-1}
\end{gather*}$$

Như vậy mình có được 

$$\begin{equation*}
p=A^{i} x+B\frac{A^{i} -1}{A-1}\bmod 2^{512}
\end{equation*}$$

Tương tự, nếu như ta thực hiện $\displaystyle j$ lần để `get\_num()` tạo ra số $\displaystyle q$ thì khi đó 

$$\begin{equation*}
q=A^{j} x+B\frac{A^{j} -1}{A-1}\bmod 2^{512}
\end{equation*}$$

Ở đây ta gọi lấy $\displaystyle p$ trước rồi mới lấy $\displaystyle q$ tức là trạng thái state khi ta gọi $\displaystyle q$ sẽ là chuyển tiếp từ trạng thái của $\displaystyle p$ cho nên ta có $\displaystyle j=i+t$ với $\displaystyle t$ là một số nào đó mà ta không rõ. 

Vậy thì 

$$\begin{gather*}
p=A^{i} x+B\frac{A^{i} -1}{A-1}\bmod 2^{512}\\
q=A^{i+t} x+B\frac{A^{i+t} -1}{A-1}\bmod 2^{512}
\end{gather*}$$

Bây giờ ta có 

$$\begin{gather*}
q=A^{i+t} x+B\left( A^{i+t-1} +...+1\right) \ \bmod 2^{512}\\
p=A^{i} x+B\left( A^{i-1} +...+1\right) \ \bmod 2^{512}
\end{gather*}$$

Xét

$$\begin{gather*}
A^{t}\left(\underbrace{A^{i} x+B\left( A^{i-1} +...+1\right)}_{=p}\right) +B\left( A^{t-1} +...+1\right)\bmod 2^{512}\\
=A^{t+i} x+B\left( A^{t+i-1} +...+A^{t}\right) +B\left( A^{t-1} +...+1\right) \ \bmod 2^{512}\\
=A^{t+i} x+B\left( A^{t+i-1} +...+A^{t} +A^{t-1} +...+1\right) =q\\
\Longrightarrow q=A^{t} p+B\left( A^{t-1} +...+1\right)\bmod 2^{512}\\
\Longrightarrow pq-N=A^{t} p^{2} +B\left( A^{t-1} +...+1\right) p-N=0\bmod 2^{512}
\end{gather*}$$



Ta có phương trình bậc 2 với các hệ số 

$$\begin{equation*}
\begin{cases}
a=A^{t} & \\
b=B\left( A^{t-1} +...+1\right) =B\sum _{j=0}^{t-1} A^{j} & \\
c=-N & 
\end{cases}
\end{equation*}$$


Lưu ý ở bài này $\displaystyle A$ là số lẻ cho nên ta không thể lấy $\displaystyle ( A-1)^{-1}$ được. 

Giả sử ta muốn giải 


$$\begin{gather*}
f( x) =ax^{2} +bx+c\\
\Longrightarrow \Delta =\sqrt{b^{2} -4ac}\\
\Longrightarrow r_{1,2} =\frac{-b\pm \sqrt{b^{2} -4ac}}{2a}\\
\Longrightarrow 2r_{1,2} \equiv \left( -b\pm \sqrt{b^{2} -4ac}\right) a^{-1}\bmod 2^{512}\\
\Longrightarrow r_{1,2} =\frac{\left( -b\pm \sqrt{b^{2} -4ac}\right) a^{-1}}{2}\bmod 2^{511}
\end{gather*}$$

Mấu chốt ở đây là reduce từ modulo $\displaystyle 2^{512}$ về modulo $\displaystyle 2^{511}$.

Ta không thể chia 2 trên modulo $\displaystyle 2^{512}$ được, giả sử ta có một số $\displaystyle r$ chẳng hạn và ta biết $\displaystyle r\vdots 2$. Ta muốn tính $\displaystyle \frac{r}{2}\bmod 2^{512}$ thì ta cần làm sao?

Đầu tiên ta viết $\displaystyle r=k+t2^{512}$ thì khi đó $\displaystyle \frac{r}{2} =\frac{k}{2} +t2^{511}$. Ta lấy $\displaystyle r$ chia lấy phần nguyên cho 2 rồi sau đó tính modulo theo $\displaystyle 2^{511}$ là ra được số dư, sau đó nếu muốn lift lên modulo $\displaystyle 2^{512}$ lại thì ta cần cộng thêm $\displaystyle t2^{511}$ với $\displaystyle t\in \{0,1\}$ (vì các số trong bài lấy theo modulo $\displaystyle 2^{512}$ nên không thể quá lớn được.)

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
