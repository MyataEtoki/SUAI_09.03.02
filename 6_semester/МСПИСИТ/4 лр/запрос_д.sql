SELECT 
    d.name AS 'Район',
    COUNT(a.id) AS 'Количество объектов'
FROM apartments a, districts d
WHERE a.district_id = d.id
  AND a.is_for_sale = TRUE
GROUP BY d.name
ORDER BY COUNT(a.id) DESC
LIMIT 1;