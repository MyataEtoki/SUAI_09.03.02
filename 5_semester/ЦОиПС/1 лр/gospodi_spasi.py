import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Единичный импульс
# -----------------------------
N = 20
delta = np.zeros(N)
delta[0] = 1  # импульс в нуле

# -----------------------------
# 2. КИХ-фильтр
# y(n) = (x(n) + x(n-1)) / 2
# -----------------------------
h_kih = np.zeros(N)
for n in range(N):
    if n == 0:
        h_kih[n] = delta[n] / 2
    else:
        h_kih[n] = (delta[n] + delta[n-1]) / 2

# Теоретическая импульсная характеристика КИХ
h_kih_theory = np.zeros(N)
h_kih_theory[0] = 0.5
h_kih_theory[1] = 0.5

# -----------------------------
# 3. БИХ-фильтр
# y(n) = x(n) + a y(n-1)
# -----------------------------
a = 0.7  # коэффициент
h_bih = np.zeros(N)
for n in range(N):
    if n == 0:
        h_bih[n] = delta[n]
    else:
        h_bih[n] = delta[n] + a * h_bih[n-1]

# Теоретическая импульсная характеристика БИХ
h_bih_theory = np.array([a**n for n in range(N)])
h_bih_theory[0] = 1

# -----------------------------
# 4. Графики
# -----------------------------
plt.figure(figsize=(12,6))

plt.subplot(2,2,1)
plt.stem(h_kih)
plt.title("КИХ-фильтр (импульсная характеристика)")
plt.xlabel("n")
plt.ylabel("h(n)")

plt.subplot(2,2,2)
plt.stem(h_kih_theory, linefmt='r-', markerfmt='ro', basefmt=' ')
plt.title("КИХ-фильтр (теоретическая характеристика)")
plt.xlabel("n")
plt.ylabel("h(n)")

plt.subplot(2,2,3)
plt.stem(h_bih)
plt.title(f"БИХ-фильтр (импульсная характеристика, a={a})")
plt.xlabel("n")
plt.ylabel("h(n)")

plt.subplot(2,2,4)
plt.stem(h_bih_theory, linefmt='r-', markerfmt='ro', basefmt=' ')
plt.title("БИХ-фильтр (теоретическая характеристика)")
plt.xlabel("n")
plt.ylabel("h(n)")

plt.tight_layout()
plt.show()

