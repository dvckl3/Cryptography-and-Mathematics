from Crypto.PublicKey import RSA

f = open('bruce_rsa.pem', 'r')
pubkey = RSA.import_key(f.read())

print(pubkey.n)
