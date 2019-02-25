
import numpy as np
import gym
from carom import Carom

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import *
from rl.random import OrnsteinUhlenbeckProcess


ENV_NAME = 'Carom-v0'
gym.undo_logger_setup()


# Get the environment and extract the number of actions.
env = Carom(render = False)
np.random.seed(324)
env.seed(324)
assert len(env.action_space.shape) == 1
nb_actions = env.action_space.shape[0]
print(env.action_space.shape)
# Next, we build a very simple model.
actor = Sequential()
actor.add(Flatten(input_shape=(1,) + env.observation_space.shape))
actor.add(Dense(100))
actor.add(Activation('relu'))
actor.add(Dense(200))
actor.add(Activation('relu'))
actor.add(Dense(300))
actor.add(Activation('relu'))
actor.add(Dense(nb_actions))
actor.add(Activation('linear'))
# print(actor.summary())

action_input = Input(shape=(nb_actions,), name='action_input')
observation_input = Input(shape=(1,) + env.observation_space.shape, name='observation_input')
print((1,) + env.observation_space.shape)
flattened_observation = Flatten()(observation_input)
x = Concatenate()([action_input, flattened_observation])
x = Dense(100)(x)
x = Activation('relu')(x)
x = Dense(200)(x)
x = Activation('relu')(x)
x = Dense(300)(x)
x = Activation('relu')(x)
x = Dense(1)(x)
x = Activation('linear')(x)
critic = Model(inputs=[action_input, observation_input], outputs=x)
# print(critic.summary())
# demo = np.load("demoTable.npy")
# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = SequentialMemory(limit=50000, window_length=1)
# for i in range(demo.shape[0]):
#     memory.append(observation = demo[i][0], action = demo[i][1], reward = demo[i][2], terminal= True)
agent = DDPGAgent(nb_actions=nb_actions, actor=actor, critic=critic, critic_action_input=action_input,
                  memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100, gamma=.99, target_model_update=1e-3)
agent.compile(Adam(lr=.001, clipnorm=1.), metrics=['mae'])
#agent.load_weights('ddpg_{}_2balls_final_weights_v4.h5f'.format(ENV_NAME))

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.,
agent.fit(env, nb_steps=300000, visualize=False, verbose=1, nb_max_episode_steps=1)

# After training is done, we save the final weights.
#agent.save_weights('ddpg_{}_1balls_5params_weights_v5.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
env.render = True
agent.test(env, nb_episodes=10, visualize=False, nb_max_episode_steps=200, modif = False)