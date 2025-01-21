import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Функция для создания куба
def create_cube(size):
    r = [-size / 2, size / 2]
    X, Y, Z = np.meshgrid(r, r, r)
    return np.array([X.flatten(), Y.flatten(), Z.flatten()])

# Функция для деформации куба
def deform_cube(cube_points, scale_factors):
    return cube_points * scale_factors[:, np.newaxis]

# Определение рёбер куба
edges = [
    [0, 1], [0, 2], [0, 4],
    [1, 3], [1, 5], [2, 3],
    [2, 6], [3, 7], [4, 5],
    [4, 6], [5, 7], [6, 7]
]

# Создание фигуры
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Функция анимации
def animate(i):
    ax.clear()
    t = i / frames
    scale_factors = (scale_start + t * (scale_end - scale_start))  # Линейная интерполяция масштабов для растяжения
    #scale_factors = (#scale_end + t * (scale_start - scale_end))  # Линейная интерполяция масштабов для сжатия
    # просто закомментить ненужное

    # Деформация куба
    deformed_cube = deform_cube(cube, scale_factors)

    # Рисуем рёбра куба
    for start, end in edges:
        xs = [deformed_cube[0, start], deformed_cube[0, end]]
        ys = [deformed_cube[1, start], deformed_cube[1, end]]
        zs = [deformed_cube[2, start], deformed_cube[2, end]]
        ax.plot(xs, ys, zs, 'b', linewidth=2)

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_title("Плавная деформация куба")

# Настройки
cube_size = 1
scale_start = np.array([1, 1, 1])
scale_end = np.array([2, 1, 0.5])
frames = 100

# Куб в исходных координатах
cube = create_cube(cube_size)

# Анимация
ani = animation.FuncAnimation(fig, animate, frames=1024, interval=50)
plt.show()
