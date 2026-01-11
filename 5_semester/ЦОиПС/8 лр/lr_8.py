import matplotlib.pyplot as plt
import numpy as np

# Параметры
U_op = 5.0          # Опорное напряжение (В)
N = 4               # Разрядность АЦП
q = U_op / (2**N)   # Шаг квантования = 0.3125 В
T_clk = 1.0         # Период тактового сигнала (усл. ед.)
U_in = 3.0          # Входное аналоговое напряжение (пример)

# Массив тактов: от 0 до 2^N - 1 (всего 16 значений)
t_ticks = np.arange(0, 2**N) * T_clk          # [0, 1, 2, ..., 15]
U_dac_ticks = np.arange(0, 2**N) * q         # [0, 0.3125, ..., 4.6875]

# Определяем код и момент останова
code = min(int(np.floor(U_in / q)), 2**N - 1)  # Код результата
stop_tick = code + 1                           # Останов происходит на следующем такте
stop_time = stop_tick * T_clk

# Формируем "реалистичный" временной массив для плотного отображения
t_dense = np.linspace(0, 2**N * T_clk, 2000, endpoint=False)

# === Выход ЦАП: ступенчатый + "заморозка" после останова ===
U_dac = np.floor(t_dense / T_clk) * q
# Обрезаем на уровне результата (после останова — не растёт!)
U_dac = np.where(t_dense < stop_time, U_dac, code * q)

# === Тактовый сигнал ===
clock = ((np.floor(t_dense / T_clk) % 2) == 0).astype(int)

# === Выход компаратора ===
# 1 — пока U_ЦАП < U_вх, иначе 0 (но только до момента останова; после — 0)
comparator = np.where(U_dac < U_in, 1, 0)
# После останова — компаратор остаётся в 0 (фиксация результата)
comparator = np.where(t_dense >= stop_time, 0, comparator)

# === Построение графиков ===
fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

# 1. Выход ЦАП
axs[0].step(t_dense, U_dac, where='post', color='r', linewidth=2, label=r'$U_{ЦАП}$')
axs[0].axhline(U_in, color='b', linestyle='-', linewidth=2, label=f'$U_{{вх}} = {U_in}$ В')
axs[0].axvline(stop_time, color='g', linestyle='--', linewidth=2, label='Конец преобразования')
axs[0].set_ylabel('Напряжение, В')
axs[0].set_title('Выход ЦАП (ступенчатый, с фиксацией после останова)')
axs[0].legend(loc='upper left')
axs[0].grid(True, linestyle='--')

# 2. Тактовые импульсы
axs[1].plot(t_dense, clock, color='b', linewidth=2, label='Тактовый сигнал')
axs[1].set_ylabel('Уровень')
axs[1].set_title('Тактовые импульсы')
axs[1].legend(loc='upper left')
axs[1].grid(True, linestyle='--')

# 3. Выход компаратора
axs[2].step(t_dense, comparator, where='post', color='m', linewidth=2, label='Выход компаратора')
axs[2].set_xlabel('Время, усл. ед.')
axs[2].set_ylabel('Уровень')
axs[2].set_title('Выход компаратора')
axs[2].legend(loc='upper left')
axs[2].grid(True, linestyle='--')

plt.tight_layout()
plt.show()