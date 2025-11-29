import numpy as np
from scipy.io import wavfile

# =========================
# 1️⃣ Параметры DTMF
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
# 2️⃣ Генерация WAV с DTMF
# =========================
def generate_dtmf_wav(sequence, fs=8000, tone_duration=0.2, filename="dtmf_test.wav"):
    """
    sequence : str - последовательность символов DTMF, например "123A0#"
    fs : int - частота дискретизации
    tone_duration : float - длительность одного символа в секундах
    """
    t = np.arange(0, tone_duration, 1/fs)
    signal = np.array([], dtype=np.float32)

    # Обратная таблица: символ -> частоты
    symbol_to_freq = {v: k for k, v in dtmf_freqs.items()}

    for s in sequence:
        f_low, f_high = symbol_to_freq[s]
        tone = np.sin(2*np.pi*f_low*t) + np.sin(2*np.pi*f_high*t)
        # Нормируем амплитуду, чтобы не клипало
        tone /= np.max(np.abs(tone))
        signal = np.concatenate((signal, tone))

    # Преобразуем в PCM 16 bit
    signal_int16 = np.int16(signal * 32767)
    wavfile.write(filename, fs, signal_int16)
    print(f"WAV файл '{filename}' с DTMF сигналом сгенерирован.")

# =========================
# 3️⃣ Декодирование DTMF
# =========================
def find_nearest(freq, candidates):
    return candidates[np.argmin(np.abs(candidates - freq))]

def decode_dtmf(wav_file, tone_duration=0.2):
    fs, data = wavfile.read(wav_file)

    if data.ndim > 1:
        data = data[:,0]  # берем только первый канал

    N_tone = int(fs * tone_duration)
    num_tones = len(data) // N_tone
    decoded = ""

    for i in range(num_tones):
        frame = data[i*N_tone : (i+1)*N_tone]
        X = np.fft.fft(frame)
        freqs = np.fft.fftfreq(len(frame), d=1/fs)
        magnitude = np.abs(X)

        # только положительные частоты
        pos_idx = freqs > 0
        freqs = freqs[pos_idx]
        magnitude = magnitude[pos_idx]

        # Находим две пиковые частоты
        peak_idx = magnitude.argsort()[-2:]
        peak_freqs = freqs[peak_idx]

        # Определяем low/high
        f_low = find_nearest(min(peak_freqs), low_freqs)
        f_high = find_nearest(max(peak_freqs), high_freqs)

        symbol = dtmf_freqs.get((f_low, f_high), '?')
        decoded += symbol

    return decoded

# =========================
# 4️⃣ Пример использования
# =========================
if __name__ == "__main__":
    # Последовательность для генерации
    test_sequence = "3566678889776563566678889776556356668999*00*9*6678#89*6687767****99999*****09876"
    #generate_dtmf_wav(test_sequence, fs=8000, tone_duration=0.18, filename="dtmf_test.wav")

    # Декодирование
    decoded_sequence = decode_dtmf("dtmf_test.wav", tone_duration=0.18)
    print("Декодированная последовательность DTMF:", decoded_sequence)
