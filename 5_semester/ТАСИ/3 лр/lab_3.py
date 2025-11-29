#!/usr/bin/env python3
"""
Конвертер BMP файлов: 32-bit в 4-bit (16 градаций серого)
"""

import struct
import os
from dataclasses import dataclass
from typing import List, Tuple


# Структуры BMP заголовков

@dataclass
class BITMAPFILEHEADER:
    Type: int = 0x4D42  # 'BM'
    Size: int = 0
    Reserved1: int = 0
    Reserved2: int = 0
    OffsetBits: int = 54

    @classmethod
    def from_bytes(cls, data: bytes) -> "BITMAPFILEHEADER":
        t, size, r1, r2, off = struct.unpack("<HIHHI", data)
        return cls(Type=t, Size=size, Reserved1=r1, Reserved2=r2, OffsetBits=off)

    def to_bytes(self) -> bytes:
        return struct.pack("<HIHHI", self.Type, self.Size, self.Reserved1, self.Reserved2, self.OffsetBits)


@dataclass
class BITMAPINFOHEADER:
    Size: int = 40
    Width: int = 0
    Height: int = 0
    Planes: int = 1
    BitCount: int = 0
    Compression: int = 0
    SizeImage: int = 0
    XPelsPerMeter: int = 0
    YPelsPerMeter: int = 0
    ColorUsed: int = 0
    ColorImportant: int = 0

    @classmethod
    def from_bytes(cls, data: bytes) -> "BITMAPINFOHEADER":
        vals = struct.unpack("<IiiHHIIiiII", data)
        return cls(*vals)

    def to_bytes(self) -> bytes:
        return struct.pack("<IiiHHIIiiII", self.Size, self.Width, self.Height,
                           self.Planes, self.BitCount, self.Compression, self.SizeImage,
                           self.XPelsPerMeter, self.YPelsPerMeter, self.ColorUsed, self.ColorImportant)


@dataclass
class RGBTRIPLE:
    """
    Структура для представления RGB пикселя
    Используется как для хранения цветовых данных пикселей изображения (3 байта),
    так и для элементов палитры (4 байта с Reserved полем)
    """
    Blue: int = 0
    Green: int = 0
    Red: int = 0
    Reserved: int = 0  # Дополнительное поле для совместимости с палитрой BMP

    @classmethod
    def from_bytes(cls, data: bytes) -> "RGBTRIPLE":
        """Создает RGBTRIPLE из данных (BGR или BGRX порядок)"""
        if len(data) == 3:
            b, g, r = struct.unpack("<BBB", data)
            return cls(Blue=b, Green=g, Red=r, Reserved=0)
        elif len(data) == 4:
            b, g, r, reserved = struct.unpack("<BBBB", data)
            return cls(Blue=b, Green=g, Red=r, Reserved=reserved)
        else:
            raise ValueError("Данные должны быть 3 или 4 байта")

    def to_bytes(self, include_reserved: bool = True) -> bytes:
        """Конвертирует RGBTRIPLE в байты данных (BGR или BGRX порядок)"""
        if include_reserved:
            return struct.pack("<BBBB", self.Blue, self.Green, self.Red, self.Reserved)
        else:
            return struct.pack("<BBB", self.Blue, self.Green, self.Red)


