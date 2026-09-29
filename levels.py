import pygame

from models import BreakablePlatform, Door, DoorLink, Enemy, ItemPickup, Room


WIDTH = 960
HEIGHT = 600
FLOOR_Y = 550

START_ROOM = "room_01"
START_SPAWN = "start"


def build_world() -> tuple[dict[str, Room], dict[tuple[str, str], DoorLink]]:
    """Build the memory-map prototype and its temporary directional routes.

    The room geometry follows the eight-room hand-drawn memory sketch.
    Door routing below is intentionally a DEMO only. Routes are directional:
    there is no assumption that walking back through a destination door returns
    to the room the player came from.
    """
    floor = pygame.Rect(0, FLOOR_Y, WIDTH, HEIGHT - FLOOR_Y)

    rooms = {
        # 1. Six-door hub: three doors on each side at three elevations.
        "room_01": Room(
            color=(224, 218, 205),
            platforms=[
                floor,
                pygame.Rect(0, 410, 305, 18),
                pygame.Rect(655, 410, 305, 18),
                pygame.Rect(0, 270, 235, 18),
                pygame.Rect(725, 270, 235, 18),
            ],
            doors=[
                Door("left_bottom", 35, 452),
                Door("right_bottom", 859, 452),
                Door("left_middle", 35, 312),
                Door("right_middle", 859, 312),
                Door("left_top", 35, 172),
                Door("right_top", 859, 172, key_id="gold_key"),
            ],
            spawns={
                "start": (480, 550),
                "return_center": (480, 550),
            },
        ),

        # 2. Simple two-door room.
        "room_02": Room(
            color=(218, 226, 232),
            platforms=[floor],
            doors=[
                Door("left_bottom", 35, 452),
                Door("right_bottom", 859, 452),
            ],
            spawns={
                "left_entry": (140, 550),
                "right_entry": (820, 550),
            },
        ),

        # 3. Lower-left door, upper-left shelf, and raised right-side block.
        "room_03": Room(
            color=(226, 221, 211),
            platforms=[
                floor,
                pygame.Rect(0, 325, 210, 18),
                pygame.Rect(300, 435, 660, 115),
            ],
            doors=[
                Door("left_bottom", 35, 452),
                Door("left_upper", 35, 227),
                Door("right_raised", 859, 337),
            ],
            spawns={
                "bottom_entry": (140, 550),
                "upper_left": (150, 325),
                "raised_right": (800, 435),
            },
        ),

        # 4. Two high doors with a descending staircase and a lower-right door.
        "room_04": Room(
            color=(218, 226, 215),
            platforms=[
                floor,
                pygame.Rect(0, 220, 220, 18),
                pygame.Rect(760, 220, 200, 18),
                pygame.Rect(220, 280, 140, 270),
                pygame.Rect(360, 340, 140, 210),
                pygame.Rect(500, 400, 140, 150),
                pygame.Rect(640, 460, 120, 90),
            ],
            doors=[
                Door("left_upper", 35, 122),
                Door("right_upper", 859, 122),
                Door("right_bottom", 859, 452),
            ],
            spawns={
                "upper_left": (150, 220),
                "upper_right": (810, 220),
                "bottom_right": (800, 550),
            },
        ),

        # 5. Three-door room with floating platforms through the center.
        "room_05": Room(
            color=(232, 225, 211),
            platforms=[
                floor,
                pygame.Rect(0, 280, 210, 18),
                pygame.Rect(300, 420, 220, 18),
                pygame.Rect(390, 340, 220, 18),
                pygame.Rect(690, 300, 170, 18),
            ],
            doors=[
                Door("left_upper", 35, 182),
                Door("left_bottom", 35, 452),
                Door("right_bottom", 859, 452),
            ],
            spawns={
                "upper_left": (150, 280),
                "bottom_left": (140, 550),
                "bottom_right": (820, 550),
            },
        ),

        # 6. Item room. Upper walkway can be drilled through in the center.
        # Entering on the upper level can become a one-way drop to the bottom.
        "room_06": Room(
            color=(220, 217, 228),
            platforms=[
                floor,
                pygame.Rect(0, 220, 400, 18),
                pygame.Rect(560, 220, 400, 18),
            ],
            breakables=[
                BreakablePlatform(pygame.Rect(400, 220, 160, 18), "upper_floor"),
            ],
            doors=[
                Door("left_upper", 35, 122),
                Door("right_upper", 859, 122),
                Door("right_bottom", 859, 452),
            ],
            spawns={
                "upper_left": (150, 220),
                "upper_right": (810, 220),
                "bottom_right": (800, 550),
            },
            items=[
                ItemPickup(pygame.Rect(375, 516, 32, 26), "gun", "gun"),
                ItemPickup(pygame.Rect(475, 514, 32, 28), "drill", "drill"),
                ItemPickup(pygame.Rect(575, 510, 38, 32), "chest", "treasure_chest"),
            ],
        ),

        # 7. Three stacked doors on the left and one door on the high right block.
        "room_07": Room(
            color=(224, 220, 213),
            platforms=[
                floor,
                pygame.Rect(0, 410, 220, 18),
                pygame.Rect(0, 270, 220, 18),
                pygame.Rect(300, 250, 660, 300),
            ],
            doors=[
                Door("left_bottom", 35, 452),
                Door("left_middle", 35, 312),
                Door("left_top", 35, 172),
                Door("right_upper", 859, 152),
            ],
            spawns={
                "left_bottom": (140, 550),
                "left_middle": (150, 410),
                "left_top": (150, 270),
                "upper_right": (800, 250),
            },
            enemies=[
                Enemy(560, 250, -1, 95),
            ],
        ),

        # 8. Stair room with the key at the top-right.
        "room_08": Room(
            color=(214, 224, 226),
            platforms=[
                floor,
                pygame.Rect(260, 480, 120, 70),
                pygame.Rect(380, 410, 120, 140),
                pygame.Rect(500, 340, 120, 210),
                pygame.Rect(620, 270, 120, 280),
                pygame.Rect(740, 200, 220, 350),
            ],
            doors=[
                Door("left_bottom", 35, 452),
            ],
            spawns={
                "bottom_left": (140, 550),
            },
            items=[
                ItemPickup(pygame.Rect(835, 160, 26, 24), "key", "gold_key"),
            ],
        ),
    }

    # Temporary demo routing.
    #
    # IMPORTANT: These links are directional. A reverse link must be declared
    # separately. Several exits intentionally converge on room_01:return_center
    # to demonstrate many-to-one and one-way door behavior.
    links = {
        # Hub -> six main destinations.
        ("room_01", "left_bottom"): DoorLink("room_02", "left_entry"),
        ("room_01", "right_bottom"): DoorLink("room_03", "bottom_entry"),
        ("room_01", "left_middle"): DoorLink("room_04", "bottom_right"),
        ("room_01", "right_middle"): DoorLink("room_05", "bottom_left"),
        ("room_01", "left_top"): DoorLink("room_06", "bottom_right"),
        ("room_01", "right_top"): DoorLink("room_07", "left_bottom"),

        # Room 2 gives access to the key stair room.
        ("room_02", "left_bottom"): DoorLink("room_01", "return_center"),
        ("room_02", "right_bottom"): DoorLink("room_08", "bottom_left"),

        # Room 3 demonstrates entering room 6 from its upper level.
        ("room_03", "left_bottom"): DoorLink("room_01", "return_center"),
        ("room_03", "left_upper"): DoorLink("room_05", "upper_left"),
        ("room_03", "right_raised"): DoorLink("room_06", "upper_left"),

        # Room 4 has intentionally non-symmetric exits.
        ("room_04", "left_upper"): DoorLink("room_01", "return_center"),
        ("room_04", "right_upper"): DoorLink("room_03", "upper_left"),
        ("room_04", "right_bottom"): DoorLink("room_01", "return_center"),

        # Room 5.
        ("room_05", "left_upper"): DoorLink("room_06", "upper_right"),
        ("room_05", "left_bottom"): DoorLink("room_01", "return_center"),
        ("room_05", "right_bottom"): DoorLink("room_04", "bottom_right"),

        # Room 6: upper exits continue elsewhere; lower exit returns to hub.
        ("room_06", "left_upper"): DoorLink("room_03", "upper_left"),
        ("room_06", "right_upper"): DoorLink("room_05", "upper_left"),
        ("room_06", "right_bottom"): DoorLink("room_01", "return_center"),

        # Room 7 is gated from the hub by gold_key.
        ("room_07", "left_bottom"): DoorLink("room_01", "return_center"),
        ("room_07", "left_middle"): DoorLink("room_02", "right_entry"),
        ("room_07", "left_top"): DoorLink("room_04", "upper_left"),
        ("room_07", "right_upper"): DoorLink("room_06", "upper_right"),

        # Key room returns to the common hub spawn instead of back to room 2.
        ("room_08", "left_bottom"): DoorLink("room_01", "return_center"),
    }

    return rooms, links
