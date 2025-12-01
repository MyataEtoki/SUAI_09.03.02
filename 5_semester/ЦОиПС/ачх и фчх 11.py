import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy.signal import windows


# 0. АЧХ И ФЧХ аналогового фильтра
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

# 1. Загрузка голосового сигнала
Fs, x_int = wavfile.read('закусочная-сосисочная-3.wav')  # должен быть 16000 Гц, моно

# Проверка и нормировка
if x_int.ndim > 1:
    x_int = x_int[:, 0]  # моно
x = x_int.astype(np.float64) / (2**15)  # [-1, 1]

# Проверка частоты дискретизации
assert Fs == 16000, f"Ожидалась Fs = 16000 Гц, получено {Fs} Гц"

# 2. Синтез заграждающего фильтра (вариант 4, N=16)
N = 16
f1 = 0.3 * N * 1e3   # 4.8 кГц
f2_raw = 0.6 * N * 1e3  # 9.6 кГц — > Fs/2 → отражаем
f2 = Fs - f2_raw     # 6.4 кГц (эффективная)

# Предыскажение
w1 = 2 * Fs * np.tan(np.pi * f1 / Fs)
w2 = 2 * Fs * np.tan(np.pi * f2 / Fs)

# Аналоговый фильтр
b_an, a_an = signal.butter(4, [w1, w2], btype='bandstop', analog=True)

# Билинейное преобразование
b, a = signal.bilinear(b_an, a_an, fs=Fs)
b = b / a[0]
a = a / a[0]

# 3. Фильтрация сигнала
def butterworth_filter(x, b, a):
    N_sig = len(x)
    y = np.zeros_like(x)
    M = len(b) - 1
    K = len(a) - 1
    for n in range(N_sig):
        acc = 0.0
        for k in range(M + 1):
            if n - k >= 0:
                acc += b[k] * x[n - k]
        for k in range(1, K + 1):
            if n - k >= 0:
                acc -= a[k] * y[n - k]
        y[n] = acc
    return y

y = butterworth_filter(x, b, a)
y = np.clip(y, -1.0, 1.0)  # защита от переполнения

# 4. Выбор фрагмента: первые 10 мс → 160 отсчётов
T_ms = 10
N_fft = int(Fs * T_ms / 1000)  # 160
start_idx = 0

x_seg = x[start_idx:start_idx + N_fft]
y_seg = y[start_idx:start_idx + N_fft]

# Дополнение нулями (на случай, если сигнала меньше 160 отсчётов)
if len(x_seg) < N_fft:
    x_seg = np.pad(x_seg, (0, N_fft - len(x_seg)))
if len(y_seg) < N_fft:
    y_seg = np.pad(y_seg, (0, N_fft - len(y_seg)))

# Окно Хэмминга
win = windows.hamming(N_fft)
x_win = x_seg * win
y_win = y_seg * win

# 5. ДПФ и спектры
X = np.fft.fft(x_win)
Y = np.fft.fft(y_win)

freqs = np.fft.fftfreq(N_fft, 1 / Fs)
half = N_fft // 2

# Амплитуды в дБ
mag_x_db = 20 * np.log10(np.abs(X[:half]) + 1e-12)
mag_y_db = 20 * np.log10(np.abs(Y[:half]) + 1e-12)

# Фазы в градусах
phase_x = np.angle(X[:half], deg=True)
phase_y = np.angle(Y[:half], deg=True)

freqs_half = freqs[:half]  # в Гц

# 6. Построение графиков
plt.figure(figsize=(12, 5))

# ЧХ: исходный и отфильтрованный
#plt.subplot(1, 2, 1)
plt.plot(freqs_half / 1e3, mag_x_db, 'b', label='Исходный сигнал')
plt.title('АЧХ исходного сигнала (первые 10 мс)')
plt.xlabel('Частота, кГц')
plt.ylabel('Уровень, дБ')
plt.grid(True, linestyle='--', alpha=0.6)
plt.axvspan(f1 / 1e3, f2 / 1e3, color='yellow', alpha=0.3, label='Полоса заграждения')
plt.legend()

plt.figure(figsize=(12, 5))
#plt.subplot(1, 2, 2)
plt.plot(freqs_half / 1e3, phase_x, 'b')
plt.title('ФЧХ исходного сигнала')
plt.xlabel('Частота, кГц')
plt.ylabel('Фаза, градусы')
plt.grid(True, linestyle='--', alpha=0.6)



plt.figure(figsize=(12, 5))
# ФЧХ: исходный и отфильтрованный
#plt.subplot(1, 2, 1)
plt.plot(freqs_half / 1e3, mag_y_db, 'r', label='Отфильтрованный сигнал')
plt.title('АЧХ отфильтрованного сигнала (первые 10 мс)')
plt.xlabel('Частота, кГц')
plt.ylabel('Уровень, дБ')
plt.grid(True, linestyle='--', alpha=0.6)
plt.axvspan(f1 / 1e3, f2 / 1e3, color='yellow', alpha=0.3, label='Полоса заграждения')
plt.legend()

plt.figure(figsize=(12, 5))
#plt.subplot(1, 2, 2)
plt.plot(freqs_half / 1e3, phase_y, 'r')
plt.title('ФЧХ отфильтрованного сигнала')
plt.xlabel('Частота, кГц')
plt.ylabel('Фаза, градусы')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

w, h = signal.freqz(b, a, fs=Fs)
plt.plot(w/1e3, 20*np.log10(abs(h) + 1e-12))
plt.axvspan(4.8, 6.4, color='yellow', alpha=0.3)
plt.xlim(0, 8)
plt.title('АЧХ цифрового фильтра')
plt.xlabel('Частота, кГц')
plt.ylabel('Уровень, дБ')
plt.grid(True)
plt.show()

# Предполагается, что y — отфильтрованный сигнал в диапазоне [-1, 1]
y_int = np.clip(y * 2**15, -2**15, 2**15 - 1).astype(np.int16)
wavfile.write('обработанно.wav', Fs, y_int)

print("Отфильтрованный сигнал сохранён как 'обработанно.wav'")


