import heapq
import random

def packet_processing(size, n, packets, failure_probability=0.1, max_wait_time=5):
    current_time = 0
    result = []
    buffer = []  # Это будет хранить (время_окончания_обработки, длительность, время_прихода)
    arrivals = []  # Очередь для поступающих пакетов

    # Добавляем пакеты в arrivals с приоритетом
    for arrival, duration in packets:
        heapq.heappush(arrivals, (arrival, duration))

    while arrivals:
        arrival, duration = heapq.heappop(arrivals)
        # Вычисляем полное время, которое пакет пробыл в системе
        total_wait_time = current_time - arrival
        # Удаляем завершенные пакеты из буфера (смотрим время прибытия)
        while buffer and buffer[0][0] <= arrival:
            buffer.pop(0)

        # Проверяем размеры буфера
        if len(buffer) < size:
            # Устанавливаем время начала обработки
            start_time = max(current_time, arrival)
            # Проверяем время нахождения в системе
            if total_wait_time > max_wait_time:
                print("Пакет отброшен из-за превышения времени ожидания!")
                result.append(-1)  # Пакет отброшен
                continue

            if random.random() < failure_probability:
                print("Сбой!")
                result.append(-1)
                # Удвоение времени обработки и добавление в очередь
                new_duration = min(duration * 2, 100)  # Ограничиваем максимальное время (например, 100)
                heapq.heappush(arrivals, (arrival, new_duration))
            else:
                # Пакет успешно обработан
                result.append(start_time)
                # Обновляем текущее время
                current_time = start_time + duration
                # Добавляем пакет в буфер с временем окончания и временем прибытия
                heapq.heappush(buffer, (current_time, duration, arrival))
        else:
            print("Буфер переполнен")
            result.append(-1)  # Буфер переполнен

    return result

# Пример использования
size, n = 1, 2  # размер буфера и кол-во пакетов
max_wait_time = 5  # максимальное время ожидания
input_data = [
    (0, 1),
    (1, 1)
]  # когда пришёл, вес

output = packet_processing(size, n, input_data, max_wait_time=max_wait_time-1)
for time in output:
    print(time)
