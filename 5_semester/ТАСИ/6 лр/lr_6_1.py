import struct
from dataclasses import dataclass
from pathlib import Path


@dataclass
class WavHeader:
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
        return f"""WavHeader(
    chunk_id:        {self.chunk_id}
    chunk_size:      {self.chunk_size}
    format:          {self.format}
    subchunk1_id:    {self.subchunk1_id}
    subchunk1_size:  {self.subchunk1_size}
    audio_format:    {self.audio_format} (1 = PCM)
    num_channels:    {self.num_channels}
    sample_rate:     {self.sample_rate} Hz
    byte_rate:       {self.byte_rate} B/s
    block_align:     {self.block_align} B/sample
    bits_per_sample: {self.bits_per_sample}
    subchunk2_id:    {self.subchunk2_id}
    subchunk2_size:  {self.subchunk2_size} B
)"""

    @classmethod
    def from_bytes(cls, data: bytes) -> 'WavHeader':
        if len(data) < 44:
            raise ValueError("WAV header must be at least 44 bytes")
        return cls(
            chunk_id=data[0:4].decode('ascii'),
            chunk_size=struct.unpack('<I', data[4:8])[0],
            format=data[8:12].decode('ascii'),
            subchunk1_id=data[12:16].decode('ascii'),
            subchunk1_size=struct.unpack('<I', data[16:20])[0],
            audio_format=struct.unpack('<H', data[20:22])[0],
            num_channels=struct.unpack('<H', data[22:24])[0],
            sample_rate=struct.unpack('<I', data[24:28])[0],
            byte_rate=struct.unpack('<I', data[28:32])[0],
            block_align=struct.unpack('<H', data[32:34])[0],
            bits_per_sample=struct.unpack('<H', data[34:36])[0],
            subchunk2_id=data[36:40].decode('ascii'),
            subchunk2_size=struct.unpack('<I', data[40:44])[0],
        )

    def to_bytes(self) -> bytes:
        return (
            self.chunk_id.encode('ascii') +
            struct.pack('<I', self.chunk_size) +
            self.format.encode('ascii') +
            self.subchunk1_id.encode('ascii') +
            struct.pack('<I', self.subchunk1_size) +
            struct.pack('<H', self.audio_format) +
            struct.pack('<H', self.num_channels) +
            struct.pack('<I', self.sample_rate) +
            struct.pack('<I', self.byte_rate) +
            struct.pack('<H', self.block_align) +
            struct.pack('<H', self.bits_per_sample) +
            self.subchunk2_id.encode('ascii') +
            struct.pack('<I', self.subchunk2_size)
        )

    def duration(self) -> float:
        """Возвращает длительность в секундах"""
        if self.byte_rate == 0:
            return 0.0
        return self.subchunk2_size / self.byte_rate

def read_wav_raw(file_path: Path) -> tuple[WavHeader, bytes]:
    with open(file_path, 'rb') as f:
        header_bytes = f.read(44)
        header = WavHeader.from_bytes(header_bytes)

        # Проверка формата
        if header.chunk_id != "RIFF" or header.format != "WAVE" or header.subchunk1_id != "fmt " or header.subchunk2_id != "data":
            raise ValueError("Invalid or unsupported WAV format")
        if header.audio_format != 1:
            raise ValueError("Only PCM (audioFormat=1) is supported")

        # Пропуск дополнительных байтов, если subchunk1Size > 16
        if header.subchunk1_size > 16:
            f.read(header.subchunk1_size - 16)
            # После этого идут data-чанк: читаем subchunk2Id и subchunk2Size
            extra_sub2_id = f.read(4).decode('ascii')
            extra_sub2_size = struct.unpack('<I', f.read(4))[0]
            header.subchunk2_id = extra_sub2_id
            header.subchunk2_size = extra_sub2_size

        # Читаем все аудиоданные как сырые байты
        audio_data = f.read(header.subchunk2_size)

        # Проверка: прочитали ровно столько, сколько заявлено
        if len(audio_data) != header.subchunk2_size:
            raise ValueError("Incomplete audio data")

        return header, audio_data

def split_wav_by_time(
    input_path: Path,
    t_split_sec: float,
    output1_path: Path,
    output2_path: Path
):
    header, audio_bytes = read_wav_raw(input_path)

    total_duration = header.duration()
    if not (0 < t_split_sec < total_duration):
        raise ValueError(f"t_split must be between 0 and {total_duration:.3f} sec")

    # Сколько байт нужно отрезать
    split_byte_exact = t_split_sec * header.byte_rate
    # Округляем вниз до кратного block_align
    split_byte = int(split_byte_exact // header.block_align) * header.block_align

    if split_byte <= 0 or split_byte >= len(audio_bytes):
        raise ValueError("Split point too close to edge")

    data1 = audio_bytes[:split_byte]
    data2 = audio_bytes[split_byte:]

    # Создаём новые заголовки
    def make_header(sub2_size: int) -> WavHeader:
        return WavHeader(
            chunk_id="RIFF",
            chunk_size=36 + sub2_size,  # 44 - 8 = 36
            format="WAVE",
            subchunk1_id="fmt ",
            subchunk1_size=16,
            audio_format=1,
            num_channels=header.num_channels,
            sample_rate=header.sample_rate,
            byte_rate=header.byte_rate,
            block_align=header.block_align,
            bits_per_sample=header.bits_per_sample,
            subchunk2_id="data",
            subchunk2_size=sub2_size,
        )

    header1 = make_header(len(data1))
    header2 = make_header(len(data2))

    # Запись файлов
    with open(output1_path, 'wb') as f:
        f.write(header1.to_bytes())
        f.write(data1)

    with open(output2_path, 'wb') as f:
        f.write(header2.to_bytes())
        f.write(data2)

    print(f"✅ Разделение завершено:")
    print(f"  → {output1_path.name}: {header1.duration():.3f} сек")
    print(f"  → {output2_path.name}: {header2.duration():.3f} сек")

def print_parameters(path: Path):
    header, _ = read_wav_raw(path)
    print(f"\n=== {path.name} ===")
    print(header)
    print(f"Длительность: {header.duration():.3f} сек")
    # Расчёт по формулам из методички
    num_samples = header.subchunk2_size * 8 // header.bits_per_sample
    calc_byte_rate = (header.sample_rate * header.num_channels * header.bits_per_sample) // 8
    print(f"Количество сэмплов (по формуле): {num_samples}")
    print(f"Скорость передачи байт (расчёт): {calc_byte_rate} B/s")
    print(f"BlockAlign (расчёт): {header.num_channels * (header.bits_per_sample // 8)}")


if __name__ == "__main__":
    input_file = Path("закусочная-сосисочная-3.wav")          # ← замените на ваш файл
    t_split = 1.7                           # ← время разреза в секундах
    out1 = Path("part1.wav")
    out2 = Path("part2.wav")

    # Проверка существования
    if not input_file.exists():
        raise FileNotFoundError(f"Файл {input_file} не найден")

    # Вывод параметров исходного
    print_parameters(input_file)

    # Разделение
    split_wav_by_time(input_file, t_split, out1, out2)

    # Вывод параметров выходных
    print_parameters(out1)
    print_parameters(out2)

