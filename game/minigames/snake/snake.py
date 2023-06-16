import random
from typing import Optional
import pythonpackages.renpygame as pygame

import renpy.exports as renpy

from pythonpackages.renpygame.event import EventType

width = 500
height = 500

cols = 25
rows = 20


class cube:
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny  # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(
            surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2)
        )
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake:
    body = []
    turns = {}

    def __init__(self, color, pos):
        # pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        if sh.move == 1:  # left
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif sh.move == 0:  # right
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif sh.move == 2:  # up
            self.dirny = -1
            self.dirnx = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif sh.move == 3:  # down
            self.dirny = 1
            self.dirnx = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow(margin: int, screen: pygame.Surface, st: float, at: float):
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


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, rows - 1)
        y = random.randrange(1, rows - 1)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


class SnakeSharedData:
    def __init__(self):
        self.snake_player = snake((255, 0, 0), (10, 10))
        self.snake_player.addCube()
        self.snack = cube(randomSnack(rows, self.snake_player), color=(0, 255, 0))
        self.flag = True
        self.move = 0  # 0 right, 1 left, 2 up, 3 down


sh = SnakeSharedData()


def main():
    # # Initialize a shared data
    global sh

    if not sh:
        sh = SnakeSharedData()

    minigame = pygame.RenpyGameByTimerForDraw(
        update_process=snake_logic,
        event_lambda=game_event,
        delay=0.7,
    )
    minigame.show(show_and_start=True)


def snake_first_step(width: int, height: int, st: float, at: float) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height))
    return screen


def snake_logic(
    cur_screen: renpy.Render,
    st: float,
    next_frame_time: Optional[float],
    current_frame_number: int,
) -> Optional[float]:
    if sh.flag:
        sh.snake_player.move()
        headPos = sh.snake_player.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            print("Score:", len(sh.snake_player.body))
            sh.snake_player.reset((10, 10))

        if sh.snake_player.body[0].pos == sh.snack.pos:
            sh.snake_player.addCube()
            sh.snack = cube(randomSnack(rows, sh.snake_player), color=(0, 255, 0))

        for x in range(len(sh.snake_player.body)):
            if sh.snake_player.body[x].pos in list(
                map(lambda z: z.pos, sh.snake_player.body[x + 1 :])
            ):
                print("Score:", len(sh.snake_player.body))
                sh.snake_player.reset((10, 10))
                break

        redrawWindow(cur_screen)
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
