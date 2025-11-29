def lz78_encode(data):
    dictionary = {}        # словарь: {фраза: индекс}
    phrases = []           # результат: список кортежей (индекс, символ)
    current = ""
    index = 1              # индексы начинаются с 1

    for char in data:
        current_with_char = current + char
        if current_with_char in dictionary:
            current = current_with_char
        else:
            # current есть в словаре (или пуст), char — новый символ
            prev_index = dictionary[current] if current != "" else 0
            phrases.append((prev_index, char))
            dictionary[current_with_char] = index
            index += 1
            current = ""

    return phrases


def read_input(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_output(phrases, filename='output.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for idx, char in phrases:
            # Записываем в формате: (индекс, символ)
            f.write(f"({idx}, '{char}')\n")

if __name__ == '__main__':
    data = read_input('text.txt')
    encoded = lz78_encode(data)
    write_output(encoded, 'output.txt')
    print("Сжатие LZ78 завершено. Результат в output.txt")

    N = len(data)  # общее число входных символов
    M = len(encoded)  # число элементарных сигналов (фраз)

    avg_signals_per_symbol = M / N  # сколько фраз приходится на 1 символ
    avg_phrase_length = N / M  # сколько символов в среднем в одной фразе

    print(f"Входных символов: {N}")
    print(f"Элементарных сигналов (фраз): {M}")
    print(f"Среднее число сигналов на символ: {avg_signals_per_symbol:.4f}")
    print(f"Средняя длина фразы: {avg_phrase_length:.2f} символов")