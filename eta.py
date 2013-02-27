import socket
import jsonrpclib
import pygame
import threading
import time

jsonrpclib.config.version = 1.0

black = (0, 0, 0)
green = (0, 255, 0)

class ETAListenClient(threading.Thread):
	daemon = True
	def __init__(self, conn, server):
		threading.Thread.__init__(self)
		self.conn = conn
		self.server = server
		self.data = ""

	def run(self):
		while True:
			d = self.conn.recv(1)
			if not d:
				break
			self.data += d
		self.server.append(self.data)
		self.conn.close()

class ETAListen(threading.Thread):
	daemon = True
	port   = 12345

	def __init__(self):
		threading.Thread.__init__(self)
		self.data = []
		self.lock = threading.Lock()
		self.socket = socket.socket(socket.AF_INET)
		while True:
			try:
				self.socket.bind(("0.0.0.0", self.port))
				print("Listening to " + str(self.port))
				break
			except socket.error as err:
				print(str(err))
				self.port += 1
		self.socket.listen(0)

	def append(self, data):
		# self.lock.acquire()
		for d in data.strip().split('\n'):
			self.data.append(d.replace('\t', ' '))
		self.data = self.data[-10:]
		# self.lock.release()

	def get(self):
		return self.data

	def run(self):
		while True:
			(conn, addr) = self.socket.accept()
			c = ETAListenClient(conn, self)
			c.start()

class ETA(threading.Thread):
	daemon = True
	timeout = 0
	def __init__(self, dim, rpcserver, clock):
		threading.Thread.__init__(self)
		self.surface = pygame.surface.Surface(dim)
		self.surface.set_colorkey(black)
		self.font_heading = pygame.font.SysFont("Liberation Mono, Monospace", 65)
		self.font = pygame.font.SysFont("Liberation Mono, Monospace", 55)
		self.lock = threading.Lock()
		self.rpcserver = rpcserver
		self.server = jsonrpclib.Server(rpcserver)
		self.clock = clock
		self.dim = dim
		self.nw = ETAListen()
		self.nw.start()

	def get_eta(self):
		try:
			return self.server.who()[unicode('eta')]
		except:
			return {}
			# return { "error": "server not reachable", "tried": self.rpcserver, "time": str(time.time()) }

	def get_timeout(self):
		return self.timeout

	def run(self):
		green = (0, 255, 0)
		while True:
			eta  = self.get_eta()
			data = self.nw.get()
			self.timeout = len(eta) * 0.5 + (len(data) + 5)

			rect = [ 20, 20 ]

			# self.lock.acquire()
			self.surface.fill(black)

			if len(eta) != 0:
				self.surface.blit(self.font_heading.render("ETA:", True, green), rect)
				rect[1] = rect[1] + self.font_heading.size("ETA:")[1]
				for nick in eta:
					s = "%s: %s" % (nick, eta[nick])
					self.surface.blit(self.font.render(s, True, green), rect)
					rect[1] = rect[1] + self.font.size(s)[1]
				rect[1] = rect[1] + self.font.size("foo")[1]

			if len(data) != 0:
				self.surface.blit(self.font_heading.render("NOISE (" + str(self.nw.port) + "):", True, green), rect)
				rect[1] = rect[1] + self.font_heading.size("N")[1]
				for t in data:
					self.surface.blit(self.font.render(t, True, green), rect)
					rect[1] = rect[1] + self.font.size(t)[1]
			else:
				self.surface.blit(self.font_heading.render(str(self.nw.port), True, green), rect)

			# self.clock.lock.acquire()
			self.surface.blit(self.clock.surface, (self.dim[0] - self.clock.get_dimensions()[0] - 10, 0))
			# self.clock.lock.release()
			# self.lock.release()
			time.sleep(5)
