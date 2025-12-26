import os
import ffmpeg
import cv2
import matplotlib.pyplot as plt
import subprocess
import json


# =============================
# 1. Считать параметры заголовка и вывести данные (через ffprobe)
# =============================
def get_mp4_info(path: str) -> None:
    try:
        probe = ffmpeg.probe(path)

        # Основной формат
        fmt = probe["format"]
        print("=== Основная информация о файле ===")
        print("Формат:", fmt.get("format_name"))
        print("Длительность (сек):", fmt.get("duration"))
        print("Размер файла (байт):", fmt.get("size"))
        print("Битрейт:", fmt.get("bit_rate"))

        # Видео- и аудиопотоки
        video_streams = [s for s in probe["streams"] if s["codec_type"] == "video"]
        audio_streams = [s for s in probe["streams"] if s["codec_type"] == "audio"]

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
        print("Ошибка FFmpeg при чтении метаданных:", e.stderr.decode())
        raise

# =============================
# 2. Сохранить до 100 кадров в JPG (через ffmpeg)
# =============================
def extract_100_frames(video_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    output_pattern = os.path.join(output_dir, "frame_%03d.jpg")
    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_pattern, vframes=1000, loglevel="quiet")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f"✅ Сохранено до 100 кадров в: {output_dir}")
    except ffmpeg.Error as e:
        print("Ошибка при извлечении кадров:", e.stderr.decode())
        raise

# =============================
# 3–4. Получить временные метки I- и P-кадров
# =============================
def extract_frame_types(video_path: str, all_frames_path: str):
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_frames",
        "-select_streams", "v:0",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print("Ошибка ffprobe:", result.stderr)
        raise RuntimeError("Не удалось получить информацию о кадрах")

    data = json.loads(result.stdout)
    frames = data.get("frames", [])

    with open(all_frames_path, "w", encoding="utf-8") as f:
        for frame in frames:
            t = frame.get("best_effort_timestamp_time", "0")
            typ = frame.get("pict_type", "N/A")
            f.write(f"{t},{typ}\n")

    print(f"✅ Сохранено {len(frames)} кадров в: {all_frames_path}")

def split_i_p_frames(all_frames_path: str, i_path: str, p_path: str):
    with open(all_frames_path, "r", encoding="utf-8") as fin, \
         open(i_path, "w", encoding="utf-8") as fi, \
         open(p_path, "w", encoding="utf-8") as fp:

        for line in fin:
            parts = line.strip().split(',')
            if len(parts) != 2:
                continue
            frame_type, timestamp = parts
            if frame_type == "I":
                fi.write(f"pict_type=I: {timestamp}\n")
            elif frame_type == "P":
                fp.write(f"pict_type=P: {timestamp}\n")
    print(f"✅ I-кадры → {i_path}")
    print(f"✅ P-кадры → {p_path}")

# =============================
# 5. Межкадровая разность (через OpenCV — быстрее и проще)
# =============================
def compute_frame_diff(video_path: str, diff_path: str) -> float:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Не удалось открыть видео для вычисления разности")

    ret, prev = cap.read()
    if not ret:
        raise RuntimeError("Видео пустое")
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    diffs = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray, prev_gray)
        diffs.append(float(diff.mean()))
        prev_gray = gray

    cap.release()

    with open(diff_path, "w", encoding="utf-8") as f:
        for d in diffs:
            f.write(f"{d}\n")

    max_diff = max(diffs) if diffs else 0.0
    print(f"✅ Максимальная межкадровая разность: {max_diff:.2f}")
    return max_diff

# =============================
# 6. Визуализация векторов движения (требует ffmpeg с фильтром `motion_vectors`)
# =============================
def create_motion_vectors_video(input_path: str, output_path: str):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vf="codecview=mv=pf+bf+bb",  # отображает motion vectors
                vcodec="libx264",
                acodec="copy",
                loglevel="quiet"
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f"✅ Видео с векторами движения сохранено: {output_path}")
    except ffmpeg.Error as e:
        print("Ошибка при создании видео с векторами движения:", e.stderr.decode())
        raise

# =============================
# Основной запуск
# =============================
if __name__ == "__main__":
    # Укажи свой путь
    video_path = r"C:\Users\etoki\Documents\SUAI_09.03.02\5_semester\ТАСИ\8 лр\Футаж_PIXEL_light_and_sun.mp4"
    data_dir = "Lab_8/data"
    os.makedirs(data_dir, exist_ok=True)

    # 1. Информация о файле
    get_mp4_info(video_path)
    print()

    # 2. 100 кадров в JPG
    extract_100_frames(video_path, os.path.join(data_dir, "frames"))
    print()

    # 3–4. I и P кадры
    all_frames_txt = os.path.join(data_dir, "frames_info.txt")
    extract_frame_types(video_path, all_frames_txt)
    split_i_p_frames(
        all_frames_txt,
        os.path.join(data_dir, "i_frames_info.txt"),
        os.path.join(data_dir, "p_frames_info.txt")
    )
    print()

    # 5. Межкадровая разность
    diff_file = os.path.join(data_dir, "frame_diff.txt")
    compute_frame_diff(video_path, diff_file)
    print()

    # 6. Видео с векторами движения
    motion_video = os.path.join(data_dir, "motion_vectors.mp4")
    create_motion_vectors_video(video_path, motion_video)
    print()
"""
    # Доп: график разности (если нужно)
    with open(diff_file, "r") as f:
        diffs = [float(x) for x in f]
    plt.plot(diffs, color="black")
    plt.title("Межкадровая разность")
    plt.xlabel("Кадр")
    plt.ylabel("Средняя абсолютная разность")
    plt.grid(True)
    plt.show()
"""