from numpy.polynomial import Polynomial as P
from Parameters import*
#import numpy as np

def NEXT_EVENT(ball, time):
	real_solutions = []
	# EVENTS = ["SLI2ROL","ROL2STA","VERT_RAIL_COL","VERT_RAIL_COL","VERT_RAIL_COL","VERT_RAIL_COL",
	# "HORI_RAIL_COL","HORI_RAIL_COL","HORI_RAIL_COL","HORI_RAIL_COL","END_SPIN"]
	EVENTS = []
	## TIME END SLIDINGROLLING ##
	if ball.state == "SLIDING":
		coef_x = 0.5*MU_s*hat(ball.u).x
		coef_y = 0.5*MU_s*hat(ball.u).y
		time_end_sliding = 2*mag(ball.u)/(7*MU_s*g)
		real_solutions.append(time_end_sliding)
		EVENTS.append("SLI2ROL")
	elif ball.state =="ROLLING":
		coef_x = (5/14)*MU_r*hat(ball.v).x
		coef_y = (5/14)*MU_r*hat(ball.v).y
		time_end_rolling = (7/5)*(mag(ball.v)/(MU_r*g))
		real_solutions.append(time_end_rolling)
		EVENTS.append("ROL2STA")

	## TIME COLLISION WITH RIGHT RAIL ##
	p = P([ball.P.x - (SURFACE_LENGTH/2 - RADIUS), ball.v.x, -coef_x*g])
	solutions = p.roots()
	real_solutions.extend([i for i in solutions if i.imag == 0])
	length_added_sol = len([i for i in solutions if i.imag == 0])
	EVENTS.extend(["VERT_RAIL_COL" for i in range(length_added_sol)])

	## TIME COLLISION WITH LEFT RAIL ##
	p = P([ball.P.x - (-SURFACE_LENGTH/2 + RADIUS), ball.v.x, -coef_x*g])
	solutions = p.roots()
	real_solutions.extend([i for i in solutions if i.imag == 0])
	length_added_sol = len([i for i in solutions if i.imag == 0])
	EVENTS.extend(["VERT_RAIL_COL" for i in range(length_added_sol)])

	# ## TIME COLLISION WITH UP RAIL ##
	p = P([ball.P.y - (SURFACE_WIDTH/2 - RADIUS), ball.v.y, -coef_y*g])
	solutions = p.roots()
	real_solutions.extend([i for i in solutions if i.imag == 0])
	length_added_sol = len([i for i in solutions if i.imag == 0])
	EVENTS.extend(["HORI_RAIL_COL" for i in range(length_added_sol)])

	# ## TIME COLLISION WITH DOWN RAIL ##
	p = P([ball.P.y - (-SURFACE_WIDTH/2 + RADIUS), ball.v.y, -coef_y*g])
	solutions = p.roots()
	#coef = [-coef*g*hat(ball.u).y,ball.v.y,ball.P.y - (-SURFACE_WIDTH/2 + RADIUS)]
	#solutions = np.roots(coef)
	real_solutions.extend([i for i in solutions if i.imag == 0])
	length_added_sol = len([i for i in solutions if i.imag == 0])
	EVENTS.extend(["HORI_RAIL_COL" for i in range(length_added_sol)])

	## TIME STOP SPIN
	time_end_spinning = np.sign(ball.w.z)*2*RADIUS*(ball.w.z)/(5*MU_sp*g)
	real_solutions.append(time_end_spinning)
	EVENTS.append("END_SPIN")

	## TIME COLLISION WITH BALL
	#  ....

	min_time = min(x for x in real_solutions if x > EPS)
	#print(real_solutions)
	#print(EVENTS)
	min_index = real_solutions.index(min_time)
	found_event = EVENTS[min_index]
	#print(min_index)
	#print(min_time)
	min_time = min_time + time
	#print(min_time)
	return found_event, min_time

