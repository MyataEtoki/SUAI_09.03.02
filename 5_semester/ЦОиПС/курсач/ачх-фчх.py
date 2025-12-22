import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Параметры (как в п.1)
N = 16
Fs = N * 1e3          # 16 кГц
f1 = 0.3 * N * 1e3    # 4.8 кГц
f2_eff = Fs - 0.6 * N * 1e3  # 6.4 кГц

# Угловые частоты (рад/с)
w1 = 2 * np.pi * f1
w2 = 2 * np.pi * f2_eff

# Синтез аналогового заграждающего фильтра Баттерворта 4-го порядка
n = 4
b_analog, a_analog = signal.butter(n, [w1, w2], btype='bandstop', analog=True)

# Диапазон частот для построения характеристик (0 – 10 кГц)
f_plot = np.linspace(0, 10e3, 2000)  # Гц
w_plot = 2 * np.pi * f_plot          # рад/с

# Расчёт частотной характеристики H(jw)
w, h = signal.freqs(b_analog, a_analog, worN=w_plot)

# АЧХ в децибелах и ФЧХ в градусах
mag_db = 20 * np.log10(np.abs(h) + 1e-12)  # +eps для защиты от log(0)
phase_deg = np.angle(h, deg=True)

# Построение графиков
plt.figure(figsize=(12, 5))

# АЧХ
plt.subplot(1, 2, 1)
plt.plot(f_plot / 1e3, mag_db, 'b')
plt.title('АЧХ аналогового заграждающего фильтра\n(Баттерворта, 4-го порядка)')
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
plt.title('ФЧХ аналогового заграждающего фильтра')
plt.xlabel('Частота, кГц')
plt.ylabel('Фаза, градусы')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.axvline(f1 / 1e3, color='r', linestyle=':')
plt.axvline(f2_eff / 1e3, color='r', linestyle=':')

plt.tight_layout()
plt.show()