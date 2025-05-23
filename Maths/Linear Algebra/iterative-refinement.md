# Tinh chỉnh lặp
Tinh chỉnh lặp là một phương pháp giúp cải thiện nghiệm xấp xỉ $\displaystyle \hat{x}$ cho hệ phương trình tuyến tính $\displaystyle Ax=b$, trong đó $\displaystyle A$ là một ma trận không suy biến $\displaystyle n\times n$. Thuật toán phát biểu đơn giản như sau:

1. Tính $\displaystyle r=b-A\hat{x}$

2. Giải tìm $\displaystyle Ad=r$.

3. Update giá trị $\displaystyle \hat{x}\leftarrow \hat{x} +d$.

4. Lặp lại bước 1 nếu cần thiết. 
