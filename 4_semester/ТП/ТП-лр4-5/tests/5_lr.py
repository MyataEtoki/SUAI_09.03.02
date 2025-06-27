from metro_parser import load_metro_map
from pathfinder import find_shortest_path


def user_shortest_route(metro_data):
    stations = set()
    for line in metro_data['lines']:
        for station in line['stations']:
            stations.add(station if isinstance(station, str)
                         else station.get('name', ''))
    print("Available stations:")
    for s in sorted(stations):
        print(s)
    start = input("Enter start station: ").strip()
    end = input("Enter end station: ").strip()
    path, transfers, total_time = find_shortest_path(
        metro_data, start, end)
    if path is None:
        print("No route found between the selected stations.")
    else:
        print("Shortest route:")
        print(" -> ".join(path))
        print(f"Number of transfers: {transfers}")
        print(f"Total travel time: {total_time} minutes")

if __name__ == "__main__":
    metro_data = load_metro_map('../metro.json')
    metro_dict = metro_map_to_dict(metro_data)
    draw_metro_map(metro_data)
    user_shortest_route(metro_data)
