"""Работа с wav файлами"""

import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Self


@dataclass
class WavHeader:
    """Заголовок wav файла"""

    chunk_id: str
    chunk_size: int
    format: str
    subchunk1_id: str
    subchunk1_size: int
    audio_format: int
    num_channels: int
    sample_rate: int
    byte_rate: int
    block_align: int
    bits_per_sample: int
    subchunk2_id: str
    subchunk2_size: int

    def __str__(self) -> str:
        return f"""{__class__.__name__}(
chunk_id:        {repr(self.chunk_id)}
chunk_size:      {self.chunk_size}
format:          {repr(self.format)}
subchunk1_id:    {repr(self.subchunk1_id)}
subchunk1_size:  {self.subchunk1_size}
audio_format:    {self.audio_format}
num_channels:    {self.num_channels}
sample_rate:     {self.sample_rate}
byte_rate:       {self.byte_rate}
block_align:     {self.block_align}
bits_per_sample: {self.bits_per_sample}
subchunk2_id:    {repr(self.subchunk2_id)}
subchunk2_size:  {self.subchunk2_size}
)"""

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Создает WavHeader из байтов заголовка WAV файла"""

        # Парсинг основного заголовка
        chunk_id = data[0:4].decode("ascii")
        chunk_size = struct.unpack("<I", data[4:8])[0]
        format = data[8:12].decode("ascii")

        # Парсинг подзаголовка fmt
        subchunk1_id = data[12:16].decode("ascii")
        subchunk1_size = struct.unpack("<I", data[16:20])[0]
        audio_format = struct.unpack("<H", data[20:22])[0]
        num_channels = struct.unpack("<H", data[22:24])[0]
        sample_rate = struct.unpack("<I", data[24:28])[0]
        byte_rate = struct.unpack("<I", data[28:32])[0]
        block_align = struct.unpack("<H", data[32:34])[0]
        bits_per_sample = struct.unpack("<H", data[34:36])[0]

        # Парсинг подзаголовка data
        subchunk2_id = data[36:40].decode("ascii")
        subchunk2_size = struct.unpack("<I", data[40:44])[0]

        return cls(
            chunk_id=chunk_id,
            chunk_size=chunk_size,
            format=format,
            subchunk1_id=subchunk1_id,
            subchunk1_size=subchunk1_size,
            audio_format=audio_format,
            num_channels=num_channels,
            sample_rate=sample_rate,
            byte_rate=byte_rate,
            block_align=block_align,
            bits_per_sample=bits_per_sample,
            subchunk2_id=subchunk2_id,
            subchunk2_size=subchunk2_size,
        )

    def to_bytes(self) -> bytes:
        """Конвертирует WavHeader в байты для записи в файл"""
        header_bytes = b""

        # Основной заголовок
        header_bytes += self.chunk_id.encode("ascii")
        header_bytes += struct.pack("<I", self.chunk_size)
        header_bytes += self.format.encode("ascii")

        # Подзаголовок fmt
        header_bytes += self.subchunk1_id.encode("ascii")
        header_bytes += struct.pack("<I", self.subchunk1_size)
        header_bytes += struct.pack("<H", self.audio_format)
        header_bytes += struct.pack("<H", self.num_channels)
        header_bytes += struct.pack("<I", self.sample_rate)
        header_bytes += struct.pack("<I", self.byte_rate)
        header_bytes += struct.pack("<H", self.block_align)
        header_bytes += struct.pack("<H", self.bits_per_sample)

        # Подзаголовок data
        header_bytes += self.subchunk2_id.encode("ascii")
        header_bytes += struct.pack("<I", self.subchunk2_size)

        return header_bytes


def read_wav_file(file_path: Path) -> tuple[WavHeader, list[int]]:
    """Читает WAV файл и возвращает заголовок и аудиоданные"""
    with open(file_path, "rb") as f:
        # Чтение всего заголовка (44 байта)
        header_data = f.read(44)
        header = WavHeader.from_bytes(header_data)

        # Пропускаем возможные дополнительные поля между подзаголовками
        if header.subchunk1_size > 16:
            f.read(header.subchunk1_size - 16)

            # Перечитываем subchunk2_id и subchunk2_size
            subchunk2_id = f.read(4).decode("ascii")
            subchunk2_size = struct.unpack("<I", f.read(4))[0]
            header.subchunk2_id = subchunk2_id
            header.subchunk2_size = subchunk2_size

        # Чтение аудиоданных
        bytes_per_sample = header.bits_per_sample // 8
        num_samples = header.subchunk2_size // bytes_per_sample

        audio_data = []
        for _ in range(num_samples):
            match header.bits_per_sample:
                case 16:
                    sample = struct.unpack("<h", f.read(2))[0]
                case 8:
                    sample = struct.unpack("<B", f.read(1))[0]
                case _:
                    raise ValueError(f"Unsupported bits per sample: {header.bits_per_sample}")
            audio_data.append(sample)

        return header, audio_data


def merge_mono_to_stereo(path_to_left_mono: Path, path_to_right_mono: Path, path_to_out_file: Path) -> None:
    """
    Объединяет два моно WAV файла в один стерео WAV файл.
    """
    # Чтение входных файлов
    left_header, left_data = read_wav_file(path_to_left_mono)
    right_header, right_data = read_wav_file(path_to_right_mono)

    if len(left_data) != len(right_data):
        # Если длины разные, используем минимальную длину
        min_length = min(len(left_data), len(right_data))
        left_data = left_data[:min_length]
        right_data = right_data[:min_length]

    # Создание стерео данных (чередование левого и правого каналов)
    stereo_data = []
    for left_sample, right_sample in zip(left_data, right_data):
        stereo_data.append(left_sample)  # левый канал
        stereo_data.append(right_sample)  # правый канал

    # Расчет параметров для нового заголовка
    bits_per_sample = left_header.bits_per_sample
    bytes_per_sample = bits_per_sample // 8
    num_channels = 2  # стерео
    block_align = num_channels * bytes_per_sample
    byte_rate = left_header.sample_rate * block_align
    subchunk2_size = len(stereo_data) * bytes_per_sample
    chunk_size = 36 + subchunk2_size  # 36 = размер заголовка без chunk_id и chunk_size

    # Создание нового заголовка
    new_header = WavHeader(
        chunk_id="RIFF",
        chunk_size=chunk_size,
        format="WAVE",
        subchunk1_id="fmt ",
        subchunk1_size=16,
        audio_format=1,  # PCM
        num_channels=num_channels,
        sample_rate=left_header.sample_rate,
        byte_rate=byte_rate,
        block_align=block_align,
        bits_per_sample=bits_per_sample,
        subchunk2_id="data",
        subchunk2_size=subchunk2_size,
    )

    # Запись выходного файла
    with open(path_to_out_file, "wb") as f:
        # Запись заголовка
        f.write(new_header.to_bytes())

        # Запись аудиоданных
        for sample in stereo_data:
            if bits_per_sample == 16:
                f.write(struct.pack("<h", sample))
            elif bits_per_sample == 8:
                f.write(struct.pack("<B", sample))


def calculate_parameters(path_to_wav_file: Path):
    header, _ = read_wav_file(path_to_wav_file)

    print(f"Количество сэмплов: {header.subchunk2_size * 8 // header.bits_per_sample}")
    print(f"Количество байт в секунду: {header.sample_rate * header.block_align}")
    print(f"Размер блока: {header.block_align}")
    print(f"Количество значащих байт на выборку: {header.bits_per_sample}")
    print(f"Скорость передачи байт: {(header.sample_rate * header.num_channels * header.bits_per_sample) // 8}")
    print(
        f"Время воспроизведения: {(header.chunk_size + 8) / ((header.sample_rate * header.num_channels * header.bits_per_sample) // 8)}"
    )


# Пример использования
if __name__ == "__main__":
    left_file = Path(r"ТехникаАудиовизуальных\data\Lab_6_data\left.wav")
    right_file = Path(r"ТехникаАудиовизуальных\data\Lab_6_data\right.wav")
    output_file = Path(r"ТехникаАудиовизуальных\data\Lab_6_data\stereo_file_merged.wav")

    # merge_mono_to_stereo(left_file, right_file, output_file)
    # print(f"Стерео файл сохранен как: {output_file}")

    # print(read_wav_file(left_file)[0])
    # print(read_wav_file(right_file)[0])
    # print(read_wav_file(output_file)[0])
