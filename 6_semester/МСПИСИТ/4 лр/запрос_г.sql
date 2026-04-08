SELECT 
    AVG(price) AS 'Средняя цена 1-комн. квартиры'
FROM apartments
WHERE rooms = 1 
  AND is_for_sale = TRUE;