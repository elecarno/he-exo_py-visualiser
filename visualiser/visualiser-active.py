import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# SERIAL -------------------------------------------------------------------------------------------
port = 'COM4'
baud_rate = 115200

ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)


# PLOT ---------------------------------------------------------------------------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

ax.set_box_aspect([1,1,1])
ax.set_title("Leader Arm Visualisation")

# Initial shaft line
shaft_line, = ax.plot([0,1], [0,0], [0,0], linewidth=4)


# UPDATE -------------------------------------------------------------------------------------------
def animation(frame):
    try:
        serial_println = ser.readline().decode('utf-8').strip()
        output_degrees = serial_println.split("output: ")[1]
        if serial_println:
            degrees = float(output_degrees)
            rad = np.deg2rad(degrees)

            x = [0, np.sin(rad)]
            y = [0, 0]
            z = [0, -np.cos(rad)]

            shaft_line.set_data(x, y)
            shaft_line.set_3d_properties(z)

    except:
        pass

    return shaft_line,

ani = FuncAnimation(fig, animation, interval=15)
plt.show()