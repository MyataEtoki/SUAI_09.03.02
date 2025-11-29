import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ------------------------------
# Исходные данные
# ------------------------------
order = 8          # порядок фильтра
fs = 8000          # частота дискретизации
fc = 1900          # частота среза
wc = 2 * np.pi * fc  # аналоговая частота среза

# -------------------------------------------------
# 1. АНАЛОГОВЫЙ ФИЛЬТР БАТТЕРВОРТА (прототип)
# -------------------------------------------------
b_a, a_a = signal.butter(order, wc, btype='low', analog=True)

# -------------------------------------------------
# 2. БИЛИНЕЙНОЕ ПРЕОБРАЗОВАНИЕ → Н(z)
# -------------------------------------------------
bz, az = signal.bilinear(b_a, a_a, fs=fs)

# -------------------------------------------------
# 3. Диаграмма НУЛЕЙ и ПОЛЮСОВ
# -------------------------------------------------
zeros = np.roots(bz)
poles = np.roots(az)

plt.figure(figsize=(6, 6))
plt.axhline(0, color='black')
plt.axvline(0, color='black')

plt.scatter(np.real(zeros), np.imag(zeros), marker='o', label='Нули')
plt.scatter(np.real(poles), np.imag(poles), marker='x', label='Полюса')

# единичная окружность
phi = np.linspace(0, 2*np.pi, 400)
plt.plot(np.cos(phi), np.sin(phi), 'r--', linewidth=1)

plt.title("Диаграмма нулей и полюсов H(z)")
plt.xlabel("Re")
plt.ylabel("Im")
plt.legend()
plt.grid(True)
plt.axis('equal')

# -------------------------------------------------
# 4. АЧХ и ФЧХ
# -------------------------------------------------
w, h = signal.freqz(bz, az, worN=2048)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(w * fs / (2*np.pi), 20 * np.log10(abs(h)))
plt.title("АЧХ (модуль)")
plt.xlabel("Частота, Гц")
plt.ylabel("Амплитуда, дБ")
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(w * fs / (2*np.pi), np.unwrap(np.angle(h)))
plt.title("ФЧХ")
plt.xlabel("Частота, Гц")
plt.ylabel("Фаза, рад")
plt.grid(True)

# -------------------------------------------------
# 5. Демонстрация фильтрации гармонического сигнала
# -------------------------------------------------

t = np.linspace(0, 0.02, int(fs*0.02), endpoint=False)

# гармонический сигнал
f_sig = 2500           # выше частоты среза → фильтр ослабит
x = np.sin(2*np.pi*f_sig * t)

# фильтрация
y = signal.lfilter(bz, az, x)

plt.figure(figsize=(10, 5))
plt.stem(t, x, basefmt=" ", label='Исходный сигнал', linefmt='C0-', markerfmt='C0o')
plt.stem(t, y, basefmt=" ", label='Отфильтрованный', linefmt='C1-', markerfmt='C1o')

plt.title("Фильтрация гармонического сигнала")
plt.xlabel("t, сек")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid(True)

plt.show()

# -------------------------------------------------
# Печать коэффициентов
# -------------------------------------------------
print("Коэффициенты цифрового фильтра:")
print("b =", bz)
print("a =", az)
