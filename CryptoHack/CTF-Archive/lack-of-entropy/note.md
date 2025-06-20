# Lack of Entropy
## Description
Mystiz's computer is lack of entropy. He needs to reuse randomness to generate the primes for RSA...

Challenge contributed by Mystiz

## Ý tưởng giải

Bài này sử dụng mã hóa RSA với quá trình sinh khóa $p,q$ trông có vẻ khá sú. $p$ được sinh hoàn toàn ngẫu nhiên bởi hàm `random.getrandbits(256)`

Sau đó $q$ chính là $p$ nhưng được biểu diễn trong hệ cơ số 3. 

```
n = 12189464288007059657184858632825479990912616419482466046617619319388181010121359489739982536798361842485210016303524715395474637570227926791570158634811951043352789232959763417380155972853016696908995809240738171081946517881643416715486249
e = 65537
c = 10093874086170276546167955043813453195412484673031739173390677430603113063707524122014352886564777373620029541666833142412009063988439640569778321681605225404251519582850624600712844557011512775502356036366115295154408488005375252950048742
```

Mình thử gen một số $n$ khác rồi ném lên FactorDB thì nó cũng không phân tích được (chịu). 

Bài này có một lỗi đó là $q$ được sinh ra có bit length lớn hơn $p$ khá nhiều. Nói đơn giản hơn thì số chữ số của $q$ có vẻ khá là nhiều.

Hmm ở bài này thì mình có thể sử dụng binary search được. Ta nên dùng binary search khi nào? Khi miền tìm kiếm là đơn điệu, tức là tăng hoặc giảm. Ở đây thì khi $p$ tăng thì tích $p\times q$ cũng sẽ tăng theo. Cho nên ta có thể kiểm tra điều kiện và tìm ra $p$ được.

