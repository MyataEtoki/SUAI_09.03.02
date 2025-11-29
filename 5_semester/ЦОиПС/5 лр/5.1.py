import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# DFT (через numpy)
# -----------------------
def dft_numpy(x):
    return np.fft.fft(x)

# -------------------------------------
# Построение графиков DFT
# -------------------------------------
def plot_dft_parts(X, title_prefix, figsize=(10,6)):
    X = np.asarray(X, dtype=complex)
    N = X.size
    k = np.arange(N)

    real = X.real
    imag = X.imag

    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True)
    fig.suptitle(f'{title_prefix}: действительная и мнимая части', fontsize=14)

    axes[0].stem(k, real, basefmt=" ")
    axes[0].set_ylabel('Re')
    axes[0].grid(True)
    axes[0].set_title('Действительная часть')

    axes[1].stem(k, imag, basefmt=" ")
    axes[1].set_xlabel('k')
    axes[1].set_ylabel('Im')
    axes[1].grid(True)
    axes[1].set_title('Мнимая часть')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# ---------------------------------------------------------
# Основная функция: применить три окна и сравнить результаты
# ---------------------------------------------------------
def compute_and_compare_windows(x):
    x = np.asarray(x)
    N = len(x)

    # --- Построим исходный сигнал ---
    plt.figure(figsize=(10,3))
    plt.plot(x)
    plt.title("Исходный сигнал")
    plt.xlabel("Отсчёт n")
    plt.ylabel("Амплитуда")
    plt.grid(True)
    plt.show()

    # Прямоугольное окно
    rect = np.ones(N)
    hann = np.hanning(N)
    hamming = np.hamming(N)

    x_rect = x * rect
    x_hann = x * hann
    x_hamming = x * hamming

    # DFT
    X_rect = dft_numpy(x_rect)
    X_hann = dft_numpy(x_hann)
    X_hamming = dft_numpy(x_hamming)

    # Рисуем спектры
    plot_dft_parts(X_rect, 'ДПФ c прямоугольным окном')
    plot_dft_parts(X_hann, 'ДПФ с окном Ханна')
    plot_dft_parts(X_hamming, 'ДПФ с окном Хемминга')

    return X_rect, X_hann, X_hamming

# -----------------------
# Пример использования
# -----------------------
if __name__ == "__main__":
    fs = 1000
    T = 0.02
    t = np.arange(0, T, 1/fs)
    x = np.sin(2*np.pi*120*t) + 0.2*np.random.randn(len(t))

    compute_and_compare_windows(x)
