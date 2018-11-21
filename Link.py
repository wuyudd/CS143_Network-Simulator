import collections


class Link(object):
    def __init__(self, id, transmission_delay, propagation_delay, buffer_size, start, end):
        self.id = id
        self.size = buffer_size
        self.buffer = {}
        self.on_the_link = {}
        self.transmission_delay = transmission_delay
        self.propagation_delay = propagation_delay
        self.start = start
        self.end = end

    def add_packet_to_buffer(self, pkt):
        if len(self.buffer) < self.size:
            self.buffer[pkt.id] = pkt

    def transmit(self, pkt):
        if pkt.id in self.buffer:
            self.on_the_link[pkt.id] = self.buffer.pop(pkt.id)

    def pick_packet_from_link(self, pkt):
        if pkt.id in self.on_the_link:
            pkt = self.on_the_link.pop(pkt.id)
        return pkt

