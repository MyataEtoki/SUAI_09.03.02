import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import windows

# Загрузка сигнала
Fs, x_int = wavfile.read('закусочная-сосисочная-3.wav')
if x_int.ndim > 1:
    x_int = x_int[:, 0]
x = x_int.astype(np.float64) / (2**15)

# Выбор фрагмента (например, с 1.0 до 1.032 сек — гласный звук)
start_sec = 1.0
N_fft = 512
start_idx = int(start_sec * Fs)
x_seg = x[start_idx:start_idx + N_fft]

# Если фрагмент короче — дополним нулями
if len(x_seg) < N_fft:
    x_seg = np.pad(x_seg, (0, N_fft - len(x_seg)))

# Применение окна Хэмминга
win = windows.hamming(N_fft)
x_win = x_seg * win

# ДПФ (через FFT)
X = np.fft.fft(x_win)
freqs = np.fft.fftfreq(N_fft, 1/Fs)

# Односторонний спектр
X_half = X[:N_fft//2]
freqs_half = freqs[:N_fft//2]

# Амплитуда (в дБ) и фаза
mag = np.abs(X_half)
mag_db = 20 * np.log10(mag + 1e-12)
phase = np.angle(X_half, deg=True)

# Графики
plt.figure(figsize=(12, 5))

plt.plot(1, 2, 1)
plt.plot(freqs_half / 1e3, mag_db)
plt.title('Амплитудный спектр (голос)')
plt.xlabel('Частота, кГц')
plt.ylabel('Уровень, дБ')
plt.grid(True, linestyle='--', alpha=0.6)

plt.figure(figsize=(12, 5))
plt.plot(1, 2, 2)
plt.plot(freqs_half / 1e3, phase)
plt.title('Фазовый спектр (голос)')
plt.xlabel('Частота, кГц')
plt.ylabel('Фаза, градусы')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()