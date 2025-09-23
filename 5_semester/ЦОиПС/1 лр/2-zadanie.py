import numpy as np
import matplotlib.pyplot as plt

N = 20
# -----------------------------
# 1. Единичный скачок
# -----------------------------
u = np.ones(N)

# -----------------------------
# 2. КИХ-фильтр: y(n) = (x(n) + x(n-1)) / 2
# -----------------------------
y_kih = np.zeros(N)
for n in range(N):
    if n == 0:
        y_kih[n] = u[n] / 2
    else:
        y_kih[n] = (u[n] + u[n-1]) / 2

# Теоретическая переходная характеристика КИХ
y_kih_theory = np.ones(N)
y_kih_theory[0] = 0.5

# -----------------------------
# 3. БИХ-фильтр: y(n) = x(n) + a y(n-1)
# -----------------------------
a = 0.7
y_bih = np.zeros(N)
for n in range(N):
    if n == 0:
        y_bih[n] = u[n]
    else:
        y_bih[n] = u[n] + a * y_bih[n-1]

# Теоретическая переходная характеристика БИХ
# Формула: y(n) = (1 - a^(n+1)) / (1 - a)
y_bih_theory = np.array([(1 - a**(n+1))/(1-a) for n in range(N)])

# -----------------------------
# 4. Графики
# -----------------------------

plt.figure(figsize=(12,6))

plt.subplot(2,2,1)
plt.stem(y_kih)
plt.title("КИХ-фильтр (переходная характеристика)")
plt.xlabel("n")
plt.ylabel("y(n)")

plt.subplot(2,2,2)
plt.stem(y_kih_theory, linefmt='r-', markerfmt='ro', basefmt=' ')
plt.title("КИХ-фильтр (теоретическая переходная)")
plt.xlabel("n")
plt.ylabel("y(n)")

plt.subplot(2,2,3)
plt.stem(y_bih)
plt.title(f"БИХ-фильтр (переходная характеристика, a={a})")
plt.xlabel("n")
plt.ylabel("y(n)")

plt.subplot(2,2,4)
plt.stem(y_bih_theory, linefmt='r-', markerfmt='ro', basefmt=' ')
plt.title("БИХ-фильтр (теоретическая переходная)")
plt.xlabel("n")
plt.ylabel("y(n)")

'''
plt.stem(u)
plt.title(f"Единичный скачок длиной 20 отсчётов")
plt.xlabel("n")
plt.ylabel("y(n)")
'''
plt.tight_layout()
plt.show()
