class GameObject:
    """Clase para objectos como Mario y Goomba"""
    #__position = {'x': 0, 'y': 0}
    #__last_position = {'x': 0, 'y': 0}
    #__size = {'x': 0, 'y': 0}
    #animator = [] #Lista bidimensional con los Frames del objeto
    #__index_state = 0 #Indice del estado del personaje a animar
    #__latest_frame = 0 #Indice del frame a dibujar
    #__mirror = False #mirror es False cuando voltea hacia la derecha
    #__velocity = {'x': 0, 'y': 0}
    __MAX_VELOCITY = 10
    
    def __init__(self, x=0, y=0, w=0, h=0, frames = []):
        self.__position = {'x': 0, 'y': 0}
        self.__last_position = {'x': 0, 'y': 0}
        self.__size = {'x': 0, 'y': 0}
        self.animator = [] #Lista bidimensional con los Frames del objeto
        self.__index_state = 0 #Indice del estado del personaje a animar
        self.__latest_frame = 0 #Indice del frame a dibujar
        self.__mirror = False #mirror es False cuando voltea hacia la derecha
        self.__velocity = {'x': 0, 'y': 0}
        
        self.__position['x'] = x
        self.__position['y'] = y
        self.__last_position['x'] = x
        self.__last_position['y'] = y
        self.__size['x'] = w
        self.__size['y'] = h
        self.animator = frames

    def move(self, input):
        '''Input:
        1.- Mover hacia la derecha
        0.- No se mueve
        -1.- Mover hacia la izquierda'''
        if input == 0:
            if self.__velocity['x'] != 0:
                self.__velocity['x'] -= 0.1*self.__velocity['x']
            if abs(self.__velocity['x']) < 0.01:
                self.__velocity['x'] = 0 
        else:
            self.__velocity['x'] = self.__position['x'] - self.__last_position['x'] + 0.5*input
            if self.__velocity['x'] > self.__MAX_VELOCITY:
                self.__velocity['x'] = self.__MAX_VELOCITY
            if self.__velocity['x'] < -self.__MAX_VELOCITY:
                self.__velocity['x'] = -self.__MAX_VELOCITY

        self.__last_position['x'] = self.__position['x']
        self.__position['x'] += self.__velocity['x']

    def change_state(self, index):
        if index >= len(self.animator):
            raise Exception('El índice está fuera del límite permitido.')
        self.__index_state = index
        self.__latest_frame = 0
    
    def get_state(self):
        return self.__index_state

    def animate(self):
        if len(self.animator[self.__index_state]) == 1:
            return
        self.__latest_frame = 0 if self.__latest_frame >= (len(self.animator[self.__index_state]) - 1) else self.__latest_frame + 1

    def get_frame_to_draw(self):
        return self.animator[self.__index_state][self.__latest_frame]
    
    def get_position(self):
        return self.__position['x'], self.__position['y']
    
    def get_size(self):
        return self.__size['x'], self.__size['y']

    def set_mirror(self, value):
        self.__mirror = value

    def is_mirrored(self):
        return self.__mirror
        

