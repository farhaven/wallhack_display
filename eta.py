import jsonrpclib
import pygame
import threading
import time

jsonrpclib.config.version = 1.0

black = (0, 0, 0)
green = (0, 255, 0)

class ETA(threading.Thread):
    daemon = True
    def __init__(self, dim, rpcserver):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey(black)
        self.font_heading = pygame.font.SysFont("Liberation Mono, Monospace", 65)
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 55)
        self.lock = threading.Lock()
        self.rpcserver = rpcserver
        self.server = jsonrpclib.Server(rpcserver)

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

    def run(self):
        green = (0, 255, 0)
        while True:
            eta  = self.get_eta()
            todo = self.get_todo()
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

            self.lock.release()
            time.sleep(5)

