import collections
import heapq
import global_var
import global_consts
import router
import host
from simulator import *
from event import *
import event_type


class Link(object):
    def __init__(self, id, link_rate, link_delay, buffer_size, start, end):
        # all time is in second
        # all link rate is in Mbps
        # all data_size is in byte
        self.id = id
        self.cur_size = 0.0
        self.max_size = buffer_size*1024
        self.link_lock = False

        self.buffer = collections.deque()
        self.on_the_link = collections.deque()

        self.link_rate = link_rate
        self.link_delay = link_delay

        self.start = start
        self.end = end

        self.plot_link_buffer_time = []
        self.plot_link_buffer = []

        self.plot_link_rate = []
        self.plot_link_rate_size = 0.0
        self.num_lost_pkt = 0.0

    def __lt__(self, other):
        return self.id < other.id

    def add_packet_to_buffer(self, pkt):
        if pkt.type != 'hello' and isinstance(self.start, router.Router):
            self.start.out_pkt_size[self.id] += pkt.size

        if self.cur_size + pkt.size <= self.max_size:
            self.buffer.append(pkt)
            self.cur_size += pkt.size
            self.plot_link_buffer_time.append(global_var.timestamp)
            self.plot_link_buffer.append(self.cur_size/1024)
            if self.link_lock == False:
                expected_waiting_time = pkt.size*8/(self.link_rate*1024*1024)
                cur_event = event_type.FetchFromBuffer(self, global_var.timestamp + expected_waiting_time)
                heapq.heappush(global_var.queue, cur_event)
                self.link_lock = True
        else:
            self.num_lost_pkt += 1

    def buffer_to_link(self):


        cur_event = event_type.FetchFromLink(self, global_var.timestamp+self.link_delay)
        heapq.heappush(global_var.queue, cur_event)
        pkt = self.buffer.popleft()
        self.cur_size -= pkt.size
        self.on_the_link.append(pkt)

        if self.buffer:
            expected_waiting_time = self.buffer[0].size * 8 / (self.link_rate * 1024 * 1024)
            cur_event = event_type.FetchFromBuffer(self, global_var.timestamp + expected_waiting_time)
            heapq.heappush(global_var.queue, cur_event)
            self.link_lock = True
        else:
            self.link_lock = False

        # plot function
        self.plot_link_buffer_time.append(global_var.timestamp)
        self.plot_link_buffer.append(self.cur_size / 1024)
        self.plot_link_rate_size += pkt.size

    def fetch_from_link(self):
        cur_pkt = self.on_the_link.popleft()
        self.end.receive_packet(cur_pkt, self)
