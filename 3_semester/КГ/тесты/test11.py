import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Функция для рисования перевернутого горшка
def draw_inverted_pot():
    glColor3f(0.8, 0.4, 0.2)  # Коричневый цвет для горшка

    # Рисуем стенки горшка
    glBegin(GL_QUAD_STRIP)
    for angle in np.arange(0, 2 * np.pi, 0.1):
        x1 = 0.5 * np.cos(angle)  # Внешняя окружность (верх)
        z1 = 0.5 * np.sin(angle)
        x2 = 0.3 * np.cos(angle)  # Внутренняя окружность (низ)
        z2 = 0.3 * np.sin(angle)
        glVertex3f(x1, 0.5, z1)  # Верхняя грань
        glVertex3f(x2, -1, z2)  # Нижняя грань
    glEnd()

    # Верхний круг (больше)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0.5, 0)  # Центр верхнего круга
    for angle in np.arange(0, 2 * np.pi, 0.1):
        x = 0.5 * np.cos(angle)
        z = 0.5 * np.sin(angle)
        glVertex3f(x, 0.5, z)  # Верхний круг (больше)
    glEnd()

    # Нижний круг (меньше)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, -1, 0)  # Центр нижнего круга
    for angle in np.arange(0, 2 * np.pi, 0.1):
        x = 0.3 * np.cos(angle)
        z = 0.3 * np.sin(angle)
        glVertex3f(x, -1, z)  # Нижний круг (меньше)
    glEnd()

# Функция для рисования стебля (цилиндра) с использованием gluCylinder
def draw_stem():
    glColor3f(0.0, 0.8, 0.0)  # Зеленый цвет для стебля

    # Создаем матрицу для стебля
    glPushMatrix()
    glTranslatef(0, 1.5, 0)  # Сдвигаем к верхнему краю горшка

    # Создаем цилиндр
    quadric = gluNewQuadric()  # Создаем объект Quadric
    gluQuadricNormals(quadric, GLU_SMOOTH)  # Устанавливаем гладкие нормали
    gluCylinder(quadric, 0.02, 0.02, 3.25, 32, 32)  # Рисуем цилиндр

    glPopMatrix()
    gluDeleteQuadric(quadric)  # Удаляем объект Quadric

# Функция для отрисовки листочков
def draw_leaves():
    glColor3f(0.0, 0.5, 0.0)  # Темно-зеленый цвет для листьев
    leaf_shape = np.array([
        [0.0, 0.1, 0.0],
        [0.1, 0.05, 0.0],
        [0.0, 0.0, 0.0],
        [-0.1, 0.05, 0.0]
    ])

    # Рисуем два листка
    for translation in [(0.5, 1.0, 0.0), (-0.10, 1.4, 2.0)]:
        glPushMatrix()
        glTranslatef(*translation)  # Перемещаем к позиции листа
        glBegin(GL_POLYGON)
        for vertex in leaf_shape:
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
        glPopMatrix()

# Основная функция
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -2, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Рисуем перевернутый горшок
        glPushMatrix()
        draw_inverted_pot()
        glPopMatrix()

        # Рисуем стебель
        draw_stem()

        # Рисуем листочки
        draw_leaves()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
