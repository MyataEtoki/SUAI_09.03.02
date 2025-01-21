import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Определяем вершины куба
def cube_vertices():
    r = 1
    return np.array([[r, r, r],
                     [-r, r, r],
                     [-r, -r, r],
                     [r, -r, r],
                     [r, r, -r],
                     [-r, r, -r],
                     [-r, -r, -r],
                     [r, -r, -r]])

# Матрица вращения вокруг оси X
def rotation_matrix_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0],
                     [0, c, -s],
                     [0, s, c]])

# Кабинетная проекция
def cabinet_projection(vertices):
    scale = 1  # Коэффициент масштабирования
    projection_matrix = np.array([[1, 0, -0.5],
                                   [0, 1, -0.5]])
    proj_vertices = vertices @ projection_matrix.T
    return proj_vertices * scale

# Анимация куба
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])

vertices = cube_vertices()
edges = [[0, 1], [1, 2], [2, 3], [3, 0],
         [4, 5], [5, 6], [6, 7], [7, 4],
         [0, 4], [1, 5], [2, 6], [3, 7]]

def update(frame):
    ax.cla()  # Очистка осей
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_xlabel('X-координата')
    ax.set_ylabel('Y-координата')

    # Вращение куба
    theta = frame * np.pi / 180
    rotated_vertices = vertices @ rotation_matrix_x(theta)

    # Применяем проекцию
    projected_vertices = cabinet_projection(rotated_vertices)

    # Рисуем куб
    for edge in edges:
        ax.plot(*zip(projected_vertices[edge[0]], projected_vertices[edge[1]]), color='b')

# Анимация
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 5), interval=100)
plt.show()
