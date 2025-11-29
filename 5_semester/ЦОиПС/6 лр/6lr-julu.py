import numpy as np
import matplotlib.pyplot as plt

# Параметры
n = 8
fc = 1900
fd = 8000
Omega_c = 2 * np.pi * fc  # аналоговая частота среза

# Расчёт полюсов фильтра Баттерворта
poles = []
for k in range(1, n+1):
    angle = np.pi * (2*k + n - 1) / (2*n)
    p = Omega_c * np.exp(1j*angle)
    if np.real(p) < 0:
        poles.append(p)

# Коэффициенты ai и bi аналоговыого фильтра
a_s = np.poly(poles).real
b_s = np.array([Omega_c**n])
print("Аналоговый фильтр H(s):")
print("b(s) =", b_s)
print("a(s) =", np.round(a_s, 6))


# Билинейное преобразование
def bilinear_manual(b, a, fs):
    T = 1/fs
    # Нахождение полюсов аналогового фильтра
    poles_s = np.roots(a)
    zeros_s = np.roots(b) if len(b) > 1 else np.array([])

    # Преобразование полюсов и нулей в z-плоскость
    z_poles = [(1 + p*T/2)/(1 - p*T/2) for p in poles_s]
    z_zeros = [(1 + z*T/2)/(1 - z*T/2) for z in zeros_s] if len(zeros_s) > 0 else np.array([-1]*len(z_poles))

    # Вычисление коэффициентов цифрового фильтра
    a_z = np.poly(z_poles).real
    b_z = np.poly(z_zeros).real
    b_z = b_z * np.sum(a_z)/np.sum(b_z)

    return b_z, a_z


b_z, a_z = bilinear_manual(b_s, a_s, fd)
print("\nЦифровой фильтр H(z):")
print("b =", np.round(b_z, 6))
print("a =", np.round(a_z, 6))


# Вывод диаграммы нулей и полюсов
# Нули и полюса
zeros = np.roots(b_z)
poles = np.roots(a_z)
plt.scatter(np.real(zeros), np.imag(zeros), marker='o', color='blue', s=80, label='Нули')
plt.scatter(np.real(poles), np.imag(poles), marker='x', color='red', s=80, label='Полюса')

# Единичная окружность
phi = np.linspace(0, 2*np.pi, 500)
plt.plot(np.cos(phi), np.sin(phi), 'k--', label='Единичная окружность')

plt.axhline(0, color='black')  # горизонтальная ось Re
plt.axvline(0, color='black')  # вертикальная ось Im
plt.xlabel('Re')
plt.ylabel('Im')
plt.legend()
plt.title("Диаграмма нулей и полюсов")
plt.grid(True)
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.axis('equal')  # равные масштабы по осям
plt.show()

# АЧХ и ФЧХ
omega = np.linspace(0, np.pi, 1024)
ejw = np.exp(1j*omega)
H = np.polyval(b_z, ejw) / np.polyval(a_z, ejw)
A = np.abs(H)
phi = np.angle(H)
phi = np.unwrap(phi)

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(omega, A)
plt.title("АЧХ")
plt.xlabel("ω, рад")
plt.ylabel("|H(e^{jω})|")
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(omega, phi)
plt.title("ФЧХ")
plt.xlabel("ω, рад")
plt.ylabel("arg(H(e^{jω}))")
plt.grid()
plt.tight_layout()
plt.show()

# Фильтрация цифрового гармонического сигнала
f0 = 1500
N = 64
n_t = np.arange(N)
x = np.sin(2*np.pi*f0*n_t/fd)


# Функция применения фильтра
def apply_filter(b, a, x):
    y = np.zeros_like(x)
    for n_idx in range(len(x)):
        y[n_idx] = b[0]*x[n_idx]
        for i in range(1, len(b)):
            if n_idx - i >= 0:
                y[n_idx] += b[i] * x[n_idx - i]
        for j in range(1, len(a)):
            if n_idx - j >= 0:
                y[n_idx] -= a[j] * y[n_idx - j]
    return y


y = apply_filter(b_z, a_z, x)
plt.figure(figsize=(12,5))
plt.stem(n_t/fd, x, linefmt='C0-', markerfmt='C0o', basefmt=" ", label="Входной сигнал")
plt.stem(n_t/fd, y, linefmt='C1-', markerfmt='C1o', basefmt=" ", label="Выход фильтра")
plt.xlabel("t, с")
plt.ylabel("u[n]")
plt.legend()
plt.grid()
plt.show()
