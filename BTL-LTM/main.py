import sys
import math
import random

import pygame

from utils import *
from entity import *
from tilemap import Tilemap
from particle import Particle


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ninja game")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            "decor": load_images("data/images/tiles/decor"),
            "grass": load_images("data/images/tiles/grass"),
            "large_decor": load_images("data/images/tiles/large_decor"),
            "stone": load_images("data/images/tiles/stone"),
            "player": load_img("data/images/entities/player.png"),
            "background": load_img("data/images/background.png"),
            "player/idle": Animations(
                load_images("data/images/entities/player/idle"), img_dur=6
            ),
            "player/run": Animations(
                load_images("data/images/entities/player/run"), img_dur=4
            ),
            "player/jump": Animations(load_images("data/images/entities/player/jump")),
            "player/slide": Animations(
                load_images("data/images/entities/player/slide")
            ),
            "player/wall_slide": Animations(
                load_images("data/images/entities/player/wall_slide")
            ),
            "particle/leaf": Animations(
                load_images("data/images/particles/leaf"), img_dur=20, loop=False
            ),
            "particle/particle": Animations(
                load_images("data/images/particles/particle"), img_dur=6, loop=False
            ),
        }

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load("map.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(
                pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13)
            )

        self.particles = []

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (
                        rect.x + random.random() * rect.width,
                        rect.y + random.random() * rect.height,
                    )
                    self.particles.append(
                        Particle(
                            self,
                            "leaf",
                            pos,
                            velocity=[-0.1, 0.3],
                            frame=random.randint(0, 20),
                        )
                    )

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == "leaf":
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.player.dash()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


Game().run()
