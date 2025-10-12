import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as patches

# Настройка русских шрифтов для matplotlib
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False


class SignalProcessor:
    """Класс для обработки и преобразования сигналов"""

    def __init__(self, A, A0, f, phi, t_min, t_max, fd, b, code_type='direct'):
        """
        Инициализация параметров сигнала

        Параметры:
        A - амплитуда косинуса, В
        A0 - постоянная составляющая, В
        f - частота сигнала, Гц
        phi - начальная фаза, рад
        t_min - начальное время, с
        t_max - конечное время, с
        fd - частота дискретизации, Гц
        b - разрядность АЦП, бит
        code_type - тип кодирования ('direct', 'inverse', 'complement')
        """
        self.A = A
        self.A0 = A0
        self.f = f
        self.phi = phi
        self.t_min = t_min
        self.t_max = t_max
        self.fd = fd
        self.b = b
        self.code_type = code_type

        # Вычисляемые параметры
        self.Td = 1 / fd  # Период дискретизации
        self.N = 2 ** b  # Количество уровней квантования

        if fd <= 2 * f:
            print(f"ВНИМАНИЕ: Частота дискретизации {fd} Гц не удовлетворяет теореме Найквиста!")
            print(f"Минимальная частота дискретизации должна быть > {2 * f} Гц")

    def analog_signal(self, t):
        """
        Генерация аналогового сигнала
        x(t) = A0 + A*cos(2πft + φ)
        """
        return self.A0 + self.A * np.cos(2 * np.pi * self.f * t + self.phi)

    def generate_time_arrays(self):
        """Генерация массивов времени для аналогового и дискретного сигналов"""
        # Аналоговый сигнал - высокое разрешение для плавной кривой
        t_analog = np.linspace(self.t_min, self.t_max, 1000)

        # Дискретный сигнал - отсчеты через период дискретизации
        num_samples = int((self.t_max - self.t_min) * self.fd) + 1
        t_discrete = np.linspace(self.t_min, self.t_max, num_samples)

        return t_analog, t_discrete

    def discretize_signal(self, t_discrete):
        """Дискретизация сигнала по времени"""
        return self.analog_signal(t_discrete)

    def quantize_signal(self, x_discrete):
        """
        Квантование сигнала по уровню с округлением
        """
        # Определение диапазона сигнала
        x_max = max(np.max(x_discrete), self.A0 + self.A)
        x_min = min(np.min(x_discrete), self.A0 - self.A)

        # Шаг квантования
        q = (x_max - x_min) / (self.N - 1)

        # Уровни квантования
        levels = np.linspace(x_min, x_max, self.N)

        # Квантование с округлением
        x_quantized = np.zeros_like(x_discrete)
        for i, x in enumerate(x_discrete):
            # Находим ближайший уровень квантования
            idx = np.argmin(np.abs(levels - x))
            x_quantized[i] = levels[idx]

        return x_quantized, levels, q

    def encode_signal(self, x_quantized, levels):
        """
        Цифровое кодирование квантованного сигнала
        """
        # Создание массива индексов уровней
        codes = np.arange(-self.N // 2, self.N // 2)

        # Поиск соответствующих кодов для каждого квантованного значения
        digital_codes = np.zeros(len(x_quantized), dtype=int)

        for i, x in enumerate(x_quantized):
            # Находим индекс ближайшего уровня
            level_idx = np.argmin(np.abs(levels - x))
            digital_codes[i] = codes[level_idx]

        # Преобразование в выбранный тип кода
        if self.code_type == 'direct':
            encoded = self._direct_code(digital_codes)
        elif self.code_type == 'inverse':
            encoded = self._inverse_code(digital_codes)
        elif self.code_type == 'complement':
            encoded = self._complement_code(digital_codes)
        else:
            raise ValueError("Неизвестный тип кодирования")

        return digital_codes, encoded

    def _direct_code(self, codes):
        """Прямой код"""
        result = []
        for code in codes:
            if code >= 0:
                binary = format(code, f'0{self.b}b')
            else:
                binary = '1' + format(abs(code), f'0{self.b - 1}b')
            result.append(binary)
        return result

    def _inverse_code(self, codes):
        """Обратный код"""
        result = []
        for code in codes:
            if code >= 0:
                binary = format(code, f'0{self.b}b')
            else:
                # Инвертируем все биты положительного числа
                positive_binary = format(abs(code), f'0{self.b - 1}b')
                inverted = ''.join('1' if bit == '0' else '0' for bit in positive_binary)
                binary = '1' + inverted
            result.append(binary)
        return result

    def _complement_code(self, codes):
        """Дополнительный код"""
        result = []
        for code in codes:
            if code >= 0:
                binary = format(code, f'0{self.b}b')
            else:
                # Дополнительный код = 2^b - |code|
                complement_value = 2 ** self.b + code
                binary = format(complement_value, f'0{self.b}b')
            result.append(binary)
        return result

    def calculate_quantization_error(self, x_discrete, x_quantized):
        """Вычисление абсолютной погрешности квантования"""
        return x_quantized - x_discrete

    def plot_all_signals(self):
        """Построение всех графиков сигналов"""
        # Генерация временных массивов
        t_analog, t_discrete = self.generate_time_arrays()

        # Генерация сигналов
        x_analog = self.analog_signal(t_analog)
        x_discrete = self.discretize_signal(t_discrete)
        x_quantized, levels, q = self.quantize_signal(x_discrete)
        digital_codes, encoded_signal = self.encode_signal(x_quantized, levels)

        # Вычисление погрешности
        error = self.calculate_quantization_error(x_discrete, x_quantized)

        # Создание фигуры с подграфиками
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Лабораторная работа №3: Непрерывные, дискретные и цифровые сигналы',
                     fontsize=16, fontweight='bold')

        # 1. Аналоговый сигнал
        axes[0, 0].plot(t_analog, x_analog, 'b-', linewidth=2, label='Аналоговый сигнал')
        axes[0, 0].set_title('Аналоговый сигнал')
        axes[0, 0].set_xlabel('Время t, с')
        axes[0, 0].set_ylabel('Сигнал x(t), В')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()

        # 2. Дискретный сигнал
        axes[0, 1].plot(t_analog, x_analog, 'b-', linewidth=1, alpha=0.5, label='Аналоговый')
        axes[0, 1].stem(t_discrete, x_discrete, linefmt='r-', markerfmt='ro',
                        basefmt=' ', label='Дискретный сигнал')
        axes[0, 1].set_title('Дискретный сигнал')
        axes[0, 1].set_xlabel('Время t, с')
        axes[0, 1].set_ylabel('Сигнал x[n], В')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()

        # 3. Квантованный сигнал
        axes[0, 2].plot(t_analog, x_analog, 'b-', linewidth=1, alpha=0.3, label='Аналоговый')
        axes[0, 2].stem(t_discrete, x_quantized, linefmt='g-', markerfmt='gs',
                        basefmt=' ', label='Квантованный сигнал')

        # Добавляем уровни квантования
        for level in levels:
            axes[0, 2].axhline(y=level, color='gray', linestyle='--', alpha=0.5)

        axes[0, 2].set_title('Квантованный сигнал')
        axes[0, 2].set_xlabel('Время t, с')
        axes[0, 2].set_ylabel('Сигнал xₖ[n], В')
        axes[0, 2].grid(True, alpha=0.3)
        axes[0, 2].legend()

        # 4. Цифровой сигнал
        axes[1, 0].plot(t_analog, x_analog, 'b-', linewidth=1, alpha=0.3, label='Аналоговый')
        axes[1, 0].stem(t_discrete, x_quantized, linefmt='m-', markerfmt='ms',
                        basefmt=' ', label='Цифровой сигнал')

        # Добавляем коды на оси Y
        y_ticks = levels
        y_labels = [f'{encoded_signal[i]} ({digital_codes[i]})'
                    for i in range(len(levels))]
        axes[1, 0].set_yticks(y_ticks)
        axes[1, 0].set_yticklabels(y_labels, fontsize=8)

        axes[1, 0].set_title(f'Цифровой сигнал ({self.code_type} код)')
        axes[1, 0].set_xlabel('Время t, с')
        axes[1, 0].set_ylabel('Код')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()

        # 5. Погрешность квантования
        axes[1, 1].stem(t_discrete, error, linefmt='orange', markerfmt='o',
                        basefmt=' ', label='Погрешность квантования')
        axes[1, 1].axhline(y=q / 2, color='red', linestyle='--',
                           label=f'Макс. погрешность = ±{q / 2:.3f}')
        axes[1, 1].axhline(y=-q / 2, color='red', linestyle='--')
        axes[1, 1].set_title('Абсолютная погрешность квантования')
        axes[1, 1].set_xlabel('Время t, с')
        axes[1, 1].set_ylabel('Погрешность ε[n], В')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()

        # 6. Гистограмма распределения погрешности
        axes[1, 2].hist(error, bins=15, density=True, alpha=0.7, color='orange',
                        edgecolor='black', label='Экспериментальная')

        # Теоретическое равномерное распределение
        theoretical_height = 1 / q
        axes[1, 2].axhline(y=theoretical_height, color='red', linestyle='--',
                           linewidth=2, label='Теоретическая')

        axes[1, 2].set_title('Распределение погрешности квантования')
        axes[1, 2].set_xlabel('Погрешность ε, В')
        axes[1, 2].set_ylabel('Плотность вероятности')
        axes[1, 2].grid(True, alpha=0.3)
        axes[1, 2].legend()

        plt.tight_layout()
        plt.show()

        # Вывод статистики
        self.print_statistics(q, error)

    def print_statistics(self, q, error):
        """Вывод статистических характеристик"""
        print("\n" + "=" * 60)
        print("СТАТИСТИЧЕСКИЕ ХАРАКТЕРИСТИКИ СИГНАЛА")
        print("=" * 60)
        print(f"Параметры сигнала:")
        print(f"  Амплитуда A = {self.A} В")
        print(f"  Постоянная составляющая A₀ = {self.A0} В")
        print(f"  Частота f = {self.f} Гц")
        print(f"  Начальная фаза φ = {self.phi} рад = {self.phi * 180 / np.pi:.1f}°")
        print(f"  Временной интервал: [{self.t_min}, {self.t_max}] с")

        print(f"\nПараметры дискретизации и квантования:")
        print(f"  Частота дискретизации fₐ = {self.fd} Гц")
        print(f"  Период дискретизации Tₐ = {self.Td} с")
        print(f"  Разрядность АЦП b = {self.b} бит")
        print(f"  Количество уровней квантования N = {self.N}")
        print(f"  Шаг квантования q = {q:.4f} В")
        print(f"  Тип кодирования: {self.code_type}")

        print(f"\nСтатистика погрешности квантования:")
        print(f"  Теоретическая максимальная погрешность = ±{q / 2:.4f} В")
        print(f"  Экспериментальная максимальная погрешность = ±{np.max(np.abs(error)):.4f} В")
        print(f"  Теоретическая дисперсия = {q ** 2 / 12:.6f} В²")
        print(f"  Экспериментальная дисперсия = {np.var(error):.6f} В²")
        print(f"  Среднее значение погрешности = {np.mean(error):.6f} В")
        print(f"  СКО погрешности = {np.std(error):.6f} В")

        # Проверка теоремы Найквиста-Котельникова
        nyquist_freq = 2 * self.f
        print(f"\nПроверка теоремы Найквиста-Котельникова:")
        print(f"  Минимальная частота дискретизации = {nyquist_freq} Гц")
        print(f"  Используемая частота дискретизации = {self.fd} Гц")

        if self.fd > nyquist_freq:
            print(f"   Условие выполнено (fₐ > 2fₘₐₓ)")
        else:
            print(f"   УСЛОВИЕ НЕ ВЫПОЛНЕНО! Возможны искажения сигнала.")


def main():
    """Основная функция программы"""

    print("Лабораторная работа №1")
    print("Непрерывные, дискретные и цифровые сигналы")
    print("=" * 60)

    # Параметры моего варианта
    # t_min = 17 с; t_max = 48 с; A = 5 В; A0 = 6 В; f = 3 Гц; φ = π/3; Код: прямой

    A = 7  # Амплитуда, В
    A0 = 1  # Постоянная составляющая, В
    f = 8  # Частота, Гц
    phi = 4 # Начальная фаза, рад
    t_min = 18  # Начальное время, с
    t_max = 41  # Конечное время, с
    fd = 100  # Частота дискретизации, Гц
    b = 8  # Разрядность АЦП, бит
    code_type = 'direct'  # Тип кодирования

    # Создание экземпляра обработчика сигналов
    processor = SignalProcessor(A, A0, f, phi, t_min, t_max, fd, b, code_type)

    # Построение всех графиков и вывод статистики
    processor.plot_all_signals()


if __name__ == "__main__":
    main()
