from typing import Union

import renpy.exports as renpy


class Surface():
    """https://www.pygame.org/docs/ref/surface.html"""

    def __init__(
            self,
            size=(0, 0),
            flags=0,
            depth=0,
            masks=None
    ):

        self.size = size
        self.dest = None

    def blit(
            self,
            dest: str,  # img
            area=None,
            special_flags=0
    ):
        self.dest = dest
        return


def mode_ok(size, flags=0, depth=0, display=0):  # -> depth:
    """https://www.pygame.org/docs/ref/display.html#pygame.display.mode_ok"""
    return


def set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0):  # -> Surface:
    """https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode"""
    return  # Surface(size, flags, depth)
