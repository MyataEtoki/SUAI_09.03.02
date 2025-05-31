# main.py
from metro_parser import load_metro
from pathfinder import find_shortest_path

if __name__ == "__main__":
    graph = load_metro("bucharest_metro_full.json")
    #print('Ввод станций в формате "НазваниеСтанции (НазваниеЛинии)"')
    print('Вводите станции с одним названием на разных линиях с указанием линии (M№)')
    start = input("Введите станцию отправления: ")
    end = input("Введите станцию назначения: ")

    path, total_time, transfers = find_shortest_path(graph, start, end)

    if path:
        print("Маршрут:", " → ".join(path))
        print("Общее время:", total_time, "мин")
        print("Пересадок:", transfers)
    else:
        print("Маршрут не найден.")
