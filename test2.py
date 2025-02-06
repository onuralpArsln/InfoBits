import matplotlib.pyplot as plt
import numpy as np

zero_array = np.zeros((100, 100))
plt.imshow(zero_array, cmap='gray', vmin=0, vmax=100, interpolation='none')
plt.axis('off')
plt.show()
