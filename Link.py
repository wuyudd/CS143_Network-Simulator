import time
import collections


class Link(object):
    def __init__(self, buffer_size, delay):
        self.delay = delay
        self.size = buffer_size
        self.buffer = collections.deque()
        self.on_the_link = collections.deque()
        
    def add_pkg_to_buffer(self, pkg):
        self.buffer.append(pkg)
        
    def transmit(self):
        pkg = self.buffer.popleft()
        time.sleep(self.delay)
        self.on_the_link.append(pkg)

    def pick_pkg_from_link(self):
        return self.on_the_link.popleft()

