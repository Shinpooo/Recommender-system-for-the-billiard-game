from carom import Carom
from Constants import*
import numpy as np
from vpython import sleep
from scipy import sparse
import matplotlib.pyplot as plt

def choose_branch(nb_branches, Q, state, e):
    if (np.count_nonzero(Q[state]) == 0 or np.random.rand(1) < e):
        chosen_branch = np.random.choice(nb_branches)
    else:
        chosen_branch = Q[state].argmax()
    return chosen_branch

tree_actions_index =  np.load("tree_actions_index.npy")

env = Carom(render = False)
actions = env.get_actions()

env.reset()
sleep(2)
nb_branches = len(tree_actions_index[0,0])
# action_index = int(tree_actions_index[0,0][2])
# env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
# action_index = int(tree_actions_index[1,2][2])
# env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
# action_index = int(tree_actions_index[2,8][1])
# env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
nb_states = 0
num_episodes = 700
lr = .8
y = .95
e = 0.2
episodes = []
episode_rewards = []
for i in range(tree_actions_index.shape[0]):
    nb_states += nb_branches**i

Q = np.zeros((nb_states,nb_branches))
for i in range(num_episodes):
    env.reset()
    index2 = 0
    state = 0
    episode_reward = 0
    for level in range(tree_actions_index.shape[0]):
        chosen_branch = choose_branch(nb_branches, Q, state, e)
        action_index = int(tree_actions_index[level,index2][chosen_branch])
        reward = env.step3(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
        episode_reward += reward
        index2 = index2*nb_branches + chosen_branch
        nextState = state*nb_branches + chosen_branch + 1
        if nextState > nb_states - 1:
            Q[state,chosen_branch] = Q[state,chosen_branch] + lr*(reward - Q[state,chosen_branch])
        else:
            Q[state,chosen_branch] = Q[state,chosen_branch] + lr*(reward + y*np.max(Q[nextState,:]) - Q[state,chosen_branch])
        #print(sparse.csr_matrix(Q))
        #print(Q)
        state = nextState
    print("Episode %d : Total reward: %.3f"%(i+1, episode_reward))
    episodes.append(i+1)
    episode_rewards.append(episode_reward)
        
np.save("treeQmatrix", Q)
plt.plot(episodes, episode_rewards)
plt.xlabel('Episodes')
plt.ylabel('Total Reward')
#plt.show()
print("Fin")