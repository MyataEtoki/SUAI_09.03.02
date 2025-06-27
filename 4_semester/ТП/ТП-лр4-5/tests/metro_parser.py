import json

def load_metro_map(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def metro_map_to_dict(metro_data):
    metro_dict = {}
    for line in metro_data['lines']:
        line_name = line['name']
        stations = [station if isinstance(station, str) else station.get(
            'name', '') for station in line['stations']]
        metro_dict[line_name] = stations
    return metro_dict
