SELECT s.name AS 'Улица', s.id AS 'Id'
FROM streets s, street_districts sd, districts d
WHERE s.id = sd.street_id 
  AND sd.district_id = d.id
  AND d.name = 'Центральный'

EXCEPT

SELECT s.name AS 'Улица', s.id AS 'Id'
FROM streets s, apartments a
WHERE s.id = a.street_id
  AND a.price > 5000000;