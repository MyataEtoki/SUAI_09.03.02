from mutagen.mp3 import MP3


def read_header(header: str) -> None:
    # header = b"fffbe204"

    bits = bin(int(header, 16)).removeprefix("0b")

    print()
    print(f"Маркер фрейма: {repr(bits[0:11])}")

    match bits[11:13]:
        case "00":
            print(f"Индекс версии MPEG: {repr(bits[11:13])}, MPEG-2.5")
        case "01":
            print(f"Индекс версии MPEG: {repr(bits[11:13])}, Не используется")
        case "10":
            print(f"Индекс версии MPEG: {repr(bits[11:13])}, MPEG-2")
        case "11":
            print(f"Индекс версии MPEG: {repr(bits[11:13])}, MPEG-1")

    match bits[13:15]:
        case "00":
            print(f"Индекс версии Layer: {repr(bits[13:15])}, Не используется")
        case "01":
            print(f"Индекс версии Layer: {repr(bits[13:15])}, Layer 3")
        case "10":
            print(f"Индекс версии Layer: {repr(bits[13:15])}, Layer 2")
        case "11":
            print(f"Индекс версии Layer: {repr(bits[13:15])}, Layer 1")

    print(f"Бит защиты: {repr(bits[15])}, {'Нет защиты' if bits[15] == '0' else 'CRC защита'}")

    print(f"Индекс битрейта, MPEG-1 Layer 3: {repr(bits[16:20])}, битрейт в кбит/с: ", end="")
    match bits[16:20]:
        case "0000":
            print("Не используется")
        case "0001":
            print(32)
        case "0010":
            print(40)
        case "0011":
            print(48)
        case "0100":
            print(56)
        case "0101":
            print(64)
        case "0110":
            print(80)
        case "0111":
            print(96)
        case "1000":
            print(112)
        case "1001":
            print(128)
        case "1010":
            print(160)
        case "1011":
            print(192)
        case "1100":
            print(224)
        case "1101":
            print(256)
        case "1110":
            print(320)
        case "1111":
            print("Не используется")

    print(f"Индекс частоты дискретизации: {repr(bits[20:22])}, для MPEG-1частота дискретизации: ", end="")
    match bits[20:22]:
        case "00":
            print("44 100 Гц")
        case "01":
            print("48 000 Гц")
        case "10":
            print("32 000 Гц")
        case "11":
            print("Не используется")

    print(f"Бит смещения: {repr(bits[22])}, {'Нет смещения' if bits[22] == '0' else 'Смещение данных на 1 байт'}")

    print(f"Бит private: {repr(bits[23])}")

    print(f"Индекс режима канала: {repr(bits[24:26])}, Режим канала: ", end="")
    match bits[24:26]:
        case "00":
            print("Stereo")
        case "01":
            print("Joint stereo")
        case "10":
            print("Dual Channel")
        case "11":
            print("Mono")

    print(f"Расширение режима канала: {repr(bits[26:28])}")
    print(f"Копирайт: {repr(bits[28])}")
    print(f"Оригинал: {repr(bits[29])}")
    print(f"Акцент: {repr(bits[30:])}")


def simple_mp3_analysis(file_path: str):
    audio = MP3(file_path)
    print(f"Размер аудиоданных: {audio.info.length * audio.info.bitrate / 8} байт")

    with open(file_path, "rb") as mp3_file:
        # Пропускаем ID3 теги если есть
        first_bytes = mp3_file.read(3)
        mp3_file.seek(0)

        if first_bytes == b"ID3":
            # Пропускаем ID3 заголовок
            id3_header = mp3_file.read(10)
            id3_size = (id3_header[6] << 21) | (id3_header[7] << 14) | (id3_header[8] << 7) | id3_header[9]
            mp3_file.seek(id3_size + 10)

        # Ищем первый MP3 фрейм
        while True:
            header = mp3_file.read(4)
            if len(header) < 4:
                break

            # Проверяем синхробайты MP3 фрейма
            if header[0] == 0xFF and (header[1] & 0xE0) == 0xE0:
                read_header(header.hex())

                break
            else:
                mp3_file.seek(mp3_file.tell() - 3)


if __name__ == "__main__":
    file_path = r"закусочная-сосисочная-4.mp3"
    simple_mp3_analysis(file_path)
