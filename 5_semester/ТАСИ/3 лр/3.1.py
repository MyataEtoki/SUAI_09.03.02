import struct
import sys


def read_bmp_header(file):
    print("[1] Чтение заголовка файла BITMAPFILEHEADER...")
    file.seek(0)
    header = file.read(14)
    if len(header) < 14:
        raise ValueError("Файл слишком короткий для заголовка")

    bfType = struct.unpack('<H', header[0:2])[0]
    if bfType != 0x4D42:  # 'BM'
        raise ValueError("Файл не в формате BMP")

    bfSize = struct.unpack('<I', header[2:6])[0]
    bfReserved1 = struct.unpack('<H', header[6:8])[0]
    bfReserved2 = struct.unpack('<H', header[8:10])[0]
    bfOffBits = struct.unpack('<I', header[10:14])[0]

    print(f"  bfType = 0x{bfType:04X} ('BM')")
    print(f"  bfSize = {bfSize} байт")
    print(f"  bfOffBits = {bfOffBits} (смещение к пиксельным данным)")

    return bfOffBits


def read_bmp_info_header(file):
    print("\n[2] Чтение заголовка изображения BITMAPINFOHEADER...")
    info = file.read(40)
    if len(info) < 40:
        raise ValueError("Недостаточно данных для BITMAPINFOHEADER")

    biSize = struct.unpack('<I', info[0:4])[0]
    biWidth = struct.unpack('<I', info[4:8])[0]
    biHeight = struct.unpack('<I', info[8:12])[0]
    biPlanes = struct.unpack('<H', info[12:14])[0]
    biBitCount = struct.unpack('<H', info[14:16])[0]
    biCompression = struct.unpack('<I', info[16:20])[0]
    biSizeImage = struct.unpack('<I', info[20:24])[0]
    biXPelsPerMeter = struct.unpack('<I', info[24:28])[0]
    biYPelsPerMeter = struct.unpack('<I', info[28:32])[0]
    biClrUsed = struct.unpack('<I', info[32:36])[0]
    biClrImportant = struct.unpack('<I', info[36:40])[0]

    print(f"  biSize = {biSize}")
    print(f"  biWidth = {biWidth} пикселей")
    print(f"  biHeight = {biHeight} пикселей")
    print(f"  biBitCount = {biBitCount} бит/пиксель")
    print(f"  biCompression = {biCompression} (0 = без сжатия)")
    print(f"  biClrUsed = {biClrUsed}")

    if biBitCount != 32:
        raise ValueError("Поддерживается только 32-битный BMP (вариант 5)")
    if biCompression != 0:
        raise ValueError("Поддерживается только несжатый BMP")

    return {
        'width': biWidth,
        'height': biHeight,
        'bit_count': biBitCount,
        'clr_used': biClrUsed,
        'size_image': biSizeImage,
    }


def read_pixel_data_32bit(file, offset, width, height):
    print(f"\n[3] Чтение 32-битных пиксельных данных (смещение = {offset})...")
    file.seek(offset)

    pixels = []
    bytes_per_pixel = 4  # BGRA
    row_size_raw = width * bytes_per_pixel
    # 32-битное BMP не имеет паддинга строк (по методичке)
    print(f"  Размер строки: {row_size_raw} байт (без паддинга)")
    print(f"  Считываем {height} строк...")

    for y in range(height - 1, -1, -1):  # BMP хранится снизу вверх
        row_data = file.read(row_size_raw)
        if len(row_data) < row_size_raw:
            raise ValueError(f"Не хватает данных в строке {y}")

        row = []
        for x in range(width):
            start = x * bytes_per_pixel
            b = row_data[start]
            g = row_data[start + 1]
            r = row_data[start + 2]
            # a = row_data[start + 3] # Alpha игнорируется
            row.append((r, g, b))
        pixels.append(row)

    print(f"  Загружено {len(pixels)} строк по {len(pixels[0])} пикселей")
    return pixels


def rgb_to_grayscale_index(r, g, b):
    # Формула из методички: 0.299*R + 0.597*G + 0.114*B
    gray_val = 0.299 * r + 0.597 * g + 0.114 * b
    gray_val = int(gray_val)
    # Найти ближайший оттенок из палитры 4-битного серого: [0, 15, 31, ..., 255]
    # Палитра: индекс * 17 (округлено: 255/15 = 17)
    index = round(gray_val / 17.0)
    index = max(0, min(15, index))  # Ограничить 0..15
    return index


