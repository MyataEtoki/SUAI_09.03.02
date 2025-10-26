"""
Лабораторная работа №4: Разностные уравнения
Вариант 5
Автор: студент группы

Параметры варианта 5:
a1 = 0.06797, a2 = 0.67549, b0 = 0.05196, b1 = 1.35097, b2 = 0 (отсутствует)
Пилообразный сигнал с частотами 20 Гц и 110 Гц, fs = 440 Гц
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

# Настройка matplotlib для корректного отображения русского текста
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

class DigitalFilter:
    """Класс для работы с цифровыми фильтрами"""
    
    def __init__(self, b_coeffs, a_coeffs):
        """
        Инициализация фильтра
        b_coeffs: коэффициенты прямой связи
        a_coeffs: коэффициенты обратной связи
        """
        self.b = np.array(b_coeffs)
        self.a = np.array(a_coeffs)
        
    def difference_equation_filter(self, x):
        """
        Реализация разностного уравнения (задание 2.2.2)
        Собственная реализация фильтра без использования встроенных функций
        """
        N = len(x)
        y = np.zeros(N)
        
        # Буферы для хранения предыдущих значений
        x_buf = np.zeros(len(self.b))
        y_buf = np.zeros(len(self.a))
        
        for n in range(N):
            # Сдвигаем буферы
            x_buf[1:] = x_buf[:-1]
            x_buf[0] = x[n]
            
            y_buf[1:] = y_buf[:-1]
            
            # Вычисляем выходной отсчет согласно разностному уравнению
            # y(n) = sum(b_i * x(n-i)) - sum(a_i * y(n-i))
            y_val = 0
            
            # Прямая связь
            for i in range(len(self.b)):
                y_val += self.b[i] * x_buf[i]
            
            # Обратная связь (начинаем с a1, так как a0 = 1)
            for i in range(1, len(self.a)):
                if i < len(y_buf):
                    y_val -= self.a[i] * y_buf[i]
            
            y[n] = y_val
            y_buf[0] = y[n]
            
        return y
    
    def get_transfer_function(self):
        """Получение передаточной функции H(z)"""
        return signal.TransferFunction(self.b, self.a, dt=True)
    
    def get_poles_zeros(self):
        """Получение полюсов и нулей"""
        tf = self.get_transfer_function()
        return tf.poles, tf.zeros
    
    def impulse_response(self, N=64):
        """Импульсная характеристика"""
        delta = np.zeros(N)
        delta[0] = 1.0
        return self.difference_equation_filter(delta)
    
    def step_response(self, N=100, n0=5):
        """Переходная характеристика - отклик на единичный скачок"""
        step = np.zeros(N)
        step[n0:] = 1.0
        return self.difference_equation_filter(step), step
    
    def frequency_response(self, w):
        """Частотная характеристика H(e^jw)"""
        # H(e^jw) = sum(b_k * e^(-jwk)) / (1 + sum(a_k * e^(-jwk)))
        numerator = np.zeros(len(w), dtype=complex)
        denominator = np.ones(len(w), dtype=complex)
        
        # Числитель
        for k in range(len(self.b)):
            numerator += self.b[k] * np.exp(-1j * w * k)
        
        # Знаменатель
        for k in range(1, len(self.a)):
            denominator += self.a[k] * np.exp(-1j * w * k)
        
        H = numerator / denominator
        return H

def generate_sawtooth_signal(freq, fs, duration=1.0):
    """Генерация пилообразного сигнала"""
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    # Пилообразный сигнал: линейно возрастающий от -1 до 1
    signal_val = 2 * (t * freq - np.floor(t * freq + 0.5))
    return t, signal_val

def analyze_eigenfrequencies(poles):
    """Анализ собственных частот (задание 2.2.3)"""
    print("\n=== Задание 2.2.3: Собственные частоты ===")
    print(f"Полюсы системы: {poles}")
    
    # Для системы второго порядка импульсная характеристика имеет вид:
    # h(n) = (α * p1^n + β * p2^n) * u(n)
    p1, p2 = poles[0], poles[1]
    
    # Составляем систему уравнений для нахождения α и β
    # h(0) = α + β
    # h(1) = α * p1 + β * p2
    
    return p1, p2

def solve_coefficients(h0, h1, p1, p2):
    """Решение системы уравнений для нахождения α и β"""
    # Система: h(0) = α + β
    #         h(1) = α * p1 + β * p2
    A = np.array([[1, 1], [p1, p2]])
    b = np.array([h0, h1])
    
    # Решение с помощью оператора backslash
    coeffs = np.linalg.solve(A, b)
    alpha, beta = coeffs[0], coeffs[1]
    
    return alpha, beta

def theoretical_impulse_response(alpha, beta, p1, p2, n_values):
    """Теоретическая импульсная характеристика по формуле (2.4)"""
    h_theory = np.zeros(len(n_values))
    for i, n in enumerate(n_values):
        if n >= 0:
            h_theory[i] = alpha * (p1**n) + beta * (p2**n)
    return h_theory

def main():
    """Основная функция для выполнения всех заданий"""
    
    print("=== Лабораторная работа №4: Разностные уравнения ===")
    print("Вариант 5")
    print("Параметры: a1=0.06797, a2=0.67549, b0=0.05196, b1=1.35097, b2=0")
    
    # Задание 2.2.1: Определение коэффициентов фильтра
    print("\n=== Задание 2.2.1: Коэффициенты фильтра ===")

    # Корректные параметры для варианта 5 (таблица 2.2)
    a1, a2 = 0.06797, 1.53449
    b0, b1, b2 = 0.67549, 0.05196, 1.35097
    
    # Формирование векторов коэффициентов
    b_coeffs = [b0, b1, b2]  # коэффициенты прямой связи
    a_coeffs = [1, a1, a2]   # коэффициенты обратной связи (a0 = 1)
    
    print(f"Коэффициенты прямой связи b: {b_coeffs}")
    print(f"Коэффициенты обратной связи a: {a_coeffs}")
    
    # Создание объекта фильтра
    filter_obj = DigitalFilter(b_coeffs, a_coeffs)
    
    # Получение передаточной функции
    tf = filter_obj.get_transfer_function()
    print(f"\nПередаточная функция:")
    print(f"Числитель: {tf.num}")
    print(f"Знаменатель: {tf.den}")
    
    # Получение полюсов и нулей
    poles, zeros = filter_obj.get_poles_zeros()
    print(f"\nПолюсы: {poles}")
    print(f"Нули: {zeros}")
    
    # Проверка стабильности
    is_stable = np.all(np.abs(poles) < 1.0)
    print(f"Система стабильна: {is_stable}")
    
    # Задание 2.2.2: Импульсная характеристика
    print("\n=== Задание 2.2.2: Импульсная характеристика ===")
    
    N = 64
    h_custom = filter_obj.impulse_response(N)
    
    # Сравнение с встроенной функцией filter
    delta = np.zeros(N)
    delta[0] = 1.0
    h_scipy = signal.lfilter(b_coeffs, a_coeffs, delta)
    
    # Проверка совпадения результатов
    diff = np.max(np.abs(h_custom - h_scipy))
    print(f"Максимальная разность между собственной и встроенной функцией: {diff:.2e}")
    
    # Задание 2.2.3: Собственные частоты
    p1, p2 = analyze_eigenfrequencies(poles)
    
    # Вычисление коэффициентов α и β
    h0, h1 = h_custom[0], h_custom[1]
    alpha, beta = solve_coefficients(h0, h1, p1, p2)
    
    print(f"Коэффициент α: {alpha}")
    print(f"Коэффициент β: {beta}")
    
    # Построение теоретической импульсной характеристики
    n_vals = np.arange(N)
    h_theory = theoretical_impulse_response(alpha, beta, p1, p2, n_vals)
    
    # Проверка совпадения
    theory_diff = np.max(np.abs(h_custom - h_theory))
    print(f"Разность между практической и теоретической h(n): {theory_diff:.2e}")
    
    # Задание 2.2.4: Переходная характеристика
    print("\n=== Задание 2.2.4: Переходная характеристика ===")
    
    N_step = 200
    n0 = 5  # номер варианта
    y_step, x_step = filter_obj.step_response(N_step, n0)
    
    # Определение установившегося значения
    steady_state = y_step[-20:].mean()  # среднее значение последних 20 отсчетов
    print(f"Установившееся значение фильтра: {steady_state:.6f}")
    
    # Задание 2.2.5: Отклик на пилообразные сигналы
    print("\n=== Задание 2.2.5: Отклик на пилообразные сигналы ===")
    
    fs = 440  # Частота дискретизации
    f1, f2 = 20, 110  # Частоты сигналов
    duration = 0.2  # Длительность сигнала
    
    # Генерация пилообразных сигналов
    t1, saw1 = generate_sawtooth_signal(f1, fs, duration)
    t2, saw2 = generate_sawtooth_signal(f2, fs, duration)
    
    # Отклик фильтра на сигналы
    y_saw1 = filter_obj.difference_equation_filter(saw1)
    y_saw2 = filter_obj.difference_equation_filter(saw2)
    
    print(f"Обработан пилообразный сигнал {f1} Гц")
    print(f"Обработан пилообразный сигнал {f2} Гц")
    
    # Задание 2.2.6: Частотная характеристика
    print("\n=== Задание 2.2.6: Частотная характеристика ===")
    
    # Частотный диапазон от 0 до π
    w = np.linspace(0, np.pi, 512)
    H = filter_obj.frequency_response(w)
    
    # АЧХ и ФЧХ
    A_w = np.abs(H)  # Амплитудно-частотная характеристика
    phi_w = np.angle(H)  # Фазо-частотная характеристика
    
    print(f"Построена частотная характеристика в диапазоне 0...π")
    
    # Задание 2.2.7: Построение графиков
    print("\n=== Задание 2.2.7: Построение графиков ===")
    
    # Создание фигуры с подграфиками
    fig = plt.figure(figsize=(15, 12))
    
    # 1. Импульсная характеристика
    plt.subplot(3, 3, 1)
    n_plot = np.arange(32)  # Показываем первые 32 отсчета
    plt.stem(n_plot, h_custom[:32], basefmt=' ')
    plt.title('Импульсная характеристика h(n)')
    plt.xlabel('n')
    plt.ylabel('h(n)')
    plt.grid(True)
    
    # 2. Сравнение собственной и встроенной функции
    plt.subplot(3, 3, 2)
    plt.plot(n_plot, h_custom[:32], 'b-', label='Собственная функция')
    plt.plot(n_plot, h_scipy[:32], 'r--', label='scipy.signal.lfilter')
    plt.title('Сравнение функций фильтрации')
    plt.xlabel('n')
    plt.ylabel('h(n)')
    plt.legend()
    plt.grid(True)
    
    # 3. Теоретическая импульсная характеристика
    plt.subplot(3, 3, 3)
    plt.plot(n_plot, h_custom[:32], 'b-', label='Практическая')
    plt.plot(n_plot, h_theory[:32], 'r--', label='Теоретическая')
    plt.title('Сравнение с теорией')
    plt.xlabel('n')
    plt.ylabel('h(n)')
    plt.legend()
    plt.grid(True)
    
    # 4. Переходная характеристика
    plt.subplot(3, 3, 4)
    n_step_plot = np.arange(len(y_step))
    plt.plot(n_step_plot, x_step, 'g-', label='Вход (единичный скачок)')
    plt.plot(n_step_plot, y_step, 'b-', label='Выход фильтра')
    plt.axhline(y=steady_state, color='r', linestyle='--', label=f'Установившееся: {steady_state:.3f}')
    plt.title('Переходная характеристика')
    plt.xlabel('n')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)
    
    # 5. Пилообразный сигнал 20 Гц
    plt.subplot(3, 3, 5)
    plt.plot(t1[:200], saw1[:200], 'g-', label=f'Вход {f1} Гц')
    plt.plot(t1[:200], y_saw1[:200], 'b-', label='Выход фильтра')
    plt.title(f'Отклик на пилообразный {f1} Гц')
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)
    
    # 6. Пилообразный сигнал 110 Гц
    plt.subplot(3, 3, 6)
    plt.plot(t2[:200], saw2[:200], 'g-', label=f'Вход {f2} Гц')
    plt.plot(t2[:200], y_saw2[:200], 'b-', label='Выход фильтра')
    plt.title(f'Отклик на пилообразный {f2} Гц')
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)
    
    # 7. АЧХ
    plt.subplot(3, 3, 7)
    plt.plot(w/np.pi, A_w)
    plt.title('Амплитудно-частотная характеристика')
    plt.xlabel('Нормированная частота (×π рад/отсчет)')
    plt.ylabel('|H(e^jω)|')
    plt.grid(True)
    
    # 8. ФЧХ
    plt.subplot(3, 3, 8)
    plt.plot(w/np.pi, phi_w)
    plt.title('Фазо-частотная характеристика')
    plt.xlabel('Нормированная частота (×π рад/отсчет)')
    plt.ylabel('∠H(e^jω), рад')
    plt.grid(True)
    
    # 9. Диаграмма полюсов и нулей
    plt.subplot(3, 3, 9)
    # Единичная окружность
    theta = np.linspace(0, 2*np.pi, 100)
    plt.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Единичная окружность')
    
    # Полюсы и нули
    plt.plot(np.real(poles), np.imag(poles), 'rx', markersize=10, label='Полюсы')
    plt.plot(np.real(zeros), np.imag(zeros), 'bo', markersize=8, label='Нули')
    
    plt.title('Диаграмма полюсов и нулей')
    plt.xlabel('Действительная часть')
    plt.ylabel('Мнимая часть')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Подведение итогов
    print("\n=== РЕЗУЛЬТАТЫ ЛАБОРАТОРНОЙ РАБОТЫ ===")
    print(f"1. Коэффициенты фильтра определены для варианта 5")
    print(f"2. Разностное уравнение реализовано и проверено")
    print(f"3. Собственные частоты: p1={p1:.6f}, p2={p2:.6f}")
    print(f"4. Коэффициенты: α={alpha:.6f}, β={beta:.6f}")
    print(f"5. Установившееся значение: {steady_state:.6f}")
    print(f"6. Обработаны пилообразные сигналы {f1} Гц и {f2} Гц")
    print(f"7. Построены АЧХ и ФЧХ")
    print(f"8. Система {'стабильна' if is_stable else 'нестабильна'}")

if __name__ == "__main__":
    main()
