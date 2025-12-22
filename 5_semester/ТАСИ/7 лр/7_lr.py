import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from mutagen.mp3 import MP3
import librosa
import soundfile as sf
from pydub import AudioSegment

# === ПАРАМЕТРЫ ===
INPUT_MP3 = r"закусочная-сосисочная-4.mp3"
OUTPUT_MP3 = r"output_variant4.mp3"

# Если ffmpeg не в PATH — раскомментируй и укажи путь:
# AudioSegment.converter = r"C:\ffmpeg\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
# AudioSegment.ffprobe = r"C:\ffmpeg\ffmpeg-7.1.1-full_build\bin\ffprobe.exe"


# === 1. ЧТЕНИЕ И АНАЛИЗ ЗАГОЛОВКА MP3 ===
def read_header(header: str) -> None:
    # header = b"fffbe204"

    bits = bin(int(header, 16)).removeprefix("0b")

    print()
    print(f"Маркер фрейма: {repr(bits[0:11])}")

    match bits[11:13]:
        case "00":
            print(f"Индекс версии MPEG: {repr(bits[11:13])}, MPEG-2.5")
        case "01":
            print(f"Индекс версии MPEG: {repr(bits[11:13])}, Не используется")
        case "10":
            print(f"Индекс версии MPEG: {repr(bits[11:13])}, MPEG-2")
        case "11":
            print(f"Индекс версии MPEG: {repr(bits[11:13])}, MPEG-1")

    match bits[13:15]:
        case "00":
            print(f"Индекс версии Layer: {repr(bits[13:15])}, Не используется")
        case "01":
            print(f"Индекс версии Layer: {repr(bits[13:15])}, Layer 3")
        case "10":
            print(f"Индекс версии Layer: {repr(bits[13:15])}, Layer 2")
        case "11":
            print(f"Индекс версии Layer: {repr(bits[13:15])}, Layer 1")

    print(f"Бит защиты: {repr(bits[15])}, {'Нет защиты' if bits[15] == '0' else 'CRC защита'}")

    print(f"Индекс битрейта, MPEG-1 Layer 3: {repr(bits[16:20])}, битрейт в кбит/с: ", end="")
    match bits[16:20]:
        case "0000":
            print("Не используется")
        case "0001":
            print(32)
        case "0010":
            print(40)
        case "0011":
            print(48)
        case "0100":
            print(56)
        case "0101":
            print(64)
        case "0110":
            print(80)
        case "0111":
            print(96)
        case "1000":
            print(112)
        case "1001":
            print(128)
        case "1010":
            print(160)
        case "1011":
            print(192)
        case "1100":
            print(224)
        case "1101":
            print(256)
        case "1110":
            print(320)
        case "1111":
            print("Не используется")

    print(f"Индекс частоты дискретизации: {repr(bits[20:22])}, для MPEG-1частота дискретизации: ", end="")
    match bits[20:22]:
        case "00":
            print("44 100 Гц")
        case "01":
            print("48 000 Гц")
        case "10":
            print("32 000 Гц")
        case "11":
            print("Не используется")

    print(f"Бит смещения: {repr(bits[22])}, {'Нет смещения' if bits[22] == '0' else 'Смещение данных на 1 байт'}")

    print(f"Бит private: {repr(bits[23])}")

    print(f"Индекс режима канала: {repr(bits[24:26])}, Режим канала: ", end="")
    match bits[24:26]:
        case "00":
            print("Stereo")
        case "01":
            print("Joint stereo")
        case "10":
            print("Dual Channel")
        case "11":
            print("Mono")

    print(f"Расширение режима канала: {repr(bits[26:28])}")
    print(f"Копирайт: {repr(bits[28])}")
    print(f"Оригинал: {repr(bits[29])}")
    print(f"Акцент: {repr(bits[30:])}")


def analyze_mp3_header_and_duration(path: str):
    audio = MP3(path)
    print(f"\n=== ОБЩИЕ ПАРАМЕТРЫ ФАЙЛА ===")
    print(f"Длительность: {audio.info.length:.2f} сек")
    print(f"Частота дискретизации: {audio.info.sample_rate} Гц")
    print(f"Битрейт: {audio.info.bitrate // 1000} кбит/с")

    with open(path, "rb") as f:
        if f.read(3) == b"ID3":
            f.seek(0)
            id3_header = f.read(10)
            id3_size = (id3_header[6] << 21) | (id3_header[7] << 14) | (id3_header[8] << 7) | id3_header[9]
            f.seek(10 + id3_size)

        while True:
            hdr = f.read(4)
            if len(hdr) < 4:
                print("Заголовок не найден!")
                return
            if hdr[0] == 0xFF and (hdr[1] & 0xE0) == 0xE0:
                read_header(hdr.hex())
                break
            f.seek(f.tell() - 3)


