from carom import Carom
from Constants import*
import numpy as np
from vpython import sleep
actions = []
for a in np.arange(-0.5*RADIUS,0.5*RADIUS,0.01):
    for b in np.arange(-0.5*RADIUS,0.5*RADIUS,0.01):
        for theta in np.arange(0,50,5):
            for phi in np.arange(0,360,20):
                for V in np.arange(0.1,6,0.5):
                    actions.append((a,b,theta,phi,V))

tree_actions_index =  np.load("tree_actions_index.npy")

env = Carom(render = True)
env.reset()
sleep(2)
action_index = int(tree_actions_index[0,0][1])
env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
action_index = int(tree_actions_index[1,1][0])
env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
action_index = int(tree_actions_index[2,2][0])
env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])