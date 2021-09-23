
from Simulator.carom import Carom
from Agents.dqn import DqnController



ENV_NAME = 'Carom-v0'


# Get the environment and extract the number of actions.

if  __name__ == "__main__":
    train_env = Carom(render = True)
    #Reinforcement learning control
    c1 = DqnController(train_env)
    c1.train()
    # c1.save()
    # c1.load()
    # c1.set_env(test_env)
    c1.simulate()
