
import pygame
import sys
from math import *
import random
import numpy as np
import time
from scipy import sparse
class Ball:
	def __init__(self, x, y,speed, color, angle):
		self.x = x 
		self.y = y 
		self.color = color
		self.angle = angle
		self.speed = speed

	def draw(self):
		pygame.draw.ellipse(display, self.color, (self.x - radius, self.y - radius, radius*2, radius*2))


	def move(self):
		self.speed -= friction
		if self.speed <= 0:
			self.speed = 0

		self.x = self.x + self.speed*cos(radians(self.angle))
		self.y = self.y + self.speed*sin(radians(self.angle))

		if (self.x >= width + margin - radius):
			self.x = width + margin - radius
			self.angle = 180 - self.angle
		if (radius + margin >= self.x):
			self.x = radius + margin
			self.angle = 180 - self.angle
		if (self.y >= height + margin - radius):
			self.y = height + margin - radius
			self.angle = 360 - self.angle
		if (radius + margin >= self.y):
			self.y = radius + margin
			self.angle = 360 - self.angle

 
#Detection de collision
def collision(ball1, ball2):
	dist = ((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)**0.5
	if dist < radius*2:
		return True
	else:
		return False

# Physique simplifiée pour des premiers résultats (à améliorer)
def checkCollision(balls):
    for i in range(len(balls)):
        for j in range(len(balls) - 1, i, -1):
            if collision(balls[i], balls[j]):
            	if balls[i].x == balls[j].x: #A changer
            		angleIncl = 180
            	else:
	                u1 = balls[i].speed
	                u2 = balls[j].speed
	                

	                balls[i].speed = ((u1*cos(radians(balls[i].angle)))**2 + (u2*sin(radians(balls[j].angle)))**2)**0.5
	                balls[j].speed = ((u2*cos(radians(balls[j].angle)))**2 + (u1*sin(radians(balls[i].angle)))**2)**0.5

	                tangent = degrees((atan((balls[i].y - balls[j].y)/(balls[i].x - balls[j].x)))) + 90
	                angle = tangent + 90
	                    
	                balls[i].angle = (2*tangent - balls[i].angle)
	                balls[j].angle = (2*tangent - balls[j].angle)

	                balls[i].x += (balls[i].speed)*sin(radians(angle))
	                balls[i].y -= (balls[i].speed)*cos(radians(angle))
	                balls[j].x -= (balls[j].speed)*sin(radians(angle))
	                balls[j].y += (balls[j].speed)*cos(radians(angle))

def border():
    pygame.draw.rect(display, green, (0, 0, width + 2*margin, margin))
    pygame.draw.rect(display, green, (0, 0, margin, height + 2*margin))
    pygame.draw.rect(display, green, (width + margin, 0, margin, height + 2*margin))
    pygame.draw.rect(display, green, (0, height + margin, width + 2*margin, margin))

def close():
	pygame.quit()
	sys.exit()

def draw_line(screen,X ,Y, color, angle, width):
	length = 300
	# if (angle>90 and angle<180):
	# 	X_final = -length*np.cos(radians(angle)) + X
	# else:
	# 	X_final = length*np.cos(radians(angle)) + X
	X_final = length*np.cos(radians(angle)) + X
	Y_final = length*np.sin(radians(angle)) + Y
	pygame.draw.line(screen, color, [X,Y], [X_final, Y_final], width)

# RL
def build_q_table(actions):
    table = np.zeros((1, len(actions)))
    return table
def update_qtable(qmatrix, action_index, R, currentState, nextState):
	q_predicted = qmatrix[currentState	,action_index]
	q_target = R + GAMMA*np.amax(qmatrix[nextState,:])
	qmatrix[currentState,action_index] += ALPHA * (q_target - q_predicted)
	return qmatrix
	
# Comments for epsilon varying over time and reward = -1 for bad moves 
def choose_action(qmatrix, currentState, angle_red,angle_yellow, opening_angle, actions):
	# EPSILON = (time.time() - start_time)/120
	# print(EPSILON)
	lb_red = angle_red - opening_angle/2
	ub_red = angle_red + opening_angle/2
	lb_yellow = angle_yellow - opening_angle/2
	ub_yellow = angle_yellow + opening_angle/2

	index_angle = []
	if (np.random.uniform() > EPSILON) or (np.count_nonzero(qmatrix[currentState]) == 0):
		print("random")
		for i in range(len(actions)):
			if(lb_red<0):
				if (actions[i][1] < ub_red or actions[i][1] > lb_red+360):
					index_angle.append(i)

			elif(ub_red>360):
				if (actions[i][1] > lb_red or actions[i][1] < ub_red-360):
					index_angle.append(i)

			else:
				if (actions[i][1] >= lb_red and actions[i][1] < ub_red):
					index_angle.append(i)

			if(lb_yellow<0):
				if (actions[i][1] < ub_yellow or actions[i][1] > lb_yellow+360):
					index_angle.append(i)

			elif(ub_yellow>360):
				if (actions[i][1] > lb_yellow or actions[i][1] < ub_yellow-360):
					index_angle.append(i)

			else:
				if (actions[i][1] >= lb_yellow and actions[i][1] < ub_yellow):
					index_angle.append(i)

			# if (actions[i][1] >= lb_red or actions[i][1] >= lb_red+360):
			# 	if(actions[i][1] <= ub_red or actions[i][1] <= ub_red-360):
			# 		index_angle.append(i)
			# elif(actions[i][1] >= lb_yellow):
			# 	if(actions[i][1] <= ub_yellow or actions[i][1] <= ub_yellow-360):
			# 		index_angle.append(i)
		# action_index = int(np.random.choice(len(qmatrix[0,:]),1))  => FULL RANDOM
		# if qmatrix[nextState, action_index] == -1: => FOR REWARD = -1 (TO BE MODIFIED...)
		# 	print("denied action")
		# 	action_index = choose_action(qmatrix, nextState)
		print("red: [%d,%d] - yellow: [%d,%d]"%(lb_red,ub_red,lb_yellow,ub_yellow))
		action_index = np.random.choice(index_angle)
		print("chosen angle:%d"%actions[action_index][1])
	else:
		action_index = qmatrix[currentState].argmax()
	return action_index

def poolTable(qmatrix, actions, State, State_index, Sindex, ball_pos, episode, points):
	loop = True
	# yellowb_pos = (0.3*(width + 2*margin) - radius, 0.5*(height + 2*margin) - radius)	
	# whiteb_pos = (np.random.choice(index_angle)0.3*(width + 2*margin) - radius, 0.65*(height + 2*margin) - radius)	
	# redb_pos = (0.8*(width + 2*margin) - radius, 0.5*(height + 2*margin) - radius)
	# init_ball_pos = [yellowb_pos, whiteb_pos, redb_pos] 

	yellowb_pos = (0.3*(width + 2*margin), 0.5*(height + 2*margin))	
	whiteb_pos = (0.3*(width + 2*margin), 0.65*(height + 2*margin))	
	redb_pos = (0.8*(width + 2*margin), 0.5*(height + 2*margin))
	init_ball_pos = [yellowb_pos, whiteb_pos, redb_pos] 
	# Keep initial positions for the next episodes
	opening_angle = 20
	if (ball_pos[2][0]>= ball_pos[1][0] and ball_pos[2][1]>= ball_pos[1][1]):
		angle_red = degrees(np.arcsin((ball_pos[2][1]-ball_pos[1][1])/sqrt((ball_pos[2][0]-ball_pos[1][0])**2+(ball_pos[2][1]-ball_pos[1][1])**2)))
		print("Anglered = %f" %angle_red)
	elif (ball_pos[2][0]>= ball_pos[1][0] and ball_pos[2][1]<= ball_pos[1][1]):
		angle_red = degrees(2*pi+np.arcsin((ball_pos[2][1]-ball_pos[1][1])/sqrt((ball_pos[2][0]-ball_pos[1][0])**2+(ball_pos[2][1]-ball_pos[1][1])**2)))
		print("Anglered = %f" %angle_red)
	else:
		angle_red = degrees(pi-np.arcsin((ball_pos[2][1]-ball_pos[1][1])/sqrt((ball_pos[2][0]-ball_pos[1][0])**2+(ball_pos[2][1]-ball_pos[1][1])**2)))
		print("Anglered = %f" %angle_red)

	if (ball_pos[0][0]>= ball_pos[1][0] and ball_pos[0][1]>= ball_pos[1][1]):
		angle_yellow = degrees(np.arcsin((ball_pos[0][1]-ball_pos[1][1])/sqrt((ball_pos[0][0]-ball_pos[1][0])**2+(ball_pos[0][1]-ball_pos[1][1])**2)))
		print("Anglered = %f" %angle_yellow)
	elif (ball_pos[0][0]>= ball_pos[1][0] and ball_pos[0][1]<= ball_pos[1][1]):
		angle_yellow = degrees(2*pi+np.arcsin((ball_pos[0][1]-ball_pos[1][1])/sqrt((ball_pos[0][0]-ball_pos[1][0])**2+(ball_pos[0][1]-ball_pos[1][1])**2)))
		print("Angleyel = %f" %angle_yellow)
	else:
		angle_yellow = degrees(pi-np.arcsin((ball_pos[0][1]-ball_pos[1][1])/sqrt((ball_pos[0][0]-ball_pos[1][0])**2+(ball_pos[0][1]-ball_pos[1][1])**2)))
		print("Angleyel = %f" %angle_yellow)




	noBalls = 3
	balls = []

	# for i in range(noBalls):
	# 	newBall = Ball(random.randrange(0, width - 2*radius), random.randrange(0, height - 2*radius), 10, white, random.randrange(-180, 180))
	# 	balls.append(newBall)
	action_index = choose_action(qmatrix, State, angle_red, angle_yellow, opening_angle, actions)
	# action_index = 677

	white_speed = actions[action_index][0]
	white_angle = actions[action_index][1]

	yellowb = Ball(ball_pos[0][0], ball_pos[0][1], 0, yellow, 0)	
	whiteb = Ball(ball_pos[1][0], ball_pos[1][1], white_speed, white, white_angle)	
	redb = Ball(ball_pos[2][0], ball_pos[2][1], 0, red, 0)	
	print("State: %d - action: %d"%(State,action_index))
	balls.append(yellowb)
	balls.append(whiteb)
	balls.append(redb)

	collWY = False
	collWR = False	

	nb_first_ep = 3
	nb_fast_ep = 100

	if (nb_first_ep < episode < nb_fast_ep):
		pygame.display.set_caption("Episode %d - Fast learning simulation until episode %d to see improvements" % (episode, nb_fast_ep))
	else: 
		pygame.display.set_caption("Episode %d - Points marqués: %d" % (episode,points))
	while loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				close()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q: # => IN qwerty so press A to quit
					close()		
				if event.key == pygame.K_r:
					poolTable(qmatrix, actions, 0, State, State_index, Sindex, ball_pos, episode, points)
		if (whiteb.speed == 0 and redb.speed == 0 and yellowb.speed == 0):
			R = 0
			nextState = 0
			if (collWR == True and  collWY == True):
				R = 1
				ball_pos = [(yellowb.x - radius,yellowb.y - radius),(whiteb.x - radius,whiteb.y - radius),(redb.x - radius,redb.y - radius)]
				if State_index[State,action_index] == 0:
					newState = np.zeros((1,len(actions)))
					qmatrix = np.concatenate((qmatrix,newState))
					State_index[State,action_index] = Sindex
					Sindex += 1
					nextState = int(State_index[State,action_index])
				else:
					nextState = int(State_index[State,action_index])
			print("Next State: %d" %nextState)
			if R == 1:
				points += 1
				qmatrix = update_qtable(qmatrix, action_index, R, State, nextState)
				# action_index = choose_action(qmatrix, nextState, angle_red, angle_yellow, opening_angle, actions)
				print(sparse.csr_matrix(qmatrix))
				poolTable(qmatrix,actions, nextState, State_index, Sindex, ball_pos, episode, points)
			else:
				points = 0
				# qmatrix[State, action_index] = -1
				# action_index = choose_action(qmatrix, nextState, angle_red, angle_yellow, opening_angle, actions)
				print(sparse.csr_matrix(qmatrix))
				episode += 1
				poolTable(qmatrix,actions, nextState, State_index, Sindex, init_ball_pos, episode, points)

		display.fill(background)
		for i in range(noBalls):
			balls[i].draw()

		for i in range(noBalls):
			balls[i].move()

		if (collision(whiteb, redb)):
			collWR = True
		if (collision(whiteb, yellowb)):
			collWY = True
		checkCollision(balls)	
		border()
		pygame.draw.line(display, red, list(ball_pos[1]),list(ball_pos[2]))
		pygame.draw.line(display, yellow, list(ball_pos[1]),list(ball_pos[0]))
		draw_line(display, ball_pos[1][0], ball_pos[1][1], red, angle_red + opening_angle/2,3)
		draw_line(display, ball_pos[1][0], ball_pos[1][1], red, angle_red - opening_angle/2,3)
		draw_line(display, ball_pos[1][0], ball_pos[1][1], yellow, angle_yellow + opening_angle/2,3)
		draw_line(display, ball_pos[1][0], ball_pos[1][1], yellow, angle_yellow - opening_angle/2,3)
		draw_line(display, ball_pos[1][0], ball_pos[1][1], white, actions[action_index][1],1)

		pygame.display.update()
		if (nb_first_ep < episode < nb_fast_ep):
			clock.tick(1000000) # Increase FPS to simulate faster
		else:
			clock.tick(60)
		
start_time = time.time()
pygame.init()
width = 284*2
height = 142*2
margin = 10

display = pygame.display.set_mode((width + 2*margin, height + 2*margin))
clock = pygame.time.Clock() 
background = (20, 140, 59) #green
white = (236, 240, 241)
yellow = (244, 208, 63)
red = (203, 67, 53)
green = (40, 180, 99)
EPSILON = 1  # greedy police > 1 - pourcentage de chance de choisir une action aléatoire 
ALPHA = 0.1     # learning rate
GAMMA = 0.9    # discount factor

radius = 10
friction = 0.01

actions = []
for i in range(1,11):
	for j in range(0,360,4):
		actions.append((i,j))
# actions = [(10,20),(5,25),(7,30)] good example to understand
episode = 1
qmatrix = build_q_table(actions)
action_index  = int(np.random.choice(len(qmatrix[0,:]),1))
print("Initial random first action: %d" %(action_index))
State = 0
State_index = np.zeros((1000,len(actions)))
Sindex = 1

# yellowb_pos = (0.3*(width + 2*margin) - radius, 0.5*(height + 2*margin) - radius)	
# whiteb_pos = (0.3*(width + 2*margin) - radius, 0.65*(height + 2*margin) - radius)	
# redb_pos = (0.8*(width + 2*margin) - radius, 0.5*(height + 2*margin) - radius)

yellowb_pos = (0.3*(width + 2*margin), 0.5*(height + 2*margin))	
whiteb_pos = (0.3*(width + 2*margin), 0.65*(height + 2*margin))	
redb_pos = (0.8*(width + 2*margin), 0.5*(height + 2*margin))

init_ball_pos = [yellowb_pos, whiteb_pos, redb_pos]

points = 0
poolTable(qmatrix, actions, State, State_index, Sindex, init_ball_pos, episode, points)