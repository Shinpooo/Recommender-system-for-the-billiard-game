from carom import Carom
import numpy as np
env = Carom(render=True)
#for i in range(13):
#    state, reward, done, info = env.step(90)
#    print(state, reward, done)
print(env.action_space.sample())