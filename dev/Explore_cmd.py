#*****************************************************************************
# Arch 441//Medium//Fall 2021//Ericson
#
# Elizaveta Nitenko
# 11.17.21
#
# Immersive Exploration
# This project creates the grid combining the primitive geometrical forms
#
# Source:  
# Source:
# source:
#
#*****************************************************************************
# imported Libraries

import rhinoscriptsyntax as  rs
import random
import math

#
#*****************************************************************************
# Constants:
    
__commandname__ = "ImmersiveExplore"

SHAPE_COUNT = 3

HEIGHT_LOWER = 280
HEIGHT_HIGHER = 400


RECT_RGB = ((88, 178), (56, 56), (76, 76))

CONE_RGB = ((74, 204), (56, 153), (76, 255))

CYL_RGB = ((88, 204), (56, 200), (76, 255))

CIRC_RGB = ((173, 173), (216, 216), (220, 255))

#11.15.21 Torus Added + Color

TOR_RGB = ((50, 52), (10, 26), (45, 255))

ROAD_SIZE = 15

GRADIENTS = (((48, 49, 127), (247, 2, 161)), ((48, 49, 127), (247, 2, 161)))

#
#*****************************************************************************
# Functions:

def color_object(object, color):
    rs.AddMaterialToObject(object)
    index = rs.ObjectMaterialIndex(object)
    rs.MaterialColor(index, color)
    
def gen_color(color_range):
    red = random.randint(color_range[0][0], color_range[0][1])
    green = random.randint(color_range[1][0], color_range[1][1])
    blue = random.randint(color_range[2][0], color_range[2][1])
    
    return rs.CreateColor((red, green, blue))

#Gradient Color Added 11.15.21

def grad_color(gradient, grad_val):
    increments = tuple(map(lambda i, j: i - j, gradient[1], gradient[0]))
    
    return rs.CreateColor((gradient[0][0] + increments[0] * grad_val, \
                           gradient[0][1] + increments[1] * grad_val, \
                           gradient[0][2] + increments[2] * grad_val))

def place_shape(coordinate, base, height_limits, gradient, grad_val):
    choice = random.randint(0, 4)
    height = random.randint(height_limits[0], height_limits[1])
    
    if (choice == 0):
        shape = rs.AddBox((coordinate,\
                          (coordinate[0] + base, coordinate[1], coordinate[2]), \
                          (coordinate[0] + base, coordinate[1] + base, coordinate[2]), \
                          (coordinate[0], coordinate[1] + base, coordinate[2]), \
                          (coordinate[0], coordinate[1], coordinate[2] + height),\
                          (coordinate[0] + base, coordinate[1], coordinate[2] + height), \
                          (coordinate[0] + base, coordinate[1] + base, coordinate[2] + height), \
                          (coordinate[0], coordinate[1] + base, coordinate[2] + height)))
                          
        color = grad_color(gradient, grad_val)
        color_object(shape, color)
    elif (choice == 1):
        shape = rs.AddCone((coordinate[0] + base / 2,\
                            coordinate[1] + base / 2,\
                            coordinate[2] + height), -height, base / 2)
        
        color = grad_color(gradient, grad_val)
        color_object(shape, color)
    elif (choice == 2):
        shape = rs.AddCylinder((coordinate[0] + base / 2,\
                                coordinate[1] + base / 2,\
                                coordinate[2] + height), -height, base / 2)
        
        color = grad_color(gradient, grad_val)
        color_object(shape, color)
    elif (choice == 3):
        shape = rs.AddSphere((coordinate[0] + base / 2, coordinate[1] + base /2, coordinate[2] + height - base / 2), \
                             base / 2)

        color = grad_color(gradient, grad_val)
        color_object(shape, color)
    elif (choice == 4):
        shape = rs.AddTorus((coordinate[0] + base / 2, coordinate[1] + base /2, coordinate[2] + height - base / 2), \
                             base / 2 - base / 6, base / 6)
        color = grad_color(gradient, grad_val)
        color_object(shape, color)
    else:
        raise NotImplemented
            
    return shape

    
def place_road(origin, x, corner, y):
    point1 = rs.AddPoint(origin)
    point2 = rs.AddPoint(x)
    point3 = rs.AddPoint(corner)
    point4 = rs.AddPoint(y)
    
    Side = rs.AddPolyline([point1, point2, point3, point4, point1])

    rs.DeleteObjects([point1, point2, point3, point4])
    
    Color = rs.CreateColor((0, 0, 0))
    h = rs.AddHatch(Side, "Solid")
    rs.ObjectColor(h,Color)
    
    
