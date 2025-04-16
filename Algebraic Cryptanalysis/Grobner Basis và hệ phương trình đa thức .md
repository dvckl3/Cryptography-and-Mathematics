---
title: 'Grobner Basis và hệ phương trình đa thức '

---


[TOC]

# Giới thiệu 
Grobner Basis là một công cụ thường được sử dụng trong Algebraic Cryptanalysis. Trong bài viết dưới đây, mình sẽ trình bày vắn tắt các khái niệm, thuật toán cũng như cơ sở toán học xoay quanh Grobner Basis. 


# Cấu trúc đại số

## Vành đa thức
Trước tiên ta cần nhắc lại định nghĩa về vành

### Vành 
Vành là một tập hợp $\displaystyle R$ khác rỗng, được trang bị hai phép toán cộng $\displaystyle +:( a,b)\rightarrow a+b$ và nhân $\displaystyle \times :( a,b)\rightarrow a\times b$ thỏa mãn đồng thời các điều kiện sau:

1. $\displaystyle ( R,+)$ là một nhóm giao hoán 
2. Phép nhân trên $\displaystyle R$ có tính kết hợp 
3. Phép nhân có tính chất phân phối đối với phép cộng, cụ thể với $\displaystyle x,y,z\in R$ thì 
\begin{gather*}
x( y+z) =xy+xz\ \\
( y+z) x=yx+zx
\end{gather*}


Kể từ bây giờ ta sẽ kí hiệu $\displaystyle ab$ để chỉ phép nhân giữa hai số $\displaystyle a$ và $\displaystyle b$ cho thuận tiện. Một vành được gọi là vành có đơn vị nếu như tồn tại một phần tử $\displaystyle 1\in R$ sao cho $\displaystyle 1a=a1=a$. Tiếp theo, một vành được gọi là vành giao hoán nếu như với mọi $\displaystyle a,b\in R$ thì $\displaystyle ab=ba$. 

Sau đây ta sẽ giả thiết các vành đa thức mà ta xét tới đều là vành giao hoán có đơn vị . 

Cho $\displaystyle A$ là một vành và $\displaystyle x$ là biến số. Ta gọi một biểu thức $\displaystyle f$ có dạng $\displaystyle c_{0} +c_{1} x+...+c_{r} x^{r}$ với $\displaystyle c_{0} ,...,c_{r} \in A$ là một đa thức với biến $\displaystyle x$ với các hệ số trong $\displaystyle A$. Nếu $\displaystyle c_{r} \neq 0$ thì $\displaystyle c_{r}$ được gọi là hệ số cao nhất của đa thức $\displaystyle f$ và $\displaystyle r$ là bậc của $\displaystyle f$, kí hiệu $\displaystyle \deg f=r$. Đa thức có hệ số cao nhất bằng 1 được gọi là đa thức monic hay đa thức chuẩn. Nếu $\displaystyle f=0$ thì ta quy ước $\displaystyle \deg f=-\infty$. Như vậy, vành đa thức $\displaystyle A[ x]$ của biến $\displaystyle x$ trên $\displaystyle A$ là tập hợp tất cả các đa thức có hệ số trong $\displaystyle A$. 

Tiếp theo ta nhắc lại không chứng minh bổ đề sau: 

**Bổ đề.** Cho $\displaystyle g\in A[ x]$ là đa thức chuẩn. Ta có thể viết mọi đa thức $\displaystyle f\in A[ x]$ về dưới dạng $\displaystyle f=gh+v$ trong đó $\displaystyle \deg v< \deg g$. 

### Vành đa thức nhiều biến 

Vành đa thức $\displaystyle n$ biến trên $\displaystyle A$ được định nghĩa quy nạp như sau: 
\begin{equation*}
A[ x_{1} ,...,x_{n}] =A[ x_{1} ,...,x_{n-1}][ x_{n}]
\end{equation*}

tức là $\displaystyle A[ x_{1} ,...,x_{n}]$ là vành đa thức của biến $\displaystyle x_{n}$ trên vành $\displaystyle A[ x_{1} ,...,x_{n-1}]$. Để thuận tiện, ta sẽ kí hiệu $\displaystyle A[ X] =A[ x_{1} ,...,x_{n}]$ kể từ bây giờ. 

Các phần tử của $\displaystyle A[ X]$ được gọi là đa thức $\displaystyle n$ biến. Ta viết một đa thức $\displaystyle n$ biến $\displaystyle f$ dưới dạng 
\begin{equation*}
f( X) =\sum _{r_{1} +...+r_{n} \leqslant r} c_{r_{1} ,...,r_{n}} x_{1}^{r_{1}} ...x_{n}^{r_{n}}
\end{equation*}

