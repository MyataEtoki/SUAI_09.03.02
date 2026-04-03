import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# ГЕНЕРАТОР БСВ
# =========================================================
def generate_bsv(N, r=12, M=12345, A0=1, m=5):
    modulus = 2 ** r
    M_step = pow(M, m, modulus)
    z = np.zeros(N)
    A = A0
    for i in range(N):
        A = (A * M_step) % modulus
        z[i] = A / modulus
    return np.clip(z, 1e-10, 1 - 1e-10)


# =========================================================
# ГЕНЕРАТОР ФИШЕРА (полностью независимый)
# =========================================================
def generate_fisher(d1, d2, N):
    """Генерирует F-распределение"""
    # Для U ~ χ²(d1)
    bsv_U = generate_bsv(2 * d1 * N)
    z1_U, z2_U = bsv_U[::2], bsv_U[1::2]
    normals_U = np.sqrt(-2 * np.log(z1_U)) * np.cos(2 * np.pi * z2_U)
    U = np.sum(normals_U[:d1 * N].reshape(d1, N) ** 2, axis=0)

    # Для V ~ χ²(d2) — НЕЗАВИСИМЫЕ БСВ!
    bsv_V = generate_bsv(2 * d2 * N)
    z1_V, z2_V = bsv_V[::2], bsv_V[1::2]
    normals_V = np.sqrt(-2 * np.log(z1_V)) * np.cos(2 * np.pi * z2_V)
    V = np.sum(normals_V[:d2 * N].reshape(d2, N) ** 2, axis=0)

    return (U / d1) / (V / d2)


# =========================================================
# ГЕНЕРАЦИЯ И ОТРИСОВКА
# =========================================================
N = 500000  # Большой объем выборки!
d1, d2 = 5, 10

print(f"Генерация распределения Фишера F({d1}, {d2})...")
x_fisher = generate_fisher(d1, d2, N)

# Статистика
M_emp = x_fisher.mean()
D_emp = x_fisher.var()
M_theor = d2 / (d2 - 2)
D_theor = (2 * d2 ** 2 * (d1 + d2 - 2)) / (d1 * (d2 - 2) ** 2 * (d2 - 4))

print(f"\n=== Распределение Фишера F({d1}, {d2}) ===")
print(f"Объем выборки: N = {N}")
print(f"Эмпирическое M = {M_emp:.4f}, теоретическое M = {M_theor:.4f}")
print(f"Эмпирическое D = {D_emp:.4f}, теоретическое D = {D_theor:.4f}")
print(f"Отклонение M: {abs(M_emp - M_theor)}")
print(f"Отклонение D: {abs(D_emp - D_theor)}")
print(f"\nМин: {x_fisher.min():.4f}, Макс: {x_fisher.max():.4f}")
print(f"Медиана: {np.median(x_fisher):.4f}")
print(f"95-й перцентиль: {np.percentile(x_fisher, 95):.4f}")

# =========================================================
# ПОСТРОЕНИЕ ГИСТОГРАММЫ
# =========================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# График 1: Полный вид с обрезанием выбросов
ax1 = axes[0]
ax1.hist(x_fisher, bins=50, density=True, alpha=0.7,
         color='skyblue', edgecolor='black', range=(0, 8))
ax1.axvline(M_theor, color='red', linestyle='--', linewidth=2,
            label=f'M_теор = {M_theor:.3f}')
ax1.axvline(M_emp, color='green', linestyle='--', linewidth=2,
            label=f'M_эмп = {M_emp:.3f}')
ax1.set_title(f'Распределение Фишера F({d1}, {d2})\nN={N}', fontsize=12)
ax1.set_xlabel('x')
ax1.set_ylabel('Плотность вероятности')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_xlim(0, 8)

# График 2: Увеличенный масштаб (0 до 5)
ax2 = axes[1]
ax2.hist(x_fisher, bins=40, density=True, alpha=0.7,
         color='coral', edgecolor='black', range=(0, 5))
ax2.axvline(M_theor, color='red', linestyle='--', linewidth=2,
            label=f'M_теор = {M_theor:.3f}')
ax2.set_title(f'Распределение Фишера F({d1}, {d2})\nУвеличенный масштаб', fontsize=12)
ax2.set_xlabel('x')
ax2.set_ylabel('Плотность вероятности')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_xlim(0, 5)

plt.tight_layout()
plt.savefig('fisher_separate.png', dpi=300, bbox_inches='tight')
plt.show()

# =========================================================
# ПРОВЕРКА: Пробуем добавить теоретическую кривую (если есть scipy)
# =========================================================
try:
    from scipy import stats

    fig, ax = plt.subplots(figsize=(10, 6))

    # Гистограмма
    ax.hist(x_fisher, bins=50, density=True, alpha=0.6,
            color='blue', edgecolor='black', range=(0, 8), label='Эмпирическая')

    # Теоретическая плотность
    x = np.linspace(0.01, 8, 500)
    y = stats.f.pdf(x, d1, d2)
    ax.plot(x, y, 'r-', linewidth=2, label=f'Teоретическая F({d1},{d2})')

    ax.set_title(f'Распределение Фишера F({d1}, {d2})\nСравнение с теоретической плотностью', fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('Плотность вероятности')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(0, 8)

    plt.tight_layout()
    plt.savefig('fisher_with_theory.png', dpi=300, bbox_inches='tight')
    plt.show()

except ImportError:
    print("\nScipy не установлен. Для сравнения с теоретической кривой установите: pip install scipy")