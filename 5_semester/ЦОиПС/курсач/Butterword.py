import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры
N = 16               # номер в списке
Fs = N * 1e3         # частота дискретизации, Гц
f1 = 0.3 * N * 1e3   # 4.8 кГц
# f2 = 0.6 * N * 1e3  # 9.6 кГц — недопустимо (> Fs/2)
f2_eff = (Fs - 0.6 * N * 1e3)  # эффективная частота: 6.4 кГц

# Переводим в угловые частоты (рад/с)
w1 = 2 * np.pi * f1
w2 = 2 * np.pi * f2_eff

print(f"Полоса заграждения: {f1/1e3:.1f} – {f2_eff/1e3:.1f} кГц")
print(f"Угловые частоты: w1 = {w1:.0f} рад/с, w2 = {w2:.0f} рад/с")

# Синтез аналогового заграждающего фильтра Баттерворта 4-го порядка
n = 4
b_analog, a_analog = signal.butter(n, [w1, w2], btype='bandstop', analog=True, output='ba')

# Найдём полюсы передаточной функции H(s) = b(s)/a(s)
poles = np.roots(a_analog)
zeros = np.roots(b_analog)

# Вывод полюсов
print("\nПолюсы аналогового фильтра Баттерворта:")
for i, p in enumerate(poles):
    print(f"  p{i+1} = {p:.3e}")

# Построение графика
plt.figure(figsize=(6, 6))
plt.axhline(0, color='k', linewidth=0.5)
plt.axvline(0, color='k', linewidth=0.5)
plt.scatter(poles.real, poles.imag, marker='x', s=100, label='Полюсы', color='red')
if len(zeros) > 0:
    plt.scatter(zeros.real, zeros.imag, marker='o', s=80, label='Нули', color='blue')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.title('Полюсы (и нули) аналогового заграждающего фильтра Баттерворта\n4-го порядка')
plt.xlabel('Re(s)')
plt.ylabel('Im(s)')
plt.legend()
plt.axis('equal')
plt.tight_layout()
plt.show()