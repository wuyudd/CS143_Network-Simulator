import collections
import heapq
import global_var
import global_consts
import router
from simulator import *
from event import *
import event_type


class Link(object):
    def __init__(self, id, link_rate, link_delay, buffer_size, start, end):
        # all time is in second, link rate is in Mbps
        # all data_size is in byte
        self.id = id
        self.cur_size = 0
        self.max_size = buffer_size*1024
        self.buffer = collections.deque()
        self.on_the_link = collections.deque()
        self.link_rate = link_rate
        self.link_delay = link_delay
        self.start = start
        self.end = end
        self.plot_link_buffer_time = []
        self.plot_link_buffer = []

    def __lt__(self, other):
        return self.id < other.id

    def add_packet_to_buffer(self, pkt):
        if pkt.type != 'hello' and isinstance(self.start, router.Router):
            self.start.out_pkt_size[self.id] += pkt.size
        if self.cur_size + pkt.size <= self.max_size:
            self.buffer.append(pkt)
            # plot function
            self.plot_link_buffer_time.append(global_var.timestamp)
            self.plot_link_buffer.append(self.cur_size)
            # cur_event is a new event to move packet from buffer to link
            expected_waiting_time = self.cur_size*8/(self.link_rate*1024*1024)#self.data_pkt_cnt * 8/(1024*1) + self.ack_pkt_cnt / (2048*1)  # in s
            cur_event = event_type.FetchFromBuffer(self, global_var.timestamp+expected_waiting_time)
            heapq.heappush(global_var.queue, cur_event)
            self.cur_size += pkt.size

    def buffer_to_link(self):
        cur_event = event_type.FetchFromLink(self, global_var.timestamp+self.link_delay)
        heapq.heappush(global_var.queue, cur_event)
        pkt = self.buffer.popleft()
        self.cur_size -= pkt.size
        self.on_the_link.append(pkt)

        # plot function
        self.plot_link_buffer_time.append(global_var.timestamp)
        self.plot_link_buffer.append(self.cur_size)


    def fetch_from_link(self):
        self.end.receive_packet(self.on_the_link.popleft(), self)
