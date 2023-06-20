import random
from typing import Optional
import pythonpackages.renpygame as pygame

import renpy.exports as renpy
from pythonpackages.renpygame.display import Surface

from pythonpackages.renpygame.event import EventType


class Snake(pygame.sprite.Sprite):
    def __init__(
        self,
        image: Surface,
        pos: tuple[int, int],
        containers: list[pygame.sprite.AbstractGroup],
    ):
        # TODO: pos * size of the rectangle
        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = image.get_rect(midbottom=pos)

    def update(self):
        self.rect.move_ip(0, 1)  # TODO: to change


class Snak(pygame.sprite.Sprite):
    def __init__(
        self,
        image: Surface,
        pos: tuple[int, int],
        containers: list[pygame.sprite.AbstractGroup],
    ):
        # TODO: pos * size of the rectangle
        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = image.get_rect(midbottom=pos)

    def update(self):
        return


class SnakeSharedData:
    def __init__(self):
        self.flag = True
        self.move = 0  # 0 right, 1 left, 2 up, 3 down
        self.snake_head_position: tuple[int, int] = 0, 0
        self.snake_tail_position = self.snake_head_position
        self.max_position: tuple[int, int] = 0, 0
        self.snack_position: tuple[int, int] = 0, 0
        self.snake_render = pygame.sprite.Group()
        self.snack_render = pygame.sprite.GroupSingle()
        self.all = pygame.sprite.RenderUpdates()
        self._background = None

    @property
    def background(self) -> pygame.Surface:
        return self._background

    @background.setter
    def background(self, value: pygame.Surface):
        self._background = value


sh = SnakeSharedData()


def main():
    # # Initialize a shared data
    global sh

    if not sh:
        sh = SnakeSharedData()

    minigame = pygame.RenpyGameByLoop(
        first_step=snake_first_step,
        update_process=snake_logic,
        event_lambda=game_event,
        delay=0.04,
    )
    minigame.show(show_and_start=True)


def redrawWindow(
    margin: int, screen: pygame.Surface, st: float, at: float
) -> tuple[int, int]:
    # create the background, tile the bgd image
    rectangle = pygame.image.load("rectangle.webp").convert(st, at)
    x_rectangle, y_rectangle = rectangle.get_size()
    sh.background = pygame.Surface(SCREENRECT.size)
    x_background, y_background = SCREENRECT.size
    max_x = x_background // (x_rectangle + margin)
    max_y = y_background // (y_rectangle + margin)
    for x in range(max_x):
        for y in range(max_y):
            screen.blit(
                rectangle, (x * (x_rectangle + margin), y * (y_rectangle + margin))
            )

    screen.blit(sh.background, (0, 0))
    pygame.display.flip()
    return max_x, max_y


def set_new_snack_position():
    """Set a new snack position"""
    snack_x = random.randrange(0, sh.max_position[0])
    snack_y = random.randrange(0, sh.max_position[1])
    sh.snack_position = (snack_x, snack_y)


def snake_first_step(width: int, height: int, st: float, at: float) -> pygame.Surface:
    # Set the display mode
    if store._preferences.fullscreen:
        winstyle = FULLSCREEN
    else:
        winstyle = 0

    bestdepth = pygame.display.mode_ok((0, 0), winstyle, 32)
    screen = pygame.display.set_mode((0, 0), winstyle, bestdepth)

    sh.max_position = redrawWindow(1, screen, st, at)

    # random starting positions, max is sh.max_position
    start_x = random.randrange(0, sh.max_position[0])
    start_y = random.randrange(0, sh.max_position[1])
    sh.snake_head_position = (start_x, start_y)
    sh.snake_tail_position = sh.snake_head_position

    set_new_snack_position()

    Snake.containers = sh.snake_render, sh.all
    Snak.containers = sh.snack_render, sh.all

    sh.snake = [Snake(sh.snake_head_position)]
    sh.snack = Snak(sh.snack_position)

    return screen


def snake_logic(
    cur_screen: renpy.Render,
    st: float,
    next_frame_time: Optional[float],
    current_frame_number: int,
) -> Optional[float]:
    if sh.flag:
        # clear/erase the last drawn sprites
        sh.all.clear(cur_screen, sh.background)

        # update all the sprites
        sh.all.update()

        new_head_position = (0, 0)
        # determines the new position of the head
        if sh.move == 0:  # right
            new_head_position = (
                sh.snake_head_position[0] + 1,
                sh.snake_head_position[1],
            )
        elif sh.move == 1:  # left
            new_head_position = (
                sh.snake_head_position[0] - 1,
                sh.snake_head_position[1],
            )
        elif sh.move == 2:  # up
            new_head_position = (
                sh.snake_head_position[0],
                sh.snake_head_position[1] - 1,
            )
        elif sh.move == 3:  # down
            new_head_position = (
                sh.snake_head_position[0],
                sh.snake_head_position[1] + 1,
            )

        # check if the new position is equal a position of the snake
        for snake in sh.snake:
            if snake.rect.midbottom == new_head_position:
                sh.flag = False
                break

        # check if the new position is equal to the snack position
        if new_head_position == sh.snack_position:
            sh.snake.append(Snake(sh.snake_head_position))
            set_new_snack_position()
            sh.snack.kill()
            sh.snack = Snak(sh.snack_position)
        else:
            sh.snake.append(Snake(sh.snake_head_position))
            # remove the tail
            sh.snake[0].kill()
    else:
        return None


def game_event(ev: EventType, x: int, y: int, st: float):
    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RIGHT:
        if sh.move == 1:
            return
        sh.move = 0
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_LEFT:
        if sh.move == 0:
            return
        sh.move = 1
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_UP:
        if sh.move == 3:
            return
        sh.move = 2
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN:
        if sh.move == 2:
            return
        sh.move = 3
    return
