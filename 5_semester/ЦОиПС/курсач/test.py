import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy.signal import windows

# ===========================
# 1. Загрузка голосового сигнала
# ===========================
Fs, x_int = wavfile.read('закусочная-сосисочная-3.wav')  # должен быть 16000 Гц, моно

# Проверка и нормировка
if x_int.ndim > 1:
    x_int = x_int[:, 0]  # моно
x = x_int.astype(np.float64) / (2**15)  # [-1, 1]

# Проверка частоты дискретизации
assert Fs == 16000, f"Ожидалась Fs = 16000 Гц, получено {Fs} Гц"

# ===========================
# 2. Синтез заграждающего фильтра (вариант 4, N=16)
# ===========================
N = 16
f1 = 0.3 * N * 1e3       # 4.8 кГц
f2_raw = 0.6 * N * 1e3   # 9.6 кГц — > Fs/2 → отражаем
f2 = Fs - f2_raw         # 6.4 кГц (эффективная)

# Предыскажение для билинейного преобразования
w1 = 2 * Fs * np.tan(np.pi * f1 / Fs)
w2 = 2 * Fs * np.tan(np.pi * f2 / Fs)

# Аналоговый прототип Баттерворта 4-го порядка
b_an, a_an = signal.butter(4, [w1, w2], btype='bandstop', analog=True)

# Билинейное преобразование → цифровой фильтр
b, a = signal.bilinear(b_an, a_an, fs=Fs)
b = b / a[0]
a = a / a[0]

# ===========================
# 3. Графики АЧХ и ФЧХ аналогового прототипа (п. 3)
# ===========================
w_analog = np.logspace(1, 5, 1000)  # 10 – 100 000 рад/с
w_analog, h_analog = signal.freqs(b_an, a_an, worN=w_analog)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.semilogx(w_analog / (2*np.pi), 20 * np.log10(np.abs(h_analog) + 1e-12))
plt.title('АЧХ аналогового фильтра-прототипа')
plt.xlabel('Частота, Гц')
plt.ylabel('Уровень, дБ')
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.axvspan(f1, f2, color='yellow', alpha=0.3, label='Полоса заграждения')
plt.legend()

plt.subplot(1, 2, 2)
plt.semilogx(w_analog / (2*np.pi), np.angle(h_analog, deg=True))
plt.title('ФЧХ аналогового фильтра-прототипа')
plt.xlabel('Частота, Гц')
plt.ylabel('Фаза, градусы')
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.axvspan(f1, f2, color='yellow', alpha=0.3)
plt.tight_layout()
plt.show()

# ===========================
# 4. Графики АЧХ и ФЧХ цифрового фильтра (п. 5)
# ===========================
w_digital, h_digital = signal.freqz(b, a, fs=Fs, worN=2048)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(w_digital / 1e3, 20 * np.log10(np.abs(h_digital) + 1e-12))
plt.title('АЧХ цифрового фильтра')
plt.xlabel('Частота, кГц')
plt.ylabel('Уровень, дБ')
plt.grid(True, linestyle='--', alpha=0.6)
plt.axvspan(f1 / 1e3, f2 / 1e3, color='yellow', alpha=0.3, label='Полоса заграждения')
plt.xlim(0, Fs/2/1e3)
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(w_digital / 1e3, np.angle(h_digital, deg=True))
plt.title('ФЧХ цифрового фильтра')
plt.xlabel('Частота, кГц')
plt.ylabel('Фаза, градусы')
plt.grid(True, linestyle='--', alpha=0.6)
plt.axvspan(f1 / 1e3, f2 / 1e3, color='yellow', alpha=0.3)
plt.xlim(0, Fs/2/1e3)
plt.tight_layout()
plt.show()

# ===========================
# 5. График полюсов аналогового фильтра (п. 2)
# ===========================
poles = np.roots(a_an)
zeros = np.roots(b_an)

