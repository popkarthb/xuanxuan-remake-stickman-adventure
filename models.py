from dataclasses import dataclass, field

import pygame


DOOR_WIDTH = 66
DOOR_HEIGHT = 98


@dataclass
class Door:
    """A physical door placed in a room.

    Door routing is intentionally NOT stored on the door itself. Each door has
    an ID and levels.py defines a directional route for that ID. This allows
    one-way routes and many doors to lead to the same destination.
    """

    door_id: str
    x: int
    y: int
    key_id: str | None = None
    flag_id: str | None = None

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, DOOR_WIDTH, DOOR_HEIGHT)


@dataclass(frozen=True)
class DoorLink:
    target_room: str
    target_spawn: str


@dataclass
class ItemPickup:
    rect: pygame.Rect
    kind: str
    item_id: str


@dataclass
class BreakablePlatform:
    rect: pygame.Rect
    break_id: str


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
    spawns: dict[str, tuple[int, int]]
    enemies: list[Enemy] = field(default_factory=list)
    items: list[ItemPickup] = field(default_factory=list)
    breakables: list[BreakablePlatform] = field(default_factory=list)
    title: str = ""

    def solid_rects(self) -> list[pygame.Rect]:
        return self.platforms + [platform.rect for platform in self.breakables]
