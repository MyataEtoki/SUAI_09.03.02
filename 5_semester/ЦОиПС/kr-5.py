import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры
N = 16
Fs = N * 1e3          # 16 кГц
f1 = 0.3 * N * 1e3    # 4.8 кГц
f2_eff = Fs - 0.6 * N * 1e3  # 6.4 кГц

# Синтез аналогового прототипа
n = 4
w1 = 2 * np.pi * f1
w2 = 2 * np.pi * f2_eff
b_analog, a_analog = signal.butter(n, [w1, w2], btype='bandstop', analog=True)

# Билинейное преобразование → цифровой фильтр
b_digital, a_digital = signal.bilinear(b_analog, a_analog, fs=Fs)

# Нормировка
b_digital = b_digital / a_digital[0]
a_digital = a_digital / a_digital[0]

# Построение АЧХ и ФЧХ цифрового фильтра
f_plot = np.linspace(0, Fs/2, 2000)  # 0 – 8 кГц
w, h = signal.freqz(b_digital, a_digital, worN=2*np.pi*f_plot/Fs)

# АЧХ в дБ, ФЧХ в градусах
mag_db = 20 * np.log10(np.abs(h) + 1e-12)
phase_deg = np.angle(h, deg=True)

# Графики
plt.figure(figsize=(12, 5))

# АЧХ
plt.subplot(1, 2, 1)
plt.plot(f_plot / 1e3, mag_db, 'b')
plt.title('АЧХ цифрового заграждающего фильтра\n(Баттерворта, 4-го порядка)')
plt.xlabel('Частота, кГц')
plt.ylabel('Уровень, дБ')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.axvline(f1 / 1e3, color='r', linestyle=':', label=f'$f_1 = {f1/1e3:.1f}$ кГц')
plt.axvline(f2_eff / 1e3, color='r', linestyle=':', label=f'$f_2 = {f2_eff/1e3:.1f}$ кГц')
plt.legend()
plt.ylim([-60, 5])

# ФЧХ
plt.subplot(1, 2, 2)
plt.plot(f_plot / 1e3, phase_deg, 'g')
plt.title('ФЧХ цифрового заграждающего фильтра')
plt.xlabel('Частота, кГц')
plt.ylabel('Фаза, градусы')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.axvline(f1 / 1e3, color='r', linestyle=':')
plt.axvline(f2_eff / 1e3, color='r', linestyle=':')

plt.tight_layout()
plt.show()