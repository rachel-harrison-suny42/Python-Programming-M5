"""
3D Projection and Terminal Rasterization Module

This module translates 3D spatial data into a 2D physical display.
It takes the transformed geometry matrices calculated by geometry.py, projects them orthographically,
and uses Bresenham's Line Algorithm to draw the resulting wireframes into a 1D character buffer.  Then,
main.py prints that character buffer to the standard output.
"""
import numpy as np
#-----------------------------------------------------------------------------------------

def get_terminal_projection(terminalWidth, terminalHeight):
    """
    Calculates the necessary scaling factor and the x and y origin translation offsets,
    given the terminal "resolution" (i.e. the # of rows and columns in the terminal 
    window) collected for this frame (i.e. pass through the main animation loop), and
    combines those values with the y-scaling factor needed to correct for the fact that
    each "pixel" of the terminal (i.e. character space) is twice as tall as it is 
    wide, and puts all of these modifications together in the context of the needed 
    matrix to orthographically (i.e. NOT perspective, therefore no vanishing points) 
    project the 3D representation to the 2D screen coordinates.

    args:
        terminalWidth (int): Horizontal width (columns) polled from shutil in MAIN
        terminalHeight (int): Vertical height (rows) polled from shutil in MAIN

    returns:
        projectionMatrix (3 x 4 numpy array): projection matrix (to be matrix 
                                              multiplied with the current frame's
                                              4D homogeneous extension of the 3d 
                                              rotation vertex matrix)
    """
    # Since the vertex coords are normalized between -1 and 1, the scaling factor
    # S should scale the entire image (i.e. both the x and y coords) by 0.9, so
    # that the resulting image has a smaller buffer at the top and bottom.  Then,
    # since the terminal window can be arbitrarily resized by a user to fit their
    # desktop working environment, we choose the minimum value from the aspect
    # ratio adjusted width and the height, and multiply that value by the 0.9 scalar.
    scalar = 0.9 * min((terminalWidth / 2.0), terminalHeight)
    # Since the (0,0) in the terminal is top leftmost character space, we need to 
    # shift both x and y 3D-to-2D projected screen coordinates halfway down the
    # height of the terminal "screen" and halfway across the width.
    translateX = terminalWidth / 2.0
    translateY = terminalHeight / 2.0
    # Finally, in order to future proof this program and these functions to allow
    # for an expansion where the user is given the choice of orthographic or
    # perspective projection and/or the geometry is rendered with shaded faces,
    # backface culling, etc., we keep the bottom row of zeroes in the base
    # projection matrix and fill the bottom row of the column carrying the 
    # x and y translations with the w=1 of a standard homogeneous extension of a
    # 2d column vector into 3 space.  Also, we remember to correct the "pixel"
    # aspect ratio from roughly 2:1 H:W to square by modifying the main diagonal
    # cell of the y-value row by both the scalar for the entire screen (that is 
    # also applied the the main diagonal value of the x-value row) by further 
    # scaling it by 0.5.
    projectionMatrix = np.array([[scalar, 0.0, 0.0, translateX], [0.0, 0.5 * scalar, 0.0, translateY], [0.0, 0.0, 0.0, 1]], dtype=float)
    return projectionMatrix
#----------------------------------------------------------------------------------

def get_new_template(rows, columns, emptyChar=' '):
    """
    Generates a new template (for the buffer) which is a list of empty character spaces
    with a newline character placed every (columns+1) spaces and continuing such that
    there are exactly (rows) rows, in order to provide a blank canvas that exactly fits
    the dimensions of the terminal window.

    args:
           rows (int) : value pulled from shutil giving the number of rows in the 
                        terminal window
        columns (int) : value pulled from shutil giving the number of columns in the
                        terminal window
    returns:
        newTemplate (list) : list of blank characters corresponding to the terminal
                             window size with newline characters after the end of 
                             each row
    """
    #stride modifies window width to make room for the newline character in each row
    stride = columns + 1
    #initialize template list with all blank character spaces
    newTemplate = [emptyChar] * (rows * stride)
    #replace the space at the end of each row with the newline character
    for row in range(rows):
        indexToUpdate = (row * stride) + columns
        newTemplate[indexToUpdate] = '\n'
    return newTemplate

#-------------------------------------------------------------------------------------------
    
def edge_to_buffer(v1_x, v1_y, v2_x, v2_y, Rows, Stride, workingBuffer):
    """
    Handles necessary pre-calculations and implementation of Bresenham's line algorithm
    to draw the edge connecting vertices 1 and 2 into the workingBuffer at the "resolution" 
    of the terminal screen given by Rows and Stride.

    args:
        v1_x (int) : x-coordinate of vertex 1
        v1_y (int) : y-coordinate of vertex 1
        v2_x (int) : x-coordinate of vertex 2
        v2_y (int) : y-coordinate of vertex 2
        Rows (int) : height of output grid
      Stride (int) : width + 1 of output grid
      workingBuffer (list): list with length Rows * Stride, with newline characters at
                            the end of each row pre-filled

    return:
        None
    """
    #absolute delta x and y
    dx = abs(v1_x - v2_x)
    dy = abs(v1_y - v2_y)
    #initialize x and y direction stepping holders
    xstep = 0
    ystep = 0
    #control flow for x step (direction in x)
    if (v1_x < v2_x):
        xstep = 1
    else:
        xstep = -1
    #control flow for y step (direction in y)
    if (v1_y < v2_y):
        ystep = 1
    else:
        ystep = -1
    #initialize initial error variable as delta x - delta y
    error = dx - dy

    #choose appropriate character to draw based on line slope
    #if run of slop is more than twice the rise
    if (dx > (2 * dy)):
        drawCharacter = '-'
    elif (dy > (2 * dx)): #else if rise of slop is more than twice the run
        drawCharacter = '|'
    elif (xstep == ystep): #else if diag UL-DR or vice versa
        drawCharacter = '\\'
    else:
        drawCharacter = '/'
        
    #begin rasterization loop
    while True:
        #check that (v1_x, v1_y) is inside the terminal window
        if (v1_x >= 0) and (v1_x < (Stride - 1)) and (v1_y >= 0) and (v1_y < Rows):
            index = (v1_y * Stride) + v1_x
            workingBuffer[index] = drawCharacter
        else:
            pass
        #exit check (does v1 == v2?)
        if (v1_x == v2_x) and (v1_y == v2_y):
            break
        #error evaluation and "pressure valve" stepping
        error2 = 2 * error
        if (error2 > (-1 * dy)):
            error -= dy
            v1_x += xstep
        if (error2 < dx):
            error += dx
            v1_y += ystep
    #when exit check conditional is passed, break stops the edge drawing loop because
    #the edge has successfully been drawn to the workingBuffer.  Return to main.
    return None
#--------------------------------------------------------------------------------------
