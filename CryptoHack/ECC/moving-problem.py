from sage.all import *
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')
# shared_secret =
# iv = 
# ciphertext = 
# print(decrypt_flag(shared_secret, iv, ciphertext))
p = 1331169830894825846283645180581
a = -35
b = 98
E = EllipticCurve(GF(p), [a,b])
G = E.gens()[0]
print(factor(G.order()))
# có một factor lớn là 1153763334005213
q1=2 * 7 * 271 * 23687
q2=1153763334005213
P1 = E(1110072782478160369250829345256, 800079550745409318906383650948)
P2 = E(1290982289093010194550717223760, 762857612860564354370535420319)
print(f"cấp của P1 là {factor(P1.order())}")
print(f"cấp của P2 Là {factor(P2.order())}")
# cấp của P1 và G như nhau nên ta sẽ giải DLP tìm n_a
# Đầu tiên là giải tìm DLP với các ước nhỏ
G1=q2*G
P1_1=q2*P1
alice_secret_small=discrete_log(P1_1, G1, operation='+')
print(alice_secret_small)
# sau đó ta giải với ước lớn
G2=q1*G
P1_2=q1*P1
# tính bậc nhúng
n=G.order()
k=1
while True:
    if (p**k-1) % q2 == 0 :
        print(f"bậc nhúng là {k}")
        break
    else:
        k+=1
print(k)
# Mở rộng trường
Epk=E.base_extend(GF(p**k))
P1pk=Epk(P1_2) # na*G
G2pk=Epk(G2) # G
# Từ thuật toán ta cần chọn ra một điểm T thuộc Epk và thỏa mãn cặp Weil của nó với G2 không bằng 1
while True:
    T=Epk.random_point()
    T=int(T.order()//q2)*T
    if T.order()==q2 and G2pk.weil_pairing(T,q2)!=1:
        break
assert T.order()==P1pk.order()==G2pk.order()

# u=T.weil_pairing(G2pk,T.order())
# v=T.weil_pairing(P1pk,T.order())
# alice_secret_big=v.log(u)
# print(alice_secret_big)
# alice_secret=crt([alice_secret_small,alice_secret_big],[q1,q2])
# print(alice_secret) # 29618469991922269
s=29618469991922269
shared_secret=(P2*s).x()
iv='eac58c26203c04f68d63dc2c58d79aca'
encrypted_flag='bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d'
print(decrypt_flag(shared_secret,iv,encrypted_flag))
