from vpython import*
from carom import Carom
from Constants import*
import numpy as np

def check_superposition(white_pos, yellow_pos, red_pos):
    #white yellow
    if sqrt((white_pos.x - yellow_pos.x)**2 + (white_pos.y - yellow_pos.y)**2) < 2*RADIUS:
        return True
    #white red
    elif sqrt((white_pos.x - red_pos.x)**2 + (white_pos.y - red_pos.y)**2) < 2*RADIUS:
        return True
    #yellow red
    elif sqrt((yellow_pos.x - red_pos.x)**2 + (yellow_pos.y - red_pos.y)**2) < 2*RADIUS:
        return True
    else:
        return False


env = Carom(render = False)
actions = env.get_actions()

X_train = []
Y_train = [] 
for w_white in np.linspace(SURFACE_WIDTH/2 - 2*RADIUS, -SURFACE_WIDTH/2 + 2*RADIUS, num=10):
    for l_white in np.linspace(-SURFACE_LENGTH/2 + 2*RADIUS, SURFACE_LENGTH/2 - 2*RADIUS, num=10):
        for w_yellow in np.linspace(SURFACE_WIDTH/2 - 2*RADIUS, -SURFACE_WIDTH/2 + 2*RADIUS, num=10):
            for l_yellow in np.linspace(-SURFACE_LENGTH/2 + 2*RADIUS, SURFACE_LENGTH/2 - 2*RADIUS, num=10):
                for w_red in np.linspace(SURFACE_WIDTH/2 - 2*RADIUS, -SURFACE_WIDTH/2 + 2*RADIUS, num=10):
                    for l_red in np.linspace(-SURFACE_LENGTH/2 + 2*RADIUS, SURFACE_LENGTH/2 - 2*RADIUS, num=10):
                        pos_white = vector(l_white,w_white,0)
                        pos_yellow = vector(l_yellow,w_yellow,0)
                        pos_red = vector(l_red,w_red,0)
                        j = 0
                        if check_superposition(pos_white, pos_yellow, pos_red):
                            j = 2
                        #sleep(0.1)
                        else:
                            X_train.append((pos_white,pos_yellow,pos_red))
                        env.reset(pos_white, pos_yellow, pos_red)
                        
                        while j < 1:
                            action_index = int(np.random.choice(len(actions)))
                            nextState, reward, done, add_new_state = env.step(actions[action_index][0],actions[action_index][1],actions[action_index][2],actions[action_index][3],actions[action_index][4])
                            if reward != 0:
                                Y_train.append(action_index)
                                print(len(Y_train),len(X_train))
                                break
                            else:
                                env.reset(pos_white, pos_yellow, pos_red)
        #sleep(1)

X_train = np.asarray(X_train)
Y_train = np.asarray(Y_train)
np.save("Xtrain", X_train)
np.save("Ytrain", Y_train)