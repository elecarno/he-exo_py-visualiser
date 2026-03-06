import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# encoder readings in degrees
enc1_deg = 30
enc2_deg = -45
enc3_deg = 0
enc4_deg = 0

# segment lengths
lineweight = 4

s = 0.4 # spacing between encoders
l1 = 1.0
l2 = 0.6*l1
l3 = 3.0*l1

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

if __name__ == "__main__":
    # create plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])
    ax.set_zlim([-4, 4])

    ax.set_box_aspect([1,1,1])
    ax.set_title("Leader Arm Visualisation")

    # add line segments
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

    seg_2a = LineSegment(
        seg_1b.get_end_position(),
        seg_1b.get_total_rotation(),
        l2
    )
    seg_2a.local_rotation = np.array([180, enc2_deg, 0])
    seg_2b = LineSegment(
        seg_2a.get_end_position(),
        seg_1b.get_total_rotation(),
        l1
    )
    seg_2b.local_rotation = np.array([90, 0, 0])

    # seg_3 = LineSegment(
    #     seg_2b.get_end_position(),
    #     seg_2b.get_total_rotation(),
    #     l3
    # )


    # plot line segments
    ax.plot(
        [
            seg_1a.position[0],
            seg_1a.get_end_position()[0],
            seg_1b.get_end_position()[0]
        ], 
        [
            seg_1a.position[1],
            seg_1a.get_end_position()[1],
            seg_1b.get_end_position()[1]
        ], 
        [
            seg_1a.position[2],
            seg_1a.get_end_position()[2],
            seg_1b.get_end_position()[2]
        ], 
        linewidth=lineweight,
        color="b"
    )

    ax.plot(
        [
            seg_2a.position[0],
            seg_2a.get_end_position()[0],
            seg_2b.get_end_position()[0]
        ], 
        [
            seg_2a.position[1],
            seg_2a.get_end_position()[1],
            seg_2b.get_end_position()[1]
        ], 
        [
            seg_2a.position[2],
            seg_2a.get_end_position()[2],
            seg_2b.get_end_position()[2]
        ], 
        linewidth=lineweight,
        color="r"
    )

    # ax.plot(
    #     [
    #         seg_3.position[0],
    #         seg_3.get_end_position()[0],
    #     ], 
    #     [
    #         seg_3.position[1],
    #         seg_3.get_end_position()[1],
    #     ], 
    #     [
    #         seg_3.position[2],
    #         seg_3.get_end_position()[2],
    #     ], 
    #     linewidth=lineweight,
    #     color="g"
    # )

    # show plot
    plt.show()