với $\displaystyle r$ là một số tự nhiên nào đó và $\displaystyle c_{r_{1} ,...,r_{n}} \in A$. Các phần tử $\displaystyle c_{r_{1} ,..,r_{n}}$ được gọi là hệ số, $\displaystyle c_{0,...,0}$ được gọi là hệ số tự do của $\displaystyle f$. Các biểu thức $\displaystyle x_{1}^{r_{1}} ...x_{n}^{r_{n}}$ được gọi là đơn thức và bậc của đơn thức này được tính toán là $\displaystyle r_{1} +...+r_{n}$. Như vậy, bậc của một đa thức đa biến $\displaystyle f\neq 0$ là bậc lớn nhất của các đơn thức với hệ số khác không. Nếu như $\displaystyle \deg f=1$ thì ta gọi $\displaystyle f$ là đa thức tuyến tính.

Vành $\displaystyle A$ được gọi là miền nguyên nếu như $\displaystyle A$ không có ước của không, tức là $\displaystyle cd\neq 0$ với mọi $\displaystyle c,d\neq 0$ trong $\displaystyle A$. Tính chất sau là một trong những tính chất cơ bản của các vành đa thức $\displaystyle n$ biến trên miền nguyên $\displaystyle A$.

**Bổ đề.** Nếu $\displaystyle A$ là miền nguyên thì $\displaystyle \deg fg=\deg f+\deg g$ với mọi $\displaystyle f,g\in A[ X]$.

Trong vành $\displaystyle A$, một phần tử $\displaystyle a\in A$ được gọi là khả nghịch nếu như tồn tại $\displaystyle b\in A$ thỏa mãn $\displaystyle ab=1$. Tiếp theo ta xét một bổ đề sau về các phần tử khả nghịch trong miền $\displaystyle A[ X]$

**Bổ đề.** Nếu $\displaystyle A$ là một miền nguyên thì $\displaystyle A[ X]$ cũng vậy và các phần tử khả nghịch của $\displaystyle A[ X]$ là các phần tử khả nghịch của $\displaystyle A$. 

*Chứng minh.* Cho $\displaystyle f,g$ là các đa thức khác 0 trong $\displaystyle A[ X]$. Do $\displaystyle \deg f,\deg g\geqslant 0$ nên $\displaystyle \deg fg\geqslant 0$ và do đó $\displaystyle fg\neq 0$ nên $\displaystyle A[ X]$ là một miền nguyên. Nếu như $\displaystyle fg=1$ thì suy ra $\displaystyle \deg f=\deg g=0$ và do đó $\displaystyle f,g\in A$. Vì vậy, $\displaystyle f,g$ cũng là các phần tử khả nghịch của $\displaystyle A$. 


Xét $\displaystyle k$ là một trường tùy ý, theo định nghĩa của $\displaystyle k$ thì $\displaystyle k$ cũng là một miền nguyên, cho nên các tính chất của $\displaystyle k[ X]$ cũng có các tính chất nêu trên. 

Ta xét với mỗi $\displaystyle a=( \alpha _{1} ,...,\alpha _{n}) \in k^{n}$ thì ta có giá trị 
\begin{equation*}
f( a) =\sum _{r_{1} +...+r_{n} \leqslant m} c_{r_{1} ,...,r_{n}} \alpha _{1}^{r_{1}} ...\alpha _{n}^{r_{n}}
\end{equation*}

Ta có thể coi $\displaystyle f$ là một hàm số từ $\displaystyle k^{n}$ vào $\displaystyle k$. Điểm $\displaystyle a$ được gọi là nghiệm của $\displaystyle f$ nếu như $\displaystyle f( a) =0$. Các kết quả sau đây sẽ giúp ta nắm một số tính chất của đa thức trên các trường vô hạn

**Tính chất 1.** Cho $\displaystyle k$ là trường vô hạn, nếu như với mọi $\displaystyle a\in k^{n}$ ta có $\displaystyle f( a) =0$ thì $\displaystyle f=0$

**Tính chất 2.** Cho $\displaystyle k$ là trường vô hạn. Nếu $\displaystyle f,g$ là hai đa thức trong $\displaystyle k[ X]$ thỏa mãn điều kiện $\displaystyle f( a) =g( a)$ với mọi $\displaystyle a\in k^{n}$ thì $\displaystyle f=g$

### Hệ phương trình đa thức

Ta gọi tập nghiệm của hệ phương trình đa thức là tập đại số affine hay ngắn gọn hơn là tập đại số. Khái niệm tập đại số không phụ thuộc vào việc chọn hệ tọa độ. Ví dụ giả sử tọa độ cũ là $\displaystyle ( \alpha _{1} ,...,\alpha _{n})$ được xác định dựa theo tọa độ mới $\displaystyle ( \beta _{1} ,...,\beta _{n})$ bởi công thức 
\begin{gather*}
\alpha _{1} =c_{10} +c_{11} \beta _{1} +...+c_{1n} \beta _{n}\\
...\\
\alpha _{n} =c_{n0} +c_{n1} \beta _{n} +...+c_{nn} \beta _{n}
\end{gather*}

với $\displaystyle c_{ij} \in k$ ($\displaystyle k$ ở đây là trường đại số). Nếu $\displaystyle V$ là tập nghiệm của hệ đa thức $\displaystyle S$ thì các điểm của $\displaystyle V$ trong tọa độ mới là nghiệm của hệ đa thức 
\begin{equation*}
f( c_{10} +c_{11} x_{1} +...+c_{1n} x_{n} ,...,c_{n0} +c_{n1} y_{1} +...+c_{nn} y_{n}) ,f\in S
\end{equation*}

