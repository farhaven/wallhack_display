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

screen_size = (1024, 768)
rpcserver   = 'http://cube.lan:4254'

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
    eta = ETA(((screen_size[0] / 3) + 100, (screen_size[1] / 3) * 2), eta_font, rpcserver)
    eta.start()

    available_font = pygame.font.SysFont("Liberation Mono, Monospace", 50)
    avail = Available(((screen_size[0] / 3) * 2 - 100, (screen_size[1] / 3) * 2 + 60), available_font, rpcserver)
    avail.start()

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

        avail.lock.acquire()
        screen.blit(avail.surface, (0, 0))
        avail.lock.release()

        pygame.display.flip()
        time.sleep(0.001)
