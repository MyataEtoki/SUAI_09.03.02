import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# =========================
# 1️⃣ Таблица DTMF
# =========================
dtmf_freqs = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D'
}

low_freqs = np.array([697, 770, 852, 941])
high_freqs = np.array([1209, 1336, 1477, 1633])
tolerance = 10  # Гц

# =========================
# 3️⃣ Декодирование DTMF с подробной визуализацией
# =========================
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
        frame = data[i*N_tone : (i+1)*N_tone]
        t = np.arange(len(frame)) / fs

        # ---- Отображаем сам тон ----
        plt.figure(figsize=(10,3))
        plt.plot(t, frame)
        plt.title(f"Тон {i+1}")
        plt.xlabel("Время (с)")
        plt.ylabel("Амплитуда")
        plt.grid(True)
        plt.show()

        # ---- FFT ----
        X = np.fft.fft(frame)
        freqs = np.fft.fftfreq(len(frame), d=1/fs)
        magnitude = np.abs(X)

        pos_idx = freqs > 0
        freqs_pos = freqs[pos_idx]
        magnitude_pos = magnitude[pos_idx]

        # ---- Находим пиковые частоты ----
        peak_idx = magnitude_pos.argsort()[-2:]
        peak_freqs = freqs_pos[peak_idx]
        peak_magnitudes = magnitude_pos[peak_idx]

        # ---- Определяем low/high частоты ----
        f_low = find_nearest(min(peak_freqs), low_freqs)
        f_high = find_nearest(max(peak_freqs), high_freqs)

        symbol = dtmf_freqs.get((f_low, f_high), '?')
        decoded += symbol

        # ---- Отображаем амплитудный спектр ----
        plt.figure(figsize=(10,3))
        plt.plot(freqs_pos, magnitude_pos)
        plt.scatter(peak_freqs, peak_magnitudes, color='red', label='Пики FFT')
        plt.title(f"АМПЛИТУДНЫЙ СПЕКТР тона {i+1} (символ '{symbol}')")
        plt.xlabel("Частота (Гц)")
        plt.ylabel("Амплитуда")
        plt.grid(True)
        plt.legend()
        plt.show()

        # ---- Выводим подробности в консоль ----
        print(f"Тон {i+1}: найденные частоты {peak_freqs[0]:.1f} Гц и {peak_freqs[1]:.1f} Гц")
        print(f"Соответствие DTMF: низкая {f_low} Гц, высокая {f_high} Гц → символ '{symbol}'\n")

    return decoded

# =========================
# 4️⃣ Пример использования
# =========================
if __name__ == "__main__":

    decoded_sequence = decode_dtmf_verbose("dtmf_test.wav", tone_duration=0.2)
    print("Декодированная последовательность DTMF:", decoded_sequence)
