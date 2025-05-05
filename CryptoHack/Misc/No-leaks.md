# No Leaks
Server của bài `socket.cryptohack.org 13370`
Source code của bài: 
```python
import base64
import os
from utils import listener

FLAG = "crypto{????????????}"


def xor_flag_with_otp():
    flag_ord = [ord(c) for c in FLAG]
    otp = os.urandom(20)

    xored = bytearray([a ^ b for a, b in zip(flag_ord, otp)])

    # make sure our OTP doesnt leak any bytes from the flag
    for c, p in zip(xored, flag_ord):
        assert c != p

    return xored


class Challenge():
    def __init__(self):
        self.before_input = "No leaks\n"

    def challenge(self, your_input):
        if your_input == {"msg": "request"}:
            try:
                ciphertext = xor_flag_with_otp()
            except AssertionError:
                return {"error": "Leaky ciphertext"}

            ct_b64 = base64.b64encode(ciphertext)
            return {"ciphertext": ct_b64.decode()}
        else:
            self.exit = True
            return {"error": "Please request OTP"}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
"""
When you connect, the 'challenge' function will be called on your JSON
input.
"""
listener.start_server(port=13370)
```
Ta phân tích bài: Đầu tiên là hàm `xor_flag_with_otp():`
```python
def xor_flag_with_otp():
    flag_ord = [ord(c) for c in FLAG]
    otp = os.urandom(20)

    xored = bytearray([a ^ b for a, b in zip(flag_ord, otp)])

    # make sure our OTP doesnt leak any bytes from the flag
    for c, p in zip(xored, flag_ord):
        assert c != p

    return xored
```
Hàm này thực hiện XOR flag của ta với một one time pad key là một chuỗi random 20 bytes = 160 bits. Đặc biệt là ta có điều kiện 
`assert c != p` để đảm bảo rằng, không có bytes nào bị trùng lại với flag ban đầu sau khi XOR. 


Tiếp theo là phần tương tác với server, ta được quyền request tới server để lấy kết quả XOR. Nếu như có bytes bị trùng lại thì nó sẽ cho ta biết. Còn nếu không nó sẽ trả về kết quả sau khi XOR với key.

Vấn đề là mỗi lần ta request tới thì key bị thay đổi, nên kể cả khi có request 2 lần trở lên đi nữa thì cũng không có tác dụng gì trong việc khôi phục lại key. 

V thì h ta phải làm sao...... Sau một hồi suy nghĩ thì mình thấy không còn cách nào khác ngoài cách Bruteforce :V