Ta có thể dùng phép biến đổi tạo độ để đưa hệ đa thức $\displaystyle S$ về một dạng đơn giản hơn. 

Ví dụ : Cho $\displaystyle V\neq \emptyset$ là tập nghiệm của một hệ đa thức độc lập tuyến tính $\displaystyle f_{1} ,...,f_{d} ,1\leqslant d\leqslant n$. Ta có thể chọn $\displaystyle c_{ij}$ sao cho 
\begin{equation*}
f_{i}( c_{10} +c_{11} x_{1} +...+c_{1n} x_{n} ,c_{n0} +...+c_{nn} y_{n}) =x_{i} ,1\leqslant i\leqslant d
\end{equation*}

Trong hệ tọa độ mới ta có $\displaystyle V=\{( 0,0,...,\alpha _{d+1} ,...,\alpha _{n}) |\alpha _{d+1} ,...,\alpha _{n} \in k\}$. Vì vậy $\displaystyle V$ có thể được coi như một không gian vector $\displaystyle k^{n-d}$. Các tập $\displaystyle V$ như vậy được gọi là đa tạp tuyến tính. 


Với mỗi đa thức $\displaystyle f$ ta kí hiệu $\displaystyle Z( f)$ là tập nghiệm của đa thức này. Nếu $\displaystyle \deg f\leqslant 0$ thì hoặc là $\displaystyle Z( f)$ chính là $\displaystyle k^{n}$, trong trường hợp $\displaystyle f=0$ hoặc là $\displaystyle Z( f) =\emptyset$ , trong trường hợp $\displaystyle c\neq 0$. Với $\displaystyle \deg f >0$ ta gọi $\displaystyle Z( f)$ là siêu mặt. $\displaystyle Z( f)$ chỉ có thể được tính trong 1 số trường hợp cụ thể. 

Ví dụ: $\displaystyle f=x^{2} -y$ trong $\displaystyle k[ x,y]$ thì $\displaystyle Z( f) =\left\{\left( \alpha ,\alpha ^{2}\right) ,\alpha \in k\right\}$

Như vậy, từ định nghĩa của $\displaystyle f$ và hệ phương trình đa thức $\displaystyle S$ thì ta có tập nghiệm của hệ phương trình đa thức $\displaystyle S$ sẽ là $\displaystyle Z( S) =\bigcap _{f\in S} Z( f)$. Vì vậy, mọi tập đại số khác rỗng đều là giao của các siêu mặt. 

Nhắc lại: Các tập $\displaystyle Z( f)$ trong $\displaystyle k$ chỉ rơi vào 3 trường hợp là rỗng, $\displaystyle k$ hoặc hữu hạn. 




Sau đây ta sẽ nghiên cứu một số tính chất của tập đại số. 
 
**Tính chất 1.** Cho $\displaystyle S_{1}$ và $\displaystyle S_{2}$ là hai hệ đa thức trong $\displaystyle k[ X]$. Khi đó nếu như $\displaystyle S_{1} \supseteq S_{2}$ thì $\displaystyle Z( S_{1}) \subseteq Z( S_{2})$

**Tính chất 2.** Cho $\displaystyle S_{1}$ và $\displaystyle S_{2}$ là hai hệ đa thức trong $\displaystyle k[ X]$. Ta có 

\begin{equation*}
Z( S_{1}) \cup Z( S_{2}) =Z( S)
\end{equation*}trong đó $\displaystyle S=\{fg|f\in S_{1} ,g\in S_{2}\}$

Chứng minh. 

Đầu tiên ta thấy rằng mọi nghiệm của $\displaystyle S_{1} ,S_{2}$ cũng là nghiệm của $\displaystyle S$ cho nên $\displaystyle Z( S_{1}) \cup Z( S_{2}) \subseteq Z( S)$. Ngược lại gọi $\displaystyle a$ là một nghiệm của $\displaystyle S$. Nếu $\displaystyle a$ không là nghiệm của $\displaystyle S_{1}$ thì tồn tại $\displaystyle f\in S_{1}$ sao cho $\displaystyle f( a) \neq 0$ và do $\displaystyle a\in S$ cho nên $\displaystyle f( a) g( a) =0$ hay $\displaystyle g( a) =0$. Do đó $\displaystyle a\in S_{2}$. Vậy $\displaystyle Z( S) \subseteq Z( S_{1}) \cup Z( S_{2})$ và ta có điều phải chứng minh. 

**Tính chất 3.** Cho $\displaystyle \{S_{i}\}$ là một họ các hệ đa thức trong $\displaystyle k[ X]$. Ta có 

\begin{equation*}
\bigcap Z( S_{i}) =Z\left(\bigcup S_{i}\right)
\end{equation*}


Ta kí hiệu $\displaystyle k[ Y] =k[ y_{1} ,...,y_{m}]$ để mô tả các hàm đa thức trên $\displaystyle k^{m}$ và $\displaystyle k[ X,Y] =k[ x_{1} ,...,x_{n} ,y_{1} ,...,y_{m}]$. Ta có một tính chất sau.

