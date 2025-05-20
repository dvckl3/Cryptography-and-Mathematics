from itertools import *
from base64 import b64decode
import string
from pwn import xor
from math import log
msg = "kOKO1fZJVp1Im90chpvtwdnCHwArCEEdJSt41fZJTLlaIMdCR+Ppj9ODA+PmBwZPslNBm/OqkzaGm92P3LEhwdfWs5QpSRWOfwOPm+WImvmIm9oBCUdoiXgDHkhrSQ8HAiDB0/AAADUAAR4aR0OpWhzCUE2m0vgb5FRwWir6Tj/Bw9xAR2sgiJtg0U4vSRKsZf6Gm/2qijbB1c6t00lkwdlgw04gSRWOfwGIm/2Imu+P3IkChpr1wdjLkZvaSaX+JStC0r1JTjAnC4kDhpvRlZvNF+b3iNryrbCDWivITniV00jUwE1ojVoZx04gSQKOfzeAm+UBweN80okJDkEmz5voGElnC6LcqvfBz3DSsTHB1c6P3JFolclCy6trSaLOqvjByFLITj/B0MGt004vwdNCy6FnCwiOfi+Pm/yImv2Vl4kDpIBoIhnOUFQviNvIqbAnC1fITXiMWhPJCgxogtNCy71nrfCOfzOIm/oBT7lbGMcGR0sgAAEMEwCD+IDUR7CDWirCTj/B12rECQAlAAECHkhnBIDVebCJfTAHADqA1IkJDsHzfJvLkZr4HU9PhlNMm/yImvWVm9+P3KFokloYwQAzAYDVaeTB2HDShznBzWzHR1Q6AAAGUEsvqtUBo7CR03DTgzHB12rOR+Ppj9ODA+PmBwZPrPGYm/OqkzaGm92P3LEhzZvOs4BnBaLP5OMAACBJRzGA1IkGhpvrkZvEGcH8xgBPp/giAf8ODHiG0kjV9k4vwdXLtpBnGQmsbeDBz/6qgTbB08CP3Kc9wX8ykZvWAEEXJStI1fZJCACu6YBOEcHyTMKDkqDUSQ+pZfnB1lLJACsAABhOE8HzctWDBMH9yAhPp3FaHPBJTblaIt1OBePij5vIGOPzBwZPqP8AATAAACyTWhLFR0KLS9WDG0kmRUECBzDBz3DTgTfB1WrECQAlAAA6BAA0iNre5PMiGf9JQrlbCscJR1Qhj9ODBMH91kEZBzDB2VLEALlbEsdAR3aLQZvABcH8+AhPp1NY1fZJTJtBm8qP3L1yweySC2h2WhQwoKaI5MkcTmG+3stZX0Z60IzBFUIiXlZY8aKD3vMU"
def hamming(string1:bytes,string2:bytes)->int:
    assert len(string1) == len(string2)
    d = 0 
    for (byte1,byte2) in zip(string1,string2):
        d += bin(byte1^byte2).count('1')
    return d
# test , source: cryptopal
# s1 = "this is a test".encode()
# s2 = "wokka wokka!!!".encode()
# dist = hamming(s1, s2)
# assert dist == 37
# có thể tăng khoảng bruteforce keysize lên tùy vào trường hợp
def guess_key_length(ciphertext):
    key_length=0
    min_dist=len(ciphertext)
    for keysize in range(2,40):
        blocks = [ciphertext[i:i+keysize] for i in range(0,len(ciphertext)-keysize+1,keysize)]
        pair_num=len(list(combinations(blocks,2)))
        average_dist=(sum(hamming(a,b) for a,b in combinations(blocks,2))/pair_num)/keysize
        if average_dist<min_dist:
            min_dist=average_dist
            key_length=keysize
    return key_length
key_size = guess_key_length(b64decode(msg))
print(key_size)
# https://en.wikipedia.org/wiki/Letter_frequency#Relative_frequencies_of_letters_in_the_English_language
# có nhiều phiên bản khác nhau của bảng này, nhưng nhìn chung cũng không chênh lệch nhau nhiều về xác suất
eng_frequencies = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.361, 'x': 0.150, 'y': 1.974,
    'z': 0.074, ' ': 18.3
}
def score_text(text:bytes)-> float:
    score = 0.0
    l=len(text)
    for letter, frequencies in eng_frequencies.items():
        frequency_actual=text.count(ord(letter))/l
        err = abs(frequencies-frequency_actual)
        score += err   
    return score # về hàm này thì nếu điểm trả về càng thấp thì chứng tỏ decrypted text của ta có khả năng cao là plaintext gốc
def single_key_xor(ciphertext):
    best_guess=(float('inf'),None)
    key=None
    for cand_key in range(256):
        full_key=bytes([cand_key])*len(ciphertext)
        plaintext=bytes([b1 ^ b2 for b1,b2 in zip(full_key,ciphertext)]) 
        score = score_text(plaintext)
        curr_guess=(score,plaintext)
        if curr_guess < best_guess:
            best_guess=curr_guess
            key=cand_key
    if best_guess[1] is None:
        exit("không giải được")
    return best_guess[0],bytes([key]),best_guess[1]
# test : https://cryptopals.com/sets/1/challenges/3
# ciphertext='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
# print(single_key_xor(bytes.fromhex(ciphertext))) 
def repeated_key_xor(ciphertext,keysize):
    blocks = [ciphertext[i:i+keysize] for i in range(0, len(ciphertext), keysize)]
    cracks = [bytes([block[i] for block in blocks if i < len(block)]) for i in range(keysize)]
    key = b""
    for block in cracks:
        key += single_key_xor(block)[1]
        print(key)
    return key
ciphertext = b64decode(msg)
key=repeated_key_xor(ciphertext,key_size)
print(xor(ciphertext,key))
