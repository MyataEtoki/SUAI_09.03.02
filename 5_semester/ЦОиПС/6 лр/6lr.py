# Выполню все шаги: построю аналоговый прототип Баттерворта (n=8) с предискажением частоты (pre-warp),
# затем применю билинейное преобразование и получу коэффициенты цифрового фильтра,
# построю диаграмму нулей/полюсов, АЧХ/ФЧХ и покажу фильтрацию синусоиды.
# Код сам построит SOS (бикуады) если scipy доступен, иначе выполнит "ручной" разбор на квадратичные секции.
import numpy as np
import matplotlib.pyplot as plt

# Параметры по заданию
n = 8
fs = 8000.0  # частота дискретизации, Гц
fc = 1900.0  # частота среза, Гц

T = 1.0 / fs

# Предискажение частоты (pre-warp) для билинейного преобразования
Omega_c = 2.0 * fs * np.tan(np.pi * fc / fs)  # аналоговая частота среза (рад/с)
# Здесь Omega_c в радианах в единицах 1/s (обычно обозначается просто Ωc)

# Вычислим полюса нормированного Баттерворта и масштабируем их на Omega_c
poles = []
for k in range(1, n+1):
    angle = np.pi * (2*k + n - 1) / (2*n)
    p = Omega_c * np.exp(1j * angle)
    if np.real(p) < 0:  # устойчивые полюса (левая полуплоскость)
        poles.append(p)

poles = np.array(poles)
# Коэффициенты знаменателя a(s) — полином с корнями = полюса
a_s = np.poly(poles).real  # коэффициенты a(s) (в порядке убывания степеней s)
# Числитель для низкочастотного прототипа Баттерворта — константа, чтобы H(0)=1
b_s = np.array([Omega_c**n])

print("Предискаженная аналоговая частота (Omega_c) = {:.6f} рад/с".format(Omega_c))
print("\nАналоговый фильтр H(s):")
print("b(s) =", np.round(b_s,6))
print("a(s) =", np.round(a_s,6))

# Попробуем использовать scipy.signal.bilinear (если доступен) — более точный и удобный способ.
use_scipy = False
try:
    import scipy.signal as sig
    use_scipy = True
except Exception as e:
    use_scipy = False

if use_scipy:
    # scipy ожидает неприведённые коэффициенты (полиномы по s)
    b_z, a_z = sig.bilinear(b_s, a_s, fs)
else:
    # Ручное билинейное преобразование через отображение полюсов и нулей
    # Полюса s->z
    poles_s = np.roots(a_s)
    # Аналоговые нули: у прототипа они в бесконечности (степень числителя < степени знаменателя)
    # При билинейном преобразовании они перейдут в z = -1 (множество нулей у z = -1)
    z_poles = (1.0 + poles_s * T / 2.0) / (1.0 - poles_s * T / 2.0)
    z_zeros = -np.ones(len(z_poles))  # нули в z=-1 (для каждого полюса)
    a_z = np.poly(z_poles).real
    b_z = np.poly(z_zeros).real
    # Масштабируем b_z так, чтобы H(z) при ω=0 совпадала с H(s) при s=0 (обычно 1 для нормированного НЧ)
    # Значение H(z) при z=1: H(1) = sum(b_z)/sum(a_z)
    b_z = b_z * (np.sum(a_z) / np.sum(b_z))

print("\nЦифровой фильтр H(z) (коэффициенты):")
print("b (numerator) =", np.round(b_z, 6))
print("a (denominator) =", np.round(a_z, 6))

# Диаграмма нулей и полюсов
zeros = np.roots(b_z)
poles_d = np.roots(a_z)

plt.figure(figsize=(6,6))
plt.scatter(np.real(zeros), np.imag(zeros), marker='o', label='Нули', s=80)
plt.scatter(np.real(poles_d), np.imag(poles_d), marker='x', label='Полюса', s=80)
phi = np.linspace(0, 2*np.pi, 400)
plt.plot(np.cos(phi), np.sin(phi), 'k--', label='Единичная окружность')
plt.axhline(0, color='black', linewidth=0.6)
plt.axvline(0, color='black', linewidth=0.6)
plt.xlabel('Re')
plt.ylabel('Im')
plt.legend()
plt.title('Диаграмма нулей и полюсов H(z)')
plt.grid(True)
plt.axis('equal')
plt.show()

