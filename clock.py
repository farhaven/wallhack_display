import pygame
import threading
import time

class Clock(threading.Thread):
    def __init__(self, dim, font):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.font = font
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

