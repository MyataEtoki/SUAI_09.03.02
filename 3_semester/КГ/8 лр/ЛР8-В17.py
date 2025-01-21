import pygame
import PyOpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Определяем параметры растения и лейки
plant_color = (0.0, 1.0, 0.0) # Зеленый цвет
water_color = (0.0, 0.0, 1.0) # Синий цвет
pot_height = 0.1
pot_radius = 0.1
watering_can_height = 0.3
watering_can_radius = 0.05

# Функция для рисования цилиндра (для горшка и лейки)
def draw_cylinder(radius, height, color):
    glBegin(GL_QUADS)
    glColor3fv(color)
    for i in range(0, 360, 10):
        theta = np.radians(i)
        x = radius * np.cos(theta)
        z = radius * np.sin(theta)
        glVertex3f(x, 0, z)
        glVertex3f(x, height, z)
        theta = np.radians(i + 10)
        x = radius * np.cos(theta)
        z = radius * np.sin(theta)
        glVertex3f(x, height, z)
        glVertex3f(x, 0, z)
    glEnd()

# Функция для рисования 3D сцены
def draw_scene():
    # Рисуем горшок
    glPushMatrix()
    glTranslatef(0, pot_height / 2, 0)
    draw_cylinder(pot_radius, pot_height, plant_color)
    glPopMatrix()

    # Рисуем растение
    glPushMatrix()
    glTranslatef(0, pot_height + 0.3, 0)
    glColor3fv(plant_color)
    glutSolidSphere(0.05, 20, 20)  # Простой шар для символизации растительности
    glPopMatrix()

    # Рисуем лейку
    glPushMatrix()
    glTranslatef(0.2, pot_height / 2 + watering_can_height / 2, 0)
    glRotatef(30, 1, 0, 0)
    draw_cylinder(watering_can_radius, watering_can_height, plant_color)
    glPopMatrix()

# Основная функция
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -1.5, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_scene()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
