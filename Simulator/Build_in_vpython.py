from Parameters import*
import math
from Event_manager import*


def BUILD_TABLE():
	surface = box(canvas=scene, pos=vector(0,0,- RADIUS - SURFACE_THICKNESS/2), size=vector(SURFACE_LENGTH,SURFACE_WIDTH, SURFACE_THICKNESS), color= green)
	Low_side = box(canvas=scene, pos=vector(0,-SURFACE_WIDTH/2 - SIDE_LENGTH/2,-RADIUS), size=vector(SURFACE_LENGTH + 2*SIDE_LENGTH, SIDE_LENGTH, 2*HEIGHT_RAILS), color = brown)
	Up_side = box(canvas=scene, pos=vector(0,SURFACE_WIDTH/2 + SIDE_LENGTH/2,-RADIUS), size=vector(SURFACE_LENGTH + 2*SIDE_LENGTH, SIDE_LENGTH,2*HEIGHT_RAILS), color = brown)
	R_side = box(canvas=scene, pos=vector(SURFACE_LENGTH/2 + SIDE_LENGTH/2,0,-RADIUS), size=vector(SIDE_LENGTH, SURFACE_WIDTH,2*HEIGHT_RAILS), color = brown)
	L_side = box(canvas=scene, pos=vector(-SURFACE_LENGTH/2 - SIDE_LENGTH/2,0,-RADIUS), size=vector(SIDE_LENGTH, SURFACE_WIDTH,2*HEIGHT_RAILS), color = brown)

def BUILD_BALLS_INITIAL_STATE():
	white_ball = sphere(canvas=scene, pos=P0_WHITE, radius=RADIUS, color=color.white, make_trail = True)
	yellow_ball = sphere(canvas=scene, pos=P0_YELLOW, radius=RADIUS, color=color.yellow, make_trail = True)
	red_ball = sphere(canvas=scene, pos=P0_RED, radius=RADIUS, color=color.red, make_trail = True)
	return white_ball, yellow_ball, red_ball

def FIND_DELTAT_NBSTEPS(time_start,time_end, print_ = False):
	nb_time_steps = math.ceil((time_end - time_start)/0.01)
	deltat = (time_end - time_start)/nb_time_steps
	if print_:
		print("Deltat : %f, nbtimestep :%d, ts + product:%f, time_end: %f" 
			%(deltat,nb_time_steps, time_start + nb_time_steps*deltat,time_end))
	return deltat, nb_time_steps

def GET_VALUE_AT_START(ball):
	ball_init = [ball.P, ball.v, ball.w, ball.u]
	return ball_init

def SLIDING(ball,time_start,time_end):
	deltat, nb_time_steps = FIND_DELTAT_NBSTEPS(time_start, time_end)
	ball_init = GET_VALUE_AT_START(ball)
	print("At %.2f sec: pos = (%.2f,%.2f,%.2f), v = (%.2f,%.2f,%.2f), w = (%.2f,%.2f,%.2f), u = (%.2f,%.2f,%.2f), |v| = %.2f, |w| = %.2f"
		%(time_start,ball_init[0].x,ball_init[0].y,ball_init[0].z,ball_init[1].x,ball_init[1].y,ball_init[1].z,ball_init[2].x,ball_init[2].y,ball_init[2].z,ball_init[3].x,ball_init[3].y,ball_init[3].z,mag(ball_init[1]),mag(ball_init[2])))
	for i in range(nb_time_steps + 1):
		rate(100)
		t = i*deltat + time_start
		ball.pos = ball_init[0] + ball_init[1]*(t - time_start) - 0.5*MU_s*g*((t - time_start)**2)*hat(ball_init[3])

	ball.P = ball_init[0] + ball_init[1]*(t - time_start) - 0.5*MU_s*g*((t - time_start)**2)*hat(ball_init[3])
	ball.v = ball_init[1] - MU_s*g*(t - time_start)*hat(ball_init[3])
	ball.w = ball_init[2] + 2.5*MU_s*g*(t - time_start)*cross(e_z,hat(ball_init[3]))/RADIUS # Has to be verified (- or + before 2.5 depending on papers)
	if(ball.spin):
		ball.w.z = ball_init[2].z - np.sign(ball_init[2].z)*2.5*MU_sp*g*(t - time_start)/RADIUS # Has no efffect (but still to be verified)
	ball.u = ball.v + RADIUS*cross(e_z, ball.w) #  OR THIS: ball.u = ball_init[3] - 3.5*MU_s*g*t*hat(ball_init[3])
	print("At %.2f sec: pos = (%.2f,%.2f,%.2f), v = (%.2f,%.2f,%.2f), w = (%.2f,%.2f,%.2f), u = (%.2f,%.2f,%.2f),|v| = %.2f, |w| = %.2f"
		%(t,ball.P.x,ball.P.y,ball.P.z,ball.v.x,ball.v.y,ball.v.z,ball.w.x,ball.w.y,ball.w.z,ball.u.x,ball.u.y,ball.u.z,mag(ball.v),mag(ball.w)))
	return ball

