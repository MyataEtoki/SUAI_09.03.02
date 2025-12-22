import wave
import struct
import sys

def read_wav_info(filepath):
    with wave.open(filepath, 'rb') as wav:
        params = wav.getparams()
        print("=== Параметры исходного WAV-файла ===")
        print(f"Количество каналов (numChannels):     {params.nchannels}")
        print(f"Частота дискретизации (sampleRate):  {params.framerate} Гц")
        print(f"Бит на сэмпл (bitsPerSample):        {params.sampwidth * 8}")
        print(f"Общее число фреймов:                 {params.nframes}")
        print(f"Режим сжатия (audioFormat):          {'PCM' if params.comptype == 'NONE' else params.comptype}")
        duration = params.nframes / params.framerate
        print(f"Длительность:                        {duration:.3f} сек")
        print("=" * 40)
        return params, duration

def split_wav_by_time(input_path, t_split_sec, output1_path, output2_path):
    with wave.open(input_path, 'rb') as wav_in:
        params = wav_in.getparams()
        nchannels = params.nchannels
        sampwidth = params.sampwidth
        framerate = params.framerate
        nframes = params.nframes

        # Проверка: t_split не должен превышать длительность
        total_duration = nframes / framerate
        if t_split_sec <= 0 or t_split_sec >= total_duration:
            raise ValueError(f"Время разреза должно быть в диапазоне (0, {total_duration:.3f}) сек")

        # Количество фреймов до точки разреза
        split_frame = int(t_split_sec * framerate)

        # Читаем все данные
        frames = wav_in.readframes(nframes)

        # Определяем размер одного фрейма в байтах
        frame_size = nchannels * sampwidth  # = blockAlign

        # Вычисляем байтовый сдвиг
        split_byte = split_frame * frame_size

        # Делим данные
        data1 = frames[:split_byte]
        data2 = frames[split_byte:]

        # Создаём выходные файлы
        with wave.open(output1_path, 'wb') as out1:
            out1.setparams((nchannels, sampwidth, framerate, split_frame, params.comptype, params.compname))

        with wave.open(output2_path, 'wb') as out2:
            out2.setparams((nchannels, sampwidth, framerate, nframes - split_frame, params.comptype, params.compname))

        # Записываем данные
        with wave.open(output1_path, 'wb') as out1:
            out1.setparams((nchannels, sampwidth, framerate, split_frame, params.comptype, params.compname))
            out1.writeframes(data1)

        with wave.open(output2_path, 'wb') as out2:
            out2.setparams((nchannels, sampwidth, framerate, nframes - split_frame, params.comptype, params.compname))
            out2.writeframes(data2)

        print(f"\n✅ Файл успешно разделён по времени {t_split_sec} сек:")
        print(f"   → {output1_path} ({split_frame / framerate:.3f} сек)")
        print(f"   → {output2_path} ({(nframes - split_frame) / framerate:.3f} сек)")


if __name__ == "__main__":
    input_file = "закусочная-сосисочная-3.wav"          # ← замени на свой файл
    t_split = 1.7                     # ← время разреза в секундах
    part1 = "part1.wav"
    part2 = "part2.wav"

    # Шаг 1: Вывести параметры исходного файла
    params, total_dur = read_wav_info(input_file)

    # Шаг 2: Разделить
    split_wav_by_time(input_file, t_split, part1, part2)

    # Шаг 3: Вывести параметры выходных файлов
    print("\n=== Параметры выходных файлов ===")
    read_wav_info(part1)
    read_wav_info(part2)