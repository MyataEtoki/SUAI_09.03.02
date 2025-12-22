def write_frames_info(all_frames_path: str, i_frames_info_path: str, p_frames_info_path: str) -> None:
    with (
        open(all_frames_path, "r", encoding="utf") as all_frames_file,
        open(i_frames_info_path, "w", encoding="utf8") as i_file,
        open(p_frames_info_path, "w", encoding="utf8") as p_file,
    ):
        all_frames_file.read(1)

        # 5 - Временная метка в секундах
        # 22 - тип кадра

        for line in all_frames_file:
            line_info = line.split("|")
            match line_info[22]:
                case "pict_type=I":
                    print(f"{line_info[22]}: {line_info[5]}", file=i_file)
                case "pict_type=P":
                    print(f"{line_info[22]}: {line_info[5]}", file=p_file)


if __name__ == "__main__":
    all_frames_path = r"Lab_8\data\frames_info.txt"
    i_frames_info_path = r"Lab_8\data\i_frames_info.txt"
    p_frames_info_path = r"Lab_8\data\p_frames_info.txt"

    write_frames_info(all_frames_path, i_frames_info_path, p_frames_info_path)