def ROLLING(ball, time_start, time_end):
	deltat, nb_time_steps = FIND_DELTAT_NBSTEPS(time_start, time_end)
	ball_init = GET_VALUE_AT_START(ball)
	print("At %.2f sec: pos = (%.2f,%.2f,%.2f), v = (%.2f,%.2f,%.2f), w = (%.2f,%.2f,%.2f), u = (%.2f,%.2f,%.2f), |v| = %.2f, |w| = %.2f"
		%(time_start,ball_init[0].x,ball_init[0].y,ball_init[0].z,ball_init[1].x,ball_init[1].y,ball_init[1].z,ball_init[2].x,ball_init[2].y,ball_init[2].z,ball_init[3].x,ball_init[3].y,ball_init[3].z,mag(ball_init[1]),mag(ball_init[2])))
	for i in range(nb_time_steps + 1):
		rate(100)
		t = i*deltat + time_start
		ball.pos = ball_init[0] + ball_init[1]*(t -	 time_start) - (5/14)*MU_r*g*((t - time_start)**2)*hat(ball_init[1])

	ball.P = ball_init[0] + ball_init[1]*(t - time_start) - (5/14)*MU_r*g*((t - time_start)**2)*hat(ball_init[1])
	ball.v = ball_init[1] - (5/7)*MU_r*g*(t - time_start)*hat(ball_init[1])
	ball.w = cross(hat(e_z),ball.v)/RADIUS
	if(ball.spin):
		ball.w.z = ball_init[2].z - np.sign(ball_init[2].z)*2.5*MU_sp*g*(t - time_start)/RADIUS # Has no efffect (but still to be verified)
	ball.u = ball.v + RADIUS*cross(e_z, ball.w) # u remains equal to 0 during rolling
	print("At %.2f sec: pos = (%.2f,%.2f,%.2f), v = (%.2f,%.2f,%.2f), w = (%.2f,%.2f,%.2f), u = (%.2f,%.2f,%.2f),|v| = %.2f, |w| = %.2f"
		%(t,ball.P.x,ball.P.y,ball.P.z,ball.v.x,ball.v.y,ball.v.z,ball.w.x,ball.w.y,ball.w.z,ball.u.x,ball.u.y,ball.u.z,mag(ball.v),mag(ball.w)))
	return ball

def SLIDING_OR_ROLLING(balls, time_start, time_end):
	#INITIAL STATE
	deltat, nb_time_steps = FIND_DELTAT_NBSTEPS(time_start, time_end)
	ball_init_white = GET_VALUE_AT_START(balls[0])
	ball_init_yellow = GET_VALUE_AT_START(balls[1])
	ball_init_red = GET_VALUE_AT_START(balls[2])
	balls[0].init = ball_init_white
	balls[1].init = ball_init_yellow
	balls[2].init = ball_init_red
	#RENDERING PART 
	if render:
		for i in range(nb_time_steps + 1):
			rate(100)
			t = i*deltat + time_start
			for ball in balls:
				if(ball.state == "SLIDING"):
					ball.pos = ball.init[0] + ball.init[1]*(t - time_start) - 0.5*MU_s*g*((t - time_start)**2)*hat(ball.init[3])
					#ball.v = ball.init[1] - MU_s*g*(t - time_start)*hat(ball.init[3])
					#print(mag(ball.v))
				elif(ball.state == "ROLLING"):
					ball.pos = ball.init[0] + ball.init[1]*(t -	 time_start) - (5/14)*MU_r*g*((t - time_start)**2)*hat(ball.init[1])
					#ball.v = ball.init[1] - (5/7)*MU_r*g*(t - time_start)*hat(ball.init[1])
					#print(mag(ball.v))
	#FINAL STATE
	else:
		t = nb_time_steps*deltat + time_start
	for ball in balls:
		if(ball.state == "SLIDING"):
			ball.P = ball.init[0] + ball.init[1]*(t - time_start) - 0.5*MU_s*g*((t - time_start)**2)*hat(ball.init[3])
			ball.v = ball.init[1] - MU_s*g*(t - time_start)*hat(ball.init[3])
			ball.w = ball.init[2] + 2.5*MU_s*g*(t - time_start)*cross(e_z,hat(ball.init[3]))/RADIUS # Has to be verified (- or + before 2.5 depending on papers)
			if(ball.spin):
				ball.w.z = ball.init[2].z - np.sign(ball.init[2].z)*2.5*MU_sp*g*(t - time_start)/RADIUS # Has no efffect (but still to be verified)
			ball.u = ball.v + RADIUS*cross(e_z, ball.w) #  OR THIS: ball.u = ball_init[3] - 3.5*MU_s*g*t*hat(ball_init[3])
		elif(ball.state == "ROLLING"):
			ball.P = ball.init[0] + ball.init[1]*(t - time_start) - (5/14)*MU_r*g*((t - time_start)**2)*hat(ball.init[1])
			ball.v = ball.init[1] - (5/7)*MU_r*g*(t - time_start)*hat(ball.init[1])
			ball.w = cross(hat(e_z),ball.v)/RADIUS
			if(ball.spin):
				ball.w.z = ball.init[2].z - np.sign(ball.init[2].z)*2.5*MU_sp*g*(t - time_start)/RADIUS # Has no efffect (but still to be verified)
			ball.u = ball.v + RADIUS*cross(e_z, ball.w) # u remains equal to 0 during rolling
	return balls
			


