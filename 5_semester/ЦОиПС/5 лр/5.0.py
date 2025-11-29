import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# -----------------------
# Ручная реализация DFT и IDFT
# -----------------------
def dft(x):
    x = np.asarray(x, dtype=complex)
    N = len(x)
    n = np.arange(N)
    k = n.reshape((N,1))
    W = np.exp(-2j * np.pi * k * n / N)
    return np.dot(W, x) / N

def idft(X):
    X = np.asarray(X, dtype=complex)
    N = len(X)
    k = np.arange(N)
    n = k.reshape((N,1))
    W = np.exp(2j * np.pi * k * n / N)
    return np.dot(W, X)

# -----------------------
# Исходный сигнал
# -----------------------
fs = 8000
T = 0.01
t = np.linspace(0, T, int(fs*T), endpoint=False)
u = np.sin(2*np.pi*1000*t) + 0.2*np.random.randn(len(t))

plt.figure(figsize=(10,3))
plt.title("Исходный сигнал")
plt.stem(t, u, linefmt='r-', markerfmt='ro', basefmt='k')
plt.xlabel("t, с")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()

# -----------------------
# Формирование окон вручную
# -----------------------
N = len(u)
k = np.arange(N)

w_rect = np.ones(N)
w_hann = 0.5 * (1 - np.cos(2*np.pi*k/(N-1)))
w_hamming = 0.53836 - 0.46164*np.cos(2*np.pi*k/(N-1))

windows = {
    "Прямоугольное окно": u * w_rect,
    "Окно Ханна": u * w_hann,
    "Окно Хэмминга": u * w_hamming
}

# -----------------------
# Построение спектров для каждого окна
# -----------------------
for name, sig in windows.items():
    U = dft(sig)
    Re = np.real(U)
    Im = np.imag(U)
    Amp = np.abs(U)
    Phase = np.angle(U)
    k_idx = np.arange(len(U))

    # Действительная и мнимая части
    plt.figure(figsize=(8,6))
    plt.suptitle(f"{name}", fontsize=14)
    plt.subplot(2,1,1)
    plt.stem(k_idx, Re, linefmt='r-', markerfmt='ro', basefmt='k')
    plt.title("Действительная часть DFT")
    plt.xlabel("k")
    plt.ylabel("Re{U[k]}")
    plt.grid(True)

    plt.subplot(2,1,2)
    plt.stem(k_idx, Im, linefmt='g-', markerfmt='go', basefmt='k')
    plt.title("Мнимая часть DFT")
    plt.xlabel("k")
    plt.ylabel("Im{U[k]}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Амплитудный и фазовый спектры
    plt.figure(figsize=(8,6))
    plt.suptitle(f"{name}", fontsize=14)
    plt.subplot(2,1,1)
    plt.stem(k_idx, Amp, linefmt='m-', markerfmt='mo', basefmt='k')
    plt.title("Амплитудный спектр")
    plt.xlabel("k")
    plt.ylabel("|U[k]|")
    plt.grid(True)

    plt.subplot(2,1,2)
    plt.stem(k_idx, Phase, linefmt='c-', markerfmt='co', basefmt='k')
    plt.title("Фазовый спектр")
    plt.xlabel("k")
    plt.ylabel("arg(U[k])")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# -----------------------
# Обратное ДПФ
# -----------------------
X_rect = dft(u)
x_rec = idft(X_rect)

plt.figure(figsize=(10,4))
plt.title("Сравнение исходного и восстановленного сигналов")
plt.stem(t, u, linefmt='r-', markerfmt='ro', label="Исходный")
plt.stem(t, np.real(x_rec), linefmt='--', markerfmt='bx', label="Восстановленный")
plt.xlabel("t, с")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid(True)
plt.show()

# =========================
# DTMF: параметры
# =========================
dtmf_freqs = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D'
}

low_freqs = np.array([697, 770, 852, 941])
high_freqs = np.array([1209, 1336, 1477, 1633])

# -----------------------
# Функция декодирования DTMF
# -----------------------
def find_nearest(freq, candidates):
    return candidates[np.argmin(np.abs(candidates - freq))]

def decode_dtmf_verbose(wav_file, tone_duration=0.2):
    fs, data = wavfile.read(wav_file)
    if data.ndim > 1:
        data = data[:,0]

    N_tone = int(fs * tone_duration)
    num_tones = len(data) // N_tone
    decoded = ""

    print(f"Частота дискретизации: {fs} Гц")
    print(f"Количество тонов в сигнале: {num_tones}")

    for i in range(num_tones):
        frame = data[i*N_tone:(i+1)*N_tone]
        t_frame = np.arange(len(frame))/fs

        # Отображаем тон
        plt.figure(figsize=(10,3))
        plt.plot(t_frame, frame)
        plt.title(f"Тон {i+1}")
        plt.xlabel("Время (с)")
        plt.ylabel("Амплитуда")
        plt.grid(True)
        plt.show()

        # FFT
        X = dft(frame)
        freqs = np.fft.fftfreq(len(frame), d=1/fs)
        magnitude = np.abs(X)
        pos_idx = freqs > 0
        freqs_pos = freqs[pos_idx]
        magnitude_pos = magnitude[pos_idx]

        # Пики
        peak_idx = magnitude_pos.argsort()[-2:]
        peak_freqs = freqs_pos[peak_idx]
        f_low = find_nearest(min(peak_freqs), low_freqs)
        f_high = find_nearest(max(peak_freqs), high_freqs)
        symbol = dtmf_freqs.get((f_low,f_high),'?')
        decoded += symbol

        # Амплитудный спектр
        plt.figure(figsize=(10,3))
        plt.plot(freqs_pos, magnitude_pos)
        plt.scatter(peak_freqs, magnitude_pos[peak_idx], color='red', label='Пики FFT')
        plt.title(f"АМПЛИТУДНЫЙ СПЕКТР тона {i+1} (символ '{symbol}')")
        plt.xlabel("Частота (Гц)")
        plt.ylabel("Амплитуда")
        plt.grid(True)
        plt.legend()
        plt.show()

        print(f"Тон {i+1}: найденные частоты {peak_freqs[0]:.1f}, {peak_freqs[1]:.1f} → символ '{symbol}'")

    return decoded

# -----------------------
# Пример декодирования DTMF
# -----------------------
# decoded_msg = decode_dtmf_verbose("dtmf_test.wav", tone_duration=0.18)
# print("Декодированная последовательность:", decoded_msg)
