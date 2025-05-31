import heapq

def find_shortest_path(graph, start, end):
    visited = set()
    queue = [(0, start, [], 0)]  # (время, текущая станция, путь, пересадки)

    while queue:
        current_time, station, path, transfers = heapq.heappop(queue)

        if station in visited:
            continue
        visited.add(station)

        path = path + [station]

        if station == end:
            return path, current_time, transfers

        for neighbor in graph.get(station, []):
            next_station = neighbor["to"]
            time = neighbor["time"]
            is_transfer = neighbor.get("transfer", False)
            heapq.heappush(queue, (
                current_time + time,
                next_station,
                path,
                transfers + 1 if is_transfer else transfers
            ))

    return None, None, None
