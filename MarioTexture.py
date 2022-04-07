from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.draw import *
from modules.transforms import *
from modules.textures import loadTexture
from modules.gameobject import GameObject
import random
from playsound import playsound #Instalar con pip install playsound==1.2.2
from threading import Thread

w,h= 1000,500


#Texturas fondo
texture_floor = []
texture_mountain = []
texture_cloud = []
clouds_coord = []


#Textura de Mario
#Arreglo bidimensional 
MARIO_IDLE = 0
MARIO_RUN = 1
MARIO_JUMP = 2
texture_mario = []
texture_goomba = []
counter_elements = 0


#Elementos de Mario
mario_gameobject = GameObject()

#Elementos Goomba
goombas = []
dummy_goomba = GameObject(-1,0,0,40,40,texture_goomba) #Sirve para checar colisiones antes de crear el goomba bueno

#Movimiento
flag_left = False
flag_right = False
flag_up = False
flag_down = False
GROUND_LEVEL = 100


#SONIDOS
def play_stomp():
    playsound('Resources/smb_stomp.wav')

def play_jump():
    playsound('Resources/smb_jump-super.wav')


#Dibujar fondo
def draw_background():
    global texture_floor, texture_mountain, texture_cloud
    global clouds_coord
    #Dibujar 5 nubes
    glBindTexture(GL_TEXTURE_2D, texture_cloud[0])
    for i in range(len(clouds_coord)):
        x_coord = clouds_coord[i][0]
        y_coord = clouds_coord[i][1]
        width = clouds_coord[i][2]
        height = clouds_coord[i][3]
        
        
        glBegin(GL_POLYGON)
        glTexCoord2f(0,0)
        glVertex2d(x_coord,y_coord)
        glTexCoord2f(1,0)
        glVertex2d(x_coord + width,y_coord)
        glTexCoord2f(1,1)
        glVertex2d(x_coord + width,y_coord + height)
        glTexCoord2f(0,1)
        glVertex2d(x_coord,y_coord + height)
        glEnd()

    #Dibujar montaña pequeña
    x_coord = 500
    y_coord = 90
    width = 317
    height = 150
    glBindTexture(GL_TEXTURE_2D, texture_mountain[0])
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(x_coord,y_coord)
    glTexCoord2f(1,0)
    glVertex2d(x_coord + width,y_coord)
    glTexCoord2f(1,1)
    glVertex2d(x_coord + width,y_coord + height)
    glTexCoord2f(0,1)
    glVertex2d(x_coord,y_coord + height)
    glEnd()
    
    #Dibujar montaña
    x_coord = 100
    y_coord = 90
    width = 436
    height = 200
    
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(x_coord,y_coord)
    glTexCoord2f(1,0)
    glVertex2d(x_coord + width,y_coord)
    glTexCoord2f(1,1)
    glVertex2d(x_coord + width,y_coord + height)
    glTexCoord2f(0,1)
    glVertex2d(x_coord,y_coord + height)
    glEnd()

    #Dibujar piso
    n_tiles_x = (int)(w/50) + 1
    n_tiles_y = (int)(100/50)
    for i in range(n_tiles_x):
        for j in range(n_tiles_y):
            x_coord = i*50
            y_coord = j*50
            width = 50
            height = 50
            glBindTexture(GL_TEXTURE_2D, texture_floor[0])
            glBegin(GL_POLYGON)
            glTexCoord2f(0,0)
            glVertex2d(x_coord,y_coord)
            glTexCoord2f(1,0)
            glVertex2d(x_coord + width,y_coord)
            glTexCoord2f(1,1)
            glVertex2d(x_coord + width,y_coord + height)
            glTexCoord2f(0,1)
            glVertex2d(x_coord,y_coord + height)
            glEnd()
    

#Dibujar Mario
def draw_mario():
    global mario_gameobject
    x,y = mario_gameobject.get_position()
    w,h = mario_gameobject.get_size()
    pin_x_start, pin_x_end = (1,0) if mario_gameobject.is_mirrored() else (0,1)
    glBindTexture(GL_TEXTURE_2D, mario_gameobject.get_frame_to_draw())
    glBegin(GL_POLYGON)
    glTexCoord2f(pin_x_start,0)
    glVertex2d(x,y)
    glTexCoord2f(pin_x_end,0)
    glVertex2d(x+w,y)
    glTexCoord2f(pin_x_end,1)
    glVertex2d(x+w,y+h)
    glTexCoord2f(pin_x_start,1)
    glVertex2d(x,y+h)
    glEnd()

#Dibujar Goomba
def draw_goombas():
    global goombas
    for i in range(len(goombas)):
        goomba_gameobject = goombas[i]
        x,y = goomba_gameobject.get_position()
        w,h = goomba_gameobject.get_size()
        pin_x_start, pin_x_end = (0,1)
        glBindTexture(GL_TEXTURE_2D, goomba_gameobject.get_frame_to_draw())
        glBegin(GL_POLYGON)
        glTexCoord2f(pin_x_start,0)
        glVertex2d(x,y)
        glTexCoord2f(pin_x_end,0)
        glVertex2d(x+w,y)
        glTexCoord2f(pin_x_end,1)
        glVertex2d(x+w,y+h)
        glTexCoord2f(pin_x_start,1)
        glVertex2d(x,y+h)
        glEnd()

