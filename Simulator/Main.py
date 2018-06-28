from Build_in_vpython import*
from vpython import *

BUILD_TABLE()
white_ball, yellow_ball, red_ball = BUILD_BALLS_INITIAL_STATE()


white_ball.P = P0_WHITE
white_ball.v = V0_WHITE
white_ball.w = W0_WHITE
white_ball.u = white_ball.v + RADIUS*cross(e_z,white_ball.w)
if (mag(white_ball.v)==0):
    white_ball.state = "STATIONNARY"
else:
    if (mag(white_ball.u)<1e-6):
        white_ball.state = "ROLLING"
    else:
        white_ball.state = "SLIDING"

white_ball.col = "WHITE"
if(abs(white_ball.w.z) > EPS):
    white_ball.spin = True
else:
    white_ball.spin = False

yellow_ball.P = P0_YELLOW
yellow_ball.v = V0_YELLOW
yellow_ball.w = W0_YELLOW
yellow_ball.u = yellow_ball.v + RADIUS*cross(e_z,yellow_ball.w)
if (mag(yellow_ball.v)==0):
    yellow_ball.state = "STATIONNARY"
else:
    if (mag(yellow_ball.u)<1e-6):
        yellow_ball.state = "ROLLING"
    else:
        yellow_ball.state = "SLIDING"
yellow_ball.col = "YELLOW"
if(abs(yellow_ball.w.z)> EPS):
    yellow_ball.spin = True
else:
    yellow_ball.spin = False

red_ball.P = P0_RED
red_ball.v = V0_RED
red_ball.w = W0_RED
red_ball.u = red_ball.v + RADIUS*cross(e_z,red_ball.w)
if (mag(red_ball.v)==0):
    red_ball.state = "STATIONNARY"
else:
    if (mag(red_ball.u)<1e-6):
        red_ball.state = "ROLLING"
    else:
        red_ball.state = "SLIDING"
red_ball.col = "RED"
if(abs(red_ball.w.z) > EPS):
    red_ball.spin = True
else:
    red_ball.spin = False
balls = []
balls.append(white_ball)
balls.append(yellow_ball)
balls.append(red_ball)

#MOVE(red_ball,0)
#MOVE(white_ball,0)
MOVE_BALLS(balls,0)
