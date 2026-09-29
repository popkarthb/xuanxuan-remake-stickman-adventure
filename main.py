import math
import sys

import pygame

from levels import START_ROOM, START_SPAWN, build_world
from models import Door, ItemPickup


WIDTH, HEIGHT = 960, 600
FPS = 60
GRAVITY = 0.75
MOVE_SPEED = 4.5
JUMP_SPEED = -13.5

WHITE = (250, 250, 247)
BLACK = (17, 17, 20)
PLAYER_COLOR = (35, 35, 38)
ENEMY_COLOR = (76, 19, 22)
PLATFORM_COLOR = (38, 38, 42)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Stickman Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 18)
        self.small_font = pygame.font.SysFont("consolas", 15)
        self.player_sprites = self.build_player_sprites()
        self.reset()

    def reset(self):
        self.rooms, self.links = build_world()
        self.room_name = START_ROOM
        self.x, self.y = self.rooms[START_ROOM].spawns[START_SPAWN]
        self.vx = self.vy = 0.0
        self.facing = 1
        self.on_ground = False
        self.ammo = 0
        self.inventory = set()
        self.bullets = []
        self.enemy_bullets = []
        self.door_cooldown = 0

    @property
    def player_rect(self):
        return pygame.Rect(int(self.x - 10), int(self.y - 50), 20, 50)

    def current_room(self):
        return self.rooms[self.room_name]

    def enter_room(self, room_name, spawn_name):
        self.room_name = room_name
        self.x, self.y = self.rooms[room_name].spawns[spawn_name]
        self.vx = self.vy = 0.0
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.door_cooldown = 16

    def try_move(self, dx, dy):
        rect = self.player_rect
        solids = self.current_room().solid_rects()

        rect.x += int(dx)
        for solid in solids:
            if rect.colliderect(solid):
                if dx > 0:
                    rect.right = solid.left
                elif dx < 0:
                    rect.left = solid.right
        self.x = rect.centerx

        rect.y += int(dy)
        self.on_ground = False
        for solid in solids:
            if rect.colliderect(solid):
                if dy > 0:
                    rect.bottom = solid.top
                    self.vy = 0
                    self.on_ground = True
                elif dy < 0:
                    rect.top = solid.bottom
                    self.vy = 0
        self.y = rect.bottom

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

    def try_drill(self):
        if "drill" not in self.inventory or not self.on_ground:
            return False

        player = self.player_rect
        room = self.current_room()

        for platform in room.breakables[:]:
            rect = platform.rect
            horizontal_overlap = player.right > rect.left and player.left < rect.right
            standing_on_it = abs(player.bottom - rect.top) <= 4
            if horizontal_overlap and standing_on_it:
                room.breakables.remove(platform)
                self.on_ground = False
                self.vy = 3.0
                return True

        return False

    def shoot_or_punch(self):
        if "gun" in self.inventory and self.ammo > 0:
            self.ammo -= 1
            self.bullets.append(
                [self.x + self.facing * 15, self.y - 28, self.facing * 10.0]
            )
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

    def use_action(self):
        keys = pygame.key.get_pressed()
        drilling = keys[pygame.K_DOWN] or keys[pygame.K_s]
        if drilling and self.try_drill():
            return
        self.shoot_or_punch()

    def update_items(self):
        room = self.current_room()
        player = self.player_rect

        for item in room.items[:]:
            if not player.colliderect(item.rect):
                continue

            if item.kind == "gun":
                self.inventory.add("gun")
                self.ammo = max(self.ammo, 6)
            elif item.kind == "drill":
                self.inventory.add("drill")
            elif item.kind == "key":
                self.inventory.add(item.item_id)
            elif item.kind == "chest":
                self.inventory.add(item.item_id)
            elif item.kind == "ammo":
                self.ammo += 6

            room.items.remove(item)

    def update_doors(self):
        if self.door_cooldown > 0:
            self.door_cooldown -= 1
            return

        player = self.player_rect
        for door in self.current_room().doors:
            if not player.colliderect(door.rect):
                continue
            if door.key_id and door.key_id not in self.inventory:
                continue
            if door.flag_id and door.flag_id not in self.inventory:
                continue

            link = self.links.get((self.room_name, door.door_id))
            if link is None:
                continue

            self.enter_room(link.target_room, link.target_spawn)
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
        right_frames = [
            self.make_player_sprite(run_frame=0),
            self.make_player_sprite(run_frame=1),
        ]
        right_idle = self.make_player_sprite(run_frame=None)

        return {
            1: {"idle": right_idle, "run": right_frames},
            -1: {
                "idle": pygame.transform.flip(right_idle, True, False),
                "run": [
                    pygame.transform.flip(frame, True, False)
                    for frame in right_frames
                ],
            },
        }

    def make_player_sprite(self, run_frame):
        surface = pygame.Surface((42, 58), pygame.SRCALPHA)

        pygame.draw.circle(surface, PLAYER_COLOR, (21, 9), 8, 2)
        pygame.draw.line(surface, PLAYER_COLOR, (21, 17), (21, 37), 3)

        if run_frame is None:
            pygame.draw.line(surface, PLAYER_COLOR, (21, 23), (33, 29), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 23), (11, 29), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 37), (31, 55), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 37), (11, 55), 3)
        elif run_frame == 0:
            pygame.draw.line(surface, PLAYER_COLOR, (21, 23), (35, 18), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 23), (9, 32), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 37), (36, 49), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 37), (9, 55), 3)
        else:
            pygame.draw.line(surface, PLAYER_COLOR, (21, 23), (34, 32), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 23), (8, 18), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 37), (34, 55), 3)
            pygame.draw.line(surface, PLAYER_COLOR, (21, 37), (8, 49), 3)

        return surface

    def draw_player(self):
        if abs(self.vx) > 0.1:
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
            not door.flag_id or door.flag_id in self.inventory
        )
        fill = (222, 218, 200) if unlocked else (82, 80, 83)
        rect = door.rect
        radius = rect.width // 2
        center = (rect.centerx, rect.y + radius)
        body = pygame.Rect(
            rect.x,
            rect.y + radius,
            rect.width,
            rect.height - radius,
        )

        # Fill an arch cap and then a straight-sided lower body.
        pygame.draw.circle(self.screen, fill, center, radius)
        pygame.draw.rect(self.screen, fill, body)

        # Draw the upper circular outline, cover its lower half, then draw
        # straight sides. This leaves a rounded top and a square floor edge.
        pygame.draw.circle(self.screen, BLACK, center, radius, 3)
        pygame.draw.rect(self.screen, fill, body)
        pygame.draw.line(
            self.screen,
            BLACK,
            (rect.left, rect.y + radius),
            (rect.left, rect.bottom),
            3,
        )
        pygame.draw.line(
            self.screen,
            BLACK,
            (rect.right - 1, rect.y + radius),
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
            (rect.right - 14, rect.y + radius + 27),
            3,
        )

    def draw_item(self, item: ItemPickup):
        rect = item.rect

        if item.kind == "gun":
            pygame.draw.rect(
                self.screen,
                BLACK,
                pygame.Rect(rect.x, rect.y + 6, rect.width - 4, 7),
            )
            pygame.draw.line(
                self.screen,
                BLACK,
                (rect.x + 11, rect.y + 12),
                (rect.x + 8, rect.bottom - 2),
                4,
            )

        elif item.kind == "drill":
            body = pygame.Rect(rect.x, rect.y + 5, 17, 16)
            pygame.draw.rect(self.screen, (82, 88, 94), body)
            pygame.draw.polygon(
                self.screen,
                BLACK,
                [
                    (rect.x + 17, rect.y + 7),
                    (rect.right, rect.centery),
                    (rect.x + 17, rect.y + 20),
                ],
            )
            pygame.draw.line(
                self.screen,
                BLACK,
                (rect.x + 7, rect.y + 21),
                (rect.x + 4, rect.bottom),
                4,
            )

        elif item.kind == "key":
            pygame.draw.circle(
                self.screen,
                (212, 170, 45),
                (rect.x + 7, rect.y + 9),
                6,
                3,
            )
            pygame.draw.line(
                self.screen,
                (212, 170, 45),
                (rect.x + 12, rect.y + 12),
                (rect.right - 2, rect.y + 12),
                4,
            )
            pygame.draw.line(
                self.screen,
                (212, 170, 45),
                (rect.right - 7, rect.y + 12),
                (rect.right - 7, rect.y + 18),
                3,
            )

        elif item.kind == "chest":
            pygame.draw.rect(
                self.screen,
                (126, 82, 42),
                pygame.Rect(rect.x, rect.y + 9, rect.width, rect.height - 9),
            )
            pygame.draw.rect(
                self.screen,
                BLACK,
                pygame.Rect(rect.x, rect.y + 9, rect.width, rect.height - 9),
                2,
            )
            pygame.draw.arc(
                self.screen,
                BLACK,
                pygame.Rect(rect.x, rect.y, rect.width, 20),
                0,
                math.pi,
                2,
            )
            pygame.draw.rect(
                self.screen,
                (214, 178, 67),
                pygame.Rect(rect.centerx - 3, rect.centery + 2, 6, 7),
            )

    def draw_breakable(self, rect):
        pygame.draw.rect(self.screen, PLATFORM_COLOR, rect)
        crack = (105, 105, 110)
        x1 = rect.left + rect.width // 3
        x2 = rect.left + (rect.width * 2) // 3
        pygame.draw.line(
            self.screen,
            crack,
            (x1, rect.top + 2),
            (x1 + 8, rect.bottom - 2),
            2,
        )
        pygame.draw.line(
            self.screen,
            crack,
            (x2, rect.top + 2),
            (x2 - 7, rect.bottom - 2),
            2,
        )

    def draw_hud(self):
        status = [
            f"Gun:{self.ammo}" if "gun" in self.inventory else "Gun:-",
            "Drill:Y" if "drill" in self.inventory else "Drill:-",
            "Key:Y" if "gold_key" in self.inventory else "Key:-",
            "Chest:Y" if "treasure_chest" in self.inventory else "Chest:-",
        ]
        line1 = self.small_font.render("   ".join(status), True, WHITE)
        line2 = self.small_font.render(
            "Move A/D or arrows   Jump W/Up/Space   Attack Z/J/Ctrl   Drill Down+Attack   R restart",
            True,
            WHITE,
        )
        self.screen.blit(line1, (12, 556))
        self.screen.blit(line2, (12, 578))

    def draw(self):
        room = self.current_room()
        self.screen.fill(room.color)

        for platform in room.platforms:
            pygame.draw.rect(self.screen, PLATFORM_COLOR, platform)

        for platform in room.breakables:
            self.draw_breakable(platform.rect)

        for door in room.doors:
            self.draw_door(door)

        for item in room.items:
            self.draw_item(item)

        for enemy in room.enemies:
            if enemy.alive:
                self.draw_enemy(enemy.x, enemy.y, enemy.facing)

        for bullet in self.bullets:
            pygame.draw.circle(
                self.screen,
                (250, 243, 166),
                (int(bullet[0]), int(bullet[1])),
                4,
            )

        for bullet in self.enemy_bullets:
            pygame.draw.circle(
                self.screen,
                (247, 110, 80),
                (int(bullet[0]), int(bullet[1])),
                5,
            )

        self.draw_player()
        self.draw_hud()
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
                    if (
                        event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE)
                        and self.on_ground
                    ):
                        self.vy = JUMP_SPEED
                    if event.key in (pygame.K_z, pygame.K_j, pygame.K_LCTRL):
                        self.use_action()

            keys = pygame.key.get_pressed()
            self.update_player(keys)
            self.update_items()
            self.update_doors()
            self.update_enemies()
            self.update_projectiles()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
