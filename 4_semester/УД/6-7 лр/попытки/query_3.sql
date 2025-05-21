USE home_library;
SELECT 
debts_records.disc_id,
discs.disc_name,
debts.debt_id,
debts.date_start,
debts.date_end
FROM debts_records JOIN discs ON discs.disc_id = debts_records.disc_id 
JOIN debts ON debts.debt_id = debts_records.debt_id
WHERE (debts.exchange_type = 'taken' AND debts_records.disc_id IS NOT NULL);