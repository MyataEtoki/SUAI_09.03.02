SELECT 
    d.name AS 'Район',
    COUNT(a.id) AS 'Количество объектов'
FROM apartments a, districts d
WHERE a.district_id = d.id
  AND a.is_for_sale = TRUE
GROUP BY d.name

-- ищем максимально продажные районы
HAVING COUNT(a.id) = (
    SELECT MAX(cnt) FROM (
        SELECT COUNT(a2.id) AS cnt
        FROM apartments a2, districts d2
        WHERE a2.district_id = d2.id
          AND a2.is_for_sale = TRUE
        GROUP BY d2.name
    ) AS subquery
);