import json
from collections import defaultdict

def load_metro(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    graph = defaultdict(list)

    for conn in data["connections"]:
        from_station = conn["from"]
        to_station = conn["to"]
        time = conn["time"]
        transfer = conn.get("transfer", False)

        graph[from_station].append({
            "to": to_station,
            "time": time,
            "transfer": transfer
        })

    return graph