**Tính chất 4.** Cho $\displaystyle S\subseteq k[ X]$ và $\displaystyle T\subseteq k[ Y]$ là hai hệ đa thức. Nếu ta coi $\displaystyle S\cup T$ như một hệ đa thức trong $\displaystyle k[ X,Y]$ thì : 

\begin{equation*}
Z( S) \times Z( T) =Z( S\cup T)
\end{equation*}

### Topo Zariski


Phần này nhìn chung khá là trừu tượng và cần một tí kiến thức về topo nên mọi người tạm tham khảo tại đây: https://math.uchicago.edu/~may/REU2019/REUPapers/Michel.pdf


## Iđêan 

Như vậy, ta đã biết tập đại số là tập nghiệm của một hệ phương trình đa thức. Sau đây ta sẽ tìm hiểu một cấu trúc đại số đặc biệt để nghiên cứu về hai hệ đa thức tương đương. 



Cho $\displaystyle A$ là một vành. Tập $\displaystyle I$ trong $\displaystyle A$ được gọi là Iđêan nếu như $\displaystyle 0\in I$ và $\displaystyle I$ thỏa mãn các điều kiện sau: 

i/ $\displaystyle f+g\in I$ với mọi $\displaystyle f,g\in I$

ii/ $\displaystyle hf\in I$ với $\displaystyle h\in A$ và $\displaystyle f\in I$.

Như vậy : Idean đóng với phép cộng và phép nhân với một phần tử của vành. $\displaystyle I$ cũng là một nhóm Abel với phép cộng. Nếu như $\displaystyle 1\in I$ thì $\displaystyle I=A$ từ tính chất ii/

Khái niệm Idean khá giống với khái niệm chia hết trong số học sơ cấp mà ta thường học. Tập các phần tử chia hết cho phần tử $\displaystyle f$ thuộc $\displaystyle A$ là tập 
\begin{equation*}
( f) :=\{hf\ |\ h\in A\}
\end{equation*}

Tập này cũng là một Idean và ta gọi là một Idean chính sinh bởi $\displaystyle f$. Tổng quát : với mọi hệ phần tử $\displaystyle S$ thuộc $\displaystyle A$ thì ta gọi tập các phần tử chia hết cho $\displaystyle S$ sẽ là 
\begin{equation*}
( S) :=\{h_{1} f_{1} +...+h_{r} f_{r} \ |\ h_{1} ,...,h_{r} \in A,f_{1} ,...,f_{r} \in S,r\geqslant 1\}
\end{equation*}

$\displaystyle ( S)$ là một Idean và là Idean nhỏ nhất sinh bởi $\displaystyle S$. Tiếp theo ta định nghĩa thế nào là tổng và tích của các Idean. 

Cho $\displaystyle I,J$ là hai Idean tùy ý trong $\displaystyle A$. Idean sinh bởi các phần tử thuộc $\displaystyle I\cup J$ được gọi là Idean tổng của $\displaystyle I$ và $\displaystyle J$, kí hiệu $\displaystyle I+J$. Tương tự với $\displaystyle IJ$ là Idean tích của $\displaystyle I$ và $\displaystyle J$. Viết dưới dạng ngôn ngữ tập hợp sẽ là 
\begin{gather*}
I+J=\{f+g\ |\ f\in I,g\in J\}\\
IJ=\{f_{1} g_{1} +...+f_{r} g_{r} \ |\ f_{i} \in I,g_{i} \in J,1\leqslant i\leqslant r\}
\end{gather*}

Ngoài ra ta có $\displaystyle IJ\subseteq I\cap J$ nhưng rõ ràng hai Idean này là khác nhau. Để minh họa ta xét một vài ví dụ sau: 

Ví dụ: Cho $\displaystyle I=\left( x,y^{2}\right) ,J=( y)$ là hai Idean của vành đa thức $\displaystyle k[ x,y]$. Ta có $\displaystyle I+J=\left( x,y^{2} ,y\right) =( x,y)$. Còn $\displaystyle IJ=\left( xy,y^{3}\right)$. Với $\displaystyle I\cap J$ ta hiểu rằng tập này cho ta một Iđêan sinh bởi các phần tử thuộc vào cả hai Iđêan $\displaystyle I$ và $\displaystyle J$. Theo định nghĩa của Iđêan thì $\displaystyle I=\left( x,y^{2}\right)$ cho nên Iđêan sinh bởi $\displaystyle I$ sẽ có dạng 
\begin{gather*}
( I) =\left\{ax+by^{2} \ |\ a,b\in k[ x,y]\right\}\\
( J) =\{hy\ |\ h\in k[ x,y]\}
\end{gather*}

Rõ ràng $\displaystyle I\cap J=\left( xy,y^{2}\right)$.

Và lúc này ta có nhận xét rằng $\displaystyle IJ\subseteq I\cap J$

