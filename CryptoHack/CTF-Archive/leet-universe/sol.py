R.<x> = PolynomialRing(ZZ)
def gcd_zmod(f,g):
  while g:
    f, g = g, f % g
  return f

f = x**13+37
g = (x+42)**13+42
r = abs(ZZ(f.resultant(g)))
print(r)
R = Zmod(r)
ff = f.change_ring(R)
gg = g.change_ring(R)
f_quo = gcd_zmod(ff,gg)
x = ZZ(-f_quo[0]/f_quo[1])
print(x)
print(gcd(f(x),g(x)))
 
