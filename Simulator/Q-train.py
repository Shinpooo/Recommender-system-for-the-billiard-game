from carom import Carom
import random
from Parameters import RADIUS
import numpy as np
from scipy import sparse

def choose_action(Q, currentState, actions):
    if (np.count_nonzero(Q[currentState]) == 0 or np.random.rand(1) < e) :
        action_index = int(np.random.choice(len(Q[0,:]),1))
    else:
        action_index = Q[currentState].argmax()
    return action_index

goal_points = 5
total_points = 0
num_episodes = 1500
lr = .8
y = .95
e = 0.2
env = Carom(render = False)
actions = env.get_actions()

#actions =[(0,0,0,20,4),(0,0,0,130,3),(0,0,0,1,8)]
Q = np.zeros((1, len(actions)))
env.reset()
#env.step(0,0,0,90,5) #a, b, thetha, phi, Vb
for i in range(num_episodes):
#while total_points < goal_points:
    env.reset()
    state = 0
    j = 0
    episode_reward = 0
    while j < 1:
        #print(sparse.csr_matrix(Q))
        action_index = choose_action(Q, state, actions)
        #action_index = int(np.random.choice(len(Q[0,:]),1))
        nextState, reward, done, add_new_state = env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
        episode_reward += reward
        #state, reward, done, add_new_state = env.step(random.uniform(-0.5, 0.5)*RADIUS,random.uniform(-0.5, 0.5)*RADIUS,random.uniform(0, 50),random.uniform(0, 360),random.uniform(0.5, 6))
        #print(action_index)
        if done:
            break
        else:
            #print(state, nextState)
            if add_new_state:
                total_points += 1
                newState = np.zeros((1,len(actions)))
                Q = np.concatenate((Q,newState))
            #Q[state,action_index] = Q[state,action_index]
            Q[state,action_index] = Q[state,action_index] + lr*(reward + y*np.max(Q[nextState,:]) - Q[state,action_index])
            state = nextState
            #print(sparse.csr_matrix(Q))
            #print(Q)
    print("Episode %d : Total reward: %.3f"%(i+1, episode_reward))
np.save("Qmatrix", Q)
print("Fin")