Các phép cộng và nhận Iđêan thỏa mãn các quy tắc sau
\begin{gather*}
I+J=J+I\\
IJ=JI\\
( I+J) +K=I+( J+K)\\
( IJ) K=I( JK)\\
( I+J) K=IK+JK
\end{gather*}

với mọi $\displaystyle I,J,K$ là Iđêan trong $\displaystyle A$. 

Ví dụ: Trong $\displaystyle \mathbb{Z}$ thì ta có $\displaystyle ( n) \cap ( m) =lcm( n,m)$. Vì $\displaystyle ( n)$ bao gồm các bội của $\displaystyle n$ còn $\displaystyle ( m)$ gồm các bội của $\displaystyle m$. Nếu lấy giao giữa chúng thì sẽ được một tập gồm các phần tử vừa là bội của $\displaystyle n$ vừa là bội của $\displaystyle m$. Phần tử sinh của tập này sẽ là bội chung nhỏ nhất giữa $\displaystyle n$ và $\displaystyle m$. 

Với mọi Iđêan $\displaystyle I$ và mọi số nguyên $\displaystyle r\geqslant 0$. Ta định nghĩa Iđêan mũ như sau 
\begin{equation*}
I^{r} =I...I\left(\text{r lần}\right)
\end{equation*}

và quy ước $\displaystyle I^{0} :=A$. 

Ví dụ: $\displaystyle ( x,y)^{r} =\left( x^{r} ,x^{r-1} y,...,y^{r}\right)$. 

Với mỗi $\displaystyle S\subset A$ ta kí hiệu $\displaystyle I:S$ để chỉ tập hợp sau\begin{equation*}
I:S:=\{f\in A|\ fg\in I,g\in S\}
\end{equation*}

Nếu $\displaystyle S$ chỉ gồm một phần tử $\displaystyle g$ thì ta viết gọn $\displaystyle I:g$ (nhìn khá loằng ngoằng :v). Lưu ý tập hợp $\displaystyle I:S$ cũng là một Iđêan 
Ví dụ: $\displaystyle I=\left( xy,y^{3}\right)$ thì 
\begin{gather*}
I:x=\{f\in A|\ fx\in I\}\\
\Longrightarrow I:x=( y)
\end{gather*}

Và tương tự 

\begin{gather*}
I:y=\{f\in A|\ fy\in I\}\\
\Longrightarrow I:x=\left( x,y^{2}\right)
\end{gather*}


Tiếp theo ta có một bổ đề quan trọng nói về mối liên hệ giữa tập đại số và Iđêan. 

**Bổ đề 1.** Cho $\displaystyle S$ là một hệ các đa thức trong $\displaystyle k[ X]$ và $\displaystyle I=( S)$. Ta có 
\begin{equation*}
Z( I) =Z( S)
\end{equation*}
Chứng minh. 

Do $\displaystyle S\subseteq I$ nên $\displaystyle Z( I) \subseteq Z( S)$. Ngược lại cho $\displaystyle a\in Z( S)$ bất kì. Thì xét $\displaystyle f\in I$ thì $\displaystyle f=h_{1} f_{1} +...+h_{r} f_{r} ,f_{1} ,..,f_{r} \in S$ và do $\displaystyle f_{1}( a) =...=f_{r}( a)$ cho nên $\displaystyle f( a) =0$ và dẫn tới $\displaystyle a\in Z( I)$. Vậy $\displaystyle Z( S) \subseteq Z( I)$.

**Bổ đề 2.** Cho $\displaystyle I$ và $\displaystyle J$ là hai Iđêan tùy ý trong $\displaystyle k[ X]$. Ta có 

i/ $\displaystyle Z( I) \cup Z( J) =Z( I\cap J) =Z( IJ)$.

ii/ $\displaystyle Z( I) \cap Z( J) =Z( I+J)$

Chứng minh. 

Để chứng minh các tính chất trên thì ta sử dụng lại một tính chất về tập đại số đã chứng minh trước đó. Cụ thể với $\displaystyle S_{1} ,S_{2}$ là hai hệ đa thức trong $\displaystyle k[ X]$ thì 

\begin{equation*}
Z( S_{1}) \cup Z( S_{2}) =Z( S)
\end{equation*}

trong đó $\displaystyle S=\{fg\ |\ f\in S_{1} ,g\in S_{2}\}$. Như vậy ta có $\displaystyle Z( I) \cup Z( J) =Z( IJ)$. Mặt khác ta có $\displaystyle Z( I\cap J)$ là tập nghiệm của hệ đa thức gồm các phần tử thuộc Iđêan sinh ra bởi các phần tử cùng thuộc $\displaystyle I$ và $\displaystyle J$. Như vậy 
\begin{equation*}
Z( I) \cup Z( J) \subseteq Z( I\cap J) \subseteq Z( IJ)
\end{equation*}

Cho nên ta có điều phải chứng minh.

Tiếp theo ta xét $\displaystyle Z( I) \cap Z( J) =Z( I+J)$. Do Iđêan $\displaystyle I+J$ sinh bởi $\displaystyle I\cup J$ và $\displaystyle Z( I) \cap Z( J) =Z( I\cup J)$ cho nên ta có điều phải chứng minh. 
### Vành căn và hữu hạn sinh 