plt.figure(figsize=(6, 6))
plt.axhline(0, color='k', linewidth=0.5)
plt.axvline(0, color='k', linewidth=0.5)
plt.scatter(poles.real, poles.imag, marker='x', s=100, label='Полюсы', color='red')
if len(zeros) > 0:
    plt.scatter(zeros.real, zeros.imag, marker='o', s=80, label='Нули', color='blue')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.title('Полюсы и нули аналогового фильтра Баттерворта (4-й порядок)')
plt.xlabel('Re(s)')
plt.ylabel('Im(s)')
plt.legend()
plt.axis('equal')
plt.tight_layout()
plt.show()

# ===========================
# 6. Фильтрация сигнала (п. 6 и п. 10)
# ===========================
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
y = np.clip(y, -1.0, 1.0)

# ===========================
# 7. График фрагмента сигнала (п. 8)
# ===========================
T_ms = 20
N_plot = int(Fs * T_ms / 1000)
plt.figure(figsize=(10, 4))
plt.stem(np.arange(N_plot) / Fs * 1000, x[:N_plot], basefmt=" ")
plt.title(f'Фрагмент голосового сигнала (первые {T_ms} мс)')
plt.xlabel('Время, мс')
plt.ylabel('Амплитуда')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# ===========================
# 8. Спектры до и после фильтрации (пп. 9, 11)
# ===========================
T_ms_spec = 10
N_fft = int(Fs * T_ms_spec / 1000)  # 160 отсчётов
start_idx = 0

x_seg = x[start_idx:start_idx + N_fft]
y_seg = y[start_idx:start_idx + N_fft]

if len(x_seg) < N_fft:
    x_seg = np.pad(x_seg, (0, N_fft - len(x_seg)))
if len(y_seg) < N_fft:
    y_seg = np.pad(y_seg, (0, N_fft - len(y_seg)))

win = windows.hamming(N_fft)
x_win = x_seg * win
y_win = y_seg * win

X = np.fft.fft(x_win)
Y = np.fft.fft(y_win)
freqs = np.fft.fftfreq(N_fft, 1 / Fs)
half = N_fft // 2
freqs_half = freqs[:half]

mag_x_db = 20 * np.log10(np.abs(X[:half]) + 1e-12)
mag_y_db = 20 * np.log10(np.abs(Y[:half]) + 1e-12)
phase_x = np.angle(X[:half], deg=True)
phase_y = np.angle(Y[:half], deg=True)

# АЧХ — до и после
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(freqs_half / 1e3, mag_x_db, 'b')
plt.title('АЧХ исходного сигнала (первые 10 мс)')
plt.xlabel('Частота, кГц')
plt.ylabel('Уровень, дБ')
plt.grid(True, linestyle='--', alpha=0.6)
plt.axvspan(f1 / 1e3, f2 / 1e3, color='yellow', alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(freqs_half / 1e3, mag_y_db, 'r')
plt.title('АЧХ отфильтрованного сигнала')
plt.xlabel('Частота, кГц')
plt.ylabel('Уровень, дБ')
plt.grid(True, linestyle='--', alpha=0.6)
plt.axvspan(f1 / 1e3, f2 / 1e3, color='yellow', alpha=0.3)
plt.tight_layout()
plt.show()

# ФЧХ — до и после
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(freqs_half / 1e3, phase_x, 'b')
plt.title('ФЧХ исходного сигнала')
plt.xlabel('Частота, кГц')
plt.ylabel('Фаза, градусы')
plt.grid(True, linestyle='--', alpha=0.6)

plt.subplot(1, 2, 2)
plt.plot(freqs_half / 1e3, phase_y, 'r')
plt.title('ФЧХ отфильтрованного сигнала')
plt.xlabel('Частота, кГц')
plt.ylabel('Фаза, градусы')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# ===========================
# 9. Сохранение результата (п. 12)
# ===========================
y_int = np.clip(y * 2**15, -2**15, 2**15 - 1).astype(np.int16)
wavfile.write('обработанно.wav', Fs, y_int)
print("Отфильтрованный сигнал сохранён как 'обработанно.wav'")