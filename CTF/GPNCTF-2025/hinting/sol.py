(venv) % cat 2perplexity.py
from Crypto.Util.number import long_to_bytes

# Daten aus output.txt
n = int("e56637432228a996b56329097e6b1a7c062bf3e09c2719d85781e519c850754710aef5b7f731c5d92ce11d7869358461334ca6f6150d84d031f12baf181fe7c7bfcffffe17c24f86fac1f92305820089327c594d8a58ff5e9fe7730c109c79d8131b162d04065f87c546ee8a3af802846c9463c6709f7bcb1bfb4339b94ffba6ec42d71a1ff6df7d97b518af9c9099332a485550ba22620beca9e38dd8b52a56bdba1fe0f84333edcef496fe581b786a5b9636d5e40e9a8137da235c0759a7806e606a6022330fd8e9c221c68f2de2f1da439db9b978c6a369adf706bc8224939671c4208af41205e210538002caa5f840fbc6eef4c44a020600b9d483010c0b", 16)
e = 0x10001
c = int("3e9a5e091ce7dde703a444e593e8ca295f5b6a3820d9506558bbaa24cb3e30e64db30e95bbe3f1df41a155f45c98ca90d19bf6d839bfd6a06bc0be8a81abf5db274584c8be677df134330f7f85efe617da58c46ad0c11b61f388befddc4f1fbaadb2f0f8c07d66c4770b0fb96343ebf29a6c17fde7c9336d28125798a1ca151e5c454168bea485083f4122ad8eda64178801f0539df5a3a32e4b7d21491ef25b00b4f726caf92199e3afa2e93062ef9c6a31395aa54b07c017539cfcadfb205cc004a38aec39c24b162cd96f2d3a324bccb8795a2eb3235000c0fb5c146166ee0cf499fae73af6b098cbf5c2ebe7d1e8c76b3d9d91022377decf70903ac55298", 16)
V = (1, 4, 3, 1, 0, 5, 2, 5, 1, 4, 1, 4, 2, 2, 1, 6, 0, 1, 5, 2, 6, 0, 4, 3, 1, 2, 0, 4, 5, 6, 0, 3, 2, 1, 4, 5, 2, 3, 0, 0, 6, 5, 1, 4, 4, 2, 4, 0, 4, 2, 0, 2, 4, 0, 0, 4, 5, 2, 3, 3, 0, 4, 3, 2, 1, 4, 0, 2, 0, 5, 0, 1, 6, 3, 0, 2, 1, 6, 2, 3, 2, 1, 1, 0, 3, 6, 5, 5, 0, 1, 6, 5, 0, 5, 4, 1, 4, 1, 1, 3, 3, 2, 5, 4, 1, 1, 6, 4, 6, 5, 3, 0, 1, 1, 2, 4, 1, 0, 4, 5, 6, 6, 1, 5, 6, 2, 5, 3, 3, 4, 0, 0, 6, 5, 5, 1, 3, 1, 5, 4, 2, 6, 2, 0, 5, 1, 2, 3, 0, 1, 0, 3, 1, 5, 2, 4, 6, 5, 5, 1, 1, 2, 0, 1, 6, 4, 4, 4, 3, 5, 6, 3, 2, 2, 0, 5, 5, 2, 4, 3, 2, 3, 3, 5, 0, 5, 3, 3, 2, 4, 3, 2, 2, 5, 2, 1, 2, 6, 1, 3, 0, 6, 5, 5, 1, 3, 5, 3, 5, 5, 1, 3, 2, 6, 3, 2, 3, 2, 1, 4, 5, 6, 4, 6, 3, 2, 2, 5, 4, 1, 1, 3, 0, 3, 3, 4, 4, 0, 5, 2, 6, 6, 0, 3, 4, 5, 3, 5, 0, 6, 4, 5, 3, 2, 2, 2, 6, 1, 0, 1, 2, 2, 5, 3, 4, 4, 0, 6, 1, 6, 5, 4, 4, 6, 4, 0, 6, 6, 4, 4, 3, 3, 2, 0, 6, 4, 1, 4, 1, 1, 0, 5, 3, 0, 0, 5, 1, 3, 1, 2, 0, 5, 0, 3, 2, 3, 1, 2, 1, 4, 0, 3, 4, 2, 2, 2, 6, 4, 2, 4, 5, 4, 3, 4, 1, 3, 1, 1, 4, 6, 2, 0, 1, 2, 3, 6, 6, 0, 3, 0, 3, 5, 2, 5, 2, 6, 6, 4, 2, 2, 0, 4, 5, 2, 5, 0, 6, 0, 0, 6, 5, 6, 4, 1, 1, 0, 0)

# Konfiguration
d = len(V)
powers = [7**i for i in range(d)]

# Backtracking-Algorithmus
stack = [(d-1, 0, 0)]  # (Stellenindex, aktuelles p, aktuelles q)
found = False

while stack:
    i, p_high, q_high = stack.pop()
    current_power = powers[i]

    for p_i in range(7):
        q_i = (V[i] - p_i) % 7
        p_curr = p_high + p_i * current_power
        q_curr = q_high + q_i * current_power

        if i == 0:
            if p_curr * q_curr == n:
                p, q = p_curr, q_curr
                found = True
                break
        else:
            max_rest = powers[i] - 1
            min_prod = p_curr * q_curr
            max_prod = (p_curr + max_rest) * (q_curr + max_rest)

            if min_prod <= n <= max_prod:
                stack.append((i-1, p_curr, q_curr))
    if found:
        break

if not found:
    print("Keine Lösung gefunden!")
    exit(1)

# RSA-Entschlüsselung
phi = (p-1) * (q-1)
d_key = pow(e, -1, phi)
m = pow(c, d_key, n)

# Byte-Konvertierung und Umkehrung
flag_bytes = long_to_bytes(m)
flag_str = flag_bytes.decode('utf-8', errors='ignore')
correct_flag = flag_str #HF#[::-1]  # WICHTIG: String umkehren

print(f"Korrekte Flag: {correct_flag}")

(venv) % python3 2perplexity.py
Korrekte Flag: GPNCTF{w0W_fac7Oring_W1TH_hintS_iS_Fun}
