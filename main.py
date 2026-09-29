import math
import sys
from dataclasses import dataclass, field

import pygame


WIDTH, HEIGHT = 960, 600
FPS = 60
GRAVITY = 0.75
MOVE_SPEED = 4.5
JUMP_SPEED = -13.5
WHITE = (250, 250, 247)
BLACK = (17, 17, 20)


@dataclass
class Door:
    x: int
    y: int
    target: str
    spawn: tuple[int, int]
    label: str = ""
    key_id: str | None = None
    flag_id: str | None = None

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 66, 98)


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
    def rect(self):
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


def make_rooms():
    floor = pygame.Rect(0, 550, WIDTH, 50)
    return {
        # Screen 1: the central hub connects to six regions.
        "hub": Room(
            (95, 88, 112),
            [floor, pygame.Rect(0, 365, 305, 18), pygame.Rect(655, 365, 305, 18),
             pygame.Rect(0, 180, 220, 18), pygame.Rect(740, 180, 220, 18),
             pygame.Rect(305, 500, 350, 18), pygame.Rect(385, 445, 190, 18)],
            [Door(35, 82, "crimson", (125, 550), "I"), Door(859, 82, "cobalt", (125, 550), "II"),
             Door(35, 267, "forest", (125, 550), "III"), Door(859, 267, "amber", (125, 550), "IV"),
             Door(35, 452, "violet", (125, 550), "V"), Door(859, 452, "slate", (125, 550), "VI")],
            title="STICKMAN ADVENTURE"
        ),
        # Screen 2
        "crimson": Room(
            (190, 63, 62),
            [floor, pygame.Rect(0, 220, 205, 18), pygame.Rect(755, 220, 205, 18),
             pygame.Rect(280, 400, 175, 18), pygame.Rect(555, 315, 145, 18)],
            [Door(35, 452, "hub", (865, 550), "HUB"),
             Door(859, 122, "abyss", (115, 550), "KEY", key_id="red_key")],
            enemies=[Enemy(480, 550, -1, 70)],
            ammo=[pygame.Rect(320, 370, 18, 18)],
            keys=[Pickup(pygame.Rect(820, 185, 18, 18), "red_key")],
            title="CRIMSON"
        ),
        # Screen 3
        "cobalt": Room(
            (50, 100, 170),
            [floor, pygame.Rect(0, 330, 240, 18), pygame.Rect(720, 330, 240, 18),
             pygame.Rect(325, 440, 310, 18), pygame.Rect(415, 270, 130, 18)],
            [Door(35, 452, "hub", (865, 550), "HUB"),
             Door(859, 232, "abyss", (115, 550), "SW", flag_id="blue_switch")],
            enemies=[Enemy(760, 550, -1, 105)],
            switches=[Pickup(pygame.Rect(465, 235, 24, 24), "blue_switch")],
            title="COBALT"
        ),
        # Screen 4
        "forest": Room(
            (66, 137, 91),
            [floor, pygame.Rect(0, 205, 280, 18), pygame.Rect(680, 205, 280, 18),
             pygame.Rect(360, 385, 240, 18)],
            [Door(35, 452, "hub", (865, 550), "HUB"),
             Door(859, 107, "crimson", (120, 550), "LOOP")],
            enemies=[Enemy(525, 385, -1, 85)],
            ammo=[pygame.Rect(165, 170, 18, 18)],
            title="FOREST"
        ),
        # Screen 5
        "amber": Room(
            (194, 138, 48),
            [floor, pygame.Rect(0, 250, 180, 18), pygame.Rect(780, 250, 180, 18),
             pygame.Rect(265, 450, 130, 18), pygame.Rect(490, 350, 130, 18),
             pygame.Rect(645, 265, 90, 18)],
            [Door(35, 452, "hub", (865, 550), "HUB"),
             Door(859, 152, "vault", (115, 550), "DEEP")],
            enemies=[Enemy(665, 265, -1, 90), Enemy(530, 350, 1, 125)],
            title="AMBER"
        ),
        # Screen 6
        "violet": Room(
            (123, 79, 159),
            [floor, pygame.Rect(0, 300, 250, 18), pygame.Rect(710, 300, 250, 18),
             pygame.Rect(315, 425, 150, 18), pygame.Rect(505, 320, 110, 18),
             pygame.Rect(395, 205, 165, 18)],
            [Door(35, 452, "hub", (865, 550), "HUB"),
             Door(859, 202, "vault", (115, 550), "LOCK", key_id="violet_key")],
            keys=[Pickup(pygame.Rect(455, 170, 18, 18), "violet_key")],
            title="VIOLET"
        ),
        # Screen 7
        "slate": Room(
            (83, 94, 103),
            [floor, pygame.Rect(0, 235, 230, 18), pygame.Rect(730, 235, 230, 18),
             pygame.Rect(300, 430, 150, 18), pygame.Rect(520, 430, 150, 18),
             pygame.Rect(405, 300, 150, 18)],
            [Door(35, 452, "hub", (865, 550), "HUB"),
             Door(859, 137, "cobalt", (115, 550), "LOOP")],
            enemies=[Enemy(475, 550, -1, 100)],
            ammo=[pygame.Rect(455, 265, 18, 18)],
            title="SLATE"
        ),
        # Screen 8
        "abyss": Room(
            (34, 37, 52),
            [floor, pygame.Rect(0, 180, 210, 18), pygame.Rect(750, 180, 210, 18),
             pygame.Rect(250, 415, 140, 18), pygame.Rect(565, 415, 140, 18),
             pygame.Rect(410, 295, 135, 18)],
            [Door(35, 452, "crimson", (865, 550), "BACK"),
             Door(859, 82, "vault", (115, 550), "INNER")],
            enemies=[Enemy(455, 295, -1, 65), Enemy(625, 415, 1, 95)],
            title="ABYSS"
        ),
        # Screen 9
        "vault": Room(
            (40, 44, 46),
            [floor, pygame.Rect(0, 270, 230, 18), pygame.Rect(730, 270, 230, 18),
             pygame.Rect(300, 445, 360, 18), pygame.Rect(390, 320, 180, 18),
             pygame.Rect(445, 210, 70, 18)],
            [Door(35, 452, "amber", (865, 550), "BACK"),
             Door(859, 172, "hub", (115, 550), "RETURN")],
            enemies=[Enemy(350, 445, 1, 75), Enemy(610, 445, -1, 75)],
            ammo=[pygame.Rect(470, 175, 18, 18)],
            title="THE INNER VAULT"
        ),
    }


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Stickman Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 32, bold=True)
        self.reset()

    def reset(self):
        self.rooms = make_rooms()
        self.room_name = "hub"
        self.x, self.y = 480.0, 550.0
        self.vx = self.vy = 0.0
        self.facing = 1
        self.on_ground = False
        self.ammo = 6
        self.inventory = set()
        self.flags = set()
        self.bullets = []
        self.enemy_bullets = []

    @property
    def player_rect(self):
        return pygame.Rect(int(self.x - 10), int(self.y - 50), 20, 50)

    def current_room(self):
        return self.rooms[self.room_name]

    def respawn_in_room(self, room_name, spawn):
        self.room_name = room_name
        self.x, self.y = spawn
        self.vx = self.vy = 0.0
        self.bullets.clear()
        self.enemy_bullets.clear()

    def try_move(self, dx, dy):
        room = self.current_room()
        rect = self.player_rect

        rect.x += int(dx)
        for platform in room.platforms:
            if rect.colliderect(platform):
                if dx > 0:
                    rect.right = platform.left
                elif dx < 0:
                    rect.left = platform.right
        self.x = rect.centerx

        rect.y += int(dy)
        self.on_ground = False
        for platform in room.platforms:
            if rect.colliderect(platform):
                if dy > 0:
                    rect.bottom = platform.top
                    self.vy = 0
                    self.on_ground = True
                elif dy < 0:
                    rect.top = platform.bottom
                    self.vy = 0
        self.y = rect.bottom

    def shoot_or_punch(self):
        if self.ammo > 0:
            self.ammo -= 1
            self.bullets.append([self.x + self.facing * 15, self.y - 28, self.facing * 10.0])
            return

        hitbox = pygame.Rect(0, 0, 45, 30)
        hitbox.centery = self.y - 27
        if self.facing > 0:
            hitbox.left = int(self.x + 8)
        else:
            hitbox.right = int(self.x - 8)

        for enemy in self.current_room().enemies:
            if enemy.alive and hitbox.colliderect(enemy.rect):
                enemy.alive = False

    def update_player(self, keys):
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -MOVE_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = MOVE_SPEED
            self.facing = 1

        self.vy += GRAVITY
        self.try_move(self.vx, 0)
        self.try_move(0, self.vy)

        self.x = max(12, min(WIDTH - 12, self.x))
        if self.y > HEIGHT + 100:
            self.reset()

    def update_pickups(self):
        room = self.current_room()
        player = self.player_rect

        for ammo in room.ammo[:]:
            if player.colliderect(ammo):
                self.ammo += 6
                room.ammo.remove(ammo)

        for pickup in room.keys[:]:
            if player.colliderect(pickup.rect):
                self.inventory.add(pickup.item_id)
                room.keys.remove(pickup)

        for pickup in room.switches[:]:
            if player.colliderect(pickup.rect):
                self.flags.add(pickup.item_id)
                room.switches.remove(pickup)

    def update_doors(self):
        player = self.player_rect
        for door in self.current_room().doors:
            if not player.colliderect(door.rect):
                continue
            if door.key_id and door.key_id not in self.inventory:
                continue
            if door.flag_id and door.flag_id not in self.flags:
                continue
            self.respawn_in_room(door.target, door.spawn)
            break

    def update_projectiles(self):
        room = self.current_room()

        for bullet in self.bullets[:]:
            bullet[0] += bullet[2]
            rect = pygame.Rect(int(bullet[0]) - 4, int(bullet[1]) - 2, 8, 4)
            if bullet[0] < -20 or bullet[0] > WIDTH + 20:
                self.bullets.remove(bullet)
                continue

            hit = False
            for enemy in room.enemies:
                if enemy.alive and rect.colliderect(enemy.rect):
                    enemy.alive = False
                    hit = True
                    break
            if hit:
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet[0] += bullet[2]
            rect = pygame.Rect(int(bullet[0]) - 5, int(bullet[1]) - 3, 10, 6)
            if bullet[0] < -20 or bullet[0] > WIDTH + 20:
                self.enemy_bullets.remove(bullet)
                continue
            if rect.colliderect(self.player_rect):
                self.reset()
                return

    def update_enemies(self):
        if self.room_name not in self.rooms:
            return
        for enemy in self.current_room().enemies:
            if not enemy.alive:
                continue
            enemy.cooldown -= 1
            if enemy.cooldown <= 0:
                enemy.facing = 1 if self.x > enemy.x else -1
                self.enemy_bullets.append([enemy.x + enemy.facing * 16, enemy.y - 30, enemy.facing * 4.2])
                enemy.cooldown = 85

    def draw_stickman(self, x, y, facing=1, enemy=False):
        color = (35, 35, 38) if not enemy else (76, 19, 22)
        x, y = int(x), int(y)
        pygame.draw.circle(self.screen, color, (x, y - 42), 8, 2)
        pygame.draw.line(self.screen, color, (x, y - 34), (x, y - 16), 2)
        pygame.draw.line(self.screen, color, (x, y - 28), (x + 10 * facing, y - 22), 2)
        pygame.draw.line(self.screen, color, (x, y - 28), (x - 8 * facing, y - 21), 2)
        pygame.draw.line(self.screen, color, (x, y - 16), (x + 8, y), 2)
        pygame.draw.line(self.screen, color, (x, y - 16), (x - 8, y), 2)

    def draw_door(self, door):
        unlocked = (not door.key_id or door.key_id in self.inventory) and (
            not door.flag_id or door.flag_id in self.flags
        )
        color = (222, 218, 200) if unlocked else (62, 61, 64)
        pygame.draw.rect(self.screen, color, door.rect, border_radius=14)
        pygame.draw.rect(self.screen, BLACK, door.rect, 3, border_radius=14)
        pygame.draw.circle(self.screen, BLACK, (door.x + 51, door.y + 51), 3)
        label = self.font.render(door.label, True, BLACK if unlocked else WHITE)
        self.screen.blit(label, (door.x + door.rect.width // 2 - label.get_width() // 2, door.y - 24))

    def draw(self):
        room = self.current_room()
        self.screen.fill(room.color)

        for platform in room.platforms:
            pygame.draw.rect(self.screen, (38, 38, 42), platform)

        for door in room.doors:
            self.draw_door(door)

        for rect in room.ammo:
            pygame.draw.rect(self.screen, (234, 223, 72), rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)

        for pickup in room.keys:
            pygame.draw.circle(self.screen, (238, 209, 74), pickup.rect.center, 8)
            pygame.draw.line(self.screen, BLACK, pickup.rect.center,
                             (pickup.rect.centerx + 13, pickup.rect.centery), 3)

        for pickup in room.switches:
            pygame.draw.rect(self.screen, (76, 215, 228), pickup.rect)
            pygame.draw.rect(self.screen, BLACK, pickup.rect, 2)

        for enemy in room.enemies:
            if enemy.alive:
                self.draw_stickman(enemy.x, enemy.y, enemy.facing, enemy=True)

        for bullet in self.bullets:
            pygame.draw.circle(self.screen, (250, 243, 166), (int(bullet[0]), int(bullet[1])), 4)
        for bullet in self.enemy_bullets:
            pygame.draw.circle(self.screen, (247, 110, 80), (int(bullet[0]), int(bullet[1])), 5)

        self.draw_stickman(self.x, self.y, self.facing)

        title = self.big_font.render(room.title, True, WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 16))

        inventory_text = f"Ammo {self.ammo}   Keys {len(self.inventory)}   Switches {len(self.flags)}"
        hud = self.font.render(inventory_text, True, WHITE)
        self.screen.blit(hud, (18, HEIGHT - 32))

        help_text = self.font.render("Move A/D or ←/→  Jump W/↑/Space  Shoot/Punch Z/J/Ctrl  R restart", True, WHITE)
        self.screen.blit(help_text, (WIDTH - help_text.get_width() - 18, HEIGHT - 32))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        self.reset()
                    if event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE) and self.on_ground:
                        self.vy = JUMP_SPEED
                    if event.key in (pygame.K_z, pygame.K_j, pygame.K_LCTRL):
                        self.shoot_or_punch()

            keys = pygame.key.get_pressed()
            self.update_player(keys)
            self.update_pickups()
            self.update_doors()
            self.update_enemies()
            self.update_projectiles()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