def MOVE_BALLS(balls, time):
	if(balls[0].state == "STATIONNARY" and balls[1].state == "STATIONNARY" and balls[2].state == "STATIONNARY"):
		scene.caption =  "<b>LINEAR SPEED</b> [m/s]\nWHITE: %.3f \nYELLOW: %.3f\nRED: %.3f "%(mag(balls[0].v),mag(balls[1].v),mag(balls[2].v))
		scene.append_to_caption("\n\n<b>ROTATIONAL SPEED</b> [deg/s]\nWHITE: (%.3f,%.3f,%.3f) - Norm: %.3f\nYELLOW: (%.3f,%.3f,%.3f) - Norm: %.3f\nRED: (%.3f,%.3f,%.3f) - Norm: %.3f"%(balls[0].w.x,balls[0].w.y,balls[0].w.z,mag(balls[0].w),balls[1].w.x,balls[1].w.y,balls[1].w.z,mag(balls[1].w),balls[2].w.x,balls[2].w.y,balls[2].w.z,mag(balls[2].w)))
		scene.append_to_caption("\n\n<b>NEXT EVENT</b>: None")
	else:
		scene.caption =  "<b>LINEAR SPEED</b> [m/s]\nWHITE: %.3f \nYELLOW: %.3f\nRED: %.3f "%(mag(balls[0].v),mag(balls[1].v),mag(balls[2].v))
		scene.append_to_caption("\n\n<b>ROTATIONAL SPEED</b> [deg/s]\nWHITE: (%.3f,%.3f,%.3f) - Norm: %.3f\nYELLOW: (%.3f,%.3f,%.3f) - Norm: %.3f\nRED: (%.3f,%.3f,%.3f) - Norm: %.3f"%(balls[0].w.x,balls[0].w.y,balls[0].w.z,mag(balls[0].w),balls[1].w.x,balls[1].w.y,balls[1].w.z,mag(balls[1].w),balls[2].w.x,balls[2].w.y,balls[2].w.z,mag(balls[2].w)))
		event,time_next_ev = NEXT_EVENT_BALLS(balls, time)
		scene.append_to_caption("\n\n<b>NEXT EVENT</b>: " + event)
		#sleep(2)
		balls = SLIDING_OR_ROLLING(balls,time,time_next_ev)
		balls = EVENT_PROCESSING_BALLS(balls, event)

		MOVE_BALLS(balls, time_next_ev)


def MOVE(ball, time):
	if ball.state == "SLIDING":
		event,time_next_ev = NEXT_EVENT(ball, time)
		#print("x = %.6f and y = %.6f"%(ball.P.x,ball.P.y))
		#sleep(1)
		ball = SLIDING(ball,time,time_next_ev)
		ball = EVENT_PROCESSING(ball, event)
		MOVE(ball, time_next_ev)
	elif ball.state == "ROLLING":
		event,time_next_ev = NEXT_EVENT(ball, time)
		#print("x = %.6f and y = %.6f"%(ball.P.x,ball.P.y))
		sleep(1)
		ball = ROLLING(ball, time, time_next_ev)
		ball = EVENT_PROCESSING(ball, event)
		MOVE(ball, time_next_ev)
	elif ball.state == "STATIONNARY":
		print("STATIO")
		return 0
