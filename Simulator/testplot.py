import numpy as np
import matplotlib.pyplot as plt
from math import*
#plt.axis([0, 10, 0, 1])
plt.ylabel('Reward')
plt.xlabel('Epoch')
for i in range(1000):
    plt.plot(i, np.cos(i), 'o')
    plt.pause(0.0001)
    print(i)
plt.show()

#