def NEXT_EVENT_BALLS(balls, time):
	real_solutions = []
	# EVENTS = ["SLI2ROL","ROL2STA","VERT_RAIL_COL","VERT_RAIL_COL","VERT_RAIL_COL","VERT_RAIL_COL",
	# "HORI_RAIL_COL","HORI_RAIL_COL","HORI_RAIL_COL","HORI_RAIL_COL","END_SPIN"]
	EVENTS = []
	## TIME END SLIDINGROLLING ##
	for ball in balls:
		if ball.state != "STATIONNARY":
			prefix = ball.col
			if ball.state == "SLIDING":
				coef_x = 0.5*MU_s*hat(ball.u).x
				coef_y = 0.5*MU_s*hat(ball.u).y
				time_end_sliding = 2*mag(ball.u)/(7*MU_s*g)
				real_solutions.append(time_end_sliding)
				EVENTS.append(prefix + "SLI2ROL")
			elif ball.state =="ROLLING":
				coef_x = (5/14)*MU_r*hat(ball.v).x
				coef_y = (5/14)*MU_r*hat(ball.v).y
				time_end_rolling = (7/5)*(mag(ball.v)/(MU_r*g))
				real_solutions.append(time_end_rolling)
				EVENTS.append(prefix + "ROL2STA")

			## TIME COLLISION WITH RIGHT RAIL ##
			p = P([ball.P.x - (SURFACE_LENGTH/2 - RADIUS), ball.v.x, -coef_x*g])
			solutions = p.roots()
			real_solutions.extend([i for i in solutions if i.imag == 0])
			length_added_sol = len([i for i in solutions if i.imag == 0])
			EVENTS.extend([prefix + "RIGHT_RAIL_COL" for i in range(length_added_sol)])

			## TIME COLLISION WITH LEFT RAIL ##
			p = P([ball.P.x - (-SURFACE_LENGTH/2 + RADIUS), ball.v.x, -coef_x*g])
			solutions = p.roots()
			real_solutions.extend([i for i in solutions if i.imag == 0])
			length_added_sol = len([i for i in solutions if i.imag == 0])
			EVENTS.extend([prefix + "LEFT_RAIL_COL" for i in range(length_added_sol)])

			# ## TIME COLLISION WITH UP RAIL ##
			p = P([ball.P.y - (SURFACE_WIDTH/2 - RADIUS), ball.v.y, -coef_y*g])
			solutions = p.roots()
			real_solutions.extend([i for i in solutions if i.imag == 0])
			length_added_sol = len([i for i in solutions if i.imag == 0])
			EVENTS.extend([prefix + "UP_RAIL_COL" for i in range(length_added_sol)])

			# ## TIME COLLISION WITH DOWN RAIL ##
			p = P([ball.P.y - (-SURFACE_WIDTH/2 + RADIUS), ball.v.y, -coef_y*g])
			solutions = p.roots()
			#coef = [-coef*g*hat(ball.u).y,ball.v.y,ball.P.y - (-SURFACE_WIDTH/2 + RADIUS)]
			#solutions = np.roots(coef)
			real_solutions.extend([i for i in solutions if i.imag == 0])
			length_added_sol = len([i for i in solutions if i.imag == 0])
			EVENTS.extend([prefix + "DOWN_RAIL_COL" for i in range(length_added_sol)])

			## TIME STOP SPIN
			if ball.spin:
				time_end_spinning = np.sign(ball.w.z)*2*RADIUS*(ball.w.z)/(5*MU_sp*g)
				real_solutions.append(time_end_spinning)
				EVENTS.append(prefix + "END_SPIN")

			## TIME COLLISION WITH BALL
			#  ....
			if ball.col == "WHITE":
    				######## COLLISION BLANCHE JAUNE ###########
				if balls[1].state == "SLIDING":
					coef_x2 = 0.5*MU_s*hat(balls[1].u).x
					coef_y2 = 0.5*MU_s*hat(balls[1].u).y
				elif balls[1].state =="ROLLING":
					coef_x2 = (5/14)*MU_r*hat(balls[1].v).x
					coef_y2 = (5/14)*MU_r*hat(balls[1].v).y	
				elif balls[1].state =="STATIONNARY":
					coef_x2 = 0
					coef_y2 = 0
				a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
				b = g*(-2*(ball.v.x - balls[1].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[1].v.y)*(coef_y - coef_y2))
				c = (ball.v.x - balls[1].v.x)**2 - 2*g*(ball.P.x - balls[1].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[1].v.y)**2 - 2*g*(ball.P.y - balls[1].P.y)*(coef_y - coef_y2)
				d = 2*(ball.P.x - balls[1].P.x)*(ball.v.x - balls[1].v.x) + 2*(ball.P.y - balls[1].P.y)*(ball.v.y - balls[1].v.y)
				e = (ball.P.x - balls[1].P.x)**2 + (ball.P.y - balls[1].P.y)**2 -4*(RADIUS**2)
				coef_eq=[a,b,c,d,e]
				solutions = np.roots(coef_eq)
				real_solutions.extend([i for i in solutions if i.imag == 0])
				length_added_sol = len([i for i in solutions if i.imag == 0])
				EVENTS.extend([prefix + "-YELLOW-BALLBALL" for i in range(length_added_sol)])	
				###### COLLISION BLANCHE -> ROUGE ########	
				if balls[2].state == "SLIDING":
					coef_x2 = 0.5*MU_s*hat(balls[2].u).x
					coef_y2 = 0.5*MU_s*hat(balls[2].u).y
				elif balls[2].state =="ROLLING":
					coef_x2 = (5/14)*MU_r*hat(balls[2].v).x
					coef_y2 = (5/14)*MU_r*hat(balls[2].v).y	
				elif balls[2].state =="STATIONNARY":
					coef_x2 = 0
					coef_y2 = 0
				a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
				b = g*(-2*(ball.v.x - balls[2].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[2].v.y)*(coef_y - coef_y2))
				c = (ball.v.x - balls[2].v.x)**2 - 2*g*(ball.P.x - balls[2].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[2].v.y)**2 - 2*g*(ball.P.y - balls[2].P.y)*(coef_y - coef_y2)
				d = 2*(ball.P.x - balls[2].P.x)*(ball.v.x - balls[2].v.x) + 2*(ball.P.y - balls[2].P.y)*(ball.v.y - balls[2].v.y)
				e = (ball.P.x - balls[2].P.x)**2 + (ball.P.y - balls[2].P.y)**2 -4*(RADIUS**2)
				coef_eq=[a,b,c,d,e]
				solutions = np.roots(coef_eq)
				real_solutions.extend([i for i in solutions if i.imag == 0])
				length_added_sol = len([i for i in solutions if i.imag == 0])
				EVENTS.extend([prefix + "-RED-BALLBALL" for i in range(length_added_sol)])

			if ball.col == "YELLOW":
    				######## COLLISION JAUNE ROUGE ###########
				if balls[2].state == "SLIDING":
					coef_x2 = 0.5*MU_s*hat(balls[2].u).x
					coef_y2 = 0.5*MU_s*hat(balls[2].u).y
				elif balls[2].state =="ROLLING":
					coef_x2 = (5/14)*MU_r*hat(balls[2].v).x
					coef_y2 = (5/14)*MU_r*hat(balls[2].v).y	
				elif balls[2].state =="STATIONNARY":
					coef_x2 = 0
					coef_y2 = 0
				a = (g**2)*((coef_x - coef_x2)**2 + (coef_y - coef_y2)**2)
				b = g*(-2*(ball.v.x - balls[2].v.x)*(coef_x - coef_x2) - 2*(ball.v.y - balls[2].v.y)*(coef_y - coef_y2))
				c = (ball.v.x - balls[2].v.x)**2 - 2*g*(ball.P.x - balls[2].P.x)*(coef_x - coef_x2) + (ball.v.y - balls[2].v.y)**2 - 2*g*(ball.P.y - balls[2].P.y)*(coef_y - coef_y2)
				d = 2*(ball.P.x - balls[2].P.x)*(ball.v.x - balls[2].v.x) + 2*(ball.P.y - balls[2].P.y)*(ball.v.y - balls[2].v.y)
				e = (ball.P.x - balls[2].P.x)**2 + (ball.P.y - balls[2].P.y)**2 -4*(RADIUS**2)
				coef_eq=[a,b,c,d,e]
				solutions = np.roots(coef_eq)
				real_solutions.extend([i for i in solutions if i.imag == 0])
				length_added_sol = len([i for i in solutions if i.imag == 0])
				EVENTS.extend([prefix + "-RED-BALLBALL" for i in range(length_added_sol)])
			


	min_time = min(x for x in real_solutions if x > EPS)
	#print(real_solutions)
	#print(EVENTS)
	min_index = real_solutions.index(min_time)
	found_event = EVENTS[min_index]
	#print(min_index)
	#print(min_time)
	min_time = min_time + time
	return found_event, min_time.real

