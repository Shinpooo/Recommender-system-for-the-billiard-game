from vpython import *
import numpy as np

# x in degrees
def cosinus(x):
    return np.cos(np.deg2rad(x))

def sinus(x):
    return np.sin(np.deg2rad(x))

simulate_cue = False
# TABLE:
# Dimensions extérieures et surface de jeu pour un Billard 2.80

SURFACE_LENGTH = 2.54 #[m]
SURFACE_WIDTH = 1.27 #[m]
SURFACE_THICKNESS = 0.02 #[m]
SIDE_LENGTH = 0.15 #[m]
HEIGHT_RAILS = 0.0375 #[m]
MU_s = 0.2 # Sliding friction
MU_r = 0.016 # Rolling friction
MU_sp = 0.044 # Spinning friction
#See Paper of W.Leckie p6 => Marlow experimental determination
# BALLS:

RADIUS = 0.061/2 #[m]
BALL_MASS = 0.21 #[kg]
INIT_DIST = 0.163 #[m]
g = 9.81 # [m/s²]
P0_WHITE = vector(-SURFACE_WIDTH/2,0,0)
P0_YELLOW = vector(-SURFACE_WIDTH/2,- INIT_DIST,0)
P0_RED = vector(SURFACE_WIDTH/2,0,0)
V0_WHITE = vector(2,0,0)
W0_WHITE = vector(0,0,0)
V0_YELLOW = vector(5,5,0)
W0_YELLOW = vector(0,0,0)
V0_RED = vector(7,4,0)
W0_RED = vector(0,0,0)
#V0_WHITE = vector(3,2,0)
#W0_WHITE = vector(45,59,45)

# COLORS:

green = vector(10, 108, 3)/255
brown = vector(139,69,19)/255

# VECTOR:

e_x = vector(1,0,0)
e_y = vector(0,1,0)
e_z = vector(0,0,1)

EPS = 1e-9

if(simulate_cue):
    #CUE
    #a = 0.5 b = 0 theta = 30 phi = 0 v = 3 => pour bien voir l'effet au roulement
    CUE_MASS = 0.54 # [kg]
    a = 0.5*RADIUS #ecartement horizontal (a>0 sur la gauche)
    b = 0*RADIUS #ecartement vertical (b>0 au-dessus)
    theta = 30 #angle vertical (90 = perpendiculaire a la table)
    phi = 0#angle horzontal (0 = visé vers la droite// 90 = vers le haut// -90 = vers la gauche// 180 = vers la gauche)
    #phi = 45 => pb car touche 2 cotés en même temps 
    V = 3 #vitesse queue
    I = (2/5)*BALL_MASS*RADIUS**2 #Moment d'inertie

    c = abs(sqrt(RADIUS**2 - a**2 - b**2))
    F = 2*BALL_MASS*V/(1 + BALL_MASS/CUE_MASS + (5/(2*RADIUS**2))*(a**2 + (b*cosinus(theta))**2 + (c*sinus(theta))**2 - 2*b*c*cosinus(theta)*sinus(theta)))

    #V0_WHITE.x = -F*cosinus(theta)*cosinus(phi)/BALL_MASS
    #V0_WHITE.y = -F*cosinus(theta)*sinus(phi)/BALL_MASS

    #cf matrice de rotation
    rotation = -90 - (180 - phi)
    compv_x = 0
    compv_y = -F*cosinus(theta)/BALL_MASS
    compv_z = 0
    V0_WHITE.x = compv_x*cosinus(rotation) - compv_y*sinus(rotation)
    V0_WHITE.y = compv_x*sinus(rotation) + compv_y*cosinus(rotation)
    V0_WHITE.z = compv_z

    compw_x = (-c*F*sinus(theta) + b*F*cosinus(theta))/I
    compw_y = a*F*sinus(theta)/I
    compw_z = -a*F*cosinus(theta)/I
    W0_WHITE.x = compw_x*cosinus(rotation) - compw_y*sinus(rotation)
    W0_WHITE.y = compw_x*sinus(rotation) + compw_y*cosinus(rotation)
    W0_WHITE.z = compw_z

print(W0_WHITE.x)
print(W0_WHITE.y)
print(W0_WHITE.z)