#COLISIONES
def check_collisions():
    global goombas, mario_gameobject
    for i in range(len(goombas)):
        if mario_gameobject.is_collision(goombas[i]):
            thread_stomp = Thread(target=play_stomp)
            thread_stomp.start()
            goombas.pop(i)
            return


def keyPressed ( key, x, y):
    global flag_left, flag_right, flag_up, flag_down
    if key == b'\x1b':
        glutLeaveMainLoop()
    if key == b'w':
        flag_up = True
    if key == b's':
        flag_down = True
    if key == b'a':
        flag_left = True
    if key == b'd':
        flag_right = True

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
    glClearColor ( 0.5725, 0.5647, 1.0, 0.0 )
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

    #---------------------DIBUJAR AQUI------------------------#
    draw_background()
    draw_mario()
    draw_goombas()
    #---------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp = 0
    #global xc_circle, yc_circle, radius, w, h

#-----------------TIMERS--------------------------#
def timer_move_mario(value):
    global mario_gameobject, flag_left, flag_right, flag_up
    global MARIO_IDLE, MARIO_RUN, MARIO_JUMP
    state = mario_gameobject.get_state()
    input = {'x': 0, 'y': 0}
    input['y'] = 1 if flag_up else 0
    if flag_right:
        input['x'] = 1
    elif flag_left:
        input['x'] = -1
    jumping_before = mario_gameobject.is_jumping()
    mario_gameobject.move(input)
    if not jumping_before and mario_gameobject.is_jumping():
        thread_jump = Thread(target=play_jump)
        thread_jump.start()

    velocity = mario_gameobject.get_velocity()

    if velocity['y'] != 0:
        if state != MARIO_JUMP:
            mario_gameobject.change_state(MARIO_JUMP)
    elif velocity['x'] > 0:
        if state != MARIO_RUN:
            mario_gameobject.change_state(MARIO_RUN)
        if mario_gameobject.is_mirrored():
            mario_gameobject.set_mirror(False)
    elif velocity['x'] < 0:
        if state != MARIO_RUN:
            mario_gameobject.change_state(MARIO_RUN)
        if not mario_gameobject.is_mirrored():
            mario_gameobject.set_mirror(True)
    else:
        if state != MARIO_IDLE:
            mario_gameobject.change_state(MARIO_IDLE)


    check_collisions()
    glutPostRedisplay()
    glutTimerFunc(20, timer_move_mario, 1)

def timer_animate_mario(value):
    global mario_gameobject
    mario_gameobject.animate()
    glutPostRedisplay()
    glutTimerFunc(100, timer_animate_mario,1)

def timer_move_goomba(id_goomba):
    global goombas, w
    for i in range(len(goombas)):
        if goombas[i].get_id() == id_goomba:
            goombas[i].static_move(goombas,w)
            glutPostRedisplay()
            glutTimerFunc(20, timer_move_goomba, id_goomba)


def timer_animate_goomba(id_goomba):
    global goombas
    for i in range(len(goombas)):
        if goombas[i].get_id() == id_goomba:
            goombas[i].animate()
            glutPostRedisplay()
            glutTimerFunc(200, timer_animate_goomba, id_goomba)

def timer_create_goomba(value):
    global goombas, texture_goomba, counter_elements, dummy_goomba
    id_goomba = counter_elements
    pos_x = 0
    flag_correct = False
    while not flag_correct:
        flag_correct = True
        pos_x = random.randint(0, w-40)
        dummy_goomba.set_position({'x':pos_x, 'y':GROUND_LEVEL})
        #Checar colisiones de goomba nuevo
        for i in range(len(goombas)):
            if dummy_goomba.is_collision(goombas[i]):
                flag_correct = False
                i = len(goombas)



    goomba = GameObject(id_goomba,pos_x,GROUND_LEVEL,40,40, texture_goomba)
    counter_elements += 1
    goombas.append(goomba)
    #glutPostRedisplay()
    timer_animate_goomba(id_goomba)
    timer_move_goomba(id_goomba)
    glutTimerFunc(3000, timer_create_goomba, 1)

#-------------------------------------------------#




def main():
    global texture_mario, mario_gameobject, GROUND_LEVEL, counter_elements
    global texture_cloud, texture_floor, texture_mountain, clouds_coord
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


    #Texturas fondo
    texture_floor.append(loadTexture('Resources/Floor.png'))
    texture_mountain.append(loadTexture('Resources/BigMountain.png'))
    texture_cloud.append(loadTexture('Resources/BigCloud.png'))

    #Coordenadas de nubes
    for i in range(5):
        height = random.randint(30,100)
        width = (int)(height*2.67)
        x_coord = random.randint(0,w-width)
        y_coord = random.randint(120,h-height)
        clouds_coord.append([x_coord,y_coord,width,height])

    #Cargar textura
    texture_mario.append([loadTexture('Resources/MarioIdle.png')])
    texture_mario.append([loadTexture('Resources/MarioRun1.png'),loadTexture('Resources/MarioRun2.png'),loadTexture('Resources/MarioRun3.png')])
    texture_mario.append([loadTexture('Resources/MarioJump.png')])
    mario_gameobject = GameObject(counter_elements,250,GROUND_LEVEL,(int)(180/4),(int)(196/4), texture_mario)
    counter_elements += 1

    texture_goomba.append([loadTexture('Resources/Goomba1.png'), loadTexture('Resources/Goomba2.png')])

    timer_move_mario(0)
    timer_animate_mario(0)
    timer_create_goomba(0)

    glutMainLoop()

print("Presiona Escape para cerrar.")
main()