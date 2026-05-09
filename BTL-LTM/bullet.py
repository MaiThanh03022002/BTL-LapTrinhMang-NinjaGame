import pygame
import sys
BLACK = (0, 0, 0)
class Bullet:
    def __init__(self,  x, y, direction):
        self.position = [x, y]
        self.direction = direction
        self.speed = 20
        self.color = BLACK
        self.radius = 5

    def move(self):
        """
        Moves the bullet horizontally in the last direction the player moved.
        """
        if self.direction == False:
            self.position[0] -= self.speed
            print("Bắn trái")
        elif self.direction ==True:
            self.position[0] += self.speed
            print("Bắn phải")

    def draw(self, screen):
        """
        Draws the bullet on the screen.
        """
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)
