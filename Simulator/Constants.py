from vpython import *
import numpy as np

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
V0_WHITE = vector(0,0,0)
W0_WHITE = vector(0,0,0)
V0_YELLOW = vector(0,0,0)
W0_YELLOW = vector(0,0,0)
V0_RED = vector(0,0,0)
W0_RED = vector(0,0,0)

ELAST = 1/2 #N(elasticity coef between balls) cf paper => recherche "Coefficient de restitution" => ivoire : 8/9

# COLORS:

green = vector(10, 108, 3)/255
brown = vector(139,69,19)/255

# VECTOR:

e_x = vector(1,0,0)
e_y = vector(0,1,0)
e_z = vector(0,0,1)

EPS = 1e-9
CUE_MASS = 0.54
I = (2/5)*BALL_MASS*RADIUS**2 #Moment d'inertie
rate_value = 100 #100
def cosinus(x):
    return np.cos(np.deg2rad(x))

def sinus(x):
    return np.sin(np.deg2rad(x))