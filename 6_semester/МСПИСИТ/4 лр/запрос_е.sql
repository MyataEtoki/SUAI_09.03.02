SELECT 
    d.name AS 'Район',
    AVG(a.price / a.area) AS '(минимальная) Средняя цена за м²'
FROM apartments a, districts d
WHERE a.district_id = d.id
  AND a.is_for_sale = TRUE
  AND a.area IS NOT NULL
  AND a.area > 0
GROUP BY d.name
-- ищем минимально продажные районы
HAVING AVG(a.price / a.area) = (
    SELECT MIN(Srednaya_Cena)
    FROM (
        SELECT AVG(a2.price / a2.area) AS Srednaya_Cena
        FROM apartments a2, districts d2
        WHERE a2.district_id = d2.id
          AND a2.is_for_sale = TRUE
          AND a2.area IS NOT NULL
          AND a2.area > 0
        GROUP BY d2.name
    ) AS SubQuery
);