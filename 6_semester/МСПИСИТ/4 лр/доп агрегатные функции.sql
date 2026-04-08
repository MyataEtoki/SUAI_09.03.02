SELECT 
    d.name AS 'Район',
    SUM(a.price) AS 'Общая стоимость объектов'
FROM apartments a, districts d
WHERE a.district_id = d.id
  AND a.is_for_sale = TRUE
GROUP BY d.name;

SELECT 
    d.name AS 'Район',
    MIN(a.price) AS 'Мин. цена',
    MAX(a.price) AS 'Макс. цена'
FROM apartments a, districts d
WHERE a.district_id = d.id
  AND a.is_for_sale = TRUE
GROUP BY d.name;

SELECT 
    d.name AS 'Район',
    COUNT(DISTINCT a.series_id) AS 'Уникальных серий'
FROM apartments a, districts d
WHERE a.district_id = d.id
GROUP BY d.name;