# Leet Universe

## Description

The flag is hidden somewhere in the 1337th universe.

Challenge contributed by maple3142

Connect at archive.cryptohack.org 3721

## Ý tưởng

Đọc sơ qua source code thì mình thấy bài chỉ đơn giản là tìm $x$ sao cho $\displaystyle \gcd\left( x^{13} +37,( x+42)^{13} +42\right)$ khác 1 là được. 

Nhìn thì có vẻ đơn giản nhưng thực sự không đơn giản tí nào...

Mình thử tới $2^{16}$ thì không có số nào cho ra ước chung khác 1 cả =)))

```python
from math import gcd

for i in range(2**16):
    g = gcd(i**13+37,(i+42)**13+42)
    if g!=1:
        print(i)
```

Review lại thì ta có một cách để lấy ước chung của hai đa thức đó chính là sử dụng Polynomial Resultant. 

Cho hai đa thức hệ số nguyên $\displaystyle f( x) ,g( x)$. Giả sử tồn tại một số nguyên $\displaystyle n$ sao cho $\displaystyle \gcd( f( n) ,g( n)) =d\neq 1$ thì khi đó xét $\displaystyle p$ là một ước nguyên tố của $\displaystyle n$. Lúc này nếu ta xem $\displaystyle f( x) ,g( x)$ như là một đa thức trên trường $\displaystyle \mathbb{Z}_{p}[ x]$ thì chúng sẽ có một nghiệm chung là $\displaystyle x=n$. 

Hai đa thức có nghiệm chung thì kết thức (resultant) của chúng sẽ bằng 0 và trong trường hợp xét trên trường mod $\displaystyle p$ thì kết thức của chúng sẽ chia hết cho $\displaystyle p$. 


```python
R.<x> = PolynomialRing(ZZ)
f = x^13 + 37
g = (x + 42)^13 + 42

res = f.resultant(g)
```

Nhưng ở bài này thì kết thức khá lớn và factor cũng hơi lâu :v. Vậy thì phải làm sao. Ta không cần phân tích mà có thể chuyển luôn về trên trường mod theo resultant cũng được rồi sau đó lấy gcd của chúng.





