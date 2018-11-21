import heapq
from Host import Host
from Packet import Packet
from Simulator import Simulator
import EventType


class Flow(object):
    Simulator.timestamp
      Simulator.queue
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

    def send_packet(self,pkt):
        self.src.send_packet()
        self.cnt+=1
        event = EventType.TimeOut(pkt,Simulator.timestamp()+*****constanttime)
        heapq.heappush(Simulator.queue,(Simulator.timestamp()+*****constanttime, event))
        return

    def receive_ack(self,ack):
        self.pkt_pool.get(ack.pos).set_ack(1)  #find the packet and mark it acknowledged
        self.cnt-=1

    def add_event(self):   # start_time & index modify
        while self.cnt<=self.window_size:
            index = 1
            start_time = 1.0
            event = EventType.send_from_flow(self, index, start_time)
            heapq.heappush(Simulator.queue, (start_time, event))

    def time_out(self, pkt):
        if pkt.get_ack()==0:
            self.cnt -= 1   #need to resend pck


