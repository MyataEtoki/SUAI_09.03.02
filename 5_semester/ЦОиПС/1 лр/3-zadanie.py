import numpy as np
import matplotlib.pyplot as plt

N = 200  # длина сигнала для измерения
freqs = np.linspace(0, np.pi, 200)  # частоты от 0 до pi
a = 0.7  # коэффициент для БИХ

amp_kih = []
amp_bih = []

for w in freqs:
    n = np.arange(N)
    x = np.sin(w * n)

    # КИХ
    y_kih = np.zeros(N)
    for i in range(N):
        if i == 0:
            y_kih[i] = x[i] / 2
        else:
            y_kih[i] = (x[i] + x[i - 1]) / 2
    amp_kih.append(np.max(np.abs(y_kih[int(N / 2):])))

    # БИХ
    y_bih = np.zeros(N)
    for i in range(N):
        if i == 0:
            y_bih[i] = x[i]
        else:
            y_bih[i] = x[i] + a * y_bih[i - 1]
    amp_bih.append(np.max(np.abs(y_bih[int(N / 2):])))

amp_kih = np.array(amp_kih)
amp_bih = np.array(amp_bih)

# --- Теоретические АЧХ ---
amp_kih_theory = np.abs(np.cos(freqs / 2))
amp_bih_theory = 1 / np.sqrt(1 - 2 * a * np.cos(freqs) + a ** 2)

# --------------------------
# График исследуемого сигнала (пример: ω = π/4)
# --------------------------
n = np.arange(N)
w_test = np.pi / 4
x_test = np.sin(w_test * n)

plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(n[:50], x_test[:50], label=f"x(n)=sin({w_test:.2f}·n)")
plt.title("Пример исследуемого сигнала (синусоида)")
plt.xlabel("n")
plt.ylabel("x(n)")
plt.grid()
plt.legend()

# --- АЧХ КИХ ---
plt.subplot(3, 1, 2)
plt.plot(freqs, amp_kih, label="эксперимент")
plt.plot(freqs, amp_kih_theory, 'r--', label="теория")
plt.title("АЧХ КИХ-фильтра")
plt.xlabel("ω (рад/отсчёт)")
plt.ylabel("|H(ω)|")
plt.legend()
plt.grid()

# --- АЧХ БИХ ---
plt.subplot(3, 1, 3)
plt.plot(freqs, amp_bih, label="эксперимент")
plt.plot(freqs, amp_bih_theory, 'r--', label="теория")
plt.title(f"АЧХ БИХ-фильтра (a={a})")
plt.xlabel("ω (рад/отсчёт)")
plt.ylabel("|H(ω)|")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
