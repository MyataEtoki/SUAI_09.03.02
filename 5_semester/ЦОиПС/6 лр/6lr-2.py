import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# Параметры фильтра
# ------------------------------
n = 8                # Порядок фильтра Баттерворта
fc = 1900            # Частота среза, Гц
fd = 8000            # Частота дискретизации, Гц
Omega_c = 2 * np.pi * fc  # Аналоговая частота среза (без предыскажения)

# ------------------------------
# Расчёт аналогового фильтра H(s)
# ------------------------------
poles_s = []
for k in range(1, n + 1):
    angle = np.pi * (2 * k + n - 1) / (2 * n)
    p = Omega_c * np.exp(1j * angle)
    if np.real(p) < 0:
        poles_s.append(p)

a_s = np.poly(poles_s).real
b_s = np.array([Omega_c ** n])

# ------------------------------
# Билинейное преобразование
# ------------------------------
def bilinear_manual(b, a, fs):
    T = 1 / fs
    poles_s = np.roots(a)
    zeros_s = np.roots(b) if len(b) > 1 else np.array([])

    z_poles = [(1 + p * T / 2) / (1 - p * T / 2) for p in poles_s]
    if len(zeros_s) > 0:
        z_zeros = [(1 + z * T / 2) / (1 - z * T / 2) for z in zeros_s]
    else:
        z_zeros = [-1] * len(z_poles)

    a_z = np.poly(z_poles).real
    b_z = np.poly(z_zeros).real
    gain = np.sum(a_z) / np.sum(b_z)
    b_z = b_z * gain
    return b_z, a_z

b_z, a_z = bilinear_manual(b_s, a_s, fd)

# ------------------------------
# Диаграмма нулей и полюсов
# ------------------------------
zeros = np.roots(b_z)
poles = np.roots(a_z)

plt.figure(figsize=(6, 6))
plt.scatter(np.real(zeros), np.imag(zeros), marker='o', color='blue', s=80, label='Нули')
plt.scatter(np.real(poles), np.imag(poles), marker='x', color='red', s=80, label='Полюса')
phi = np.linspace(0, 2*np.pi, 500)
plt.plot(np.cos(phi), np.sin(phi), 'k--', label='Единичная окружность')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlabel('Re')
plt.ylabel('Im')
plt.title('Диаграмма нулей и полюсов')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.show()

# ------------------------------
# АЧХ и ФЧХ
# ------------------------------
omega = np.linspace(0, np.pi, 2048)
ejw = np.exp(1j * omega)
H = np.polyval(b_z, ejw) / np.polyval(a_z, ejw)
mag = np.abs(H)
phase = np.angle(H)
phase_unwrapped = np.unwrap(phase)

plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(omega, mag, 'b')
plt.title('АЧХ')
plt.xlabel('ω, рад')
plt.ylabel('|H(e^{jω})|')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(omega, phase_unwrapped, 'r')
plt.title('ФЧХ')
plt.xlabel('ω, рад')
plt.ylabel('arg(H(e^{jω}))')
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------
# Демонстрация фильтрации
# ------------------------------
def apply_filter(b, a, x):
    y = np.zeros_like(x, dtype=float)
    for n_idx in range(len(x)):
        y[n_idx] = b[0] * x[n_idx]
        for i in range(1, len(b)):
            if n_idx - i >= 0:
                y[n_idx] += b[i] * x[n_idx - i]
        for j in range(1, len(a)):
            if n_idx - j >= 0:
                y[n_idx] -= a[j] * y[n_idx - j]
    return y

f_pass = 1500   # Частота в полосе пропускания
f_stop = 2000   # Частота в полосе заграждения
N = 80
n_t = np.arange(N)

x_pass = np.sin(2 * np.pi * f_pass * n_t / fd)
x_stop = np.sin(2 * np.pi * f_stop * n_t / fd)

y_pass = apply_filter(b_z, a_z, x_pass)
y_stop = apply_filter(b_z, a_z, x_stop)

# Визуализация
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.stem(n_t / fd * 1000, x_pass, linefmt='C0-', markerfmt='C0o', basefmt=' ', label='Вход (1500 Гц)')
plt.stem(n_t / fd * 1000, y_pass, linefmt='C1-', markerfmt='C1s', basefmt=' ', label='Выход')
plt.title('Сигнал в полосе пропускания')
plt.xlabel('t, мс')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.stem(n_t / fd * 1000, x_stop, linefmt='C0-', markerfmt='C0o', basefmt=' ', label='Вход (2500 Гц)')
plt.stem(n_t / fd * 1000, y_stop, linefmt='C1-', markerfmt='C1s', basefmt=' ', label='Выход')
plt.title('Сигнал в полосе заграждения')
plt.xlabel('t, мс')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()