import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Задаем размеры стрелок (длина линии)
minute_hand_length = 0.75
hour_hand_length = 0.5
second_hand_length = 1

# Угловые скорости стрелок (в радианах за секунду)
second_hand_speed = (2 * np.pi) / 60  # 360° за 60 секунды
minute_hand_speed = (2 * np.pi) / 3600  # 360° за 3600 секунды (1 час)
hour_hand_speed = (2 * np.pi) / 43200  # 360° за 43200 секунд (12 часов)


# Функция для создания матрицы вращения
def rotation_matrix(theta):
    return np.array([[np.cos(theta), np.sin(theta)],
                     [-np.sin(theta), np.cos(theta)]])
# theta - угол на который вращаем
# array - создаёт матрицу

# Функция для обновления рисунка
def update(frame):
    plt.clf()  # Очистка текущего рисунка
    koef = 1 # вычислено экспериментально, чтобы секундная стрелка проходила 360 градусов за 60 секунд.
    # Чем меньше, тем быстрее двигаются стрелки.
    # Вычисляем углы для стрелок
    # каждая итерация цикла (каждый кадр) увеличивает угол на величину, соответствующую угловой скорости
    second_angle = (frame/koef) * second_hand_speed # каждый кадр
    minute_angle = (frame/(koef^2)) * minute_hand_speed
    hour_angle = (frame/(koef^3)) * hour_hand_speed

    # Вектора стрелок
    second_hand = rotation_matrix(second_angle).dot(np.array([0, second_hand_length]))
    minute_hand = rotation_matrix(minute_angle).dot(np.array([0, minute_hand_length]))
    hour_hand = rotation_matrix(hour_angle).dot(np.array([0, hour_hand_length]))
    # dot - матричное умножение текущей позиции на повёрнутую матрицу => новые координаты вектора.
    # => координаты конца стрелки в новой позиции, которая была получена путём вращения на угол тета.

    # Рисуем стрелки
    # Используя матрицы вращения, умножаем их на векторы, представляющие положение конца стрелок.
    # Векторы задаются в виде [0,длина стрелки] => стрелки начинаются от начала координат (0,0) => вращение вокруг 0,0.
    plt.plot([0, second_hand[0]], [0, second_hand[1]], 'r', lw=1, label='Секунды')
    plt.plot([0, minute_hand[0]], [0, minute_hand[1]], 'g', lw=2, label='Минуты')
    plt.plot([0, hour_hand[0]], [0, hour_hand[1]], 'b', lw=3, label='Часы')

    # Настройки графика
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.title("The Часы")
    plt.grid()
    plt.legend(loc='upper right')


# Настройка анимации
fig = plt.figure()
ani = animation.FuncAnimation(fig, update, frames=(60*60*60), interval=(1000/60))
# interval - время в миллисекундах между обновлениями кадров анимации.
# frames - длина анимации в кадрах

# Показ анимации
plt.show()
