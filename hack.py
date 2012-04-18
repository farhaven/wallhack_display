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
from subraum import Subraum

screen_size = (1024, 768)
rpcserver   = 'http://cube.lan:4254'

green = (0, 255, 0)
darkgreen = (0, 31, 0)
black = (0, 0, 0)

if __name__ == "__main__":
	pygame.init()

	# screen = pygame.display.set_mode(screen_size)
  screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
	pygame.display.set_caption("Wallhack")

	background = pygame.surface.Surface(screen_size)
	background.fill(black)

	pygame.draw.rect(background, green, (0, 0, screen_size[0], screen_size[1]), 4)

	clock = Clock()
	clock.start()

	eta = ETA(screen_size, rpcserver, clock)
	eta.start()

	chaos = Chaos(screen_size, rpcserver, clock)
	chaos.start()

	subraum = Subraum(screen_size, clock)
	# subraum.start()

	modules = [ (eta, eta.get_timeout), (chaos, lambda: 4) ]
	mod = 0
	mod_timer = time.time()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		if pygame.key.get_pressed()[pygame.K_q]:
			sys.exit()
		elif pygame.key.get_pressed()[pygame.K_f]:
			pygame.display.toggle_fullscreen()

		screen.fill(black)
		screen.blit(background, (0, 0))

		if time.time() > mod_timer + modules[mod][1]():
			mod_timer = time.time()
			mod = mod + 1
			if mod >= len(modules):
				mod = 0

		modules[mod][0].lock.acquire()
		screen.blit(modules[mod][0].surface, (0, 0))
		modules[mod][0].lock.release()

		for y in range(1, screen_size[1], 5):
			pygame.draw.line(screen, darkgreen, (0, y), (screen_size[0], y), 1)

		pygame.display.flip()
		time.sleep(0.005)
