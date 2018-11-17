from packet import Packet
import time
import collections


class Link(object):
    def __init__(self, buffer_in_size, buffer_out_size, delay):
        self.__delay = delay
        self.__buffer_in = collections.deque(maxlen=buffer_in_size)
        self.__buffer_out = collections.deque(maxlen=buffer_out_size)
        
    def add_pkg_to_buffer_in(self, pkg):
        self.__buffer_in.append(pkg)
        
    def transmit(self):
        pkg = self.__buffer_in.pop()
        time.sleep(self.__delay)
        self.__buffer_out.append(pkg)
        
    def pick_pkg_from_buffer_out(self):
        return self.__buffer_out.pop()