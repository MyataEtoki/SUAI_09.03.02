import matplotlib.pyplot as plt
import json
import networkx as nx
import heapq


def load_metro_map(json_file):
    """Парсер json схемы метро"""
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def metro_map_to_dict(metro_data):
    """Преобразуем текстовою схему в удобный словарь"""
    metro_dict = {}
    for line in metro_data['lines']:
        line_name = line['name']
        stations = [station if isinstance(station, str) else station.get(
            'name', '') for station in line['stations']]
        metro_dict[line_name] = stations
    return metro_dict


def travel_time_dict(metro_data):
    """Для расчёта времени в пути"""
    return metro_data.get("travel_time", {})


def find_shortest_path(metro_data, start_station, end_station, transfer_time=5, default_travel_time=3):

    travel_times = travel_time_dict(metro_data)
    station_lines = {}
    line_stations = {}

    #TODO: надо объединить с metro_map_to_dict()
    """считываем инфу о станциях"""
    for line in metro_data['lines']:
        line_name = line['name']
        stations = [station if isinstance(station, str) else station.get(
            'name', '') for station in line['stations']]
        line_stations[line_name] = stations
        for station in stations:
            station_lines.setdefault(station, set()).add(line_name)

    heap = []
    visited = {}

    # забиваем очередь кортежами из линий, где есть стартовая станция
    for line in station_lines.get(start_station, []):
        heapq.heappush(heap, (0, 0, start_station,
                       line, [(start_station, line)]))

    best_path = None
    best_cost = float('inf')
    best_transfers = None

    while heap:
        # берём путь с мин временем
        cost, transfers, station, line, path = heapq.heappop(heap)
        key = (station, line)
        if key in visited and visited[key] <= cost: #скипаем путь, если быстрее уже было
            continue
        visited[key] = cost

        if station == end_station:
            transfer_count = sum(1 for i in range(
                1, len(path)) if path[i][1] != path[i-1][1]) #считаем пересадки по изменению линии в пути
            if cost < best_cost:
                best_cost = cost
                best_path = path
                best_transfers = transfer_count
            continue

        stations = line_stations[line]
        idx = stations.index(station)
        #смотрим для каждой станции соседей, и для каждого соседа время до него - разведываем маршруты
        for next_idx in [idx - 1, idx + 1]:
            if 0 <= next_idx < len(stations):
                next_station = stations[next_idx]
                t = travel_times.get(line, {}).get(
                    station, default_travel_time) #время в пути до след станции
                heapq.heappush(
                    heap, (cost + t, transfers, next_station, line, path + [(next_station, line)]))

        #смотрим пути с пересадками на другие линии, если есть возможность
        for other_line in station_lines[station]:
            if other_line != line:
                heapq.heappush(heap, (cost + transfer_time, transfers + 1,
                               station, other_line, path + [(station, other_line)]))

    if best_path is None:
        return None, None, None

    station_path = [station for station, _ in best_path]
    return station_path, best_transfers, best_cost


def user_data(metro_data):
    """Работа с выводом инфы в консоль из файла метро, ввод из консоли точек маршрута пользователем"""
    stations = set()
    for line in metro_data['lines']:
        for station in line['stations']:
            stations.add(station if isinstance(station, str)
                         else station.get('name', ''))
    print("Ух ты, вот это станции:")
    for s in sorted(stations):
        print(s)
    start = input("Я здеся: ").strip()
    end = input("А хочу сюда: ").strip()
    path, transfers, total_time = find_shortest_path(
        metro_data, start, end)
    if path is None:
        print("Блин, маршрут между станциями не найден.")
    else:
        print("Короткая дорожка:")
        print(" -> ".join(path))
        print(f"Пересадок: {transfers}")
        print(f"Всего ехать: {total_time} минуток")


if __name__ == "__main__":
    metro_data = load_metro_map('metro.json')
    user_data(metro_data)
