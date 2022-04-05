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
    #__MAX_VELOCITY = 10
    
    def __init__(self, id_element=0,x=0, y=0, w=0, h=0, frames = []):
        self.__position = {'x': 0, 'y': 0}
        self.__last_position = {'x': 0, 'y': 0}
        self.__size = {'x': 0, 'y': 0}
        self.animator = [] #Lista bidimensional con los Frames del objeto
        self.__index_state = 0 #Indice del estado del personaje a animar
        self.__latest_frame = 0 #Indice del frame a dibujar
        self.__mirror = False #mirror es False cuando voltea hacia la derecha
        self.__velocity = {'x': 0, 'y': 0}
        self.__MAX_VELOCITY = 10
        self.__jumping = False
        
        self.__id_element = id_element
        self.__position['x'] = x
        self.__position['y'] = y
        self.__last_position['x'] = x
        self.__last_position['y'] = y
        self.__size['x'] = w
        self.__size['y'] = h
        self.animator = frames

    def move(self, input):
        '''input['x']:
        1.- Mover hacia la derecha
        0.- No se mueve
        -1.- Mover hacia la izquierda'''

        if not self.__jumping and input['y'] == 1:
            self.__jumping = True
            self.__velocity['y'] = self.__MAX_VELOCITY

        if self.__jumping:
            self.__velocity['y'] -= 0.2
            if self.__velocity['y'] < -self.__MAX_VELOCITY:
                self.__velocity['y'] = -self.__MAX_VELOCITY
            self.__last_position['y'] = self.__position['y']
            self.__position['y'] += self.__velocity['y']
            if self.__position['y'] <= 150:
                self.__position['y'] = 150
                self.__jumping = False




        if input['x'] == 0:
            if self.__velocity['x'] != 0:
                self.__velocity['x'] -= 0.1*self.__velocity['x']
            if abs(self.__velocity['x']) < 0.01:
                self.__velocity['x'] = 0 
        else:
            self.__velocity['x'] = self.__position['x'] - self.__last_position['x'] + 0.5*input['x']
            if self.__velocity['x'] > self.__MAX_VELOCITY:
                self.__velocity['x'] = self.__MAX_VELOCITY
            if self.__velocity['x'] < -self.__MAX_VELOCITY:
                self.__velocity['x'] = -self.__MAX_VELOCITY

        self.__last_position['x'] = self.__position['x']
        self.__position['x'] += self.__velocity['x']

    def is_collision(self,obj):
        if not isinstance(obj, GameObject):
            raise Exception('La función requiere un GameObject')
        col_x = self.__position['x'] < obj.__position['x'] + obj.__size['x'] and self.__position['x'] + self.__size['x'] > obj.__position['x']
        col_y = self.__position['y'] < obj.__position['y'] + obj.__size['y'] and self.__position['y'] + self.__size['y'] > obj.__position['y']
        return col_x and col_y

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
    
    def get_id(self):
        return self.__id_element
    
    def get_velocity(self):
        return self.__velocity
        

