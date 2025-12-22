# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from typing import Literal
from lr_6_1 import WavHeader  # класс WavHeader из Части 1

# === НОВЫЕ ИМПОРТЫ ДЛЯ СУБПОЛОСНОГО КОДИРОВАНИЯ ===
from scipy.signal import firwin, lfilter


def generate_signal(
        duration: float,
        amplitude_percent: float,
        sample_rate: int = 44100,
        signal_type: Literal["noise", "triangle"] = "noise",
        frequency: float = 440.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    :param duration: Длительность сигнала в секундах.
    :param amplitude_percent: Амплитуда в процентах от максимума (0–100).
    :param sample_rate: Частота дискретизации (Гц).
    :param signal_type: Тип сигнала — 'noise' или 'triangle'.
    :param frequency: Частота (Гц), используется только для 'triangle'.
    :return: (время, сигнал) как numpy массивы.
    """
    if not (0 <= amplitude_percent <= 100):
        raise ValueError("Амплитуда должна быть в диапазоне [0, 100]")

    max_amplitude = 1.0  # нормализованный диапазон [-1, 1]
    amplitude = max_amplitude * (amplitude_percent / 100.0)

    n_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)

    if signal_type == "noise":
        signal = np.random.uniform(-1, 1, n_samples)
    elif signal_type == "triangle":
        phase = (t * frequency) % 1.0
        signal = np.where(phase < 0.5, 4 * phase - 1, -4 * phase + 3)
    else:
        raise ValueError("Поддерживаются только 'noise' и 'triangle'")

    signal = amplitude * signal
    return t, signal


def subband_decomposition(signal: np.ndarray, sample_rate: int, decim_factor: int = 2):
    """
    Субполосная децимация: разложение сигнала на НЧ и ВЧ компоненты
    с последующей децимацией каждой в decim_factor раз.

    Возвращает:
        low_band: низкочастотная полоса
        high_band: высокочастотная полоса
        new_sample_rate: новая частота дискретизации
    """
    if decim_factor != 2:
        raise NotImplementedError("Поддерживается только decim_factor=2 для простоты.")

    N = 51  # длина фильтра (нечётная)
    cutoff = sample_rate / 4.0  # Nyquist новой частоты = (fs/2)/2

    # Низкочастотный фильтр
    lpf = firwin(N, cutoff, fs=sample_rate, window='hamming')

    # Высокочастотный фильтр (через инверсию LPF)
    hpf = -lpf.copy()
    hpf[N // 2] += 1.0

    # Фильтрация
    low_filtered = lfilter(lpf, 1.0, signal)
    high_filtered = lfilter(hpf, 1.0, signal)

    # Децимация
    low_band = low_filtered[::decim_factor]
    high_band = high_filtered[::decim_factor]

    new_sample_rate = sample_rate // decim_factor
    return low_band, high_band, new_sample_rate


def quantize_and_dequantize(
        signal: np.ndarray,
        bits: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Равномерное квантование и последующее деквантование (восстановление).

    :param signal: Исходный сигнал в диапазоне [-1, 1].
    :param bits: Число бит квантования (1–16).
    :return: (квантованный сигнал, деквантованный сигнал = квантованный)
    """
    if not (1 <= bits <= 16):
        raise ValueError("Число бит должно быть от 1 до 16")

    levels = 2 ** bits
    min_val, max_val = -1.0, 1.0
    step = (max_val - min_val) / (levels - 1)
    quantization_levels = np.linspace(min_val, max_val, levels)

    # Квантование
    clipped = np.clip(signal, min_val, max_val)
    indices = np.round((clipped - min_val) / step).astype(int)
    indices = np.clip(indices, 0, levels - 1)
    quantized = quantization_levels[indices]

    # Деквантование — в данном случае просто возврат квантованного сигнала
    dequantized = quantized.copy()

    return quantized, dequantized


def signal_to_wav(signal: np.ndarray, sample_rate: int, filename: str):
    """
    Сохраняет нормированный сигнал [-1, 1] в 16-битный моно WAV-файл.
    """
    signal_int16 = np.int16(signal * 32767)
    data_size = signal_int16.nbytes
    header = WavHeader(
        chunk_id="RIFF",
        chunk_size=36 + data_size,
        format="WAVE",
        subchunk1_id="fmt ",
        subchunk1_size=16,
        audio_format=1,
        num_channels=1,
        sample_rate=sample_rate,
        byte_rate=sample_rate * 2,
        block_align=2,
        bits_per_sample=16,
        subchunk2_id="data",
        subchunk2_size=data_size,
    )

    with open(filename, "wb") as f:
        f.write(header.to_bytes())
        f.write(signal_int16.tobytes())
    print(f"✅ Сохранён: {filename}")


# === Основной блок ===
if __name__ == "__main__":
    # 1. Генерация сигнала
    duration = 2.0
    amp_percent = 80.0
    sr = 44100

    # Шум
    t_noise, noise = generate_signal(duration, amp_percent, sr, "noise")
    signal_to_wav(noise, sr, "generated_noise.wav")

    # Треугольник
    t_tri, tri = generate_signal(duration, amp_percent, sr, "triangle", frequency=220.0)
    signal_to_wav(tri, sr, "generated_triangle.wav")

    # 2. СУБПОЛОСНОЕ КОДИРОВАНИЕ (вместо простой децимации)
    low_band, high_band, new_sr = subband_decomposition(tri, sr, decim_factor=2)
    signal_to_wav(low_band, new_sr, "triangle_subband_LPF.wav")  # НЧ
    signal_to_wav(high_band, new_sr, "triangle_subband_HPF.wav")  # ВЧ

    # 3. Квантование
    q_signal, dq_signal = quantize_and_dequantize(tri, bits=4)
    signal_to_wav(q_signal, sr, "triangle_quantized_4bit.wav")

    # 4. Визуализация
    if True:
        plt.figure(figsize=(12, 10))

        # Исходный
        plt.subplot(4, 1, 1)
        plt.plot(t_tri[:1000], tri[:1000], 'k', label="Исходный треугольник")
        plt.title("Исходный сигнал")
        plt.grid(True)
        plt.legend()

        # НЧ-полоса
        t_low = np.linspace(0, duration, len(low_band), endpoint=False)
        plt.subplot(4, 1, 2)
        plt.plot(t_low[:500], low_band[:500], 'b', label="НЧ-полоса (LPF)")
        plt.title(f"Низкочастотная субполоса (fs = {new_sr} Гц)")
        plt.grid(True)
        plt.legend()

        # ВЧ-полоса
        plt.subplot(4, 1, 3)
        plt.plot(t_low[:500], high_band[:500], 'r', label="ВЧ-полоса (HPF)")
        plt.title(f"Высокочастотная субполоса (fs = {new_sr} Гц)")
        plt.grid(True)
        plt.legend()

        # Квантование
        plt.subplot(4, 1, 4)
        plt.plot(t_tri[:1000], tri[:1000], 'k', alpha=0.6, label="Исходный")
        plt.step(t_tri[:1000], q_signal[:1000], 'm', where='mid', label="Квантованный (4 бит)")
        plt.title("Квантование сигнала")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()