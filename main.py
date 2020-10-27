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

def gen_zero_list(array):
    l = []
    for i in range(array.shape[0]):
        m = []
        for e in range(array.shape[1]):
            m.append(0)
        l.append(m)
    return l

def add_heat(heat,x,y,size):
    added_heat = gen_zero_list(heat)
    added_heat[y][x] = size
    new_heat = heat + np.array(added_heat)
    return new_heat

def fire_heat(fire_array):
    parameter_add_heat = 0.5
    fire_pos = []
    y = fire_array.shape[0]
    x = fire_array.shape[1]
    for i in range(y):
        for j in range(x):
            if fire_array[i,j] > 0:
                fire_pos.append((i, j))
    heat = gen_zero_list(fire_array)
    for m in fire_pos:
        #1
        heat[m[0]][m[1]] = 100

        if m[1] + 1 < x:
            if heat[m[0]][m[1]+1] == 0:
                heat[m[0]][m[1]+1] += parameter_add_heat
            else:
                heat[m[0]][m[1] + 1] += parameter_add_heat/2
        if m[1] - 1 >= 0:
            if heat[m[0]][m[1] - 1] == 0:
                heat[m[0]][m[1] - 1] += parameter_add_heat
            else:
                heat[m[0]][m[1] - 1] += parameter_add_heat/2
        #2
        if m[0] + 1 < y:
            if heat[m[0]+1][m[1]] == 0:
                heat[m[0]+1][m[1]] += parameter_add_heat
            else:
                heat[m[0] + 1][m[1]] += parameter_add_heat/2

            if m[1] + 1 < x:
                if heat[m[0]+1][m[1] + 1] == 0:
                    heat[m[0]+1][m[1] + 1] += parameter_add_heat
                else:
                    heat[m[0] + 1][m[1] + 1] += parameter_add_heat/2
            if m[1] - 1 >= 0:
                if heat[m[0]+1][m[1] - 1] == 0:
                    heat[m[0]+1][m[1] - 1] += parameter_add_heat
                else:
                    heat[m[0] + 1][m[1] - 1] += parameter_add_heat/2
        #3
        if m[0] - 1 >= 0:
            if heat[m[0] - 1][m[1]] ==0:
                heat[m[0] - 1][m[1]] += parameter_add_heat
            else:
                heat[m[0] - 1][m[1]] += parameter_add_heat/2

            if m[1] + 1 < x:
                if heat[m[0] - 1][m[1] + 1] == 0 :
                    heat[m[0] - 1][m[1] + 1] += parameter_add_heat
                else:
                    heat[m[0] - 1][m[1] + 1] += parameter_add_heat/2
            if m[1] - 1 >= 0:
                if heat[m[0]-1][m[1] - 1] == 0:
                    heat[m[0]-1][m[1] - 1] += parameter_add_heat
                else:
                    heat[m[0] - 1][m[1] - 1] += parameter_add_heat/2

    heat_array = np.array(heat)
    return heat_array

def gen_fire_pos(heat):
    l = []
    y = heat.shape[0]
    x = heat.shape[1]
    for i in range(y):
        for j in range(x):
            if heat[i,j] > 99:
                l.append((i,j))
    return l

def gen_fire2_pos(fire1):
    l = []
    y = fire1.shape[0]
    x = fire1.shape[1]
    for i in range(y):
        for j in range(x):
            if (fire1[i,j] > 0) and (fire1[i+1,j] > 0) and (fire1[i-1,j] > 0) and (fire1[i,j+1] > 0) and (fire1[i,j-1] > 0):
                l.append((i, j))
    return l




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
fire_array = layer.Layer((0, 0, 0), MAX_X, MAX_Y)
fire2_array = layer.Layer((0, 255, 0), MAX_X, MAX_Y)
# add new layers here
layers.append(heat_array)
layers.append(fire_array)
layers.append(fire2_array)
# do not forget to append the new one here
'''end of layers implement'''

heat_array.data = add_heat(heat_array.data,3,3,20)
fire_array.data[5,5] = 20
fire_array.data[3,7] = 20
fire_array.data[1,1] = 20

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

    #heat_array.data = heat_array.data + 1
    heat_array.data = heat_array.data + fire_heat(fire_array.data)

    new_fire_pos = gen_fire_pos(heat_array.data)
    for i in new_fire_pos:
        fire_array.data[i[0]][i[1]] = 20
        heat_array.data[i[0]][i[1]] = 100

    new_fire2_pos = gen_fire2_pos(fire_array.data)
    for i in new_fire2_pos:
        fire2_array.data[i[0]][i[1]] = 40

    pygame.display.update()
    clock.tick(60)

# close game after crash
pygame.quit()
quit()
