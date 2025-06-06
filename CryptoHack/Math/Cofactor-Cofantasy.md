# Cofactor Cofantasy
Source code của bài
```python
from utils import listener
from Crypto.Random.random import randint

FLAG = b"crypto{???????????????????????????????????}"

# N is a product of safe primes
N = 56135841374488684373258694423292882709478511628224823806418810596720294684253418942704418179091997825551647866062286502441190115027708222460662070779175994701788428003909010382045613207284532791741873673703066633119446610400693458529100429608337219231960657953091738271259191554117313396642763210860060639141073846574854063639566514714132858435468712515314075072939175199679898398182825994936320483610198366472677612791756619011108922142762239138617449089169337289850195216113264566855267751924532728815955224322883877527042705441652709430700299472818705784229370198468215837020914928178388248878021890768324401897370624585349884198333555859109919450686780542004499282760223378846810870449633398616669951505955844529109916358388422428604135236531474213891506793466625402941248015834590154103947822771207939622459156386080305634677080506350249632630514863938445888806223951124355094468682539815309458151531117637927820629042605402188751144912274644498695897277
phi = 56135841374488684373258694423292882709478511628224823806413974550086974518248002462797814062141189227167574137989180030483816863197632033192968896065500768938801786598807509315219962138010136188406833851300860971268861927441791178122071599752664078796430411769850033154303492519678490546174370674967628006608839214466433919286766123091889446305984360469651656535210598491300297553925477655348454404698555949086705347702081589881912691966015661120478477658546912972227759596328813124229023736041312940514530600515818452405627696302497023443025538858283667214796256764291946208723335591637425256171690058543567732003198060253836008672492455078544449442472712365127628629283773126365094146350156810594082935996208856669620333251443999075757034938614748482073575647862178964169142739719302502938881912008485968506720505975584527371889195388169228947911184166286132699532715673539451471005969465570624431658644322366653686517908000327238974943675848531974674382848
g = 986762276114520220801525811758560961667498483061127810099097

def get_bit(i):
    if FLAG[i // 8] & (1 << (i % 8)):
        return pow(g, randint(2, phi - 1), N)
    else:
        return randint(1, N - 1)

class Challenge():
    def __init__(self):
        self.before_input = "Is this real life, or is it just overly complicated math?\n"

    def challenge(self, your_input):
        if "option" not in your_input:
            return {"error": "Your input should contain an option"}
        if your_input["option"] == "get_bit":
            if "i" not in your_input:
                return {"error": "Open your eyes, look up to the skies and see: there's no bit index here."}
            i = int(your_input["i"])
            if not 0 <= i < 8*len(FLAG):
                return {"error": "This bit is a little high or a little low."}
            return {"bit": hex(get_bit(i))}
        else:
            return {"error": "I'm just a poor boy from a poor fantasy, I don't know how to do that."}


import builtins; builtins.Challenge = Challenge # hack to enable challenge to be run locally, see https://cryptohack.org/faq/#listener
listener.start_server(port=13398)
```
Phân tích: Ta có $\displaystyle N$ là tích của các safe primes. 

