import threading
import pygame
import time
import math

class Chaos(threading.Thread):
    def __init__(self, dim):
        threading.Thread.__init__(self)
        self.daemon = True
        self.lock = threading.Lock()
        self.surface = pygame.surface.Surface(dim)
        self.surface.set_colorkey((0, 0, 0))
        self.dim = dim
        self.iter = 0

    def run(self):
        radius_bottom = 150
        radius_top    = 65
        white = (255, 255, 255)
        while True:
            if self.iter > math.pi / 2:
                self.iter = 0
            self.iter = self.iter + 0.01

            self.lock.acquire()
            self.surface.fill((0, 0, 0))

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

            pygame.draw.lines(self.surface, white, True, [pos1_b, pos3_b, pos2_b, pos4_b])
            pygame.draw.line(self.surface, white, pos1_b, pos2_b)
            pygame.draw.line(self.surface, white, pos3_b, pos4_b)

            pygame.draw.lines(self.surface, white, True, [pos1_t, pos3_t, pos2_t, pos4_t])
            pygame.draw.line(self.surface, white, pos1_t, pos2_t)
            pygame.draw.line(self.surface, white, pos3_t, pos4_t)

            pygame.draw.line(self.surface, white, pos1_b, pos1_t)
            pygame.draw.line(self.surface, white, pos2_b, pos2_t)
            pygame.draw.line(self.surface, white, pos3_b, pos3_t)
            pygame.draw.line(self.surface, white, pos4_b, pos4_t)

            eye = (int(self.dim[0] / 2), self.dim[0] / 2 - 60)
            pygame.draw.line(self.surface, white, (eye[0] - 40, eye[1]),      (eye[0] + 40,  eye[1]))
            pygame.draw.line(self.surface, white, (eye[0] - 40, eye[1] - 80), (eye[0] + 40,  eye[1] - 80))

            pygame.draw.line(self.surface, white, (eye[0] - 40, eye[1] - 80), (eye[0] - 140, eye[1] - 40))
            pygame.draw.line(self.surface, white, (eye[0] - 40, eye[1]),      (eye[0] - 140, eye[1] - 40))

            pygame.draw.line(self.surface, white, (eye[0] + 40, eye[1]),      (eye[0] + 140, eye[1] - 40))
            pygame.draw.line(self.surface, white, (eye[0] + 40, eye[1] - 80), (eye[0] + 140, eye[1] - 40))

            pygame.draw.line(self.surface, white, (eye[0] - 20, eye[1]),      (eye[0] - 40,  eye[1] - 20))
            pygame.draw.line(self.surface, white, (eye[0] - 40, eye[1] - 20), (eye[0] - 40,  eye[1] - 60))
            pygame.draw.line(self.surface, white, (eye[0] - 40, eye[1] - 60), (eye[0] - 20,  eye[1] - 80))

            pygame.draw.line(self.surface, white, (eye[0] + 20, eye[1]),      (eye[0] + 40,  eye[1] - 20))
            pygame.draw.line(self.surface, white, (eye[0] + 40, eye[1] - 20), (eye[0] + 40,  eye[1] - 60))
            pygame.draw.line(self.surface, white, (eye[0] + 40, eye[1] - 60), (eye[0] + 20,  eye[1] - 80))

            pygame.draw.line(self.surface, white, (eye[0] - 15, eye[1] - 25), (eye[0] + 15,  eye[1] - 25))
            pygame.draw.line(self.surface, white, (eye[0] - 15, eye[1] - 25), (eye[0] - 15,  eye[1] - 55))
            pygame.draw.line(self.surface, white, (eye[0] - 15, eye[1] - 55), (eye[0] + 15,  eye[1] - 55))
            pygame.draw.line(self.surface, white, (eye[0] + 15, eye[1] - 55), (eye[0] + 15,  eye[1] - 25))

            self.lock.release()

            time.sleep(0.005)
