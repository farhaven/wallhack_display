import pygame
import threading
import time

class Clock(threading.Thread):
    daemon = True
    dim = (0, 0)

    def __init__(self):
        threading.Thread.__init__(self)
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 120)
        self.lock = threading.Lock()

    def get_dimensions(self):
        return self.dim

    def run(self):
        green = (0, 255, 0)
        while True:
            s = time.strftime("%H:%M")
            self.dim = self.font.size(s)
            self.lock.acquire()
            self.surface = self.font.render(s, True, green)
            self.lock.release()
            time.sleep(1)
