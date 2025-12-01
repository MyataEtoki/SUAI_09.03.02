import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры (из п.1)
N = 16
Fs = N * 1e3          # 16 кГц
f1 = 0.3 * N * 1e3    # 4.8 кГц
f2_eff = Fs - 0.6 * N * 1e3  # 6.4 кГц

# Угловые частоты для аналогового прототипа (предыскажение НЕ нужно — делает bilinear)
w1 = 2 * np.pi * f1
w2 = 2 * np.pi * f2_eff

# 1. Синтез аналогового заграждающего фильтра Баттерворта 4-го порядка
n = 4
b_analog, a_analog = signal.butter(n, [w1, w2], btype='bandstop', analog=True)

print("Коэффициенты аналогового фильтра H(s):")
print("b_analog =", b_analog)
print("a_analog =", a_analog)

# 2. Применение билинейного преобразования
# Период дискретизации
T = 1.0 / Fs

# Функция signal.bilinear выполняет: s = (2/T) * (1 - z^{-1}) / (1 + z^{-1})
b_digital, a_digital = signal.bilinear(b_analog, a_analog, fs=Fs)

print("\nКоэффициенты цифрового фильтра H(z):")
print("b (числитель) =", b_digital)
print("a (знаменатель) =", a_digital)

# Нормировка (часто a[0] = 1)
b_digital = b_digital / a_digital[0]
a_digital = a_digital / a_digital[0]

print("\nНормированные коэффициенты (a[0] = 1):")
for i, (bi, ai) in enumerate(zip(b_digital, a_digital)):
    print(f"  b[{i}] = {bi:.6e},   a[{i}] = {ai:.6e}")