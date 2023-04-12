import math
import pygame
import math as m

pygame.init()
# GLOBAL VARIABLES

screen_height = 480 * 1.5
screen_width = 2 * screen_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Raycasting')
clock = pygame.time.Clock()
fps = 30
fov = math.pi /3
half_fov = fov / 2
player_angle = m.pi
casted_rays = 60
step_angle = fov / casted_rays
scale = screen_width * 0.5 / casted_rays
map_size = 32
tile_size = screen_width * 0.5 / map_size
max_depth = int(map_size * tile_size) + 150
player_x = int(screen_height * 0.5)
player_y = int(screen_height * 0.5)
angle_gunSway = 0
# colours
black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)
grey_light = (100, 100, 100)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
# TEXT FONT
font = pygame.font.SysFont('Monospace Regular', 30)
# GUN
gun = pygame.image.load('gun.webp')
gunn = pygame.transform.scale(gun, (700, 350))

map = (
    '################################'
    '#                              #'
    '#                          #   #'
    '#                          #   #'
    '#        #######           #   #'
    '#        #     #           #   #'
    '#        #     #           #   #'
    '#        #     #           #   #'
    '#        #     #           #   #'
    '#                          #   #'
    '#                              #'
    '#                          #   #'
    '#        ##          #     #   #'
    '#                    #     #   #'
    '#                    #     #   #'
    '#                    #         #'
    '#    #######         #     #   #'
    '#                          #   #'
    '#              ##          #   #'
    '#              ##          #   #'
    '#                     #        #'
    '#           ##        #    #   #'
    '#                          #   #'
    '# #                        #   #'
    '# #                        #   #'
    '# #      ###                   #'
    '# #      ###       ##      #   #'
    '# #                        #   #'
    '# #                        #   #'
    '# ######                   #   #'
    '#                              #'
    '################################'

)

# DRAW MAP #
def draw_map():
    for row in range(32):
        for col in range(32):
            square = row * map_size + col
            pygame.draw.rect(screen, grey if map[square] == '#' else (100, 100, 100),(col * tile_size, row * tile_size, tile_size - 1, tile_size - 1))

    pygame.draw.circle(screen, red, (player_x, player_y), 2)
    pygame.draw.line(screen, green, (player_x, player_y),
                     (player_x - m.sin(player_angle - half_fov) * 10,
                      player_y + m.cos(player_angle - half_fov) * 10))
    pygame.draw.line(screen, green, (player_x, player_y),
                     (player_x - m.sin(player_angle + half_fov) * 10,
                      player_y + m.cos(player_angle + half_fov) * 10))

# RAYCASTING ALGORITHM
def cast_rays():
    start_angle = player_angle - half_fov

    for ray in range(casted_rays):
        for depth in range(max_depth):
            target_x = player_x - m.sin(start_angle) * depth
            target_y = player_y + m.cos(start_angle) * depth
            col = int(target_x / tile_size)
            row = int(target_y / tile_size)
            square = row * map_size + col

            if map[square] == '#':
                # pygame.draw.rect(screen,green,(col * tile_size,row * tile_size,tile_size - 1,tile_size -1))
                colour = 255 / (1 + depth * depth * 0.0001)

                depth *= m.cos(player_angle - start_angle)

                wall_height = 22000 / (depth + 0.1)

                if wall_height > screen_height:
                    wall_height = screen_height
                # draw 3d
                pygame.draw.rect(screen, (colour, colour, colour), (screen_height + ray * scale,
                                                                    (screen_height / 2) - wall_height / 2,
                                                                    scale, wall_height))
                break
            pygame.draw.line(screen, green, (player_x, player_y), (target_x, target_y), 1)

        start_angle += step_angle


forward = True
# game loop
run = True
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    col = int(player_x / tile_size)
    row = int(player_y / tile_size)
    square = row * map_size + col

    if map[square] == '#':
        if forward:
            player_x -= (-m.sin(player_angle)) * 4
            player_y -= (m.cos(player_angle)) * 4
        else:
            player_x += (-m.sin(player_angle)) * 4
            player_y += (m.cos(player_angle)) * 4
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player_angle -= 0.1
    if key[pygame.K_d]:
        player_angle += 0.1
    if key[pygame.K_w]:
        forward = True
        player_x += (-m.sin(player_angle)) * 4
        player_y += (m.cos(player_angle)) * 4
    if key[pygame.K_s]:
        forward = False
        player_x -= (-m.sin(player_angle)) * 4
        player_y -= (m.cos(player_angle)) * 4


    # Floor and ceiling on right side
    pygame.draw.rect(screen, grey_light, (screen_width * 0.5, screen_height * 0.5, screen_width, screen_height))
    pygame.draw.rect(screen, grey, (screen_width * 0.5, 0, screen_width, screen_height * 0.5))

    screen.fill(white, (0, 0, screen_width * 0.5, screen_height))

    draw_map()
    cast_rays()
    fps_count = str(int(clock.get_fps()))
    fps_display = font.render(fps_count, True, blue)
    screen.blit(fps_display, (screen_width - 30, 0))
    screen.blit(gunn, (880 + (m.sin(angle_gunSway)) * 10, 400 + (m.sin(angle_gunSway)*m.cos(angle_gunSway)) * 10))
    angle_gunSway += 0.09
    pygame.display.update()
