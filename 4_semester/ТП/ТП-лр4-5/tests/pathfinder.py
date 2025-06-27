import heapq


def travel_time_dict(metro_data):
    return metro_data.get("travel_time", {})


def find_shortest_path(metro_data, start_station, end_station, transfer_time=5, default_travel_time=3):
    travel_times = travel_time_dict(metro_data)
    station_lines = {}
    line_stations = {}

    for line in metro_data['lines']:
        line_name = line['name']
        stations = [station if isinstance(station, str) else station.get(
            'name', '') for station in line['stations']]
        line_stations[line_name] = stations
        for station in stations:
            station_lines.setdefault(station, set()).add(line_name)

    heap = []
    visited = {}

    for line in station_lines.get(start_station, []):
        heapq.heappush(heap, (0, 0, start_station,
                       line, [(start_station, line)]))

    best_path = None
    best_cost = float('inf')
    best_transfers = None

    while heap:
        cost, transfers, station, line, path = heapq.heappop(heap)
        key = (station, line)
        if key in visited and visited[key] <= cost:
            continue
        visited[key] = cost

        if station == end_station:
            transfer_count = sum(1 for i in range(
                1, len(path)) if path[i][1] != path[i-1][1])
            if cost < best_cost:
                best_cost = cost
                best_path = path
                best_transfers = transfer_count
            continue

        stations = line_stations[line]
        idx = stations.index(station)
        for next_idx in [idx - 1, idx + 1]:
            if 0 <= next_idx < len(stations):
                next_station = stations[next_idx]
                t = travel_times.get(line, {}).get(
                    station, default_travel_time)
                heapq.heappush(
                    heap, (cost + t, transfers, next_station, line, path + [(next_station, line)]))

        for other_line in station_lines[station]:
            if other_line != line:
                heapq.heappush(heap, (cost + transfer_time, transfers + 1,
                               station, other_line, path + [(station, other_line)]))

    if best_path is None:
        return None, None, None

    station_path = [station for station, _ in best_path]
    return station_path, best_transfers, best_cost


