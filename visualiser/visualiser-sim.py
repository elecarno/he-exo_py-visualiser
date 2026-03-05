import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# encoder readings in degrees
enc1 = 30
enc2 = 0
enc3 = 0
enc4 = 0

# points
e1 = np.array([0, 0, 0])
j1 = np.array([0, 0, 0])
e2 = np.array([0, 0, 0])

# segment lengths
s = 0.4 # spacing between encoders
l1 = 1.0
l2 = 0.5*l1