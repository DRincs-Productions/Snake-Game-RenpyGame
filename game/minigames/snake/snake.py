from enum import Enum
import random
from typing import Optional, Union
import pythonpackages.renpygame as pygame

import renpy.exports as renpy
from pythonpackages.renpygame.display import Surface

from pythonpackages.renpygame.event import EventType
from pythonpackages.renpygame.rect import Rect
import renpy.exports as renpy

GAME_SCREEN_SIZE = Rect(0, 0, 640, 480)
MARGIN = 4


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
        self.rect.left = pos[0] * (sh.x_rectangle + MARGIN)
        self.rect.top = pos[1] * (sh.x_rectangle + MARGIN)

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
        life: int = 1,
    ):
        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = self.image.get_rect()
        self.rect.left = pos[0] * (sh.x_rectangle + MARGIN)
        self.rect.top = pos[1] * (sh.x_rectangle + MARGIN)
        self.life = life

    def update(self):
        if self.life != sh.point:
            self.kill()
        return


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class SnakeSharedData:
    def __init__(self):
        self.is_alive = True
        self.current_direction: Direction = Direction.RIGHT
        self.before_direction: Direction = self.current_direction
        self.snake_head_position: tuple[int, int] = 0, 0
        self.max_position: tuple[int, int] = 0, 0
        self.snack_position: tuple[int, int] = 0, 0
        self.snake_render = pygame.sprite.Group()
        self.snack_render = pygame.sprite.GroupSingle()
        self.all = pygame.sprite.RenderUpdates()
        self.point = 0
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

    minigame = pygame.RenpyGameByLoop(
        first_step=snake_first_step,
        update_process=snake_logic,
        event_lambda=game_event,
        delay=0.3,
    )
    minigame.show(show_and_start=True)


def draw_background(
    margin: int, screen: pygame.Surface, st: float, at: float
) -> tuple[int, int]:
    # create the background, tile the bgd image
    rectangle = pygame.image.load("rectangle.webp").convert(st, at)
    sh.x_rectangle, sh.y_rectangle = rectangle.get_size()
    sh.background = pygame.Surface(GAME_SCREEN_SIZE.size)
    x_background, y_background = GAME_SCREEN_SIZE.size
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
    sh.snack_position = (snack_x, snack_y)


def snake_first_step(width: int, height: int, st: float, at: float) -> pygame.Surface:
    bestdepth = pygame.display.mode_ok((0, 0), 0, 32)
    screen = pygame.display.set_mode((0, 0), 0, bestdepth)

    sh.max_position = draw_background(MARGIN, screen, st, at)

    # random starting positions, max is sh.max_position
    start_x = random.randrange(0, sh.max_position[0])
    start_y = random.randrange(0, sh.max_position[1])
    sh.snake_head_position = (start_x, start_y)

    Snake.image = pygame.image.load("snake.webp").convert(st, at)
    Snak.image = pygame.image.load("snak.webp").convert(st, at)

    Snake(sh.snake_head_position, [sh.snake_render, sh.all])

    sh.point = 0

    return screen


def snake_logic(
    cur_screen: pygame.Surface,
    st: float,
    next_frame_time: Optional[float],
    current_frame_number: int,
) -> Optional[float]:
    if sh.point == 0:
        sh.point = 1
        set_new_snack_position()
        Snak(sh.snack_position, [sh.snack_render, sh.all], sh.point)

    if sh.is_alive:
        # clear/erase the last drawn sprites
        sh.all.clear(cur_screen, sh.background)

        # update all the sprites
        sh.all.update()

        # determines the new position of the head
        new_head_position = (0, 0)

        if (
            sh.current_direction == Direction.RIGHT
            and sh.before_direction == Direction.LEFT
        ):
            sh.current_direction = Direction.LEFT
        elif (
            sh.current_direction == Direction.LEFT
            and sh.before_direction == Direction.RIGHT
        ):
            sh.current_direction = Direction.RIGHT
        elif (
            sh.current_direction == Direction.UP
            and sh.before_direction == Direction.DOWN
        ):
            sh.current_direction = Direction.DOWN
        elif (
            sh.current_direction == Direction.DOWN
            and sh.before_direction == Direction.UP
        ):
            sh.current_direction = Direction.UP

        if sh.current_direction == Direction.RIGHT:
            sh.before_direction = Direction.RIGHT
            new_head_position = (
                sh.snake_head_position[0] + 1,
                sh.snake_head_position[1],
            )
        elif sh.current_direction == Direction.LEFT:
            sh.before_direction = Direction.LEFT
            new_head_position = (
                sh.snake_head_position[0] - 1,
                sh.snake_head_position[1],
            )
        elif sh.current_direction == Direction.UP:
            sh.before_direction = Direction.UP
            new_head_position = (
                sh.snake_head_position[0],
                sh.snake_head_position[1] - 1,
            )
        elif sh.current_direction == Direction.DOWN:
            sh.before_direction = Direction.DOWN
            new_head_position = (
                sh.snake_head_position[0],
                sh.snake_head_position[1] + 1,
            )

        if new_head_position[0] < 0:
            new_head_position = (sh.max_position[0] - 1, new_head_position[1])
        elif new_head_position[0] > sh.max_position[0] - 1:
            new_head_position = (0, new_head_position[1])
        elif new_head_position[1] < 0:
            new_head_position = (new_head_position[0], sh.max_position[1] - 1)
        elif new_head_position[1] > sh.max_position[1] - 1:
            new_head_position = (new_head_position[0], 0)

        # # check if the new position is equal a position of the snake
        # for snake in sh.snake:
        #     if snake.rect.midbottom == new_head_position:
        #         sh.flag = False
        #         break

        # create a new snake head and add it to the sprite groups
        Snake(new_head_position, [sh.snake_render, sh.all], life=sh.point)
        sh.snake_head_position = new_head_position

        # check if the new position is equal to the snack position
        if sh.snake_head_position == sh.snack_position:
            sh.point += 1
            set_new_snack_position()
            Snak(sh.snack_position, [sh.snack_render, sh.all], sh.point)

        # draw the scene
        dirty = sh.all.draw(cur_screen)
        pygame.display.update(dirty)

        return next_frame_time
    else:
        return None


def game_event(ev: EventType, x: int, y: int, st: float):
    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RIGHT:
        sh.current_direction = Direction.RIGHT
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_LEFT:
        sh.current_direction = Direction.LEFT
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_UP:
        sh.current_direction = Direction.UP
    elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN:
        sh.current_direction = Direction.DOWN
    return
