SELECT 
    s.name AS 'Улица',
    a1.apartment_number AS 'Кв. 1',
    d1.name AS 'Район 1',
    a2.apartment_number AS 'Кв. 2',
    d2.name AS 'Район 2'
FROM apartments a1, apartments a2, districts d1, districts d2, streets s
WHERE 
    a1.street_id = a2.street_id
    AND a1.street_id = s.id       -- Связь с таблицей улиц
    AND a1.district_id = d1.id
    AND a2.district_id = d2.id    
    AND a1.district_id <> a2.district_id
    AND a1.id < a2.id;            -- без дублей и самопересечений