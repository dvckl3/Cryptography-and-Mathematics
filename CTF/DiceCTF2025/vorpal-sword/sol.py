from pwn import *
from Crypto.Util.number import *
import re
DEATH_CAUSES = [
	'a fever',
	'dysentery',
	'measles',
	'cholera',
	'typhoid',
	'exhaustion',
	'a snakebite',
	'a broken leg',
	'a broken arm',
	'drowning',
]
death_msgs = [f'you die of {cause}.' for cause in DEATH_CAUSES]
death_vals = [int.from_bytes(msg.encode(), 'big') for msg in death_msgs]
HOST="dicec.tf"
PORT=31001
io=remote(HOST,PORT)

def extract_page(data):
    match = re.search(rb"turn to page (\d+)\.", data)
    if match:
        page_str = match.group(1).decode()
        if page_str.isdigit():
            return int(page_str)
    return None

def round(server):
    server.recvuntil(b"n: ")
    n=int(server.recvline().strip())
    server.recvuntil(b"e: ")
    e=int(server.recvline().strip())
    server.recvuntil(b"x0: ")
    x0=int(server.recvline().strip())
    server.recvuntil(b"x1: ")
    x1=int(server.recvline().strip())
    scale=2
    v = (x0 + pow(scale, e, n) * x1) * pow(1 + pow(scale, e, n), -1, n) % n
    server.sendlineafter("v: ",str(v).encode())
    server.recvuntil(b"c0: ")
    c0=int(server.recvline().strip())
    server.recvuntil(b"c1: ")
    c1=int(server.recvline().strip())
    comp=c0+scale*c1 # comp=m0+scale*m1
    # truong hop m0 la die
    page=None
    for d in death_vals:
        cand=((comp-d) * (pow(scale,-1,n))) % n 
        pos=long_to_bytes(cand)
        print("debug case 1: ",pos)
        page=extract_page(pos)
        if page is not None:
            break
    # truong hop m1 la die
    if page is None:
        for d in death_vals:
            cand=(comp-scale*d)%n
            pos=long_to_bytes(cand)
            print("debug case 2: ",pos)
            page=extract_page(pos)
            if page is not None:
                break
    if page is not None:
        print(f"tìm được valid pages: {page}")
        server.sendlineafter(b"turn to page: ",str(page).encode())
    else:
        print("bug cmnr")

    
for _ in range(64):
    round(io)

io.interactive()
