import numpy as np
import matplotlib.pyplot as plt

# Вариант 3: антисимметричная пилообразная функция
def signal(t, omega=np.pi*1.2):  # можно менять omega
    return 6 * np.arcsin(np.sin(omega * t))

# Восстановление по теореме Котельникова
def reconstruct_signal(t, samples, Ts):
    y_rec = np.zeros_like(t)
    k = np.arange(len(samples))
    for i in range(len(t)):
        y_rec[i] = np.sum(samples * np.sinc((t[i] - k * Ts) / Ts))
    return y_rec

# Основные параметры
T_obs = 2 * np.pi        # интервал наблюдения
N = 25                   # количество отсчётов (можно менять)
Ts = T_obs / N           # шаг дискретизации
t_cont = np.linspace(0, T_obs, 2000)   # "идеальное" время
t_samp = np.arange(0, T_obs, Ts)       # дискретные моменты времени

# Исходный сигнал
y_true = signal(t_cont)
y_samp = signal(t_samp)

# Восстановленный сигнал
y_rec = reconstruct_signal(t_cont, y_samp, Ts)

# Ошибка восстановления
rms = np.sqrt(np.mean((y_true - y_rec)**2))

# Построение графиков
plt.figure(figsize=(10, 6))
plt.plot(t_cont, y_true, 'b', label="Исходный сигнал (непрерывный)")
plt.stem(t_samp, y_samp, linefmt='r-', markerfmt='ro', basefmt=" ", label="Дискретные отсчёты")
plt.plot(t_cont, y_rec, 'g--', label="Восстановленный сигнал")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.title(f"Восстановление пилообразного сигнала, {N} отсчётов, \n Ошибка восстановления: {rms}")
plt.legend()
plt.grid(True)
plt.show()
