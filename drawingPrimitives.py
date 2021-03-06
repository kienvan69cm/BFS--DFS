from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import math

RAD = 30
WIDTH = 800
HEIGHT = 600


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def drawPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def drawLine(a, b, c, d):
    glBegin(GL_LINES)
    glVertex2f(a, b)
    glVertex2f(c, d)
    glEnd()


def drawHollowCircle(x, y, i, r=RAD):
    lineAmount = 100
    twoPi = math.pi * 2
    font = pygame.font.Font(None, 64)
    textSurface = font.render(
        str(i), True, (255, 255, 255), (154, 70, 76, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(x-13, y+25, 0)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)
    glBegin(GL_LINE_LOOP)
    for i in range(lineAmount):
        glVertex2f(
            x + (r * math.cos(i * twoPi / lineAmount)),
            y + (r * math.sin(i * twoPi / lineAmount))
        )
    glEnd()


def drawFilledCircle(x, y, r=RAD):
    triangleAmount = 100
    twoPi = math.pi * 2
    glBegin(GL_TRIANGLE_FAN)
    for i in range(triangleAmount):
        glVertex2f(
            x + (r * math.cos(i * twoPi / triangleAmount)),
            y + (r * math.sin(i * twoPi / triangleAmount))
        )
    glEnd()
