import pygame

from models import Door, Enemy, Pickup, Room


WIDTH = 960
HEIGHT = 600
FLOOR_Y = 550


def make_rooms() -> dict[str, Room]:
    """Build the current prototype rooms.

    Keep room layout, connections, enemies, pickups, keys and switches here.
    The game loop and player physics belong in main.py.
    """
    floor = pygame.Rect(0, FLOOR_Y, WIDTH, HEIGHT - FLOOR_Y)

    return {
        # Central prototype hub.
        # Extra connector platforms keep every level reachable with the
        # standard jump physics while the final map is still being designed.
        "hub": Room(
            (95, 88, 112),
            [
                floor,
                pygame.Rect(305, 500, 350, 18),
                pygame.Rect(385, 435, 190, 18),
                pygame.Rect(0, 365, 305, 18),
                pygame.Rect(655, 365, 305, 18),
                pygame.Rect(260, 275, 440, 18),
                pygame.Rect(0, 180, 220, 18),
                pygame.Rect(740, 180, 220, 18),
            ],
            [
                Door(35, 82, "crimson", (125, 550)),
                Door(859, 82, "cobalt", (125, 550)),
                Door(35, 267, "forest", (125, 550)),
                Door(859, 267, "amber", (125, 550)),
                Door(35, 452, "violet", (125, 550)),
                Door(859, 452, "slate", (125, 550)),
            ],
            title="STICKMAN ADVENTURE",
        ),
        "crimson": Room(
            (190, 63, 62),
            [
                floor,
                pygame.Rect(280, 440, 175, 18),
                pygame.Rect(555, 335, 145, 18),
                pygame.Rect(350, 245, 180, 18),
                pygame.Rect(0, 220, 205, 18),
                pygame.Rect(755, 220, 205, 18),
            ],
            [
                Door(35, 452, "hub", (865, 550)),
                Door(859, 122, "abyss", (115, 550), key_id="red_key"),
            ],
            enemies=[Enemy(480, 550, -1, 70)],
            ammo=[pygame.Rect(320, 410, 18, 18)],
            keys=[Pickup(pygame.Rect(820, 185, 18, 18), "red_key")],
            title="CRIMSON",
        ),
        "cobalt": Room(
            (50, 100, 170),
            [
                floor,
                pygame.Rect(325, 440, 310, 18),
                pygame.Rect(0, 330, 240, 18),
                pygame.Rect(720, 330, 240, 18),
                pygame.Rect(415, 270, 130, 18),
            ],
            [
                Door(35, 452, "hub", (865, 550)),
                Door(859, 232, "abyss", (115, 550), flag_id="blue_switch"),
            ],
            enemies=[Enemy(760, 550, -1, 105)],
            switches=[Pickup(pygame.Rect(465, 235, 24, 24), "blue_switch")],
            title="COBALT",
        ),
        "forest": Room(
            (66, 137, 91),
            [
                floor,
                pygame.Rect(360, 440, 240, 18),
                pygame.Rect(285, 330, 165, 18),
                pygame.Rect(500, 285, 150, 18),
                pygame.Rect(0, 205, 280, 18),
                pygame.Rect(680, 205, 280, 18),
            ],
            [
                Door(35, 452, "hub", (865, 550)),
                Door(859, 107, "crimson", (120, 550)),
            ],
            enemies=[Enemy(525, 285, -1, 85)],
            ammo=[pygame.Rect(165, 170, 18, 18)],
            title="FOREST",
        ),
        "amber": Room(
            (194, 138, 48),
            [
                floor,
                pygame.Rect(265, 450, 130, 18),
                pygame.Rect(490, 350, 130, 18),
                pygame.Rect(645, 265, 90, 18),
                pygame.Rect(0, 250, 180, 18),
                pygame.Rect(780, 250, 180, 18),
            ],
            [
                Door(35, 452, "hub", (865, 550)),
                Door(859, 152, "vault", (115, 550)),
            ],
            enemies=[Enemy(665, 265, -1, 90), Enemy(530, 350, 1, 125)],
            title="AMBER",
        ),
        "violet": Room(
            (123, 79, 159),
            [
                floor,
                pygame.Rect(315, 440, 150, 18),
                pygame.Rect(505, 325, 110, 18),
                pygame.Rect(395, 215, 165, 18),
                pygame.Rect(0, 300, 250, 18),
                pygame.Rect(710, 300, 250, 18),
            ],
            [
                Door(35, 452, "hub", (865, 550)),
                Door(859, 202, "vault", (115, 550), key_id="violet_key"),
            ],
            keys=[Pickup(pygame.Rect(455, 180, 18, 18), "violet_key")],
            title="VIOLET",
        ),
        "slate": Room(
            (83, 94, 103),
            [
                floor,
                pygame.Rect(300, 430, 150, 18),
                pygame.Rect(520, 430, 150, 18),
                pygame.Rect(405, 315, 150, 18),
                pygame.Rect(0, 235, 230, 18),
                pygame.Rect(730, 235, 230, 18),
            ],
            [
                Door(35, 452, "hub", (865, 550)),
                Door(859, 137, "cobalt", (115, 550)),
            ],
            enemies=[Enemy(475, 550, -1, 100)],
            ammo=[pygame.Rect(455, 280, 18, 18)],
            title="SLATE",
        ),
        "abyss": Room(
            (34, 37, 52),
            [
                floor,
                pygame.Rect(250, 430, 140, 18),
                pygame.Rect(565, 430, 140, 18),
                pygame.Rect(410, 315, 135, 18),
                pygame.Rect(300, 215, 150, 18),
                pygame.Rect(0, 180, 210, 18),
                pygame.Rect(750, 180, 210, 18),
            ],
            [
                Door(35, 452, "crimson", (865, 550)),
                Door(859, 82, "vault", (115, 550)),
            ],
            enemies=[Enemy(455, 315, -1, 65), Enemy(625, 430, 1, 95)],
            title="ABYSS",
        ),
        "vault": Room(
            (40, 44, 46),
            [
                floor,
                pygame.Rect(300, 445, 360, 18),
                pygame.Rect(390, 330, 180, 18),
                pygame.Rect(445, 215, 70, 18),
                pygame.Rect(0, 270, 230, 18),
                pygame.Rect(730, 270, 230, 18),
            ],
            [
                Door(35, 452, "amber", (865, 550)),
                Door(859, 172, "hub", (115, 550)),
            ],
            enemies=[Enemy(350, 445, 1, 75), Enemy(610, 445, -1, 75)],
            ammo=[pygame.Rect(470, 180, 18, 18)],
            title="THE INNER VAULT",
        ),
    }
