from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

#-----------------------HERRAMIENTAS DE DIBUJO------------------------#
def polygon(xc,yc,R,n, red,green, blue):
    angle = 2*3.141592/n
    glColor3f(red,green,blue)
    glBegin(GL_POLYGON)
    for i in range(n):
        x = xc + R*np.cos(angle*i)
        y = yc + R*np.sin(angle*i)
        glVertex2d(x,y)
    glEnd()

def polygon_coordinates(xc,yc,R,n):
    angle = 2*3.141592/n
    list_coordiantes = []
    for i in range(n):
        x = xc + R*np.cos(angle*i)
        y = yc + R*np.sin(angle*i)
        list_coordiantes.append([x,y])
    return list_coordiantes

def frame_1(R):
    angle = 2*3.141592/32
    list_coordiantes = []
    for i in range(32):
        x = R*np.cos(angle*i)
        y = R*np.sin(angle*i)
        list_coordiantes.append([int(x),int(y)])
    return list_coordiantes

def frame_2(R):
    angle = 2*3.141592/32
    list_coordiantes = [[0,0]]
    for i in range(4,29):
        x = R*np.cos(angle*i)
        y = R*np.sin(angle*i)
        list_coordiantes.append([int(x),int(y)])
    return list_coordiantes