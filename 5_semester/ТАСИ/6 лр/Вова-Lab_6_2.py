from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

from Lab_6_1 import WavHeader


def generate_signal(
    duration: float,
    amplitude: float,
    signal_frequency: int,
    sample_rate: int = 44100,
    signal_type: Literal["rect", "sin"] = "sin",
) -> tuple[np.ndarray, np.ndarray]:
    # Создаем массив временных отсчетов
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    match signal_type:
        case "sin":
            signal = amplitude * np.sin(2 * np.pi * signal_frequency * t)
        case "rect":
            signal = amplitude * np.sign(np.sin(2 * np.pi * signal_frequency * t))

    return t, signal


def saw_to_wav(signal: np.ndarray, sample_rate: int = 44100, out_path_file: str = "wav_file.wav") -> None:
    # нормализация в диапазон 16-битного PCM
    signal_int16 = np.int16(signal * 32767)

    # количество байт данных
    data_size = signal_int16.nbytes

    header = WavHeader(
        "RIFF", 36 + data_size, "WAVE", "fmt ", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16, "data", data_size
    )

    with open(out_path_file, "wb") as out_wav_file:
        out_wav_file.write(header.to_bytes())
        out_wav_file.write(signal_int16.tobytes())


def upsample_signal(signal: np.ndarray, old_sample_rate: int, new_sample_rate: int) -> tuple[np.ndarray, np.ndarray]:
    duration = len(signal) / old_sample_rate
    old_t = np.linspace(0, duration, len(signal), endpoint=False)

    new_length = int(duration * new_sample_rate)
    new_t = np.linspace(0, duration, new_length, endpoint=False)

    new_signal = np.interp(new_t, old_t, signal)

    return new_t, new_signal


def quantize(signal: np.ndarray, levels: int, min_value: float, max_value: float):
    # Количество уровней
    step = (max_value - min_value) / (levels - 1)

    # Создаем уровни квантования
    quantization_levels = np.linspace(min_value, max_value, levels)

    # Отсекаем значения, выходящие за пределы диапазона
    quantized_signal = np.clip(signal, min_value, max_value)

    # Находим ближайший уровень квантования для каждого отсчета
    indices = np.round((quantized_signal - min_value) / step).astype(int)

    # Ограничиваем индексы допустимым диапазоном
    indices = np.clip(indices, 0, levels - 1)

    # Присваиваем квантованные значения
    quantized_signal = quantization_levels[indices]

    return quantized_signal, quantization_levels


def spline_dequantization(quantized_signal: np.ndarray, smoothness: float = 0.1):
    quantized_signal = np.asarray(quantized_signal)
    n = len(quantized_signal)
    x = np.arange(n)

    # Создаем сплайн
    spline = interpolate.UnivariateSpline(x, quantized_signal, s=smoothness * n)

    # Генерируем сглаженный сигнал
    interpolated_signal = spline(x)

    return interpolated_signal


if __name__ == "__main__":
    # 1) generation signal
    t, signal = generate_signal(2.5, 5, 1, 44100, "sin")

    if False:
        plt.plot(t, signal, "k")
        plt.title("Генерация сигнала")
        plt.xlabel("Временные отсчеты, с.")
        plt.ylabel("Амплитуда сигнала")
        plt.grid(True)
        plt.show()

    # 2) upsampling signal
    up_t, x = generate_signal(2.5, 5, 4, 100, "sin")
    new_t, new_signal = upsample_signal(x, 100, 150)

    if False:
        plt.plot(up_t, x, "-o", color="blue", markerfacecolor="red", label="Исходный сигнал")
        plt.plot(new_t, new_signal, "-o", color="black", markerfacecolor="pink", label="Новый сигнал")
        plt.title("Увеличение частоты дискретизации сигнала")
        plt.xlabel("Временные отсчеты, с.")
        plt.ylabel("Амплитуда сигнала")
        plt.legend(loc="lower left")
        plt.grid()
        plt.show()

    # 3) quantize and dequantize signal
    q_signal, indeces = quantize(signal, 8, -3.5, 3.5)
    deq_signal = spline_dequantization(q_signal)

    if True:
        plt.plot(t, signal, "black", label="Исходный сигнал")
        plt.step(t, q_signal, "blue", label="Квантованный сигнал")
        plt.plot(t, deq_signal, "red", label="Деквантованный сигнал")
        plt.title("Квантование и деквантование сигнала")
        plt.xlabel("Временные отсчеты, с")
        plt.ylabel("Амплитуда сигнала")
        plt.legend()
        plt.grid()
        plt.show()
