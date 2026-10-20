"""
Matrix Math and 3D Geometry Module

This module is the core mathematical engine.  It handles mathematical transformations, vertex and edge list generation, and matrix rotation logic.  It is decoupled from the terminal interface.  It takes in parameters from main.py and returns spatial coordinate arrays to be passed on to the renderer module.
"""
import numpy as np
import math
#-------------------------------------------------------#
#-Matrix Generation and Homogeneous Extension Functions-#
#------------------------START--------------------------#
def get_vertices_and_edges(nGonSides):
    """
    Calculates the initial vertex positions of the uniform regular n-prism inside 
    a unit sphere in 3-space and the list of pair of vertices that are connected
    by an edge and returns: (1) as a 3 x n numpy array with the (x,y,z)
    coordinates of those vertices as its columns, and (2) a list of ordered pairs
    of vertices to connect with an edge as the index of their columns in the 3 x n
    numpy array
    
    args:
        nGonSides(int): the number of sides in each n-gon base (value collected from
                        user via query_number_sides())

    returns: 
        3 x n numpy array with (x, y, z) coordinates as columns
        list of (column index, column index) pairs of vertices in 3 x n array
    """
    #initialize list of theta displacements for equidistant rotations about a circle
    #between each vertex of the regular polygon bases of the uniform regular n-prism
    thetaDisplace = []
    
    #initialize lists from which the rows of the numpy array will be populated
    xList = []
    yList = []
    zList = []
    
    #R is the circumradius of the n-gon (i.e. the distance from the center of  
    #the polygon (to which the vertex belongs) to each of its vertices)
    R = 1.0/(2.0 * math.sin((math.pi)/float(nGonSides)))

    #loop from k=0 to k=nGonSides-1 to add vertices of n-gon base in plane y=0.5
    for k in range(nGonSides):
        thetaDisplace.append((2.0 * math.pi * float(k))/float(nGonSides))
        xList.append(R * math.cos(thetaDisplace[k]))
        yList.append(0.5)
        zList.append(R * math.sin(thetaDisplace[k]))
    
    #Loop from l=0 to l=nGonSides-1 to add vertices of n-gon base in plane y=-0.5
    for l in range(nGonSides):
        xList.append(R * math.cos(thetaDisplace[l]))
        yList.append(-0.5)
        zList.append(R * math.sin(thetaDisplace[l]))
    
    #create numpy array whose rows are x_list, y_list, and z_list
    startVertices = np.array([xList, yList, zList], dtype=float) 
    #initialize list to hold pairs of raw column indices of the vertices in startVertices
    indexPairs = []
    #Create Edge List
    for i in range(nGonSides):
        nextIndex = (i + 1) % nGonSides
        #Base 1 Edges
        indexPairs.append((i, nextIndex))
        #Base 2 Edges
        indexPairs.append((i + nGonSides, nextIndex + nGonSides))
        #Base 1 to Base 2 Edges
        indexPairs.append((i, i + nGonSides))
    
    #return the vertex numpy array
    return startVertices, indexPairs
#-----------------------------------------------------------------------------

#Function that lifts this frame's Rotated Vertex Matrix to 4 x n for toScreen operation#
def lift_to_four_d(frameVertsInThreeD):
    """
    Converts 3 x n matrix holding the vertices rotated for the current frame to
    a 4 x n matrix for homogeneous equation that uses 2 x 4 matrix for orthographic
    3d-to-2d projection, aspect ratio correction, and scaling in order to render
    the 3d animation to a 2d screen using ANSI escape animation (ascii in the 
    resolution and character-as-pixel aspect ratio) of the terminal.

    args:
        frameVertsinThreeD (3 x n numpy array): called frameVert in MAIN

    returns:
        4 x n numpy array with 1s in bottom row
    """
    # create a new 4 x n numpy array by putting the 3 x n array as the first 3 rows and
    # adding a row of ones
    frameVertsinFourD = np.vstack([frameVertsInThreeD, np.ones(frameVertsInThreeD.shape[1])])

    return frameVertsinFourD

#----------------------------------END---------------------------------------#
#-------------------------#   
#Rotation Matrix Functions#
#----------START----------#
def get_rotation_x(theta):
    """
    Calculates the trigonometric values for theta and returns 3 x 3 matrix for rotation
    about the x axis.

    args:
        theta(float): rotation angle in radians

    returns:
        3 x 3 numpy array with dtype=float
    """
    #calculate values for matrix that not in {0,1}
    cosT = math.cos(theta)
    sinT = math.sin(theta)
    negSinT = -1.0 * sinT
    
    #assemble rotation matrix
    rotationMatrix = np.array([[1.0, 0.0, 0.0], [0.0, cosT, negSinT], [0.0, sinT, cosT]], dtype=float)
    
    #return
    return rotationMatrix    
#-----
def get_rotation_y(theta):
    """
    Calculates the trigonometric values for theta and returns 3 x 3 matrix for rotation
    about the y axis.

    args:
        theta(float): rotation angle in radians

    returns:
        3 x 3 numpy array with dtype=float
    """
    #calculate values for matrix that not in {0,1}
    cosT = math.cos(theta)
    sinT = math.sin(theta)
    negSinT = -1.0 * sinT
    
    #assemble rotation matrix
    rotationMatrix = np.array([[cosT, 0.0, sinT], [0.0, 1.0, 0.0], [negSinT, 0.0, cosT]], dtype=float)
    
    #return
    return rotationMatrix    
#-----
def get_rotation_z(theta):
    """
    Calculates the trigonometric values for theta and returns 3 x 3 matrix for rotation
    about the z axis.

    args:
        theta(float): rotation angle in radians

    returns:
        3 x 3 numpy array with dtype=float
    """
    #calculate values for matrix that not in {0,1}
    cosT = math.cos(theta)
    sinT = math.sin(theta)
    negSinT = -1.0 * sinT
    
    #assemble rotation matrix
    rotationMatrix = np.array([[cosT, negSinT, 0.0], [sinT, cosT, 0.0], [0.0, 0.0, 1.0]], dtype=float)
    
    #return
    return rotationMatrix    
#----------END----------#