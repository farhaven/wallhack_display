import jsonrpclib
import pygame
import threading
import time

class ETA(threading.Thread):
    def __init__(self, dim, rpcserver):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 30)
        self.font_heading = pygame.font.SysFont("Liberation Mono, Monospace", 35)
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

    def get_todo(self):
        try:
            return self.server.todo()
        except:
            return [ "fix server" ]

    def run(self):
        green = (0, 255, 0)
        while True:
            eta  = self.get_eta()
            rect = [0, 0]

            txt_head = "TODO:" if len(eta) == 0 else "ETA:"
            txt_body = []

            if len(eta) == 0:
                txt_body = map(lambda s: "- " + s, self.get_todo())
            else:
                for nick in eta:
                    txt_body.append("%s: %s" % (nick, eta[nick]))

            self.lock.acquire()
            self.surface.fill((0, 0, 0))

            self.surface.blit(self.font_heading.render(txt_head, True, green), rect)
            rect[1] = rect[1] + self.font_heading.size(txt_head)[1]

            for line in txt_body:
                self.surface.blit(self.font.render(line, True, green), rect)
                rect[1] = rect[1] + self.font.size(line)[1]

            self.lock.release()
            time.sleep(5)

