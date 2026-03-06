import numpy as np
import matplotlib.pyplot as plt

# Параметры генератора
r = 12
M = 12345
A0 = 1
N = 500
K = 10
m = 5

# Генерация БСВ (little-frog)
modulus = 2 ** r
z = []
A = A0

if m > 1:
    M_step = pow(M, m, modulus)
else:
    M_step = M

for i in range(N):
    A = (A * M_step) % modulus
    z.append(A / modulus)

z = np.array(z)

x_vals = np.array([-87.8, -86.6, -15.7, 4.1, 22.1, 71.4, 98.8])
p_vals = np.array([0.044, 0.017, 0.140, 0.162, 0.153, 0.246, 0.238])

print(f"Сумма вероятностей: {np.sum(p_vals)}")

cum_p = np.cumsum(p_vals)

generated_x = []

for r_val in z:
    idx = np.searchsorted(cum_p, r_val)
    generated_x.append(x_vals[idx])

generated_x = np.array(generated_x)

M_theor = np.sum(x_vals * p_vals)
D_theor = np.sum(p_vals * (x_vals - M_theor)**2)

M_emp = np.mean(generated_x)
D_emp = np.var(generated_x, ddof=1)  # ddof=1 для несмещенной оценки

print(f"\n--- Результаты ---")
print(f"M теор: {M_theor:.4f} | M эмп: {M_emp:.4f}")
print(f"D теор: {D_theor:.4f} | D эмп: {D_emp:.4f}")


plt.figure(figsize=(10, 6))

plt.bar(x_vals, p_vals, width=5, alpha=0.5, label='Теоретические вероятности', color='blue', align='center')

unique, counts = np.unique(generated_x, return_counts=True)
emp_probs = counts / N
plt.bar(unique, emp_probs, width=5, alpha=0.5, label='Эмпирические вероятности', color='orange', align='center')

plt.xlabel('Значения СВ (x)')
plt.ylabel('Вероятность')
plt.title('Сравнение теоретического и эмпирического распределений')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

print("\nПервые 30 значений выборки:")
print(generated_x[:30])