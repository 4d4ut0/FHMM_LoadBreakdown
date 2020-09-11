###################################################################
# Basic real-time serial data plotting
# by Shivam Chudasama - may 2013
###################################################################
# Prepare your data as comma seperated and finish each line with
# the 'n'. Set how many data point you have at the each line by
# editing the STEP variable.
###################################################################

import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial('/dev/ttyACM0', 9600)

temp = np.arange(32)
def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 1000:
        cnt += 1
        temp_y = ser.readline()
        xtc = temp_y.split(',')
        temp = xtc[0:32]
        yield cnt, temp
data_gen.t = 0

fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot([], [], lw=2)
ax.set_ylim(0, 120)
ax.set_xlim(0, 5)
ax.grid()
xdata, ydata = [], []
def run(data):
    # update the data
    cnt, y = data
    xdata.append(cnt)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if cnt >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
    repeat=False)
plt.show()