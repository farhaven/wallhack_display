import pygame
import threading
import time

class Clock(threading.Thread):
    daemon = True
    def __init__(self, dim):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 300)
        self.lock = threading.Lock()
        self.dim  = dim

    def run(self):
        green = (0, 255, 0)
        while True:
            s = time.strftime("%H:%M")
            size = self.font.size(s)
            self.lock.acquire()
            self.surface.fill((0, 0, 0))
            self.surface.blit(self.font.render(s, True, green), (self.dim[0] / 2 - size[0] / 2, self.dim[1] / 2 - size[1] / 2))
            self.lock.release()
            time.sleep(1)

