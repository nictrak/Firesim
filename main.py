import pygame
import tile
import numpy as np

SIZE = 64


def tile_rect(size):
    return [size * col_num + 1, size * row_num + 1, size - 1, size - 1]


def heat_pos(row, col, size):
    return int(size/2 + size * col), int(size/2 + size * row)

def heat_radius(value, max_size):
    return int(value * max_size / 100)


pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Firerush: fire prototype')
pygame.font.init()
clock = pygame.time.Clock()
crashed = False

tile_list = []
heat_array = np.zeros((8, 8))
heat_array[1][1] = 70
for i in range(8):
    tile_row = []
    for j in range(8):
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
        pygame.draw.circle(gameDisplay,
                           (255, 0, 0),
                           heat_pos(row_num, col_num, SIZE),
                           heat_radius(heat_array[row_num][col_num], SIZE/2))

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
