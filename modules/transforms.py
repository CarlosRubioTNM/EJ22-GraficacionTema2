import numpy as np
#--------------------TRANSFORMACIONES----------------------------#
def translate(coordinates, x_dist, y_dist):
    #coordinates es lista bidimensional con valores de x y y.
    coord = []
    for i in range(len(coordinates)):
        coord.append([coordinates[i][0]+x_dist, coordinates[i][1]+y_dist])
        
    return coord

def resize(coordinates, ex, ey):
    #coordinates es lista bidimensional con valores de x y y.
    for i in range(len(coordinates)):
        coordinates[i][0] = int(coordinates[i][0]*ex)
        coordinates[i][1] = int(coordinates[i][1]*ey)
    return coordinates

def rotate(coordinates, theta):
    #Theta en radianes
    coord = []
    for i in range(len(coordinates)):
        new_x = int(coordinates[i][0]*np.cos(theta) + coordinates[i][1]*np.sin(theta))
        new_y = int(-coordinates[i][0]*np.sin(theta) + coordinates[i][1]*np.cos(theta))
        coord.append([new_x, new_y])
    return coord
#----------------------------------------------------------------#