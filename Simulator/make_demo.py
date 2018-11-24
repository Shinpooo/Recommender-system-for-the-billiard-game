import numpy as np
from carom import Carom
import gym

nb_rows = 1000
nb_good_steps = 0
env = Carom(render=False)
np.random.seed(321)
env.seed(321)
demo_table = np.zeros((nb_rows, 4), dtype=object)

while nb_good_steps < nb_rows:
    env.reset()
    state = np.array(env.state)
    action = env.action_space.sample()
    next_state, reward, done, info = env.step(action)
    if reward == 1:
        demo_table[nb_good_steps][0] = state
        demo_table[nb_good_steps][1] = action
        demo_table[nb_good_steps][2] = reward
        demo_table[nb_good_steps][3] = next_state
        nb_good_steps += 1
        print("demo: %d/%d"%(nb_good_steps, nb_rows))

np.save("demoTable", demo_table)