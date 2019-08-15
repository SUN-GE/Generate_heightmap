#!/usr/bin/env python

import rospy
import time
from grid_map_msgs.msg import GridMap
from grid_map_msgs.msg import GridMapInfo
from std_msgs.msg import Float32MultiArray
import numpy as np
import matplotlib.pyplot as plt

def grid_callback(grid_msg):
    #subscribe to the gridmap data
    grid = grid_msg.data
    a = grid[0].data

    #get grid map dimensions
    array_dimension = grid[0].layout.dim[0].size

    #convert gridmap data in to numpy array and reshape to 2D
    b = np.array(a)
    c = b.reshape(array_dimension,array_dimension)
    np.save('hm_array.npy', c)

def process_hm():
    #amount of border around the actual heightmap
    padding = 5
    
    #load the saved array and replace all 'nan' with zeroes
    hm_array = np.load('hm_array.npy')
    hm_array_zero = np.nan_to_num(hm_array)

    #returns the indices of all non zero elements in a tuple_of_arrays
    indices = np.nonzero(hm_array_zero) 

    #obtain the dimensions of the actual heightmap (considering padding)
    first_row = min(indices[0]-padding)
    last_row = max(indices[0]+padding)
    first_col = min(indices[1]-padding)
    last_col = max(indices[1]+padding)

    #extracts a subarray
    new_hm_array = hm_array_zero[first_row:last_row, first_col:last_col]

    return new_hm_array

def show_image(hm_array):
    fig = plt.imshow(hm_array, cmap="gray")
    plt.axis('off')
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig('hm.png', bbox_inches='tight', pad_inches = 0)
    plt.show()

def subscriber():
    rospy.init_node('hm_generation')
    rospy.Subscriber('/elevation_mapping/elevation_map_raw', GridMap, grid_callback)
    rospy.spin()

if __name__ == '__main__':
    
    try:
        subscriber()
        heightmap = process_hm()
        show_image(heightmap)

    except rospy.ROSInterruptException:
        pass
