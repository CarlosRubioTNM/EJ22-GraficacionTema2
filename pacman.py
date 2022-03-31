from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.draw import *
from modules.transforms import *
from modules.bezier import evaluate_bezier

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
MOVE_RIGHT = 0
MOVE_DOWN = 3.1416/2 #90°
MOVE_LEFT = 3.1416 #180°
MOVE_UP = 3.1416/2*3 #270°
NO_INPUT = -1000
direction = NO_INPUT
waiting_direction = NO_INPUT
flag_is_pressed = False

def keyPressed ( key, x, y):
    global flag_is_pressed, direction, waiting_direction, MOVE_DOWN, MOVE_RIGHT, MOVE_UP, MOVE_LEFT
    if key == b'\x1b':
        glutLeaveMainLoop()
    if key == b'w':
        if flag_is_pressed:
            waiting_direction = MOVE_UP
        else:
            direction = MOVE_UP
            flag_is_pressed = True
    if key == b's':
        if flag_is_pressed:
            waiting_direction = MOVE_DOWN
        else:
            direction = MOVE_DOWN
            flag_is_pressed = True
    if key == b'a':
        if flag_is_pressed:
            waiting_direction = MOVE_LEFT
        else:
            direction = MOVE_LEFT
            flag_is_pressed = True
    if key == b'd':
        if flag_is_pressed:
            waiting_direction = MOVE_RIGHT
        else:
            direction = MOVE_RIGHT
            flag_is_pressed = True

def keyUp(key, x, y):
    global flag_is_pressed, direction, waiting_direction, MOVE_DOWN, MOVE_RIGHT, MOVE_UP, MOVE_LEFT, NO_INPUT
    if key == b'w':
        if direction == MOVE_UP:
            if not(waiting_direction == NO_INPUT):
                direction = waiting_direction
                waiting_direction = NO_INPUT
            else:
                flag_is_pressed = False
    if key == b's':
        if direction == MOVE_DOWN:
            if not(waiting_direction == NO_INPUT):
                direction = waiting_direction
                waiting_direction = NO_INPUT
            else:
                flag_is_pressed = False
    if key == b'a':
        if direction == MOVE_LEFT:
            if not(waiting_direction == NO_INPUT):
                direction = waiting_direction
                waiting_direction = NO_INPUT
            else:
                flag_is_pressed = False
    if key == b'd':
        if direction == MOVE_RIGHT:
            if not(waiting_direction == NO_INPUT):
                direction = waiting_direction
                waiting_direction = NO_INPUT
            else:
                flag_is_pressed = False

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
    global direction, MOVE_DOWN, MOVE_RIGHT, MOVE_UP, MOVE_LEFT, NO_INPUT
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

    #---------------------DIBUJAR AQUI------------------------#
    #Rectangulo con degradado    
    glBegin(GL_QUADS)
    glColor3f(0,0,0)
    glVertex2d(100,100)
    glColor3f(1,0,0)
    glVertex2d(100,200)
    glColor3f(1,1,1)
    glVertex2d(200,200)
    glColor3f(0,0,1)
    glVertex2d(200,100)
    glEnd()
    #PACMAN
    #polygon(xc_circle,yc_circle,radius,32,1,1,1)
    coord_rotated = rotate(pacman_latest_frame, direction) if direction != NO_INPUT else pacman_latest_frame
    coord = translate(coord_rotated,xc_circle,yc_circle)
    glBegin(GL_POLYGON)
    for i in range(len(coord)):
        glVertex2d(coord[i][0], coord[i][1])
    glEnd()

    #Curva Bezier
    points = np.array([[0,250],[250,500],[500,250],[250,0],[0,250]])
    paths = evaluate_bezier(points,50) #Obtener coordenadas de lineas
    path_x, path_y = paths[:,0], paths[:,1]
    glColor3f(0.8,0.8,0.8)
    glBegin(GL_LINE_STRIP)
    for i in range(len(path_x)-1):
        glVertex2d(path_x[i], path_y[i])
    glEnd()
    #---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp = 0
    #global xc_circle, yc_circle, radius, w, h

def timer_movement(value):
    global xc_circle, yc_circle, radius, w, h
    global direction, waiting_direction, MOVE_DOWN, MOVE_RIGHT, MOVE_UP, MOVE_LEFT, NO_INPUT
    global pacman_frame_2, pacman_latest_frame
    pixels = 5
    

    #xc_circle = xc_circle + pixels if (direction == MOVE_RIGHT and (xc_circle + radius + pixels) <= w) else xc_circle
    #xc_circle = xc_circle - pixels if (direction == MOVE_LEFT and (xc_circle - radius - pixels) >= 0) else xc_circle
    #yc_circle = yc_circle + pixels if (direction == MOVE_UP and (yc_circle + radius + pixels) <= h) else yc_circle
    #yc_circle = yc_circle - pixels if (direction == MOVE_DOWN and (yc_circle - radius - pixels) >= 0) else yc_circle

    #Nueva forma de moverse
    if direction == MOVE_RIGHT:
        if (xc_circle + radius + pixels) <= w:
            xc_circle += pixels
        else:
            xc_circle = w - radius
            direction = NO_INPUT
            waiting_direction = NO_INPUT
    if direction == MOVE_LEFT:
        if (xc_circle - radius - pixels) >= 0:
            xc_circle -= pixels
        else:
            xc_circle = radius
            direction = NO_INPUT
            waiting_direction = NO_INPUT
    if direction == MOVE_UP:
        if (yc_circle + radius + pixels) <= h:
            yc_circle += pixels
        else:
            yc_circle = h - radius
            direction = NO_INPUT
            waiting_direction = NO_INPUT
    if direction == MOVE_DOWN:
        if (yc_circle - radius - pixels) >= 0:
            yc_circle -= pixels
        else:
            yc_circle = radius
            direction = NO_INPUT
            waiting_direction = NO_INPUT

    if not (direction == NO_INPUT):
        glutPostRedisplay()
    glutTimerFunc(10,timer_movement,5)

    

def timer_pacman_frame(value):
    global pacman_frame_1, pacman_frame_2, pacman_latest_frame, flag_pacman_frame
    global direction, NO_INPUT
    if direction != NO_INPUT:
        pacman_latest_frame = pacman_frame_1 if flag_pacman_frame else pacman_frame_2
        flag_pacman_frame = not flag_pacman_frame
        glutPostRedisplay()
    glutTimerFunc(100,timer_pacman_frame,5)


def main():
    global w, h, radius, pacman_frame_1, pacman_frame_2, pacman_latest_frame
    pacman_frame_1 = frame_1(radius)
    pacman_frame_2 = frame_2(radius)
    pacman_latest_frame = pacman_frame_2
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