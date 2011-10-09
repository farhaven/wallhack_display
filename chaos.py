import threading
import pygame
import time
import math
import random
import jsonrpclib

jsonrpclib.config.version = 1.0
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
darkgreen = (0, 127, 0)

class Chaos_background(threading.Thread):
    daemon = True
    def __init__(self, dim, rpcserver):
        threading.Thread.__init__(self)
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey(black)
        self.dim = dim
        self.font = pygame.font.SysFont("Liberation Mono, Monospace", 55)
        self.rpcserver = rpcserver
        self.server = jsonrpclib.Server(rpcserver)
        self.lock = threading.Lock()

    def get_available(self):
        try:
            return self.server.who()[unicode('available')]
        except Exception as err:
            return [ "fix", self.rpcserver, str(err) ]

    def run(self):
        while True:
            self.lock.acquire()
            self.surface.fill(black)
            print(str(self.get_available()))
            for nick in self.get_available():
                self.surface.blit(pygame.transform.rotate(self.font.render(nick, False, darkgreen), random.random() * 360),
                          (random.randint(0, self.dim[0] - self.font.size('foobar')[0]), random.randint(0, self.dim[1] - self.font.size('foobar')[1])))
            self.lock.release()
            time.sleep(5)

class Chaos(threading.Thread):
    iter = 0
    daemon = True
    def __init__(self, dim, rpcserver, clock):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey(black)
        self.dim = dim
        self.clock = clock
        self.rpcserver = rpcserver
        self.background = Chaos_background(dim, rpcserver)

    def run(self):
        radius_bottom = 150
        radius_top    = 65
        s = pygame.surface.Surface((80, 80))
        s.fill(black)
        self.background.start()
        while True:
            if self.iter > math.pi / 2:
                self.iter = 0
            self.iter = self.iter + 0.01

            self.lock.acquire()
            self.surface.fill(black)
            self.background.lock.acquire()
            self.surface.blit(self.background.surface, (0, 0))
            self.background.lock.release()

            pos1_b = (int(math.cos(self.iter) * radius_bottom), int(math.sin(self.iter) * radius_bottom * 0.2))
            pos1_t = (int(math.cos(self.iter) * radius_top), int(math.sin(self.iter) * radius_top * 0.2))
            pos2_b = (self.dim[0] / 2 - pos1_b[0], self.dim[1] / 2 - pos1_b[1] + 150)
            pos2_t = (self.dim[0] / 2 - pos1_t[0], self.dim[1] / 2 - pos1_t[1] - 30)
            pos1_b = (self.dim[0] / 2 + pos1_b[0], self.dim[1] / 2 + pos1_b[1] + 150)
            pos1_t = (self.dim[0] / 2 + pos1_t[0], self.dim[1] / 2 + pos1_t[1] - 30)

            pos3_b = (int(math.cos(self.iter + math.pi / 2) * radius_bottom), int(math.sin(self.iter + math.pi / 2) * radius_bottom * 0.2))
            pos3_t = (int(math.cos(self.iter + math.pi / 2) * radius_top), int(math.sin(self.iter + math.pi / 2) * radius_top * 0.2))
            pos4_b = (self.dim[0] / 2 - pos3_b[0], self.dim[1] / 2 - pos3_b[1] + 150)
            pos4_t = (self.dim[0] / 2 - pos3_t[0], self.dim[1] / 2 - pos3_t[1] - 30)
            pos3_b = (self.dim[0] / 2 + pos3_b[0], self.dim[1] / 2 + pos3_b[1] + 150)
            pos3_t = (self.dim[0] / 2 + pos3_t[0], self.dim[1] / 2 + pos3_t[1] - 30)

            pygame.draw.lines(self.surface, green, True, [pos1_b, pos3_b, pos2_b, pos4_b], 3)
            pygame.draw.line(self.surface, green, pos1_b, pos2_b, 3)
            pygame.draw.line(self.surface, green, pos3_b, pos4_b, 3)

            pygame.draw.lines(self.surface, green, True, [pos1_t, pos3_t, pos2_t, pos4_t], 3)
            pygame.draw.line(self.surface, green, pos1_t, pos2_t, 3)
            pygame.draw.line(self.surface, green, pos3_t, pos4_t, 3)

            pygame.draw.line(self.surface, green, pos1_b, pos1_t, 3)
            pygame.draw.line(self.surface, green, pos2_b, pos2_t, 3)
            pygame.draw.line(self.surface, green, pos3_b, pos3_t, 3)
            pygame.draw.line(self.surface, green, pos4_b, pos4_t, 3)

            eye = (int(self.dim[0] / 2), int(self.dim[0] / 2) - 200)

            pygame.draw.circle(self.surface, green, (eye[0], eye[1] - 40), 40, 3)
            pygame.draw.circle(self.surface, green, (eye[0], eye[1] - 40), 15)

            for i in [0, math.pi / 8, math.pi / 2, math.pi / 4 + math.pi / 2]:
                pos1_b = (int(math.cos(self.iter + i) * 40), int(math.sin(self.iter + i) * 40))
                pos2_b = (int(math.cos(self.iter + i + math.pi / 2) * 40), int(math.sin(self.iter + i + math.pi / 2) * 40))
                pos3_b = (eye[0] - pos1_b[0], eye[1] - pos1_b[1] - 40)
                pos4_b = (eye[0] - pos2_b[0], eye[1] - pos2_b[1] - 40)
                pos1_b = (eye[0] + pos1_b[0], eye[1] + pos1_b[1] - 40)
                pos2_b = (eye[0] + pos2_b[0], eye[1] + pos2_b[1] - 40)

                pygame.draw.line(self.surface, green, (eye[0], eye[1] - 40), pos1_b, 2)
                pygame.draw.line(self.surface, green, (eye[0], eye[1] - 40), pos2_b, 2)
                pygame.draw.line(self.surface, green, (eye[0], eye[1] - 40), pos3_b, 2)
                pygame.draw.line(self.surface, green, (eye[0], eye[1] - 40), pos4_b, 2)

            pygame.draw.line(self.surface, green, (eye[0] - 40, eye[1]),      (eye[0] + 40,  eye[1]), 3)
            pygame.draw.line(self.surface, green, (eye[0] - 40, eye[1] - 80 * (math.sin(self.iter * 2))), (eye[0] + 40,  eye[1] - 80 * (math.sin(self.iter * 2))), 3)

            pygame.draw.line(self.surface, green, (eye[0] - 40, eye[1] - 80 * (math.sin(self.iter * 2))), (eye[0] - 140, eye[1] - 40), 3)
            pygame.draw.line(self.surface, green, (eye[0] - 40, eye[1]),      (eye[0] - 140, eye[1] - 40), 3)

            pygame.draw.line(self.surface, green, (eye[0] + 40, eye[1]),      (eye[0] + 140, eye[1] - 40), 3)
            pygame.draw.line(self.surface, green, (eye[0] + 40, eye[1] - 80 * (math.sin(self.iter * 2))), (eye[0] + 140, eye[1] - 40), 3)

            self.surface.blit(s, (eye[0] - 40, eye[1] - (80 * (math.sin(self.iter * 2))) - 81))
            pygame.draw.line(self.surface, green, (eye[0] - 40, eye[1] - 80), (eye[0] + 40, eye[1] - 80), 3)
            pygame.draw.line(self.surface, green, (eye[0] - 40, eye[1] - 80), (eye[0] - 140, eye[1] - 40), 3)
            pygame.draw.line(self.surface, green, (eye[0] + 40, eye[1] - 80), (eye[0] + 140, eye[1] - 40), 3)

            self.clock.lock.acquire()
            self.surface.blit(self.clock.surface, (self.dim[0] - self.clock.get_dimensions()[0] - 10, 0))
            self.clock.lock.release()
            self.lock.release()

            time.sleep(0.005)