# Частотная характеристика (АЧХ/ФЧХ) — считаем H(e^{jω}) подстановкой z = e^{jω}
omega = np.linspace(0, np.pi, 2048)
ejw = np.exp(1j * omega)
H = np.polyval(b_z, ejw) / np.polyval(a_z, ejw)
A = np.abs(H)
phi = np.angle(H)
phi = np.unwrap(phi)

plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(omega, 20*np.log10(A + 1e-15))  # АЧХ в дБ
plt.title('АЧХ (H(e^{jω})) — в дБ')
plt.xlabel('ω, рад/с')
plt.ylabel('|H(e^{jω})|, дБ')
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(omega, phi)
plt.title('ФЧХ (phase)')
plt.xlabel('ω, рад/с')
plt.ylabel('arg(H(e^{jω}))')
plt.grid(True)
plt.tight_layout()
plt.show()

# Разбиение на бикуады (2-го порядка) для канонической реализации
# Попробуем scipy.signal.tf2sos, если доступен. Иначе составим вручную, группируя сопряжённые корни.
sos = None
if use_scipy:
    sos = sig.tf2sos(b_z, a_z)
else:
    # ручной разбор на квадраты
    poles_list = list(poles_d)
    zeros_list = list(zeros)
    # Сортируем по действительной части (для группировки сопряжённых)
    used = [False]*len(poles_list)
    sos_list = []
    # Функция для взять пару сопряжённых корней (если есть)
    for i, p in enumerate(poles_list):
        if used[i]:
            continue
        # если корень вещественный — возьмём его и следующий вещественный (или сам +1?), но в нашем случае корни комплексные
        # ищем его сопряжённый
        conj = np.conj(p)
        # Найдём индекс сопряжённого (в пределах tol)
        found = None
        for j in range(i+1, len(poles_list)):
            if not used[j] and np.abs(poles_list[j] - conj) < 1e-6:
                found = j
                break
        if found is None:
            # нет очевидной пары — возьмём его как одиночный (создадим квадратичный с сопряжённым вручную)
            denom = np.poly([p, np.conj(p)]).real
            used[i] = True
        else:
            denom = np.poly([p, poles_list[found]]).real
            used[i] = True
            used[found] = True
        # для числителя возьмём по два нуля (если есть), иначе используем нули в z=-1
        if len(zeros_list) >= 2:
            z0 = zeros_list.pop(0)
            z1 = zeros_list.pop(0)
            numer = np.poly([z0, z1]).real
        elif len(zeros_list) == 1:
            z0 = zeros_list.pop(0)
            numer = np.poly([z0, -1]).real
        else:
            numer = np.poly([-1, -1]).real
        sos_list.append(np.hstack([numer, denom]))
    sos = np.array(sos_list)

print("\nSOS (biquad sections) — каждая строка: [b0 b1 b2 a0 a1 a2] :")
for row in sos:
    print(np.round(row,6))

# Демонстрация фильтрации гармонического сигнала
f0 = 2000.0  # частота синусоиды
N = 256
n_t = np.arange(N)
x = np.sin(2.0 * np.pi * f0 * n_t / fs)

# Реализация фильтрации прямым использованием разностного уравнения
def apply_filter(b, a, x):
    y = np.zeros_like(x, dtype=float)
    NB = len(b)
    NA = len(a)
    for n_idx in range(len(x)):
        # numerator part
        for i in range(NB):
            if n_idx - i >= 0:
                y[n_idx] += b[i] * x[n_idx - i]
        # denominator part (a[0] assumed = 1)
        for j in range(1, NA):
            if n_idx - j >= 0:
                y[n_idx] -= a[j] * y[n_idx - j]
    return y

y = apply_filter(b_z, a_z, x)

plt.figure(figsize=(10,5))
plt.plot(n_t / fs, x, label='Входной сигнал (sin {:.0f} Гц)'.format(f0))
plt.plot(n_t / fs, y, label='Выход фильтра')
plt.xlabel('t, с')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)
plt.title('Фильтрация гармонического сигнала')
plt.show()

# Вывод первых нескольких отсчётов для сравнения
print("\nПервые 16 отсчётов входа и выхода:")
for i in range(16):
    print(f"n={i:2d}: x={x[i]: .6f}, y={y[i]: .6f}")
