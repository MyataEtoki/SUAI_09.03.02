import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# Функция для отрисовки лейки
def draw_watering_can(height=1, radius=1, handle_radius=0.5, handle_angle=180, spout_length=1):
    glPushMatrix()

    # Отрисовка основной части лейки (цилиндр)
    glTranslatef(0, height / 2, 0)
    glRotatef(90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, height, 32, 16)
    gluDeleteQuadric(quadric)

    # Отрисовка дна лейки
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, -height / 2, 0)
    glRotatef(handle_angle / 2, 16, 0, 0)
    quadric = gluNewQuadric()
    gluDisk(quadric, 0, radius, 32, 16)
    gluDeleteQuadric(quadric)

    # Отрисовка верха лейки
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.5, -0)
    glRotatef(handle_angle / 2, 10, 0, 0)
    quadric = gluNewQuadric()
    gluPartialDisk(quadric, 0.25, 0.5, 30, 1, 0, 360)
    gluDeleteQuadric(quadric)
    #Нижний верх лейки
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.4, -0)
    glRotatef(handle_angle / 2, 10, 0, 0)
    quadric = gluNewQuadric()
    gluPartialDisk(quadric, 0.25, 0.5, 30, 1, 0, 360)
    gluDeleteQuadric(quadric)
    #стенки верха лейки
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    glRotatef(90, 10, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.25, 0.25, 0.1, 32, 16)
    gluDeleteQuadric(quadric)

    # Отрисовка ручки лейки в виде дуги
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, -0.5)
    glRotatef(handle_angle / 2, 0, 1, 0)
    quadric = gluNewQuadric()
    gluPartialDisk(quadric, 0.3, handle_radius, 30, 1, 0, handle_angle)
    gluDeleteQuadric(quadric)

    # Отрисовка носика лейки
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, 0.4)
    glRotatef(-30, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.07, 0.03, spout_length, 32, 16)
    gluDeleteQuadric(quadric)

    # Отрисовка душика лейки
    '''glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, 0.4)
    glRotatef(-30, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.07, 0.03, spout_length, 32, 16)
    gluDeleteQuadric(quadric)'''

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
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 1, 2, 2))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (2, 5, 10, 1))

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    rotate_vector = [0, 0, 0]
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

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if rotate_vector != [0, 0, 0]:
            glRotatef(1, rotate_vector[0], rotate_vector[1], rotate_vector[2])

        # Рисуем лейку
        draw_watering_can(height=1, radius=0.5, handle_radius=0.5, handle_angle=180, spout_length=1)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()