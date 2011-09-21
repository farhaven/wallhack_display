import jsonrpclib
import pygame
import threading
import time

jsonrpclib.config.version = 1.0

black = (0, 0, 0)
green = (0, 255, 0)

class ETA(threading.Thread):
    daemon = True
    timeout = 0
    def __init__(self, dim, rpcserver, clock):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey(black)
        self.font_heading = pygame.font.SysFont("Liberation Mono, Monospace", 65)
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 55)
        self.lock = threading.Lock()
        self.rpcserver = rpcserver
        self.server = jsonrpclib.Server(rpcserver)
        self.clock = clock
        self.dim = dim

    def get_eta(self):
        try:
            return self.server.who()[unicode('eta')]
        except:
            return { "error": "server not reachable", "tried": self.rpcserver, "time": str(time.time()) }

    def get_todo(self):
        try:
            return self.server.todo()
        except:
            return [ "fix server" ]

    def get_timeout(self):
        return self.timeout

    def run(self):
        green = (0, 255, 0)
        while True:
            eta  = self.get_eta()
            todo = self.get_todo()
            self.timeout = len(eta) * 0.5 + len(todo)

            rect = [ 20, 20 ]

            self.lock.acquire()
            self.surface.fill(black)

            if len(eta) != 0:
                self.surface.blit(self.font_heading.render("ETA:", True, green), rect)
                rect[1] = rect[1] + self.font_heading.size("ETA:")[1]
                for nick in eta:
                    s = "%s: %s" % (nick, eta[nick])
                    self.surface.blit(self.font.render(s, True, green), rect)
                    rect[1] = rect[1] + self.font.size(s)[1]
                rect[1] = rect[1] + self.font.size("foo")[1]

            if len(todo) != 0:
                self.surface.blit(self.font_heading.render("TODO:", True, green), rect)
                rect[1] = rect[1] + self.font_heading.size("TODO:")[1]
                for t in todo:
                    self.surface.blit(self.font.render("- " + t, True, green), rect)
                    rect[1] = rect[1] + self.font.size("- " + t)[1]

            self.clock.lock.acquire()
            self.surface.blit(self.clock.surface, (self.dim[0] - self.clock.get_dimensions()[0] - 10, 0))
            self.clock.lock.release()
            self.lock.release()
            time.sleep(5)

