import numpy as np
import matplotlib.pyplot as plt

def generate_axes(variables, x_range, y_ranges, colors = None):
    #generate default colors
    if not colors:
        color_options = ['blue','green','orange']
        colors = color_options*int(np.ceil(len(variables)/len(color_options)))
        colors = colors[:len(variables)]

    #create figure and axis objects
    fig, axs = plt.subplots(len(variables), figsize=(25,10))

    #lines are objects used to set data live
    lines = []
    data = []

    #creating lines for each variable
    for ind,label in enumerate(variables):
        axs[ind].set_ylim(y_ranges[ind])
        data.append(np.random.randn(x_range))
        line, = axs[ind].plot(data[ind], 'tab:'+colors[ind])
        lines.append(line)
        axs[ind].set_title(label)
    fig.tight_layout()
    return fig,axs,lines,data

def update_plot(lines,data,new_data):
    for ind in range(len(data)):
        data[ind] = data[ind][1:]
        data[ind] = np.append(data[ind],new_data[ind])
        lines[ind].set_ydata(data[ind])
    plt.pause(0.01)