def EVENT_PROCESSING(ball, event):
	print(event)
	if event == "SLI2ROL":
		ball.state = "ROLLING"
	elif event == "ROL2STA":
		ball.state = "STATIONNARY"
	elif event == "VERT_RAIL_COL":
		ball = VERTICAL_RAIL_COLLISION(ball)
	elif event == "HORI_RAIL_COL":
		ball = HORIZONTAL_RAIL_COLLISION(ball)
	elif event == "END_SPIN":
		ball.spin = False
	return ball

def EVENT_PROCESSING_BALLS(balls, event):
	print(event)
	for ball in balls:
		if event == ball.col + "SLI2ROL":
			ball.state = "ROLLING"
		elif event == ball.col + "ROL2STA":
			ball.state = "STATIONNARY"
		elif event == ball.col + "LEFT_RAIL_COL":
			#ball = VERTICAL_RAIL_COLLISION(ball)
			ball = RAIL_COLLISION(ball, "left")
		elif event == ball.col + "RIGHT_RAIL_COL":
    		#ball = VERTICAL_RAIL_COLLISION(ball)
			ball = RAIL_COLLISION(ball, "right")
		elif event == ball.col + "UP_RAIL_COL":
			#ball = HORIZONTAL_RAIL_COLLISION(ball)
			ball = RAIL_COLLISION(ball, "up")
		elif event == ball.col + "DOWN_RAIL_COL":
    		#ball = HORIZONTAL_RAIL_COLLISION(ball)
			ball = RAIL_COLLISION(ball, "down")
		elif event == ball.col + "END_SPIN":
			ball.spin = False
		elif event == ball.col + "-YELLOW-BALLBALL":
			ball, balls[1] = BALLS_COLLISION(ball, balls[1])
		elif event == ball.col + "-RED-BALLBALL":
			ball, balls[2] = BALLS_COLLISION(ball, balls[2])
	return balls