def place_block(x, y, f_count, s_count, step):
    shapes = []
    
    max_grad = math.sqrt(((f_count - 1) * step) ** 2 + ((s_count - 1) * step) ** 2)
    
    for i in range(f_count):
        coordinate = rs.CreatePoint(x + i * step, y + 0, 0)
        grad_val = math.sqrt((i * step) ** 2 + (0) ** 2) / max_grad
        shapes.append(place_shape(coordinate, step,\
                                  (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], grad_val))
        coordinate = rs.CreatePoint(x + i * step, y + step * (s_count - 1), 0)
        shapes.append(place_shape(coordinate, step,\
                                  (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], grad_val))
                                  
    for i in range(1, s_count - 1):
        coordinate = rs.CreatePoint(x + 0, y + i * step, 0)
        grad_val = math.sqrt((0) ** 2 + (i * step) ** 2) / max_grad
        shapes.append(place_shape(coordinate, step,\
                                  (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], grad_val))
        coordinate = rs.CreatePoint(x + step * (f_count - 1), y + i * step, 0)
        shapes.append(place_shape(coordinate, step,\
                                  (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], grad_val))
                                  
    return shapes
                                  
def place_grid(x, y, f_count, s_count, city_width, city_length, obj_size):
    shapes = []
    x_offset = obj_size * f_count
    y_offset = obj_size * s_count

    for i in range(city_width):
        start_x = x + i * x_offset + i * ROAD_SIZE
        for j in range(city_length):
            start_y = y + j * y_offset + j * ROAD_SIZE
            block = place_block(start_x, start_y, f_count, s_count, obj_size)
            shapes.append(block)
            if (j != city_length - 1):
                place_road((x, start_y + y_offset, 0),
                           (x, start_y + y_offset + ROAD_SIZE, 0), 
                           (x + city_width * x_offset + (city_width - 1) * ROAD_SIZE, start_y + y_offset + ROAD_SIZE, 0),
                           (x + city_width * x_offset + (city_width - 1) * ROAD_SIZE, start_y + y_offset, 0))
        if (i != city_width - 1):
            place_road((start_x + x_offset, y, 0), 
                       (start_x + x_offset + ROAD_SIZE, y ,0),
                       (start_x + x_offset + ROAD_SIZE, y + city_length * y_offset + (city_length - 1) * ROAD_SIZE, 0),
                       (start_x + x_offset, y + city_length * y_offset + (city_length - 1) * ROAD_SIZE, 0))
                                  
def get_integer_loop(phrase, minimum, maximum):
    int = rs.GetInteger(phrase)
    
    while (int < minimum or int > maximum):
        print("Please check your input parameters.")
        int = rs.GetInteger(phrase)
        
    return int

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    #*****************************************************************************
    # MAIN
    # Place all functions to be called inside the Main() function.
    
    # Error messages added 11.1.21
    # Constrains added 11.7.21
    
    ######## Start of Python Script ##############
    ####### Setting up the object size, count, length and width #######
    
    obj_size = get_integer_loop("Please, provide the object size (From 20 to 500).", 20, 500)
    
    f_count = get_integer_loop("Please, provide the first object count (From 2 to 50).", 2, 50)
    
    s_count = get_integer_loop("Please, provide the second object count (From 2 to 50).", 2, 50)
    
    city_width = get_integer_loop("Please, provide city width (Number of blocks 1 - 30.", 1, 30)
    
    city_length = get_integer_loop("Please, provide city length (Number of blocks 1 - 30.", 1, 30)
    
    # Count changed to first and second in order to produce rectangular blocks 11.1.21
    
    print("Now select points that will serve as anchors for individual grids")
    grid_count = get_integer_loop("Please, the grid count (Number of grids 1 - 30).", 1, 30)
    
    # Grid Anchors added 11.7.21
    
    grid_anchors = []
    for i in range(grid_count):
        point = rs.GetPoint("Anchor")
        place_grid(point.X, point.Y, f_count, s_count, city_width, city_length, obj_size)
    
    rs.ZoomExtents()
    
    return 0

# Debug, remove before release!!!
#RunCommand(True)