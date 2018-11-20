class Link(object):
	def __init__(self, transmission_delay, propagation_delay, buffer_size,start,end):
		self.size = buffer_size
		self.buffer = collections.deque()
		self.on_the_link = collections.deque()
		self.transmission_delay = transmission_delay
		self.propagation_delay = propagation_delay
		self.start = start
		self.end = end

	def add_pkg_to_buffer(self, pkg):
		if len(self.buffer) < self.size:
			self.buffer.append(pkg)

	def transmit(self):
		pkg = self.buffer.popleft()
		time.sleep(self.delay)
		self.on_the_link.append(pkg)

	def pick_pkg_from_link(self):
		return self.on_the_link.popleft()










