from decimal import Decimal, getcontext
from math import log2, ceil

getcontext().prec = 100  # высокая точность

# Фиксированные интервалы
intervals = {
    '1': (Decimal('0.0'),   Decimal('0.03')), #eof
    ' ': (Decimal('0.03'), Decimal('0.12')), # пробел
    'ц': (Decimal('0.12'), Decimal('0.21')),
    'и': (Decimal('0.21'),  Decimal('0.30')),
    'т': (Decimal('0.30'), Decimal('0.39')),
    'г': (Decimal('0.39'), Decimal('0.48')),
    'р': (Decimal('0.48'), Decimal('0.57')),
    'а': (Decimal('0.57'), Decimal('0.66')),
    'н': (Decimal('0.66'), Decimal('0.83')),
    'е': (Decimal('0.83'), Decimal('1.0')),
}
##КОДИРОВАНИЕ
def arithmetic_encode(text):
    low, high = Decimal('0'), Decimal('1')
    step = 1
    for ch in text:
        if ch.lower() not in intervals:
            raise ValueError(f"Нет интервала для символа: {ch!r}")
        l, h = intervals[ch.lower()]
        rng = high - low
        high = low + rng * h
        low = low + rng * l
        print(f"{ch} - L{step} = {low}, h{step} = {high}")
        step+=1
    return low, high, (low + high) / 2

# ================= ДЕКОДИРОВАНИЕ =================
def arithmetic_decode_verbose(code, n):
    code = Decimal(code)
    result = []
    print("\nПошаговое декодирование:\n")
    for step in range(1, n + 1):
        print(f"Символ №{step}")
        found = False
        for ch, (low, high) in intervals.items():
            in_interval = (low <= code < high)
            if in_interval:
                print(f"Код {code} в интервале для '{ch}': [{low}, {high})")
                print(f"\n ПОЛУЧЕННЫЙ СИМВОЛ: {ch}\n")
            if in_interval and not found:
                result.append(ch)
                numer = code - low
                denom = high - low
                new_code = numer / denom
                print(f"Новый код = ({code} - {low}) / ({high} - {low})")
                print(f"Новый код = {numer} / {denom} = {new_code}\n")
                code = new_code
                found = True
                break
        if not found:
            raise ValueError("Код не попал ни в один интервал!")
    return ''.join(result)

# ================= ОСНОВНОЙ БЛОК =================
if __name__ == "__main__":
    phrase = "аргентинец ценит негра1"
    low, high, code = arithmetic_encode(phrase)
    bits = ceil(-log2(float(high - low)))  # количество бит для представления кода
    print("\nРезультаты кодирования:")
    # print("Количество бит:", bits)
    print("Итоговый интервал:", (low, high))
    print("Выходной код (середина отрезка):", code)

    # Декодирование пошагово
    decoded = arithmetic_decode_verbose(code, len(phrase))
    print("Декодированное сообщение:", decoded)

    # Энтропия и объём
    p = [0.03, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.17, 0.17]
    H = -sum(pi*log2(pi) for pi in p)
    n = len(phrase)
    L = n * H
    print("\nH =", H, "бит/символ")
    print("L =", L, "бит")
