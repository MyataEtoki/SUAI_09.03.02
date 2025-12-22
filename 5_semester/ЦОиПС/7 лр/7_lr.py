import numpy as np
import matplotlib.pyplot as plt

# ================================
# ПАРАМЕТРЫ ВАРИАНТА 16
# ================================
N = 29                # длина импульсной характеристики
cutoff_frac_pi = 0.4  # частота среза в долях от Найквиста (т.е. от π)
omega_c = cutoff_frac_pi * np.pi

# ================================
# Идеальная ИХ (непричинная: от -M до M)
# ================================
n_sym = np.arange(-(N-1)//2, (N-1)//2 + 1)  # [-14, ..., 0, ..., 14]
h = np.zeros(N, dtype=float)
for idx, ni in enumerate(n_sym):
    if ni == 0:
        h[idx] = omega_c / np.pi  # = 0.4
    else:
        h[idx] = np.sin(omega_c * ni) / (np.pi * ni)

# ================================
# Оконные функции
# ================================
def rectangular_window(N):
    return np.ones(N)

def hamming_window_formula(N):
    n = np.arange(N)
    return 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))

w_rect = rectangular_window(N)
w_hamm = hamming_window_formula(N)

# Применение окон
h_rect = h * w_rect
h_hamm = h * w_hamm

# ================================
# Частотная характеристика
# ================================
omega = np.linspace(0, np.pi, 2048)

def compute_H(h, omega_array):
    n_idx = np.arange(len(h))
    E = np.exp(-1j * np.outer(omega_array, n_idx))
    return E @ h

H_rect = compute_H(h_rect, omega)
H_hamm = compute_H(h_hamm, omega)

# Идеальная АЧХ
H_ideal_mask = np.zeros_like(omega)
H_ideal_mask[(omega / np.pi) <= cutoff_frac_pi] = 1.0

# ================================
# Функция построения графиков (ТОЛЬКО ОДИН ФИЛЬТР ЗА РАЗ)
# ================================
def plot_single_filter(h, H, title_suffix):
    n = np.arange(len(h))
    # 1. Импульсная характеристика
    plt.figure(figsize=(8, 3))
    plt.stem(n, h)
    plt.title(f'Импульсная характеристика {title_suffix}')
    plt.xlabel('n')
    plt.ylabel('h[n]')
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show()

    # 2. АЧХ (линейная)
    plt.figure(figsize=(8, 3))
    plt.plot(omega / np.pi, np.abs(H), linewidth=1.5, label='Реальная АЧХ')
    plt.plot(omega / np.pi, H_ideal_mask, 'r--', linewidth=1.0, label='Идеальная АЧХ')
    plt.axvline(x=cutoff_frac_pi, color='g', linestyle=':', label=f'f_c = {cutoff_frac_pi}')
    plt.title(f'АЧХ (линейный масштаб) {title_suffix}')
    plt.xlabel('Нормированная частота ω/π')
    plt.ylabel('|H(ω)|')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show()

    # 3. АЧХ (дБ)
    plt.figure(figsize=(8, 3))
    plt.plot(omega / np.pi, 20 * np.log10(np.abs(H) + 1e-12), linewidth=1.5)
    plt.axvline(x=cutoff_frac_pi, color='r', linestyle='--')
    plt.title(f'АЧХ (дБ) {title_suffix}')
    plt.xlabel('Нормированная частота ω/π')
    plt.ylabel('Уровень, дБ')
    plt.ylim([-100, 5])
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show()

    # 4. ФЧХ
    plt.figure(figsize=(8, 3))
    phase = np.unwrap(np.angle(H))
    plt.plot(omega / np.pi, phase, linewidth=1.5)
    plt.title(f'ФЧХ {title_suffix}')
    plt.xlabel('Нормированная частота ω/π')
    plt.ylabel('Фаза, рад')
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.show()

    # 5. Нули
    zeros = np.roots(h[::-1])
    plt.figure(figsize=(5, 5))
    plt.plot(np.real(zeros), np.imag(zeros), 'ro', markersize=6, label='Нули')
    circle = plt.Circle((0, 0), 1, color='k', fill=False, linestyle='--', alpha=0.6)
    ax = plt.gca()
    ax.add_artist(circle)
    plt.axhline(0, color='k', linewidth=0.5)
    plt.axvline(0, color='k', linewidth=0.5)
    ax.set_aspect('equal', 'box')
    plt.title(f'Диаграмма нулей {title_suffix}')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.grid(True, alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

# ================================
# Выполнение задания ПО ПУНКТАМ
# ================================

# Пункт 1: Прямоугольное окно
plot_single_filter(h_rect, H_rect, '(прямоугольное окно)')

# Пункт 2: Окно Хэмминга (ваш вариант)
plot_single_filter(h_hamm, H_hamm, '(окно Хэмминга, вариант 16)')

# Пункт 3: Сравнение АЧХ
plt.figure(figsize=(8, 3))
plt.plot(omega / np.pi, np.abs(H_rect), linewidth=1.5, label='Прямоугольное окно')
plt.plot(omega / np.pi, np.abs(H_hamm), linewidth=1.5, label='Окно Хэмминга')
plt.plot(omega / np.pi, H_ideal_mask, 'k--', linewidth=1.0, label='Идеальная АЧХ')
plt.axvline(x=cutoff_frac_pi, color='g', linestyle=':', label=f'f_c = {cutoff_frac_pi}')
plt.title('Сравнение АЧХ (линейный масштаб)')
plt.xlabel('Нормированная частота ω/π')
plt.ylabel('|H(ω)|')
plt.legend()
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 3))
plt.plot(omega / np.pi, 20 * np.log10(np.abs(H_rect) + 1e-12), linewidth=1.5, label='Прямоугольное окно')
plt.plot(omega / np.pi, 20 * np.log10(np.abs(H_hamm) + 1e-12), linewidth=1.5, label='Окно Хэмминга')
plt.axvline(x=cutoff_frac_pi, color='r', linestyle='--')
plt.title('Сравнение АЧХ (дБ)')
plt.xlabel('Нормированная частота ω/π')
plt.ylabel('Уровень, дБ')
plt.ylim([-100, 5])
plt.legend()
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()