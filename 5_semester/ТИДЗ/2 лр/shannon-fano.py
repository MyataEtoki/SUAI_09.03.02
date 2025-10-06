import matplotlib.pyplot as plt

# === Чтение текста и подсчет частот ===
Code = []
with open("text.txt", encoding='utf8') as file:
    text = file.read().lower()

d = {}
for i in text:
    d[i] = d.get(i, 0) + 1

# переводим в вероятности
sum_sim = sum(d.values())
for i in d:
    d[i] = round(d[i] / sum_sim, 3)

# сортируем по убыванию вероятности
d = sorted(d.items(), key=lambda x: x[1], reverse=True)

# создаем массив для кодов
arr = []
for i in d:
    arr.append([i[0], i[1], ''])

# === Рекурсивная функция построения дерева Шеннона-Фано ===
def build_tree(arr):
    if len(arr) == 1:
        sym, prob, code = arr[0]
        return {
            'symbols': [sym],
            'prob_sum': prob,
            'code': code,
            'left': None,
            'right': None
        }

    total = sum(x[1] for x in arr)
    sum1 = 0
    index = 0
    for i, j in enumerate(arr):
        sum1 += j[1]
        if sum1 >= total / 2:
            # выбираем индекс так, чтобы разбиение было ближе к половине
            if i > 0 and abs((sum1 - j[1]) - total / 2) < abs(sum1 - total / 2):
                index = i
            else:
                index = i + 1
            break

    left_arr = arr[:index]
    right_arr = arr[index:]

    # добавляем коды
    for i in left_arr:
        i[2] += '0'
    for i in right_arr:
        i[2] += '1'

    left_node = build_tree(left_arr) if left_arr else None
    right_node = build_tree(right_arr) if right_arr else None

    return {
        'symbols': [s[0] for s in arr],
        'prob_sum': sum(x[1] for x in arr),
        'code': '',
        'left': left_node,
        'right': right_node
    }

tree_root = build_tree(arr)

# === Рекурсивная функция для отрисовки дерева ===
def plot_tree(node, x=0, y=0, dx=5, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('off')
        plot_tree(node, x, y, dx, ax=ax)
        plt.show()
        return

    # подпись узла
    symbols_str = ''.join(node['symbols'])
    prob_str = f"{node['prob_sum']:.3f}"
    code_str = node.get('code', '')
    label = f"{symbols_str}\nP={prob_str}"
    if code_str:
        label += f"\ncode={code_str}"

    ax.text(x, -y, label, ha='center', va='center',
            bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'),
            fontsize=9, fontfamily='monospace')

    # соединяем с потомками
    if node['left']:
        ax.plot([x, x - dx], [-y - 0.25, -y - 1.5], color='black')
        plot_tree(node['left'], x - dx, y + 1.5, dx / 1.5, ax=ax)
    if node['right']:
        ax.plot([x, x + dx], [-y - 0.25, -y - 1.5], color='black')
        plot_tree(node['right'], x + dx, y + 1.5, dx / 1.5, ax=ax)

# === Отрисовка дерева ===
plot_tree(tree_root)
