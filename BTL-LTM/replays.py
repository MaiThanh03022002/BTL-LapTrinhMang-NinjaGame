import pygame
import json
import pygame
import json

from utils import *
from entity import *
from tilemap import Tilemap
from particle import Particle
from network import *


class Replay:
    def __init__(self, replay_file):
        self.replay_file = replay_file
        self.game_states = self.load_game_states()
        self.current_index = 0

    def load_game_states(self):
        with open(self.replay_file, 'r') as file:
            return [json.loads(line.strip()) for line in file if line.strip()]

    def get_next_state(self):
        if self.current_index < len(self.game_states):
            state = self.game_states[self.current_index]
            self.current_index += 1
            return state
        else:
            return None 

class GameReplay():
    def __init__(self):
        pygame.init()
        pygame.font.init()
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
            "gun": load_img("data/images/gun.png"),
            "projectile": load_img("data/images/projectile.png"),
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

    def run_replay(self,file):
        replay = Replay(file)

        while True:           
            game_state = replay.get_next_state()
            if game_state is None:
                print("Replay finished.")
                break

            # Cập nhật trạng thái của player dựa vào dữ liệu replay
            player1_data = game_state['player1']
            player1_id, player1_pos = player1_data.split(':')
            player1_x, player1_y = map(float, player1_pos.split(','))

            player2_data = game_state['player2']
            player2_id, player2_pos = player2_data.split(':')
            player2_x, player2_y = map(float, player2_pos.split(','))

            # Cập nhật vị trí người chơi dựa trên dữ liệu JSON
            self.player.pos = (player1_x, player1_y)
            
            # Theo hình người chơi
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.display.blit(self.assets["background"], (0, 0))
            self.tilemap.render(self.display, offset=render_scroll)     
            if int(game_state['room_info'].split(',')[1])>1:
                self.player2 = Player(self, (player2_x, player2_y), (8, 15))
                self.player2.render(self.display, offset=render_scroll)
            self.player.render(self.display, offset=render_scroll)
            
            data=game_state['room_info']+"/"+game_state['id']
            print(data)
            self.draw_text(data)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
        pygame.display.quit()

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
        # Split the data to get room info, number of connected players, ranking list, and player id
        room_info, playerId = data.split('/')
        parts = room_info.split(',')
        roomId = int(parts[0])
        number_of_connected_players = int(parts[1])
        ranking_datas = parts[2:]
        ranking_data=ranking_datas[:number_of_connected_players]
        font = pygame.font.Font('Consolas.ttf', 10)  # Use a smaller font size for more text

        self.draw_text_with_outline(f"PlayerId: {playerId}", font, 10, 10, (255, 255, 255), (0, 0, 0))
        self.draw_text_with_outline(f"RoomId: {roomId} Players: {number_of_connected_players}", font, 10, 30, (255, 255, 255), (0, 0, 0))

        # Render and blit ranking list line by line
        ranking_y = 50  
        for i, rank in enumerate(ranking_data, start=1):
            self.draw_text_with_outline(f"Rank {i}: {rank}", font, 10, ranking_y, (255, 255, 255), (0, 0, 0))
            ranking_y += 20  