import random
from typing import Optional, Union
import pythonpackages.renpygame as pygame

import renpy.exports as renpy
from pythonpackages.renpygame.display import Surface

from pythonpackages.renpygame.event import EventType
from pythonpackages.renpygame.rect import Rect
import renpy.exports as renpy
import renpy.store as store

SCREENRECT = Rect(0, 0, 640, 480)


class Snake(pygame.sprite.Sprite):
    image: Surface

    def __init__(
        self,
        pos: tuple[int, int],
        containers: list[
            Union[
                pygame.sprite.AbstractGroup,
                pygame.sprite.Group,
                pygame.sprite.RenderUpdates,
                pygame.sprite.GroupSingle,
            ]
        ],
        life: int = 1,
    ):
        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = self.image.get_rect()
        self.life = life
        self.rect.left = pos[0] * (sh.x_rectangle + sh.margin)
        self.rect.top = pos[1] * (sh.x_rectangle + sh.margin)
        print(self.rect.left, self.rect.top)

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()


class Snak(pygame.sprite.Sprite):
    image: Surface

    def __init__(
        self,
        pos: tuple[int, int],
        containers: list[
            Union[
                pygame.sprite.AbstractGroup,
                pygame.sprite.Group,
                pygame.sprite.RenderUpdates,
                pygame.sprite.GroupSingle,
            ]
        ],
    ):
        # TODO: pos * size of the rectangle
        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        return


class SnakeSharedData:
    def __init__(self):
        self.flag = True
        self.move = 0  # 0 right, 1 left, 2 up, 3 down
        self.before_move = self.move
        self.snake_head_position: tuple[int, int] = 0, 0
        self.max_position: tuple[int, int] = 0, 0
        self.snack_position: tuple[int, int] = 0, 0
        self.snake_render = pygame.sprite.Group()
        self.snack_render = pygame.sprite.GroupSingle()
        self.all = pygame.sprite.RenderUpdates()
        self.point = 1
        self.margin = 3
        self.x_rectangle = 0
        self.y_rectangle = 0

    @property
    def background(self) -> pygame.Surface:
        return self._background

    @background.setter
    def background(self, value: pygame.Surface):
        self._background = value

    @property
    def snack(self) -> Snak:
        return self._snack

    @snack.setter
    def snack(self, value: Snak):
        self._snack = value


sh = SnakeSharedData()


def main():
    # # Initialize a shared data
    global sh

    if not sh:
        sh = SnakeSharedData()

    minigame = pygame.RenpyGameByTimer(
        first_step=snake_first_step,
        update_process=snake_logic,
        event_lambda=game_event,
        delay=0.5,
    )
    minigame.show(show_and_start=True)


def redrawWindow(
    margin: int, screen: pygame.Surface, st: float, at: float
) -> tuple[int, int]:
    # create the background, tile the bgd image
    rectangle = pygame.image.load("rectangle.webp").convert(st, at)
    sh.x_rectangle, sh.y_rectangle = rectangle.get_size()
    sh.background = pygame.Surface(SCREENRECT.size)
    x_background, y_background = SCREENRECT.size
    max_x = int(x_background // (sh.x_rectangle + margin))
    max_y = int(y_background // (sh.y_rectangle + margin))
    for x in range(max_x):
        for y in range(max_y):
            sh.background.blit(
                rectangle,
                (x * (sh.x_rectangle + margin), y * (sh.y_rectangle + margin)),
            )
    sh.max_position = max_x, max_y

    screen.blit(sh.background, (0, 0))
    pygame.display.flip()
    return max_x, max_y


def set_new_snack_position():
    """Set a new snack position"""
    snack_x = random.randrange(0, sh.max_position[0])
    snack_y = random.randrange(0, sh.max_position[1])
    print(snack_x, snack_y)
    sh.snack_position = (snack_x, snack_y)


def snake_first_step(width: int, height: int, st: float, at: float) -> pygame.Surface:
    # Set the display mode
    if store._preferences.fullscreen:
        winstyle = FULLSCREEN
    else:
        winstyle = 0

    bestdepth = pygame.display.mode_ok((0, 0), winstyle, 32)
    screen = pygame.display.set_mode((0, 0), winstyle, bestdepth)

    sh.max_position = redrawWindow(sh.margin, screen, st, at)

    # random starting positions, max is sh.max_position
    start_x = random.randrange(0, sh.max_position[0])
    start_y = random.randrange(0, sh.max_position[1])
    sh.snake_head_position = (start_x, start_y)

    set_new_snack_position()

    Snake.image = pygame.image.load("snake.webp").convert(st, at)
    Snak.image = pygame.image.load("snak.webp").convert(st, at)

    Snake(sh.snake_head_position, [sh.snake_render, sh.all])
    sh.snack = Snak((0, 0), [sh.snack_render, sh.all])

    return screen


def snake_logic(
    cur_screen: pygame.Surface,
    st: float,
    next_frame_time: Optional[float],
    current_frame_number: int,
) -> Optional[float]:
    if sh.flag:
        # clear/erase the last drawn sprites
        sh.all.clear(cur_screen, sh.background)

        # update all the sprites
        sh.all.update()

        # determines the new position of the head
        new_head_position = (0, 0)

        if sh.move == 0 and sh.before_move == 1:
            sh.move = 1
        elif sh.move == 1 and sh.before_move == 0:
            sh.move = 0
        elif sh.move == 2 and sh.before_move == 3:
            sh.move = 3
        elif sh.move == 3 and sh.before_move == 2:
            sh.move = 2

        if sh.move == 0:  # right
            sh.before_move = 0
            new_head_position = (
                sh.snake_head_position[0] + 1,
                sh.snake_head_position[1],
            )
        elif sh.move == 1:  # left
            sh.before_move = 1
            new_head_position = (
                sh.snake_head_position[0] - 1,
                sh.snake_head_position[1],
            )
        elif sh.move == 2:  # up
            sh.before_move = 2
            new_head_position = (
                sh.snake_head_position[0],
                sh.snake_head_position[1] - 1,
            )
        elif sh.move == 3:  # down
            sh.before_move = 3
            new_head_position = (
                sh.snake_head_position[0],
                sh.snake_head_position[1] + 1,
            )

        if new_head_position[0] < 0:
            new_head_position = (sh.max_position[0], new_head_position[1])
        elif new_head_position[0] > sh.max_position[0]:
            new_head_position = (0, new_head_position[1])
        elif new_head_position[1] < 0:
            new_head_position = (new_head_position[0], sh.max_position[1])
        elif new_head_position[1] > sh.max_position[1]:
            new_head_position = (new_head_position[0], 0)

        # # check if the new position is equal a position of the snake
        # for snake in sh.snake:
        #     if snake.rect.midbottom == new_head_position:
        #         sh.flag = False
        #         break

        # check if the new position is equal to the snack position
        # if new_head_position == sh.snack_position:
        #     Snake(sh.snake_head_position, [sh.snake_render, sh.all])
        #     set_new_snack_position()
        #     sh.snack.kill()
        #     sh.snack = Snak(sh.snack_position, [sh.snack_render, sh.all])
        # else:
        Snake(new_head_position, [sh.snake_render, sh.all], life=sh.point)
        sh.snake_head_position = new_head_position

        # draw the scene
        dirty = sh.all.draw(cur_screen)
        pygame.display.update(dirty)

        return next_frame_time
    else:
        return None


def game_event(ev: EventType, x: int, y: int, st: float):
    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RIGHT:
        sh.move = 0
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_LEFT:
        sh.move = 1
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_UP:
        sh.move = 2
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN:
        sh.move = 3
    return
