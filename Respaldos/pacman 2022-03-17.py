from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.draw import *
from modules.transforms import *

w,h= 500,500



#Dibujo de Pacman
xc_circle = 250
yc_circle = 250
radius = 25
pacman_frame_1 = []
pacman_frame_2 = []
pacman_latest_frame = []
flag_pacman_frame = False

#Movimiento
flag_left = False
flag_right = False
flag_up = False
flag_down = False

def keyPressed ( key, x, y):
    global flag_left, flag_right, flag_up, flag_down
    if key == b'\x1b':
        glutLeaveMainLoop()
    if key == b'w':
        flag_up = True
        #yc_circle += 3
        #glutPostRedisplay()
    if key == b's':
        flag_down = True
        #yc_circle -= 3
        #glutPostRedisplay()
    if key == b'a':
        flag_left = True
        #xc_circle -= 3
        #glutPostRedisplay()
    if key == b'd':
        flag_right = True
        #xc_circle += 3
        #glutPostRedisplay()

def keyUp(key, x, y):
    global flag_left, flag_right, flag_up, flag_down
    if key == b'w':
        flag_up = False
    if key == b's':
        flag_down = False
    if key == b'a':
        flag_left = False
    if key == b'd':
        flag_right = False

def init():
    glClearColor ( 0.0, 0.0, 0.0, 0.0 )

def reshape(width, height):
    global w, h
    glViewport ( 0, 0, width, height )
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    w = width
    h = height
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

def display():
    global xc_circle, yc_circle, radius, pacman_latest_frame
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

    #---------------------DIBUJAR AQUI------------------------#
    #polygon(xc_circle,yc_circle,radius,32,1,1,1)
    coord = translate(pacman_latest_frame,xc_circle,yc_circle)
    glBegin(GL_POLYGON)
    for i in range(len(coord)):
        glVertex2d(coord[i][0], coord[i][1])
    glEnd()
    #---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp = 0
    #global xc_circle, yc_circle, radius, w, h

def timer_movement(value):
    global xc_circle, yc_circle, radius, w, h
    global flag_left, flag_right, flag_up, flag_down
    pixels = 5
    

    xc_circle = xc_circle + pixels if (flag_right and (xc_circle + radius + pixels) <= w) else xc_circle
    xc_circle = xc_circle - pixels if (flag_left and (xc_circle - radius - pixels) >= 0) else xc_circle
    yc_circle = yc_circle + pixels if (flag_up and (yc_circle + radius + pixels) <= h) else yc_circle
    yc_circle = yc_circle - pixels if (flag_down and (yc_circle - radius - pixels) >= 0) else yc_circle

    if flag_left or flag_right or flag_up or flag_down:
        glutPostRedisplay()
    glutTimerFunc(10,timer_movement,5)

    

def timer_pacman_frame(value):
    global pacman_frame_1, pacman_frame_2, pacman_latest_frame, flag_pacman_frame
    pacman_latest_frame = pacman_frame_1 if flag_pacman_frame else pacman_frame_2
    flag_pacman_frame = not flag_pacman_frame
    glutPostRedisplay()
    glutTimerFunc(100,timer_pacman_frame,5)


def main():
    global w, h, radius, pacman_frame_1, pacman_frame_2
    pacman_frame_1 = frame_1(radius)
    pacman_frame_2 = frame_2(radius)
    glutInit (  )
    glutInitDisplayMode ( GLUT_RGBA )
    glutInitWindowSize ( w, h )
    glutInitWindowPosition( 0, 0 )
    
    glutCreateWindow( "Ventana de PyOpenGL" )
    glutDisplayFunc (display)
    #glutIdleFunc ( animate )
    glutReshapeFunc ( reshape )
    glutKeyboardFunc( keyPressed )
    glutKeyboardUpFunc(keyUp)
    init()
    
    timer_pacman_frame(0)
    timer_movement(0)
    glutMainLoop()

print("Presiona Escape para cerrar.")
main()