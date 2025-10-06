import matplotlib.pyplot as plt

Code = []
file = open("text.txt", encoding='utf8')
text = file.read().lower()
file.close()
d = {}

# считаем появление символов
for i in text:
    # if i not in '!—,.-?...()—:;«»\n':
    #     d[i] = d.get(i, 0) + 1
    d[i] = d.get(i, 0) + 1

# всего символов:
sum_sim = sum(d.values())

# ч/з => х.ххх
for i in d:
    d[i] = round(d[i] / sum_sim, 3)

# сортируем по убыванию
d = sorted(d.items(), key=lambda x: x[1], reverse=True)

# место для записи кода
arr = []
for i in d:
    arr.append(list(i) + [''])


# === Рекурсивная функция построения дерева ===
def build_tree(arr):
    # Базовый случай — один символ
    if len(arr) == 1:
        sym, prob, code = arr[0]
        return {
            'symbols': [sym],
            'prob_sum': prob,
            'code': code,
            'left': None,
            'right': None
        }

    # Считаем точку разбиения
    half = sum(x[1] for x in arr)
    sum1 = 0
    for i, j in enumerate(arr):
        sum1 += j[1]
        if sum1 * 2 >= half:
            index = i + (abs(2 * sum1 - half) < abs(2 * (sum1 - j[1]) - half))
            break

    left_arr = arr[:index]
    right_arr = arr[index:]

    for i in left_arr:
        i[2] += '0'
    for i in right_arr:
        i[2] += '1'

    left_node = build_tree(left_arr)
    right_node = build_tree(right_arr)

    return {
        'symbols': [s[0] for s in arr],
        'prob_sum': sum(x[1] for x in arr),
        'code': '',
        'left': left_node,
        'right': right_node
    }


tree_root = build_tree(arr)

def plot_tree(node, x=0, y=0, dx=1.5, level=0, ax=None):
    """Рекурсивная отрисовка дерева Шеннона–Фано с кодами"""
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('off')
        plot_tree(node, x, y, dx, level, ax=ax)
        plt.show()
        return

    # Формируем подпись узла
    symbols_str = ''.join(node['symbols'])
    prob_str = f"{node['prob_sum']:.3f}"
    if node['code']:
        code_str = node['code']
        label = f"{symbols_str}\nP={prob_str}\ncode={code_str}"
    else:
        label = f"{symbols_str}\nP={prob_str}"

    ax.text(x, -y, label, ha='center', va='center',
            bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'),
            fontsize=9, fontfamily='monospace')

    if node['left']:
        ax.plot([x, x - dx-0.05], [-y - 0.25, -y - 1.5], color='black')
        plot_tree(node['left'], x - dx-0.05, y + 1.5, dx / 1.8, level + 1, ax=ax)

    if node['right']:
        ax.plot([x, x + dx+0.05], [-y - 0.25, -y - 1.5], color='black')
        plot_tree(node['right'], x + dx+0.05, y + 1.5, dx / 1.8, level + 1, ax=ax)


# Отрисовать дерево:
plot_tree(tree_root)