def HORIZONTAL_RAIL_COLLISION(ball): #FastFiz equations
	ball.v.x = 0.9*ball.v.x
	ball.v.y = -0.6*ball.v.y
	ball.w = 0.1*ball.w
	ball.u = ball.v + RADIUS*cross(e_z,ball.w)
	if (mag(ball.u)<1e-6):
		ball.state = "ROLLING"
	else:
		ball.state = "SLIDING"
	return ball

def VERTICAL_RAIL_COLLISION(ball): #FastFiz equations # change?
	ball.v.x = -0.6*ball.v.x
	ball.v.y = 0.9*ball.v.y
	ball.w = 0.1*ball.w
	ball.u = ball.v + RADIUS*cross(e_z,ball.w)
	if (mag(ball.u)<1e-6):
		ball.state = "ROLLING"
	else:
		ball.state = "SLIDING"
	return ball
def RAIL_COLLISION(ball, direction):
	if direction == "left":
		n = vector(1,0,0)
	elif direction == "right":
		n = vector(-1,0,0)
	elif direction == "up":
		n = vector(0,-1,0)
	elif direction == "down":
		n = vector(0,1,0)
	v_init = ball.v
	w_init = ball.w
	k = 1 + ELAST
	P = k*BALL_MASS*dot(vector(0,0,0) - v_init,n)
	Vc_init = v_init - vector(0,0,0) - (dot(v_init - vector(0,0,0), n))*n + cross(n,RADIUS*w_init + vector(0,0,0))
	ball.v = v_init + n*P/BALL_MASS - Vc_init/7
	ball.w = w_init + (5/(7*RADIUS))*cross(n,Vc_init/2)
	ball.v.z = v_init.z
	if (mag(ball.u)<1e-6):
		ball.state = "ROLLING"
	else:
		ball.state = "SLIDING"
	return ball

