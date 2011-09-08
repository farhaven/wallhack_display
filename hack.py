import pygame
import sys
import time
import threading
import jsonrpclib
import json

screen_size = (1024, 768)
rpcserver   = 'http://cube.lan:4254'

class Clock(threading.Thread):
    def __init__(self, dim, font):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.font = font
        self.lock = threading.Lock()
        self.daemon = True

    def run(self):
        while self.is_alive():
            s = time.strftime("%H:%M")
            self.lock.acquire()
            self.surface.fill((0, 0, 0))
            self.surface.blit(self.font.render(s, True, (255, 255, 255)), (0, 0))
            self.lock.release()
            time.sleep(60)

class ETA(threading.Thread):
    def __init__(self, dim, font):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.font = font
        self.lock = threading.Lock()
        self.daemon = True
        jsonrpclib.config.version = 1.0
        self.server = jsonrpclib.Server(rpcserver)

    def get_eta(self):
        try:
            return self.server.who()[unicode('eta')]
        except:
            print("server not reachable. trying test.json instead")
            try:
                fd = open('test.json', 'r')
                e = json.load(fd)
                fd.close()
                return e
            except Exception as e:
                print("loading test.json failed: " + str(e))
                return { "farhaven": "1337 - foobar!", "fnord": "2342" }

    def run(self):
        eta = self.get_eta()
        rect = [0, 0]
        self.lock.acquire()
        self.surface.fill((0, 0, 0))
        for nick in eta:
            s = "%s: %s" % (nick, eta[nick])
            self.surface.blit(self.font.render(s, True, (255, 255, 255)), rect)
            rect[1] = rect[1] + self.font.size(s)[1]
        self.lock.release()
        time.sleep(5)

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    background = pygame.surface.Surface(screen_size)
    background.fill((0, 0, 0))

    pygame.draw.line(background, (255, 255, 255), ((screen_size[0] / 3) * 2 - 100, 0), ((screen_size[0] / 3) * 2 - 100, screen_size[1]))
    pygame.draw.line(background, (255, 255, 255), (0, (screen_size[1] / 3) * 2 + 60), ((screen_size[0] / 3) * 2 - 100, (screen_size[1] / 3) * 2 + 60))
    pygame.draw.rect(background, (255, 255, 255), (0, 0, screen_size[0], screen_size[1]), 1)

    clock_font = pygame.font.SysFont("Liberation Mono, Monospace", 175)
    clock = Clock(((screen_size[0] / 3) * 2 - 80, (screen_size[1] / 3)), clock_font)
    clock.start()

    eta_font = pygame.font.SysFont("Liberation Mono, Monospace", 25)
    eta = ETA(((screen_size[0] / 3) + 100, (screen_size[1] / 3) * 2), eta_font)
    eta.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        if pygame.key.get_pressed()[pygame.K_q]:
            sys.exit()

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        clock.lock.acquire()
        screen.blit(clock.surface, (25, (screen_size[1] / 3) * 2 + 70))
        clock.lock.release()

        eta.lock.acquire()
        screen.blit(eta.surface, ((screen_size[0] / 3) * 2 - 90, 10))
        eta.lock.release()

        pygame.display.flip()
