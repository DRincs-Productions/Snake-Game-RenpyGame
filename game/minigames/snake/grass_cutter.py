import random
from enum import Enum
from typing import Optional, Union

import renpy.exports as renpy

import pythonpackages.renpygame as pygame
from pythonpackages.renpygame.display import Surface
from pythonpackages.renpygame.event import EventType

game_screen_size: tuple[int, int] = (0, 0)
game_margin = 0


class Lawnmower(pygame.sprite.Sprite):
    image: Surface
    pos: tuple[int, int]

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
        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = self.image.get_rect()
        self.rect.left = pos[0] * (sh.x_rectangle + game_margin)
        self.rect.top = pos[1] * (sh.x_rectangle + game_margin)
        self.pos = pos
        self.life = 1

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()


class Ground(pygame.sprite.Sprite):
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
        pygame.sprite.Sprite.__init__(self, containers)
        self.rect = self.image.get_rect()
        self.rect.left = pos[0] * (sh.x_rectangle + game_margin)
        self.rect.top = pos[1] * (sh.x_rectangle + game_margin)
        self.pos = pos


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3


class SnakeSharedData:
    def __init__(self):
        self.current_direction: Direction = Direction.RIGHT
        self.before_direction: Direction = self.current_direction
        self.snake_head_position: tuple[int, int] = 0, 0
        self.max_position: tuple[int, int] = 0, 0
        self.grass_list = pygame.sprite.GroupSingle()
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
    def grass(self) -> Ground:
        return self._grass

    @grass.setter
    def grass(self, value: Ground):
        self._grass = value


sh = SnakeSharedData()


def main(size: tuple[int, int], margin=0) -> int:
    global game_screen_size
    game_screen_size = size
    global game_margin
    game_margin = margin
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

    return sh.point


def draw_background(
    margin: int, screen: pygame.Surface, st: float, at: float
) -> tuple[int, int]:
    # create the background, tile the bgd image
    rectangle = pygame.image.load("grass.webp").convert(st, at)
    sh.x_rectangle, sh.y_rectangle = rectangle.get_size()
    sh.background = pygame.Surface(game_screen_size)
    x_background, y_background = game_screen_size
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


def snake_first_step(width: int, height: int, st: float, at: float) -> pygame.Surface:
    bestdepth = pygame.display.mode_ok((0, 0), 0, 32)
    screen = pygame.display.set_mode((0, 0), 0, bestdepth)

    sh.max_position = draw_background(game_margin, screen, st, at)

    # random starting positions, max is sh.max_position
    start_x = random.randrange(0, sh.max_position[0])
    start_y = random.randrange(0, sh.max_position[1])
    sh.snake_head_position = (start_x, start_y)

    Lawnmower.image = pygame.image.load("lawnmower.webp").convert(st, at)
    Ground.image = pygame.image.load("ground.webp").convert(st, at)

    Lawnmower(sh.snake_head_position, [sh.all])

    sh.point = 0

    return screen


def snake_logic(
    cur_screen: pygame.Surface,
    st: float,
    next_frame_time: Optional[float],
    current_frame_number: int,
) -> Optional[float]:
    if sh.point != (sh.max_position[0] * sh.max_position[1]) - 1:
        # clear/erase the last drawn sprites
        sh.all.clear(cur_screen, sh.background)

        # update all the sprites
        sh.all.update()

        # determines the new position of the head
        new_head_position = (0, 0)

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

        # check if the new position is equal a position of the snake
        add_snack = True
        for item in sh.all.sprites():
            print(sh.snake_head_position, item.pos)
            if sh.snake_head_position == item.pos:
                add_snack = False
        if add_snack:
            Ground(sh.snake_head_position, [sh.grass_list, sh.all])
            sh.point += 1

        # create a new snake head and add it to the sprite groups
        Lawnmower(new_head_position, [sh.all])
        sh.snake_head_position = new_head_position

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
