import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==============================
# 1. ИНИЦИАЛИЗАЦИЯ ПАРАМЕТРОВ
# ==============================
# Заданные параметры сигнала
t_min = 18.0
t_max = 41.0
A = 7.0
A0 = 1.0
f = 8.0        # Гц
phi = 4.0      # рад

# Параметры АЦП
f_d = 100.0    # Гц (частота дискретизации)
b = 8          # бит (разрядность)
code_type = "прямой"  # тип кода

# ==============================
# 2. ГЕНЕРАЦИЯ СИГНАЛОВ
# ==============================
def generate_signals(t_min, t_max, A, A0, f, phi, f_d, dt_high=0.001):
    # Временные массивы
    t_high = np.arange(t_min, t_max, dt_high)
    t_samp = np.arange(t_min, t_max, 1.0 / f_d)
    # Аналоговый сигнал
    x_high = A0 + A * np.cos(2 * np.pi * f * t_high + phi)
    x_samp = A0 + A * np.cos(2 * np.pi * f * t_samp + phi)
    return t_high, x_high, t_samp, x_samp

# ==============================
# 3. КВАНТОВАНИЕ
# ==============================
def quantize_signal(x_samp, b):
    xmin = np.min(x_samp)
    xmax = np.max(x_samp)
    Vref = max(abs(xmin), abs(xmax))    # симметричный диапазон
    Vmin, Vmax = -Vref, Vref

    levels = 2 ** b
    Delta = (Vmax - Vmin) / levels

    q_index = np.round((x_samp - Vmin) / Delta).astype(int)
    q_index = np.clip(q_index, 0, levels - 1)

    x_quant = Vmin + (q_index + 0.5) * Delta
    return x_quant, q_index, Vmin, Vmax, Delta

# ==============================
# 4. КОДИРОВАНИЕ (ПРЯМОЙ КОД)
# ==============================
def sign_magnitude_code(q_index, b):
    levels = 2 ** b
    mid = levels // 2
    codes = []
    for idx in q_index:
        sign = 1 if idx < mid else 0
        if sign == 1:
            mag_idx = mid - 1 - idx
        else:
            mag_idx = idx - mid
        mag_bits = format(int(mag_idx), f'0{b-1}b')
        code = str(sign) + mag_bits
        codes.append(code)
    return codes

# ==============================
# 5. ПОСТРОЕНИЕ ГРАФИКОВ
# ==============================
def plot_all(t_high, x_high, t_samp, x_samp, x_quant, quant_error):
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), constrained_layout=True)

    # Аналоговый сигнал
    axs[0].plot(t_high, x_high, label='аналоговый')
    axs[0].set_title("Аналоговый сигнал")
    axs[0].set_xlabel("t, c")
    axs[0].set_ylabel("V")
    axs[0].grid(True)
    axs[0].legend()

    # Дискретный + квантованный
    axs[1].plot(t_high, x_high, 'C0', alpha=0.5, label='аналоговый')
    axs[1].stem(t_samp, x_samp, markerfmt='C1o', linefmt='C1-', basefmt=" ")
    axs[1].step(t_samp, x_quant, where='mid', label='квантованный', linewidth=1.5)
    axs[1].set_title("Дискретизация и квантование")
    axs[1].set_xlabel("t, c")
    axs[1].set_ylabel("V")
    axs[1].grid(True)
    axs[1].legend()

    # Ошибка квантования
    axs[2].stem(t_samp, quant_error, basefmt=" ")
    axs[2].set_title("Ошибка квантования")
    axs[2].set_xlabel("t, c")
    axs[2].set_ylabel("Ошибка (V)")
    axs[2].grid(True)

    plt.show()
# ==============================
# Квантованный сигнал (отдельно)
# ==============================
def plot_quantized_signal(t_samp, x_quant):
    plt.figure(figsize=(10,4))
    plt.step(t_samp, x_quant, where='mid', label='квантованный сигнал', linewidth=1.5)
    plt.title("Квантованный сигнал")
    plt.xlabel("t, c")
    plt.ylabel("V")
    plt.grid(True)
    plt.legend()
    plt.show()

# ==============================
# Цифровой сигнал (отдельно, по индексам квантования)
# ==============================
def plot_digital_signal(t_samp, q_index):
    plt.figure(figsize=(10,4))
    plt.step(t_samp, q_index, where='mid', label='цифровой сигнал (индексы квантования)', color='C3')
    plt.title("Цифровой сигнал")
    plt.xlabel("t, c")
    plt.ylabel("Код")
    plt.grid(True)
    plt.legend()
    plt.show()

# ==============================
# 6. СТАТИСТИЧЕСКИЙ АНАЛИЗ
# ==============================
def quantization_statistics(x_samp, x_quant, Delta):
    error = x_samp - x_quant
    abs_error = np.abs(error)
    mse = np.mean(error ** 2)
    std = np.std(error)
    theoretical_var = (Delta ** 2) / 12
    theoretical_std = np.sqrt(theoretical_var)

    print("=== Статистика квантования ===")
    print(f"MSE (эмпирическая): {mse:.6f} В²")
    print(f"σ (эмпирическая): {std:.6f} В")
    print(f"Теоретическая дисперсия Δ²/12: {theoretical_var:.6f} В²")
    print(f"Теоретическая σ: {theoretical_std:.6f} В")

    # Гистограмма ошибок
    plt.figure(figsize=(8, 4))
    plt.hist(abs_error, bins=30)
    plt.title("Гистограмма абсолютной ошибки квантования |e|")
    plt.xlabel("|e|, В")
    plt.ylabel("Частота")
    plt.grid(True)
    plt.show()

# ==============================
# ГЛАВНЫЙ БЛОК ПРОГРАММЫ
# ==============================
if __name__ == "__main__":
    # 1. Генерация сигналов
    t_high, x_high, t_samp, x_samp = generate_signals(t_min, t_max, A, A0, f, phi, f_d)

    # 2. Квантование
    x_quant, q_index, Vmin, Vmax, Delta = quantize_signal(x_samp, b)

    # 3. Кодирование
    codes = sign_magnitude_code(q_index, b)

    # (опционально) первые 12 отсчётов в таблицу
    df = pd.DataFrame({
        "t, c": t_samp[:12],
        "x_samp, V": x_samp[:12],
        "x_quant, V": x_quant[:12],
        "q_index": q_index[:12],
        "code (прямой)": codes[:12]
    })
    print("\n=== Первые 12 отсчётов ===")
    print(df.to_string(index=False))

    # 4. Построение графиков
    quant_error = x_samp - x_quant
    plot_all(t_high, x_high, t_samp, x_samp, x_quant, quant_error)

    # Квантованный сигнал
    plot_quantized_signal(t_samp, x_quant)

    # Цифровой сигнал
    plot_digital_signal(t_samp, q_index)

    # 5. Статистика
    quantization_statistics(x_samp, x_quant, Delta)

max_abs_error = np.max(np.abs(quant_error))
print("Эмпирическая максимальная ошибка квантования:", max_abs_error, "В")
