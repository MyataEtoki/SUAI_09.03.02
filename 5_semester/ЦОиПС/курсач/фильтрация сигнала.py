import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

# === Шаг 1: Получение коэффициентов фильтра (как в п.4) ===
N = 16
Fs = N * 1e3
f1 = 0.3 * N * 1e3
f2_eff = Fs - 0.6 * N * 1e3  # 6.4 кГц

# Аналоговый прототип
n = 4
w1 = 2 * np.pi * f1
w2 = 2 * np.pi * f2_eff
b_analog, a_analog = signal.butter(n, [w1, w2], btype='bandstop', analog=True)

# Цифровой фильтр через билинейное преобразование
b, a = signal.bilinear(b_analog, a_analog, fs=Fs)
b = b / a[0]  # нормировка
a = a / a[0]

# Убедимся, что a[0] = 1
assert np.isclose(a[0], 1.0), "a[0] должен быть равен 1"

print("Коэффициенты фильтра:")
print("b =", b)
print("a =", a)

# === Шаг 2: Считывание входного сигнала ===
Fs, x = wavfile.read('закусочная-сосисочная-3.wav')
x = x.astype(np.float64)
if x.ndim > 1:
    x = x[:, 0]  # моно
t = np.arange(len(x)) / Fs


# === Шаг 3: Собственная реализация фильтрации (каноническая форма) ===
def butterworth_filter(x, b, a):
    """
    Реализация IIR-фильтра по разностному уравнению.
    x — входной сигнал (массив)
    b, a — коэффициенты (a[0] = 1)
    """
    N = len(x)
    M = len(b) - 1
    K = len(a) - 1
    y = np.zeros_like(x)

    # Цикл по отсчётам
    for n in range(N):
        # Часть с x[n-k]
        acc = 0.0
        for k in range(M + 1):
            if n - k >= 0:
                acc += b[k] * x[n - k]
        # Часть с y[n-k]
        for k in range(1, K + 1):
            if n - k >= 0:
                acc -= a[k] * y[n - k]
        y[n] = acc
    return y


# Фильтрация
y_custom = butterworth_filter(x, b, a)

# Для проверки — используем scipy
y_scipy = signal.lfilter(b, a, x)

# Проверка совпадения
print("\nМаксимальное отклонение от scipy.lfilter:", np.max(np.abs(y_custom - y_scipy)))
# === Шаг 4: Визуализация входного и выходного сигналов ===
T = int(Fs * 0.010)  # 20 миллисекунд → 320 отсчётов

plt.figure(figsize=(10, 5))

# Входной сигнал
plt.plot(2, 1, 1)
plt.stem(t[:T] * 1000, x[:T], linefmt='C0-', markerfmt='C0o', basefmt=" ")
plt.title(f'Входной сигнал (первые {T} отсчётов, {T/Fs*1000:.1f} мс)')
plt.ylabel('x[n]')
plt.grid(True, linestyle='--', alpha=0.6)

plt.figure(figsize=(10, 5))
# Выходной сигнал
plt.plot(2, 1, 2)
plt.stem(t[:T] * 1000, y_custom[:T], linefmt='C1-', markerfmt='C1s', basefmt=" ")
plt.title('Выходной сигнал после фильтрации')
plt.xlabel('Время, мс')
plt.ylabel('y[n]')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

