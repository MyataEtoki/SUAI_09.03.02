"""
lab_dft_dtmf.py

Реализация для лабораторной работы:
1) прямое ДПФ (наивная реализация) + окна (прямоугольное, Ханна, Хэмминг) и графики действительной/мнимой частей;
2) построение амплитудного и фазового спектров и их графиков;
3) декодирование DTMF из WAV (PCM16 mono);
4) обратное ДПФ (наивная реализация).

Зависимости:
- numpy
- matplotlib
- scipy (только для чтения WAV, опционально; если scipy нет, в коде есть запасной вариант через "wave" и "struct")

Как использовать:
- Импортировать функции из этого файла или запустить как скрипт (внизу есть пример).
- Для декодирования DTMF: вызвать decode_dtmf_wav("path/to/file.wav")

Автор: сгенерировано ChatGPT — учебная версия для лабораторной.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

try:
    from scipy.io import wavfile
except Exception:
    wavfile = None
    import wave, struct

# ------------------------ 1. Прямое ДПФ (наивная реализация) ------------------------

def dft(x):
    """Прямая ДПФ (наивная реализация). Возвращает массив комплексных значений X[k].
    x: 1D numpy array (действительный или комплексный)
    """
    x = np.asarray(x, dtype=complex)
    N = x.size
    n = np.arange(N)
    k = n.reshape((N, 1))  # столбец
    W = np.exp(-2j * np.pi * k * n / N)
    X = W.dot(x)
    return X


def idft(X):
    """Обратное ДПФ (наивная реализация). Возвращает временную последовательность (комплексную).
    X: 1D numpy array комплексных спектральных значений
    """
    X = np.asarray(X, dtype=complex)
    N = X.size
    k = np.arange(N)
    n = k.reshape((N, 1))
    W = np.exp(2j * np.pi * k * n / N)
    x = (W.dot(X)) / N
    return x

# ------------------------ Окна ------------------------

def get_window(x, name='rect'):
    """Вернуть окно той же длины, что и x.
    name: 'rect' (прямоугольное), 'hann', 'hamming'
    """
    N = len(x)
    name = name.lower()
    if name in ('rect', 'rectangle', 'none'):
        return np.ones(N)
    elif name in ('hann', 'hanning'):
        return np.hanning(N)
    elif name in ('hamming',):
        return np.hamming(N)
    else:
        raise ValueError(f"Неизвестное окно: {name}")

# ------------------------ Графики действительной и мнимой частей ------------------------

def plot_real_imag(X, fs=1.0, title_prefix='', use_positive_freqs=True):
    """Построить графики действительной и мнимой частей спектра X.
    fs: частота дискретизации (Гц), для построения оси частот
    use_positive_freqs: если True, отображаем только неотрицательные частоты (для реального входа)
    """
    N = len(X)
    if use_positive_freqs:
        freqs = np.fft.rfftfreq(N, d=1.0/fs) if N>0 else np.array([])
        X_plot = np.fft.rfft(X)
        real = X_plot.real
        imag = X_plot.imag
    else:
        freqs = np.fft.fftfreq(N, d=1.0/fs)
        X_plot = X
        real = X_plot.real
        imag = X_plot.imag

    plt.figure(figsize=(10, 4))
    plt.plot(freqs, real, label='Действительная')
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.title(f'{title_prefix} Действительная часть')
    plt.grid(True)
    plt.legend()

    plt.figure(figsize=(10, 4))
    plt.plot(freqs, imag, label='Мнимaя')
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Амплитуда')
    plt.title(f'{title_prefix} Мнимая часть')
    plt.grid(True)
    plt.legend()

    plt.show()

# ------------------------ 2. Амплитудный и фазовый спектры ------------------------

def amplitude_phase_spectra(X):
    """Возвращает (амплитуда, фаза) для комплексного спектра X.
    Амплитуда возвращается в линейном масштабе, фаза в радианах.
    """
    X = np.asarray(X, dtype=complex)
    A = np.abs(X)
    P = np.angle(X)
    return A, P


def plot_amplitude_phase(X, fs=1.0, title_prefix='', use_db=False, use_positive_freqs=True):
    """Построить амплитудный и фазовый спектры.
    use_db: если True, показать амплитуду в дБ (20*log10(A)).
    """
    N = len(X)
    if use_positive_freqs:
        freqs = np.fft.rfftfreq(N, d=1.0/fs)
        X_plot = np.fft.rfft(X)
    else:
        freqs = np.fft.fftfreq(N, d=1.0/fs)
        X_plot = X

    A, P = amplitude_phase_spectra(X_plot)

    plt.figure(figsize=(10, 4))
    if use_db:
        with np.errstate(divide='ignore'):
            Adb = 20 * np.log10(A)
        plt.plot(freqs, Adb)
        plt.ylabel('Амплитуда (дБ)')
    else:
        plt.plot(freqs, A)
        plt.ylabel('Амплитуда')
    plt.xlabel('Частота (Гц)')
    plt.title(f'{title_prefix} Амплитудный спектр')
    plt.grid(True)

    plt.figure(figsize=(10, 4))
    plt.plot(freqs, P)
    plt.xlabel('Частота (Гц)')
    plt.ylabel('Фаза (рад)')
    plt.title(f'{title_prefix} Фазовый спектр')
    plt.grid(True)

    plt.show()

# ------------------------ 3. Декодирование DTMF ------------------------

# Частоты DTMF в Гц
DTMF_LOW = np.array([697, 770, 852, 941])
DTMF_HIGH = np.array([1209, 1336, 1477, 1633])

# Клавиатура DTMF (строка low index, столбец high index)
DTMF_KEYS = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3', (697, 1633): 'A',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6', (770, 1633): 'B',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9', (852, 1633): 'C',
    (941, 1209): '*', (941, 1336): '0', (941, 1477): '#', (941, 1633): 'D',
}


def read_wav_mono(path):
    """Читать WAV PCM16 mono. Возвращает (fs, samples as float in [-1,1]).
    Попытка сначала через scipy, иначе через wave+struct.
    """
    if wavfile is not None:
        fs, data = wavfile.read(path)
        # Если stereo, привести к mono (усреднить каналы) — но ожидается mono
        if data.ndim == 2:
            data = data.mean(axis=1)
        # Преобразовать в float в [-1,1] если тип int16
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
        else:
            data = data.astype(np.float32)
        return fs, data

    # fallback
    with wave.open(path, 'rb') as wf:
        nchan = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        fs = wf.getframerate()
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)
        if sampwidth == 2:
            fmt = f"<{nframes * nchan}h"
            ints = struct.unpack(fmt, raw)
            arr = np.array(ints, dtype=np.int16)
            if nchan == 2:
                arr = arr.reshape(-1, 2).mean(axis=1)
            data = arr.astype(np.float32) / 32768.0
            return fs, data
        else:
            raise RuntimeError('Unsupported sample width: ' + str(sampwidth))


def detect_dtmf_in_frame(frame, fs, f_tol=20, min_relative_peak=0.2):
    """Определить присутствие DTMF тона в одном фрейме.
    Возвращает (low_freq, high_freq, spectrum) или (None, None, spectrum)
    f_tol: допустимая погрешность (Гц) при сопоставлении частот
    min_relative_peak: относительный порог от максимума спектра (0..1)
    """
    N = len(frame)
    if N == 0:
        return (None, None, None)
    # Используем rFFT для эффективности
    spec = np.fft.rfft(frame * np.hanning(N))
    freqs = np.fft.rfftfreq(N, d=1.0/fs)
    mag = np.abs(spec)

    # Для каждого целевого частотного списка находим индекс ближайшей частоты
    def pick_freq(targets):
        best = None
        best_mag = 0.0
        for f in targets:
            # найти индекс, где |freqs - f| минимально
            idx = np.argmin(np.abs(freqs - f))
            # можно учесть соседние бины (интерполяция) — для простоты смотрим только один бин
            val = mag[idx]
            if val > best_mag:
                best_mag = val
                best = f
        return best, best_mag

    low_f, low_mag = pick_freq(DTMF_LOW)
    high_f, high_mag = pick_freq(DTMF_HIGH)

    # Оценим порог: оба обнаруженных пика должны быть заметны
    global_max = mag.max() if mag.size>0 else 0.0
    if global_max <= 0:
        return (None, None, (freqs, mag))

    if low_mag >= min_relative_peak * global_max and high_mag >= min_relative_peak * global_max:
        return (low_f, high_f, (freqs, mag))
    else:
        return (None, None, (freqs, mag))


def decode_dtmf_wav(path, frame_duration=0.08, hop=None, visualize=False):
    """Декодировать DTMF последовательность из WAV-файла.
    frame_duration: длительность окна в секундах (типично 50-100 ms для тонов DTMF)
    hop: шаг между окнами (если None, равен frame_duration)
    visualize: если True, рисует спектр для каждого обнаруженного тона

    Возвращает строку обнаруженных клавиш и список временных меток (в секундах).
    """
    fs, data = read_wav_mono(path)
    if hop is None:
        hop = frame_duration
    Nframe = int(round(frame_duration * fs))
    Nhop = int(round(hop * fs))
    if Nframe <= 0:
        raise ValueError('Слишком маленькая длительность фрейма / слишком большая частота дискретизации')

    keys = []
    times = []
    pos = 0
    while pos + Nframe <= len(data):
        frame = data[pos:pos+Nframe]
        low, high, spec = detect_dtmf_in_frame(frame, fs)
        t = pos / fs
        if low is not None and high is not None:
            key = DTMF_KEYS.get((low, high), '?')
            keys.append(key)
            times.append(t)
            if visualize:
                freqs, mag = spec
                plt.figure(figsize=(8,3))
                plt.plot(freqs, mag)
                plt.axvline(low, linestyle='--')
                plt.axvline(high, linestyle='--')
                plt.title(f'DTMF detect: {key} at {t:.3f}s (low={low}, high={high})')
                plt.xlabel('Hz')
                plt.grid(True)
                plt.show()
            # пропустить вперед на длительность фрейма (предполагается, что тон длится >= frame_duration)
            pos += Nframe
        else:
            pos += Nhop

    # Консолидировать подряд идущие одинаковые обнаружения (дебаунсинг)
    consolidated = []
    consolidated_times = []
    for k, t in zip(keys, times):
        if len(consolidated) == 0 or k != consolidated[-1]:
            consolidated.append(k)
            consolidated_times.append(t)
    return ''.join(consolidated), consolidated_times

# ------------------------ Пример использования и тесты ------------------------

if __name__ == '__main__':
    # Пример синтетического сигнала: сумма двух синусоид (DTMF-подобный)
    fs = 8000
    T = 0.5
    t = np.arange(0, T, 1/fs)
    f1 = 697
    f2 = 1209
    x = 0.6*np.sin(2*np.pi*f1*t) + 0.6*np.sin(2*np.pi*f2*t)

    # 1) сравнение окон
    for wname in ('rect', 'hann', 'hamming'):
        w = get_window(x, wname)
        xw = x * w
        # вычисляем DFT (в учебных целях наивная реализация) — для больших N это долго
        X = dft(xw)
        print(f'Окно: {wname}, длина {len(x)}')
        # рисуем действительную/мнимую части (только положительные частоты)
        plot_real_imag(X, fs=fs, title_prefix=f'Окно={wname}', use_positive_freqs=True)
        plot_amplitude_phase(X, fs=fs, title_prefix=f'Окно={wname}', use_db=False, use_positive_freqs=True)

    # 3) если есть файл example_dtmf.wav рядом, попытаться декодировать
    example_path = 'example_dtmf.wav'
    if os.path.exists(example_path):
        seq, times = decode_dtmf_wav(example_path, frame_duration=0.08, visualize=True)
        print('Обнаруженная последовательность:', seq)
    else:
        print('Файл example_dtmf.wav не найден. Поместите WAV-файл в ту же папку под именем example_dtmf.wav или вызовите функцию decode_dtmf_wav(path) отдельно.')

    # 4) тест обратного ДПФ
    X = dft(x)
    x_rec = idft(X)
    # x_rec может быть комплексным с очень маленькой мнимой частью — отрежем
    x_rec = np.real_if_close(x_rec, tol=1e-5)
    err = np.max(np.abs(x - x_rec))
    print(f'Максимальная ошибка восстановления (прямо->обратно): {err:.6e}')

# Конец файла