Cho $\displaystyle I$ là một Iđêan tùy ý trong vành $\displaystyle A$. Ta gọi tập tất cả các phần tử thuộc $\displaystyle A$ có một lũy thừa $\displaystyle f^{r} \in I$ là căn của $\displaystyle I$, kí hiệu là $\displaystyle \sqrt{I}$.

Tập trên cũng là một Iđêan. Cụ thể ta có thể chứng minh như sau: Cho $\displaystyle f,g\in \sqrt{I}$ thì $\displaystyle f^{r} ,g^{s} \in I$. Khi đó 
\begin{equation*}
( f+g)^{r+s} =\sum _{i=1}^{r+s}\binom{r+s}{i} f^{r+s-i} g^{i}
\end{equation*}

Rõ ràng là $\displaystyle r+s-i\geqslant r$ hoặc $\displaystyle i\geqslant s$. Vì vậy $\displaystyle f^{r+s-i} g^{i}$ chia hết cho $\displaystyle f^{r}$ hoặc $\displaystyle g^{s}$ với mọi $\displaystyle i=1,...,r+s$. Từ đây suy ra $\displaystyle ( f+g)^{r+s} \in I$ và do đó $\displaystyle f+g\in \sqrt{I}$. Tương tự ta có $\displaystyle hf\in \sqrt{I}$ vì $\displaystyle ( hf)^{r} =h^{r} f^{r} \in I$. 

Ta luôn có $\displaystyle I\subseteq \sqrt{I} =\sqrt{\sqrt{I}}$ và dấu bằng xảy ra thì ta gọi $\displaystyle I$ là Iđêan căn. 



Cho $\displaystyle I$ là Iđêan thực sự của vành $\displaystyle A$ tức là $\displaystyle I\neq A$. Ta gọi $\displaystyle I$ là Iđêan cực đại nếu $\displaystyle I$ không nằm trong một Iđêan thực sự nào khác của $\displaystyle A$. Ta gọi $\displaystyle I$ là Iđêan cực đại nếu $\displaystyle I$ không nằm trong một Iđêan thực sự nào khác của 

**Bổ đề.** Iđêan $\displaystyle I_{a} =( x_{1} -a_{1} ,...,x_{n} -a_{n})$ là Iđêan cực đại trong $\displaystyle k[X]$. 


Chứng minh. Dùng liên tiếp thuật toán Euclide thì ta có thể viết mọi đa thức $\displaystyle f\in k[ X]$ dưới dạng 
\begin{equation*}
f=h_{1}( x_{1} -a_{1}) +...+h_{n}( x_{n} -a_{n}) +\alpha 
\end{equation*}
Với $\displaystyle \alpha \in k$. Nếu như $\displaystyle f\notin I_{a}$ thì $\displaystyle \alpha \neq 0$ và do đó $\displaystyle ( I_{a} ,f) =k[ X]$.



### Iđêan đơn thức


Như ta đã biết với $\displaystyle R$ là một vành và $\displaystyle x_{1} ,...,x_{n}( n\geqslant 1)$ là các biến thì các đơn thức là các biểu thức có dạng $\displaystyle x_{1}^{a_{1}} ...x_{n}^{a_{n}}$ trong đó $\displaystyle a_{i} \in \mathbb{N}$ được gọi là bộ số mũ của đơn thức. Sau đây là đi tìm hiểu một khái niệm mới gọi là Iđêan đơn thức.



Định nghĩa 1. Iđêan $\displaystyle I\in k[ X]$ là Iđêan đơn thức nếu có tập con $\displaystyle A\subset \mathbb{N}^{n}$ (có thể vô hạn) mà ở đó $\displaystyle I$ bao gồm tất cả các đa thức là tổng hữu hạn của dạng hình thứ $\displaystyle \sum _{a\in A} h_{a} x^{a}$ trong đó $\displaystyle h_{a} \in k[ X]$. Trong trường hợp này thì ta viết $\displaystyle I=\left( x^{a} ;a\in A\right)$, ở đây, để chọn gọn ta đã viết $\displaystyle x^{a} =x_{1}^{a_{1}} ...x_{n}^{a_{n}}$. 

"Từ" ở đây là thuật ngữ để chỉ các biểu thức có dạng $\displaystyle \alpha x_{1}^{a_{1}} ...x_{n}^{a_{n}}$ trong đó $\displaystyle \alpha$ được gọi là hệ số của từ. 





**Bổ đề 1.** Cho $\displaystyle I=\left( x^{a} ;a\in A\right)$ là Iđêan đơn thức. Đơn thức $\displaystyle x^{b} \in I$ khi và khi khi $\displaystyle x^{b}$ chia hết cho một đơn thức $\displaystyle x^{a}$ với $\displaystyle a\in A$ nào đó. 

Chứng minh. 

