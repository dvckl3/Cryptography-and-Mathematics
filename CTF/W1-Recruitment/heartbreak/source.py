from Crypto.Util.number import getPrime, bytes_to_long
FLAG = "W1{???}"

FLAG_PART1, FLAG_PART2 = FLAG[:len(FLAG)//2], FLAG[len(FLAG)//2:]

f =  open("output.txt", "w")

def part1():
    p = getPrime(2048)
    q = getPrime(2048)
    e = 0x10001
    n = p * q
    d = pow(e, -1, (p-1)*(q-1))

    m = bytes_to_long(FLAG_PART1.encode())

    c = pow(m, e, n)

    f.write("ct = " + str(c))

    hints = [p, q, e, n, d]
    for _ in range(len(hints)):
        hints[_] = (hints[_] * getPrime(1024)) % n
        if hints[_] == 0: hints[_] = (hints[_] - 1) % n

    f.write("\nHints = " + str(hints) + "\n")


def part2():
    e = getPrime(10)
    p = getPrime(256)
    q = getPrime(256)
    n = p * q
    # print(e)
    m1 = bytes_to_long(FLAG_PART2.encode())
    m2 = m1 >> 8


    c1, c2 = pow(m1, e, n), pow(m2, e, n)
    f.write(f"n = {n}\nc1 = {c1}\nc2 = {c2}\n")

if __name__ == "__main__":
    part1()
    part2()
