import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, lfilter, sawtooth

# Параметры для варианта 5
variant = 5


def task_2_2_1():
    """Задание 2.2.1 - Нахождение коэффициентов фильтра"""
    # Для варианта 5 используем блок-схему с параметрами из таблицы 2.2
    a1 = 0.06797
    a2 = 1.53449
    b0 = 0.67549
    b1 = 0.05196
    b2 = 1.35097

    # Коэффициенты передаточной функции H(z) = (b0 + b1*z^-1 + b2*z^-2) / (1 + a1*z^-1 + a2*z^-2)
    b = [b0, b1, b2]  # коэффициенты числителя
    a = [1, a1, a2]  # коэффициенты знаменателя

    # Находим нули и полюса
    zeros = np.roots(b)
    poles = np.roots(a)

    print("2.2.1 — Коэффициенты фильтра (вариант 5):")
    print(f"b = {b}")
    print(f"a = {a}")
    print(f"Нули: {zeros}")
    print(f"Полюса: {poles}")

    # Проверка устойчивости
    stable = all(np.abs(poles) < 1)
    print(f"Фильтр устойчив: {stable}")

    return b, a, zeros, poles


def difference_equation(b, a, x):
    """Функция разностного уравнения (аналог filter в Matlab)"""
    # Используем scipy.signal.lfilter для точного расчета
    return lfilter(b, a, x)


def task_2_2_2(b, a):
    """Задание 2.2.2 - Импульсная характеристика фильтра"""
    N = 64
    x = np.zeros(N)
    x[0] = 1  # Единичный импульс

    # Используем нашу функцию
    y_custom = difference_equation(b, a, x)

    # Сравниваем с scipy.signal.lfilter
    y_scipy = lfilter(b, a, x)

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.stem(range(N), y_custom, linefmt='b-', markerfmt='bo', basefmt='r-')
    plt.title("2.2.2 — Импульсная характеристика фильтра")
    plt.xlabel("n")
    plt.ylabel("h[n]")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.stem(range(N), y_scipy, linefmt='g-', markerfmt='go', basefmt='r-')
    plt.title("Сравнение с scipy.signal.lfilter")
    plt.xlabel("n")
    plt.ylabel("h[n]")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Проверка совпадения
    diff = np.max(np.abs(y_custom - y_scipy))
    print(f"Максимальное расхождение с scipy.signal.lfilter: {diff:.2e}")

    return y_custom


def task_2_2_3(b, a, y_custom):
    """Задание 2.2.3 - Собственные частоты импульсной характеристики"""
    # Находим корни характеристического полинома
    poles = np.roots(a)
    p1, p2 = poles

    print(f"2.2.3 — Собственные частоты:")
    print(f"p1 = {p1:.6f}")
    print(f"p2 = {p2:.6f}")

    # Находим коэффициенты α и β из системы уравнений
    # h[0] = α + β
    # h[1] = α*p1 + β*p2
    h0 = y_custom[0]
    h1 = y_custom[1]

    A = np.array([[1, 1], [p1, p2]])
    b_vec = np.array([h0, h1])

    try:
        alpha, beta = np.linalg.solve(A, b_vec)

        # Моделируем импульсную характеристику по формуле (2.4)
        n = np.arange(len(y_custom))
        h_model = alpha * (p1 ** n) + beta * (p2 ** n)

        plt.figure(figsize=(10, 6))
        plt.stem(n, y_custom, 'b', label='Импульсная характеристика из 2.2.2', markerfmt='bo')
        plt.stem(n, h_model, 'r', label='Модель: αp₁ⁿ + βp₂ⁿ', markerfmt='rx')
        plt.title("2.2.3 — Сравнение импульсных характеристик")
        plt.xlabel("n")
        plt.ylabel("h[n]")
        plt.legend()
        plt.grid(True)
        plt.show()

        print(f"α = {alpha:.6f}")
        print(f"β = {beta:.6f}")

        # Ошибка аппроксимации
        error = np.sqrt(np.mean((y_custom - h_model) ** 2))
        print(f"Среднеквадратичная ошибка аппроксимации: {error:.2e}")

    except np.linalg.LinAlgError:
        print("Система уравнений вырождена")

def task_2_2_4(b, a):
    """Задание 2.2.4 - Отклик на единичный скачок"""
    N = 100
    n0 = variant  # Для варианта 5: n0 = 5

    x = np.zeros(N)
    x[n0:] = 1  # Единичный скачок, начинающийся с n0

    y = difference_equation(b, a, x)

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.stem(range(N), x, 'r', label=f'Вход: u(n-{n0})')
    plt.title("2.2.4 — Входной сигнал (единичный скачок)")
    plt.xlabel("n")
    plt.ylabel("x[n]")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.stem(range(N), y, 'g', label='Выход фильтра')
    plt.axhline(y=y[-1], color='k', linestyle='--', label=f'Установившееся значение: {y[-1]:.4f}')
    plt.title("Отклик фильтра на единичный скачок")
    plt.xlabel("n")
    plt.ylabel("y[n]")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    print(f"2.2.4 — Установившееся значение: {y[-1]:.6f}")


