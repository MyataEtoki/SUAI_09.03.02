import ffmpeg


def get_mp4_info(path: str) -> None:
    try:
        probe = ffmpeg.probe(path)

        # Достаём данные видео-потока
        video_streams = [s for s in probe["streams"] if s["codec_type"] == "video"]
        audio_streams = [s for s in probe["streams"] if s["codec_type"] == "audio"]

        print("=== Основная информация о файле ===")
        print("Формат:", probe["format"]["format_name"])
        print("Длительность (сек):", probe["format"]["duration"])
        print("Размер файла (байт):", probe["format"]["size"])
        print("Битрейт:", probe["format"]["bit_rate"])

        if video_streams:
            v = video_streams[0]
            print("\n=== Видео ===")
            print("Кодек:", v.get("codec_name"))
            print("Разрешение:", f"{v.get('width')}x{v.get('height')}")
            print("FPS:", v.get("avg_frame_rate"))
            print("Битрейт:", v.get("bit_rate"))

        if audio_streams:
            a = audio_streams[0]
            print("\n=== Аудио ===")
            print("Кодек:", a.get("codec_name"))
            print("Частота дискретизации:", a.get("sample_rate"))
            print("Каналы:", a.get("channels"))

    except ffmpeg.Error as e:
        print("Ошибка FFmpeg:", e)


# Пример вызова
video_path = r"C:\Users\opari\OneDrive\Рабочий стол\5_semestr_programming\Lab_8\data\usa_video.mp4"
print()
get_mp4_info(video_path)
