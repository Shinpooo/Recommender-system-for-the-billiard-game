from numpy.polynomial import Polynomial as P
from Parameters import*
from Build_in_vpython import*

def NEXT_EVENT_AFTER_SLIDING(ball, time):
	real_solutions = []

	## TIME END SLIDING ##
	time_end_sliding = 2*mag(ball.u)/(7*MU_s*g)
	real_solutions.append(time_end_sliding)

	## TIME COLLISION WITH RAIL ##
	p = P([ball.P.x - (SURFACE_LENGTH/2 - RADIUS), ball.v.x, -0.5*MU_s*g*hat(ball.u).x])
	solutions = p.roots()
	real_solutions += [i for i in solutions if i.imag == 0]

	## TIME COLLISION WITH BALL


	min_time = min(x for x in real_solutions if x > EPS) + time

	return min_time

def NEXT_EVENT_AFTER_ROLLING(ball,time):
	# print(time)
	real_solutions = []

	## TIME END ROLLING ##
	time_end_rolling = (7/5)*(mag(ball.v)/(MU_r*g))
	real_solutions.append(time_end_rolling)

	## TIME COLLISION WITH RAIL ##
	p = P([ball.P.x - (SURFACE_LENGTH/2 - RADIUS), ball.v.x, -(5/14)*MU_r*g*hat(ball.u).x])
	solutions = p.roots() 
	real_solutions += [i for i in solutions if i.imag == 0]

	min_time = min(x for x in real_solutions if x > EPS) + time# EPS sinon sol pour t = 0 
	return min_time


def NEXT_EVENT(ball, time):
	real_solutions = []
	# EVENTS = ["SLI2ROL","ROL2STA","VERT_RAIL_COL","VERT_RAIL_COL","VERT_RAIL_COL","VERT_RAIL_COL",
	# "HORI_RAIL_COL","HORI_RAIL_COL","HORI_RAIL_COL","HORI_RAIL_COL"]
	EVENTS = []
	## TIME END SLIDING ##
	if ball.state == "SLIDING":
		coef = 0.5*MU_s
		time_end_sliding = 2*mag(ball.u)/(7*MU_s*g)
		real_solutions.append(time_end_sliding)
		EVENTS.append("SLI2ROL")
	elif ball.state =="ROLLING":
		coef = (5/14)*MU_r
		time_end_rolling = (7/5)*(mag(ball.v)/(MU_r*g))
		real_solutions.append(time_end_rolling)
		EVENTS.append("ROL2STA")

	## TIME COLLISION WITH RIGHT RAIL ##
	p = P([ball.P.x - (SURFACE_LENGTH/2 - RADIUS), ball.v.x, -coef*g*hat(ball.u).x])
	solutions = p.roots()
	real_solutions.extend([i for i in solutions if i.imag == 0])
	length_added_sol = len([i for i in solutions if i.imag == 0])
	EVENTS.extend(["VERT_RAIL_COL" for i in range(length_added_sol)])

	## TIME COLLISION WITH LEFT RAIL ##
	p = P([ball.P.x - (-SURFACE_LENGTH/2 + RADIUS), ball.v.x, -coef*g*hat(ball.u).x])
	solutions = p.roots()
	real_solutions.extend([i for i in solutions if i.imag == 0])
	length_added_sol = len([i for i in solutions if i.imag == 0])
	EVENTS.extend(["VERT_RAIL_COL" for i in range(length_added_sol)])

	# ## TIME COLLISION WITH UP RAIL ##
	p = P([ball.P.y - (SURFACE_WIDTH/2 - RADIUS), ball.v.y, -coef*g*hat(ball.u).y])
	solutions = p.roots()
	real_solutions.extend([i for i in solutions if i.imag == 0])
	length_added_sol = len([i for i in solutions if i.imag == 0])
	EVENTS.extend(["HORI_RAIL_COL" for i in range(length_added_sol)])

	# ## TIME COLLISION WITH DOWN RAIL ##
	p = P([ball.P.y - (-SURFACE_WIDTH/2 + RADIUS), ball.v.y, -coef*g*hat(ball.u).y])
	solutions = p.roots()
	real_solutions.extend([i for i in solutions if i.imag == 0])
	length_added_sol = len([i for i in solutions if i.imag == 0])
	EVENTS.extend(["HORI_RAIL_COL" for i in range(length_added_sol)])

	## TIME COLLISION WITH BALL
	#  ....

	min_time = min(x for x in real_solutions if x > EPS)
	print(real_solutions)
	print(EVENTS)
	min_index = real_solutions.index(min_time)
	found_event = EVENTS[min_index]
	print(min_index)
	min_time += time
	# print(min_time)
	return found_event, min_time

def EVENT_PROCESSING(ball, event):
	if event == "SLI2ROL":
		ball.state = "ROLLING"
	elif event == "ROL2STA":
		ball.state = "STATIONNARY"
	elif event == "VERT_RAIL_COL":
		ball = VERTICAL_RAIL_COLLISION(ball)
	elif event == "HORI_RAIL_COL":
		ball = HORIZONTAL_RAIL_COLLISION(ball)
	return ball

def HORIZONTAL_RAIL_COLLISION(ball): #FastFiz equations
	ball.v.x = 0.9*ball.v.x
	ball.v.y = -0.6*ball.v.y
	ball.w = 0.1*ball.w
	ball.u = ball.v + RADIUS*cross(e_z,ball.w)
	return ball

def VERTICAL_RAIL_COLLISION(ball): #FastFiz equations # change?
	ball.v.x = -0.6*ball.v.x
	ball.v.y = 0.9*ball.v.y
	ball.w = 0.1*ball.w
	ball.u = ball.v + RADIUS*cross(e_z,ball.w)
	return ball

	# if ball.state == "SLIDING":
 	# 		if min_time == time_end_sliding:
 	# 			ball.state = "ROLLING"
	# elif ball.state == "ROLLING":
	# 	if min_time == time_end_rolling:
	# 		ball.state = "STATIONNARY"