import cv2
import numpy as np
import os


def extract_max_diff_frames(video_path, output_dir="output_frames"):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Не удалось открыть видео: {video_path}")

    prev_frame_gray = None
    max_diff_value = 0
    max_diff_frames = (None, None)
    frame_index = 0
    best_index = -1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame_gray is not None:
            diff = cv2.absdiff(gray, prev_frame_gray)
            diff_value = np.sum(diff)

            if diff_value > max_diff_value:
                max_diff_value = diff_value
                max_diff_frames = (prev_frame.copy(), frame.copy())
                best_index = frame_index

        prev_frame_gray = gray
        prev_frame = frame
        frame_index += 1

    cap.release()

    if max_diff_frames[0] is None:
        raise RuntimeError("Недостаточно кадров для анализа")

    frame1_path = os.path.join(output_dir, "frame_max_diff_1.jpg")
    frame2_path = os.path.join(output_dir, "frame_max_diff_2.jpg")

    cv2.imwrite(frame1_path, max_diff_frames[0])
    cv2.imwrite(frame2_path, max_diff_frames[1])

    diff_image = cv2.absdiff(
        cv2.cvtColor(max_diff_frames[0], cv2.COLOR_BGR2GRAY), cv2.cvtColor(max_diff_frames[1], cv2.COLOR_BGR2GRAY)
    )

    # Нормализация для лучшей визуализации
    diff_image_norm = cv2.normalize(diff_image, None, 0, 255, cv2.NORM_MINMAX)

    diff_path = os.path.join(output_dir, "frame_difference.jpg")
    cv2.imwrite(diff_path, diff_image_norm)

    return {
        "frame1": frame1_path,
        "frame2": frame2_path,
        "difference_image": diff_path,
        "difference_value": int(max_diff_value),
        "second_frame_index": best_index,
    }


if __name__ == "__main__":
    video_file = r"Lab_8\data\usa_video.mp4"  # путь к mp4 файлу
    result = extract_max_diff_frames(video_file)
    print("Сохранены кадры с максимальной разностью:")
    for k, v in result.items():
        print(f"{k}: {v}")
