import pygame
import tile
import layer
import numpy as np

# Constant
SIZE = 64  # pixel length of tile.
MAX_X = 10  # x board size.
MAX_Y = 8  # y board size.


def tile_rect(size):
    return [size * col_num + 1, size * row_num + 1, size - 1, size - 1]


def cal_pos(row, col, size):
    return int(size/2 + size * col), int(size/2 + size * row)


def cal_radius(value, max_size):
    return int(value * max_size / 100)



pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Firerush: fire prototype')
pygame.font.init()
clock = pygame.time.Clock()
crashed = False

tile_list = []
layers = []
heat_array = layer.Layer((255, 0, 0), MAX_X, MAX_Y)
fire_array = layer.Layer((0, 0, 0), MAX_X, MAX_Y)
layers.append(heat_array)
layers.append(fire_array)

fire_array.data[3][4] = 100

for i in range(MAX_Y):
    tile_row = []
    for j in range(MAX_X):
        tile_row.append(tile.simple_tile)
    tile_list.append(tile_row)

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

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
