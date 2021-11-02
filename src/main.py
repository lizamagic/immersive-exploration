import Rhino
import rhinoscriptsyntax as  rs
import random
import math

SHAPE_COUNT = 3

HEIGHT_LOWER = 40
HEIGHT_HIGHER = 70

RECT_RGB = ((88, 178), (56, 56), (76, 76))

CONE_RGB = ((74, 204), (56, 153), (76, 255))

CYL_RGB = ((88, 204), (56, 200), (76, 255))

CIRC_RGB = ((173, 173), (216, 216), (220, 255))

ROAD_SIZE = 15


def color_object(object, color):
    rs.AddMaterialToObject(object)
    index = rs.ObjectMaterialIndex(object)
    rs.MaterialColor(index, color)
    
def gen_color(color_range):
    red = random.randint(color_range[0][0], color_range[0][1])
    green = random.randint(color_range[1][0], color_range[1][1])
    blue = random.randint(color_range[2][0], color_range[2][1])
    
    return rs.CreateColor((red, green, blue))

def place_shape(coordinate, base, height_limits):
    choice = random.randint(0, 3)
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
                          
        color = gen_color(RECT_RGB)
        color_object(shape, color)
    elif (choice == 1):
        shape = rs.AddCone((coordinate[0] + base / 2,\
                            coordinate[1] + base / 2,\
                            coordinate[2] + height), -height, base / 2)
        
        color = gen_color(CONE_RGB)
        color_object(shape, color)
    elif (choice == 2):
        shape = rs.AddCylinder((coordinate[0] + base / 2,\
                                coordinate[1] + base / 2,\
                                coordinate[2] + height), -height, base / 2)
        
        color = gen_color(CYL_RGB)
        color_object(shape, color)
    elif (choice == 3):
        shape = rs.AddSphere((coordinate[0] + base / 2, coordinate[1] + base /2, coordinate[2] + height - base / 2), \
                             base / 2)

        color = gen_color(CIRC_RGB)
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
    
    Color = rs.CreateColor((0, 0, 0))
    h = rs.AddHatch(Side, "Solid")
    rs.ObjectColor(h,Color)
    
    
def place_block(x, y, f_count, s_count, step):
    for i in range(f_count):
        coordinate = rs.CreatePoint(x + i * step, y + 0, 0)
        shapes.append(place_shape(coordinate, step,\
                                  (HEIGHT_LOWER, HEIGHT_HIGHER)))
        coordinate = rs.CreatePoint(x + i * step, y + step * (s_count - 1), 0)
        shapes.append(place_shape(coordinate, step,\
                                  (HEIGHT_LOWER, HEIGHT_HIGHER)))
                                  
    for i in range(1, s_count - 1):
        coordinate = rs.CreatePoint(x + 0, y + i * step, 0)
        shapes.append(place_shape(coordinate, step,\
                                  (HEIGHT_LOWER, HEIGHT_HIGHER)))
        coordinate = rs.CreatePoint(x + step * (f_count - 1), y + i * step, 0)
        shapes.append(place_shape(coordinate, step,\
                                  (HEIGHT_LOWER, HEIGHT_HIGHER)))

All = rs.AllObjects()
rs.DeleteObjects(All)

# Error messages added 11.1.21

obj_size = rs.GetInteger("Please, provide the object size (From 20 to 500).")

if obj_size < 20 or obj_size > 500:
    print("Please check your input parameters.")
    exit()

f_count = rs.GetInteger("Please, provide the first object count (From 2 to 50).")

if f_count < 2 or obj_size > 50:
    print("Please check your input parameters.")
    exit()

s_count = rs.GetInteger("Please, provide the second object count (From 2 to 50).")

if s_count < 2 or obj_size > 50:
    print("Please check your input parameters.")
    exit()

city_width = rs.GetInteger("Please, provide city width (Number of blocks 1-30.")

if city_width < 1 or obj_size > 30:
    print("Please check your input parameters.")
    exit()

city_length = rs.GetInteger("Please, provide city length (Number of blocks 1-30.")

if city_length < 1 or obj_size > 30:
    print("Please check your input parameters.")
    exit()

# Count changed to first and second in order to produce rectangular blocks 11.1.21

shapes = []
x_offset = obj_size * f_count
y_offset = obj_size * s_count

for i in range(city_width):
    start_x = i * x_offset + i * ROAD_SIZE
    for j in range(city_length):
        start_y = j * y_offset + j * ROAD_SIZE
        place_block(start_x, start_y, f_count, s_count, obj_size)
        if (j != city_length - 1):
            place_road((0, start_y + y_offset, 0),
                       (0, start_y + y_offset + ROAD_SIZE, 0), 
                       (city_width * x_offset + (city_width - 1) * ROAD_SIZE, start_y + y_offset + ROAD_SIZE, 0),
                       (city_width * x_offset + (city_width - 1) * ROAD_SIZE, start_y + y_offset, 0))
    if (i != city_width - 1):
        place_road((start_x + x_offset, 0, 0), 
                   (start_x + x_offset + ROAD_SIZE, 0 ,0),
                   (start_x + x_offset + ROAD_SIZE, city_length * y_offset + (city_length - 1) * ROAD_SIZE, 0),
                   (start_x + x_offset, city_length * y_offset + (city_length - 1) * ROAD_SIZE, 0))


rs.ZoomExtents()