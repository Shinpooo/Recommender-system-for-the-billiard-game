from carom import Carom
import random
from Parameters import RADIUS
# import sys
# sys.setrecursionlimit(10000)
a = True
b = False
print(int(a),int(b))
liste = [ 3,3,3]
print(4 not in liste, 3 in liste)
env = Carom(render = True)
env.reset()
#env.step(0,0,0,90,5) #a, b, thetha, phi, V
env.step(0,0,0,1,8)
# for i in range(2000):
    # env.step(random.uniform(-0.5, 0.5)*RADIUS,random.uniform(-0.5, 0.5)*RADIUS,random.uniform(0, 50),random.uniform(0, 360),random.uniform(0.5, 6))

print("Fin")

# pb: step infinie