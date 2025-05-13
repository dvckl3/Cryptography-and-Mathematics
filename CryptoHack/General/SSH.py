# pip install rsa
import base64
with open('brute_rsa.pub', 'rb') as public_file:
    key_data = public_file.read()
key_str = key_data.decode().strip()
key_parts = key_str.split()
key_b64 = key_parts[1]
raw = base64.b64decode(key_b64)
def read_string(data):
    l = int.from_bytes(data[0:4], "big")
    return data[4:4+l], data[4+l:]
def read_mpint(data):
    l = int.from_bytes(data[0:4], "big")
    int_bytes = data[4:4+l]
    return int.from_bytes(int_bytes, "big"), data[4+l:]
_, rest = read_string(raw)
e, rest = read_mpint(rest)
n, rest = read_mpint(rest)
print(e)
print(n)

