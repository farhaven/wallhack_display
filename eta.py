import jsonrpclib
import pygame
import sys
import time
import random
import math

screen_size = (1024, 768)
rpcserver   = 'http://cube.lan:4254'
delay       = 5

def render_eta(font, surf, eta, color, rect):
    for nick in eta:
        s = "%s: %s" % (nick, eta[nick])
        surf.blit(font.render(s, False, color), rect)
        rect[1] = rect[1] + font.size(s)[1]

def random_color():
    return (int(random.random() * 128), int(random.random() * 128), int(random.random() * 128))

def render_available(font, surf, available):
    for nick in available:
        size = font.size(nick)
        s = pygame.Surface(size)
        s.set_colorkey((0, 0, 0))
        s.fill((0, 0, 0))
        s.blit(font.render(nick, False, random_color()), (0, 0))
        surf.blit(pygame.transform.rotate(s, random.random() * 360),
                  (random.randint(0, screen_size[0]), random.randint(0, screen_size[1])))

if __name__ == "__main__":
    jsonrpclib.config.version = 1.0
    server = jsonrpclib.Server(rpcserver)
    pygame.init()
    random.seed()

    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    loopcount = 0
    font = pygame.font.SysFont("Liberation Mono, Monospace", 50)

    while True:
        loopcount = (loopcount + 1) % delay
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        if pygame.key.get_pressed()[pygame.K_q]:
            sys.exit()

        if loopcount == 0:
            pygame.display.flip()
            time.sleep(1)
            continue

        users = server.who()
        screen.fill((0, 0, 0))
        screen.blit(font.render("ETA:", False, (255, 255, 255)), [20, 20])
        render_available(font, screen, users[unicode('available')])
        render_eta(font, screen, users[unicode('eta')], (255, 255, 255), [20, font.size("ETA")[1] + 30])
