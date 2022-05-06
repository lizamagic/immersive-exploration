import rhinoscriptsyntax as rs
import random
import math
import Rhino
import scriptcontext


SHAPE_COUNT = 3

HEIGHT_LOWER = 40
HEIGHT_HIGHER = 80


RECT_RGB = ((88, 178), (56, 56), (76, 76))

CONE_RGB = ((74, 204), (56, 153), (76, 255))

CYL_RGB = ((88, 204), (56, 200), (76, 255))

CIRC_RGB = ((173, 173), (216, 216), (220, 255))

#11.15.21 Torus Added + Color

TOR_RGB = ((50, 52), (10, 26), (45, 255))

#ROAD_SIZE = 15

GRADIENTS = (((48, 49, 127), (247, 2, 161)), ((48, 49, 127), (247, 2, 161)))

#
#*****************************************************************************
#Functions:


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

def place_shape(coordinate, base, height_limits, gradient, restricted=False):
    if restricted:
        choice = random.randint(0, 2)
    else:
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
    elif (choice == 1):
        shape = rs.AddCone((coordinate[0] + base / 2,\
                            coordinate[1] + base / 2,\
                            coordinate[2] + height), -height, base / 2)
    elif (choice == 2):
        shape = rs.AddCylinder((coordinate[0] + base / 2,\
                                coordinate[1] + base / 2,\
                                coordinate[2] + height), -height, base / 2)
    elif (choice == 3):
        shape = rs.AddSphere((coordinate[0] + base / 2, coordinate[1] + base /2, coordinate[2] + height - base / 2), \
                             base / 2)
    elif (choice == 4):
        shape = rs.AddTorus((coordinate[0] + base / 2, coordinate[1] + base /2, coordinate[2] + height  - base / 2), \
                             base / 2 - base / 6, base / 6)
    else:
        raise NotImplemented
            
    return shape
    
    
def place_block(x, y, z, f_count, s_count, step, grad_val, restricted=False):
    shapes = []
    
    shape_step = step / 2
    
    walls = []
    anchor = rs.CreatePoint(x - 1, y - 1, z)
    box = rs.AddBox((anchor,
              (anchor[0] + shape_step, anchor[1], anchor[2]),
              (anchor[0] + shape_step, anchor[1] + (s_count + 1) * shape_step + 2, anchor[2]),
              (anchor[0], anchor[1] + (s_count + 1) * shape_step + 2, anchor[2]),
              (anchor[0], anchor[1], anchor[2] + HEIGHT_HIGHER),
              (anchor[0] + shape_step, anchor[1], anchor[2] + HEIGHT_HIGHER),
              (anchor[0] + shape_step, anchor[1] + (s_count + 1) * shape_step + 2, anchor[2] + HEIGHT_HIGHER),
              (anchor[0], anchor[1] + (s_count + 1) * shape_step + 2, anchor[2] + HEIGHT_HIGHER)))
    walls.append(box)
              
    anchor = rs.CreatePoint(x + f_count * shape_step + 1, y - 1, z)
    box = rs.AddBox((anchor,
              (anchor[0] + shape_step, anchor[1], anchor[2]),
              (anchor[0] + shape_step, anchor[1] + (s_count + 1) * shape_step + 2, anchor[2]),
              (anchor[0], anchor[1] + (s_count + 1) * shape_step + 2, anchor[2]),
              (anchor[0], anchor[1], anchor[2] + HEIGHT_HIGHER),
              (anchor[0] + shape_step, anchor[1], anchor[2] + HEIGHT_HIGHER),
              (anchor[0] + shape_step, anchor[1] + (s_count + 1) * shape_step + 2, anchor[2] + HEIGHT_HIGHER),
              (anchor[0], anchor[1] + (s_count + 1) * shape_step + 2, anchor[2] + HEIGHT_HIGHER)))
    walls.append(box)
    
    anchor = rs.CreatePoint(x + f_count * shape_step + 1, y - 1, z)
    box = rs.AddBox((anchor,
              (anchor[0] - shape_step * (f_count + 0), anchor[1], anchor[2]),
              (anchor[0] - shape_step * (f_count + 0), anchor[1] + shape_step, anchor[2]),
              (anchor[0], anchor[1] + shape_step, anchor[2]),
              (anchor[0], anchor[1], anchor[2] + HEIGHT_HIGHER),
              (anchor[0] - shape_step * (f_count + 0), anchor[1], anchor[2] + HEIGHT_HIGHER),
              (anchor[0] - shape_step * (f_count + 0
              ), anchor[1] + + shape_step, anchor[2] + HEIGHT_HIGHER),
              (anchor[0], anchor[1] + + shape_step, anchor[2] + HEIGHT_HIGHER)))
    walls.append(box)
    
    anchor = rs.CreatePoint(x + f_count * shape_step + 1, y + s_count * shape_step + 1 , z)
    box = rs.AddBox((anchor,
              (anchor[0] - shape_step * (f_count + 0), anchor[1], anchor[2]),
              (anchor[0] - shape_step * (f_count + 0), anchor[1] + shape_step, anchor[2]),
              (anchor[0], anchor[1] + shape_step, anchor[2]),
              (anchor[0], anchor[1], anchor[2] + HEIGHT_HIGHER),
              (anchor[0] - shape_step * (f_count + 0), anchor[1], anchor[2] + HEIGHT_HIGHER),
              (anchor[0] - shape_step * (f_count + 0
              ), anchor[1] + + shape_step, anchor[2] + HEIGHT_HIGHER),
              (anchor[0], anchor[1] + + shape_step, anchor[2] + HEIGHT_HIGHER)))
    walls.append(box)
    walls = rs.BooleanUnion(walls, True)
           
    diffed_walls = None
    
    while (diffed_walls == None):
        rs.DeleteObjects(shapes)
        shapes = []
        
        for i in range(f_count):
            coordinate = rs.CreatePoint(x + i * shape_step, y + 0, z)
            shapes.append(place_shape(coordinate, step,\
                                      (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], restricted))
            coordinate = rs.CreatePoint(x + i * shape_step, y + shape_step * (s_count - 1), z)
            shapes.append(place_shape(coordinate, step,\
                                      (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], restricted))
                                      
            coordinate = rs.CreatePoint(x + i * shape_step, y - 1.9 * shape_step, z)
            shapes.append(place_shape(coordinate, step,\
                                      (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], restricted))
            coordinate = rs.CreatePoint(x + i * shape_step, y + shape_step * (s_count - 1) + 1.9 * shape_step, z)
            shapes.append(place_shape(coordinate, step,\
                                      (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], restricted))
                                      
        for i in range(1, s_count - 1):
            coordinate = rs.CreatePoint(x + 0, y + i * shape_step, z)
            shapes.append(place_shape(coordinate, step,\
                                      (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], restricted))
            coordinate = rs.CreatePoint(x + shape_step * (f_count - 1), y + i * shape_step, z)
            shapes.append(place_shape(coordinate, step,\
                                      (HEIGHT_LOWER, HEIGHT_HIGHER), GRADIENTS[0], restricted))
                                    
                                    
        diffed_walls = rs.BooleanDifference(walls, shapes, True)

                                  
    color = grad_color(GRADIENTS[0], grad_val)
    color_object(diffed_walls, color)
    
    anchor = rs.CreatePoint(x, y, z)
    floor = rs.AddBox(((anchor[0], anchor[1], anchor[2]),
              (anchor[0] + shape_step * (f_count + 1), anchor[1], anchor[2] - 0.1),
              (anchor[0] + shape_step * (f_count + 1), anchor[1] + shape_step * (s_count + 1), anchor[2] - 0.1),
              (anchor[0], anchor[1] + shape_step * (s_count + 1), anchor[2] - 0.1),
              (anchor[0], anchor[1], anchor[2] - 1),
              (anchor[0] + shape_step * (f_count + 1), anchor[1], anchor[2] - 1),
              (anchor[0] + shape_step * (f_count + 1), anchor[1] + shape_step * (s_count + 1), anchor[2] - 1),
              (anchor[0], anchor[1] + shape_step * (s_count + 1), anchor[2] - 1)))
              
    anchor = rs.CreatePoint(x + shape_step * (f_count + 1) / 2, y + shape_step * (s_count + 1) / 2, z)
     
    hole_size = 40
    hole = rs.AddBox(((anchor[0] - hole_size, anchor[1] - hole_size, anchor[2] - hole_size),
              (anchor[0] + hole_size, anchor[1] - hole_size, anchor[2] - hole_size),
              (anchor[0] + hole_size, anchor[1] + hole_size, anchor[2] - hole_size),
              (anchor[0] - hole_size, anchor[1] + hole_size, anchor[2] - hole_size),
              (anchor[0] - hole_size, anchor[1] - hole_size, anchor[2] + hole_size),
              (anchor[0] + hole_size, anchor[1] - hole_size, anchor[2] + hole_size),
              (anchor[0] + hole_size, anchor[1] + hole_size, anchor[2] + hole_size),
              (anchor[0] - hole_size, anchor[1] + hole_size, anchor[2] + hole_size)))
              
    diffed_floor = rs.BooleanDifference(floor, hole, True)
                                  
    return (diffed_walls, diffed_floor)

