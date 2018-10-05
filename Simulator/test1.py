from carom import Carom
#import random
#from Parameters import RADIUS
#import numpy as np
#from scipy import sparse
from Constants import*
from vpython import*


# pos_white = vector(-SURFACE_WIDTH/3,0,0)
# pos_yellow = vector(-SURFACE_WIDTH/4,- INIT_DIST/2,0)
# pos_red = vector(SURFACE_WIDTH/4 -0.2,-0.5,0)
# pos_white = vector(-SURFACE_WIDTH/2,0,0)
# pos_yellow = vector(-SURFACE_WIDTH/2 + 0.03,SURFACE_WIDTH/2 - 0.07,0)
# pos_red = vector(-SURFACE_WIDTH/2 - 0.4,SURFACE_WIDTH/2 - 0.07,0)
env = Carom(render = False)
#env.reset(pos_white, pos_yellow, pos_red)
sleep(2)    
a = -0.2*RADIUS
b = 0*RADIUS
theta = 5
phi = 85
V = 5
actions = env.get_fixed_actions()
nb_shots = 5
shots = []

for i in range(nb_shots):
    coll_reward = 0
    while coll_reward == 0:
        #env.reset(pos_white, pos_yellow, pos_red)
        env.reset()
        action_index = int(np.random.choice(len(actions)))
        action_reward, coll_reward = env.step3(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
        if coll_reward == 1:
            if action_index in shots:
                coll_reward = 0
    shots.append(action_index)

env.render = True
for i in range(nb_shots):
    #env.reset(pos_white, pos_yellow, pos_red)
    env.reset()
    env.step3(actions[shots[i]][0],actions[shots[i]][1],actions[shots[i]][2],actions[shots[i]][3],actions[shots[i]][4] - 1)
# env.reset(pos_white, pos_yellow, pos_red)

#index = 3237
#index2 = 1256
#env.step3(actions[index][0],actions[index][1],actions[index][2],actions[index][3],actions[index][4])
# print(actions[index][0],actions[index][1],actions[index][2],actions[index][3],actions[index][4])
# a = -0*RADIUS
# b = 0*RADIUS
# theta = 5
# phi = -91
# V = 4.6
# env.step3(a,b,theta,phi,V)
