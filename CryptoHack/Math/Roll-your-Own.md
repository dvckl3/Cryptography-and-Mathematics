# Roll your Own
Source code của bài:
```python
from Crypto.Util.number import getPrime
import random
from utils import listener

FLAG = 'crypto{???????????????????????????????????}'

class Challenge():
    def __init__(self):
        self.no_prompt = True
        self.q = getPrime(512)
        self.x = random.randint(2, self.q)

        self.g = None
        self.n = None
        self.h = None

        self.current_step = "SHARE_PRIME"

    def check_params(self, data):
        self.g = int(data['g'], 16)
        self.n = int(data['n'], 16)
        if self.g < 2:
            return False
        elif self.n < 2:
            return False
        elif pow(self.g,self.q,self.n) != 1:
            return False
        return True

    def check_secret(self, data):
        x_user = int(data['x'], 16)
        if self.x == x_user:
            return True
        return False

    def challenge(self, your_input):
        if self.current_step == "SHARE_PRIME":
            self.before_send = "Prime generated: "
            self.before_input = "Send integers (g,n) such that pow(g,q,n) = 1: "
            self.current_step = "CHECK_PARAMS"
            return hex(self.q)

        if self.current_step == "CHECK_PARAMS":
            check_msg = self.check_params(your_input)
            if check_msg:
                self.x = random.randint(0, self.q)
                self.h = pow(self.g, self.x, self.n)
            else:
                self.exit = True
                return {"error": "Please ensure pow(g,q,n) = 1"}

            self.before_send = "Generated my public key: "
            self.before_input = "What is my private key: "
            self.current_step = "CHECK_SECRET"

            return hex(self.h)

        if self.current_step == "CHECK_SECRET":
            self.exit = True
            if self.check_secret(your_input):
                return {"flag": FLAG}
            else:
                return {"error": "Protocol broke somewhere"}

        else:
            self.exit = True
            return {"error": "Protocol broke somewhere"}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13403)
```
Luồng của bài:

Đầu tiên trả về cho ta một số nguyên tố $\displaystyle q$. Bước tiếp theo nó check params điều kiện là $\displaystyle g^{q} \equiv 1\bmod n$. Ta được chọn cặp số $\displaystyle ( g,n)$. Sau đó nó sinh random số $\displaystyle x$ rồi tính $\displaystyle g^{x} =h\bmod n$. 

```python
        if self.current_step == "CHECK_SECRET":
            self.exit = True
            if self.check_secret(your_input):
                return {"flag": FLAG}
            else:
                return {"error": "Protocol broke somewhere"}
```
Ta cần giải tìm $\displaystyle x$ để server trả về flag. 
Vấn đề của bài này: Lúc đầu mình cố nghĩ tới cách tạo $\displaystyle n$ để nó là một cyclic group rồi sau đó giải DLP. Nhưng mình nhận ra rằng ở bài này không thể đưa về trên nhóm mà làm được. Lí do là vì khi ta chọn $\displaystyle g$ thỏa mãn $\displaystyle g^{q} \equiv 1\bmod n$ thì $\displaystyle g$ có cấp đúng là $\displaystyle q$ . Điều này dẫn tới các Attack nhằm vào cấp để khai thác như Pohlig-Hellman sẽ không còn hiệu quả nữa. Vậy ta cần phải làm sao....

Mình thử chọn $\displaystyle ( g,n) =( q+1,q)$. Thì khi đó 

$$\begin{equation*}
( q+1)^{q} =1\bmod q
\end{equation*}$$

Sau đó khi tính $\displaystyle h=( q+1)^{x} =1\bmod q$ thì cách này fail. Do $\displaystyle x$ bằng bao nhiêu đi nữa thì nó cũng trả về $\displaystyle 1$. 

Trick lỏ giải bài này là nâng lên $\displaystyle n=q^{2}$. Lúc này 

$$\begin{equation*}
( q+1)^{x} \equiv qx+1\bmod q^{2}
\end{equation*}$$

Nên ta có $\displaystyle h=qx+1\bmod q^{2}$ và ta tính được $\displaystyle x=( h-1) //q$.

Script:

```python
# from pwn import *
# from Crypto.Util.number import *
# import json
# from sage.all import *
# host,port = "socket.cryptohack.org",13398
# r = remote(host,port)
# def json_recv():
#     line = r.recvline()
#     return json.loads(line.decode())
# def json_send(hsh):
#     request = json.dumps(hsh).encode()
#     r.sendline(request)
from pwn import *
from sage.all import *
from Crypto.Util.number import *
import json
r = remote("socket.cryptohack.org" ,13403)
r.recvuntil(b"Prime generated: ")
q = r.recvline().strip()
q = q.decode().strip('"')
q = int(q,16)
n = q**2
g = q + 1 
payload1 = {"g":hex(g),"n":hex(n)}
r.sendlineafter(b"pow(g,q,n) = 1: ", json.dumps(payload1).encode())
response = r.recvuntil(b"Generated my public key: ")
response = r.recvline().strip()
h = response.decode().strip('"')
h = int(h,16)
print(h)
x = (h-1)//q
get_flag = {"x" : hex(x)}
r.send(json.dumps(get_flag).encode())
response = r.recvline().strip()
print(response)
```
Nói thêm về hệ mật Paillier https://en.wikipedia.org/wiki/Paillier_cryptosystem
