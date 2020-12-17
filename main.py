import pygame
import tile
import layer
import numpy as np

# Constant
SIZE = 64  # pixel length of tile.
MAX_X = 10  # x board size.
MAX_Y = 8  # y board size.


# return data for drawing rectangle
def tile_rect(size):
    return [size * col_num + 1, size * row_num + 1, size - 1, size - 1]


# calculate real position
def cal_pos(row, col, size):
    return int(size/2 + size * col), int(size/2 + size * row)


# return radius of circle in layer presentation
def cal_radius(value, max_size):
    return int(value * max_size / 100)


#array modify
def shift_left(array):
    a = np.delete(array, 0, axis = 1)
    z = np.zeros((array.shape[0],1))
    return np.append(a,z,axis = 1)

def shift_right(array):
    a = np.delete(array, -1, axis = 1)
    z = np.zeros((array.shape[0],1))
    return np.append(z,a,axis = 1)

def shift_up(array):
    a = np.delete(array, 0, axis=0)
    z = np.zeros((1,array.shape[1]))
    return np.append(a, z, axis=0)

def shift_down(array):
    a = np.delete(array, -1, axis=0)
    z = np.zeros((1,array.shape[1]))
    return np.append(z, a, axis=0)

def spread(value_array,fire_array,add_heat):
    spreader_array = np.clip(fire_array,0,1)
    total =  shift_up(shift_left(spreader_array)) + shift_up(spreader_array) + shift_up(shift_right(spreader_array)) + shift_left(spreader_array) + spreader_array + shift_right(spreader_array) + shift_down(shift_left(spreader_array)) + shift_down(spreader_array) + shift_down(shift_right(spreader_array))
    total = total * add_heat
    return value_array + total

def update_fire_array(value_array,fire_array,start_point,size):
    new_fire = np.where(value_array > start_point, 1,0)
    #total_fire = fire_array + new_fire
    #total_fire = np.clip(total_fire,0,1)*size
    return  new_fire*size



# start pygame
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Firerush: fire prototype')
pygame.font.init()
clock = pygame.time.Clock()
crashed = False

'''start implement layers'''
tile_list = []
layers = []
heat_array = layer.Layer((255, 0, 0), MAX_X, MAX_Y)
fire_lv1_array = layer.Layer((0, 0, 0), MAX_X, MAX_Y)
fire_lv2_array = layer.Layer((0, 0, 0), MAX_X, MAX_Y)
fire_lv3_array = layer.Layer((0, 0, 0), MAX_X, MAX_Y)
wall_array = layer.Layer((0, 255, 0), MAX_X, MAX_Y)


# add new layers here
layers.append(heat_array)
layers.append(fire_lv1_array)
layers.append(fire_lv2_array)
layers.append(fire_lv3_array)
layers.append(wall_array)
# do not forget to append the new one here
'''end of layers implement'''

#initiate
heat_array.data[0,7] = 50
heat_array.data[1,1] = 65
heat_array.data[3,3] = 65
heat_array.data[5,7] = 65

wall_array.data[4,3] = 100
wall_array.data[4,4] = 100
wall_array.data[4,5] = 100
wall_array.data[4,6] = 100
wall_array.data[5,3] = 100
wall_array.data[7,3] = 100
wall_array.data[3,4] = 100
wall_array.data[2,4] = 100
wall_array.data[1,4] = 100




'''start draw tile'''
# test only evey tile is simple_tile. You can change this set of code to draw new tile set.
for i in range(MAX_Y):
    tile_row = []
    for j in range(MAX_X):
        tile_row.append(tile.simple_tile)
    tile_list.append(tile_row)
'''end draw tile'''

for row in enumerate(tile_list):
    row_num = row[0]
    row_content = row[1]
    for element in enumerate(row_content):
        col_num = element[0]
        content = element[1]
        pygame.draw.rect(gameDisplay,
                         content['color'],
                         tile_rect(SIZE),
                         0)
        for l in layers:
            pygame.draw.circle(gameDisplay,
                               l.color,
                               cal_pos(row_num, col_num, SIZE),
                               cal_radius(l.data[row_num][col_num], SIZE/2))

# game loop
fire_lv1_size = 20
fire_lv2_size = 40
fire_lv3_size = 60

fire_lv1_start_point = 30
fire_lv2_start_point = 60
fire_lv3_start_point = 90

heat_decay = -0.1
fire2_add_heat = 0.1
fire3_add_heat = fire2_add_heat + 0.05

while not crashed:

    for row in enumerate(tile_list):
        row_num = row[0]
        row_content = row[1]
        for element in enumerate(row_content):
            col_num = element[0]
            content = element[1]
            pygame.draw.rect(gameDisplay,
                             content['color'],
                             tile_rect(SIZE),
                             0)
            for l in layers:
                pygame.draw.circle(gameDisplay,
                                   l.color,
                                   cal_pos(row_num, col_num, SIZE),
                                   cal_radius(l.data[row_num][col_num], SIZE / 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True


    heat_array.data += heat_decay
    heat_array.data = spread(heat_array.data,fire_lv2_array.data,fire2_add_heat)
    heat_array.data = spread(heat_array.data, fire_lv3_array.data, fire3_add_heat)
    heat_array.data = heat_array.data - wall_array.data
    heat_array.data = np.clip(heat_array.data,0,100)

    fire_lv1_array.data = update_fire_array(heat_array.data,fire_lv1_array.data,fire_lv1_start_point,fire_lv1_size)
    fire_lv2_array.data = update_fire_array(heat_array.data, fire_lv2_array.data, fire_lv2_start_point, fire_lv2_size)
    fire_lv3_array.data = update_fire_array(heat_array.data, fire_lv3_array.data, fire_lv3_start_point, fire_lv3_size)

    pygame.display.update()
    clock.tick(60)

# close game after crash
pygame.quit()
quit()
