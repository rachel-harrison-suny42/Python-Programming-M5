# Rachel Harrison
# Python Programming
# M5 Assignment - Modular Programming

#Goal: Update my submission for the M4 Assignment using the principles of Modular Programming covered in Module 5.

#Assignment Requirements & How they are satisfied:

# Requirement 1. At least two custom modules, each handling a distinct purpose (for example, one module for calculations and one for file handling).
# Satisfied: In the engine folder, there are 3 modules: inputs.py, geometry.py, and renderer.py.  Then, there is an __init__.py that ties these all together in the same folder.

# Requirement 2. A main program that imports your modules using at least two import styles (such as import module_name and from module_name import function).
# Satisfied:  the functions that were migrated to the renderer.py module are imported via "from engine import renderer" and therefore require the renderer.* prefix when they are called here in main.py.  The rest of the functions that were migrated to inputs.py and geometry.py are imported via "from engine import ([list])" where list is the individual function names being listed.  These do not require a special prefix when they are called here in main.py.

# Requirement 3.  Use of at least one built-in library module (for example, math, datetime, or random).
# Satisfied:  Both main.py and geometry.py require the built-in math library module and main.py also requires the time, sys, and shutil built-in library modules.

# Requirement 4. Docstrings and comments in each module explaining what it does and how it interacts with the rest of the program.
# Satisfied: all of the original docstrings are carried over from the M4 assignment version (that was all one file) and each individual module file in the engine folder also has a new docstring description.



#------------------------------------------------------------------
# Goal: Implement a simple program that requests an input from the 
# user of an n value.  Then, use that n value to calculate the 
# structural elements (topology) of the regular prism (which has a
# pair of (regular) n-gons as its bases) using Euler's polyhedra formula
# V - E + F = 2 (where V is the number of vertices, E is the number
# of edges, and F is the number of faces of the resulting polyhedron).
# Then, using the calculated structural elements, construct the 
# polyhedra in 3-space (X, Y, Z) and use multiplication by
# yaw/pitch/roll angles to compute how the object repositions in 
# space as the result of being rotated about an axis.  Finally,
# use 3-space to 2-space camera projection to render the image to
# the screen from the perspective of a stationary camera at a fixed
# distance.

#Secondary goal: Accomplish the first goal procedurally using linear algebra
#and render to the terminal as an escape animation by writing a renderer from
#scratch that utilizes Bresenham's Line Algorithm.  Write this in such a way
#that makes future modification/reuse of code (e.g. changing from orthographic
# to perspective projection, swapping escape animations for a modern renderer,
# etc.) as straight forward as possible.

import numpy as np #simplifies matrix math
import math        #for trigonometric math
import shutil      #to query terminal resolution
import time        #needed to render at 60fps
import sys         #in order to control terminal cursor position & timing

from engine import renderer

from engine import (
    query_number_sides,
    query_rotation_axis,
    get_vertices_and_edges,
    lift_to_four_d,
    get_rotation_x,
    get_rotation_y,
    get_rotation_z
)


#At 60 frames per second, the object must rotate [(2*Pi)/60] radians each frame in order to
#complete a full rotation in one second.  Instead of carrying over the truncation/rounding
#errors by multiplying each successive frame's vertex matrix by the same rotation matrix, we
#will increment the rotation angle theta and calculate each successive frame using the 
#original vertex matrix in real time.  However, a full rotation each second is very fast, so 
#we will automatically have the shape complete 5 rotations over 10 seconds.  Thus, we will 
#define frameTheta as t*[(Pi)/60], and increment t from 0 through 599, passing it as a 
#parameter to the appropriate get_rotation_{x,y,z}() at each increment, then matrix multiplying 
#the returned matrix by the initial vertex matrix each time, and finally passing the result 
#to the terminal renderer to be output to the screen.

############################################
###------------------MAIN----------------###
############################################


########---------------------------#########
##----GLOBAL VARIABLE INITIALIZATIONS-----##
########---------------------------#########


#------------------------------------------#
# VARIABLES DEFINED ONLY ONCE PER FILE RUN #
#-------------------START------------------#

# define n as n-gon side count
n = query_number_sides()

# initialize axis as axis of rotation
axis = query_rotation_axis()

# initialize vertMatrix as initial vertex matrix & edgeList as edge list, passing n as param
vertMatrix, edgeList = get_vertices_and_edges(n)

# initialize FPS as desired frames per second of animation
FPS = 60

# initialize frameDuration to hold conversion of FPS to seconds
frameDuration = 1.0 / FPS

#-------------------STOP-------------------#


#-------------------------------------------------#
# VARIABLES THAT ARE INITIALIZED & UPDATED IN lOOP#
#----------------------START----------------------#

# initialize frame count to track animation progress
frameCount = 0

