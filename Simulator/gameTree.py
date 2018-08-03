from carom import Carom
import random
from Parameters import RADIUS
import numpy as np
from scipy import sparse
from Constants import*
from vpython import*
import math
import sys
sys.setrecursionlimit(1000)


nb_branches = 2
goal_points = 7
total_points = 0
sum_goal_points = 0
pos_white = P0_WHITE
pos_yellow = P0_YELLOW
pos_red = P0_RED
myList = []
letters = ['a','b','c','d','e','f','g','x','y','z']
for i in range(goal_points):
    sum_goal_points += nb_branches**(i+1)

for i in range(nb_branches):
    myList.append((letters[i],np.float32))
#num_episodes = 2000
#lr = .8
#y = .95
env = Carom(render = False)
#tree_states_index = np.zeros((goal_points,nb_branches**(goal_points-1)))
tree_actions_index = np.zeros((goal_points,nb_branches**(goal_points-1)),dtype= myList)

#print(tree_states_index)
actions = env.get_actions()


states_list = [(pos_white.x,pos_white.y,pos_yellow.x,pos_yellow.y,pos_red.x,pos_red.y)]
#actions =[(0,0,0,20,4),(0,0,0,130,3),(0,0,0,1,8)]
#Q = np.zeros((1, len(actions)))
env.reset()
#env.step(0,0,0,90,5) #a, b, thetha, phi, Vb
#for i in range(num_episodes):
level = 0
state_index = -1
while total_points < sum_goal_points:
    level += 1
    for i in range(nb_branches**level):
        if (i % nb_branches == 0 or i == 0):
            state_index+=1
            pos_white = vector(states_list[state_index][0], states_list[state_index][1], 0)
            pos_yellow = vector(states_list[state_index][2], states_list[state_index][3], 0)
            pos_red = vector(states_list[state_index][4], states_list[state_index][5], 0)
        j = 0
        a = i%nb_branches
        while j < 1:
            env.reset(pos_white,pos_yellow,pos_red)
            #print(sparse.csr_matrix(Q))
            #action_index = choose_action(Q, state, actions)
            action_index = int(np.random.choice(len(actions)))
            observation, reward, done, add_new_state = env.step2(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
            #state, reward, done, add_new_state = env.step(random.uniform(-0.5, 0.5)*RADIUS,random.uniform(-0.5, 0.5)*RADIUS,random.uniform(0, 50),random.uniform(0, 360),random.uniform(0.5, 6))
            #print(action_index)
            if (done == False and level <= goal_points):
                total_points += 1
                print("%d/%d points"%(total_points,sum_goal_points))
                states_list.append(observation)
                tree_actions_index[level-1,math.floor(i/nb_branches)][a] = action_index
                break

np.save("tree_actions_index", tree_actions_index)            
print("Fin")