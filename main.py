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
# add new layers here
layers.append(heat_array)
layers.append(fire_array)
# do not forget to append the new one here
'''end of layers implement'''

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    pygame.display.update()
    clock.tick(60)

# close game after crash
pygame.quit()
quit()
