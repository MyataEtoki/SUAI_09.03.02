import numpy as np
from PIL import Image
import math

def rotate_image_with_artifacts(input_path, output_path, angle):
    # Открываем исходное изображение
    input_image = Image.open(input_path)
    width, height = input_image.size

    # Конвертируем угол в радианы
    angle_rad = math.radians(angle)

    # Создаем новое пустое изображение (начальное состояние пикселей - None)
    output_image = Image.new("RGB", (width, height))

    # Центр изображения
    cx, cy = width // 2, height // 2

    for y in range(height):
        for x in range(width):
            # Перемещаем координаты так, чтобы центр изображения был в (0,0)
            x_shifted = x - cx
            y_shifted = y - cy

            # Применяем матрицу поворота
            new_x = round(x_shifted * math.cos(angle_rad) - y_shifted * math.sin(angle_rad))
            new_y = round(x_shifted * math.sin(angle_rad) + y_shifted * math.cos(angle_rad))

            # Перемещаем координаты обратно
            new_x += cx
            new_y += cy

            # Копируем пиксель, если он попадает в границы изображения
            if 0 <= new_x < width and 0 <= new_y < height:
                output_image.putpixel((new_x, new_y), input_image.getpixel((x, y)))

    # Сохраняем изображение с артефактами
    output_image.save(output_path)
    print(f"Изображение сохранено: {output_path}")

def apply_transformation(input_image, width, height, matrix, center):
    size = input_image.size
    new_size = (width, height)

    # Создаем черное изображение для перемещения
    output = Image.new('RGB', new_size, (0, 0, 0))

    # Перемещение изображения в центр области
    for y in range(size[1]):
        for x in range(size[0]):
            output.putpixel((x + new_size[0] // 2 - size[0] // 2, y + new_size[1] // 2 - size[1] // 2), input_image.getpixel((x, y)))

    transformed = Image.new('RGB', new_size, (0, 0, 0))

    for y in range(new_size[1]):
        for x in range(new_size[0]):
            # Преобразование координат в систему с центром
            pos = np.array([x - new_size[0] / 2.0, y - new_size[1] / 2.0, 1])
            result = np.zeros(3)

            # Применение матрицы преобразования
            for i in range(3):
                result[i] = sum(matrix[i][j] * pos[j] for j in range(3))

            # Возвращение в исходную систему координат
            new_x = int(result[0] + new_size[0] / 2)
            new_y = int(result[1] + new_size[1] / 2)

            # Проверка границ изображения
            if 0 <= new_x < new_size[0] and 0 <= new_y < new_size[1]:
                transformed.putpixel((new_x, new_y), output.getpixel((x, y)))

    return transformed

def crop_image(input_image, x, y, width, height):
    """ Обрезает изображение до заданных размеров """
    return input_image.crop((x, y, x + width, y + height))

def rotate_image_without_artifacts(input_image, angle, base_filename):
    size = input_image.size
    # Размеры увеличенной области для преобразований
    width = size[0] * 2
    height = size[1] * 2

    temp1 = Image.new('RGB', (width, height), (0, 0, 0))
    temp2 = Image.new('RGB', (width, height), (0, 0, 0))
    output = Image.new('RGB', (width, height), (0, 0, 0))

    rad = np.deg2rad(angle)
    center = (size[0] / 2.0, size[1] / 2.0)

    # Первая матрица
    shift_matrix1 = np.array([
        [1, -np.tan(rad) / 2, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    # Вторая матрица
    shift_matrix2 = np.array([
        [1, 0, 0],
        [np.sin(rad), 1, 0],
        [0, 0, 1]
    ])

    # Применение первой матрицы
    temp1 = apply_transformation(input_image, width, height, shift_matrix1, center)
    temp1_cropped = crop_image(temp1, size[0] / 2.0, size[1] / 2.0, size[0], size[1])
    temp1_cropped.save(base_filename + "_crop_step1.bmp")

    # Применение второй матрицы
    temp2 = apply_transformation(temp1, width, height, shift_matrix2, center)
    temp2_cropped = crop_image(temp2, size[0] / 2.0, size[1] / 2.0, size[0], size[1])
    temp2_cropped.save(base_filename + "_crop_step2.bmp")

    # Применение первой матрицы
    output = apply_transformation(temp2, width, height, shift_matrix1, center)
    output_cropped = crop_image(output, size[0] / 2.0, size[1] / 2.0, size[0], size[1])
    output_cropped.save(base_filename + "_crop_step3.bmp")

    # Обрезка окончательного изображения
    #output_cropped = crop_image(output, size[0] / 2.0, size[1] / 2.0, size[0], size[1])
    #output_cropped.save(base_filename + "_cropped.bmp")

    return output_cropped


# Задаём параметры:
a, a3, a5=8, 8*3, 8*5
x=a5
# Поворот через аффинные, с артефактами
rotate_image_with_artifacts("розовый-танк.bmp", f"output_affin_{x}.bmp", x)

# Поворот через Оуэна-Македона, без артефактов
#input_image = Image.open("розовый-танк.bmp")
#rotated_image = rotate_image_without_artifacts(input_image, x, f"rotated_{x}")