# === 2. ОБРАБОТКА: ↓2 + 8 БИТ ===
def process_variant4(input_path: str, output_path: str):
    y, sr = librosa.load(input_path, sr=None, mono=True)
    print(f"\n=== ОБРАБОТКА ПО ВАРИАНТУ 4 ===")
    print(f"Исходная частота: {sr} Гц → новая: {sr // 2} Гц")
    print("Битовая глубина: 8 бит (256 уровней)")

    # ↓2
    y_res = librosa.resample(y, orig_sr=sr, target_sr=sr // 2)
    new_sr = sr // 2

    # 8-битное квантование
    levels = 256
    y_norm = (y_res + 1) / 2
    y_quant = np.round(y_norm * (levels - 1)) / (levels - 1)
    y_quant = y_quant * 2 - 1

    # Сохранение в MP3
    y_int16 = (y_quant * 32767).astype(np.int16)
    audio = AudioSegment(
        y_int16.tobytes(),
        frame_rate=new_sr,
        sample_width=2,
        channels=1
    )
    audio.export(output_path, format="mp3")
    print(f"✅ Файл сохранён: {output_path}")
    return y_quant, new_sr


# === 3. ВИЗУАЛИЗАЦИИ ===
def plot_comparison(original_path: str, processed_y: np.ndarray, processed_sr: int):
    y_orig, sr_orig = librosa.load(original_path, sr=None)

    # Амплитуды
    amp_orig = np.max(y_orig) - np.min(y_orig)
    amp_proc = np.max(processed_y) - np.min(processed_y)
    print(f"\n=== АМПЛИТУДА ===")
    print(f"Исходная: {amp_orig:.6f}")
    print(f"После обработки: {amp_proc:.6f}")
    print("Битовая глубина (по заданию): 8 бит")

    titles = ["Исходный сигнал", "Обработанный (↓2, 8 бит)"]
    signals = [y_orig, processed_y]
    srs = [sr_orig, processed_sr]

    for i, (y, sr, title) in enumerate(zip(signals, srs, titles)):
        # 1. Осциллограмма
        plt.figure(figsize=(10, 2))
        librosa.display.waveshow(y, sr=sr)
        plt.title(f"{title} — временная область")
        plt.xlabel("Время, с")
        plt.ylabel("Амплитуда")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # 2. Спектр
        spec = fft(y)
        freqs = np.fft.fftfreq(len(spec), 1 / sr)
        plt.figure(figsize=(10, 2))
        plt.plot(freqs[:len(freqs)//2], np.abs(spec[:len(spec)//2]))
        plt.title(f"{title} — частотный спектр")
        plt.xlabel("Частота, Гц")
        plt.ylabel("Амплитуда")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # 3. Хромограмма
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_norm = chroma / (chroma.max(axis=0, keepdims=True) + 1e-8)
        plt.figure(figsize=(10, 2))
        librosa.display.specshow(chroma_norm, sr=sr, x_axis='time', y_axis='chroma', cmap='viridis')
        plt.colorbar()
        plt.title(f"{title} — хромаграмма")
        plt.tight_layout()
        plt.show()

        # 4. Спектрограмма
        X = librosa.stft(y)
        Xdb = librosa.amplitude_to_db(np.abs(X), ref=np.max)
        plt.figure(figsize=(10, 3))
        librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log', cmap='magma')
        plt.colorbar(format='%+2.0f dB')
        plt.title(f"{title} — спектрограмма (лог. шкала)")
        plt.tight_layout()
        plt.show()


# === 4. СЕГМЕНТАЦИЯ ПО ЛАПЛАСУ ===
def laplacian_segmentation(y: np.ndarray, sr: int, threshold: float = 0.08):
    print("\n=== СЕГМЕНТАЦИЯ ПО ЛАПЛАСУ ===")
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    lap = np.gradient(np.gradient(rms))
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)

    seg_points = times[np.abs(laplacian := lap) > threshold]
    print(f"Найдено {len(seg_points)} сегментов")
    print(f"Временные метки: {seg_points}")

    plt.figure(figsize=(12, 9))
    plt.subplot(3, 1, 1)
    librosa.display.waveshow(y, sr=sr)
    plt.title("Аудиосигнал (обработанный)")

    plt.subplot(3, 1, 2)
    plt.plot(times, rms)
    plt.title("Энергия (RMS)")

    plt.subplot(3, 1, 3)
    plt.plot(times, lap)
    for t in seg_points:
        plt.axvline(x=t, color='red', linestyle='--', alpha=0.7)
    plt.title("Лапласиан энергии")
    plt.tight_layout()
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
import librosa

def laplacian_segmentation_spectrograms(file_path: str, threshold: float = 0.08):
    """
    Выполняет сегментацию исходного MP3-файла методом Лапласа.
    Визуализирует:
      - Аудиосигнал, энергию, лапласиан во временной области
      - Спектрограммы сигнала, энергии, лапласиана энергии
    """
    print("\n=== СЕГМЕНТАЦИЯ ЛАПЛАСА (ИСХОДНЫЙ СИГНАЛ) ===")

    # 1. Загрузка сигнала
    y, sr = librosa.load(file_path, sr=None, mono=True)
    print(f"Частота дискретизации: {sr} Гц")
    print(f"Длительность: {len(y) / sr:.2f} сек")

    # 2. Параметры STFT
    n_fft = 2048
    hop_length = 512
    frame_length = n_fft

    # 3. Энергия сигнала (RMS)
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    times_rms = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

    # 4. Лапласиан энергии (вторая производная по времени)
    laplacian_rms = np.gradient(np.gradient(rms))
    seg_points = times_rms[np.abs(laplacian_rms) > threshold]

    # 5. STFT и спектрограммы
    stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    spectrogram_energy = np.abs(stft) ** 2  # |STFT|^2 — энергия
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    times_stft = librosa.frames_to_time(np.arange(spectrogram_energy.shape[1]), sr=sr, hop_length=hop_length)

    # 6. Лапласиан энергии в частотно-временной области
    # Для каждой частотной полосы вычисляем лапласиан по времени
    laplacian_spectrogram = np.zeros_like(spectrogram_energy)
    for i in range(spectrogram_energy.shape[0]):
        laplacian_spectrogram[i] = np.gradient(np.gradient(spectrogram_energy[i]))

    # 7. Визуализация
    # --- Спектрограммы ---
    plt.figure(figsize=(10, 8))
    ax4 = plt.subplot(3, 1, 1)
    img4 = librosa.display.specshow(
        librosa.amplitude_to_db(np.abs(stft), ref=np.max),
        sr=sr,
        x_axis='time',
        y_axis='log',
        cmap='magma'
    )
    ax4.set_title("Спектрограмма сигнала (STFT)")
    plt.colorbar(img4, format='%+2.0f dB', ax=ax4)

    ax5 = plt.subplot(3, 1, 2)
    img5 = librosa.display.specshow(
        librosa.amplitude_to_db(spectrogram_energy, ref=np.max),
        sr=sr,
        x_axis='time',
        y_axis='log',
        cmap='magma'
    )
    ax5.set_title("Энергия сигнала (|STFT|²)")
    plt.colorbar(img5, format='%+2.0f dB', ax=ax5)

    ax6 = plt.subplot(3, 1, 3)
    img6 = librosa.display.specshow(
        librosa.amplitude_to_db(np.abs(laplacian_spectrogram), ref=np.max),
        sr=sr,
        x_axis='time',
        y_axis='log',
        cmap='magma'
    )
    ax6.set_title("Лапласиан энергии (по времени для каждой частоты)")
    plt.colorbar(img6, format='%+2.0f dB', ax=ax6)

    plt.tight_layout()
    plt.show()

    # 8. Вывод результатов
    print(f"\n✅ Найдено {len(seg_points)} границ сегментов:")
    print(f"Временные метки (сек): {np.round(seg_points, 3)}")

    return seg_points

# === ГЛАВНАЯ ФУНКЦИЯ ===
def main():
    if not os.path.exists(INPUT_MP3):
        raise FileNotFoundError(f"Файл не найден: {INPUT_MP3}")

    # 1. Анализ заголовка и длительности
    analyze_mp3_header_and_duration(INPUT_MP3)

    # 2. Обработка по варианту 4
    y_proc, sr_proc = process_variant4(INPUT_MP3, OUTPUT_MP3)

    # 3. Визуализации
    plot_comparison(INPUT_MP3, y_proc, sr_proc)

    # 4. Сегментация
    laplacian_segmentation(y_proc, sr_proc)
    laplacian_segmentation_spectrograms(INPUT_MP3, threshold=0.002)

    print("\n✅ Лабораторная работа выполнена!")


if __name__ == "__main__":
    main()