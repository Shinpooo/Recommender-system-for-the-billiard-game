import numpy as np
import matplotlib.pyplot as plt

#plt.axis([0, 10, 0, 1])
plt.ylabel('Reward')
plt.xlabel('Epoch')
for i in range(100):
    plt.plot(i, np.sin(i), 'o')
    plt.pause(0.01)
plt.show()

#