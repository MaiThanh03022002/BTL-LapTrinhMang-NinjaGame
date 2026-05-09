import sys
import math
import random
import pygame
import json
import os
import datetime

from utils import *
from entity import *
from tilemap import Tilemap
from particle import Particle
from network import *
from spark import *
from bullet import Bullet
class Game():
    def __init__(self, net):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("ninja game")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.net = net
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
            "gun": load_img("data/images/gun.png"),
            "projectile": load_img("data/images/projectile.png"),
        }

        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load("map.json")
        self.game_state_file=""
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(
                pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13)
            )

        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]
        self.projectiles = []
        self.dead = 0
        self.bullets = []
    def run(self):
        self.game_state_file = self.create_game_state_file()

        while True:
            for bullet in self.bullets[:]:
                bullet.move()
                
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
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets["projectile"]
                self.display.blit(
                    img,
                    (
                        projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                        projectile[0][1] - img.get_height() / 2 - render_scroll[1],
                    ),
                )
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(
                            Spark(
                                projectile[0],
                                random.random()
                                - 0.5
                                + (math.pi if projectile[1] > 0 else 0),
                                2 + random.random(),
                            )
                        )
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(
                                Spark(
                                    self.player.rect().center,
                                    angle,
                                    2 + random.random(),
                                )
                            )
                            self.particles.append(
                                Particle(
                                    self,
                                    "particle",
                                    self.player.rect().center,
                                    velocity=[
                                        math.cos(angle + math.pi) * speed * 0.5,
                                        math.sin(angle + math.pi) * speed * 0.5,
                                    ],
                                    frame=random.randint(0, 7),
                                )
                            )
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(
                                Spark(
                                    self.player.rect().center,
                                    angle,
                                    2 + random.random(),
                                )
                            )
                            self.particles.append(
                                Particle(
                                    self,
                                    "particle",
                                    self.player.rect().center,
                                    velocity=[
                                        math.cos(angle + math.pi) * speed * 0.5,
                                        math.sin(angle + math.pi) * speed * 0.5,
                                    ],
                                    frame=random.randint(0, 7),
                                )
                            )
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)
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
                    if event.button == 1:
                        # self.player.attack = True
                        bullet = Bullet(self.player.pos[0], self.player.pos[1], self.player.right)
                        self.bullets.append(bullet)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.player.attack = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                  
                        self.player.right=False
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                     
                        self.player.right=True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
            print(self.send_data())
            string_data=self.send_data()
            data = json.loads(string_data)
            # Khởi tạo biến trước khi kiểm tra
            nhanVT = data['opponent_position']
            nhanInfor = data['room_info']
            playerId = data['player_id']
            # In ra kết quả
            print("nhanVT:", nhanVT)
            print("nhanInfor:", nhanInfor)
            print("playerId:", playerId)
            self.save_game_state(nhanVT,nhanInfor,int(playerId))

            nhan = nhanVT
            ids = nhan.split(":")
            x = ids[1].split(",")
            num1 = int(ids[0])
            num2 = float(x[0])
            num3 = float(x[1])
            print(num1)
            print(num2)
            print(num3)
            t=nhanInfor.split(",")[1]
            if int(t)>1:
                self.player2 = Player(self, (num2, num3), (8, 15))
                self.player2.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player2.render(self.display, offset=render_scroll)
            
            # Gọi cập nhật thông tin
            data=nhanInfor+"/"+ str(playerId)
            print(data)
            self.draw_text(data)
            
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)
          
    def save_game_state(self,pl2,detail,playerId):
        player1_position_str = f"{self.net.id}:{self.player.pos[0]},{self.player.pos[1]}"
        state = {
            'player1': player1_position_str,
            'player2': pl2,
            'room_info': detail,
            'time': pygame.time.get_ticks(),
            'id': str(playerId)
        }
        self.append_to_json(state,self.game_state_file)   
    def create_game_state_file(self):

        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"game_state_{timestamp}.json"
        if os.path.exists(filename):
            filename = f"game_state_{timestamp}_{random.randint(1000, 9999)}.json"
        return filename     
    def append_to_json(self, data, file_path):
        with open(file_path, 'a') as file:
            file.write(json.dumps(data) + "\n")   
    def draw_text_with_outline(self, text, font, x, y, text_color, outline_color):
        base = font.render(text, False, text_color)
        outline = pygame.Surface(base.get_size(), pygame.SRCALPHA)
        # Vẽ viền cho chữ
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx != 0 or dy != 0:
                    temp_surf = font.render(text, False, outline_color)
                    outline.blit(temp_surf, (dx, dy))
        # Vẽ chữ lên viền
        outline.blit(base, (0, 0))
        # Vẽ toàn bộ lên màn hình
        self.display.blit(outline, (x, y))
    
    # Vẽ thông tin
    def draw_text(self, data):
        room_info, playerId = data.split('/')
        parts = room_info.split(',')
        roomId = int(parts[0])
        number_of_connected_players = int(parts[1])
        ranking_datas = parts[2:]
        ranking_data = ranking_datas[:number_of_connected_players]
        font = pygame.font.Font('Consolas.ttf', 10) 

        self.draw_text_with_outline(f"PlayerId: {playerId}", font, 10, 10, (255, 255, 255), (0, 0, 0))
        self.draw_text_with_outline(f"RoomId: {roomId} Players: {number_of_connected_players}", font, 10, 30, (255, 255, 255), (0, 0, 0))

        ranking_y = 50
        for i, rank in enumerate(ranking_data, start=1):
            self.draw_text_with_outline(f"Rank {i}: {rank}", font, 10, ranking_y, (255, 255, 255), (0, 0, 0))
            ranking_y += 20 

    def send_data(self):
        data = (
            str(self.net.id)
            + ":"
            + str(self.player.pos[0])
            + ","
            + str(self.player.pos[1])
        )
        print(self.net.id)
        print("dend" + data)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0

