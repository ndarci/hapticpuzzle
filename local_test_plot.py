import matplotlib.pyplot as plt
import numpy as np
import time
from hapticpuzzle_plot import *


fig,axs,lines,data = generate_axes(['pos','vel','acc'],100)

while True:
    try:
        #idea here is to grab one data point for pos,vel, and acc from the rpi,
        #then send this data into our update plot function to display in real time

        update_plot(lines,data,np.random.randn(3))
    except KeyboardInterrupt:
        break

print('goodbye')
