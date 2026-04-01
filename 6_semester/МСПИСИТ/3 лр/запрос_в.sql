SELECT 
    a1.apartment_number AS 'Кв. 1',
    a1.rooms AS 'Комн. 1',
    a1.area AS 'Общая площадь',
    a2.apartment_number AS 'Кв. 2',
    a2.rooms AS 'Комн. 2'
FROM apartments a1, apartments a2
WHERE 
    a1.area = a2.area
    AND a1.rooms IN (2, 3)
    AND a2.rooms IN (2, 3)
    AND a1.id < a2.id;             -- без дублей пар