def task_2_2_5(b, a):
    """Задание 2.2.5 - Отклик на пилообразные сигналы"""
    # Для варианта 5: пилообразные сигналы 20 Гц и 110 Гц, Fs = 440 Гц
    fs = 440
    duration = 0.1  # 100 мс

    t = np.arange(0, duration, 1 / fs)

    # Пилообразные сигналы
    x1 = sawtooth(2 * np.pi * 20 * t, width=0.5)  # Симметричный пилообразный
    x2 = sawtooth(2 * np.pi * 110 * t, width=0.5)

    y1 = difference_equation(b, a, x1)
    y2 = difference_equation(b, a, x2)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(t, x1, 'b', label='Вход 20 Гц')
    plt.title("Входной сигнал 20 Гц")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(t, y1, 'r', label='Выход 20 Гц')
    plt.title("Выходной сигнал 20 Гц")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(t, x2, 'b', label='Вход 110 Гц')
    plt.title("Входной сигнал 110 Гц")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(t, y2, 'r', label='Выход 110 Гц')
    plt.title("Выходной сигнал 110 Гц")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid(True)

    plt.suptitle("2.2.5 — Отклик на пилообразные сигналы (вариант 5)")
    plt.tight_layout()
    plt.show()


def task_2_2_6(b, a):
    """Задание 2.2.6 - Расчет АЧХ и ФЧХ по формуле"""
    M = len(b) - 1  # Порядок фильтра

    # Вычисление частотной характеристики
    omega = np.linspace(0, np.pi, 1000)

    # Вычисляем числитель и знаменатель
    numerator = np.zeros_like(omega, dtype=complex)
    denominator = np.zeros_like(omega, dtype=complex)

    for k in range(M + 1):
        numerator += b[k] * np.exp(-1j * omega * k)

    for k in range(1, M + 1):
        denominator += a[k] * np.exp(-1j * omega * k)

    denominator = 1 + denominator

    H = numerator / denominator

    A = np.abs(H)  # АЧХ
    phi = np.angle(H)  # ФЧХ

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(omega, A)
    plt.title("2.2.6 — Амплитудно-частотная характеристика")
    plt.xlabel("ω, рад/отсчет")
    plt.ylabel("|H(e^{jω})|")
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(omega, phi)
    plt.title("2.2.6 — Фазо-частотная характеристика")
    plt.xlabel("ω, рад/отсчет")
    plt.ylabel("arg(H(e^{jω})), рад")
    plt.grid(True)

    # Сравнение с scipy.signal.freqz
    w_scipy, H_scipy = freqz(b, a, worN=1000)
    A_scipy = np.abs(H_scipy)
    phi_scipy = np.angle(H_scipy)

    plt.subplot(2, 2, 3)
    plt.plot(w_scipy, A_scipy, 'r--', label='scipy.freqz')
    plt.plot(omega, A, 'b-', label='Наш расчет', alpha=0.7)
    plt.title("Сравнение АЧХ")
    plt.xlabel("ω, рад/отсчет")
    plt.ylabel("|H(e^{jω})|")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(w_scipy, phi_scipy, 'r--', label='scipy.freqz')
    plt.plot(omega, phi, 'b-', label='Наш расчет', alpha=0.7)
    plt.title("Сравнение ФЧХ")
    plt.xlabel("ω, рад/отсчет")
    plt.ylabel("arg(H(e^{jω})), рад")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def task_2_2_7(b, a):
    """Задание 2.2.7 - АЧХ и ФЧХ с помощью freqz"""
    w, H = freqz(b, a, worN=1000)

    A = np.abs(H)
    phi = np.angle(H)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(w, A)
    plt.title("2.2.7 — АЧХ (scipy.signal.freqz)")
    plt.xlabel("ω, рад/отсчет")
    plt.ylabel("|H(e^{jω})|")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(w, phi)
    plt.title("2.2.7 — ФЧХ (scipy.signal.freqz)")
    plt.xlabel("ω, рад/отсчет")
    plt.ylabel("arg(H(e^{jω})), рад")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    print(f"Лабораторная работа №2 'Разностные уравнения' - Вариант {variant}")
    print("=" * 60)

    # Выполняем задания по порядку
    b, a, zeros, poles = task_2_2_1()
    print()

    y_custom = task_2_2_2(b, a)
    print()

    task_2_2_3(b, a, y_custom)
    print()

    task_2_2_4(b, a)
    print()

    task_2_2_5(b, a)
    print()

    task_2_2_6(b, a)
    print()

    task_2_2_7(b, a)

    print("Все задания выполнены!")


if __name__ == "__main__":
    main()