def BALLS_COLLISION(ball1, ball2):
	v1_init = ball1.v
	v2_init = ball2.v
	w1_init = ball1.w
	w2_init = ball2.w
	intersection = (ball1.P + ball2.P)/2
	n = ball1.P - intersection
	k = (1 + ELAST)/2
	P = k*BALL_MASS*dot(v2_init - v1_init,hat(n))
	Vc_init = v1_init - v2_init - (dot(v1_init - v2_init, hat(n)))*hat(n) + cross(hat(n),RADIUS*w1_init + RADIUS*w2_init)
	ball1.v = v1_init + hat(n)*P/BALL_MASS - Vc_init/7
	ball1.w = w1_init + (5/(7*RADIUS))*cross(hat(n),Vc_init/2)
	ball2.v = v2_init + (v1_init - ball1.v)
	ball2.w = w2_init - (w1_init - ball1.w)
	ball1.v.z = v1_init.z
	ball2.v.z = v2_init.z
	ball1.u = ball1.v + RADIUS*cross(e_z,ball1.w)
	ball2.u = ball2.v + RADIUS*cross(e_z,ball2.w)

	if (mag(ball1.u)<1e-6):
		ball1.state = "ROLLING"
	else:
		ball1.state = "SLIDING"
	if (mag(ball2.u)<1e-6):
		ball2.state = "ROLLING"
	else:
		ball2.state = "SLIDING"
	return ball1, ball2
""" 	temp1 = ball1.v.x
	temp2 = ball2.v.x
	temp3 = ball1.v.y
	temp4 = ball2.v.y
	ball1.v.x = temp2
	ball1.v.y = temp4
	ball2.v.x = temp1
	ball2.v.y = temp3

	temp1 = ball1.w.x
	temp2 = ball2.w.x
	temp3 = ball1.w.y
	temp4 = ball2.w.y
	ball1.w.x = temp2
	ball1.w.y = temp4
	ball2.w.x = temp1
	ball2.w.y = temp3

	ball1.w.z = 0.1*ball1.w.z
	ball2.w.z = 0.1*ball2.w.z """

''' 	print(ball1.v.x)
	ball1.u = ball1.v + RADIUS*cross(e_z,ball1.w)
	ball2.u = ball2.v + RADIUS*cross(e_z,ball2.w)

	if (mag(ball1.u)<1e-6):
    		ball1.state = "ROLLING"
	else:
		ball1.state = "SLIDING"
	if (mag(ball2.u)<1e-6):
    		ball2.state = "ROLLING"
	else:
		ball2.state = "SLIDING"
	return ball1, ball2 '''

""" 	sleep(1)
	ball1.u = ball1.v - ball2.v - cross(RADIUS*e_x, (ball1.w +ball2.w))
	ball2.u = ball2.v - ball2.v - cross(RADIUS*e_x, (ball1.w +ball2.w))
	temp1 = ball1.v.x
	temp2 = ball2.v.x
	temp3 = ball1.v.y
	temp4 = ball2.v.y
	ball1.v.x = temp2
	ball2.v.x = temp1
	ball1.v.y = temp3 - MU_r*temp1*hat(ball1.u).y          #ATTENTION PAS MU_R -> MUc
	ball2.v.y = temp4 - MU_r*temp2*hat(ball1.u).y

	w_add = (-2.5*MU_r*temp1/(1.000575*RADIUS))*cross(e_x,hat(ball1.u))
	ball1.w = ball1.w - w_add
	ball2.w = ball2.w + w_add
	if (mag(ball1.u)<1e-6):
		ball1.state = "ROLLING"
	else:
		ball1.state = "SLIDING"
	if (mag(ball2.u)<1e-6):
    		ball2.state = "ROLLING"
	else:
		ball2.state = "SLIDING" """
