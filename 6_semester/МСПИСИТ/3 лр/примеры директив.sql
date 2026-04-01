SELECT DISTINCT rooms AS 'Количество комнат'
FROM apartments
WHERE rooms IS NOT NULL;

SELECT 
    apartment_number AS 'Квартира', 
    price AS 'Цена'
FROM apartments
ORDER BY price DESC;

SELECT 
    apartment_number, 
    rooms
FROM apartments
WHERE rooms NOT IN (1, 2);

SELECT 
    apartment_number, 
    price
FROM apartments
WHERE price NOT BETWEEN 3000000 AND 6000000;

SELECT 
    last_name, 
    first_name, 
    middle_name
FROM agents
WHERE middle_name IS NULL;

SELECT 
    id, 
    name
FROM streets
WHERE name LIKE 'Л%';