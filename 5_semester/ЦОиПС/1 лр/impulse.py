import numpy as np
import matplotlib.pyplot as plt

def create_impulse(n=20):
    # Создаем импульс
    impulse = np.zeros(n)
    impulse[0] = 1

    # Визуализируем
    plt.stem(range(n), impulse)
    plt.title(f'Единичный импульс ({n} отсчетов)')
    plt.xlabel('Отсчеты')
    plt.ylabel('Амплитуда')
    plt.grid(True)
    plt.show()

create_impulse()