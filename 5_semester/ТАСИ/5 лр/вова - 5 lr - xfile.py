"Реализация JPEG-2000"

from collections import Counter
from pathlib import Path
from math import ceil, log2
from functools import reduce
from operator import mul

from PIL import Image
import numpy as np
import pywt


def create_color_shift_table(image_path, shift_value=128):
    with Image.open(image_path) as img:
        img_rgb = img.convert("RGB")
        img_array = np.array(img_rgb)

        # Применяем цветовой сдвиг
        shifted_array = img_array.astype(np.int16) - np.int16(shift_value)

    return shifted_array


def get_rgb(rgb_triplets) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Получение RGB компонентов из изображения"""

    return rgb_triplets[:, :, 0], rgb_triplets[:, :, 1], rgb_triplets[:, :, 2]


def rgb_to_yuv(
    r_matrix: np.ndarray, g_matrix: np.ndarray, b_matrix: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Преобразование в цветовое пространство YUV"""
    height, width = r_matrix.shape
    Y = np.zeros((height, width), dtype=np.float64)
    U = np.zeros((height, width), dtype=np.float64)
    V = np.zeros((height, width), dtype=np.float64)

    # Матрица преобразования RGB -> YUV
    transform_matrix = np.array([[0.299, 0.587, 0.114], [-0.14713, -0.28886, 0.436], [0.615, -0.51499, -0.10001]])

    for i in range(height):
        for j in range(width):
            rgb = np.array([r_matrix[i, j], g_matrix[i, j], b_matrix[i, j]], dtype=np.float64)
            yuv = np.dot(transform_matrix, rgb)
            Y[i, j], U[i, j], V[i, j] = yuv

    return Y.astype(np.int32), U.astype(np.int32), V.astype(np.int32)


def dwt_to_y(matrix: np.ndarray) -> np.ndarray:
    """Дискретное вейвлет преобразование Хаара в 2 раунда"""
    copy_matrix = matrix.copy().astype(float)

    # 1 раунд
    coeffs1 = pywt.dwt2(copy_matrix, "haar")
    LL1, (_, _, _) = coeffs1

    # 2 раунд
    coeffs2 = pywt.dwt2(LL1, "haar")
    LL2, (_, _, _) = coeffs2

    return LL2


def quantization_with_dead_zone(matrix: np.ndarray, step: int = 10) -> np.ndarray:
    """Квантование с мертвой зоной с выбранным шагом квантования"""
    return (np.sign(matrix) * np.floor(np.abs(matrix) / step)).astype(np.int32)


def arithmetic_encode(matrix: np.ndarray) -> tuple[float, dict[str, tuple[float, float]], float]:
    """Арифметическое кодирование"""
    sequence = list(np.ravel(matrix)) + ["EOM"]
    counts = Counter(sequence)
    total = counts.total()

    probabilities = {sym: counts[sym] / total for sym in counts}

    symbols = sorted(probabilities.keys(), key=lambda x: str(x))
    cumulative = {}
    cum = 0.0
    for s in symbols:
        cumulative[s] = (cum, cum + probabilities[s])
        cum += probabilities[s]

    # кодирование
    low, high = 0.0, 1.0
    for symbol in sequence:
        range_ = high - low
        sym_low, sym_high = cumulative[symbol]
        high = low + range_ * sym_high
        low = low + range_ * sym_low

    return (low + high) / 2, cumulative, -len(sequence) * sum(p * log2(p) for p in probabilities.values())


if __name__ == "__main__":
    np.set_printoptions(precision=2, suppress=True, linewidth=120)

    # step 1
    r, g, b = get_rgb(create_color_shift_table(r"ТехникаАудиовизуальных\data\Lab_5_data\test1.png"))

    # step2
    y, u, v = rgb_to_yuv(r, g, b)

    # step 3
    ll = dwt_to_y(y)

    # step 4
    ll = quantization_with_dead_zone(ll)

    # step 5
    ll, ll_table, compressed_file_size = arithmetic_encode(ll)

    for k, v in ll_table.items():
        print(f"{k:<3}: ({v[0]:.2f}, {v[1]:.2f})")

    print()
    print(f"Закодированный результат: {ll:.2f}")
    print(f"Степень сжатия: {768 * 8 / compressed_file_size:.2f}")
