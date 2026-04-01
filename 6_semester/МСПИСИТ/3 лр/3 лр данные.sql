INSERT INTO districts(name, city_id) values ('Московский', 2);
INSERT INTO streets(name) values ('Ленсовета');
INSERT INTO streets(name) values ('Гастелло');

INSERT INTO street_districts(street_id, district_id) values (5,5);
INSERT INTO street_districts(street_id, district_id) values (6,5);

INSERT INTO apartments(street_id, district_id, floor, apartment_number, rooms, area, price, is_for_sale, agent_id, series_id, year_built) values
(5,5,3,'345',2,55.5,5000000,1,3,1,2003),
(6,5,4,'456',3,55.5,5500000,1,100,1,2003);

INSERT INTO apartments(street_id, district_id, floor, apartment_number, rooms, area, price, is_for_sale, agent_id, series_id, year_built) values
(6,5,1,'349',1,25.5,4500000,1,100,1,2003),
(6,5,2,'359',1,27.0,4700000,1,100,1,2003);

INSERT INTO districts(name, city_id) values ('Кировский',2);
INSERT INTO streets(name) values ('Краснопутиловская');
INSERT INTO street_districts(street_id, district_id) values (7,6), (7,5);

INSERT INTO apartments(street_id, district_id, floor, apartment_number, rooms, area, price, is_for_sale, agent_id, series_id, year_built) values
(7,6,3,'123',1,33.0,4000000,1,3,3,1976),
(7,5,3,'3121',2,43.0,5000000,1,3,3,1967);

INSERT INTO agents(first_name, last_name) values ('Петр','Петров');