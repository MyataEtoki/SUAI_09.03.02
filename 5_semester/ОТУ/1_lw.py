import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Настройка стиля графиков
plt.style.use('seaborn-v0_8')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# =============================================================================
# 1. АПЕРИОДИЧЕСКОЕ ЗВЕНО (K=7, T=0.3)
# =============================================================================
K_aper = 7
T_aper = 0.3

# Создаем передаточную функцию: W(s) = K / (T*s + 1)
num_aper = [K_aper]
den_aper = [T_aper, 1]
system_aper = signal.TransferFunction(num_aper, den_aper)

# Диапазон частот для построения
w_aper = np.logspace(-2, 3, 1000)  # от 0.01 до 1000 рад/с

# Вычисляем АЧХ и ФЧХ
w_aper, mag_aper, phase_aper = signal.bode(system_aper, w_aper)

# ЛАЧХ
ax1.semilogx(w_aper, mag_aper, 'b', linewidth=2, label=f'K={K_aper}, T={T_aper}')
ax1.set_title('ЛАЧХ апериодического звена', fontsize=12, fontweight='bold')
ax1.set_ylabel('Амплитуда [дБ]', fontsize=10)
ax1.grid(True, which='both', alpha=0.3)
ax1.legend()

# ЛФЧХ
ax2.semilogx(w_aper, phase_aper, 'r', linewidth=2, label=f'K={K_aper}, T={T_aper}')
ax2.set_title('ЛФЧХ апериодического звена', fontsize=12, fontweight='bold')
ax2.set_ylabel('Фаза [градусы]', fontsize=10)
ax2.set_xlabel('Частота [рад/с]', fontsize=10)
ax2.grid(True, which='both', alpha=0.3)
ax2.legend()

# =============================================================================
# 2. КОЛЕБАТЕЛЬНОЕ ЗВЕНО (K=2, T₂=0.1, T₃=0.4)
# =============================================================================
K_osc = 2
T3_osc = 0.4  # T = T3
T2_osc = 0.1
xi_osc = T2_osc / (2 * T3_osc)  # коэффициент демпфирования

print(f"Коэффициент демпфирования ξ = {xi_osc:.3f}")

# Создаем передаточную функцию: W(s) = K / (T²*s² + 2*ξ*T*s + 1)
num_osc = [K_osc]
den_osc = [T3_osc**2, 2*xi_osc*T3_osc, 1]
system_osc = signal.TransferFunction(num_osc, den_osc)

# Диапазон частот для построения
w_osc = np.logspace(-2, 2, 1000)  # от 0.01 до 100 рад/с

# Вычисляем АЧХ и ФЧХ
w_osc, mag_osc, phase_osc = signal.bode(system_osc, w_osc)

# ЛАЧХ
ax3.semilogx(w_osc, mag_osc, 'g', linewidth=2, label=f'K={K_osc}, T2={T2_osc}, T3={T3_osc}')
ax3.set_title('ЛАЧХ колебательного звена', fontsize=12, fontweight='bold')
ax3.set_ylabel('Амплитуда [дБ]', fontsize=10)
ax3.grid(True, which='both', alpha=0.3)
ax3.legend()

# ЛФЧХ
ax4.semilogx(w_osc, phase_osc, 'm', linewidth=2, label=f'ξ={xi_osc:.3f}')
ax4.set_title('ЛФЧХ колебательного звена', fontsize=12, fontweight='bold')
ax4.set_ylabel('Фаза [градусы]', fontsize=10)
ax4.set_xlabel('Частота [рад/с]', fontsize=10)
ax4.grid(True, which='both', alpha=0.3)
ax4.legend()

plt.tight_layout()
plt.show()

# =============================================================================
# 3. ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ - СРАВНЕНИЕ РАЗНЫХ ПАРАМЕТРОВ
# =============================================================================
print("\n" + "="*60)
print("АНАЛИТИЧЕСКИЕ ВЫВОДЫ")
print("="*60)

# Сопрягающие частоты
w_c_aper = 1 / T_aper
w_c_osc = 1 / T3_osc

print(f"Апериодическое звено:")
print(f"  - Сопрягающая частота: ω_c = {w_c_aper:.2f} рад/с")
print(f"  - Установившееся усиление: {20*np.log10(K_aper):.1f} дБ")

print(f"\nКолебательное звено:")
print(f"  - Сопрягающая частота: ω_c = {w_c_osc:.2f} рад/с")
print(f"  - Коэффициент демпфирования: ξ = {xi_osc:.3f}")
print(f"  - Установившееся усиление: {20*np.log10(K_osc):.1f} дБ")

if xi_osc < 0.707:
    print(f"  - Резонансный всплеск: ДА (ξ < 0.707)")
    # Находим резонансную частоту и амплитуду
    resonance_idx = np.argmax(mag_osc)
    resonance_freq = w_osc[resonance_idx]
    resonance_mag = mag_osc[resonance_idx]
    print(f"  - Резонансная частота: {resonance_freq:.2f} рад/с")
    print(f"  - Резонансный всплеск: {resonance_mag:.1f} дБ")
else:
    print(f"  - Резонансный всплеск: НЕТ (ξ ≥ 0.707)")

# =============================================================================
# 4. ПОСТРОЕНИЕ ОТДЕЛЬНЫХ ГРАФИКОВ ДЛЯ ОТЧЕТА
# =============================================================================
# График для апериодического звена с разными параметрами
plt.figure(figsize=(12, 5))

# Параметры для сравнения
params_aper = [
    (7, 0.3, 'b', 'K=7, T=0.3 (исходные)'),
    (14, 0.6, 'r', 'K=14, T=0.6 (увеличены)'),
    (3.5, 0.15, 'g', 'K=3.5, T=0.15 (уменьшены)')
]

plt.subplot(1, 2, 1)
for K, T, color, label in params_aper:
    system = signal.TransferFunction([K], [T, 1])
    w, mag, phase = signal.bode(system, np.logspace(-2, 3, 1000))
    plt.semilogx(w, mag, color, linewidth=2, label=label)

plt.title('ЛАЧХ апериодического звена\n(влияние параметров)', fontweight='bold')
plt.ylabel('Амплитуда [дБ]')
plt.xlabel('Частота [рад/с]')
plt.grid(True, alpha=0.3)
plt.legend()

# График для колебательного звена с разными параметрами
plt.subplot(1, 2, 2)

params_osc = [
    (2, 0.1, 0.4, 'b', 'K=2, T2=0.1, T3=0.4 (исходные)'),
    (10, 0.1, 0.4, 'r', 'K=10, T2=0.1, T3=0.4 (K увеличен)'),
    (2, 0.1, 4.0, 'g', 'K=2, T2=0.1, T3=4.0 (T₃ увеличен)')
]

for K, T2, T3, color, label in params_osc:
    xi = T2 / (2 * T3)
    system = signal.TransferFunction([K], [T3**2, 2*xi*T3, 1])
    w, mag, phase = signal.bode(system, np.logspace(-2, 2, 1000))
    plt.semilogx(w, mag, color, linewidth=2, label=label)

plt.title('ЛАЧХ колебательного звена\n(влияние параметров)', fontweight='bold')
plt.ylabel('Амплитуда [дБ]')
plt.xlabel('Частота [рад/с]')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()