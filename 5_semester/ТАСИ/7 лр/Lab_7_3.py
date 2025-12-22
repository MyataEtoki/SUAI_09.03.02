import matplotlib.pyplot as plt
import numpy as np
import librosa


def laplacian_segmentation(file_path: str, threshold: float = 0.1):
    y, sr = librosa.load(file_path, sr=None)

    # Вычисление энергии сигнала
    energy = librosa.feature.rms(y=y)[0]

    print(energy)

    # Применяем оператор Лапласа к энергии
    laplacian = np.gradient(np.gradient(energy))

    # Находим точки значительных изменений
    segment_points = np.where(np.abs(laplacian) > threshold)[0]

    # Конвертируем в временные метки
    times = librosa.frames_to_time(segment_points, sr=sr)

    return times, laplacian, energy


if __name__ == "__main__":
    # Использование
    file_path = r"закусочная-сосисочная-4.mp3"
    times, laplacian, energy = laplacian_segmentation(file_path)

    # Визуализация
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    librosa.display.waveshow(
        librosa.load(file_path)[0],
        sr=44100,
    )
    plt.title("Аудиосигнал")

    plt.subplot(3, 1, 2)
    plt.plot(energy)
    plt.title("Энергия сигнала")

    plt.subplot(3, 1, 3)
    plt.plot(laplacian)
    plt.title("Лапласиан энергии")
    for point in np.where(np.abs(laplacian) > 0.1)[0]:
        plt.axvline(x=point, color="red", linestyle="--")
    plt.tight_layout()
    plt.show()
