import cv2


def write_frame_diff(video_path: str, output_path: str) -> None:
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Не удалось открыть видео: " + video_path)

    ret, prev_frame = cap.read()
    if not ret:
        raise Exception("Не удалось прочитать первый кадр в видео.")

    # Переводим в grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    diff_values = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # абсолютная разница между кадрами
        diff = cv2.absdiff(gray, prev_gray)

        # средняя разница кадра (одно число)
        mean_diff = diff.mean()

        diff_values.append(mean_diff)

        prev_gray = gray

    cap.release()

    # запись результата
    with open(output_path, "w", encoding="utf-8") as f:
        for value in diff_values:
            f.write(f"{value}\n")

    print(f"Готово! Межкадровая разница записана в:\n{output_path}")


def show_graph():
    import matplotlib.pyplot as plt

    with open(
        r"C:\Users\opari\OneDrive\Рабочий стол\5_semestr_programming\Lab_8\data\frame_diff.txt", "r", encoding="utf8"
    ) as txt_file:
        data = list(map(float, txt_file))
        t = range(len(data))

        plt.plot(t, data, color="black")
        plt.title("Межкадровая разность")
        plt.xlabel("Кадры")
        plt.ylabel("МVежкадровая разность")
        plt.grid()
        plt.show()


if __name__ == "__main__":
    video_path = r"D:\video.mp4"
    output_path = r"C:\Users\opari\OneDrive\Рабочий стол\5_semestr_programming\Lab_8\data\frame_diff.txt"

    # print()
    # with open(output_path, "r", encoding="utf8") as txt_file:
    #     print(f"Максимальное  значение межкадровой разности: {max(map(float, txt_file))}")

    show_graph()
