import json

# Список станций и соединений по линиям, основываясь на карте
lines = {
    "M1": [
        "Pantelimon", "Republica", "Costin Georgian", "Titan", "Nicolae Grigorescu (M1)",
        "1 Decembrie 1918", "Dristor 2", "Dristor 1 (M1)", "Piața Muncii", "Iancului",
        "Obor", "Ștefan cel Mare", "Piața Victoriei (M1)", "Gara de Nord (M1)",
        "Basarab (M1)", "Crângași", "Petrache Poenaru", "Grozăvești", "Politehnica",
        "Eroilor (M1)", "Izvor (M1)", "Piața Unirii (M1)", "Timpuri Noi", "Mihai Bravu",
        "Dristor 1 (M1)"
    ],
    "M2": [
        "Pipera", "Aurel Vlaicu", "Aviatorilor", "Piața Victoriei (M2)", "Piața Romană",
        "Universitate", "Piața Unirii (M2)", "Tineretului", "Eroii Revoluției",
        "Constantin Brâncoveanu", "Piața Sudului", "Apărătorii Patriei", "IMGB",
        "Depoul IMGB"
    ],
    "M3": [
        "Preciziei", "Păcii", "Gorjului", "Lujerului", "Politehnica", "Eroilor (M3)",
        "Izvor (M3)", "Piața Unirii (M3)", "Timpuri Noi", "Mihai Bravu", "Dristor 1 (M3)",
        "Nicolae Grigorescu (M3)", "1 Decembrie 1918", "Nicolae Teclu", "Anghel Saligny"
    ],
    "M4": [
        "Gara de Nord (M4)", "Basarab (M4)", "Grivița", "1 Mai", "Parc Bazilescu", "Laminorului", "Străulești"
    ]
}

# Пересадочные станции (со временем пересадки 4 минуты)
transfers = [
    ("Dristor 1 (M1)", "Dristor 1 (M3)"),
    ("Nicolae Grigorescu (M1)", "Nicolae Grigorescu (M3)"),
    ("Piața Unirii (M1)", "Piața Unirii (M2)"),
    ("Piața Unirii (M1)", "Piața Unirii (M3)"),
    ("Piața Unirii (M2)", "Piața Unirii (M3)"),
    ("Eroilor (M1)", "Eroilor (M3)"),
    ("Izvor (M1)", "Izvor (M3)"),
    ("Politehnica", "Politehnica"),  # общая станция
    ("Piața Victoriei (M1)", "Piața Victoriei (M2)"),
    ("Gara de Nord (M1)", "Gara de Nord (M4)"),
    ("Basarab (M1)", "Basarab (M4)")
]

# Построение JSON-структур
stations = []
connections = []

# Добавляем станции
for line, stops in lines.items():
    for stop in stops:
        stations.append({
            "name": stop,
            "line": line
        })

# Добавляем соединения между станциями на линии (время — 2 мин)
for stops in lines.values():
    for i in range(len(stops) - 1):
        connections.append({
            "from": stops[i],
            "to": stops[i + 1],
            "time": 2
        })

# Добавляем пересадки
for from_station, to_station in transfers:
    if from_station != to_station:  # настоящая пересадка
        connections.append({
            "from": from_station,
            "to": to_station,
            "time": 4
        })
        connections.append({
            "from": to_station,
            "to": from_station,
            "time": 4
        })

# Собираем всё в словарь
metro_data = {
    "stations": stations,
    "connections": connections,
    "transfer_time": 4
}

# Сохраняем в JSON
output_path = "bucharest_metro_full.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(metro_data, f, ensure_ascii=False, indent=2)

output_path
