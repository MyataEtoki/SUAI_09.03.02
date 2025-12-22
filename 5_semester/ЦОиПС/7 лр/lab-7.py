import numpy as np
import matplotlib.pyplot as plt

# Параметры
N = 29                # длина импульсной характеристики
cutoff_frac_pi = 0.4  # частота среза в долях от Найквиста
omega_c = cutoff_frac_pi * np.pi

# Импульсная характеристика для ФНЧ
n_sym = np.arange(-(N-1)//2, (N-1)//2 + 1)  # от -M..M
h = np.zeros(N, dtype=float)
for idx, ni in enumerate(n_sym):
    if ni == 0:
        h[idx] = omega_c / np.pi
    else:
        h[idx] = np.sin(omega_c * ni) / (np.pi * ni)


# Окна
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

# Расчёт ЧХ
omega = np.linspace(0, np.pi, 2048)
def compute_H(h, omega_array):
    n_idx = np.arange(len(h))            # 0..N-1
    E = np.exp(-1j * np.outer(omega_array, n_idx))  # K x N
    H = E @ h
    return H


H_rect = compute_H(h_rect, omega)
H_hamm = compute_H(h_hamm, omega)

# Идеальная АЧХ для окон
H_ideal_mask = np.zeros_like(omega)
H_ideal_mask[(omega / np.pi) <= cutoff_frac_pi] = 1.0


# Функция для рисования графиков
def plot_filter_graphs(h, H, omega_array, H_ideal_mask, title_suffix, show_ideal=True):
    N_local = len(h)

    # Импульсная характеристика
    plt.figure(figsize=(10, 4))
    plt.stem(np.arange(N_local), h)
    plt.title(f'Импульсная характеристика {title_suffix} (N={N_local})')
    plt.xlabel('n')
    plt.ylabel('h[n]')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # АЧХ (линейная шкала)
    plt.figure(figsize=(10, 4))
    plt.plot(omega_array/np.pi, np.abs(H), linewidth=1.2, label='Реальная АЧХ')
    if show_ideal:
        plt.plot(omega_array/np.pi, H_ideal_mask, 'r--', linewidth=1.0, label='Идеальная АЧХ')
        plt.axvline(x=cutoff_frac_pi, color='g', linestyle=':', label=f'граница {cutoff_frac_pi:.3f}·π')
    plt.title(f'АЧХ {title_suffix}')
    plt.xlabel('Нормализованная частота ω×π')
    plt.ylabel('|H(ω)|')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # АЧХ (логарифмическая шкала)
    plt.figure(figsize=(10, 4))
    plt.plot(omega_array/np.pi, 20*np.log10(np.abs(H) + 1e-12), linewidth=1.2)
    if show_ideal:
        plt.axvline(x=cutoff_frac_pi, color='r', linestyle='--')
    plt.title(f'АЧХ (лог, дБ) {title_suffix}')
    plt.xlabel('Нормализованная частота ω×π')
    plt.ylabel('20·log10 |H(ω)|, дБ')
    plt.ylim([-120, 5])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # ФЧХ
    plt.figure(figsize=(10, 4))
    coeff = np.polyfit(omega_array, np.unwrap(np.angle(H)), 1)
    phase_lin = np.polyval(coeff, omega_array)
    plt.plot(omega_array / np.pi, phase_lin, linewidth=1.2)
    plt.title(f'ФЧХ {title_suffix}')
    plt.xlabel('Частота (×π рад/отсч.)')
    plt.ylabel('Фаза, рад')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Диаграмма нулей
    zeros = np.roots(h[::-1])
    plt.figure(figsize=(6, 6))
    plt.plot(np.real(zeros), np.imag(zeros), 'o', markersize=8, label='Нули')
    circle = plt.Circle((0, 0), 1, fill=False, linestyle='--', alpha=0.7)
    ax = plt.gca()
    ax.add_artist(circle)
    plt.axhline(0, color='k', linewidth=0.6)
    plt.axvline(0, color='k', linewidth=0.6)
    ax.set_aspect('equal', 'box')
    plt.title(f'Диаграмма нулей {title_suffix}')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Рисование графиков
plot_filter_graphs(h_rect, H_rect, omega, H_ideal_mask, title_suffix='(прямоугольное окно)')
plot_filter_graphs(h_hamm, H_hamm, omega, H_ideal_mask, title_suffix='(окно Хэмминга)')


# Функция сравнения АЧХ двух фильтров
def compare_frequency_responses(H1, H2, omega_array, label1='Фильтр 1', label2='Фильтр 2', H_ideal_mask=None, show_ideal=True):
    # Линейная шкала
    plt.figure(figsize=(10, 4))
    plt.plot(omega_array/np.pi, np.abs(H1), linewidth=1.2, label=label1)
    plt.plot(omega_array/np.pi, np.abs(H2), linewidth=1.2, label=label2)
    if show_ideal and H_ideal_mask is not None:
        plt.plot(omega_array/np.pi, H_ideal_mask, 'r--', linewidth=1.0, label='Идеальная АЧХ')
    plt.title('Сравнение АЧХ (линейная шкала)')
    plt.xlabel('Нормализованная частота ω×π')
    plt.ylabel('|H(ω)|')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Логарифмическая шкала, дБ
    plt.figure(figsize=(10, 4))
    plt.plot(omega_array/np.pi, 20*np.log10(np.abs(H1)+1e-12), linewidth=1.2, label=label1)
    plt.plot(omega_array/np.pi, 20*np.log10(np.abs(H2)+1e-12), linewidth=1.2, label=label2)
    if show_ideal:
        plt.axvline(x=cutoff_frac_pi, color='r', linestyle='--')
    plt.title('Сравнение АЧХ (лог, дБ)')
    plt.xlabel('Частота (×π рад/отсч.)')
    plt.ylabel('20·log10 |H(ω)|, дБ')
    plt.ylim([-120, 5])
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


compare_frequency_responses(H_rect, H_hamm, omega, label1='Прямоугольное окно', label2='Окно Хэмминга', H_ideal_mask=H_ideal_mask)


def print_coeffs(h, label):
    print(f"\nКоэффициенты {label}:")
    for i, val in enumerate(h):
        print(f"h[{i:3d}] = {val:.8f}")


print_coeffs(h_rect, "с прямоугольным окном")
print_coeffs(h_hamm, "с окном Хэмминга")
