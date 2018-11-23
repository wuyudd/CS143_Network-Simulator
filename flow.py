import heapq
import global_var
from host import *
from packet import *
from simulator import *
import event_type


class Flow(object):
    def __init__(self, id, src, dest, size, start_time, packet_size):
        self.id = id
        self.src = src
        self.dest = dest
        self.size = size
        self.start_time = start_time
        self.cnt = 0
        self.window_size = 64
        self.packet_size = packet_size
        self.pkt_pool = {}
        self.num_pkt_send = 0

    def generate_packet(self):
        number_of_packet = int(self.size/self.packet_size)
        prefix = 'pkt'
        for i in range(number_of_packet):
            # pkt: id, type, size, end1, end2, pos
            self.pkt_pool[prefix+str(i)] = Packet(self.id+prefix+str(i), 'data', self.packet_size, self.src, self.dest)
            # print(self.pkt_pool)
        return

    def send_packet(self,pkt):
        self.src.send_packet(pkt)
        #self.cnt+=1
        event = event_type.TimeOut(pkt, self, global_var.timestamp+1) # constant need to be modified
        heapq.heappush(global_var.queue, event)
        return

    def receive_ack(self, ack):
        l = ack.id.split('pkt')
        l1 = l[1].split('ack')
        name = 'pkt'+l1[0]
        self.pkt_pool[name].set_ack(1)  # find the packet and mark it acknowledged
        self.cnt -= 1
        self.add_event()

    def add_event(self):   # start_time & index
        i = 0
        while self.num_pkt_send < len(self.pkt_pool) and self.cnt < self.window_size:
            index = self.num_pkt_send
            curr_link_rate = self.src.outgoing_links.link_rate
            start_time = global_var.timestamp #+ i * (8/(curr_link_rate*1024))
            event = event_type.SendFromFlow(self, index, start_time)
            heapq.heappush(global_var.queue, event)
            self.cnt += 1
            self.num_pkt_send += 1
            i += 1

    def time_out(self, pkt):
        if pkt.get_ack()==0:
            self.cnt -= 1   # need to resend pck


