from vpython import *
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

# BALLS:

RADIUS = 0.061/2 #[m]
BALL_MASS = 0.21 #[g]
INIT_DIST = 0.163 #[m]
g = 9.81 # [m/s²]
P0_WHITE = vector(-SURFACE_WIDTH/2,0,0)
P0_YELLOW = vector(-SURFACE_WIDTH/2,- INIT_DIST,0)
P0_RED = vector(SURFACE_WIDTH/2,0,0)
V0_WHITE = vector(1,0,0)
W0_WHITE = vector(0,0,0)

# COLORS:

green = vector(10, 108, 3)/255
brown = vector(139,69,19)/255

# VECTOR:

e_x = vector(1,0,0)
e_y = vector(0,1,0)
e_z = vector(0,0,1)

EPS = 1e-3