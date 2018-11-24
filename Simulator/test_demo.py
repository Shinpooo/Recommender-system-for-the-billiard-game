import numpy as np
from carom import Carom
import gym
from vpython import *

nb_rows = 1000
nb_good_steps = 0
env = Carom(render=True)
np.random.seed(32)
env.seed(32)
demo_table = np.load('demoTable.npy')

for i in range(10):
    index = np.random.choice(1000)
    env.state = demo_table[index][0]
    pos_white = vector(env.state[0], env.state[1],0)
    pos_yellow = vector(env.state[2], env.state[3],0)
    pos_red = vector(env.state[4], env.state[5],0)
    env.non_random_reset(pos_white, pos_yellow, pos_red)
    action = demo_table[index][1]
    env.step(action)