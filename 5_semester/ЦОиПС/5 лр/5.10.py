import numpy as np
import matplotlib.pyplot as plt
import wave
import struct


# Функции DFT и IDFT


def dft(x):
    """
    Прямое Дискретное Преобразование Фурье (DFT) через матричное умножение.
    Возвращает комплексный спектр.
    """
    x = np.asarray(x, dtype=complex)
    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    W = np.exp(-2j * np.pi * k * n / N)
    return np.dot(W, x) / N

def idft(X):
    """
    Обратное Дискретное Преобразование Фурье (IDFT) через матричное умножение.
    """
    X = np.asarray(X, dtype=complex)
    N = len(X)
    k = np.arange(N)
    n = k.reshape((N, 1))
    W = np.exp(2j * np.pi * k * n / N)
    return np.dot(W, X)


# Генерация сигнала

fs = 5000
t = np.linspace(0, 0.01, fs // 100)
u = np.sin(2 * np.pi * 1000 * t)

plt.figure(figsize=(10,4))
plt.title("Исходный сигнал")
plt.stem(t, u, linefmt='b-', markerfmt='bo', basefmt='b', label="дискретный")
plt.xlabel("t, с")
plt.ylabel("Амплитуда")
plt.grid()
plt.legend()
plt.show()


# Формирование окон

N = len(u)
k = np.arange(N)

# Прямоугольное окно
w_rect = np.ones(N)
rect = u * w_rect

# Окно Ханна
w_hann = 0.5 * (1 - np.cos(2 * np.pi * k / (N - 1)))
hann = u * w_hann

# Окно Хэмминга
w_hamming = 0.53836 - 0.46164 * np.cos(2 * np.pi * k / (N - 1))
hamming = u * w_hamming

windows = {
    "Прямоугольное окно": rect,
    "Окно Ханна": hann,
    "Окно Хэмминга": hamming
}


# Обработка каждого окна

for name, sig in windows.items():
    U = dft(sig)
    Re = np.real(U)
    Im = np.imag(U)
    Amp = np.abs(U)
    Phase = np.angle(U)
    k = np.arange(len(U))

    # Сигнал
    plt.figure(figsize=(10, 4))
    plt.title(f"{name}")
    plt.stem(t, sig, linefmt='b-', markerfmt='bo', basefmt='b', label="дискретный")
    plt.xlabel("t, с")
    plt.ylabel("u[n]")
    plt.grid()
    plt.legend()
    plt.show()

    # Действительная и мнимая части
    plt.figure(figsize=(8,6))
    plt.suptitle(f"{name}", fontsize=14)

    plt.subplot(2, 1, 1)
    plt.title("Действительная часть DFT")
    plt.stem(k, Re, linefmt='b-', markerfmt='bo', basefmt='b')
    plt.xlabel("k")
    plt.ylabel("Re{U[k]}")
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.title("Мнимая часть DFT")
    plt.stem(k, Im, linefmt='r-', markerfmt='ro', basefmt='b')
    plt.xlabel("k")
    plt.ylabel("Im{U[k]}")
    plt.grid()
    plt.show()

    # Амплитудный и фазовый спектры
    plt.figure(figsize=(8,6))
    plt.suptitle(f"{name}", fontsize=14)

    plt.subplot(2, 1, 1)
    plt.title("Амплитудный спектр")
    plt.stem(k, Amp, linefmt='b-', markerfmt='bo', basefmt='b')
    plt.xlabel("k")
    plt.ylabel("|U[k]|")
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.title("Фазовый спектр")
    plt.stem(k, Phase, linefmt='g-', markerfmt='go', basefmt='g')
    plt.xlabel("k")
    plt.ylabel("arg(U[k])")
    plt.grid()
    plt.show()


# Восстановление сигнала

X_rect = dft(u)
x_recovered = idft(X_rect)

plt.figure(figsize=(10,4))
plt.title("Сравнение исходного и восстановленного сигналов")
plt.stem(t, u, linefmt='b-', markerfmt='bo', label="исходный")
plt.stem(t, np.real(x_recovered), linefmt='--', label="восстановленный")
plt.xlabel("t, с")
plt.ylabel("u[n]")
plt.legend()
plt.grid()
plt.show()


# Частоты DTMF

low_freqs = [697, 770, 852, 941]
high_freqs = [1209, 1336, 1477, 1633]

dtmf_map = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D'
}

# Декодирование DTMF
def decode_dtmf(filename):
    # Чтение WAV файла
    with wave.open(filename, 'rb') as wav:
        fs = wav.getframerate()
        frames = wav.readframes(wav.getnframes())
        samples = np.array(struct.unpack('<' + 'h' * wav.getnframes(), frames))

    frame_len = int(0.05 * fs)
    decoded = ""
    prev_symbol = None

    for start in range(0, len(samples), frame_len):
        frame = samples[start:start+frame_len]
        if len(frame) < frame_len:
            break
        if np.max(np.abs(frame)) < 500:
            prev_symbol = None
            continue

        X = np.abs(dft(frame))
        freqs = np.fft.fftfreq(len(frame), 1/fs)

        # Низкий диапазон
        low_mask = (freqs >= 600) & (freqs <= 1000)
        low_X = X[low_mask]
        low_freqs_axis = freqs[low_mask]
        lf_detected = low_freqs_axis[np.argmax(low_X)]

        # Высокий диапазон
        high_mask = (freqs >= 1200) & (freqs <= 1700)
        high_X = X[high_mask]
        high_freqs_axis = freqs[high_mask]
        hf_detected = high_freqs_axis[np.argmax(high_X)]

        # Ближайшие стандартные частоты
        lf = min(low_freqs, key=lambda f: abs(f-lf_detected))
        hf = min(high_freqs, key=lambda f: abs(f-hf_detected))
        symbol = dtmf_map.get((lf,hf), None)

        if symbol is not None and symbol != prev_symbol:
            decoded += symbol
            # Визуализация сигнала
            t_frame = np.arange(len(frame))/fs
            plt.figure(figsize=(6,3))
            plt.plot(t_frame, frame)
            plt.title(f"Сигнал для символа '{symbol}'")
            plt.xlabel("Время, с")
            plt.ylabel("Амплитуда")
            plt.grid()
            plt.show()

        prev_symbol = symbol

    return decoded


# 8️⃣ Пример использования DTMF

decoded_msg = decode_dtmf("dtmf_test.wav")
print("Расшифрованное сообщение:", decoded_msg)
