import numpy as np
import matplotlib.pyplot as plt

def amplitude_phase_spectra(real_part, imag_part, title_prefix="Спектры"):
    real_part = np.asarray(real_part)
    imag_part = np.asarray(imag_part)
    X = real_part + 1j*imag_part

    amplitude = np.abs(X)
    phase = np.unwrap(np.angle(X))

    N = len(X)
    k = np.arange(N)

    fig, axs = plt.subplots(2, 1, figsize=(10,6), sharex=True)
    fig.suptitle(f"{title_prefix}: амплитудный и фазовый спектры", fontsize=14)

    axs[0].stem(k, amplitude, basefmt=" ")
    axs[0].set_ylabel("Амплитуда |X[k]|")
    axs[0].grid(True)
    axs[0].set_title("Амплитудный спектр")

    axs[1].stem(k, phase, basefmt=" ")
    axs[1].set_xlabel("k")
    axs[1].set_ylabel("Фаза arg(X[k])")
    axs[1].grid(True)
    axs[1].set_title("Фазовый спектр")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    return amplitude, phase

# ---------------------
# Пример использования
# ---------------------
if __name__ == "__main__":
    fs = 1000
    T = 0.02
    t = np.arange(0, T, 1/fs)
    # Единый сигнал для обоих файлов
    x = np.sin(2*np.pi*120*t) + 0.2*np.random.randn(len(t))

    # --- Исходный сигнал ---
    plt.figure(figsize=(10,3))
    plt.plot(x)
    plt.title("Исходный сигнал")
    plt.xlabel("Отсчёт n")
    plt.ylabel("Амплитуда")
    plt.grid(True)
    plt.show()

    X = np.fft.fft(x)
    amp, ph = amplitude_phase_spectra(X.real, X.imag)
