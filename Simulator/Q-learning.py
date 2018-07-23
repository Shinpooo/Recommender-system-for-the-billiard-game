from carom import Carom
import random
from Parameters import RADIUS
import numpy as np
from scipy import sparse

def choose_action(Q, currentState, actions):
    if np.count_nonzero(Q[currentState]) == 0:
        action_index = int(np.random.choice(len(Q[0,:]),1))
    else:
        action_index = Q[currentState].argmax()
    return action_index


num_episodes = 500
lr = .8
y = .95
env = Carom(render = False)
actions = []
for a in np.arange(-0.5*RADIUS,0.5*RADIUS,0.01):
    for b in np.arange(-0.5*RADIUS,0.5*RADIUS,0.01):
        for theta in np.arange(0,50,5):
            for phi in np.arange(0,360,20):
                for V in np.arange(0.1,6,0.5):
                    actions.append((a,b,theta,phi,V))
#actions =[(0,0,0,20,4),(0,0,0,130,3),(0,0,0,1,8)]
Q = np.zeros((1, len(actions)))
env.reset()
#env.step(0,0,0,90,5) #a, b, thetha, phi, Vb
for i in range(num_episodes):
    env.reset()
    state = 0
    j = 0
    while j < 1:
        print(sparse.csr_matrix(Q))
        action_index = choose_action(Q, state, actions)
        #action_index = int(np.random.choice(len(Q[0,:]),1))
        nextState, reward, done, add_new_state = env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
        #state, reward, done, add_new_state = env.step(random.uniform(-0.5, 0.5)*RADIUS,random.uniform(-0.5, 0.5)*RADIUS,random.uniform(0, 50),random.uniform(0, 360),random.uniform(0.5, 6))
        if done:
            break
        else:
            #print(state, nextState)
            if add_new_state:
                print("mnt!")
                newState = np.zeros((1,len(actions)))
                Q = np.concatenate((Q,newState))
            #Q[state,action_index] = Q[state,action_index]
            Q[state,action_index] = Q[state,action_index] + lr*(reward + y*np.max(Q[nextState,:]) - Q[state,action_index])
            state = nextState
            #print(sparse.csr_matrix(Q))
            #print(Q)
            
print("Fin")