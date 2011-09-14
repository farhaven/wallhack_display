import pygame
import sys
import time
import threading
import jsonrpclib
import random
import math

from available import Available
from clock import Clock
from eta import ETA
from chaos import Chaos

screen_size = (1024, 768)
rpcserver   = 'http://cube.lan:4254'

green = (0, 255, 0)
darkgreen = (0, 31, 0)
black = (0, 0, 0)

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode(screen_size) #, pygame.FULLSCREEN)
    pygame.display.set_caption("Wallhack")

    background = pygame.surface.Surface(screen_size)
    background.fill((0, 0, 0))

    pygame.draw.line(background, green, ((screen_size[0] / 3) * 2 - 100, 0), ((screen_size[0] / 3) * 2 - 100, screen_size[1]), 4)
    pygame.draw.line(background, green, (0, (screen_size[1] / 3) * 2 + 60), ((screen_size[0] / 3) * 2 - 100, (screen_size[1] / 3) * 2 + 60), 4)
    pygame.draw.rect(background, green, (0, 0, screen_size[0], screen_size[1]), 4)

    clock = Clock(((screen_size[0] / 3) * 2 - 80, (screen_size[1] / 3)))
    clock.start()

    eta = ETA(((screen_size[0] / 3) + 100, (screen_size[1] / 3) * 2), rpcserver)
    eta.start()

    # avail = Available(((screen_size[0] / 3) * 2 - 100, (screen_size[1] / 3) * 2 + 60), rpcserver)
    # avail.start()

    chaos = Chaos(((screen_size[0] / 3) * 2 - 100, (screen_size[1] / 3) * 2 + 60))
    chaos.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        if pygame.key.get_pressed()[pygame.K_q]:
            sys.exit()

        screen.fill(black)
        screen.blit(background, (0, 0))

        clock.lock.acquire()
        screen.blit(clock.surface, (25, (screen_size[1] / 3) * 2 + 70))
        clock.lock.release()

        eta.lock.acquire()
        screen.blit(eta.surface, ((screen_size[0] / 3) * 2 - 90, 10))
        eta.lock.release()

        # avail.lock.acquire()
        # screen.blit(avail.surface, (0, 0))
        # avail.lock.release()

        chaos.lock.acquire()
        screen.blit(chaos.surface, (0, 0))
        chaos.lock.release()

        for l in range(1, screen_size[1], 5):
            pygame.draw.line(screen, darkgreen, (0, l), (screen_size[0], l), 1)

        pygame.display.flip()
        time.sleep(0.001)
