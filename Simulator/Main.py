from Build_in_vpython import*
from Event_manager import*

BUILD_TABLE()
white_ball, yellow_ball, red_ball = BUILD_BALLS_INITIAL_STATE()

white_ball.P = P0_WHITE
white_ball.v = V0_WHITE
white_ball.w = W0_WHITE
white_ball.u = white_ball.v + RADIUS*cross(e_z,white_ball.w)
white_ball.state = "SLIDING"
MOVE(white_ball,0)
# time0 = 0
# time1 = NEXT_EVENT_AFTER_SLIDING(white_ball, time0)
# white_ball = SLIDING(white_ball,time0,time1)
# time2 = NEXT_EVENT_AFTER_ROLLING(white_ball,time1)
# white_ball = ROLLING(white_ball,time1,time2)
# white_ball = VERTICAL_RAIL_COLLISION(white_ball)
# time3 = NEXT_EVENT_AFTER_ROLLING(white_ball,time2)

# white_ball = ROLLING(white_ball,time2,time3)
# print(time0)
# print(time1)
# print(time2)
# print(time3)

# 0
# 0.14562399883500798
# 3.454346183008374
# 5.291742841923314