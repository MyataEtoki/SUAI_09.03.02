USE real_estate;

-- Города
INSERT INTO cities (name) VALUES 
('Москва'),
('Санкт-Петербург'),
('Казань');

-- Районы
INSERT INTO districts (name, city_id) VALUES 
('Центральный', 1),
('Западный', 1),
('Невский', 2),
('Вахитовский', 3);

-- Улицы
INSERT INTO streets (name) VALUES 
('Тверская'),
('Арбат'),
('Невский проспект'),
('Баумана');

-- Связь улиц и районов (многие-ко-многим)
INSERT INTO street_districts (street_id, district_id) VALUES 
(1, 1),  -- Тверская в Центральном
(1, 2),  -- Тверская также в Западном (улица через 2 района)
(2, 1),  -- Арбат в Центральном
(3, 3),  -- Невский в Невском
(4, 3);  -- Баумана в Вахитовском

-- Агенты
INSERT INTO agents (last_name, first_name, middle_name) VALUES 
('Иванов', 'Иван', 'Иванович'),
('Петров', 'Петр', NULL),
('Сидорова', 'Анна', 'Сергеевна');

-- Строительные серии
INSERT INTO building_series (name) VALUES 
('П-44'),
('Хрущевка'),
('Сталинка');

-- Квартиры (корректные данные)
INSERT INTO apartments (street_id, district_id, floor, apartment_number, rooms, area, price, is_for_sale, agent_id, series_id) VALUES 
(1, 1, 5, '12', 2, 54.50, 5000000.00, TRUE, 1, 1),
(1, 2, 3, '45а', 1, 32.00, 3500000.00, TRUE, 2, 2),
(2, 1, 9, '101', 3, 75.20, 8500000.00, FALSE, 1, 1),
(3, 3, 2, '7', 2, 48.00, 4200000.00, TRUE, 3, 3),
(4, 4, 1, '3', 1, 28.50, 2100000.00, TRUE, NULL, 2);