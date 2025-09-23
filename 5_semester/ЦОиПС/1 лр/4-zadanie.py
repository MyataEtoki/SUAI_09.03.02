import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, lfilter

# -----------------------------
# Параметры
# -----------------------------
Fs = 1000          # Частота дискретизации, Гц
N_per = 2048       # Длина синусоидального сигнала
freqs_count = 5    # Количество исследуемых частот
a = 0.5            # Коэффициент для IIR-фильтра

# Частоты (рад/отсчет) — не начиная с 0, иначе будет константа
omega = np.linspace(0.1, np.pi, freqs_count)
freqs_hz = omega * Fs / (2 * np.pi)

n = np.arange(N_per)

# -----------------------------
# Подготовка сигналов и фильтров
# -----------------------------
signals = []
firs = []
iirs = []

# FIR: y[n] = (x[n] + x[n-1]) / 2
b_fir = np.array([0.5, 0.5])
a_fir = np.array([1])

# IIR: y[n] = x[n] + a * y[n-1]
b_iir = np.array([1])
a_iir = np.array([1, -a])

for w in omega:
    x = np.sin(w * n)
    signals.append(x)

    # Фильтрация FIR
    y_fir = lfilter(b_fir, a_fir, x)
    firs.append(y_fir)

    # Фильтрация IIR
    y_iir = lfilter(b_iir, a_iir, x)
    iirs.append(y_iir)

# -----------------------------
# Частотный отклик фильтров
# -----------------------------
w, h_fir = freqz(b_fir, a_fir, worN=2048)
_, h_iir = freqz(b_iir, a_iir, worN=2048)

freqs = w * Fs / (2 * np.pi)  # Перевод в Гц

# -----------------------------
# Фазовые характеристики
# -----------------------------
phi_fir_freqz = np.unwrap(np.angle(h_fir))
phi_iir_freqz = np.unwrap(np.angle(h_iir))

# Аналитические формулы для фаз
phi_fir_analytic = np.unwrap(np.arctan2(-np.sin(w), 1 + np.cos(w)))
phi_iir_analytic = np.unwrap(-np.arctan2(a * np.sin(w), 1 - a * np.cos(w)))

# -----------------------------
# Построение графика
# -----------------------------
plt.figure(figsize=(10, 6))

# FIR
plt.plot(freqs, phi_fir_freqz, color='blue', label="ФЧХ КИХ-фильтра")
plt.plot(freqs, phi_fir_analytic, color='red', linestyle='--', label="Расчёт ФЧХ КИХ-фильтра")

# IIR
plt.plot(freqs, phi_iir_freqz, color='blue', label="ФЧХ БИХ-фильтра")
plt.plot(freqs, phi_iir_analytic, color='red', linestyle='--', label="Расчёт ФЧХ БИХ-фильтра")

plt.title("Сравнение фазо-частотных характеристик КИХ и БИХ")
plt.xlabel("Частота, Гц")
plt.ylabel("Фаза, рад")
plt.legend()
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.show()
