from carom import Carom
from Constants import*
import numpy as np
from vpython import sleep

def choose_branch(Q, state):
    chosen_branch = Q[state].argmax()
    return chosen_branch

tree_actions_index =  np.load("tree_actions_index.npy")
Q =  np.load("treeQmatrix.npy")

env = Carom(render = True)
env.reset()
actions = env.get_actions()
nb_states = 0
index2 = 0
state = 0
episode_reward = 0
nb_branches = len(tree_actions_index[0,0])

for i in range(tree_actions_index.shape[0]):
    nb_states += nb_branches**i

for level in range(tree_actions_index.shape[0]):
    chosen_branch = choose_branch(Q, state)
    action_index = int(tree_actions_index[level,index2][chosen_branch])
    reward, coll_r = env.step3(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
    episode_reward += reward
    index2 = index2*nb_branches + chosen_branch
    nextState = state*nb_branches + chosen_branch + 1
    state = nextState

print("Total reward: %.3f"%(episode_reward))