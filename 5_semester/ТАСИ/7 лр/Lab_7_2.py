import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
import librosa
import soundfile as sf
from pydub import AudioSegment


def read_amplitude_and_bit_depth(path: str) -> None:
    waveform, _ = librosa.load(path)
    audio_data, _ = sf.read(path)

    amplitude = np.max(waveform) - np.min(waveform)
    bit_depth = audio_data.dtype.itemsize

    print(f"Амплитуда: {amplitude}")
    print(f"Битовая глубина: {bit_depth}")


def signal_for_time(path: str) -> None:
    waveform, sampling_rate = librosa.load(path)
    librosa.display.waveshow(waveform, sr=sampling_rate)
    plt.title("Представление формы сигнала во временной области")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid()
    plt.show()


def frequency_spectrum(path: str) -> None:
    waveform, sampling_rate = librosa.load(path)
    spectrum = fft(waveform)
    frequencies = np.fft.fftfreq(len(spectrum), 1 / sampling_rate)

    plt.plot(frequencies[: len(frequencies) // 2], np.abs(spectrum[: len(spectrum) // 2]))  # type: ignore
    plt.xlabel("Частота, Гц")
    plt.ylabel("Амплитуда")
    plt.title("Частотный спектр")
    plt.grid(True)
    plt.show()


def chromagram(path: str) -> None:
    # 1. Загрузка аудио
    waveform, sampling_rate = librosa.load(path)

    # 2. Построение хромограммы энергии цветности
    chroma = librosa.feature.chroma_stft(y=waveform, sr=sampling_rate)

    # 3. Нормализация хромограммы по каждому фрейму
    chroma_norm = chroma / chroma.max(axis=0, keepdims=True)
    chroma_norm = np.nan_to_num(chroma_norm)  # на случай деления на 0

    # 4. Отображение
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(chroma_norm, x_axis="time", y_axis="chroma", sr=sampling_rate, cmap="viridis")
    plt.colorbar(label="Normalized Energy")
    plt.title("Normalized Chromagram")
    plt.tight_layout()
    plt.show()


def show_spectrogram(mp3_path):
    # 1. Загрузка аудио
    y, sr = librosa.load(mp3_path, sr=None)

    # 2. Вычисление STFT (короткое преобразование Фурье)
    stft = librosa.stft(y)

    # 3. Преобразование в амплитудную спектрограмму (логарифмическую)
    spectrogram = librosa.amplitude_to_db(np.abs(stft), ref=np.max)

    # 4. Отображение спектрограммы
    plt.figure(figsize=(12, 5))
    librosa.display.specshow(
        spectrogram,
        sr=sr,
        x_axis="time",
        y_axis="log",  # логарифмическая шкала частот — удобнее для слуха
        cmap="magma",
    )

    plt.colorbar(format="%+2.0f dB")
    plt.title("Log Spectrogram (STFT)")
    plt.tight_layout()
    plt.show()


def process_mp3(
    input_path: str,
    output_path: str,
    target_sr: int = 8000,  # новая частота дискретизации
):
    """
    Загружает MP3, уменьшает частоту дискретизации,
    квантует сигнал до 4 бит и сохраняет обратно в MP3.
    """
    AudioSegment.converter = r"C:\ffmpeg\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"
    AudioSegment.ffprobe = r"C:\ffmpeg\ffmpeg-7.1.1-full_build\bin\ffprobe.exe"

    # 1. Загрузка MP3 через librosa
    y, sr = librosa.load(input_path, sr=None, mono=True)

    # 2. Ресемплинг
    if sr != target_sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=target_sr)

    # 3. Квантизация до 4 бит
    # 4 бита → 16 уровней квантизации
    bits = 4
    levels = 2**bits  # 16 уровней

    # Нормализуем [-1,1] → [0,1]
    y_norm = (y + 1) / 2

    # Квантуем
    y_quant = np.round(y_norm * (levels - 1)) / (levels - 1)

    # Возвращаем в диапазон [-1,1]
    y_quant = y_quant * 2 - 1

    # Конвертируем в int16 для сохранения
    y_int16 = (y_quant * 32767).astype(np.int16)

    # 4. Сохранение в MP3 через pydub
    # pydub принимает raw audio как bytes
    audio = AudioSegment(
        y_int16.tobytes(),
        frame_rate=target_sr,
        sample_width=2,  # 16-bit PCM для MP3-кодирования
        channels=1,
    )

    audio.export(output_path, format="mp3")
    print(f"Файл сохранён: {output_path}")


if __name__ == "__main__":
    path = r"закусочная-сосисочная-4.mp3"
    new_path = r"output_variant4.mp3"

    read_amplitude_and_bit_depth(path)
