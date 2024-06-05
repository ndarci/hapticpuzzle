import matplotlib.pyplot as plt
import numpy as np
import time

fig, axs = plt.subplots(3)

pline, = axs[0].plot(np.random.randn(100), 'tab:blue')
axs[0].set_title('Position')
vline, = axs[1].plot(np.random.randn(100), 'tab:green')
axs[1].set_title('Velocity')
aline, = axs[2].plot(np.random.randn(100), 'tab:orange')
axs[2].set_title('Acceleration')
fig.tight_layout()

while True:
    try:
        pline.set_ydata(np.random.randn(100))
        vline.set_ydata(np.random.randn(100))
        aline.set_ydata(np.random.randn(100))
        plt.pause(0.01)
    except KeyboardInterrupt:
        break

print('goodbye')
