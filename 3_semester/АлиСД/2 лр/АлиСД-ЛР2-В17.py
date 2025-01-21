# Построение дерева
def build_tree(n, parents):
    # Создаем список для хранения детей каждой вершины
    tree = [[] for x in range(n)] # список из пустых списков -> дети соотв. узла
    root = None # будет хранить индекс корн. узла

    # Заполняем дерево детьми для каждой вершины
    for child, parent in enumerate(parents): # перебираем индекс - значение в parents
        if parent == -1: # элемент -1 это корень и нам нужен его индекс-child
            root = child
        else:
            tree[parent].append(child)

    return tree, root

# Вычисление высоты дерева
def calculate_height(tree, node):
    if not tree[node]:  # Если у узла нет детей
        return 1
    heights = [calculate_height(tree, child) for child in tree[node]]
    return 1 + max(heights)  # Возвращаем высоту

#n = 5
n = int(input())  # ввод количества узлов - 1 строка
#input_parents = '4 -1 4 1 1'
#input_parents = '-1 0 4 0 3'
parents = list(map(int, input().split()))  # ввод родителей - 2 строка, перечисление
#parents = list(map(int, input_parents.split()))

tree, root = build_tree(n, parents)  # Строим дерево
height = calculate_height(tree, root)  # Вычисляем высоту

#print(n, "\n", input_parents)
print("Высота дерева: ", height)  # Печатаем высоту дерева
#print(tree)
