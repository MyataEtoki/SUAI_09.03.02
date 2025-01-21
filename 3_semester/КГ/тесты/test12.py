import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin, radians


def draw_cylinder(radius, height, slices):
    """Рисует цилиндр (тело лейки)"""
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        angle = 2 * 3.14159 * i / slices
        x = radius * cos(angle)
        z = radius * sin(angle)

        # Устанавливаем цвет для тела лейки
        glColor3f(0.1, 0.5, 0.1)  # Зеленый цвет

        glVertex3f(x, 0, z)
        glVertex3f(x, height, z)
    glEnd()


def draw_cone(radius, height, slices):
    """Рисует конус (носик лейки)"""
    glBegin(GL_TRIANGLE_FAN)
    # Устанавливаем цвет для носика
    glColor3f(0.8, 0.4, 0.2)  # Коричневый цвет

    glVertex3f(0, height, 0)  # Вершина конуса
    for i in range(slices + 1):
        angle = 2 * 3.14159 * i / slices
        x = radius * cos(angle)
        z = radius * sin(angle)
        glVertex3f(x, 0, z)
    glEnd()


def draw_ellipse(radius_x, radius_y, height, slices):
    """Рисует эллипс (душик лейки)"""
    glBegin(GL_QUAD_STRIP)
    # Устанавливаем цвет для душика
    glColor3f(0.2, 0.8, 0.8)  # Голубой цвет

    for i in range(slices + 1):
        angle = 2 * 3.14159 * i / slices
        x = radius_x * cos(angle)
        z = radius_y * sin(angle)
        # Вместо высоты души, используем небольшой offset
        glVertex3f(x, height, z)
        glVertex3f(x, height + 0.1, z)  # Добавляем небольшой высотный элемент
    glEnd()


def draw_watering_can():
    """Рисует лейку"""
    glPushMatrix()

    # Рисуем тело лейки
    draw_cylinder(1, 1.5, 30)  # Тело лейки
    glTranslatef(0, 1.5, 0)  # Переход к носику

    # Рисуем носик
    draw_cone(0.3, 1, 20)  # Носик лейки
    glTranslatef(0, 1, 0)  # Перемещаемся вверх на высоту носика

    # Рисуем душик
    glTranslatef(0, 0, 0)  # Сброс координат по z
    draw_ellipse(0.5, 0.3, 1.5, 20)  # Душик

    glPopMatrix()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Лейка")
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Основной цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLight(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))

        draw_watering_can()  # Рисуем лейку

        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)

        pygame.display.flip()
        pygame.time.wait(10)


main()
