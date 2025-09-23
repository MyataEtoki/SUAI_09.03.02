import numpy as np
import matplotlib.pyplot as plt

def create_fir_impulse_response(order, f_cutoff=0.2):
    """Создает импульсную характеристику КИХ-фильтра"""
    n = np.arange(order)
    impulse = np.sinc(2 * f_cutoff * (n - (order-1)/2))
    impulse *= np.hamming(order)  # применяем оконную функцию
    return impulse

def create_iir_impulse_response(length, alpha=0.2):
    """Создает импульсную характеристику БИХ-фильтра"""
    input_signal = np.zeros(length)
    input_signal[0] = 1
    output = np.zeros(length)

    for n in range(length):
        if n == 0:
            output[n] = alpha * input_signal[n]
        else:
            output[n] = alpha * input_signal[n] + (1 - alpha) * output[n - 1]

    return output

# Параметры
length = 20

# Создаем импульсные характеристики
fir_response = create_fir_impulse_response(length, f_cutoff=0.3)
iir_response = create_iir_impulse_response(length, alpha=0.3)

# Визуализация
plt.figure(figsize=(12, 6))

# КИХ-фильтр
plt.subplot(1, 2, 1)
plt.stem(range(length), fir_response, basefmt="gray")
plt.title('КИХ-фильтр (нерекурсивный)\nИмпульсная характеристика')
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.grid(True)

# БИХ-фильтр
plt.subplot(1, 2, 2)
plt.stem(range(length), iir_response, basefmt="gray")
plt.title('БИХ-фильтр (рекурсивный)\nИмпульсная характеристика')
plt.xlabel('Отсчеты')
plt.ylabel('Амплитуда')
plt.grid(True)

plt.tight_layout()
plt.show()

# Вывод коэффициентов
print("Коэффициенты КИХ-фильтра (b):")
print(fir_response)
print("\nКоэффициенты БИХ-фильтра (рекурсивная часть):")
print(f"a = [1, {- (1 - 0.3):.3f}]")  # для alpha=0.3
print(f"b = [{0.3:.3f}]")

