import threading
import pygame
import time
import jsonrpclib
import random

class Available(threading.Thread):
    def __init__(self, dim, rpcserver):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 50)
        self.lock = threading.Lock()
        self.daemon = True
        self.rpcserver = rpcserver
        self.dim = dim
        self.server = jsonrpclib.Server(rpcserver)

    def get_available(self):
        try:
            return self.server.who()[unicode('available')]
        except:
            return [ "could", "not", "reach", "server", self.rpcserver, str(time.time()) ]

    def random_color(self):
        return (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))

    def run(self):
        while True:
            a = self.get_available()
            self.lock.acquire()
            self.surface.fill((0, 0, 0))
            for nick in a:
                surf = pygame.transform.rotate(self.font.render(nick, True, self.random_color()), random.random() * 360)
                self.surface.blit(surf, 
                          (random.randint(0, max(1, self.dim[0] - surf.get_width())),
                           random.randint(0, max(1, self.dim[1] - surf.get_height()))))

            self.lock.release()
            time.sleep(1)