def color_object(object, color):
    rs.AddMaterialToObject(object)
    index = rs.ObjectMaterialIndex(object)
    rs.MaterialColor(index, color)
    rs.ObjectColor(object, color)

def get_integer_loop(phrase, minimum, maximum):
    int = rs.GetInteger(phrase)
    
    while (int < minimum or int > maximum):
        print("Please check your input parameters.")
        int = rs.GetInteger(phrase)
        
    return int

__commandname__ = "ImmersiveExploration"

def RunCommand( is_interactive ):
    #*****************************************************************************
    #MAIN
    #Place all functions to be called inside the Main() function.
    
    All = rs.AllObjects()
    rs.DeleteObjects(All)
    
    # Error messages added 11.1.21
    # Constrains added 11.7.21
    
    ######## Start of Python Script ##############
    ####### Setting up the object size, count, length and width #######
    
    obj_size = get_integer_loop("Please, provide the object size (From 20 to 500).", 20, 500)
    
    f_count = get_integer_loop("Please, provide the first object count (From 2 to 50).", 2, 50)
    
    s_count = get_integer_loop("Please, provide the second object count (From 2 to 50).", 2, 50)
    
    # Count changed to first and second in order to produce rectangular blocks 11.1.21
    
    #print("Now select points that will serve as anchors for individual grids")
    #grid_count = get_integer_loop("Please, the grid count (Number of grids 1 - 30).", 1, 30)
    
    tower_height = get_integer_loop("Enter height. (1 - 30)", 1, 30)
    
    # Grid Anchors added 11.7.21
    
    point = rs.GetPoint("Anchor")
    
    max_grad = tower_height
    
    for i in range(tower_height):
        place_block(point.X, point.Y, HEIGHT_HIGHER * i, f_count, s_count, obj_size, i / max_grad)
    
    #rs.Command("Contour")
    
    #rs.Command("Rotate")
    
    #rs.Command("Shear")
    
    #rs.Command("Make2D")
    
    rs.ZoomExtents()
    #rs.ViewCamera(camera_location=rs.CreatePoint(point.X + f_count * (obj_size) / 4, 
    #                                             point.Y + s_count * (obj_size) / 4,
    #                                             HEIGHT_HIGHER / 2))

    return 0
