from Crypto.Util.number import bytes_to_long, long_to_bytes
import itertools
from tqdm import tqdm
from string import printable

is_printable = [i in printable.encode() for i in range(256)]

round_constants = [3, 141, 59, 26, 53, 58, 97, 93, 23, 84, 62, 64, 33, 83, 27, 9, 50, 28, 84, 197, 169, 39, 93, 75]

p1 = b'Good luck on solving the chal!'

R = Zmod(2^256 - 1)

nrounds = len(round_constants)

coefs = [R(0)] * nrounds + [R(bytes_to_long(p1))] + [R(0)]
for i in range(nrounds):
	coefs[-1] += 1
	coefs[i] -= 1
	for j in range(len(coefs)): coefs[j] *= R(2)^(256 - round_constants[i])

const_coef = 1239507101017535755241021503192414295708425140346924975455738409598007145464 - coefs[-2]
key_coef = coefs[-1]
g = gcd(int(key_coef), 2^256 - 1)

M2 = Integer((2^256 - 1) / g)
R2 = Zmod(M2)

key_coef = R2(Integer(key_coef) / g)

MASK = 2^256 - 1

round_constants_reversed = round_constants[::-1]

for s in tqdm(itertools.product(range(2), repeat=nrounds), total=int(2^nrounds)):
	rhs = Integer(const_coef - sum(coef for i, coef in zip(s, coefs) if i))
	if rhs % g != 0: continue
	k = int(R2(rhs // g) / key_coef)
	s_rev = s[::-1]
	for _ in range(g):
		block = 1239507101017535755241021503192414295708425140346924975455738409598007145464
		for rcon, ss in zip(round_constants_reversed, s_rev):
			block = ((block << rcon) & MASK) | (block >> (256 - rcon))
			block = block - k
			if (block < 0) != ss: break
			block &= MASK
		else:
			block = 96887724055188441187495947602065815010851561208340821350405558115730186415087
			for rcon in round_constants_reversed:
				block = ((block << rcon) & MASK) | (block >> (256 - rcon))
				block = block - k
				block &= MASK
			else:
				flag = long_to_bytes(block)
				print(flag)
		k += M2
