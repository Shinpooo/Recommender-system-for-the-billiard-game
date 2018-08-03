import numpy as np
from scipy import sparse
from carom import Carom
from Constants import RADIUS

def choose_action(Q, currentState):
    action_index = Q[currentState].argmax()
    return action_index


#actions =[(0,0,0,20,4),(0,0,0,130,3),(0,0,0,1,8)]
Q =  np.load("Qmatrix.npy")
print(sparse.csr_matrix(Q))
print(len(Q))
env = Carom(render = True)
actions = env.get_actions()

state = 0
for i in range(len(Q)-1):
    action_index = choose_action(Q, state)
    env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
    state = state + 1
    

