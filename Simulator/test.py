from carom import Carom
import sys
import random
from Parameters import RADIUS
sys.setrecursionlimit(10000)
env = Carom(render = True)
env.reset()
env.step(0,0,0,0,0.3)
env.step(0,0,0,90,4)
env.step(0,0,0,90,5) #a, b, thetha, phi, V
env.step(0,0,0,90,5)
env.step(0,0,0,90,5)
env.step(0,0,0,90,5)
env.reset()
for i in range(50):
    env.step(random.uniform(-0.5, 0.5)*RADIUS,random.uniform(-0.5, 0.5)*RADIUS,random.uniform(0, 50),random.uniform(0, 360),random.uniform(0.5, 6))

print("Fin")

# pb: step infinie