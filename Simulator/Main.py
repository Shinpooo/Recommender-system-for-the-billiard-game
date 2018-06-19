from Build_in_vpython import*
from vpython import *

BUILD_TABLE()
white_ball, yellow_ball, red_ball = BUILD_BALLS_INITIAL_STATE()

white_ball.P = P0_WHITE
white_ball.v = V0_WHITE
white_ball.w = W0_WHITE
white_ball.u = white_ball.v + RADIUS*cross(e_z,white_ball.w)
white_ball.state = "SLIDING"
if(abs(white_ball.w.z) > EPS):
    white_ball.spin = True
else:
    white_ball.spin = False

MOVE(white_ball,0)
