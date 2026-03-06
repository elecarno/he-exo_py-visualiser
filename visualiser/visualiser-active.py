import serial
import time
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# SERIAL -------------------------------------------------------------------------------------------
port = 'COM4'
baud_rate = 115200

ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)


# VARIABLES ----------------------------------------------------------------------------------------
# encoder readings in degrees
enc1_deg = 0
enc2_deg = 0
enc3_deg = 0
enc4_deg = 0

# segment lengths
lineweight = 4

s = 0.4 # spacing between encoders
l1 = 1.0
l2 = 0.6*l1
l3 = 3.0*l1


# CLASSES ------------------------------------------------------------------------------------------
class Rotation:
    @classmethod
    def rot_x(self, deg):
        rad = np.deg2rad(deg)
        return np.array([
            [1, 0, 0],
            [0, np.cos(rad), -np.sin(rad)],
            [0, np.sin(rad), np.cos(rad)]
        ])

    @classmethod
    def rot_y(self, deg):
        rad = np.deg2rad(deg)
        return np.array([
            [np.cos(rad), 0, np.sin(rad)],
            [0, 1, 0],
            [-np.sin(rad), 0, np.cos(rad)]
        ])

    @classmethod
    def rot_z(self, deg):
        rad = np.deg2rad(deg)
        return np.array([
            [np.cos(rad), -np.sin(rad), 0],
            [np.sin(rad), np.cos(rad), 0],
            [0, 0, 1]
        ])


class LineSegment:
    def __init__(self, position=np.array([0, 0, 0]), rotation=np.array([0, 0, 0]), length=0.0):
        self.position = position
        self.global_rotation = rotation
        self.local_rotation = np.array([0, 0, 0])
        self.length = length

    def get_end_position(self):
        # set to initially point directly up (z-axis up)
        endpoint = np.array([0, 0, self.length])

        # apply local rotation
        endpoint = Rotation.rot_x(self.local_rotation[0]) @ endpoint
        endpoint = Rotation.rot_y(self.local_rotation[1]) @ endpoint
        endpoint = Rotation.rot_z(self.local_rotation[2]) @ endpoint

        # apply global rotation
        endpoint = Rotation.rot_x(self.global_rotation[0]) @ endpoint
        endpoint = Rotation.rot_y(self.global_rotation[1]) @ endpoint
        endpoint = Rotation.rot_z(self.global_rotation[2]) @ endpoint

        # add calculated endpoint to start position
        endpoint += self.position

        # return calculated endpoint
        return endpoint

    def get_total_rotation(self):
        return self.local_rotation + self.global_rotation


# PLOT ---------------------------------------------------------------------------------------------
def animation(frame):
    global seg1_line, seg2_line

    try:
        serial_println = ser.readline().decode('utf-8').strip()

        if not serial_println:
            return seg1_line, seg2_line

        encoder_degrees = [float(part.split(":")[1]) for part in serial_println.split(",")]

        enc1_deg = encoder_degrees[0]
        enc2_deg = encoder_degrees[1]

        print(enc1_deg, enc2_deg)

        # SEGMENT 1
        seg_1a = LineSegment(
            np.array([0, 0, 0]),
            np.array([0, 180, 0]),
            l1
        )
        seg_1a.local_rotation = np.array([0, enc1_deg, 0])

        seg_1b = LineSegment(
            seg_1a.get_end_position(),
            seg_1a.get_total_rotation(),
            l1
        )
        seg_1b.local_rotation = np.array([90, 0, 0])

        # SEGMENT 2
        seg_2a = LineSegment(
            seg_1b.get_end_position(),
            seg_1b.get_total_rotation(),
            l2
        )
        seg_2a.local_rotation = np.array([180, enc2_deg, 0])

        seg_2b = LineSegment(
            seg_2a.get_end_position(),
            seg_1a.get_total_rotation(),
            l1
        )
        seg_2b.local_rotation = np.array([0, 180, 0])


        # Update segment 1 line
        x1 = [
            seg_1a.position[0],
            seg_1a.get_end_position()[0],
            seg_1b.get_end_position()[0]
        ]

        y1 = [
            seg_1a.position[1],
            seg_1a.get_end_position()[1],
            seg_1b.get_end_position()[1]
        ]

        z1 = [
            seg_1a.position[2],
            seg_1a.get_end_position()[2],
            seg_1b.get_end_position()[2]
        ]

        seg1_line.set_data(x1, y1)
        seg1_line.set_3d_properties(z1)

        # Update segment 2 line
        x2 = [
            seg_2a.position[0],
            seg_2a.get_end_position()[0],
            seg_2b.get_end_position()[0]
        ]

        y2 = [
            seg_2a.position[1],
            seg_2a.get_end_position()[1],
            seg_2b.get_end_position()[1]
        ]

        z2 = [
            seg_2a.position[2],
            seg_2a.get_end_position()[2],
            seg_2b.get_end_position()[2]
        ]

        seg2_line.set_data(x2, y2)
        seg2_line.set_3d_properties(z2)

    except Exception as e:
        print("Error:", e)

    return seg1_line, seg2_line


if __name__ == "__main__":
    # create plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    size = 1.5
    ax.set_xlim([-size, size])
    ax.set_ylim([-size, size])
    ax.set_zlim([-size, size])

    ax.set_box_aspect([1,1,1])
    ax.set_title("Leader Arm Visualisation")

    seg1_line = ax.plot([0,0],[0,0],[0,0], linewidth=lineweight, color="b")[0]
    seg2_line = ax.plot([0,0],[0,0],[0,0], linewidth=lineweight, color="r")[0]

    ani = FuncAnimation(fig, animation, interval=15, blit=False)

    # show plot
    plt.show()