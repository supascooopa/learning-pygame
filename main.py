import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BREAKOUT")

# define colors
bg = (99, 89, 133)
# block colors
red_block = (214, 19, 85)
green_block = (192, 226, 24)
blue_block = (48, 227, 223)
#paddle color
paddle_color = (233, 0, 100)
paddle_outline = (100, 100, 100)

# define game variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60


# define brick-wall class
class Wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []
        # define an empty list for an individual block
        block_individual = []
        for row in range(rows):
            # reset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(cols):
                # generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # assign block strength based on row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                # create a list at this point to store the rectangle and color data
                block_individual = [rect, strength]
                # append that individual block to the block row
                block_row.append(block_individual)
            # append the row to the full list of blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign a color based on block strength
                if block[1] == 3:
                    block_color = blue_block
                elif block[1] == 2:
                    block_color = green_block
                elif block[1] == 1:
                    block_color = red_block
                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)


# paddle class
class Paddle:
    def __init__(self):
        # define paddle variables
        self.height = 20
        self.width = int(screen_width / cols)
        self.x_cor = int(screen_width / 2) - (self.width / 2)
        self.y_cor = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x_cor, self.y_cor, self.width, self.height)
        self.direction = 0

    def move_paddle(self):
        # reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)


class Ball:
    def __init__(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

    def draw(self):
        pygame.draw.circle(screen, paddle_color,
                           (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), 3)

    def move(self):

        collision_tresh = 5

        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    # check if the collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_tresh and self.speed_y > 0:
                        self.speed_y *= -1
                    # check if the collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_tresh and self.speed_y < 0:
                        self.speed_y *= -1
                    # check if the collision was from left
                    if abs(self.rect.right - item[0].left) < collision_tresh and self.speed_x > 0:
                        self.speed_x *= -1
                    # check if the collision was from right
                    if abs(self.rect.left - item[0].right) < collision_tresh and self.speed_x < 0:
                        self.speed_x *= -1
                    # apply damage to block
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                        # check if block still exists, in whcih case the wall is not destroyed
                    if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                        wall_destroyed = 0
                item_count += 1
            row_count += 1
        # check if wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1

        # checking for collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # checking for collision with top and bottom
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        # look for collision with paddle
        if self.rect.colliderect(player_paddle):
            # check if colliding from the top
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_tresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        return self.game_over


# create wall
wall = Wall()
wall.create_wall()

# create paddle
player_paddle = Paddle()

ball = Ball(player_paddle.x_cor + (player_paddle.width // 2), player_paddle.y_cor - player_paddle.height)


run = True
while run:
    clock.tick(fps)
    screen.fill(bg)
    wall.draw_wall()

    player_paddle.draw()
    player_paddle.move_paddle()

    ball.draw()
    ball.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
