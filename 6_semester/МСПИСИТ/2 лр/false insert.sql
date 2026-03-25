USE real_estate;

-- CHECK: пустое имя города
INSERT INTO cities (name) VALUES ('   ');

-- CHECK: отрицательный этаж
INSERT INTO apartments (street_id, district_id, floor) VALUES (1, 1, -1);

-- CHECK: отрицательная цена
INSERT INTO apartments (street_id, district_id, price) VALUES (1, 1, -500000);

-- NOT NULL: отсутствует street_id
INSERT INTO apartments (district_id, floor) VALUES (1, 5);

-- FOREIGN KEY: несуществующий agent_id
INSERT INTO apartments (street_id, district_id, floor, agent_id) VALUES (1, 1, 5, 999);

-- UNIQUE: дубликат серии
INSERT INTO building_series (name) VALUES ('П-44');

-- PRIMARY KEY: дубликат связи улица-район
INSERT INTO street_districts (street_id, district_id) VALUES (1, 1);