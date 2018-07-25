import numpy as np
from scipy import sparse
from carom import Carom
from Constants import RADIUS
def choose_action(Q, currentState):
    action_index = Q[currentState].argmax()
    return action_index

actions = []
for a in np.arange(-0.5*RADIUS,0.5*RADIUS,0.01):
    for b in np.arange(-0.5*RADIUS,0.5*RADIUS,0.01):
        for theta in np.arange(0,50,5):
            for phi in np.arange(0,360,20):
                for V in np.arange(0.1,6,0.5):
                    actions.append((a,b,theta,phi,V))
#actions =[(0,0,0,20,4),(0,0,0,130,3),(0,0,0,1,8)]
Q =  np.load("Qmatrix.npy")
print(sparse.csr_matrix(Q))
print(len(Q))
env = Carom(render = True)
state = 0
for i in range(len(Q)-1):
    action_index = choose_action(Q, state)
    env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
    state = state + 1
    

