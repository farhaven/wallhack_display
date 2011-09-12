import jsonrpclib
import pygame
import threading
import time

class ETA(threading.Thread):
    def __init__(self, dim, rpcserver):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 25)
        self.lock = threading.Lock()
        self.daemon = True
        jsonrpclib.config.version = 1.0
        self.rpcserver = rpcserver
        self.server = jsonrpclib.Server(rpcserver)

    def get_eta(self):
        try:
            return self.server.who()[unicode('eta')]
        except:
            return { "error": "server not reachable", "tried": self.rpcserver, "time": str(time.time()) }

    def run(self):
        while True:
            eta = self.get_eta()
            rect = [0, 0]
            self.lock.acquire()
            self.surface.fill((0, 0, 0))
            self.surface.blit(self.font.render("ETA:", True, (255, 255, 255)), rect)
            rect[1] = rect[1] + self.font.size("ETA")[1]
            for nick in eta:
                s = "%s: %s" % (nick, eta[nick])
                self.surface.blit(self.font.render(s, True, (255, 255, 255)), rect)
                rect[1] = rect[1] + self.font.size(s)[1]
            self.lock.release()
            time.sleep(5)

