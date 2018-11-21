from Host import Host
from Packet import Packet

  class Flow(object):
    def __init__(self, id, src, dest, size, start_time, packet_size):
        self.id = id
        self.src = src
        self.dest = dest
        self.size = size
        self.start_time = start_time
        self.cnt = 0
        self.window_size = 3
        self.packet_size = packet_size
        self.pkt_pool = {}

    def generate_packet(self):
        number_of_packet = self.size/self.packet_size
        prefix = 'pkt'
        for i in range(number_of_packet):
            self.pkt_pool[prefix+str(i)] = Packet(self.id+prefix+str(i), 'data', self.packet_size, self.src, self.dest)
        return

    def send_packet(self):
        self.src.send_packet()
        return