def create_4bit_grayscale_palette():
    print("\n[4] Создание 4-битной палитры (16 оттенков серого)...")
    palette = []
    for i in range(16):
        val = i * 17  # 0, 17, 34, ..., 255
        palette.append((val, val, val))  # (R, G, B)
    print(f"  Палитра: [0,0,0], [17,17,17], [34,34,34], ..., [255,255,255]")
    return palette


def convert_to_4bit_indices(pixels):
    print("\n[5] Преобразование пикселей в 4-битные индексы палитры...")
    height = len(pixels)
    width = len(pixels[0])
    indices = []

    for y in range(height):
        idx_row = []
        for x in range(width):
            r, g, b = pixels[y][x]
            idx = rgb_to_grayscale_index(r, g, b)
            idx_row.append(idx)
        indices.append(idx_row)

    print(f"  Пример: пиксель[0][0] = RGB{pixels[0][0]} → индекс = {indices[0][0]} (цвет {indices[0][0] * 17})")
    return indices


def pack_4bit_row(row_indices):
    """Упаковывает строку индексов (0-15) в байты."""
    packed = bytearray()
    for i in range(0, len(row_indices), 2):
        high = row_indices[i] & 0x0F  # Старшие 4 бита
        low = row_indices[i + 1] & 0x0F if i + 1 < len(row_indices) else 0  # Младшие 4 бита
        byte = (high << 4) | low
        packed.append(byte)
    return bytes(packed)


def write_4bit_bmp(filename, width, height, indices, palette):
    print(f"\n[6] Запись 4-битного BMP в файл '{filename}'...")

    palette_size = 16 * 4  # 16 цветов × 4 байта (B,G,R,0)
    row_size_unpadded = (width + 1) // 2  # Каждый байт = 2 пикселя
    row_padding = (4 - (row_size_unpadded % 4)) % 4
    row_size_padded = row_size_unpadded + row_padding
    image_size = row_size_padded * height
    file_size = 14 + 40 + palette_size + image_size

    # BITMAPFILEHEADER
    bfType = 0x4D42
    bfSize = file_size
    bfReserved1 = 0
    bfReserved2 = 0
    bfOffBits = 14 + 40 + palette_size

    # BITMAPINFOHEADER
    biSize = 40
    biWidth = width
    biHeight = height
    biPlanes = 1
    biBitCount = 4
    biCompression = 0
    biSizeImage = image_size
    biXPelsPerMeter = 2835
    biYPelsPerMeter = 2835
    biClrUsed = 16
    biClrImportant = 0

    with open(filename, 'wb') as f:
        # Заголовок файла
        f.write(struct.pack('<HIHHI', bfType, bfSize, bfReserved1, bfReserved2, bfOffBits))

        # Заголовок изображения
        f.write(struct.pack('<IIIHHIIIIII',
                            biSize, biWidth, biHeight, biPlanes, biBitCount,
                            biCompression, biSizeImage, biXPelsPerMeter, biYPelsPerMeter,
                            biClrUsed, biClrImportant))

        # Запись палитры (B, G, R, 0)
        for r, g, b in palette:
            f.write(struct.pack('BBBB', b, g, r, 0))

        # Запись пикселей (сверху вниз)
        for y in range(height):
            row = indices[y]
            packed_row = pack_4bit_row(row)
            f.write(packed_row)
            if row_padding > 0:
                f.write(b'\x00' * row_padding)

    print(f"  Файл '{filename}' успешно сохранён!")
    print(f"  Размер файла: {file_size} байт")
    print(f"  Размер изображения: {image_size} байт")
    print(f"  Палитра: {16} цветов")
    print(
        f"  Упаковка: {len(indices[0])} пикселей -> {len(packed_row)} байт на строку (до {row_size_padded} с паддингом)")


def main():

    input_path = 'input_32bit.bmp'
    output_path = 'output_4bit.bmp'

    print("=== Лабораторная работа: Преобразование BMP 32 бит -> 4 бит (Вариант 5) ===\n")

    with open(input_path, 'rb') as f:
        offset = read_bmp_header(f)
        info = read_bmp_info_header(f)
        pixels = read_pixel_data_32bit(f, offset, info['width'], info['height'])

    indices = convert_to_4bit_indices(pixels)
    palette = create_4bit_grayscale_palette()
    write_4bit_bmp(output_path, info['width'], info['height'], indices, palette)

    print("\n✅ Преобразование завершено!")


if __name__ == "__main__":
    main()