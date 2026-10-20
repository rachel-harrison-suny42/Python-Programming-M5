#this file explicitly allows for the folder name to be called in main.py and the functions from each of the individual module files in this folder to be found within it
# (.) means the current folder
from .inputs import query_number_sides, query_rotation_axis
from .geometry import get_vertices_and_edges, lift_to_four_d, get_rotation_x, get_rotation_y, get_rotation_z
from .renderer import get_terminal_projection, get_new_template, edge_to_buffer