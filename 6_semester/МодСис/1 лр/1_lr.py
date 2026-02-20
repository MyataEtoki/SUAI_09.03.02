import numpy as np
import matplotlib.pyplot as plt

# Параметры генератора
r = 12
M = 12345
A0 = 1
N = 1000
K = 10
m = 5

# Генерация БСВ (little-frog)
modulus = 2 ** r
z = []
A = A0

if m > 1:
    M_step = pow(M, m, modulus)  # Быстрое возведение в степень по модулю
else:
    M_step = M

for i in range(N):
    A = (A * M_step) % modulus
    z.append(A / modulus)

z = np.array(z)

# Мат. ожидание и дисперсия
M_emp = np.mean(z)
D_emp = np.var(z)
M_theory = 0.5
D_theory = 1/12

print(f"M_emp = {M_emp:.6f}, M_theory = {M_theory:.6f}")
print(f"D_emp = {D_emp:.6f}, D_theory = {D_theory:.6f}")

# Гистограмма
plt.figure(figsize=(8, 5))
plt.hist(z, bins=K, edgecolor='black', alpha=0.7)
plt.axhline(N/K, color='red', linestyle='--', label='Ожидание')
plt.title("Гистограмма распределения БСВ")
plt.xlabel("Интервал")
plt.ylabel("Частота")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("histogram.png", dpi=300, bbox_inches='tight')
plt.show()

# Корреляция
def calc_R(z, s):
    T = len(z)
    sum_prod = sum(z[i] * z[i+s] for i in range(T - s))
    return (12 / (T - s)) * sum_prod - 3

s_values = [2, 5, 10]
T_range = range(100, N + 1, 100)

print(f"\nКорреляция при T={2**(r-2)}:")
for s in s_values:
    R = calc_R(z, s)
    print(f"s={s}: R = {R:.6f}")

# График корреляции
plt.figure(figsize=(8, 5))
for s in s_values:
    R_vals = [calc_R(z[:T], s) for T in T_range]
    plt.plot(T_range, R_vals, marker='o', label=f's={s}')

plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.title("Зависимость R̂s от T")
plt.xlabel("Объём выборки T")
plt.ylabel("Коэффициент корреляции")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("correlation.png", dpi=300, bbox_inches='tight')
plt.show()