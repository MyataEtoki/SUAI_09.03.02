def build_tree(keys, lefts, rights):
    return {
        'keys': keys,
        'lefts': lefts,
        'rights': rights
    }

# симметричный
def in_order(tree, v, result):
    if v != -1: # проверяем есть ли у узла потомки
        # идём от левого потомка к корню
        # смотрим индекс левого потомка в массиве левых потомков по индексу текущего узла.
        in_order(tree, tree['lefts'][v], result)
        # записываем значение узла
        result.append(tree['keys'][v])
        # идём от правого потомка к корню
        in_order(tree, tree['rights'][v], result)

# прямой
def pre_order(tree, v, result):
    if v != -1:
        # записываем значение
        result.append(tree['keys'][v])
        # идём к левым потомкам
        pre_order(tree, tree['lefts'][v], result)
        # идём к правым потомкам
        pre_order(tree, tree['rights'][v], result)

# обратный
def post_order(tree, v, result):
    if v != -1: # проверяем что у узла есть потомки,
        # если нет, то он самый нижний, возвращаемся на шаг раньше в рекурсии

        # идём к левым потомкам
        post_order(tree, tree['lefts'][v], result)
        # идём к правым потомкам
        post_order(tree, tree['rights'][v], result)
        # если он самый нижний, записываем его и идём наверх.
        result.append(tree['keys'][v])


def main():
    import sys

    input = sys.stdin.read # читаем данные до конца ввода
    data = input().splitlines() # делим на строки

    n = int(data[0])
    keys = []
    lefts = []
    rights = []

    for i in range(1, n + 1):
        key, left, right = map(int, data[i].split())
        keys.append(key)
        lefts.append(left)
        rights.append(right)

    tree = build_tree(keys, lefts, rights)

    in_order_result = []
    pre_order_result = []
    post_order_result = []

    in_order(tree, 0, in_order_result)
    pre_order(tree, 0, pre_order_result)
    post_order(tree, 0, post_order_result)

    print(" ".join(map(str, in_order_result)))
    print(" ".join(map(str, pre_order_result)))
    print(" ".join(map(str, post_order_result)))


if __name__ == "__main__":
    main()
