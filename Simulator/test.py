from carom import Carom

env = Carom(render = True)
env.reset()
env.step(0,0,0,0,1) #a, b, thetha, phi, V
env.reset()
env.step(0,0,0,0,3)
env.step(0,0,40,10,3)
env.step(0,0,40,10,3)
env.step(0,0,40,10,3)
env.step(0,0,40,10,3)
env.step(0,0,40,10,3)
env.step(0,0,40,10,3)

for a in range(40):
    env.step(0,0,40,10,3)

print("Fin")
