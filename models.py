from dataclasses import dataclass, field

import pygame


DOOR_WIDTH = 66
DOOR_HEIGHT = 98


@dataclass
class Door:
    x: int
    y: int
    target: str
    spawn: tuple[int, int]
    key_id: str | None = None
    flag_id: str | None = None

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, DOOR_WIDTH, DOOR_HEIGHT)


@dataclass
class Pickup:
    rect: pygame.Rect
    item_id: str = ""


@dataclass
class Enemy:
    x: float
    y: float
    facing: int = -1
    cooldown: int = 80
    alive: bool = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - 12), int(self.y - 50), 24, 50)


@dataclass
class Room:
    color: tuple[int, int, int]
    platforms: list[pygame.Rect]
    doors: list[Door]
    enemies: list[Enemy] = field(default_factory=list)
    ammo: list[pygame.Rect] = field(default_factory=list)
    keys: list[Pickup] = field(default_factory=list)
    switches: list[Pickup] = field(default_factory=list)
    title: str = ""
