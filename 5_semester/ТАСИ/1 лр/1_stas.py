from decimal import Decimal, getcontext
from math import log2, ceil

getcontext().prec = 100  # высокая точность

# Фиксированные интервалы
intervals = {
    ',': (Decimal('0.0'),   Decimal('0.044')),
    'о': (Decimal('0.044'), Decimal('0.087')),
    '!': (Decimal('0.087'), Decimal('0.13')),
    'ц': (Decimal('0.13'),  Decimal('0.217')),
    'с': (Decimal('0.217'), Decimal('0.304')),
    'в': (Decimal('0.304'), Decimal('0.391')),
    'и': (Decimal('0.391'), Decimal('0.478')),
    'н': (Decimal('0.478'), Decimal('0.652')),
    'е': (Decimal('0.652'), Decimal('0.826')),
    ' ': (Decimal('0.826'), Decimal('1.0')),  # пробел
}
##КОДИРОВАНИЕ
def arithmetic_encode(text):
    low, high = Decimal('0'), Decimal('1')
    for ch in text:
        if ch.lower() not in intervals:
            raise ValueError(f"Нет интервала для символа: {ch!r}")
        l, h = intervals[ch.lower()]
        rng = high - low
        high = low + rng * h
        low = low + rng * l
        print(f"Символ: '{ch}' | Интервал: [{l}, {h}) | Новый интервал: [{low}, {high})")
    return low, high, (low + high) / 2

# ================= ДЕКОДИРОВАНИЕ =================
def arithmetic_decode_verbose(code, n):
    code = Decimal(code)
    result = []
    print("\nПошаговое декодирование:\n")
    for step in range(1, n + 1):
        print(f"--- Шаг {step} ---")
        print(f"Текущий код: {code}")
        found = False
        for ch, (low, high) in intervals.items():
            in_interval = (low <= code < high)
            if in_interval:
                print(f"  Интервал для '{ch}': [{low}, {high}) → Да")
            if in_interval and not found:
                result.append(ch)
                numer = code - low
                denom = high - low
                new_code = numer / denom
                print(f"  >>> Выбран символ: '{ch}'")
                print(f"      Числитель = {code} - {low} = {numer}")
                print(f"      Знаменатель = {high} - {low} = {denom}")
                print(f"      Новый код = {numer} / {denom} = {new_code}\n")
                code = new_code
                found = True
        if not found:
            raise ValueError("Код не попал ни в один интервал!")
    return ''.join(result)

# ================= ОСНОВНОЙ БЛОК =================
if __name__ == "__main__":
    phrase = "цени все, но не свинец!"
    low, high, code = arithmetic_encode(phrase)
    bits = ceil(-log2(float(high - low)))  # количество бит для представления кода
    print("\nРезультаты кодирования:")
    print(" Количество бит:", bits)
    print(" Итоговый интервал:", (low, high))
    print(" Выбранный код:", code)

    # Декодирование пошагово
    decoded = arithmetic_decode_verbose(code, len(phrase))
    print("Декодированное сообщение:", decoded)

    # Энтропия и объём
    p = [0.044,0.043,0.043,0.087,0.087,0.087,0.087,0.174,0.174,0.174]
    H = -sum(pi*log2(pi) for pi in p)
    n = len(phrase)
    L = n * H
    print("\nH =", H, "бит/символ")
    print("L =", L, "бит")
