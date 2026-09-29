import math
import sys

import pygame

from levels import make_rooms
from models import Door


WIDTH, HEIGHT = 960, 600
FPS = 60
GRAVITY = 0.75
MOVE_SPEED = 4.5
JUMP_SPEED = -13.5
WHITE = (250, 250, 247)
BLACK = (17, 17, 20)
PLAYER_COLOR = (35, 35, 38)
ENEMY_COLOR = (76, 19, 22)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Stickman Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.big_font = pygame.font.SysFont("consolas", 32, bold=True)
        self.player_sprites = self.build_player_sprites()
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
        for enemy in self.current_room().enemies:
            if not enemy.alive:
                continue
            enemy.cooldown -= 1
            if enemy.cooldown <= 0:
                enemy.facing = 1 if self.x > enemy.x else -1
                self.enemy_bullets.append(
                    [enemy.x + enemy.facing * 16, enemy.y - 30, enemy.facing * 4.2]
                )
                enemy.cooldown = 85

    def build_player_sprites(self):
        """Create lightweight two-frame run sprites and mirror them by direction."""
        right_frames = [
            self.make_player_sprite(run_frame=0),
            self.make_player_sprite(run_frame=1),
        ]
        right_idle = self.make_player_sprite(run_frame=None)
        return {
            1: {"idle": right_idle, "run": right_frames},
            -1: {
                "idle": pygame.transform.flip(right_idle, True, False),
                "run": [pygame.transform.flip(frame, True, False) for frame in right_frames],
            },
        }

    def make_player_sprite(self, run_frame):
        surface = pygame.Surface((42, 58), pygame.SRCALPHA)
        color = PLAYER_COLOR

        pygame.draw.circle(surface, color, (21, 9), 8, 2)
        pygame.draw.line(surface, color, (21, 17), (21, 37), 3)

        if run_frame is None:
            pygame.draw.line(surface, color, (21, 23), (33, 29), 3)
            pygame.draw.line(surface, color, (21, 23), (11, 29), 3)
            pygame.draw.line(surface, color, (21, 37), (31, 55), 3)
            pygame.draw.line(surface, color, (21, 37), (11, 55), 3)
        elif run_frame == 0:
            pygame.draw.line(surface, color, (21, 23), (35, 18), 3)
            pygame.draw.line(surface, color, (21, 23), (9, 32), 3)
            pygame.draw.line(surface, color, (21, 37), (36, 49), 3)
            pygame.draw.line(surface, color, (21, 37), (9, 55), 3)
        else:
            pygame.draw.line(surface, color, (21, 23), (34, 32), 3)
            pygame.draw.line(surface, color, (21, 23), (8, 18), 3)
            pygame.draw.line(surface, color, (21, 37), (34, 55), 3)
            pygame.draw.line(surface, color, (21, 37), (8, 49), 3)

        return surface

    def draw_player(self):
        moving = abs(self.vx) > 0.1
        if moving:
            frame_index = (pygame.time.get_ticks() // 110) % 2
            sprite = self.player_sprites[self.facing]["run"][frame_index]
        else:
            sprite = self.player_sprites[self.facing]["idle"]

        rect = sprite.get_rect(midbottom=(int(self.x), int(self.y)))
        self.screen.blit(sprite, rect)

    def draw_enemy(self, x, y, facing=1):
        x, y = int(x), int(y)
        pygame.draw.circle(self.screen, ENEMY_COLOR, (x, y - 42), 8, 2)
        pygame.draw.line(self.screen, ENEMY_COLOR, (x, y - 34), (x, y - 16), 2)
        pygame.draw.line(
            self.screen, ENEMY_COLOR, (x, y - 28), (x + 10 * facing, y - 22), 2
        )
        pygame.draw.line(
            self.screen, ENEMY_COLOR, (x, y - 28), (x - 8 * facing, y - 21), 2
        )
        pygame.draw.line(self.screen, ENEMY_COLOR, (x, y - 16), (x + 8, y), 2)
        pygame.draw.line(self.screen, ENEMY_COLOR, (x, y - 16), (x - 8, y), 2)

    def draw_door(self, door: Door):
        unlocked = (not door.key_id or door.key_id in self.inventory) and (
            not door.flag_id or door.flag_id in self.flags
        )
        color = (222, 218, 200) if unlocked else (62, 61, 64)
        rect = door.rect

        # Arch-shaped top with straight vertical sides down to the floor/platform.
        arch_height = rect.width // 2
        arch_box = pygame.Rect(rect.x, rect.y, rect.width, arch_height * 2)
        body = pygame.Rect(
            rect.x,
            rect.y + arch_height,
            rect.width,
            rect.height - arch_height,
        )

        pygame.draw.ellipse(self.screen, color, arch_box)
        pygame.draw.rect(self.screen, color, body)

        pygame.draw.arc(
            self.screen,
            BLACK,
            arch_box,
            0,
            math.pi,
            3,
        )
        pygame.draw.line(
            self.screen,
            BLACK,
            (rect.left, rect.y + arch_height),
            (rect.left, rect.bottom),
            3,
        )
        pygame.draw.line(
            self.screen,
            BLACK,
            (rect.right - 1, rect.y + arch_height),
            (rect.right - 1, rect.bottom),
            3,
        )
        pygame.draw.line(
            self.screen,
            BLACK,
            (rect.left, rect.bottom - 1),
            (rect.right - 1, rect.bottom - 1),
            3,
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (rect.right - 14, rect.y + arch_height + 28),
            3,
        )

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
            pygame.draw.line(
                self.screen,
                BLACK,
                pickup.rect.center,
                (pickup.rect.centerx + 13, pickup.rect.centery),
                3,
            )

        for pickup in room.switches:
            pygame.draw.rect(self.screen, (76, 215, 228), pickup.rect)
            pygame.draw.rect(self.screen, BLACK, pickup.rect, 2)

        for enemy in room.enemies:
            if enemy.alive:
                self.draw_enemy(enemy.x, enemy.y, enemy.facing)

        for bullet in self.bullets:
            pygame.draw.circle(
                self.screen, (250, 243, 166), (int(bullet[0]), int(bullet[1])), 4
            )
        for bullet in self.enemy_bullets:
            pygame.draw.circle(
                self.screen, (247, 110, 80), (int(bullet[0]), int(bullet[1])), 5
            )

        self.draw_player()

        title = self.big_font.render(room.title, True, WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 16))

        inventory_text = (
            f"Ammo {self.ammo}   Keys {len(self.inventory)}   "
            f"Switches {len(self.flags)}"
        )
        hud = self.font.render(inventory_text, True, WHITE)
        self.screen.blit(hud, (18, HEIGHT - 32))

        help_text = self.font.render(
            "Move A/D or ←/→  Jump W/↑/Space  Shoot/Punch Z/J/Ctrl  R restart",
            True,
            WHITE,
        )
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