Nếu $\displaystyle x^{b}$ chia hết cho một đơn thức $\displaystyle x^{a}$ với $\displaystyle a\in A$ thì theo định nghĩa của Iđêan ta có $\displaystyle x^{b} \in I$. Ngược lại nếu $\displaystyle x^{b} \in I$ thì $\displaystyle x^{b} =\sum _{i=1}^{s} h_{i} x^{a( i)} ,$trong đó $\displaystyle h_{i} \in k[ X]$ và $\displaystyle a( i) \in A$. 

Ta có thể xem $\displaystyle h_{i}$ như tổng hữu hạn của các từ và khai triển vế phải của đẳng thức thì ta thấy mỗi từ của nó phải chia hết cho $\displaystyle x^{a( i)}$ nào đó. Sau khi giản ước, một trong số từ đó còn lại và phải bằng $\displaystyle x^{b}$. Vậy $\displaystyle x^{b}$ phải có tính chất của những từ đó, tức là chia hết cho $\displaystyle x^{a( i)}$ đó. 



**Bổ đề 2.** Cho $\displaystyle I$ là Iđêan đơn thức và $\displaystyle f\in k[ X]$. Các điều kiện sau là tương đương:

i/ $\displaystyle f\in I$
ii/ Mọi từ của $\displaystyle f$ thuộc $\displaystyle I$
iii/ $\displaystyle f$ là tổ hợp tuyến tính trên $\displaystyle k$ của các đơn thức thuộc $\displaystyle I$. 



## Grobner Basis

### Thứ tự từ

Trước khi bắt đầu ta cần nắm một số khái niệm cơ bản về thứ tự toàn phần.

Mọi người có thể tham khảo tại đây: https://vi.wikipedia.org/wiki/Th%E1%BB%A9_t%E1%BB%B1_to%C3%A0n_ph%E1%BA%A7n

Tiếp theo ta có một số định nghĩa sau: 


**Định nghĩa 1.** Thứ tự từ $\displaystyle \leqslant$ là một thứ tự toàn phần trên tập $\displaystyle M$ tất cả các đơn thức của vành $\displaystyle k[ X]$ thỏa mãn các tính chất sau: 

i/ Với mọi $\displaystyle m\in M,1\leqslant m$.

ii/ Nếu $\displaystyle m_{1} ,m_{2} ,m\in M$ mà $\displaystyle m_{1} \leqslant m_{2}$ thì $\displaystyle mm_{1} \leqslant mm_{2}$



**Định nghĩa 2.** Thứ tự từ điển là thứ tự $\displaystyle \leqslant _{lex}$ xác định như sau: $\displaystyle x_{1}^{a_{1}} ...x_{n}^{a_{n}} < _{lex} x_{1}^{b_{1}} ...x_{n}^{b_{n}}$ nếu như thành phần đầu tiên khác không kể từ bên trái của vector $\displaystyle ( a_{1} -b_{1} ,...,a_{n} -b_{n})$ là âm. 



**Định nghĩa 3.** Thứ tự từ điển phân bậc là thứ tự $\displaystyle \leqslant _{glex}$ xác định như sau: $\displaystyle x_{1}^{a_{1}} ...x_{n}^{a_{n}} < _{glex} x_{1}^{b_{1}} ...x_{n}^{b_{n}}$ nếu như $\displaystyle \deg\left( x^{a}\right) \leqslant \deg\left( x^{b}\right)$ và thành phần đầu tiên khác không kể từ bên trái của vector $\displaystyle ( a_{1} -b_{1} ,...,a_{n} -b_{n})$ là âm. 

**Định nghĩa 4.** Thứ tự từ điển ngược là thứ tự $\displaystyle \leqslant _{rlex}$ xác định như sau: $\displaystyle x_{1}^{a_{1}} ...x_{n}^{a_{n}} < _{rlex} x_{1}^{b_{1}} ...x_{n}^{b_{n}}$ nếu $\displaystyle \deg\left( x^{a}\right) \leqslant \deg\left( x^{b}\right)$ và thành phần khác không đầu tiên kể từ bên trái của vector $\displaystyle ( a_{1} -b_{1} ,...,a_{n} -b_{n})$ là dương 



(dấu như dấu bé và lớn như bth ta học vậy :v??? nhưng trừu tượng hơn và xét trên các cấu trúc đại số mở rộng hơn)



Thực chất, thứ tự từ điển ngược được định nghĩa như theo sơ đồ của thứ tự từ điển phân bậc chứ không phải của thứ tự từ điển.

Cho $\displaystyle \leqslant$ là một thứ tự từ và $\displaystyle f\in k[ X]$. Từ khởi đầu của $\displaystyle f$, kí hiệu là $\displaystyle in_{\leqslant }( f)$ , là từ lớn nhất của đa thức $\displaystyle f$ đối với thứ tự từ $\displaystyle \leqslant$.



Nếu $\displaystyle in_{\leqslant }( f) =\alpha x^{a}$ thì $\displaystyle lc_{\leqslant }( f) =\alpha$ được gọi là hệ số đầu và $\displaystyle lm_{\leqslant }( f) =x^{a}$ được gọi là đơn thức đầu của $\displaystyle f$ đối với thứ tự từ $\displaystyle \leqslant$. 



