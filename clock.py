import pygame
import threading
import time

class Clock(threading.Thread):
    def __init__(self, dim):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 175)
        self.lock = threading.Lock()
        self.daemon = True

    def run(self):
        while True:
            s = time.strftime("%H:%M")
            self.lock.acquire()
            self.surface.fill((0, 0, 0))
            self.surface.blit(self.font.render(s, True, (255, 255, 255)), (0, 0))
            self.lock.release()
            time.sleep(1)