# initilize running as boolean flag for animation render loop
running = True

# initialize cached terminal window size holders, which are used to check if size has
# changed each loop.  They control the conditional invalidation of the back buffer's
# master template.  When a change occurs, a new template must be created with the new
# size parameters, and the cached sizes must be overwritten with the new sizes for the
# next loop's use.
cachedColumns = 0
cachedRows = 0
cachedStride = cachedColumns + 1

#----------------------STOP----------------------#


########---------------------------#########
##---------ANIMATION RENDER LOOP----------##
########---------------------------#########

# All  of the calculations of vertex rotations and mathematical preparation 
# needed to output the animation to the terminal are wrapped inside a loop 
# which tracks the high-accuracy system time via time.perf_counter() in 
# order to verify that a new frame of the animation is populated to the 
# terminal screen at a rate of EXACTLY 1 frame per 1/60 seconds in order to 
# guarantee a steady 60 FPS animation is output.

#clear the terminal
print('\033[2J')
#initialize frame animation loop using boolean flag running
while running:
    #get exact time this frame's loop started
    frameStart = time.perf_counter()

    #PUT MATH CHAIN HERE
    # convert frameCount(k) to frameTheta(k*[(Pi)/60]) for rotation matrix query
    frameTheta = float(frameCount) * ((1.0 * math.pi)/60.0)
    # control flow using axis to get chosen rotation matrix for current frame 
    if (axis == 'x'):
        frameRotationMatrix = get_rotation_x(frameTheta)
    elif (axis == 'y'):
        frameRotationMatrix = get_rotation_y(frameTheta)
    else:
        frameRotationMatrix = get_rotation_z(frameTheta)
    
    # calculate current frame's vert positions (matrix mult via rotation matrix @ verts)
    frameVert = frameRotationMatrix @ vertMatrix

    # convert rotated 3 x n vertex matrix to its homogeneous 4 x n equivalent
    frameVertInFour =  lift_to_four_d(frameVert)
    
    # get current terminal (output "screen") resolution
    newColumns, newRows = shutil.get_terminal_size()

    #control flow for (Has the terminal window size changed?)
    if ((newColumns == cachedColumns) and (newRows == cachedRows)):
        pass
    else:
        #generate a new 1D buffer list template (with the \n's cooked in)
        masterTemplate = renderer.get_new_template(newRows, newColumns)
        #update the cached terminal window size holders
        cachedColumns = newColumns
        cachedRows = newRows
        cachedStride = cachedColumns + 1
        # get projection matrix and store as termProjMatrix
        termProjMatrix = renderer.get_terminal_projection(cachedColumns, cachedRows)
    
    #copy the template (empty list with \n's cooked in at intervals determined
    #by the current terminal window size) into the workingBuffer
    workingBuffer = masterTemplate.copy()
    
    # calculate projectedMatrix as matrix multiplication product of 3 x 4 projection
    # matrix @ homogeneous 4 x n vertex matrix
    projectedMatrix = termProjMatrix @ frameVertInFour

    # create integer 2 x n numpy array toScreen from projected matrix by dropping
    # the homogeneous 3rd row of 1s, rounding each cell's value to the nearest 
    # integer, and casting those values to integers
    toScreen = np.round(projectedMatrix[:2]).astype(int)
    
    # loop over every pair of vertex column indices in edgelist and use them to pull
    # (x,y) points in pairs and hands to the edge_to_buffer function (i.e. Bresenham)
    for a, b in edgeList:
        a_x = toScreen[0, a]
        a_y = toScreen[1, a]
        b_x = toScreen[0, b]
        b_y = toScreen[1, b]
        renderer.edge_to_buffer(a_x, a_y, b_x, b_y, cachedRows, cachedStride, workingBuffer)
        
    #once edgeList has been rendered to the working buffer, concatentate to string
    frameOut = "".join(workingBuffer)
    
    #Use sys.stdout.write to write leading move-cursor-home character and frameOut
    #to frame buffer
    sys.stdout.write("\033[H" + frameOut)
    
    #force terminal to render the frame buffer immediately
    sys.stdout.flush()

    #increment frame counter
    frameCount += 1
    #After 300 frames, change running flag to false, which will break render loop
    if (frameCount > 599):
        running = False
    #calculate exact elapsed time between frameStart and now
    elapsed = time.perf_counter() - frameStart

    #calculate time to wait before next loop so output is always 60FPS
    sleepTime = frameDuration - elapsed

    #control flow to sleep/not sleep before next loop
    if sleepTime > 0:
        time.sleep(sleepTime)
    else:
        # if frame took longer to calculate and render than duration of 
        # single frame (i.e. frameDuration), do not sleep, start next loop
        pass
input("Thank you for trying my program.  Press ENTER to quit. - Rachel Harrison")