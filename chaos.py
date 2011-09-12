import threading
import pygame
import time
import math

class Chaos(threading.Thread):
    def __init__(self, dim):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lock = threading.Lock()
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.dim = dim
        self.iter = 0

    def run(self):
        radius = 100
        target = (self.dim[0] / 2, self.dim[1] / 2 - 150)
        while True:
            if self.iter > math.pi / 2:
                self.iter = 0
            self.iter = self.iter + 0.01

            self.lock.acquire()
            self.surface.fill((0, 0, 0))

            x = int(math.cos(self.iter) * radius + self.dim[0] / 2)
            y = int(math.sin(self.iter) * radius * 0.5 + self.dim[1] / 2)
            pygame.draw.circle(self.surface, (255, 255, 255), (x, y), 2)
            pygame.draw.line(self.surface, (255, 255, 255), (x, y), target)

            x2 = int(math.cos(self.iter + math.pi / 2) * radius + self.dim[0] / 2)
            y2 = int(math.sin(self.iter + math.pi / 2) * radius * 0.5 + self.dim[1] / 2)
            pygame.draw.circle(self.surface, (255, 255, 255), (x2, y2), 2)
            pygame.draw.line(self.surface, (255, 255, 255), (x2, y2), target)
            pygame.draw.line(self.surface, (255, 255, 255), (x, y), (x2, y2))

            x3 = int(math.cos(self.iter + math.pi) * radius + self.dim[0] / 2)
            y3 = int(math.sin(self.iter + math.pi) * radius * 0.5 + self.dim[1] / 2)
            pygame.draw.circle(self.surface, (255, 255, 255), (x3, y3), 2)
            pygame.draw.line(self.surface, (255, 255, 255), (x3, y3), target)
            pygame.draw.line(self.surface, (255, 255, 255), (x2, y2), (x3, y3))

            x2 = int(math.cos(self.iter + 3 * (math.pi / 2)) * radius + self.dim[0] / 2)
            y2 = int(math.sin(self.iter + 3 * (math.pi / 2)) * radius * 0.5 + self.dim[1] / 2)
            pygame.draw.circle(self.surface, (255, 255, 255), (x2, y2), 2)
            pygame.draw.line(self.surface, (255, 255, 255), (x2, y2), target)
            pygame.draw.line(self.surface, (255, 255, 255), (x3, y3), (x2, y2))
            pygame.draw.line(self.surface, (255, 255, 255), (x, y), (x2, y2))

            self.lock.release()

            time.sleep(0.001)
