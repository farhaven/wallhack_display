from __future__ import division

import threading
import time
import math

from pygame import draw, surface

black = (0, 0, 0)
green = (0, 255, 0)

def rotate_vector(v, a):
    return (v[0] * math.cos(a) - v[1] * math.sin(a),
            v[0] * math.sin(a) + v[1] * math.cos(a))

class Subraum(threading.Thread):
    daemon = True
    iter = 0
    def __init__(self, dim, clock):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.surface = surface.Surface(dim)
        self.surface.set_colorkey(black)
        self.dim = dim
        self.clock = clock

    def run(self):
        radius = 70
        (xoff, yoff) = (self.dim[0] / 2, self.dim[1] / 2)
        (xscale, yscale) = (1, 0.5)
        while True:
            if self.iter > 2 * math.pi:
                self.iter = 0
            self.iter += 0.01

            (x1, y1) = (math.cos(self.iter) * xscale, math.sin(self.iter) * yscale)
            (x2, y2) = (math.cos(self.iter + math.pi / 2) * xscale, math.sin(self.iter + math.pi / 2) * yscale)
            (x3, y3) = (int(-x1 * radius + xoff), int(-y1 * radius + yoff))
            (x4, y4) = (int(-x2 * radius + xoff), int(-y2 * radius + yoff))
            (x1, y1) = (int(x1 * radius + xoff), int(y1 * radius + yoff))
            (x2, y2) = (int(x2 * radius + xoff), int(y2 * radius + yoff))

            self.lock.acquire()
            self.surface.fill(black)

            draw.lines(self.surface, green, True, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], 3)
            draw.lines(self.surface, green, True, [(x1, y1 - radius), (x2, y2 - radius), (x3, y3 - radius), (x4, y4 - radius)], 3)
            draw.line(self.surface, green, (x1, y1), (x1, y1 - radius), 3)
            draw.line(self.surface, green, (x2, y2), (x2, y2 - radius), 3)
            draw.line(self.surface, green, (x3, y3), (x3, y3 - radius), 3)
            draw.line(self.surface, green, (x4, y4), (x4, y4 - radius), 3)

            vdot = rotate_vector((0, 0.6), self.iter)
            draw.circle(self.surface, green, (int(vdot[0] * radius * xscale + xoff), int(vdot[1] * radius * yscale + yoff - radius)), 5)

            self.clock.lock.acquire()
            self.surface.blit(self.clock.surface, (self.dim[0] - self.clock.get_dimensions()[0] - 10, 0))
            self.clock.lock.release()

            self.lock.release()
            time.sleep(0.005)