![image](https://github.com/user-attachments/assets/e506d48e-1137-4540-95a8-bf6d49c1ec8a)

Và ta cũng được cho biết $\displaystyle \phi ( n)$. Vấn đề là $\displaystyle g$. Lúc đầu mình cũng không thực sự rõ $\displaystyle g$ nó là cái gì. Mình thử check xem $\displaystyle g$ có phải là phần tử sinh của nhóm $\displaystyle \mathbb{Z} /N\mathbb{Z}$ không thì không đúng. 

![image](https://github.com/user-attachments/assets/24143900-d273-4851-949c-8f9e40d818f4)

Tạm thời thì mình bỏ qua $g$ và đi tới phần sau để xem hàm `get_bit` nó đang làm gì. 

Nó sẽ check điều kiện: `FLAG[i//8] & (1 << (i % 8))`. Tức là với mỗi $i$ nó sẽ lấy byte thứ $i/8$ của flag. Sau đó nó sẽ lấy `1 << (i % 8)`. Đây chính là phép dịch bit, tức là nó sẽ tạo ra một số có bit 1 tại vị trí `i % 8`. Kết quả này sau đó lại được AND với byte trước đó. Như vậy điều kiện này sẽ kiểm tra xem bit ở vị trí `FLAG[i//8]` có đúng là 1 hay không do tính chất của phép AND chỉ trả về True nếu như cả hai đều True. Nếu như True thì nó sẽ trả về $\displaystyle g^{x}\bmod N$ trong đó $\displaystyle x\in [ 2,\phi ( N) -1]$.

Ngược lại nếu như bit ở vị trí này bằng 0 thì nó sẽ sinh ra một số ngẫu nhiên trong khoảng từ $\displaystyle [ 1,N-1]$

Tiếp theo là tới class Challenge()

Ta được chọn duy nhất 1 option là `"get_bit"`. Gửi lên server vị trí của bit mà ta muốn đoán và nó sẽ trả về kết quả của hàm `get_bit`. 

Vậy là ta đã nắm được bài này cần phải làm gì, đó là phân biệt được khi nào server trả về kết quả bit 1 hoặc kết quả bit 0. 

![image](https://github.com/user-attachments/assets/bd3cccfc-b450-4ad1-b011-5270a33237e4)

Bài toán như sau: Cho một phần tử $\displaystyle a$. Làm sao để xác định được $\displaystyle a$ có thuộc nhóm con được sinh ra bởi $\displaystyle \langle g\rangle $ hay không. Do $\displaystyle ( g,N) =1$ nên $\displaystyle g$ có cấp hữu hạn tức là tồn tại $\displaystyle r$ sao cho $\displaystyle g^{r} \equiv 1\bmod N$. Khi đó ta biết $\displaystyle r|\phi ( N)$. Mình có thử tính thì thấy $\displaystyle g^{\frac{\phi ( N)}{2^{15}}} \equiv 1\bmod N$ nên là $\displaystyle |g|=2s$ trong đó $\displaystyle s$ là tích của các số nguyên tố còn lại

Bây giờ nếu server trả lại $\displaystyle h=g^{r}$ thì nếu ta lấy $\displaystyle h^{2s} \equiv 1(\bmod N)$. Nhưng vấn đề là mình có thử lấy $\displaystyle x$ random và mũ $\displaystyle 2s$ lên thì nó cũng ra bằng 1 khá nhiều....

Ngược lại nếu như $\displaystyle x$ là một phần tử ngẫu nhiên thì xác suất để nó thuộc một nhóm có cấp là $\displaystyle s$ sẽ là $\displaystyle \frac{s}{\phi ( N)} =\frac{1}{2^{16}}$ còn đối với $\displaystyle h=g^{r}$ ta sẽ tính $\displaystyle h^{s} =g^{2\times \frac{r}{2} \times s} =g^{2s\times \frac{r}{2}} =1$ sẽ có xác suất xảy ra là $\displaystyle \frac{1}{2}$.


Vậy cách xác định bit sẽ là tính $\displaystyle h^{s}$ trong khoảng 8 lần, nếu như nó trả về kết quả là 1 thì ta xác định được rằng bit tại vị trí đó bằng 1. Còn nếu như bằng 0 thì coi như là rơi vào trường hợp còn lại. 

```python
from pwn import *
from sage.all import *
from Crypto.Util.number import *
from Crypto.Random.random import randint
import json
r = remote("socket.cryptohack.org", 13398)
N = 56135841374488684373258694423292882709478511628224823806418810596720294684253418942704418179091997825551647866062286502441190115027708222460662070779175994701788428003909010382045613207284532791741873673703066633119446610400693458529100429608337219231960657953091738271259191554117313396642763210860060639141073846574854063639566514714132858435468712515314075072939175199679898398182825994936320483610198366472677612791756619011108922142762239138617449089169337289850195216113264566855267751924532728815955224322883877527042705441652709430700299472818705784229370198468215837020914928178388248878021890768324401897370624585349884198333555859109919450686780542004499282760223378846810870449633398616669951505955844529109916358388422428604135236531474213891506793466625402941248015834590154103947822771207939622459156386080305634677080506350249632630514863938445888806223951124355094468682539815309458151531117637927820629042605402188751144912274644498695897277
phi = 56135841374488684373258694423292882709478511628224823806413974550086974518248002462797814062141189227167574137989180030483816863197632033192968896065500768938801786598807509315219962138010136188406833851300860971268861927441791178122071599752664078796430411769850033154303492519678490546174370674967628006608839214466433919286766123091889446305984360469651656535210598491300297553925477655348454404698555949086705347702081589881912691966015661120478477658546912972227759596328813124229023736041312940514530600515818452405627696302497023443025538858283667214796256764291946208723335591637425256171690058543567732003198060253836008672492455078544449442472712365127628629283773126365094146350156810594082935996208856669620333251443999075757034938614748482073575647862178964169142739719302502938881912008485968506720505975584527371889195388169228947911184166286132699532715673539451471005969465570624431658644322366653686517908000327238974943675848531974674382848
g = 986762276114520220801525811758560961667498483061127810099097
r.recvline()

def get_bit(i):
    for _ in range(8):
        r.sendline(json.dumps({"option":"get_bit","i":str(i)}).encode())
        response = json.loads(r.recvline())
        h = int(response["bit"],16)
        e = phi//(2**16)
        if pow(h,e,N)==1:
            return 1
    return 0
flag = []
len = 43
for i in range(len*8):
    b = get_bit(i)
    flag.append(str(b))
    print(flag)
f = ''.join(flag)
real_flag = long_to_bytes(int(f[::-1],2))[::-1]
print(real_flag)
```
Những gì học được: Đối với các bài tập như này thì việc quan trọng nhất cần làm đó là xác định được cấp của $g$. 