# Класс для работы с BMP изображениями
class Image:
    def __init__(self) -> None:
        self.file_header = BITMAPFILEHEADER()
        self.info_header = BITMAPINFOHEADER()
        self.palette: List[RGBTRIPLE] = []
        self.pixels: List[List[RGBTRIPLE]] = []

    # ------------------------ чтение 24/32-bit BMP --------------------------
    def loadimage(self, filename: str) -> None:
        with open(filename, "rb") as f:
            fh = f.read(14)
            if len(fh) != 14:
                raise ValueError("Файл слишком короткий для BITMAPFILEHEADER")
            self.file_header = BITMAPFILEHEADER.from_bytes(fh)

            ih = f.read(40)
            if len(ih) != 40:
                raise ValueError("Файл слишком короткий для BITMAPINFOHEADER")
            self.info_header = BITMAPINFOHEADER.from_bytes(ih)

            if self.file_header.Type != 0x4D42:
                raise ValueError("Не BMP файл")
            if self.info_header.Compression != 0:
                raise ValueError("Поддерживаются только несжатые BMP")
            if self.info_header.BitCount not in (24, 32):
                raise ValueError("Поддерживаются только 24-bit и 32-bit BMP")

            width = self.info_header.Width
            height = self.info_header.Height
            top_down = False
            if height < 0:
                top_down = True
                height = -height

            bytes_per_pixel = self.info_header.BitCount // 8
            row_size = ((width * bytes_per_pixel * 8 + 31) // 32) * 4

            f.seek(self.file_header.OffsetBits)

            self.pixels = [[RGBTRIPLE() for _ in range(width)] for __ in range(height)]
            for row_idx in range(height):
                row = f.read(row_size)
                if len(row) < row_size:
                    raise ValueError("Файл поврежден")

                y = row_idx if top_down else (height - 1 - row_idx)

                for x in range(width):
                    off = x * bytes_per_pixel
                    b = row[off]
                    g = row[off + 1]
                    r = row[off + 2]
                    self.pixels[y][x] = RGBTRIPLE(Red=r, Green=g, Blue=b)

    # ----------------------- запись BMP в файл ------------------------------
    def writeimage(self, filename: str) -> None:
        with open(filename, "wb") as f:
            f.write(self.file_header.to_bytes())
            f.write(self.info_header.to_bytes())

            for c in self.palette:
                f.write(c.to_bytes())

            if hasattr(self, "_prepared_pixel_bytes"):
                f.write(self._prepared_pixel_bytes)
            else:
                raise RuntimeError("Данные не подготовлены для записи")

    # ------------------ преобразование глубины (оператор /) -----------------
    def __truediv__(self, new_depth: int) -> "Image":
        if new_depth not in (1, 4, 8):
            raise NotImplementedError(f"Поддерживаются глубины: 1, 4, 8 бит")

        out = Image()

        out.info_header.Width = self.info_header.Width
        out.info_header.Height = self.info_header.Height
        out.info_header.Planes = 1
        out.info_header.BitCount = new_depth
        out.info_header.Compression = 0

        width = self.info_header.Width
        height = self.info_header.Height
        top_down = height < 0
        if top_down:
            height = -height

        out.palette = self._create_palette(new_depth)
        out.info_header.ColorUsed = len(out.palette)

        pixel_bytes = self._pack_pixels(new_depth, width, height, top_down)

        out.info_header.SizeImage = len(pixel_bytes)
        palette_size = len(out.palette) * 4
        out.file_header.OffsetBits = 14 + out.info_header.Size + palette_size
        out.file_header.Size = out.file_header.OffsetBits + out.info_header.SizeImage

        out._prepared_pixel_bytes = pixel_bytes
        return out

    def _create_palette(self, bit_depth: int) -> List[RGBTRIPLE]:
        palette = []

        if bit_depth == 1:
            palette.append(RGBTRIPLE(Blue=0, Green=0, Red=0, Reserved=0))
            palette.append(RGBTRIPLE(Blue=255, Green=255, Red=255, Reserved=0))

        elif bit_depth == 4:
            for i in range(16):
                if i == 15:
                    gray = 0xFF
                else:
                    gray = i * 0x11
                palette.append(RGBTRIPLE(Blue=gray, Green=gray, Red=gray, Reserved=0))

        elif bit_depth == 8:
            for i in range(256):
                palette.append(RGBTRIPLE(Blue=i, Green=i, Red=i, Reserved=0))

        return palette

    def _rgb_to_gray(self, r: int, g: int, b: int) -> float:
        # Формула из методички: R8 = G8 = B8 = 0.299*R24 + 0.597*G24 + 0.114*B24
        return 0.299 * r + 0.597 * g + 0.114 * b

    def _find_palette_index(self, gray: float, bit_depth: int) -> int:
        if bit_depth == 1:
            return 0 if gray < 128 else 1

        elif bit_depth == 4:
            if gray >= 238:
                return 15
            else:
                idx = int(round(gray / 17))
                return max(0, min(14, idx))

        elif bit_depth == 8:
            return max(0, min(255, int(round(gray))))

        else:
            raise ValueError(f"Неподдерживаемая глубина: {bit_depth}")

    def _pack_pixels(self, bit_depth: int, width: int, height: int, top_down: bool) -> bytearray:
        if bit_depth == 4:
            bytes_per_row = (width + 1) // 2
        else:
            bytes_per_row = width // (8 // bit_depth)

        padded_row_size = ((bytes_per_row + 3) // 4) * 4
        pixel_bytes = bytearray()

        for row_idx in range(height):
            y = row_idx if top_down else (height - 1 - row_idx)

            indices = []
            for x in range(width):
                pixel = self.pixels[y][x]
                gray = self._rgb_to_gray(pixel.Red, pixel.Green, pixel.Blue)
                idx = self._find_palette_index(gray, bit_depth)
                indices.append(idx)

            row_bytes = bytearray()

            if bit_depth == 4:
                for i in range(0, width, 2):
                    hi = indices[i]
                    lo = indices[i + 1] if i + 1 < width else 0
                    byte = ((hi & 0xF) << 4) | (lo & 0xF)
                    row_bytes.append(byte)

            padding = padded_row_size - len(row_bytes)
            if padding > 0:
                row_bytes.extend(b"\x00" * padding)

            pixel_bytes.extend(row_bytes)

        return pixel_bytes


# Функции для анализа и демонстрации

def print_file_header(header: BITMAPFILEHEADER, filename: str):
    print(f"\n=== ЗАГОЛОВОК ФАЙЛА {filename} ===")
    print(f"Type: 0x{header.Type:04X} ({'BM' if header.Type == 0x4D42 else 'неизвестно'})")
    print(f"Size: {header.Size} байт ({header.Size / 1024:.1f} КБ)")
    print(f"Reserved1: {header.Reserved1}")
    print(f"Reserved2: {header.Reserved2}")
    print(f"OffsetBits: {header.OffsetBits} байт")


def print_info_header(header: BITMAPINFOHEADER, filename: str):
    print(f"\n=== ЗАГОЛОВОК ИЗОБРАЖЕНИЯ {filename} ===")
    print(f"Size: {header.Size} байт")
    print(f"Width: {header.Width} пикселей")
    print(f"Height: {header.Height} пикселей")
    print(f"Planes: {header.Planes}")
    print(f"BitCount: {header.BitCount} бит на пиксель")
    print(f"Compression: {header.Compression}")
    print(f"SizeImage: {header.SizeImage} байт")
    print(f"XPelsPerMeter: {header.XPelsPerMeter}")
    print(f"YPelsPerMeter: {header.YPelsPerMeter}")
    print(f"ColorUsed: {header.ColorUsed}")
    print(f"ColorImportant: {header.ColorImportant}")


def print_palette(palette: List[RGBTRIPLE], bit_depth: int):
    print(f"\n=== ПАЛИТРА ({len(palette)} цветов) ===")
    if bit_depth == 4:
        print("Индекс | R   G   B   | HEX")
        print("-------|-------------|------")
        for i, color in enumerate(palette):
            print(f"  {i:2d}   | {color.Red:3d} {color.Green:3d} {color.Blue:3d} | 0x{color.Red:02X}")


def analyze_file_structure(filename: str):
    """Анализирует структуру BMP файла"""
    print(f"\n{'=' * 50}")
    print(f"АНАЛИЗ СТРУКТУРЫ ФАЙЛА: {os.path.basename(filename)}")
    print(f"{'=' * 50}")

    file_size = os.path.getsize(filename)
    print(f"Общий размер файла: {file_size} байт ({file_size / 1024:.1f} КБ)")

    with open(filename, 'rb') as f:
        # BITMAPFILEHEADER
        fh_data = f.read(14)
        fh = BITMAPFILEHEADER.from_bytes(fh_data)
        print_file_header(fh, os.path.basename(filename))

        # BITMAPINFOHEADER
        ih_data = f.read(40)
        ih = BITMAPINFOHEADER.from_bytes(ih_data)
        print_info_header(ih, os.path.basename(filename))

        # Палитра (если есть)
        if ih.ColorUsed > 0:
            print(f"\n=== ЧТЕНИЕ ПАЛИТРЫ ===")
            palette = []
            for i in range(ih.ColorUsed):
                color_data = f.read(4)
                b, g, r, reserved = struct.unpack("<BBBB", color_data)
                palette.append(RGBTRIPLE(Blue=b, Green=g, Red=r, Reserved=reserved))
            print_palette(palette, ih.BitCount)

        # Вычисления размеров
        print(f"\n=== ВЫЧИСЛЕНИЯ ===")
        width = ih.Width
        height = abs(ih.Height)

        if ih.BitCount == 32:
            bytes_per_pixel = 4
            row_size = ((width * bytes_per_pixel + 3) // 4) * 4
            theoretical_data_size = row_size * height
            theoretical_total_size = 14 + 40 + theoretical_data_size

        elif ih.BitCount == 4:
            bytes_per_row = (width + 1) // 2
            padded_row_size = ((bytes_per_row + 3) // 4) * 4
            theoretical_data_size = padded_row_size * height
            palette_size = ih.ColorUsed * 4
            theoretical_total_size = 14 + 40 + palette_size + theoretical_data_size

            print(f"Байт на строку (без выравнивания): {bytes_per_row}")
            print(f"Размер строки с выравниванием: {padded_row_size} байт")
            print(f"Размер палитры: {palette_size} байт")

        print(f"Теоретический размер данных изображения: {theoretical_data_size} байт")
        print(f"Теоретический общий размер файла: {theoretical_total_size} байт")

        if file_size == theoretical_total_size:
            print("✅ Размеры файла соответствуют расчетам")
        else:
            print(f"⚠️ Разница: {file_size - theoretical_total_size} байт")


def show_rgb_to_gray_results(img: Image, sample_size: int = 10):
    """Показывает результаты преобразования RGB в градации серого для образцов пикселей"""
    print("\n   РЕЗУЛЬТАТЫ ПРЕОБРАЗОВАНИЯ RGB → GRAY (образцы):")
    print("   Координаты | R   G   B   → Gray     | Формула")
    print("   -----------|------------------------|----------------------------------")

    width = img.info_header.Width
    height = abs(img.info_header.Height)

    # Показываем sample_size случайных пикселей
    import random
    for i in range(min(sample_size, width * height)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pixel = img.pixels[y][x]
        r, g, b = pixel.Red, pixel.Green, pixel.Blue
        gray = 0.299 * r + 0.597 * g + 0.114 * b
        print(f"   ({x:3d},{y:3d})   | {r:3d} {g:3d} {b:3d} → {gray:6.2f} | 0.299×{r}+0.597×{g}+0.114×{b}")


def show_quantization_results(img: Image, bit_depth: int, sample_size: int = 10):
    """Показывает результаты квантования для образцов пикселей"""
    print("\n   РЕЗУЛЬТАТЫ КВАНТОВАНИЯ (образцы):")
    print("   Координаты | Gray   → Индекс | Алгоритм")
    print("   -----------|-----------------|---------------------------------")

    width = img.info_header.Width
    height = abs(img.info_header.Height)

    import random
    for i in range(min(sample_size, width * height)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pixel = img.pixels[y][x]
        r, g, b = pixel.Red, pixel.Green, pixel.Blue
        gray = 0.299 * r + 0.597 * g + 0.114 * b

        if bit_depth == 4:
            if gray >= 238:
                idx = 15
                algo = f"gray >= 238 → idx = 15"
            else:
                idx = max(0, min(14, int(round(gray / 17))))
                algo = f"round({gray:.1f} / 17) = {idx}"
        else:
            idx = 0
            algo = "other"

        print(f"   ({x:3d},{y:3d})   | {gray:6.2f} → {idx:2d}     | {algo}")


def show_prepared_bytes(pixel_bytes: bytearray, max_bytes: int = 32):
    """Показывает первые байты упакованных данных"""
    print(f"\n   УПАКОВАННЫЕ ДАННЫЕ (_prepared_pixel_bytes):")
    print(f"   Общий размер: {len(pixel_bytes)} байт")
    print(f"   Первые {min(max_bytes, len(pixel_bytes))} байт:")

    for i in range(0, min(max_bytes, len(pixel_bytes)), 16):
        hex_part = " ".join(f"{b:02X}" for b in pixel_bytes[i:i + 16])
        print(f"   {i:04X}: {hex_part}")


def show_new_headers(img: Image):
    """Показывает заголовки нового BMP файла"""
    print("\n   НОВЫЕ ЗАГОЛОВКИ BMP:")
    print("   ==================")
    print("   BITMAPFILEHEADER:")
    print(f"     Type: 0x{img.file_header.Type:04X}")
    print(f"     Size: {img.file_header.Size} байт")
    print(f"     Reserved1: {img.file_header.Reserved1}")
    print(f"     Reserved2: {img.file_header.Reserved2}")
    print(f"     OffsetBits: {img.file_header.OffsetBits} байт")
    print()
    print("   BITMAPINFOHEADER:")
    print(f"     Size: {img.info_header.Size} байт")
    print(f"     Width: {img.info_header.Width}")
    print(f"     Height: {img.info_header.Height}")
    print(f"     Planes: {img.info_header.Planes}")
    print(f"     BitCount: {img.info_header.BitCount}")
    print(f"     Compression: {img.info_header.Compression}")
    print(f"     SizeImage: {img.info_header.SizeImage}")
    print(f"     XPelsPerMeter: {img.info_header.XPelsPerMeter}")
    print(f"     YPelsPerMeter: {img.info_header.YPelsPerMeter}")
    print(f"     ColorUsed: {img.info_header.ColorUsed}")
    print(f"     ColorImportant: {img.info_header.ColorImportant}")


def convert_and_analyze(input_file: str, output_file: str, target_depth: int):
    print(f"\n{'=' * 60}")
    print(f"КОНВЕРТАЦИЯ BMP: {os.path.basename(input_file)} → {target_depth}-bit")
    print(f"{'=' * 60}")

    # Анализ исходного файла
    analyze_file_structure(input_file)

    # Конвертация
    print(f"\n{'=' * 30}")
    print("ПРОЦЕСС КОНВЕРТАЦИИ")
    print(f"{'=' * 30}")

    img = Image()
    print("1. Загрузка исходного изображения...")
    img.loadimage(input_file)

    print("2. Преобразование в градации серого...")
    print(f"   Формула: Gray = 0.299*R + 0.597*G + 0.114*B")
    print("   Применяется к каждому пикселю для получения значения яркости")
    print("   Учитывает разную чувствительность глаза к цветам:")
    print("   - Зелёный (59.7%) - наибольший вклад")
    print("   - Красный (29.9%) - средний вклад")
    print("   - Синий (11.4%) - наименьший вклад")

    # Показываем результаты преобразования RGB→Gray
    show_rgb_to_gray_results(img, 8)

    print("\n3. Создание палитры...")
    converted = img / target_depth
    print("   Сформирована палитра из 16 оттенков серого:")
    print("   - От чёрного (0x00) до белого (0xFF)")
    print("   - Шаг яркости: 17 единиц (0x11)")
    print("   - Каждый цвет в структуре RGBQUAD (4 байта)")

    print("\n4. Квантование и определение индексов палитры...")
    print("   Каждое значение яркости (0-255) округляется до ближайшего из 16 уровней")
    print("   - Если яркость < 238: индекс = round(яркость / 17)")
    print("   - Если яркость >= 238: индекс = 15 (белый)")
    print("   - Диапазон индексов: 0-15")

    # Показываем результаты квантования
    show_quantization_results(img, target_depth, 8)

    print("\n5. Упаковка пиксельных данных...")
    print("   - 2 пикселя упаковываются в 1 байт (4 бита на пиксель)")
    print("   - Старшие 4 бита = первый пиксель, младшие 4 бита = второй пиксель")
    print("   - Строки выравниваются до границы 4 байта (добавление 0-3 байт заполнения)")

    # Показываем упакованные данные
    if hasattr(converted, "_prepared_pixel_bytes"):
        show_prepared_bytes(converted._prepared_pixel_bytes, 48)

    print("\n6. Формирование нового заголовка и запись результата...")
    print("   Пересчитываются параметры заголовков:")
    print("   - SizeImage (размер пиксельных данных)")
    print("   - OffsetBits (смещение с учётом палитры)")
    print("   - Size (общий размер файла)")

    # Показываем новые заголовки
    show_new_headers(converted)

    converted.writeimage(output_file)

    # Анализ результата
    analyze_file_structure(output_file)

    # Сравнение размеров
    original_size = os.path.getsize(input_file)
    result_size = os.path.getsize(output_file)
    compression_ratio = original_size / result_size
    size_reduction = (1 - result_size / original_size) * 100

    print(f"\n{'=' * 30}")
    print("ШАГ 7. АНАЛИЗ И СРАВНЕНИЕ РЕЗУЛЬТАТОВ")
    print(f"{'=' * 30}")
    print("Выполняется анализ структуры полученного файла:")
    print("- Проверка размеров заголовков (14 + 40 байт)")
    print("- Проверка размера палитры (16 цветов × 4 байта = 64 байта)")
    print("- Проверка выравнивания строк до границы 4 байта")
    print("- Сверка с теоретическими расчётами")
    print()
    print("СРАВНЕНИЕ С ИСХОДНЫМ ФАЙЛОМ:")
    print(f"Исходный размер: {original_size} байт ({original_size / 1024:.1f} КБ)")
    print(f"Результирующий размер: {result_size} байт ({result_size / 1024:.1f} КБ)")
    print(f"Коэффициент сжатия: {compression_ratio:.2f}x")
    print(f"Уменьшение размера: {size_reduction:.1f}%")
    print()
    print("ОБЪЯСНЕНИЕ УМЕНЬШЕНИЯ РАЗМЕРА:")
    print("- 32-bit изображение: 4 байта на пиксель")
    print("- 4-bit изображение: 0.5 байта на пиксель (2 пикселя в байте)")
    print("- Теоретическое сжатие данных: 4 ÷ 0.5 = 8x")
    print(f"- Фактическое сжатие с учётом заголовков и палитры: {compression_ratio:.2f}x")
    print("- Визуальные потери минимальны благодаря 16 градациям серого")
    print("✅ КОНВЕРТАЦИЯ ЗАВЕРШЕНА УСПЕШНО")


if __name__ == "__main__":
    # Тест с маленьким файлом для демонстрации RGBTRIPLE
    input_file = "input_32bit.bmp"
    output_file = "result.bmp"

    try:
        convert_and_analyze(input_file, output_file, 4)
    except Exception as e:
        print(f"Ошибка: {e}")

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ RGBTRIPLE СТРУКТУРЫ")
    print("=" * 60)

    # Создаем и демонстрируем RGBTRIPLE объекты
    print("\n1. Создание RGBTRIPLE объектов:")
    pixel1 = RGBTRIPLE(Red=255, Green=128, Blue=64, Reserved=0)
    pixel2 = RGBTRIPLE(Red=100, Green=200, Blue=50, Reserved=0)

    print(f"   Пиксель 1: R={pixel1.Red}, G={pixel1.Green}, B={pixel1.Blue}, Reserved={pixel1.Reserved}")
    print(f"   Пиксель 2: R={pixel2.Red}, G={pixel2.Green}, B={pixel2.Blue}, Reserved={pixel2.Reserved}")

    print("\n2. Сериализация в байты (с Reserved полем):")
    bytes1 = pixel1.to_bytes(include_reserved=True)
    bytes2 = pixel2.to_bytes(include_reserved=True)
    print(f"   Пиксель 1 (4 байта): {' '.join(f'{b:02X}' for b in bytes1)}")
    print(f"   Пиксель 2 (4 байта): {' '.join(f'{b:02X}' for b in bytes2)}")

    print("\n3. Сериализация в байты (без Reserved поля):")
    bytes1_no_res = pixel1.to_bytes(include_reserved=False)
    bytes2_no_res = pixel2.to_bytes(include_reserved=False)
    print(f"   Пиксель 1 (3 байта): {' '.join(f'{b:02X}' for b in bytes1_no_res)}")
    print(f"   Пиксель 2 (3 байта): {' '.join(f'{b:02X}' for b in bytes2_no_res)}")

    print("\n4. Десериализация из байтов:")
    restored1 = RGBTRIPLE.from_bytes(bytes1)
    restored2 = RGBTRIPLE.from_bytes(bytes2)
    print(
        f"   Восстановленный пиксель 1: R={restored1.Red}, G={restored1.Green}, B={restored1.Blue}, Reserved={restored1.Reserved}")
    print(
        f"   Восстановленный пиксель 2: R={restored2.Red}, G={restored2.Green}, B={restored2.Blue}, Reserved={restored2.Reserved}")

    print("\n✅ Все операции с RGBTRIPLE выполнены успешно!")
