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
        radius = 150
        white = (255, 255, 255)
        target = (self.dim[0] / 2, self.dim[1] / 2 - 150)
        while True:
            if self.iter > math.pi / 2:
                self.iter = 0
            self.iter = self.iter + 0.01

            self.lock.acquire()
            self.surface.fill((0, 0, 0))

            pos1 = (int(math.cos(self.iter) * radius), int(math.sin(self.iter) * radius * 0.25))
            pos2 = (self.dim[0] / 2 - pos1[0], self.dim[1] / 2 - pos1[1] + 150)
            pos1 = (self.dim[0] / 2 + pos1[0], self.dim[1] / 2 + pos1[1] + 150)

            pos3 = (int(math.cos(self.iter + math.pi / 2) * radius), int(math.sin(self.iter + math.pi / 2) * radius * 0.25))
            pos4 = (self.dim[0] / 2 - pos3[0], self.dim[1] / 2 - pos3[1] + 150)
            pos3 = (self.dim[0] / 2 + pos3[0], self.dim[1] / 2 + pos3[1] + 150)

            pygame.draw.lines(self.surface, white, True, [pos1, pos3, pos2, pos4])
            pygame.draw.line(self.surface, white, pos1, pos2)
            pygame.draw.line(self.surface, white, pos3, pos4)

            pygame.draw.line(self.surface, white, pos1, target)
            pygame.draw.line(self.surface, white, pos2, target)
            pygame.draw.line(self.surface, white, pos3, target)
            pygame.draw.line(self.surface, white, pos4, target)

            self.lock.release()

            time.sleep(0.005)
