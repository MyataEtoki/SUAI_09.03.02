import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Функция для отрисовки лейки
def draw_watering_can(height=1, radius=1, handle_radius=0.5, handle_angle=180, spout_length=1):

    # Отрисовка основной части лейки (цилиндр)
    glPushMatrix()
    glTranslatef(0, height / 2, 0)
    glRotatef(90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, height, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Отрисовка дна лейки
    glPushMatrix()
    glTranslatef(0, -height / 2, 0)
    glRotatef(handle_angle / 2, 16, 0, 0)
    quadric = gluNewQuadric()
    gluDisk(quadric, 0, radius, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    # второе дно, чтобы закрыть остаток носика лейки
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(handle_angle / 2, 16, 0, 0)
    quadric = gluNewQuadric()
    gluDisk(quadric, 0, radius, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Отрисовка верха лейки
    glPushMatrix()
    glTranslatef(0, 0.5, -0)
    glRotatef(handle_angle / 2, 10, 0, 0)
    quadric = gluNewQuadric()
    gluPartialDisk(quadric, 0.25, 0.5, 30, 1, 0, 360)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    #Нижний верх лейки
    glPushMatrix()
    glTranslatef(0, 0.4, -0)
    glRotatef(handle_angle / 2, 10, 0, 0)
    quadric = gluNewQuadric()
    gluPartialDisk(quadric, 0.25, 0.5, 30, 1, 0, 360)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    #стенки верха лейки
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    glRotatef(90, 10, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.25, 0.25, 0.1, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Отрисовка ручки лейки в виде дуги
    glPushMatrix()
    glTranslatef(0, 0, -0.5)
    glRotatef(handle_angle / 2, 0, 1, 0)
    quadric = gluNewQuadric()
    gluPartialDisk(quadric, 0.3, handle_radius, 30, 1, 0, handle_angle)
    gluDeleteQuadric(quadric)
    glPopMatrix()
# ручка - цилиндром (нет)
#     glPushMatrix()
#     glTranslatef(0, 0, -0.5)
#     glRotatef(handle_angle / 2, 0, 1, 0)
#     quadric = gluNewQuadric()
#     gluCylinder(quadric, 0.25, 0.25, 0.1, 32, 16)
#     gluDeleteQuadric(quadric)
#     glPopMatrix()

    # Отрисовка носика лейки
    glPushMatrix()
    glTranslatef(0, 0, 0.4)
    glRotatef(-30, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.07, 0.03, spout_length, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Отрисовка душика лейки
    glPushMatrix()
    glTranslatef(0, 0.5, 1.25)
    glScalef(1.0, 1, 0.3)
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.15, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def draw_water(angle):
    # Считываем радиус дуги
    arc_radius = 0.5  # Радиус дуги

    # Вычисляем новые координаты капель по формуле
    y1 = 0.5 + arc_radius * math.sin(math.radians(angle))
    z1 = 1.6 + arc_radius * (1 - math.cos(math.radians(angle)))

    y2 = 0.3 + arc_radius * math.sin(math.radians(angle))
    z2 = 1.7 + arc_radius * (1 - math.cos(math.radians(angle)))

    y3 = 0.37 + arc_radius * math.sin(math.radians(angle))
    z3 = 1.75 + arc_radius * (1 - math.cos(math.radians(angle)))

    # Отрисовка капель
    glPushMatrix()
    glTranslatef(0, y1, z1)  # Применяем новую координату
    glScalef(1.0, 1, 1)
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.05, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, y1, z1 - 0.11)  # Применяем новую координату для цилиндра
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0, 0.05, 0.1, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Для капли 2
    glPushMatrix()
    glTranslatef(0.2, y2, z2)
    glScalef(1.0, 1, 1)
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.05, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.2, y2 + 0.1, z2 - 0.05)
    glRotatef(63, 0.5, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0, 0.05, 0.1, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Для капли 3
    glPushMatrix()
    glTranslatef(-0.13, y3, z3)
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.05, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.15, y3 + 0.1, z3 - 0.08)
    glRotatef(45, 0.5, 0.1, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0, 0.05, 0.1, 32, 16)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def main():
    pygame.init()
    display = (1000, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Watering Can')
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Настройка освещения
    glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))  # Свет исходит слева сверху спереди
    glLightfv(GL_LIGHT0, GL_AMBIENT, (2, 1, 2, 4))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (2, 10, 1, 1))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    rotate_vector = [0, 0, 0]
    angle = 0  # Начальный угол

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Обработка нажатий клавиш для вращения
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            rotate_vector = [-1, 0, 0]
        if pressed[pygame.K_DOWN]:
            rotate_vector = [1, 0, 0]
        if pressed[pygame.K_RIGHT]:
            rotate_vector = [0, 1, 0]
        if pressed[pygame.K_LEFT]:
            rotate_vector = [0, -1, 0]
        if pressed[pygame.K_SPACE]:
            rotate_vector = [0, 0, 0]
        # if pressed[pygame.K_LEFT]:
        #     glTranslatef(0.1,0.1,0)
        # if pressed[pygame.K_RIGHT]:
        #     glTranslatef(-0.1,-0.1,0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Обновляем угол для движения капель

        angle += 2  # Увеличиваем угол на 2 градуса в каждом кадре
        if angle >= 100:
            angle = 0  # Обнуляем угол для непрерывного движения

        if rotate_vector != [0, 0, 0]:
             glRotatef(1, rotate_vector[0], rotate_vector[1], rotate_vector[2])

        # Рисуем лейку
        draw_watering_can(height=1, radius=0.5, handle_radius=0.5, handle_angle=180, spout_length=1)
        draw_water(angle)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()