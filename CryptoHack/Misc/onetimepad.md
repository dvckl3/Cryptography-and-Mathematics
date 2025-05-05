Chall cho ta một file source code như sau: 

```python
#!/usr/bin/env python3

import time
from Crypto.Util.number import long_to_bytes
import hashlib
from utils import listener


FLAG = b'crypto{????????????????????}'


def generate_key():
    current_time = int(time.time())
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()


def encrypt(b):
    key = generate_key()
    assert len(b) <= len(key), "Data package too large to encrypt"
    ciphertext = b''
    for i in range(len(b)):
        ciphertext += bytes([b[i] ^ key[i]])
    return ciphertext.hex()


class Challenge():
    def __init__(self):
        self.before_input = "Gotta go fast!\n"

    def challenge(self, your_input):
        if not 'option' in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'get_flag':
            return {"encrypted_flag": encrypt(FLAG)}

        elif your_input['option'] == 'encrypt_data':
            input_data = bytes.fromhex(your_input['input_data'])
            return {"encrypted_data": encrypt(input_data)}

        else:
            return {"error": "Invalid option"}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
"""
When you connect, the 'challenge' function will be called on your JSON
input.
"""
listener.start_server(port=13372)
```

Phân tích: 
```python

def generate_key():
    current_time = int(time.time())
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()

```
Đoạn code này cho ta biết một key sẽ được tạo ra theo thời gian và do đó nó sẽ không cố định. 
Tiếp theo 
```python
def encrypt(b):
    key = generate_key()
    assert len(b) <= len(key), "Data package too large to encrypt"
    ciphertext = b''
    for i in range(len(b)):
        ciphertext += bytes([b[i] ^ key[i]])
    return ciphertext.hex()

```
Hàm này thực hiện phép XOR giữa input và key được tạo ra. 
Cuối cùng là lớp challenge ở cuối. Tùy vào input của ta mà server sẽ trả về encrypt_data hoặc encrypt_flag. Như vậy ta sẽ kết nối đến server để lấy encrypt_data và encrypt_flag, xor 2 giá trị này lại để tìm ra key và cuối cùng xor key này với encrypt_flag để thu được flag cần tìm.
Key là output của hàm băm nên encrypt_data mà ta nhập phải phải là một chuỗi binary có độ dài 32 bytes. 
Code sử dụng pwntools như dưới đây: 
```python
from pwn import *
import json 
from Cryptodome.Util.number import *

conn=remote('socket.cryptohack.org',13372)
conn.recvline()
def send_request(option,input_data=None):
    request={"option":option,"input_data":input_data}
    conn.sendline(json.dumps(request).encode())
    response=conn.recvline()
    return json.loads(response.decode())
plaintext=b'A' * 32
response=send_request("encrypt_data",plaintext.hex())
ciphertext=bytes.fromhex(response["encrypted_data"])
key=bytes([ciphertext[i] ^ ord("A") for i in range(32)])
response=send_request("get_flag")
encrypted_flag=bytes.fromhex(response["encrypted_flag"])
flag=bytes([encrypted_flag[i] ^ key[i] for i in range(len(encrypted_flag))])    
print(flag.decode())
```
