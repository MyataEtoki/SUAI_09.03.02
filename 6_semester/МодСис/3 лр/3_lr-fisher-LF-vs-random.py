import numpy as np
import matplotlib.pyplot as plt


# Твой little-frog генератор
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
# ПРОВЕРКА 1: Качество БСВ
# =========================================================
print("=" * 60)
print("ПРОВЕРКА 1: Качество базовой случайной величины")
print("=" * 60)

N_test = 100000
z_little_frog = generate_bsv(N_test)
z_numpy = np.random.uniform(0, 1, N_test)

print(f"\nLittle-frog:")
print(f"  M = {z_little_frog.mean():.4f} (должно быть ~0.5)")
print(f"  D = {z_little_frog.var():.4f} (должно быть ~0.0833)")
print(f"  min = {z_little_frog.min():.4f}, max = {z_little_frog.max():.4f}")

print(f"\nNumPy (для сравнения):")
print(f"  M = {z_numpy.mean():.4f}")
print(f"  D = {z_numpy.var():.4f}")

# Гистограмма БСВ
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(z_little_frog, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
axes[0].axhline(1.0, color='red', linestyle='--', label='Теоретическая плотность')
axes[0].set_title('Little-frog БСВ')
axes[0].legend()

axes[1].hist(z_numpy, bins=50, density=True, alpha=0.7, color='green', edgecolor='black')
axes[1].axhline(1.0, color='red', linestyle='--', label='Теоретическая плотность')
axes[1].set_title('NumPy БСВ')
axes[1].legend()

plt.tight_layout()
plt.savefig('bsv_check.png', dpi=300)
plt.show()

# =========================================================
# ПРОВЕРКА 2: Генерация Фишера с NumPy (эталон)
# =========================================================
print("\n" + "=" * 60)
print("ПРОВЕРКА 2: Фишер с NumPy (эталон)")
print("=" * 60)


def generate_fisher_numpy(d1, d2, N):
    """Используем готовый генератор NumPy"""
    return np.random.f(d1, d2, N)


d1, d2 = 5, 10
N = 100000

x_fisher_numpy = generate_fisher_numpy(d1, d2, N)
M_numpy = x_fisher_numpy.mean()
D_numpy = x_fisher_numpy.var()
M_theor = d2 / (d2 - 2)
D_theor = (2 * d2 ** 2 * (d1 + d2 - 2)) / (d1 * (d2 - 2) ** 2 * (d2 - 4))

print(f"\nNumPy Фишер F({d1}, {d2}):")
print(f"  M_эмп = {M_numpy:.4f}, M_теор = {M_theor:.4f}, отклонение = {abs(M_numpy - M_theor) / M_theor * 100:.2f}%")
print(f"  D_эмп = {D_numpy:.4f}, D_теор = {D_theor:.4f}, отклонение = {abs(D_numpy - D_theor) / D_theor * 100:.2f}%")

# =========================================================
# ПРОВЕРКА 3: Генерация Фишера с little-frog
# =========================================================
print("\n" + "=" * 60)
print("ПРОВЕРКА 3: Фишер с little-frog")
print("=" * 60)


def generate_fisher_littlefrog(d1, d2, N):
    """Твоя реализация с little-frog"""
    # Для U ~ χ²(d1)
    bsv_U = generate_bsv(2 * d1 * N)
    z1_U, z2_U = bsv_U[::2], bsv_U[1::2]
    normals_U = np.sqrt(-2 * np.log(z1_U)) * np.cos(2 * np.pi * z2_U)
    U = np.sum(normals_U[:d1 * N].reshape(d1, N) ** 2, axis=0)

    # Для V ~ χ²(d2)
    bsv_V = generate_bsv(2 * d2 * N)
    z1_V, z2_V = bsv_V[::2], bsv_V[1::2]
    normals_V = np.sqrt(-2 * np.log(z1_V)) * np.cos(2 * np.pi * z2_V)
    V = np.sum(normals_V[:d2 * N].reshape(d2, N) ** 2, axis=0)

    return (U / d1) / (V / d2)


x_fisher_lf = generate_fisher_littlefrog(d1, d2, N)
M_lf = x_fisher_lf.mean()
D_lf = x_fisher_lf.var()

print(f"\nLittle-frog Фишер F({d1}, {d2}):")
print(f"  M_эмп = {M_lf:.4f}, M_теор = {M_theor:.4f}, отклонение = {abs(M_lf - M_theor) / M_theor * 100:.2f}%")
print(f"  D_эмп = {D_lf:.4f}, D_теор = {D_theor:.4f}, отклонение = {abs(D_lf - D_theor) / D_theor * 100:.2f}%")

# =========================================================
# СРАВНЕНИЕ ГИСТОГРАММ
# =========================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# NumPy
axes[0].hist(x_fisher_numpy, bins=50, density=True, alpha=0.7, color='green', edgecolor='black', range=(0, 8))
axes[0].axvline(M_theor, color='red', linestyle='--', linewidth=2, label=f'M_теор = {M_theor:.3f}')
axes[0].set_title(f'NumPy F({d1},{d2})\nM={M_numpy:.3f}, D={D_numpy:.3f}')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Little-frog
axes[1].hist(x_fisher_lf, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black', range=(0, 8))
axes[1].axvline(M_theor, color='red', linestyle='--', linewidth=2, label=f'M_теор = {M_theor:.3f}')
axes[1].set_title(f'Little-frog F({d1},{d2})\nM={M_lf:.3f}, D={D_lf:.3f}')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fisher_comparison.png', dpi=300)
plt.show()

print("\n" + "=" * 60)
print("ВЫВОД:")
print("=" * 60)
if abs(M_lf - M_theor) / M_theor > 0.05:
    print("❌ Little-frog генератор даёт плохие результаты!")
    print("   Рекомендация: использовать numpy.random для этой работы")
else:
    print("✅ Little-frog работает нормально, проблема в другом")