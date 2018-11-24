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
        self.ack_pool = {}
        self.sending_queue = collections.deque()
        self.timeout_queue = collections.deque()
        self.num_pkt_send = 0

    def generate_packet(self):
        number_of_packet = int(self.size/self.packet_size)
        prefix = 'pkt'
        for i in range(number_of_packet):
            # pkt: id, type, size, end1, end2, pos
            cur_pkt = Packet(self.id + prefix + str(i), 'data', self.packet_size, self.src, self.dest)
            self.pkt_pool[prefix+str(i)] = cur_pkt
            self.ack_pool[cur_pkt.id] = False
            self.sending_queue.append(cur_pkt)
            # print(self.pkt_pool)
        return

    def send_packet(self,pkt):
        self.src.send_packet(pkt)
        event = event_type.TimeOut(pkt, self, global_var.timestamp+2) # constant need to be modified
        heapq.heappush(global_var.queue, event)
        return

    def receive_ack(self, ack):

        pkt_name = ack.id.split('ack')[0]
        self.ack_pool[pkt_name] = True  # find the packet and mark it acknowledged
        self.cnt -= 1
        #print('++++++++++++++++++++++++++++++++++++++++++')
        #print(self.ack_pool)
        self.add_event()

    def add_event(self):   # start_time & index
        i = 0
        while self.timeout_queue and self.cnt < self.window_size:
            #index = self.num_pkt_send
            curr_link_rate = self.src.outgoing_links.link_rate
            start_time = global_var.timestamp #+ i * (8/(curr_link_rate*1024))
            pkt = self.timeout_queue.popleft()
            event = event_type.SendFromFlow(self, pkt, start_time)
            heapq.heappush(global_var.queue, event)
            self.cnt += 1
            i += 1

        while self.sending_queue and self.cnt < self.window_size:
            #index = self.num_pkt_send
            curr_link_rate = self.src.outgoing_links.link_rate
            start_time = global_var.timestamp #+ i * (8/(curr_link_rate*1024))
            pkt = self.sending_queue.popleft()
            event = event_type.SendFromFlow(self, pkt, start_time)
            heapq.heappush(global_var.queue, event)
            self.cnt += 1
            i += 1

    def time_out(self, pkt):
        if not self.ack_pool[pkt.id]:
            self.cnt -= 1   # need to resend pck
            new_pkt = Packet(pkt.id, pkt.type, pkt.size, pkt.start, pkt.end)
            self.timeout_queue.append(new_pkt)
            self.add_event()



