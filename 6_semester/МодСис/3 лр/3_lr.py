import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 1. ГЕНЕРАТОР БСВ (little-frog)
# =========================================================
def generate_bsv(N, r=12, M=12345, A0=1, m=5):
    modulus = 2 ** r
    M_step = pow(M, m, modulus)
    z = np.zeros(N)
    A = A0
    for i in range(N):
        A = (A * M_step) % modulus
        z[i] = A / modulus
    return z


# =========================================================
# 2. ГЕНЕРАТОР СТАНДАРТНЫХ НОРМАЛЬНЫХ ВЕЛИЧИН (Бокс-Мюллер)
# =========================================================
def generate_normal(n, bsv):
    """Генерирует n стандартных нормальных величин из массива БСВ"""
    if len(bsv) < 2 * n:
        bsv = np.concatenate([bsv, generate_bsv(2 * n)])
    bsv = np.clip(bsv[:2 * n], 1e-10, 1 - 1e-10)
    z1 = bsv[::2]
    z2 = bsv[1::2]
    x1 = np.sqrt(-2 * np.log(z1)) * np.cos(2 * np.pi * z2)
    x2 = np.sqrt(-2 * np.log(z1)) * np.sin(2 * np.pi * z2)
    return np.concatenate([x1, x2])[:n]


# =========================================================
# 3. ГЕНЕРАТОР ХИ-КВАДРАТ (через сумму квадратов нормальных)
# =========================================================
def generate_chi_squared(k, N):
    """Генерирует N значений χ²(k)"""
    bsv = generate_bsv(2 * k * N)
    normals = generate_normal(k * N, bsv).reshape(k, N)
    return np.sum(normals ** 2, axis=0)


# =========================================================
# 4. ГЕНЕРАТОР РАСПРЕДЕЛЕНИЯ ФИШЕРА
# =========================================================
def generate_fisher(d1, d2, N):
    """Генерирует N значений F-распределения с параметрами d1, d2"""
    U = generate_chi_squared(d1, N)
    V = generate_chi_squared(d2, N)
    return (U / d1) / (V / d2)


# =========================================================
# 5. ОСНОВНАЯ ЧАСТЬ: ГЕНЕРАЦИЯ ВСЕХ 5 РАСПРЕДЕЛЕНИЙ
# =========================================================
N = 50000  # Объём выборки
z_base = generate_bsv(N * 20)
z_base = np.clip(z_base, 1e-10, 1 - 1e-10)

# Параметры
lam = 2.0
A_uni, B_uni = 5.0, 15.0
K_erlang = 3
m_norm, sigma_norm = 0.0, 1.0
d1_fisher, d2_fisher = 5, 10

# 5.1. Экспоненциальное
z_exp = z_base[:N]
x_exp = -np.log(z_exp) / lam

# 5.2. Равномерное
z_uni = z_base[N:2 * N]
x_uni = A_uni + (B_uni - A_uni) * z_uni

# 5.3. Эрланга
z_erl = generate_bsv(N * K_erlang).reshape(K_erlang, N)
z_erl = np.clip(z_erl, 1e-10, 1 - 1e-10)
x_erl = -np.sum(np.log(z_erl), axis=0) / lam

# 5.4. Нормальное
z_norm = z_base[2 * N:4 * N]
if len(z_norm) % 2 != 0:
    z_norm = z_norm[:-1]
z1, z2 = z_norm[::2], z_norm[1::2]
x1 = np.sqrt(-2 * np.log(z1)) * np.sin(2 * np.pi * z2)
x2 = np.sqrt(-2 * np.log(z1)) * np.cos(2 * np.pi * z2)
x_norm = np.concatenate([x1, x2]) * sigma_norm + m_norm

# 5.5. Фишера (вариант 13)
x_fisher = generate_fisher(d1_fisher, d2_fisher, N)

# Словарь для обработки
distributions = {
    "Экспоненциальное": x_exp,
    "Равномерное": x_uni,
    f"Эрланга (K={K_erlang})": x_erl,
    "Нормальное": x_norm,
    f"Фишера (d1={d1_fisher}, d2={d2_fisher})": x_fisher
}


# =========================================================
# 6. ТЕОРЕТИЧЕСКИЕ И ЭМПИРИЧЕСКИЕ МОМЕНТЫ + ОТКЛОНЕНИЯ
# =========================================================
def calc_theoretical(name):
    if "Эксп" in name:
        return 1 / lam, 1 / (lam ** 2)
    elif "Равн" in name:
        return (A_uni + B_uni) / 2, (B_uni - A_uni) ** 2 / 12
    elif "Эрл" in name:
        return K_erlang / lam, K_erlang / (lam ** 2)
    elif "Норм" in name:
        return m_norm, sigma_norm ** 2
    elif "Фишера" in name:
        d1, d2 = d1_fisher, d2_fisher
        M = d2 / (d2 - 2) if d2 > 2 else np.nan
        D = (2 * d2 ** 2 * (d1 + d2 - 2)) / (d1 * (d2 - 2) ** 2 * (d2 - 4)) if d2 > 4 else np.nan
        return M, D


# Печать заголовка таблицы с отклонениями
print(f"{'Распределение':<25} | {'M теор.':<8} {'M эмп.':<8} {'ΔM, %':<7} | {'D теор.':<8} {'D эмп.':<8} {'ΔD, %':<7}")
print("-" * 105)

for name, x in distributions.items():
    m_th, d_th = calc_theoretical(name)
    m_emp, d_emp = np.mean(x), np.var(x)

    # Расчёт отклонений в процентах
    delta_M = abs(m_emp - m_th) / m_th * 100 if m_th != 0 and not np.isnan(m_th) else np.nan
    delta_D = abs(d_emp - d_th) / d_th * 100 if d_th != 0 and not np.isnan(d_th) else np.nan

    print(f"{name:<25} | {m_th:<8.4f} {m_emp:<8.4f} {delta_M:<7.2f} | {d_th:<8.4f} {d_emp:<8.4f} {delta_D:<7.2f}")

# =========================================================
# 7. ПОСТРОЕНИЕ ГИСТОГРАММ
# =========================================================
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
axes = axes.flatten()

for i, (name, x) in enumerate(distributions.items()):
    axes[i].hist(x, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
    axes[i].set_title(name, fontsize=11)
    axes[i].set_xlabel('x')
    axes[i].set_ylabel('Плотность')
    axes[i].grid(True, linestyle='--', alpha=0.5)

    # Для Фишера ограничим ось, чтобы убрать выбросы
    if "Фишера" in name:
        axes[i].set_xlim(0, np.percentile(x, 98))

plt.tight_layout()
plt.savefig('fisher_lab_hist.png', dpi=300, bbox_inches='tight')
plt.show()