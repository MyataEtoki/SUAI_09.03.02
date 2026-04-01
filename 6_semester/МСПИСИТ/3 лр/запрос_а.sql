SELECT 
    a.id AS 'ID квартиры',
    a.apartment_number AS 'Номер кв.',
    s.name AS 'Улица',
    d.name AS 'Район',
    a.area AS 'Площадь',
    a.price AS 'Цена'
FROM apartments a, districts d, streets s
WHERE 
    a.district_id = d.id -- соединение квартир и районов 
    AND a.street_id = s.id -- соединение квартир и улиц
    AND a.rooms = 1
    AND a.is_for_sale = TRUE
    AND d.name = 'Московский';