Nếu thứ tự từ $\displaystyle \leqslant$ đã được ngầm hiểu hoặc định nghĩa trước đó thì ta sẽ lược bỏ và chỉ viết $\displaystyle in( f) ,lm( f) ,lc( f)$ cho gọn. 

Từ khởi đầu còn gọi là từ đầu hay từ đầu tiên. 

Ví dụ: $\displaystyle f=x^{3} y^{2} z+5xyz-3x^{4} +7yz^{3} -2y^{6} +z^{4}$. 

i/ Viết theo thứ tự từ điển thì $\displaystyle f=-3x^{4} +x^{3} y^{2} z+5xyz-2y^{6} +7yz^{3} +z^{4}$ và $\displaystyle in( f) =-3x^{4} ,lc( f) =-3,lm( f) =x^{4}$

ii/ Viết theo thứ tự từ điển phân bậc $\displaystyle f=x^{3} y^{2} z-2y^{6} -3x^{4} +7yz^{3} +z^{4} +5xyz$

Một số tính chất cơ bản: Với $\displaystyle f,g\in k[ X]$ và $\displaystyle m\in M$ là tập tất cả các đơn thức của $\displaystyle k[ X]$

i/ $\displaystyle in( fg) =in( f) in( g)$

ii/ $\displaystyle in( mf) =min( f)$

iii/ $\displaystyle lm( f+g) \leqslant \max\{lm( f) ,lm( g)\}$. Dấu $\displaystyle <$ xảy ra khi và chỉ khi $\displaystyle in( f) =-in( g)$

### Iđêan khởi đầu và Grobner Basis

**Iđêan khởi đầu.** Cho $\displaystyle I$ là một Iđêan của $\displaystyle k[ X]$ và $\displaystyle \leqslant$ là một thứ tự từ, Iđêan khởi đầu của $\displaystyle I$, kí hiệu là $\displaystyle in_{\leqslant }( I)$ là Iđêan của $\displaystyle R=k[ X]$ sinh ra bởi các từ khởi đầu của các phần tử của $\displaystyle I$, nghĩa là 
\begin{equation*}
in_{\leqslant }( I) =\{in_{\leqslant }( f) \ |\ f\in I\}
\end{equation*}

Vấn đề đặt ra là làm thế nào để xác định được Iđêan khởi đầu $\displaystyle in( I)$ của một Iđêan $\displaystyle I$ cho trước. Cách tốt nhất là tìm một hệ sinh tối tiểu của nó. Tuy nhiên mọi Iđêan đơn thức đều có một tập sinh đơn thức và tập đó hữu hạn. Do đó ta có một khái niệm quan trọng sau đây: 

**Định nghĩa.** Cho $\displaystyle \leqslant$ là một thứ tự từ và $\displaystyle I$ là Iđêan của $\displaystyle R=k[ X]$. Tập hữu hạn các đa thức khác không $\displaystyle g_{1} ,...,g_{s} \in I$ được gọi là một cơ sở Grobner của $\displaystyle I$ đối với thứ tự từ $\displaystyle \leqslant$, nếu: 
\begin{equation*}
in_{\leqslant }( I) =( in_{\leqslant }( g_{1}) ,...,in_{\leqslant }( g_{s}))
\end{equation*}

Tập $\displaystyle g_{1} ,...,g_{s}$ được gọi là một cơ sở Grobner, nếu nó là cơ sở Grobner của Iđêan sinh bởi các phần tử này. 

Hoặc nói đơn giản như sau: Ta có một hệ phương trình đa thức, khi đó sẽ đi tìm Groebner Basis của hệ đó. Hệ mới tìm được sẽ giữ nguyên các biến ban đầu, tập nghiệm và được "sắp xếp" một cách hợp lí để dễ giải hơn


Sau đây là một số tính chất của Groebner Basis


**Mệnh đề.** Cho $\displaystyle I$ là một Iđêan tùy ý của $\displaystyle R$. Nếu $\displaystyle g_{1} ,...,g_{s} \in I$ là cơ sở Grobner của $\displaystyle I$ thì $\displaystyle g_{1} ,...,g_{s}$ cũng là một cơ sở của $\displaystyle I$. 




## Tài liệu tham khảo 

[1] Algebraic Cryptanalysis, Gregory V. Bard
[2] [Gröbner bases techniques in Cryptography](https://web.stevens.edu/algebraic/Files/SCPQ/SCPQ-2011-03-30-talk-Perret.pdf)
[3] Advanced Modern Algebra ,Third Edition, Part 1, Joseph J. Rotman 
[4] CƠ SỞ GROBNER VÀ GIẢI HỆ PHƯƠNG TRÌNH ĐA THỨC, Đỗ Ngọc Thủy
[5] https://jingnanshi.com/blog/groebner_basis.html#fn.3
[6] Ideals, Varieties, and Algorithms (4th ed.) [Cox, Little & O'Shea 2015-06-14]
[7][Groebner Basis Attack on Block Cipher](https://www.isec.tugraz.at/wp-content/uploads/teaching/mfc/GB_Attacks_Schofnegger.pdf)
