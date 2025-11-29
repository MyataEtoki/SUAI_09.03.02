import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------
# 1) Наивная реализация обратного ДПФ (O(N^2))
#    x[n] = (1/N) * sum_{k=0..N-1} X[k] * exp(+j*2*pi*k*n/N)
# ------------------------------------------------
def idft_naive(X):
    """
    Наивная реализация обратного ДПФ.

    Вход:
        X : array_like (complex) - спектр длины N
    Возврат:
        x : numpy.ndarray (complex) - восстановленный сигнал длины N
    """
    X = np.asarray(X, dtype=complex)
    N = X.size
    n = np.arange(N)
    x = np.empty(N, dtype=complex)
    for ni in range(N):
        exponents = np.exp(2j * np.pi * np.arange(N) * ni / N)  # exp(+j*2π k n / N)
        x[ni] = np.sum(X * exponents) / N
    return x

# ------------------------------------------------
# 2) Быстрая реализация через numpy
# ------------------------------------------------
def idft_numpy(X):
    """
    Обратное ДПФ через numpy.fft.ifft.
    Возвращает комплексный сигнал (обычно почти вещественный, если X — корректный DFT).
    """
    return np.fft.ifft(X)

# ------------------------------------------------
# 3) Восстановление из Re и Im частей
# ------------------------------------------------
def idft_from_parts(real_part, imag_part, method='numpy'):
    """
    Восстановить сигнал по Re и Im частям спектра.

    method: 'numpy' или 'naive'
    """
    X = np.asarray(real_part, dtype=float) + 1j * np.asarray(imag_part, dtype=float)
    if method == 'numpy':
        return idft_numpy(X)
    elif method == 'naive':
        return idft_naive(X)
    else:
        raise ValueError("method must be 'numpy' or 'naive'")

# ------------------------------------------------
# 4) Утилита: построение сравнения исходного и восстановленного сигнала
# ------------------------------------------------
def plot_reconstruction(original, reconstructed, title_prefix="Reconstruction", sample_rate=None):
    """
    Строит график: исходный сигнал (реальная часть), восстановленный (реальная часть),
    и график ошибки (исходный - восстановленный).

    Если указан sample_rate (Hz), по оси X будет время в секундах, иначе — номера отсчётов.
    """
    original = np.asarray(original)
    reconstructed = np.asarray(reconstructed)

    # По оси X
    N = len(original)
    if sample_rate is not None:
        t = np.arange(N) / sample_rate
        xlabel = "Время (с)"
    else:
        t = np.arange(N)
        xlabel = "Отсчёт n"

    rec_real = np.real(reconstructed)
    error = original - rec_real

    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f"{title_prefix}", fontsize=14)

    axs[0].plot(t, original, label='Исходный (реал)', linewidth=1)
    axs[0].set_ylabel("Амплитуда")
    axs[0].grid(True)
    axs[0].legend()

    axs[1].plot(t, rec_real, label='Восстановленный (реал)', linewidth=1)
    axs[1].set_ylabel("Амплитуда")
    axs[1].grid(True)
    axs[1].legend()

    axs[2].plot(t, error, label='Ошибка (исх - восст)', linewidth=1)
    axs[2].set_xlabel(xlabel)
    axs[2].set_ylabel("Ошибка")
    axs[2].grid(True)
    axs[2].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    # Возвращаем численные метрики
    mse = np.mean(error**2)
    max_abs_err = np.max(np.abs(error))
    print(f"MSE: {mse:.6e}, max abs error: {max_abs_err:.6e}")

    return mse, max_abs_err

# ------------------------------------------------
# 5) Пример использования
# ------------------------------------------------
if __name__ == "__main__":
    # Пример: тот же сигнал, что и раньше — синус 120 Hz + шум
    fs = 1000.0
    T = 0.02
    t = np.arange(0, T, 1/fs)
    x = np.sin(2*np.pi*120*t) + 0.2*np.random.randn(len(t))

    # Вычислим спектр (DFT)
    X = np.fft.fft(x)

    # 1) восстановление через numpy.ifft
    x_rec_np = idft_numpy(X)
    print("Восстановление через numpy.ifft:")
    plot_reconstruction(x, x_rec_np, title_prefix="IDFT via numpy.ifft", sample_rate=fs)

    # 2) восстановление через наивный IDFT (демонстрация; для больших N долго)
    # (если N большой, можно закомментировать следующий блок)
    if len(X) <= 1024:  # защитный порог
        x_rec_naive = idft_naive(X)
        print("Восстановление через наивный idft_naive:")
        plot_reconstruction(x, x_rec_naive, title_prefix="IDFT naive", sample_rate=fs)
    else:
        print("Наивный IDFT пропущен (N > 1024) — слишком медленно для демонстрации.")
